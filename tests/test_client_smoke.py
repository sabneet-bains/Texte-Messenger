import os
import sys

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("TEXTE_DISABLE_AUTO_START", "1")

from PyQt6 import QtCore, QtWidgets

from texte.client import ChatClient


def test_client_constructs_with_messages_shell() -> None:
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)

    client = ChatClient()
    client.resize(1280, 720)

    assert client.windowTitle() == "texte"
    assert client.windowFlags() & QtCore.Qt.WindowType.Window
    assert client.protocol_selector.count() == 2
    assert [client.protocol_selector.itemText(index) for index in range(2)] == ["TCP", "UDP"]
    assert [client.chat_theme.itemText(index) for index in range(2)] == ["Light", "Dark"]
    assert client.chat_theme.currentText() in {"Light", "Dark"}
    assert client.host_address.text() == "127.0.0.1"
    assert client.port_number.text() == "33002"
    assert client.server_button.text() == "Connect"
    assert client.sign_in_button.text() == "Sign in"
    assert client.auto_server_checkbox.isChecked()
    assert client.setup_sheet.isHidden()
    assert client.profile_popup.isHidden()
    assert client.avatar_selector_panel.isHidden()
    assert client.setup_sheet.height() >= client.setup_content.sizeHint().height()
    first_conversation = client.conversation_list.item(0)
    assert first_conversation is not None
    assert first_conversation.text() == "ALL"
    assert client.conversation_list.itemWidget(first_conversation) is not None
    assert client.composer_panel is not None
    assert client.composer_shell is not None
    assert client.attach_button is not None
    assert client.message_field is not None
    assert client.emoji_button is not None
    assert client.username.text() == ""
    assert client.header_username.text() == "Pick profile"
    assert not client.sign_in_button.isEnabled()

    client.server_connected = True
    client._update_profile_action_state()
    client.username.setText("Alex")
    assert client.sign_in_button.isEnabled()

    client.close()
    assert app is not None


def test_client_layout_survives_key_window_sizes() -> None:
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)

    client = ChatClient()
    for width, height in [(760, 520), (1180, 720), (1500, 900)]:
        client.resize(width, height)
        assert client.minimumWidth() <= width
        assert client.minimumHeight() <= height
        assert not client.setup_button.isHidden()
        assert not client.conversation_list.isHidden()
        assert not client.composer_panel.isHidden()

    client.close()
    assert app is not None


def test_setup_sheet_and_action_labels_toggle() -> None:
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)

    client = ChatClient()
    client._toggle_setup_sheet(True)
    assert not client.setup_sheet.isHidden()

    client.server_connected = True
    client.user_signed_in = True
    client.server_button.setChecked(True)
    client.sign_in_button.setChecked(True)
    client.server_button.setText("Disconnect")
    client.sign_in_button.setText("Sign out")
    client.username.setText("Local 1234")
    client.active_avatar_name = "user1"
    client._refresh_status_text()

    assert client.server_button.text() == "Disconnect"
    assert client.sign_in_button.text() == "Sign out"
    assert client.header_username.text() == "Local 1234"

    assert client.profile_popup.isHidden()
    client.toggle_profile_popup()
    assert not client.profile_popup.isHidden()

    client.close()
    assert app is not None


def test_protocol_cannot_switch_while_connected() -> None:
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)

    client = ChatClient()
    client.server_connected = True
    client.protocol_selector.setCurrentText("TCP")
    client._sync_protocol_buttons("TCP")
    client._set_protocol_controls_enabled(False)

    client._select_protocol("UDP")

    assert client.protocol_selector.currentText() == "TCP"
    assert client.protocol_tcp_button.isChecked()
    assert not client.protocol_udp_button.isChecked()
    assert not client.protocol_tcp_button.isEnabled()
    assert not client.protocol_udp_button.isEnabled()

    client.server_connected = False
    client._set_protocol_controls_enabled(True)
    assert client.protocol_tcp_button.isEnabled()
    assert client.protocol_udp_button.isEnabled()

    client.close()
    assert app is not None


def test_auto_local_session_starts_only_for_tcp_and_auto_mode() -> None:
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)

    client = ChatClient()
    client.auto_server_checkbox.setChecked(False)
    client.start_local_session()
    assert not client.server_connected

    client.auto_server_checkbox.setChecked(True)
    client.protocol_selector.setCurrentText("UDP")
    client.start_local_session()
    assert not client.server_connected

    client.close()
    assert app is not None


def test_client_message_rows_are_distinct_and_selectable() -> None:
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)

    client = ChatClient()
    client.username.setText("Hugo")
    client._add_chat_text("Welcome Hugo!", "system")
    client._add_chat_text("[12:00] Hugo: hello", "outgoing")
    client._add_chat_text("[12:01] Jam: hi", "incoming")

    assert client.chat_log.count() == 3
    for index in range(client.chat_log.count()):
        container = client.chat_log.itemWidget(client.chat_log.item(index))
        assert container is not None
        labels = container.findChildren(QtWidgets.QLabel)
        assert labels
        assert any(
            label.textInteractionFlags() & QtCore.Qt.TextInteractionFlag.TextSelectableByMouse
            for label in labels
        )

    client.close()
    assert app is not None


