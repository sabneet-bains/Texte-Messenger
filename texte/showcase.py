"""Launch a ready-to-use Texte showcase session."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Sequence

from PyQt6 import QtGui, QtNetwork, QtWidgets

from texte.client import ChatClient
from texte.protocol import chat_message

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 33042
DEFAULT_PROTOCOL: Literal["tcp", "udp"] = "tcp"
SHOWCASE_TITLE = "Texte Showcase"


@dataclass(frozen=True, slots=True)
class ShowcaseConfig:
    """Connection settings for the showcase session."""

    protocol: Literal["tcp", "udp"] = DEFAULT_PROTOCOL
    host: str = DEFAULT_HOST
    port: int = DEFAULT_PORT


@dataclass(frozen=True, slots=True)
class ShowcaseProfile:
    """Identity and window metadata for one showcase client."""

    username: str
    avatar: str
    window_title: str


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Launch the Texte showcase session.")
    parser.add_argument("--protocol", choices=["tcp", "udp"], default=DEFAULT_PROTOCOL)
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    return parser.parse_args(list(argv) if argv is not None else sys.argv[1:])


def build_config(args: argparse.Namespace) -> ShowcaseConfig:
    return ShowcaseConfig(
        protocol=args.protocol,
        host=args.host,
        port=args.port,
    )


def default_profiles() -> tuple[ShowcaseProfile, ShowcaseProfile]:
    return (
        ShowcaseProfile("Alice", "user1", f"{SHOWCASE_TITLE} - Alice"),
        ShowcaseProfile("Bob", "user2", f"{SHOWCASE_TITLE} - Bob"),
    )


def server_command(config: ShowcaseConfig) -> list[str]:
    return [
        sys.executable,
        "-m",
        "texte.server",
        "--protocol",
        config.protocol,
        "--host",
        config.host,
        "--port",
        str(config.port),
    ]


def launch_server(config: ShowcaseConfig) -> subprocess.Popen[bytes]:
    return subprocess.Popen(server_command(config))


def terminate_server(process: subprocess.Popen[bytes]) -> None:
    if process.poll() is not None:
        return
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5)


def wait_for_server(
    config: ShowcaseConfig,
    process: subprocess.Popen[bytes],
    timeout: float = 5.0,
) -> None:
    deadline = time.monotonic() + timeout
    ready_at = time.monotonic() + 1.0

    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError(
                f"Showcase server exited with code {process.returncode} before it became ready."
            )
        if time.monotonic() >= ready_at:
            return
        time.sleep(0.1)
    raise RuntimeError(f"Timed out waiting for the showcase server on {config.host}:{config.port}.")


def seed_client(
    client: ChatClient,
    profile: ShowcaseProfile,
    config: ShowcaseConfig,
) -> None:
    client.auto_server_checkbox.setChecked(False)
    client.host_address.setText(config.host)
    client.port_number.setText(str(config.port))
    client.protocol_selector.setCurrentText(config.protocol.upper())
    client._use_protocol(config.protocol.upper())
    client.username.setText(profile.username)
    client.choose_avatar(profile.avatar)
    client._seeded_onboarding = True
    client.setWindowTitle(profile.window_title)
    client.resize(920, 820)


def connect_client(client: ChatClient) -> None:
    client.server_button.setChecked(True)
    client.connect_client()
    if not client.server_connected:
        raise RuntimeError("Showcase client failed to connect.")
    client.sign_in_button.setChecked(True)
    client.sign_in()
    if not client.user_signed_in:
        raise RuntimeError("Showcase client failed to sign in.")


def pump_events(app: QtWidgets.QApplication, iterations: int = 6, delay: float = 0.05) -> None:
    for _ in range(iterations):
        app.processEvents()
        time.sleep(delay)


def wait_for_socket_ready(
    client: ChatClient,
    app: QtWidgets.QApplication,
    timeout: float = 5.0,
) -> None:
    qt_socket = client.socket
    if not isinstance(qt_socket, QtNetwork.QTcpSocket):
        return

    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        app.processEvents()
        if qt_socket.state() == QtNetwork.QAbstractSocket.SocketState.ConnectedState:
            return
        time.sleep(0.05)
    raise RuntimeError("Timed out waiting for the TCP showcase client to connect.")


def tile_windows(clients: Sequence[QtWidgets.QWidget]) -> None:
    screen = QtGui.QGuiApplication.primaryScreen()
    if screen is None:
        return

    geometry = screen.availableGeometry()
    gap = 24
    count = max(1, len(clients))
    width = max(700, (geometry.width() - gap * (count + 1)) // count)
    height = max(700, geometry.height() - (gap * 2))

    for index, window in enumerate(clients):
        x = geometry.left() + gap + index * (width + gap)
        y = geometry.top() + gap
        window.resize(min(width, 980), min(height, 920))
        window.move(max(geometry.left() + gap, x), y)


def send_demo_messages(clients: Sequence[ChatClient]) -> None:
    alice, _bob = clients
    alice.send_message(chat_message("ALL", "hello"))
    alice.send_message(chat_message("Bob", "private ping"))


def select_useful_conversations(clients: Sequence[ChatClient]) -> None:
    alice, bob = clients
    alice._set_active_recipient("Bob")
    bob._set_active_recipient("Alice")
    alice.message_field.setFocus()


def main(argv: Sequence[str] | None = None) -> int:
    os.environ["TEXTE_DISABLE_AUTO_START"] = "1"
    config = build_config(parse_args(argv))
    server = launch_server(config)
    closed = False

    def shutdown() -> None:
        nonlocal closed
        if closed:
            return
        closed = True
        terminate_server(server)

    try:
        wait_for_server(config, server)
        app = QtWidgets.QApplication([Path(sys.argv[0]).name])
        profiles = default_profiles()
        clients = [
            ChatClient(),
            ChatClient(),
        ]

        for client, profile in zip(clients, profiles, strict=True):
            seed_client(client, profile, config)
            connect_client(client)
            wait_for_socket_ready(client, app)

        pump_events(app)
        select_useful_conversations(clients)
        send_demo_messages(clients)
        pump_events(app)
        tile_windows(clients)

        for client in clients:
            client.show()
            client.raise_()

        clients[0].raise_()
        clients[0].activateWindow()
        clients[0].message_field.setFocus()
        app.aboutToQuit.connect(shutdown)
        return app.exec()
    finally:
        shutdown()


if __name__ == "__main__":
    raise SystemExit(main())
