# Code Tour

Texte is shaped around chat concepts rather than framework-heavy layers. The
desktop UI, socket adapters, protocol helpers, and routing state are separate so
the data flow stays visible.

```text
client widgets
  -> protocol commands
  -> UDP datagram or TCP frame
  -> server socket adapter
  -> ChatRoom routing
  -> explicit deliveries
  -> client rendering
```

## Core Pipeline

| File | Owns | What to notice |
| --- | --- | --- |
| `texte/protocol.py` | Command constants, parsing, framing, file payloads | TCP framing and message parsing are deterministic and testable. |
| `texte/chat_room.py` | Registration, presence, broadcast, direct routing | UDP and TCP share one routing source of truth. |
| `texte/server.py` | Qt socket adapters and CLI args | Network events are translated into `ChatRoom.route(...)` calls. |
| `texte/client.py` | Client state, events, validation, rendering | UI actions become protocol commands; server messages become visible state. |
| `texte/ui.py` | Layout-based widget construction | Window geometry comes from Qt layouts, not fixed pixel placement. |
| `texte/themes.py` | Built-in palettes | Theme data stays separate from event handling. |

## Support Files

| File | Owns | What to notice |
| --- | --- | --- |
| `examples/two_client_demo.py` | Scripted local demo | Starts a temporary server and drives two real clients. |
| `examples/expected/` | Demo output contracts | Keeps README-style examples tied to real behavior. |
| `docs/protocol.md` | Wire command reference | States the exact supported messages and limits. |
| `docs/correctness.md` | Verification notes | Explains what the tests prove and what they do not prove. |
| `tests/` | Behavior contract | Covers pure protocol logic, routing, demos, and real UDP/TCP sockets. |

The simple-code signature is intentional: domain names, explicit deliveries,
small routing decisions, and direct tests for each behavior.
