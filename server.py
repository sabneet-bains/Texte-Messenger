import sys
import os
from typing import List

from PyQt6 import QtCore, QtNetwork

# ---------------- UDP Server Implementation ----------------

def run_udp_server(host: str = "127.0.0.1", port: int = 33002) -> None:
    app = QtCore.QCoreApplication(sys.argv)
    udp_socket = QtNetwork.QUdpSocket()

    if not udp_socket.bind(QtNetwork.QHostAddress(host), port):
        print("UDP bind failed")
        sys.exit(1)

    def send_message(message: str, client: str, port: int) -> None:
        udp_socket.writeDatagram(message.encode(), QtNetwork.QHostAddress(client), port)

    def receive_message() -> None:
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

    udp_socket.readyRead.connect(receive_message)
    print(f"UDP server running on {host}:{port}")
    sys.exit(app.exec())


# ---------------- TCP Server Implementation ----------------

class TcpConnectionHandler(QtCore.QObject):
    """Handles a single TCP connection."""
    def __init__(self, socket: QtNetwork.QTcpSocket) -> None:
        super().__init__()
        self.socket = socket
        self.socket.readyRead.connect(self.read_data)
        self.socket.disconnected.connect(self.socket.deleteLater)

    def read_data(self) -> None:
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
    app = QtCore.QCoreApplication(sys.argv)
    tcp_server = QtNetwork.QTcpServer()
    if not tcp_server.listen(QtNetwork.QHostAddress(host), port):
        print("TCP Server could not start")
        sys.exit(1)
    print(f"TCP server listening on {host}:{port}")

    # Keep references to connection handlers to prevent garbage collection.
    connections: List[TcpConnectionHandler] = []

    def new_connection() -> None:
        while tcp_server.hasPendingConnections():
            client_socket = tcp_server.nextPendingConnection()
            handler = TcpConnectionHandler(client_socket)
            connections.append(handler)

    tcp_server.newConnection.connect(new_connection)
    sys.exit(app.exec())


# ---------------- Main ----------------

if __name__ == "__main__":
    protocol = "UDP"
    if len(sys.argv) > 1 and sys.argv[1].lower() == "tcp":
        protocol = "TCP"
    host = "127.0.0.1"
    port = 33002

    if protocol == "UDP":
        run_udp_server(host, port)
    else:
        run_tcp_server(host, port)
