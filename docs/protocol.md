# Texte Protocol

Texte uses small command-prefixed text messages. UDP sends one command per
datagram. TCP uses newline-delimited frames so commands can be split or merged
by the network without confusing the parser.

## Client Commands

| Command | Payload | Meaning |
| --- | --- | --- |
| `{CONNECT}` | none | Client connected. |
| `{DISCONNECT}` | none | Client disconnected. |
| `{REGISTER}` | display name | Register a local display name. |
| `{UNREGISTER}` | display name | Remove the registered display name. |
| `{ALL}` | message text | Send a public room message. |
| `{TO}` | `recipient|message text` | Send a direct message to one user. |
| `{FILE}` | `recipient|filename|base64-data` | Send a small TCP attachment. |

## Server Messages

| Command | Payload | Meaning |
| --- | --- | --- |
| `{MSG}` | display text | Chat, direct, welcome, goodbye, or system text. |
| `{USERS}` | comma-separated names | Current signed-in users. |
| `{FILE}` | `sender|filename|base64-data` | Routed file attachment. |
| `{ERROR}` | display text | Validation or routing error. |

## Limits

- File payloads are capped at 1 MB.
- Attachments are TCP-only in the GUI.
- Usernames are display names, not authenticated identities.
- Direct messages route by current display name.
- There is no encryption, persistence, or account database.

## Code Entry Points

The protocol helpers live in `texte/protocol.py`. The shared routing state lives
in `texte/chat_room.py`. Both UDP and TCP server adapters call the same
`ChatRoom.route(...)` method.
