from texte.chat_room import ChatRoom


def test_room_registers_users_and_sends_presence() -> None:
    room = ChatRoom()

    result = room.route("client-1", "{REGISTER}Alice", "127.0.0.1:1")

    assert [delivery.message for delivery in result.deliveries] == [
        "{MSG}Welcome Alice!",
        "{USERS}Alice",
    ]
    assert room.usernames == ["Alice"]


def test_room_rejects_duplicate_usernames() -> None:
    room = ChatRoom()

    room.route("client-1", "{REGISTER}Alice", "127.0.0.1:1")
    result = room.route("client-2", "{REGISTER}Alice", "127.0.0.1:2")

    assert result.deliveries[0].recipient == "client-2"
    assert result.deliveries[0].message == "{ERROR}Username 'Alice' is already signed in."


def test_room_broadcasts_to_registered_clients() -> None:
    room = ChatRoom()

    room.route("client-1", "{REGISTER}Alice", "127.0.0.1:1")
    room.route("client-2", "{REGISTER}Bob", "127.0.0.1:2")
    result = room.route("client-1", "{ALL}hello", "127.0.0.1:1")

    recipients = {delivery.recipient for delivery in result.deliveries}
    messages = [delivery.message for delivery in result.deliveries]

    assert recipients == {"client-1", "client-2"}
    assert all(message.startswith("{MSG}[") for message in messages)
    assert all(" Alice: hello" in message for message in messages)


def test_room_routes_direct_message_to_sender_and_target() -> None:
    room = ChatRoom()

    room.route("client-1", "{REGISTER}Alice", "127.0.0.1:1")
    room.route("client-2", "{REGISTER}Bob", "127.0.0.1:2")
    room.route("client-3", "{REGISTER}Cara", "127.0.0.1:3")
    result = room.route("client-1", "{TO}Bob|private ping", "127.0.0.1:1")

    recipients = {delivery.recipient for delivery in result.deliveries}

    assert recipients == {"client-1", "client-2"}
    assert all("Alice -> Bob: private ping" in delivery.message for delivery in result.deliveries)


def test_room_unregisters_and_sends_updated_presence() -> None:
    room = ChatRoom()

    room.route("client-1", "{REGISTER}Alice", "127.0.0.1:1")
    room.route("client-2", "{REGISTER}Bob", "127.0.0.1:2")
    result = room.route("client-2", "{UNREGISTER}Bob", "127.0.0.1:2")

    assert "{MSG}Bye Bob!" in [delivery.message for delivery in result.deliveries]
    assert "{USERS}Alice" in [delivery.message for delivery in result.deliveries]
    assert room.usernames == ["Alice"]
