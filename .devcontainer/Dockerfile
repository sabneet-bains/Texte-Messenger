FROM mcr.microsoft.com/devcontainers/python:1-3.12-bookworm

# The base image carries an inherited Yarn apt source that breaks `apt-get update`
# in Codespaces when its signing key is unavailable. Remove it before installing
# the Qt/X11 stack we actually need.
RUN for source in /etc/apt/sources.list.d/*; do \
        if [ -f "$source" ] && grep -q 'dl.yarnpkg.com' "$source"; then \
            rm -f "$source"; \
        fi; \
    done \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        fluxbox \
        libegl1 \
        libfontconfig1 \
        libgl1 \
        libopengl0 \
        libxcb-cursor0 \
        libxcb-icccm4 \
        libxcb-image0 \
        libxcb-keysyms1 \
        libxcb-randr0 \
        libxcb-render-util0 \
        libxcb-shape0 \
        libxcb-xfixes0 \
        libxcb-xinerama0 \
        libxkbcommon-x11-0 \
        novnc \
        websockify \
        x11vnc \
        xvfb \
    && rm -rf /var/lib/apt/lists/* \
    && python -m pip install --no-cache-dir "PyQt6>=6.11,<7"
