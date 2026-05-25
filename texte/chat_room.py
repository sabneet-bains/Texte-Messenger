"""Shared registration and routing logic for Texte servers."""

from collections.abc import Hashable
from dataclasses import dataclass, field

from texte.protocol import (
    ALL,
    CONNECT,
    DISCONNECT,
    FILE,
    REGISTER,
    TO,
    UNREGISTER,
    chat_line,
    command_payload,
    direct_chat_line,
    display_name,
    error_message,
    parse_direct_message,
    parse_file_message,
    routed_file_message,
    server_message,
    users_message,
)


@dataclass(frozen=True, slots=True)
class Delivery:
    recipient: Hashable
    message: str


@dataclass(slots=True)
class RoutingResult:
    deliveries: list[Delivery] = field(default_factory=list)
    log_line: str | None = None
    close_connection: bool = False


class ChatRoom:
    """Track registered clients and route protocol messages."""

    def __init__(self) -> None:
        self._clients: dict[Hashable, str] = {}

    @property
    def usernames(self) -> list[str]:
        return sorted(self._clients.values(), key=str.casefold)

    def unregister(self, client_id: Hashable) -> RoutingResult:
        removed = self._clients.pop(client_id, None)
        if removed is None:
            return RoutingResult()
        return RoutingResult(deliveries=self._presence_deliveries())

    def route(self, client_id: Hashable, message: str, peer_name: str) -> RoutingResult:
        if message.startswith(CONNECT):
            return RoutingResult()

        if message.startswith(DISCONNECT):
            result = self.unregister(client_id)
            result.close_connection = True
            return result

        if message.startswith(REGISTER):
            return self._register(client_id, message, peer_name)

        if message.startswith(UNREGISTER):
            return self._unregister(client_id, message, peer_name)

        if message.startswith(ALL):
            return self._broadcast(client_id, message, peer_name)

        if message.startswith(TO):
            return self._direct(client_id, message, peer_name)

        if message.startswith(FILE):
            return self._file(client_id, message, peer_name)

        return RoutingResult()

    def _register(self, client_id: Hashable, message: str, peer_name: str) -> RoutingResult:
        name = display_name(message, REGISTER, peer_name)
        if not name:
            return self._error(client_id, "Choose a username before signing in.")

        owner = self._client_for_name(name)
        if owner is not None and owner != client_id:
            return self._error(client_id, f"Username '{name}' is already signed in.")

        self._clients[client_id] = name
        deliveries = [Delivery(client_id, server_message(f"Welcome {name}!"))]
        deliveries.extend(self._presence_deliveries())
        return RoutingResult(deliveries=deliveries)

    def _unregister(self, client_id: Hashable, message: str, peer_name: str) -> RoutingResult:
        name = self._clients.pop(client_id, display_name(message, UNREGISTER, peer_name))
        deliveries = [Delivery(client_id, server_message(f"Bye {name}!"))]
        deliveries.extend(self._presence_deliveries())
        return RoutingResult(deliveries=deliveries)

    def _broadcast(self, client_id: Hashable, message: str, peer_name: str) -> RoutingResult:
        text = command_payload(message, ALL)
        if not text:
            return self._error(client_id, "Write a message before sending.")
        sender = self._clients.get(client_id, peer_name)
        recipients = list(self._clients) or [client_id]
        line = server_message(chat_line(sender, text))
        return RoutingResult([Delivery(recipient, line) for recipient in recipients])

    def _direct(self, client_id: Hashable, message: str, peer_name: str) -> RoutingResult:
        direct = parse_direct_message(message)
        if direct is None:
            return self._error(client_id, "Choose a recipient and write a message.")

        sender = self._clients.get(client_id, peer_name)
        recipient = self._client_for_name(direct.recipient)
        if recipient is None:
            return self._error(client_id, f"User '{direct.recipient}' is not signed in.")

        line = server_message(direct_chat_line(sender, direct.recipient, direct.text))
        deliveries = [Delivery(recipient, line)]
        if recipient != client_id:
            deliveries.append(Delivery(client_id, line))
        return RoutingResult(deliveries)

    def _file(self, client_id: Hashable, message: str, peer_name: str) -> RoutingResult:
        parsed = parse_file_message(message)
        if parsed is None:
            return self._error(client_id, "Attachment could not be sent.")

        sender = self._clients.get(client_id, peer_name)
        routed = routed_file_message(sender, parsed.filename, parsed.data)

        if parsed.recipient == "ALL":
            recipients = list(self._clients) or [client_id]
        else:
            recipient = self._client_for_name(parsed.recipient)
            if recipient is None:
                return self._error(client_id, f"User '{parsed.recipient}' is not signed in.")
            recipients = [recipient]
            if recipient != client_id:
                recipients.append(client_id)

        return RoutingResult([Delivery(recipient, routed) for recipient in recipients])

    def _presence_deliveries(self) -> list[Delivery]:
        message = users_message(self.usernames)
        return [Delivery(client_id, message) for client_id in self._clients]

    def _client_for_name(self, name: str) -> Hashable | None:
        target = name.casefold()
        for client_id, username in self._clients.items():
            if username.casefold() == target:
                return client_id
        return None

    def _error(self, client_id: Hashable, message: str) -> RoutingResult:
        return RoutingResult([Delivery(client_id, error_message(message))])
