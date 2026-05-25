import re
import socket
import subprocess
import sys
from pathlib import Path

HOST = "127.0.0.1"


def test_tcp_demo_matches_expected_transcript() -> None:
    output = _run_demo("tcp")
    expected = Path("examples/expected/tcp-demo.txt").read_text(encoding="utf-8").strip()

    assert _normalize_timestamps(output) == expected


def test_udp_demo_matches_expected_transcript() -> None:
    output = _run_demo("udp")
    expected = Path("examples/expected/udp-demo.txt").read_text(encoding="utf-8").strip()

    assert _normalize_timestamps(output) == expected


def _run_demo(protocol: str) -> str:
    result = subprocess.run(
        [
            sys.executable,
            "examples/two_client_demo.py",
            "--protocol",
            protocol,
            "--port",
            str(_free_port()),
        ],
        check=True,
        capture_output=True,
        text=True,
        timeout=10,
    )
    return result.stdout.strip()


def _normalize_timestamps(output: str) -> str:
    return re.sub(r"\[\d\d:\d\d\]", "[HH:MM]", output)


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST, 0))
        return sock.getsockname()[1]
