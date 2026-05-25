# Tutorial

This walkthrough runs Texte locally with two clients.

If you want the browser-hosted version that opens directly from GitHub, use the
Codespaces showcase path in [docs/showcase.md](showcase.md).

## 1. Install

```bash
python -m pip install -e ".[dev]"
```

## 2. Start Two Clients

Open two terminals and run:

```bash
python client.py
```

The first client starts a local TCP server automatically when one is not
already running. The second client connects to that same server and appears in
the conversation list.

## 3. Advanced Server Mode

Manual server startup is still available:

```bash
python server.py tcp
python server.py
```

Use the setup sheet to change host, port, protocol, display name, avatar, or
automatic local-server startup.

## 4. Send Messages

Select `ALL` for public room messages. Select a specific display name for a
direct message. Attachments require TCP mode and are saved into `downloads/`.

## 5. Verify The Project

```bash
python -m pytest
python -m compileall client.py server.py texte tests examples
python -m ruff check .
python -m ruff format --check .
python -m mypy texte examples tests
python -m build
```
