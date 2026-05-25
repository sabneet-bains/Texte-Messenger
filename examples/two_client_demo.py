"""Run a small scripted Texte demo against a local server."""

import argparse
import socket
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOST = "127.0.0.1"

sys.path.insert(0, str(ROOT))

from texte.protocol import chat_message, file_message, frame_message, parse_file_delivery  # noqa: E402


class DemoClient:
    def __init__(self, protocol: str, port: int) -> None:
        self.protocol = protocol
        self.port = port
        self.buffer = ""
        if protocol == "udp":
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        else:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(2)

    def connect(self) -> None:
        if self.protocol == "tcp":
            deadline = time.time() + 5
            while time.time() < deadline:
                try:
                    self.socket.connect((HOST, self.port))
                    return
                except OSError:
                    time.sleep(0.1)

    def send(self, message: str) -> None:
        if self.protocol == "udp":
            self.socket.sendto(message.encode(), (HOST, self.port))
        else:
            self.socket.sendall(frame_message(message))

    def send_until(self, message: str, predicate) -> str:
        if self.protocol == "tcp":
            self.send(message)
            return self.recv_until(predicate)

        deadline = time.time() + 5
        last_error: OSError | None = None
        while time.time() < deadline:
            try:
                self.send(message)
                reply = self.socket.recvfrom(4096)[0].decode()
                if predicate(reply):
                    return reply
            except OSError as error:
                last_error = error
                time.sleep(0.1)
        raise RuntimeError("Timed out waiting for UDP demo response.") from last_error

    def recv_until(self, predicate) -> str:
        deadline = time.time() + 5
        while time.time() < deadline:
            try:
                for message in self._read_messages():
                    if predicate(message):
                        return message
            except OSError:
                time.sleep(0.1)
        raise RuntimeError("Timed out waiting for demo message.")

    def close(self) -> None:
        self.socket.close()

    def _read_messages(self) -> list[str]:
        if self.protocol == "udp":
            return [self.socket.recvfrom(4096)[0].decode()]

        while "\n" not in self.buffer:
            self.buffer += self.socket.recv(4096).decode()
        parts = self.buffer.split("\n")
        self.buffer = parts.pop()
        return [part.strip() for part in parts if part.strip()]


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a two-client Texte demo.")
    parser.add_argument("--protocol", choices=["udp", "tcp"], default="tcp")
    parser.add_argument("--port", type=int, default=33042)
    args = parser.parse_args()

    server_args = [sys.executable, str(ROOT / "server.py"), "--port", str(args.port)]
    if args.protocol == "tcp":
        server_args.insert(2, "tcp")
    server = subprocess.Popen(server_args)
    alice = DemoClient(args.protocol, args.port)
    bob = DemoClient(args.protocol, args.port)

    try:
        alice.connect()
        bob.connect()

        alice.send_until("{REGISTER}Alice", lambda message: message == "{MSG}Welcome Alice!")
        print("Alice signed in")

        bob.send_until("{REGISTER}Bob", lambda message: message == "{MSG}Welcome Bob!")
        print("Bob signed in")

        alice.send(chat_message("ALL", "hello"))
        bob_message = bob.recv_until(lambda message: " Alice: hello" in message)
        print(f"Bob received public message: {bob_message.removeprefix('{MSG}')}")

        alice.send(chat_message("Bob", "private ping"))
        bob_direct = bob.recv_until(lambda message: "Alice -> Bob: private ping" in message)
        print(f"Bob received direct message: {bob_direct.removeprefix('{MSG}')}")

        if args.protocol == "tcp":
            alice.send(file_message("Bob", "demo.txt", b"hello from texte"))
            delivery = parse_file_delivery(
                bob.recv_until(lambda message: message.startswith("{FILE}"))
            )
            if delivery is None:
                raise RuntimeError("Expected a file delivery.")
            print(
                f"Bob received file: {delivery.filename} "
                f"from {delivery.sender} ({len(delivery.data)} bytes)"
            )
        else:
            print("UDP demo skipped file transfer; attachments are TCP-only.")
    finally:
        alice.close()
        bob.close()
        if server.poll() is None:
            server.terminate()
            server.wait(timeout=5)


if __name__ == "__main__":
    main()
