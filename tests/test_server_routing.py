import socket
import subprocess
import sys
import time

from texte.protocol import file_message, frame_message, parse_file_delivery

HOST = "127.0.0.1"


def test_udp_server_registers_and_broadcasts_to_registered_clients() -> None:
    port = _free_port()
    server = subprocess.Popen([sys.executable, "server.py", "--port", str(port)])
    first = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    second = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    first.settimeout(2)
    second.settimeout(2)

    try:
        _send_udp_until(first, port, b"{REGISTER}Alice", lambda text: text == "{MSG}Welcome Alice!")
        _send_udp_until(second, port, b"{REGISTER}Bob", lambda text: text == "{MSG}Welcome Bob!")

        first.sendto(b"{ALL}hello", (HOST, port))
        first_message = _recv_udp_until(first, lambda text: " Alice: hello" in text)
        second_message = _recv_udp_until(second, lambda text: " Alice: hello" in text)

        assert first_message.startswith("{MSG}[")
        assert second_message.startswith("{MSG}[")
    finally:
        first.close()
        second.close()
        _stop_process(server)


def test_udp_server_rejects_file_messages() -> None:
    port = _free_port()
    server = subprocess.Popen([sys.executable, "server.py", "--port", str(port)])
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.settimeout(2)

    try:
        message = _send_udp_until(
            client,
            port,
            b"{FILE}ALL|demo.txt|aGVsbG8=",
            lambda text: text == "{ERROR}Attachments require TCP.",
        )

        assert message == "{ERROR}Attachments require TCP."
    finally:
        client.close()
        _stop_process(server)


def test_tcp_server_registers_and_broadcasts_to_registered_clients() -> None:
    port = _free_port()
    server = subprocess.Popen([sys.executable, "server.py", "tcp", "--port", str(port)])
    first_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    second_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    first_socket.settimeout(2)
    second_socket.settimeout(2)
    first = FramedSocket(first_socket)
    second = FramedSocket(second_socket)

    try:
        _connect_tcp(first_socket, port)
        _connect_tcp(second_socket, port)

        first.send("{REGISTER}Alice")
        assert first.recv_until(lambda text: text == "{MSG}Welcome Alice!") == "{MSG}Welcome Alice!"
        second.send("{REGISTER}Bob")
        assert second.recv_until(lambda text: text == "{MSG}Welcome Bob!") == "{MSG}Welcome Bob!"

        first.send("{ALL}hello")
        first_message = first.recv_until(lambda text: " Alice: hello" in text)
        second_message = second.recv_until(lambda text: " Alice: hello" in text)

        assert first_message.startswith("{MSG}[")
        assert second_message.startswith("{MSG}[")
    finally:
        first_socket.close()
        second_socket.close()
        _stop_process(server)


def test_tcp_server_routes_direct_messages_only_to_target_and_sender() -> None:
    port = _free_port()
    server = subprocess.Popen([sys.executable, "server.py", "tcp", "--port", str(port)])
    alice_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bob_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cara_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    for sock in (alice_socket, bob_socket, cara_socket):
        sock.settimeout(1)
    alice = FramedSocket(alice_socket)
    bob = FramedSocket(bob_socket)
    cara = FramedSocket(cara_socket)

    try:
        for sock in (alice_socket, bob_socket, cara_socket):
            _connect_tcp(sock, port)

        alice.send("{REGISTER}Alice")
        alice.recv_until(lambda text: text == "{MSG}Welcome Alice!")
        bob.send("{REGISTER}Bob")
        bob.recv_until(lambda text: text == "{MSG}Welcome Bob!")
        cara.send("{REGISTER}Cara")
        cara.recv_until(lambda text: text == "{MSG}Welcome Cara!")

        alice.send("{TO}Bob|private ping")
        alice_message = alice.recv_until(lambda text: "Alice -> Bob: private ping" in text)
        bob_message = bob.recv_until(lambda text: "Alice -> Bob: private ping" in text)

        assert alice_message.startswith("{MSG}[")
        assert bob_message.startswith("{MSG}[")
        assert not cara.has_message(lambda text: "private ping" in text)
    finally:
        for sock in (alice_socket, bob_socket, cara_socket):
            sock.close()
        _stop_process(server)