def test_direct_messages_route_to_their_own_conversation() -> None:
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)

    client = ChatClient()
    client.username.setText("Local 1111")

    outgoing_kind, outgoing_conversation = client._message_route(
        "[12:00] Local 1111 -> Local 2222: hey"
    )
    incoming_kind, incoming_conversation = client._message_route(
        "[12:01] Local 2222 -> Local 1111: yo"
    )

    assert outgoing_kind == "outgoing"
    assert outgoing_conversation == "Local 2222"
    assert incoming_kind == "incoming"
    assert incoming_conversation == "Local 2222"

    client.close()
    assert app is not None


def test_message_reaction_popup_can_open_without_crashing() -> None:
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)

    client = ChatClient()
    client.show()
    client._add_chat_text("[12:00] Alice: hello", "incoming", conversation="ALL")

    item = client.chat_log.item(0)
    assert item is not None
    container = client.chat_log.itemWidget(item)
    assert container is not None
    bubble = container.findChild(QtWidgets.QFrame, "Message_Bubble")
    assert bubble is not None

    client._show_message_action_popup(
        bubble,
        entry={"type": "text", "text": "[12:00] Alice: hello", "kind": "incoming", "reactions": []},
        sender="Alice",
        conversation="ALL",
    )
    app.processEvents()

    assert client.reaction_bar_popup is not None
    assert client.reaction_bar_popup.isVisible()
    assert client.message_options_popup is not None
    assert client.message_options_popup.isVisible()

    client.close()
    assert app is not None


def test_client_file_delivery_adds_file_card(tmp_path) -> None:
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)

    client = ChatClient()
    client.download_dir = tmp_path
    client._save_file_delivery("Alice", "demo.txt", b"payload")

    assert client.chat_log.count() == 1
    container = client.chat_log.itemWidget(client.chat_log.item(0))
    assert container is not None
    assert container.findChild(QtWidgets.QFrame, "File_Card") is not None
    assert (tmp_path / "demo.txt").exists()

    client.close()
    assert app is not None


def test_client_avatar_selector_updates_visible_avatar() -> None:
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)

    client = ChatClient()
    assert client.avatar_selector_widget.count() == 3
    client.avatar_selector_panel.hide()
    client.open_avatar_selector()

    assert not client.avatar_selector_panel.isHidden()
    assert not client.avatar_previous_button.isEnabled()
    assert client.avatar_next_button.isEnabled()

    client.next_avatar_page()
    assert client.avatar_selector_widget.currentIndex() == 1
    assert client.avatar_previous_button.isEnabled()

    client.choose_avatar("user12")
    assert client.user_avatar.objectName() == "user12"
    assert client.avatar_selector_panel.isHidden()
    assert not client.user_avatar.isChecked()


def test_client_commits_username_rename_while_signed_in() -> None:
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)

    client = ChatClient()
    client.server_connected = True
    client.user_signed_in = True
    client.active_username = "Hugo"
    client.active_avatar_name = "user1"
    client.username.setText("Alex")

    messages: list[str] = []
    client.send_message = lambda message, host=None, port=None: messages.append(message)  # type: ignore[assignment]

    client._commit_username_change()

    assert messages == ["{UNREGISTER}Hugo", "{REGISTER}Alex"]
    assert client.active_username == "Alex"
    assert client.header_username.text() == "Alex"

    client.close()
    assert app is not None


def test_conversation_list_updates_from_presence_and_selects_recipient() -> None:
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)

    client = ChatClient()
    client.username.setText("Hugo")
    client._update_users(["Hugo", "Jam", "Alice"])

    conversations = []
    for index in range(3):
        item = client.conversation_list.item(index)
        assert item is not None
        conversations.append(item.text())
    assert conversations == ["ALL", "Jam", "Alice"]
    client.conversation_list.setCurrentRow(1)
    assert client.chat_selector.currentText() == "Jam"
    assert client.chat_title.text() == "Jam"
    assert client.chat_header_avatar.text() == "J"

    client.close()
    assert app is not None


def test_theme_override_buttons_switch_theme() -> None:
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)

    client = ChatClient()
    client._apply_theme_preference("Dark")
    assert client.chat_theme.currentText() == "Dark"
    assert client.theme_dark_button.isChecked()
    assert not client.theme_light_button.isChecked()

    client._apply_theme_preference("Light")
    assert client.chat_theme.currentText() == "Light"
    assert client.theme_light_button.isChecked()
    assert not client.theme_dark_button.isChecked()

    client.close()
    assert app is not None


def test_start_local_session_uses_selected_udp_protocol() -> None:
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)

    client = ChatClient()
    client.auto_server_checkbox.setChecked(True)
    client.protocol_selector.setCurrentText("UDP")

    calls: list[tuple[str, str, int]] = []

    def fake_start(protocol: str, host: str, port: int) -> None:
        calls.append((protocol, host, port))

    client._start_owned_server = fake_start  # type: ignore[method-assign]
    client._connect_and_sign_in = lambda host, port, protocol=None: None  # type: ignore[assignment]
    client.start_local_session()

    assert calls == [("udp", "127.0.0.1", 33002)]

    client.close()
    assert app is not None
