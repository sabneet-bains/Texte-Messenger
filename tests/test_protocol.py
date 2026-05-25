from datetime import datetime

from texte.protocol import (
    ALL,
    CONNECT,
    DISCONNECT,
    FIELD,
    REGISTER,
    TO,
    UNREGISTER,
    chat_line,
    chat_message,
    clean_chat_text,
    command_payload,
    direct_chat_line,
    display_text,
    display_name,
    file_message,
    frame_message,
    handle_server_message,
    message_has_chat_text,
    outgoing_payload,
    parse_direct_message,
    parse_file_delivery,
    parse_file_message,
    register_message,
    server_message,
    split_frames,
    timestamp,
    unregister_message,
    users_message,
    users_payload,
)


def test_server_message_round_trip() -> None:
    message = server_message("Welcome back")

    assert message == "{MSG}Welcome back"
    assert display_text(message) == "Welcome back"


def test_display_text_ignores_client_commands() -> None:
    assert display_text(CONNECT) is None


def test_chat_message_formats_recipient_and_text() -> None:
    assert chat_message("ALL", "hello") == "{ALL}hello"
    assert chat_message("Bob", "hello") == "{TO}Bob|hello"


def test_outgoing_payload_strips_field_marker_only() -> None:
    assert outgoing_payload(FIELD + chat_message("ALL", "hello")) == "{ALL}hello"
    assert outgoing_payload(REGISTER) == REGISTER


def test_registration_commands_include_usernames() -> None:
    assert register_message(" Hugo ") == "{REGISTER}Hugo"
    assert unregister_message(" Hugo ") == "{UNREGISTER}Hugo"


def test_command_payload_and_display_name() -> None:
    assert command_payload("{REGISTER}Hugo", REGISTER) == "Hugo"
    assert display_name(REGISTER, REGISTER, "127.0.0.1") == "127.0.0.1"


def test_chat_line_includes_timestamp_sender_and_text() -> None:
    now = datetime(2026, 5, 12, 9, 7)

    assert timestamp(now) == "09:07"
    assert chat_line("Hugo", "hello", now) == "[09:07] Hugo: hello"
    assert direct_chat_line("Hugo", "Bob", "hello", now) == "[09:07] Hugo -> Bob: hello"


def test_users_message_round_trip() -> None:
    message = users_message(["Bob", "Alice"])

    assert message == "{USERS}Alice,Bob"
    assert users_payload(message) == ["Alice", "Bob"]


def test_direct_message_parsing() -> None:
    parsed = parse_direct_message(TO + "Bob|hello")

    assert parsed is not None
    assert parsed.recipient == "Bob"
    assert parsed.text == "hello"
    assert parse_direct_message(TO + "Bob|") is None


def test_file_message_round_trip() -> None:
    message = file_message("Bob", "avatar|one.png", b"image-bytes")
    parsed = parse_file_message(message)
    delivery = parse_file_delivery(message)

    assert parsed is not None
    assert parsed.recipient == "Bob"
    assert parsed.filename == "avatar_one.png"
    assert parsed.data == b"image-bytes"
    assert delivery is not None
    assert delivery.sender == "Bob"


def test_tcp_frames_split_complete_messages_and_keep_remainder() -> None:
    encoded = frame_message("{REGISTER}Alice") + b"{ALL}hel"
    messages, remainder = split_frames(encoded.decode())

    assert messages == ["{REGISTER}Alice"]
    assert remainder == "{ALL}hel"


def test_chat_text_validation() -> None:
    assert clean_chat_text(" hello\nthere ") == "hello there"
    assert message_has_chat_text("{ALL}hello")
    assert message_has_chat_text("{TO}Bob|hello")
    assert not message_has_chat_text("{ALL}   ")


def test_connect_logs_without_reply() -> None:
    result = handle_server_message(CONNECT, "127.0.0.1", 33002)

    assert result.reply is None
    assert result.log_line == "127.0.0.1:33002 has connected."
    assert not result.close_connection
    assert not result.stop_server


def test_disconnect_logs_and_closes() -> None:
    result = handle_server_message(DISCONNECT, "127.0.0.1", 33002)

    assert result.reply is None
    assert result.log_line == "127.0.0.1:33002 has disconnected."
    assert result.close_connection
    assert not result.stop_server


def test_register_replies_with_welcome_name() -> None:
    result = handle_server_message(REGISTER + "Hugo", "127.0.0.1", 33002)

    assert result.reply == "{MSG}Welcome Hugo!"


def test_unregister_replies_with_goodbye_name() -> None:
    result = handle_server_message(UNREGISTER + "Hugo", "127.0.0.1", 33002)

    assert result.reply == "{MSG}Bye Hugo!"


def test_all_message_replies_with_timestamped_chat_line() -> None:
    result = handle_server_message(ALL + "hello", "127.0.0.1", 33002)

    assert result.reply is not None
    assert result.reply.startswith("{MSG}[")
    assert result.reply.endswith("] 127.0.0.1: hello") or " 127.0.0.1: hello" in result.reply


def test_unknown_message_has_no_effect() -> None:
    result = handle_server_message("hello", "127.0.0.1", 33002)

    assert result.reply is None
    assert result.log_line is None
    assert not result.close_connection
    assert not result.stop_server
