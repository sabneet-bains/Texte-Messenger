# Correctness Notes

Texte is a local messenger prototype with tested transport and routing behavior.
It is not a secure or production chat system.

## Scope Boundary

The project supports local UDP and TCP servers, display-name registration,
presence updates, public `ALL` messages, direct display-name messages, and small
TCP-only file payloads.

It intentionally does not implement authentication, encryption, persistence,
offline delivery, cloud sync, mobile layouts, or general-purpose file sharing.

## Shared Routing Core

Both transports call the same `ChatRoom` routing logic. That prevents a common
demo-app drift where UDP and TCP behave differently because each has its own
registration or recipient code.

The socket adapters own only transport concerns:

- UDP receives one command per datagram.
- TCP receives newline-framed commands from a byte stream.
- `ChatRoom` returns explicit deliveries for the adapter to write.

## Verification Strategy

The tests cover three layers:

- Pure helpers: protocol parsing, framing, timestamp formatting, file payloads.
- Routing state: registration, duplicate names, presence, direct messages,
  disconnect cleanup, and errors.
- Integration: real UDP/TCP sockets, scripted demos, and offscreen PyQt6 client
  construction.

The scripted demo output is checked against files in `examples/expected/` after
normalizing timestamps.

## Verification Commands

```bash
python -m pip install -e ".[dev]"
python -m ruff check .
python -m ruff format --check .
python -m mypy texte examples tests
python -m compileall client.py server.py texte tests examples
python -m pytest
python examples/two_client_demo.py --protocol tcp
python examples/two_client_demo.py --protocol udp
python -m build
```
