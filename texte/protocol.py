"""Message helpers for the Texte client and server."""

import base64
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

CONNECT = "{CONNECT}"
DISCONNECT = "{DISCONNECT}"
REGISTER = "{REGISTER}"
UNREGISTER = "{UNREGISTER}"
ALL = "{ALL}"
TO = "{TO}"
USERS = "{USERS}"
FILE = "{FILE}"
ERROR = "{ERROR}"
FIELD = "{FIELD}"
SERVER_MESSAGE = "{MSG}"

DIRECT_SEPARATOR = "|"
MAX_FILE_BYTES = 1_000_000


@dataclass(frozen=True, slots=True)
class ServerResult:
    reply: str | None = None
    log_line: str | None = None
    close_connection: bool = False
    stop_server: bool = False


@dataclass(frozen=True, slots=True)
class DirectMessage:
    recipient: str
    text: str


@dataclass(frozen=True, slots=True)
class FileMessage:
    recipient: str
    filename: str
    data: bytes


@dataclass(frozen=True, slots=True)
class FileDelivery:
    sender: str
    filename: str
    data: bytes


def server_message(text: str) -> str:
    return f"{SERVER_MESSAGE}{text}"


def error_message(text: str) -> str:
    return f"{ERROR}{text}"


def users_message(usernames: list[str]) -> str:
    return f"{USERS}{','.join(sorted(usernames, key=str.casefold))}"


def register_message(username: str) -> str:
    return f"{REGISTER}{normalize_username(username)}"


def unregister_message(username: str) -> str:
    return f"{UNREGISTER}{normalize_username(username)}"


def normalize_username(username: str) -> str:
    return " ".join(username.strip().split())


def clean_chat_text(text: str) -> str:
    return " ".join(text.strip().splitlines())


def safe_filename(filename: str) -> str:
    name = Path(filename).name.strip().replace(DIRECT_SEPARATOR, "_")
    return name or "attachment"


def chat_message(recipient: str, text: str) -> str:
    clean_text = clean_chat_text(text)
    if recipient == "ALL":
        return f"{ALL}{clean_text}"
    return f"{TO}{normalize_username(recipient)}{DIRECT_SEPARATOR}{clean_text}"


def outgoing_payload(message: str) -> str:
    return message.removeprefix(FIELD)


def display_text(message: str) -> str | None:
    if message.startswith(SERVER_MESSAGE):
        return message.removeprefix(SERVER_MESSAGE)
    if message.startswith(ERROR):
        return message.removeprefix(ERROR)
    return None


def users_payload(message: str) -> list[str] | None:
    if not message.startswith(USERS):
        return None
    payload = message.removeprefix(USERS)
    if not payload:
        return []
    return [name for name in payload.split(",") if name]


def command_payload(message: str, command: str) -> str:
    return message.removeprefix(command).strip()


def display_name(message: str, command: str, fallback: str) -> str:
    name = normalize_username(command_payload(message, command))
    return name or fallback


def parse_direct_message(message: str) -> DirectMessage | None:
    if not message.startswith(TO):
        return None
    payload = message.removeprefix(TO)
    if DIRECT_SEPARATOR not in payload:
        return None
    recipient, text = payload.split(DIRECT_SEPARATOR, 1)
    recipient = normalize_username(recipient)
    text = clean_chat_text(text)
    if not recipient or not text:
        return None
    return DirectMessage(recipient, text)


def file_message(recipient: str, filename: str, data: bytes) -> str:
    encoded = base64.b64encode(data).decode("ascii")
    return f"{FILE}{normalize_username(recipient)}{DIRECT_SEPARATOR}{safe_filename(filename)}{DIRECT_SEPARATOR}{encoded}"


def routed_file_message(sender: str, filename: str, data: bytes) -> str:
    encoded = base64.b64encode(data).decode("ascii")
    return f"{FILE}{normalize_username(sender)}{DIRECT_SEPARATOR}{safe_filename(filename)}{DIRECT_SEPARATOR}{encoded}"


def parse_file_message(message: str) -> FileMessage | None:
    if not message.startswith(FILE):
        return None
    payload = message.removeprefix(FILE)
    parts = payload.split(DIRECT_SEPARATOR, 2)
    if len(parts) != 3:
        return None
    recipient, filename, encoded = parts
    recipient = normalize_username(recipient)
    filename = safe_filename(filename)
    if not recipient or not encoded:
        return None
    try:
        data = base64.b64decode(encoded.encode("ascii"), validate=True)
    except (ValueError, UnicodeEncodeError):
        return None
    if not data or len(data) > MAX_FILE_BYTES:
        return None
    return FileMessage(recipient, filename, data)


def parse_file_delivery(message: str) -> FileDelivery | None:
    parsed = parse_file_message(message)
    if parsed is None:
        return None
    return FileDelivery(parsed.recipient, parsed.filename, parsed.data)


def timestamp(now: datetime | None = None) -> str:
    moment = now or datetime.now()
    return moment.strftime("%H:%M")


def chat_line(sender: str, text: str, now: datetime | None = None) -> str:
    return f"[{timestamp(now)}] {sender}: {text}"


def direct_chat_line(sender: str, recipient: str, text: str, now: datetime | None = None) -> str:
    return f"[{timestamp(now)}] {sender} -> {recipient}: {text}"


def frame_message(message: str) -> bytes:
    return f"{message.rstrip(chr(10)).rstrip(chr(13))}\n".encode()


def split_frames(buffer: str) -> tuple[list[str], str]:
    parts = buffer.splitlines(keepends=True)
    messages: list[str] = []
    remainder = ""

    for part in parts:
        if part.endswith(("\n", "\r")):
            messages.append(part.strip())
        else:
            remainder = part

    return [message for message in messages if message], remainder


def message_has_chat_text(message: str) -> bool:
    if message.startswith(ALL):
        return bool(clean_chat_text(command_payload(message, ALL)))
    direct = parse_direct_message(message)
    return direct is not None and bool(direct.text)


def handle_server_message(message: str, peer: str, peer_port: int) -> ServerResult:
    peer_label = f"{peer}:{peer_port}"

    if message.startswith(CONNECT):
        return ServerResult(log_line=f"{peer_label} has connected.")

    if message.startswith(DISCONNECT):
        return ServerResult(
            log_line=f"{peer_label} has disconnected.",
            close_connection=True,
        )

    if message.startswith(REGISTER):
        name = display_name(message, REGISTER, peer)
        return ServerResult(reply=server_message(f"Welcome {name}!"))

    if message.startswith(UNREGISTER):
        name = display_name(message, UNREGISTER, peer)
        return ServerResult(reply=server_message(f"Bye {name}!"))

    if message.startswith(ALL):
        text = command_payload(message, ALL)
        return ServerResult(reply=server_message(chat_line(peer, text)))

    direct = parse_direct_message(message)
    if direct is not None:
        return ServerResult(
            reply=server_message(direct_chat_line(peer, direct.recipient, direct.text))
        )

    return ServerResult()
