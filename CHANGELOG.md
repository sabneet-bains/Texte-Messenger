# Changelog

All notable changes for this project are tracked here.

## 0.1.0 - Local PyQt6 Messenger Prototype

### What Became Possible

- Added a package-based PyQt6 desktop client with UDP/TCP transport selection.
- Added local UDP and TCP servers with shared registration and routing logic.
- Added display-name presence, public `ALL` messages, direct messages, and
  disconnect cleanup.
- Added newline-framed TCP commands so stream reads can split or merge messages
  safely.
- Added small TCP-only attachment routing with local download saving.
- Added scripted TCP and UDP demos with expected transcripts.

### Verification

- Added tests for protocol helpers, routing state, UDP/TCP socket integration,
  scripted demos, theme data, and offscreen GUI construction.
- Added Ruff, format checks, compile checks, package build, and demo smoke
  checks through GitHub Actions.

### Intentional Limits

- Kept authentication, encryption, persistence, cloud hosting, and offline
  delivery out of scope.
- Kept file transfer small and TCP-only.
