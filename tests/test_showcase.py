import os
import sys

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("TEXTE_DISABLE_AUTO_START", "1")

from PyQt6 import QtWidgets

from texte.client import ChatClient
from texte.showcase import (
    ShowcaseConfig,
    ShowcaseProfile,
    build_config,
    default_profiles,
    parse_args,
    seed_client,
    server_command,
)


def test_parse_args_defaults_to_tcp() -> None:
    config = build_config(parse_args([]))

    assert config == ShowcaseConfig()


def test_server_command_targets_texte_server() -> None:
    command = server_command(ShowcaseConfig(protocol="tcp", host="127.0.0.1", port=33042))

    assert command[:3] == [sys.executable, "-m", "texte.server"]
    assert command[3:9] == ["--protocol", "tcp", "--host", "127.0.0.1", "--port", "33042"]


def test_seed_client_preconfigures_identity_and_transport() -> None:
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)

    client = ChatClient()
    seed_client(
        client,
        ShowcaseProfile("Alice", "user1", "Texte Showcase - Alice"),
        ShowcaseConfig(protocol="tcp", host="127.0.0.1", port=33042),
    )

    assert not client.auto_server_checkbox.isChecked()
    assert client.host_address.text() == "127.0.0.1"
    assert client.port_number.text() == "33042"
    assert client.protocol_selector.currentText() == "TCP"
    assert client.username.text() == "Alice"
    assert client.user_avatar.objectName() == "user1"
    assert client.windowTitle() == "Texte Showcase - Alice"
    assert client._seeded_onboarding is True

    client.close()
    assert app is not None


def test_default_profiles_cover_alice_and_bob() -> None:
    profiles = default_profiles()

    assert [profile.username for profile in profiles] == ["Alice", "Bob"]
    assert [profile.avatar for profile in profiles] == ["user1", "user2"]
