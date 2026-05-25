#!/usr/bin/env python3
"""
Chat Server

This script runs the Texte chat server. It listens on localhost by default and
responds to the small command-prefixed messages sent by client.py.

Supported commands:
    {CONNECT}    - Logs a connection.
    {DISCONNECT} - Logs a disconnection and removes registration.
    {REGISTER}   - Registers a display name and sends a welcome message.
    {UNREGISTER} - Sends a goodbye message.
    {ALL}        - Broadcasts a timestamped message to registered clients.
    {TO}         - Routes a direct message to one registered user.
    {FILE}       - Routes small TCP file attachments.

Usage:
    python server.py
    python server.py tcp
    python server.py --protocol tcp --port 33003

Author: Sabneet Bains
License: MIT
"""

import argparse
import sys
from typing import TypeGuard

from PyQt6 import QtCore, QtNetwork

from texte.chat_room import ChatRoom, Delivery, RoutingResult
from texte.protocol import FILE, error_message, frame_message, split_frames


def run_udp_server(host: str = "127.0.0.1", port: int = 33002) -> None:
    """Run the UDP server."""
    app = QtCore.QCoreApplication(sys.argv)
    udp_socket = QtNetwork.QUdpSocket()
    room = ChatRoom()

    if not udp_socket.bind(QtNetwork.QHostAddress(host), port):
        print("UDP bind failed")
        sys.exit(1)

    def send_delivery(delivery: Delivery) -> None:
        recipient = delivery.recipient
        if not _is_udp_recipient(recipient):
            return
        client_host, client_port = recipient
        udp_socket.writeDatagram(
            delivery.message.encode(),
            QtNetwork.QHostAddress(client_host),
            client_port,
        )

    def apply_result(result: RoutingResult) -> None:
        if result.log_line:
            print(result.log_line)
        for delivery in result.deliveries:
            send_delivery(delivery)

    def receive_message() -> None:
        while udp_socket.hasPendingDatagrams():
            datagram, sender, sender_port = udp_socket.readDatagram(
                udp_socket.pendingDatagramSize()
            )
            if sender is None:
                continue
            sender_str = sender.toString()
            peer = (sender_str, sender_port)
            peer_label = f"{sender_str}:{sender_port}"
            message = datagram.decode().strip()
            if message.startswith(FILE):
                udp_socket.writeDatagram(
                    error_message("Attachments require TCP.").encode(),
                    QtNetwork.QHostAddress(sender_str),
                    sender_port,
                )
                continue
            apply_result(room.route(peer, message, peer_label))

    udp_socket.readyRead.connect(receive_message)
    print(f"UDP server running on {host}:{port}")
    sys.exit(app.exec())


class TcpConnectionHandler(QtCore.QObject):
    """Handle one newline-framed TCP client connection."""

    def __init__(
        self,
        socket: QtNetwork.QTcpSocket,
        room: ChatRoom,
        connections: dict[QtNetwork.QTcpSocket, "TcpConnectionHandler"],
        on_empty_connections,
    ) -> None:
        super().__init__()
        self.socket = socket
        self.room = room
        self.connections = connections
        self.on_empty_connections = on_empty_connections
        self.buffer = ""
        self.socket.readyRead.connect(self.read_data)
        self.socket.disconnected.connect(self.close)
        self.socket.disconnected.connect(self.socket.deleteLater)

    @property
    def peer_label(self) -> str:
        return f"{self.socket.peerAddress().toString()}:{self.socket.peerPort()}"

    def write(self, message: str) -> None:
        self.socket.write(frame_message(message))

    def close(self) -> None:
        result = self.room.unregister(self.socket)
        self.connections.pop(self.socket, None)
        self._apply_result(result)
        if not self.connections:
            self.on_empty_connections()

    def read_data(self) -> None:
        self.buffer += self.socket.readAll().data().decode()
        messages, self.buffer = split_frames(self.buffer)
        for message in messages:
            result = self.room.route(self.socket, message, self.peer_label)
            self._apply_result(result)
            if result.close_connection:
                self.socket.disconnectFromHost()
                break

    def _apply_result(self, result: RoutingResult) -> None:
        if result.log_line:
            print(result.log_line)
        for delivery in result.deliveries:
            recipient = delivery.recipient
            if not isinstance(recipient, QtNetwork.QTcpSocket):
                continue
            handler = self.connections.get(recipient)
            if handler is not None:
                handler.write(delivery.message)


def run_tcp_server(host: str = "127.0.0.1", port: int = 33002) -> None:
    """Run the TCP server."""
    app = QtCore.QCoreApplication(sys.argv)
    tcp_server = QtNetwork.QTcpServer()
    room = ChatRoom()

    if not tcp_server.listen(QtNetwork.QHostAddress(host), port):
        print("TCP Server could not start")
        sys.exit(1)
    print(f"TCP server listening on {host}:{port}")

    connections: dict[QtNetwork.QTcpSocket, TcpConnectionHandler] = {}

    def stop_when_idle() -> None:
        if connections:
            return
        tcp_server.close()
        app.quit()

    def new_connection() -> None:
        while tcp_server.hasPendingConnections():
            client_socket = tcp_server.nextPendingConnection()
            if client_socket is None:
                continue
            handler = TcpConnectionHandler(client_socket, room, connections, stop_when_idle)
            connections[client_socket] = handler

    tcp_server.newConnection.connect(new_connection)
    sys.exit(app.exec())


def _is_udp_recipient(value: object) -> TypeGuard[tuple[str, int]]:
    return (
        isinstance(value, tuple)
        and len(value) == 2
        and isinstance(value[0], str)
        and isinstance(value[1], int)
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Texte UDP/TCP chat server.")
    parser.add_argument(
        "mode",
        nargs="?",
        choices=["udp", "tcp"],
        help="Transport mode. Kept for compatibility with `python server.py tcp`.",
    )
    parser.add_argument(
        "--protocol",
        choices=["udp", "tcp"],
        help="Transport mode. Overrides the positional mode when provided.",
    )
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=33002)
    return parser.parse_args(argv)


def main() -> None:
    """Start the chat server from command-line arguments."""
    args = parse_args(sys.argv[1:])
    protocol = args.protocol or args.mode or "udp"

    if protocol == "udp":
        run_udp_server(args.host, args.port)
    else:
        run_tcp_server(args.host, args.port)


if __name__ == "__main__":
    main()
