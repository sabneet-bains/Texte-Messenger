# Contributing

Texte favors small changes that keep chat behavior easy to inspect.

## Local Checks

```bash
python -m pip install -e ".[dev]"
python -m ruff check .
python -m ruff format --check .
python -m mypy texte examples tests
python -m compileall client.py server.py texte tests examples
python -m pytest
python -m build
```

## Adding Protocol Behavior

Protocol changes should follow the same path the app uses:

```text
protocol.py -> chat_room.py -> server/client adapter -> tests -> docs
```

1. Add or update parsing/formatting helpers in `texte/protocol.py`.
2. Route the behavior in `texte/chat_room.py` when it affects users.
3. Keep UDP and TCP behavior shared unless a transport difference is explicit.
4. Add positive and failure tests.
5. Update `docs/protocol.md` and README claims only after the behavior is real.

Unsupported behavior should fail clearly. Do not add UI labels or README claims
for features that are only planned.