def test_tcp_server_routes_small_file_attachments() -> None:
    port = _free_port()
    server = subprocess.Popen([sys.executable, "server.py", "tcp", "--port", str(port)])
    alice_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bob_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    alice_socket.settimeout(2)
    bob_socket.settimeout(2)
    alice = FramedSocket(alice_socket)
    bob = FramedSocket(bob_socket)

    try:
        _connect_tcp(alice_socket, port)
        _connect_tcp(bob_socket, port)

        alice.send("{REGISTER}Alice")
        alice.recv_until(lambda text: text == "{MSG}Welcome Alice!")
        bob.send("{REGISTER}Bob")
        bob.recv_until(lambda text: text == "{MSG}Welcome Bob!")

        alice.send(file_message("Bob", "note.txt", b"hello file"))
        alice_delivery = parse_file_delivery(
            alice.recv_until(lambda text: text.startswith("{FILE}"))
        )
        bob_delivery = parse_file_delivery(bob.recv_until(lambda text: text.startswith("{FILE}")))

        assert alice_delivery is not None
        assert alice_delivery.sender == "Alice"
        assert alice_delivery.filename == "note.txt"
        assert alice_delivery.data == b"hello file"
        assert bob_delivery == alice_delivery
    finally:
        alice_socket.close()
        bob_socket.close()
        _stop_process(server)


def test_tcp_server_exits_after_last_client_disconnects() -> None:
    port = _free_port()
    server = subprocess.Popen([sys.executable, "server.py", "tcp", "--port", str(port)])
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(2)
    client = FramedSocket(client_socket)

    try:
        _connect_tcp(client_socket, port)
        client.send("{REGISTER}Alice")
        assert (
            client.recv_until(lambda text: text == "{MSG}Welcome Alice!") == "{MSG}Welcome Alice!"
        )
        client.send("{DISCONNECT}")
        deadline = time.time() + 5
        while time.time() < deadline:
            if server.poll() is not None:
                break
            time.sleep(0.1)
        assert server.poll() is not None
    finally:
        client_socket.close()
        _stop_process(server)


class FramedSocket:
    def __init__(self, sock: socket.socket) -> None:
        self.sock = sock
        self.buffer = ""

    def send(self, message: str) -> None:
        self.sock.sendall(frame_message(message))

    def recv_until(self, predicate) -> str:
        deadline = time.time() + 5
        while time.time() < deadline:
            for message in self._pop_messages():
                if predicate(message):
                    return message
            self.buffer += self.sock.recv(4096).decode()
        raise RuntimeError("TCP server did not send expected frame")

    def has_message(self, predicate) -> bool:
        deadline = time.time() + 0.3
        while time.time() < deadline:
            try:
                self.buffer += self.sock.recv(4096).decode()
            except OSError:
                break
            for message in self._pop_messages():
                if predicate(message):
                    return True
        return False

    def _pop_messages(self) -> list[str]:
        if "\n" not in self.buffer:
            return []
        parts = self.buffer.split("\n")
        self.buffer = parts.pop()
        return [part.strip() for part in parts if part.strip()]


def _send_udp_until(
    sock: socket.socket,
    port: int,
    payload: bytes,
    predicate,
) -> str:
    deadline = time.time() + 5
    while time.time() < deadline:
        try:
            sock.sendto(payload, (HOST, port))
            return _recv_udp_until(sock, predicate)
        except OSError:
            time.sleep(0.1)
    raise RuntimeError("UDP server did not respond")


def _recv_udp_until(sock: socket.socket, predicate) -> str:
    deadline = time.time() + 5
    while time.time() < deadline:
        message = sock.recvfrom(4096)[0].decode()
        if predicate(message):
            return message
    raise RuntimeError("UDP server did not send expected datagram")


def _connect_tcp(sock: socket.socket, port: int) -> None:
    deadline = time.time() + 5
    while time.time() < deadline:
        try:
            sock.connect((HOST, port))
            return
        except OSError:
            time.sleep(0.1)
    raise RuntimeError("TCP server did not accept connections")


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST, 0))
        return sock.getsockname()[1]


def _stop_process(process: subprocess.Popen) -> None:
    if process.poll() is None:
        process.terminate()
        process.wait(timeout=5)
