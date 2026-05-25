#!/usr/bin/env bash
set -euo pipefail

export DISPLAY="${DISPLAY:-:99}"
export QT_QPA_PLATFORM="${QT_QPA_PLATFORM:-xcb}"
export XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR:-/tmp/xdg-runtime-${UID:-$(id -u)}}"
mkdir -p "$XDG_RUNTIME_DIR"
chmod 700 "$XDG_RUNTIME_DIR"

if ! pgrep -f "Xvfb ${DISPLAY}" >/dev/null 2>&1; then
  nohup Xvfb "$DISPLAY" -screen 0 1800x1000x24 -ac +extension GLX +render -noreset \
    >/tmp/texte-showcase-xvfb.log 2>&1 &
  sleep 1
fi

if ! pgrep -f "fluxbox" >/dev/null 2>&1; then
  nohup fluxbox >/tmp/texte-showcase-fluxbox.log 2>&1 &
fi

if ! pgrep -f "x11vnc .*5901" >/dev/null 2>&1; then
  nohup x11vnc -display "$DISPLAY" -localhost -forever -shared -nopw -rfbport 5901 \
    >/tmp/texte-showcase-x11vnc.log 2>&1 &
fi

NOVNC_PROXY="${NOVNC_PROXY:-/usr/share/novnc/utils/novnc_proxy}"
if ! pgrep -f "novnc_proxy .*6080" >/dev/null 2>&1; then
  nohup "$NOVNC_PROXY" --vnc localhost:5901 --listen 6080 \
    >/tmp/texte-showcase-novnc.log 2>&1 &
fi

if ! pgrep -f "texte-showcase --protocol tcp" >/dev/null 2>&1; then
  nohup texte-showcase --protocol tcp >/tmp/texte-showcase-app.log 2>&1 &
fi
