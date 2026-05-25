# GitHub Showcase Path

Texte is designed to be opened from GitHub, not only cloned and run by hand.
The Codespaces path gives visitors a browser-accessible desktop session with the
real PyQt6 app, the local server, and a ready-made two-client conversation.

<div align="center">

<img src="../texte/assets/showcase-path.svg" alt="GitHub repo to Codespaces to browser desktop showcase flow" width="94%">

</div>

## What Starts Automatically

- The devcontainer installs the Linux Qt/X11 packages needed for the desktop app.
- A virtual X display and a browser-accessible VNC bridge start inside the container.
- `texte-showcase` launches a local server and two preconfigured PyQt6 clients.
- The showcase seeds one public message and one direct message so the transcript is visible immediately.

## Manual Relaunch

```bash
texte-showcase
```

## What Visitors Can Do

- Type in the Alice or Bob window and watch the other client receive the message.
- Switch between `ALL` and a direct recipient to inspect the protocol from the UI.
- Use the normal attachments flow in TCP mode.
- Close the browser tab or the windows without leaving the repository in a fake state.

## Why Not github.dev

`github.dev` is a code editor in the browser. It is useful for inspection, but it
does not run this desktop app. The Codespaces path exists so hiring teams can
actually interact with the project instead of reading about it.
