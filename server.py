#!/usr/bin/env python3
"""
Chat Server

This script runs a chat server that works with the updated chat client.
It supports both UDP and TCP protocols. The server listens on a specified host
and port, processes incoming messages, and responds to special commands.

Supported commands:
    {CONNECT}    - Logs a connection.
    {DISCONNECT} - Logs a disconnection (and in UDP mode, shuts down the server).
    {REGISTER}   - Sends a welcome message.
    {UNREGISTER} - Sends a goodbye message.
    {ALL}        - Echoes the message back.

Usage:
    python server.py          # Runs in UDP mode by default.
    python server.py tcp      # Runs in TCP mode.

Author: Sabneet Bains
License: MIT
"""

import sys
import os
from typing import List

from PyQt6 import QtCore, QtNetwork

# ---------------- UDP Server Implementation ----------------

def run_udp_server(host: str = "127.0.0.1", port: int = 33002) -> None:
    """
    Runs the chat server using the UDP protocol.
    
    This function creates a QCoreApplication and a QUdpSocket, binds the socket
    to the specified host and port, and connects the readyRead signal to the
    receive_message() function. It processes incoming datagrams and responds
    according to the message prefix.
    
    Parameters:
        host (str): The IP address to bind (default "127.0.0.1").
        port (int): The port number to bind (default 33002).
    """
    app = QtCore.QCoreApplication(sys.argv)
    udp_socket = QtNetwork.QUdpSocket()

    # Bind the UDP socket to the host and port.
    if not udp_socket.bind(QtNetwork.QHostAddress(host), port):
        print("UDP bind failed")
        sys.exit(1)

    def send_message(message: str, client: str, port: int) -> None:
        """
        Encodes and sends a message to the specified client and port via UDP.
        
        Parameters:
            message (str): The message to send.
            client (str): The client IP address (as a string).
            port (int): The destination port.
        """
        udp_socket.writeDatagram(message.encode(), QtNetwork.QHostAddress(client), port)

    def receive_message() -> None:
        """
        Reads and processes incoming datagrams.
        
        The function decodes incoming messages, checks for special command
        prefixes, and sends appropriate responses. For example, it sends a welcome
        message for "{REGISTER}" and a goodbye message for "{UNREGISTER}".
        """
        while udp_socket.hasPendingDatagrams():
            datagram, sender, sender_port = udp_socket.readDatagram(udp_socket.pendingDatagramSize())
            message = datagram.decode()
            sender_str = sender.toString()

            if message.startswith("{CONNECT}"):
                print(f"{sender_str}:{sender_port} has connected.")
            elif message.startswith("{DISCONNECT}"):
                print(f"{sender_str}:{sender_port} has disconnected.")
                udp_socket.close()
                QtCore.QCoreApplication.quit()
                break
            elif message.startswith("{REGISTER}"):
                reply = f"{{MSG}}Welcome {sender_str}!"
                send_message(reply, sender_str, sender_port)
            elif message.startswith("{UNREGISTER}"):
                reply = f"{{MSG}}Bye {sender_str}!"
                send_message(reply, sender_str, sender_port)
            elif message.startswith("{ALL}"):
                reply = f"{{MSG}} {message}"
                send_message(reply, sender_str, sender_port)

    # Connect the readyRead signal to our receive_message function.
    udp_socket.readyRead.connect(receive_message)
    print(f"UDP server running on {host}:{port}")
    sys.exit(app.exec())


# ---------------- TCP Server Implementation ----------------

class TcpConnectionHandler(QtCore.QObject):
    """
    Handles a single TCP connection for the chat server.
    
    This class wraps a QTcpSocket and connects its readyRead signal to a method
    that processes incoming data. It follows similar logic to the UDP handler.
    """
    def __init__(self, socket: QtNetwork.QTcpSocket) -> None:
        super().__init__()
        self.socket = socket
        self.socket.readyRead.connect(self.read_data)
        # When the socket disconnects, delete it.
        self.socket.disconnected.connect(self.socket.deleteLater)

    def read_data(self) -> None:
        """
        Reads and processes available data from the TCP socket.
        
        The function decodes data from the socket, checks the command prefix, and
        responds with an appropriate message using the same logic as in UDP.
        """
        while self.socket.bytesAvailable() > 0:
            data = self.socket.readAll().data().decode()
            peer = self.socket.peerAddress().toString()
            peer_port = self.socket.peerPort()
            if data.startswith("{CONNECT}"):
                print(f"{peer}:{peer_port} has connected.")
            elif data.startswith("{DISCONNECT}"):
                print(f"{peer}:{peer_port} has disconnected.")
                self.socket.disconnectFromHost()
            elif data.startswith("{REGISTER}"):
                reply = f"{{MSG}}Welcome {peer}!"
                self.socket.write(reply.encode())
            elif data.startswith("{UNREGISTER}"):
                reply = f"{{MSG}}Bye {peer}!"
                self.socket.write(reply.encode())
            elif data.startswith("{ALL}"):
                reply = f"{{MSG}} {data}"
                self.socket.write(reply.encode())


def run_tcp_server(host: str = "127.0.0.1", port: int = 33002) -> None:
    """
    Runs the chat server using the TCP protocol.
    
    This function creates a QCoreApplication and a QTcpServer. The server listens
    for incoming connections on the specified host and port. Each new connection is
    wrapped in a TcpConnectionHandler instance to process incoming data.
    
    Parameters:
        host (str): The IP address to listen on (default "127.0.0.1").
        port (int): The port number to listen on (default 33002).
    """
    app = QtCore.QCoreApplication(sys.argv)
    tcp_server = QtNetwork.QTcpServer()
    
    if not tcp_server.listen(QtNetwork.QHostAddress(host), port):
        print("TCP Server could not start")
        sys.exit(1)
    print(f"TCP server listening on {host}:{port}")

    # List to hold active connection handlers (to prevent garbage collection).
    connections: List[TcpConnectionHandler] = []

    def new_connection() -> None:
        """
        Called when a new TCP connection is pending.
        
        Retrieves pending connections and wraps each in a TcpConnectionHandler.
        """
        while tcp_server.hasPendingConnections():
            client_socket = tcp_server.nextPendingConnection()
            handler = TcpConnectionHandler(client_socket)
            connections.append(handler)

    tcp_server.newConnection.connect(new_connection)
    sys.exit(app.exec())


# ---------------- Main Entry Point ----------------

if __name__ == "__main__":
    # Determine protocol based on command-line argument (default UDP).
    protocol = "UDP"
    if len(sys.argv) > 1 and sys.argv[1].lower() == "tcp":
        protocol = "TCP"
    host = "127.0.0.1"
    port = 33002

    if protocol == "UDP":
        run_udp_server(host, port)
    else:
        run_tcp_server(host, port)
