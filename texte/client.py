#!/usr/bin/env python3
"""
Chat Client

This script builds the Texte desktop chat client with PyQt6. It provides a
single chat window, UDP/TCP transport selection, sign-in controls, themes,
avatar selection, a message log, and local image attachment previews.

Usage:
    python client.py

Author: Sabneet Bains
License: MIT
"""

import logging
import os
import platform
import subprocess
import sys
from datetime import datetime
from functools import partial
from pathlib import Path
from typing import Literal

from PyQt6 import QtCore, QtGui, QtWidgets, QtNetwork

from texte.client_support import (
    ConversationListItem,
    entry_bool,
    entry_int,
    entry_strings,
    entry_text,
    qbytearray_to_text,
    scrollbar_or_raise,
)
from texte.glass import animate_entry
from texte.ui import setup_ui
from texte.widgets import (
    ClickableLabel,
    ConversationRow,
    PinnedConversationTile,
    ReactionBarPopup,
    ReactionLabel,
    MessageOptionsPopup,
    TransientScrollStyle,
    emoji_font,
)

from texte.protocol import (
    CONNECT,
    DISCONNECT,
    ERROR,
    FIELD,
    MAX_FILE_BYTES,
    chat_message,
    display_text,
    file_message,
    frame_message,
    message_has_chat_text,
    outgoing_payload,
    parse_file_delivery,
    register_message,
    split_frames,
    unregister_message,
    users_payload,
)
from texte.themes import ThemePalette, theme_palette

PACKAGE_DIR = Path(__file__).resolve().parent
ASSET_DIR = PACKAGE_DIR / "assets"
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def suppress_socket_warnings(
    msg_type: QtCore.QtMsgType,
    ctx: QtCore.QMessageLogContext,
    msg: str | None,
) -> None:
    """Suppress noisy Qt socket cleanup warnings that don't affect functionality."""
    if msg is None:
        return
    # Filter out QNativeSocketEngine and socket disconnect warnings during cleanup
    if "QNativeSocketEngine" in msg or (
        "QObject::disconnect" in msg and ("Socket" in msg or "Engine" in msg)
    ):
        return
    # Let other messages through to stderr
    if msg_type == QtCore.QtMsgType.QtDebugMsg:
        print(f"DEBUG: {msg}", file=sys.stderr)
    elif msg_type == QtCore.QtMsgType.QtWarningMsg:
        print(f"WARNING: {msg}", file=sys.stderr)
    elif msg_type == QtCore.QtMsgType.QtCriticalMsg:
        print(f"CRITICAL: {msg}", file=sys.stderr)
    elif msg_type == QtCore.QtMsgType.QtFatalMsg:
        print(f"FATAL: {msg}", file=sys.stderr)


QtCore.qInstallMessageHandler(suppress_socket_warnings)


class ChatClient(QtWidgets.QWidget):
    """PyQt6 dialog for the Texte chat client."""

    # Window and transport state
    socket: QtNetwork.QUdpSocket | QtNetwork.QTcpSocket
    root_layout: QtWidgets.QHBoxLayout
    splitter: QtWidgets.QSplitter
    app_title: QtWidgets.QLabel
    app_subtitle: QtWidgets.QLabel
    new_message_button: QtWidgets.QPushButton

    # Sidebar and setup sheet
    sidebar: QtWidgets.QWidget
    setup_button: QtWidgets.QPushButton
    setup_sheet: QtWidgets.QFrame
    setup_scroll: QtWidgets.QScrollArea
    setup_content: QtWidgets.QWidget
    setup_title: QtWidgets.QLabel
    setup_close_button: QtWidgets.QPushButton
    search_field: QtWidgets.QLineEdit
    pinned_title: QtWidgets.QLabel
    pinned_widget: QtWidgets.QWidget
    pinned_layout: QtWidgets.QGridLayout
    recent_title: QtWidgets.QLabel
    conversation_list: QtWidgets.QListWidget
    profile_popup: QtWidgets.QFrame
    profile_title: QtWidgets.QLabel

    # Server controls
    host_title: QtWidgets.QLabel
    host_address: QtWidgets.QLineEdit
    port_title: QtWidgets.QLabel
    port_number: QtWidgets.QLineEdit
    protocol_selector: QtWidgets.QComboBox
    protocol_switch: QtWidgets.QFrame
    protocol_tcp_button: QtWidgets.QPushButton
    protocol_udp_button: QtWidgets.QPushButton
    auto_server_checkbox: QtWidgets.QCheckBox
    server_button: QtWidgets.QPushButton
    server_connection_status: QtWidgets.QLabel

    # Sign-in controls
    username_title: QtWidgets.QLabel
    username: QtWidgets.QLineEdit
    sign_in_button: QtWidgets.QPushButton
    user_avatar: QtWidgets.QPushButton
    temporary_avatar: QtWidgets.QPushButton
    avatar_selector_panel: QtWidgets.QDialog
    avatar_selector_widget: QtWidgets.QStackedWidget
    avatar_previous_button: QtWidgets.QPushButton
    avatar_next_button: QtWidgets.QPushButton
    reaction_bar_popup: ReactionBarPopup | None
    message_options_popup: MessageOptionsPopup | None

    # Chat controls
    chat_theme_title: QtWidgets.QLabel
    chat_theme: QtWidgets.QComboBox
    chat_selector_title: QtWidgets.QLabel
    chat_selector: QtWidgets.QComboBox
    chat_confirm_button: QtWidgets.QPushButton
    chat_header: QtWidgets.QWidget
    chat_header_avatar: QtWidgets.QLabel
    chat_title: QtWidgets.QLabel
    chat_subtitle: QtWidgets.QLabel
    header_username: QtWidgets.QLabel
    theme_switch: QtWidgets.QWidget
    theme_light_button: QtWidgets.QPushButton
    theme_dark_button: QtWidgets.QPushButton
    chat_log: QtWidgets.QListWidget
    composer_panel: QtWidgets.QFrame
    composer_shell: QtWidgets.QFrame
    message_field: QtWidgets.QLineEdit
    attach_button: QtWidgets.QPushButton
    emoji_button: QtWidgets.QPushButton

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)
        self.logger = logger

        self.socket = QtNetwork.QUdpSocket(self)
        self.tcp_buffer = ""
        self.server_connected = False
        self.user_signed_in = False
        self.download_dir = Path.cwd() / "downloads"
        self._icons: dict[str, QtGui.QIcon] = {}
        self.conversation_previews: dict[str, str] = {}
        self.conversation_times: dict[str, str] = {}
        self.conversation_history: dict[str, list[dict[str, object]]] = {"ALL": []}
        self.pinned_tiles: dict[str, PinnedConversationTile] = {}
        self._seeded_onboarding = False
        self._last_message_kind: str | None = None
        self._last_message_sender: str | None = None
        self.active_username: str = ""
        self.active_avatar_name: str = "user1"
        self.theme_preference: Literal["Light", "Dark"] | None = None
        self.started_server_process = False
        self.native_backdrop_enabled = False
        self.reaction_bar_popup = None
        self.message_options_popup = None

        self._setup_scaling()
        self._setup_ui()
        self._connect_signals()
        app = QtWidgets.QApplication.instance()
        if isinstance(app, QtWidgets.QApplication):
            app.installEventFilter(self)
        self._apply_theme_preference(None)
        self._set_conversations(["ALL"])
        self._configure_platform_scrollbars()
        if os.environ.get("TEXTE_DISABLE_AUTO_START") != "1":
            QtCore.QTimer.singleShot(0, self.start_local_session)

    # Setup helpers

    def _setup_scaling(self) -> None:
        """Keep style measurements independent from physical screen pixels."""
        app = QtWidgets.QApplication.instance()
        font = self._ui_font()
        self.setFont(font)
        if isinstance(app, QtWidgets.QApplication):
            app.setFont(font)

        font_size = font.pointSize()
        self.scaled_border_radius = "8"
        self.scaled_font_size = str(font_size if font_size > 0 else 10)
        self.scaled_underline_size = "1"

    def _ui_font(self) -> QtGui.QFont:
        available_fonts = set(QtGui.QFontDatabase.families())
        for family in ("Segoe UI", "Inter", "Arial", "Noto Sans", "DejaVu Sans"):
            if family in available_fonts:
                return QtGui.QFont(family, 10)
        return QtGui.QFont("Sans Serif", 10)

    def _asset_path(self, *parts: str) -> str:
        return str(ASSET_DIR.joinpath(*parts))

    def _icon(self, *parts: str) -> QtGui.QIcon:
        path = self._asset_path(*parts)
        if path not in self._icons:
            self._icons[path] = QtGui.QIcon(path)
        return self._icons[path]

    def _setup_ui(self) -> None:
        setup_ui(self)
        self.username.setText("")
        self.username.setPlaceholderText("Choose a username")
        self.user_avatar.setToolTip("Choose avatar")
        self.header_username.setText("Pick profile")
        self._position_setup_sheet()

    def _configure_platform_scrollbars(self) -> None:
        """Let Qt prefer platform scrollbars instead of a custom painted one."""
        style = TransientScrollStyle(self.style())
        vertical = scrollbar_or_raise(self.chat_log)
        horizontal = self.chat_log.horizontalScrollBar()
        assert horizontal is not None
        vertical.setStyle(style)
        horizontal.setStyle(style)

    def _default_display_name(self) -> str:
        return f"Local {os.getpid() % 10_000:04d}"

    def _css_color(self, color: str, alpha: int | None = None) -> str:
        qt_color = QtGui.QColor(color)
        if alpha is not None:
            qt_color.setAlpha(max(0, min(alpha, 255)))
        return qt_color.name(QtGui.QColor.NameFormat.HexArgb)

    def _replace_socket(self, socket: QtNetwork.QUdpSocket | QtNetwork.QTcpSocket) -> None:
        old_socket = self.socket
        old_socket.blockSignals(True)
        old_socket.disconnect()
        self.socket = socket
        self.tcp_buffer = ""
        self.socket.readyRead.connect(self.receive_message)
        old_socket.deleteLater()

    def _use_protocol(self, protocol: str) -> None:
        if protocol == "TCP" and not isinstance(self.socket, QtNetwork.QTcpSocket):
            self._replace_socket(QtNetwork.QTcpSocket(self))
        elif protocol == "UDP" and not isinstance(self.socket, QtNetwork.QUdpSocket):
            self._replace_socket(QtNetwork.QUdpSocket(self))
        self._sync_protocol_buttons(protocol)

    def _sync_protocol_buttons(self, protocol: str) -> None:
        self.protocol_tcp_button.blockSignals(True)
        self.protocol_udp_button.blockSignals(True)
        self.protocol_tcp_button.setChecked(protocol == "TCP")
        self.protocol_udp_button.setChecked(protocol == "UDP")
        self.protocol_tcp_button.blockSignals(False)
        self.protocol_udp_button.blockSignals(False)

    def _set_protocol_controls_enabled(self, enabled: bool) -> None:
        self.protocol_selector.setEnabled(enabled)
        self.protocol_tcp_button.setEnabled(enabled)
        self.protocol_udp_button.setEnabled(enabled)

    def _show_profile_onboarding(self) -> None:
        self.profile_popup.hide()
        self.avatar_selector_panel.hide()
        self._set_presence()
        self._update_profile_action_state()

    def _update_profile_action_state(self) -> None:
        if self.user_signed_in:
            self.sign_in_button.setEnabled(True)
            return
        ready = bool(
            self.server_connected and self.username.text().strip() and self.active_avatar_name
        )
        self.sign_in_button.setEnabled(ready)

    def _select_protocol(self, protocol: str) -> None:
        if self.server_connected:
            self._sync_protocol_buttons(self.protocol_selector.currentText())
            return
        self.protocol_selector.setCurrentText(protocol)
        self._use_protocol(protocol)

    def _server_address(self, host: str | None = None, port: int | None = None) -> tuple[str, int]:
        if host is None:
            host = self.host_address.text().strip() or "127.0.0.1"
        if port is None:
            port = int(self.port_number.text())
        if not 1 <= port <= 65535:
            raise ValueError("port must be between 1 and 65535")
        return host, port

    def start_local_session(self) -> None:
        """Make the local chat usable without exposing server setup first."""
        if self.server_connected or not self.auto_server_checkbox.isChecked():
            return
        self._connect_or_start_server(self.protocol_selector.currentText())

    def _connect_or_start_server(self, protocol: str) -> None:
        normalized = protocol.upper()
        if normalized == "TCP":
            self._connect_or_start_tcp_server()
            return
        self._connect_or_start_udp_server()

    def _connect_or_start_tcp_server(self) -> None:
        try:
            host, port = self._server_address()
        except ValueError:
            self._add_chat_text("Enter a valid port from 1 to 65535.", "system")
            return

        probe = QtNetwork.QTcpSocket(self)
        probe.connectToHost(QtNetwork.QHostAddress(host), port)
        if probe.waitForConnected(140):
            probe.disconnectFromHost()
            probe.deleteLater()
            self._connect_and_sign_in(host, port)
            return
        probe.abort()
        probe.deleteLater()
        self._start_owned_server("tcp", host, port)

    def _connect_or_start_udp_server(self) -> None:
        try:
            host, port = self._server_address()
        except ValueError:
            self._add_chat_text("Enter a valid port from 1 to 65535.", "system")
            return

        self._start_owned_server("udp", host, port)
        QtCore.QTimer.singleShot(140, lambda: self._connect_and_sign_in(host, port, "UDP"))

    def _start_owned_server(self, protocol: str, host: str, port: int) -> None:
        arguments = [
            "-m",
            "texte.server",
            "--protocol",
            protocol,
            "--host",
            host,
            "--port",
            str(port),
        ]
        if not QtCore.QProcess.startDetached(sys.executable, arguments):
            self._add_chat_text("Could not start the local server.", "system")
            return
        self.started_server_process = True
        if protocol == "tcp":
            QtCore.QTimer.singleShot(250, lambda: self._connect_and_sign_in(host, port, "TCP"))

    def _connect_and_sign_in(self, host: str, port: int, protocol: str | None = None) -> None:
        if self.server_connected:
            return
        selected_protocol = protocol or self.protocol_selector.currentText()
        self.protocol_selector.setCurrentText(selected_protocol)
        self._use_protocol(selected_protocol)
        self.server_button.setChecked(True)
        self.connect_client()
        if not self.user_signed_in:
            self.sign_in_button.setChecked(True)
            self.sign_in()

    # Theme and styling

    def theme(self, theme_name: str) -> None:
        """Apply one of the built-in color themes."""
        palette = theme_palette(theme_name)
        if palette is None:
            self.logger.error(f"Unknown theme: {theme_name}")
            return

        self.current_palette = palette
        self.chat_theme.setCurrentText(theme_name)
        self.native_backdrop_enabled = self._apply_native_backdrop(theme_name)
        self.setStyleSheet(self._app_style(palette))
        self._refresh_status_text()
        self._refresh_conversation_rows()
        self._sync_theme_buttons(theme_name)

    def _apply_native_backdrop(self, theme_name: str) -> bool:
        # Native backdrop support removed — return False to disable glass/backdrop logic.
        return False

    def _apply_theme_preference(self, preference: Literal["Light", "Dark"] | None) -> None:
        self.theme_preference = preference
        target = preference or self._os_theme_name()
        self.theme(target)

    def _os_theme_name(self) -> Literal["Light", "Dark"]:
        app = QtWidgets.QApplication.instance()
        if isinstance(app, QtWidgets.QApplication):
            style_hints = app.styleHints()
            if style_hints is not None and hasattr(style_hints, "colorScheme"):
                scheme = style_hints.colorScheme()
                if scheme == QtCore.Qt.ColorScheme.Dark:
                    return "Dark"
        palette = self.palette().window().color()
        return "Dark" if palette.lightness() < 128 else "Light"

    def _sync_theme_buttons(self, active_theme: str) -> None:
        self.theme_light_button.setChecked(active_theme == "Light")
        self.theme_dark_button.setChecked(active_theme == "Dark")
        if hasattr(self.theme_switch, "set_theme"):
            self.theme_switch.set_theme(active_theme)

    def _app_style(self, palette: ThemePalette) -> str:
        use_backdrop = self.native_backdrop_enabled
        app_background = (
            self._css_color(palette.app_background, 228) if use_backdrop else palette.app_background
        )
        sidebar_background = (
            self._css_color(palette.sidebar_background, 244)
            if use_backdrop
            else palette.sidebar_background
        )
        panel_background = (
            self._css_color(palette.sidebar_background, 250)
            if use_backdrop
            else palette.sidebar_background
        )
        field_fill = (
            self._css_color(palette.field_fill, 248) if use_backdrop else palette.field_fill
        )
        glass_fill = (
            self._css_color(palette.glass_fill, 244) if use_backdrop else palette.glass_fill
        )
        system_bubble = (
            self._css_color(palette.system_bubble, 244) if use_backdrop else palette.system_bubble
        )
        composer_fill = (
            self._css_color(palette.composer_fill, 246) if use_backdrop else palette.composer_fill
        )
        return f"""
        QWidget#Chat_Window {{
            background: {app_background};
            font-family: "Segoe UI", "Inter", "Arial", "Noto Sans", "DejaVu Sans", sans-serif;
        }}
        QSplitter#Main_Splitter::handle {{
            background: {palette.separator};
            width: 1px;
        }}
        QWidget#Sidebar {{
            background: {sidebar_background};
            border-right: 1px solid {palette.separator};
        }}
        QLabel#App_Title {{
            color: {palette.primary_text};
            font-size: 17pt;
            font-weight: 700;
        }}
        QLabel#App_Subtitle {{
            color: {palette.secondary_text};
            font-size: 8pt;
            padding-bottom: 2px;
        }}
        QFrame#Setup_Sheet {{
            background: {panel_background};
            border: 1px solid {palette.separator};
            border-radius: 14px;
        }}
        QFrame#Profile_Popup {{
            background: {panel_background};
            border: 1px solid {palette.separator};
            border-radius: 16px;
        }}
        QFrame#Reaction_Bar_Popup {{
            background: {self._css_color(palette.app_background, 248) if use_backdrop else palette.app_background};
            border: 1px solid {palette.glass_border};
            border-radius: 28px;
        }}
        QFrame#Reaction_Bar_Popup QPushButton#Reaction_Bar_Emoji {{
            color: {palette.primary_text};
            background: transparent;
            border: none;
            border-radius: 20px;
            min-width: 40px;
            max-width: 40px;
            min-height: 40px;
            max-height: 40px;
            padding: 0;
        }}
        QFrame#Reaction_Bar_Popup QPushButton#Reaction_Bar_Emoji:hover {{
            background: {palette.hover_fill};
        }}
        QFrame#Message_Options_Popup {{
            background: {self._css_color(palette.app_background, 250) if use_backdrop else palette.app_background};
            border: 1px solid {palette.glass_border};
            border-radius: 18px;
        }}
        QFrame#Message_Options_Popup QPushButton#Message_Options_Button {{
            color: {palette.primary_text};
            background: transparent;
            border: none;
            text-align: left;
            border-radius: 12px;
            min-height: 42px;
            padding: 8px 14px;
            font-size: 10pt;
        }}
        QFrame#Message_Options_Popup QPushButton#Message_Options_Button:hover {{
            background: {palette.hover_fill};
        }}
        QFrame#Message_Action_List {{
            background: transparent;
            border: none;
        }}
        QToolButton#Message_Action_Emoji {{
            color: {palette.primary_text};
            background: {system_bubble};
            border: 1px solid {palette.glass_border};
            border-radius: 15px;
            min-width: 30px;
            min-height: 30px;
            font-size: 13pt;
        }}
        QToolButton#Message_Action_Emoji:hover {{
            background: {palette.hover_fill};
        }}
        QToolButton#Message_Action_Button {{
            color: {palette.primary_text};
            background: transparent;
            border: none;
            text-align: left;
            padding: 8px 10px;
            min-height: 28px;
            font-size: 9.5pt;
        }}
        QToolButton#Message_Action_Button:hover {{
            background: {palette.hover_fill};
            border-radius: 10px;
        }}
        /* Ensure popup content has sufficient contrast in dark mode */
        QFrame#Profile_Popup QLabel,
        QFrame#Profile_Popup QLineEdit,
        QFrame#Profile_Popup QPushButton#Sign_In_Button {{
            color: {palette.primary_text};
        }}
        QFrame#Profile_Popup QLineEdit {{
            background: {field_fill};
            border: 1px solid {palette.glass_border};
            border-radius: 10px;
            padding: 6px 10px;
            color: {palette.primary_text};
        }}
        QLabel {{
            color: {palette.secondary_text};
            font-size: {self.scaled_font_size}pt;
        }}
        QLabel#Setup_Title,
        QLabel#Chat_Title {{
            color: {palette.primary_text};
            font-size: 11pt;
            font-weight: 700;
        }}
        QLabel#Chat_Header_Avatar {{
            color: {palette.primary_text};
            background: {self._css_color(palette.incoming_bubble, 242) if use_backdrop else palette.incoming_bubble};
            border-radius: 17px;
            font-size: 9.5pt;
            font-weight: 800;
        }}
        QLabel#Header_Username {{
            color: {palette.secondary_text};
            font-size: 7.5pt;
            font-weight: 600;
        }}
        QLabel#Setup_Section_Label {{
            color: {palette.secondary_text};
            font-size: 8pt;
            font-weight: 700;
            letter-spacing: 0px;
            padding-top: 4px;
        }}
        QLabel#Chat_Subtitle {{
            color: {palette.secondary_text};
            font-size: 7.5pt;
        }}
        QLabel#Message_Sender {{
            color: {palette.secondary_text};
            font-size: 7.5pt;
            font-weight: 600;
        }}
        QLabel#Message_Meta {{
            color: {palette.secondary_text};
            font-size: 7pt;
        }}
        QLabel#Server_Connection_Status {{
            color: {palette.secondary_text};
            background: {system_bubble};
            border: none;
            border-radius: 11px;
            padding: 5px 10px;
            font-size: 8pt;
            font-weight: 600;
        }}
        QLineEdit, QComboBox {{
            min-height: 34px;
            color: {palette.primary_text};
            background: {field_fill};
            border: 1px solid {palette.glass_border};
            border-radius: 12px;
            padding: 3px 38px 3px 12px;
            selection-background-color: {palette.accent_blue};
            font-size: {self.scaled_font_size}pt;
        }}
        QLineEdit#Search_Field {{
            min-height: 28px;
            background: {system_bubble};
            border: none;
            border-radius: 16px;
            padding: 6px 12px 6px 8px;
            font-size: 9pt;
        }}
        QLabel#Sidebar_Section_Label {{
            color: {palette.secondary_text};
            font-size: 7.5pt;
            font-weight: 700;
            padding: 4px 2px 0 2px;
            text-transform: uppercase;
        }}
        QLineEdit {{
            padding-right: 12px;
        }}
        QLineEdit:disabled, QComboBox:disabled {{
            color: {palette.secondary_text};
            background: {glass_fill};
            border-color: {palette.glass_border};
        }}
        QFrame#Protocol_Switch {{
            background: {field_fill};
            border: 1px solid {palette.glass_border};
            border-radius: 16px;
        }}
        QPushButton#Protocol_TCP_Button,
        QPushButton#Protocol_UDP_Button {{
            color: {palette.secondary_text};
            background: transparent;
            border: none;
            border-radius: 12px;
            min-height: 30px;
            padding: 4px 12px;
            font-weight: 700;
        }}
        QPushButton#Protocol_TCP_Button:checked,
        QPushButton#Protocol_UDP_Button:checked {{
            color: {palette.primary_text};
            background: {system_bubble};
            border: 1px solid {palette.glass_border};
        }}
        QScrollArea#Setup_Scroll,
        QWidget#Setup_Content {{
            background: transparent;
            border: none;
        }}
        QCheckBox#Auto_Server_Checkbox {{
            color: {palette.secondary_text};
            spacing: 8px;
            font-size: 9pt;
        }}
        QPushButton {{
            color: {palette.primary_text};
            background: transparent;
            border: none;
            border-radius: 10px;
            padding: 4px;
        }}
        QPushButton:hover {{
            background: {palette.hover_fill};
        }}
        QPushButton:checked {{
            background: {palette.selected_fill};
        }}
        QPushButton:disabled {{
            color: {palette.secondary_text};
        }}
        QPushButton#Setup_Button,
        QPushButton#New_Message_Button,
        QPushButton#Server_Button,
        QPushButton#Sign_In_Button,
        QPushButton#Chat_Confirm_Button,
        QPushButton#Avatar_Previous_Button,
        QPushButton#Avatar_Next_Button {{
            border: 1px solid {palette.glass_border};
            border-radius: 14px;
            padding: 6px 12px;
            font-weight: 700;
            background: {field_fill};
        }}
        QPushButton#Setup_Button:hover,
        QPushButton#New_Message_Button:hover {{
            background: {system_bubble};
        }}
        QPushButton#Setup_Button {{
            min-width: 34px;
            max-width: 34px;
        }}
        QPushButton#New_Message_Button {{
            min-width: 34px;
            max-width: 34px;
        }}
        QPushButton#Server_Button,
        QPushButton#Sign_In_Button {{
            color: #FFFFFF;
            background: {palette.accent_blue};
            border-color: {palette.accent_blue};
        }}
        QPushButton#Server_Button:checked,
        QPushButton#Sign_In_Button:checked {{
            background: {palette.danger_fill};
            border-color: {palette.danger_fill};
        }}
        QPushButton#Attach_Button,
        QPushButton#Emoji_Button {{
            color: {palette.primary_text};
            background: {self._css_color(palette.control_fill, 242) if use_backdrop else palette.control_fill};
            border: 1px solid {palette.glass_border};
            border-radius: 17px;
            font-weight: 700;
        }}
        QPushButton#Attach_Button:hover,
        QPushButton#Emoji_Button:hover {{
            background: {palette.hover_fill};
        }}
        QPushButton#Attach_Button:disabled,
        QPushButton#Emoji_Button:disabled {{
            background: {self._css_color(palette.control_fill, 242) if use_backdrop else palette.control_fill};
            border-color: {palette.glass_border};
        }}
        QListWidget#Conversation_List {{
            color: {palette.primary_text};
            background: transparent;
            border: none;
            outline: none;
            padding: 0;
        }}
        QListWidget#Conversation_List::item {{
            min-height: 58px;
            border: none;
            padding: 0;
            margin: 0;
        }}
        QListWidget#Conversation_List::item:selected {{
            background: transparent;
        }}
        QListWidget#Conversation_List::item:hover {{
            background: transparent;
        }}
        QWidget#Pinned_Widget {{
            background: transparent;
        }}
        QWidget#Chat_Area {{
            background: {app_background};
        }}
        QWidget#Chat_Header {{
            background: transparent;
            border-bottom: 1px solid {palette.separator};
        }}
        QListWidget#Chat_Log {{
            color: {palette.primary_text};
            background: transparent;
            border: none;
            outline: none;
            padding: 8px 8px 6px 8px;
        }}
        QListWidget#Chat_Log::item {{
            border: none;
            padding: 2px;
        }}
        QFrame#File_Card {{
            background: {system_bubble};
            border: 1px solid {palette.glass_border};
            border-radius: 16px;
            min-width: 220px;
        }}
        QFrame#Media_Card {{
            background: {system_bubble};
            border: 1px solid {palette.glass_border};
            border-radius: 18px;
            min-width: 220px;
        }}
        QLabel#File_Card_Title {{
            color: {palette.primary_text};
            font-weight: 700;
        }}
        QLabel#File_Card_Subtitle {{
            color: {palette.secondary_text};
            font-size: 8pt;
        }}
        QLabel#Media_Card_Image {{
            background: {glass_fill};
            border-radius: 14px;
        }}
        QPushButton#Reaction_Chip {{
            color: {palette.primary_text};
            background: {app_background};
            border: 1px solid {palette.glass_border};
            border-radius: 12px;
            padding: 3px 8px;
            font-size: 8pt;
        }}
        QPushButton#Reaction_Chip:hover {{
            background: {system_bubble};
        }}
        QPushButton#Reaction_Chip:checked {{
            background: {system_bubble};
            border-color: {palette.accent_blue};
        }}
        QLabel#Reaction_Badge {{
            color: {palette.primary_text};
            background: transparent;
            border: none;
            min-width: 40px;
            min-height: 44px;
            max-height: 44px;
            padding: 0;
            font-size: 12pt;
            font-weight: 700;
        }}
        QPushButton#Thread_Chip {{
            color: {palette.accent_blue_dark};
            background: transparent;
            border: none;
            font-size: 8pt;
            font-weight: 700;
            padding: 0 2px;
            text-align: left;
        }}
        QPushButton#Thread_Chip:hover {{
            color: {palette.accent_blue};
            text-decoration: underline;
        }}
        QFrame#Composer_Panel {{
            background: transparent;
            border: none;
        }}
        QFrame#Composer_Shell {{
            background: {composer_fill};
            border: 1px solid {palette.glass_border};
            border-radius: 23px;
        }}
        QLineEdit#Message_Field {{
            min-height: 38px;
            border: none;
            background: transparent;
            padding: 0 2px 0 6px;
            selection-background-color: {palette.accent_blue};
        }}
        QLineEdit#Message_Field:focus {{
            border: none;
        }}
        """

    def _refresh_status_text(self) -> None:
        server_text = "Connected" if self.server_connected else "Offline"
        self.server_connection_status.setText(server_text)
        self._set_presence()

    def _set_presence(self) -> None:
        # Update header username display
        display_name = self.username.text().strip()
        if self.user_signed_in and display_name:
            self.header_username.setText(display_name)
        elif display_name:
            self.header_username.setText(display_name)
        else:
            self.header_username.setText("Pick profile")

    def _commit_username_change(self) -> None:
        if not self.server_connected or not self.user_signed_in:
            self._set_presence()
            self._update_profile_action_state()
            return

        new_username = self.username.text().strip()
        if not new_username or new_username == self.active_username:
            self._set_presence()
            self._update_profile_action_state()
            return

        previous_username = self.active_username
        self.send_message(unregister_message(previous_username))
        self.send_message(register_message(new_username))
        self.active_username = new_username
        self._set_presence()
        self._refresh_status_text()
        self._update_profile_action_state()

    # Connection and sign-in workflow

    def connect_client(self) -> None:
        """Connect to or disconnect from the configured chat server."""
        protocol = self.protocol_selector.currentText()
        self._use_protocol(protocol)

        if self.server_button.isChecked():
            try:
                host, port = self._server_address()
            except ValueError:
                self._add_chat_text("Enter a valid port from 1 to 65535.", "system")
                self.server_button.setChecked(False)
                return
            self.socket.connectToHost(QtNetwork.QHostAddress(host), port)
            self.send_message(CONNECT, host, port)
            self.server_connected = True
            self.server_button.setText("Disconnect")
            self.host_address.setEnabled(False)
            self.port_number.setEnabled(False)
            self._set_protocol_controls_enabled(False)
            self.user_avatar.setEnabled(True)
            self.username.setEnabled(True)
            self._update_profile_action_state()
            self.message_field.setText("Waiting for sign-in...")
            self.chat_subtitle.setText(f"Connected to {host}:{port}; sign in to start")
            self._refresh_status_text()
        else:
            self._disconnect_client_session()

    def _disconnect_client_session(self) -> None:
        if self.server_connected:
            try:
                self.send_message(DISCONNECT)
            except Exception:
                pass

        self.socket.blockSignals(True)
        self.socket.disconnect()
        if isinstance(self.socket, QtNetwork.QTcpSocket):
            self.socket.abort()
        else:
            self.socket.close()

        self.server_connected = False
        self.user_signed_in = False
        self.server_button.setText("Connect")
        self.server_button.setChecked(False)
        self.sign_in_button.setText("Sign in")
        self.sign_in_button.setChecked(False)
        self.host_address.setEnabled(True)
        self.port_number.setEnabled(True)
        self._set_protocol_controls_enabled(True)
        self.user_avatar.setEnabled(True)
        self.username.setEnabled(True)
        self._update_profile_action_state()
        self.message_field.setText("Disconnected! Good Bye...")
        self.message_field.setEnabled(False)
        self.attach_button.setEnabled(False)
        self.emoji_button.setEnabled(False)
        self.chat_subtitle.setText("Disconnected")
        self._set_conversations(["ALL"])
        self._refresh_status_text()

    def sign_in(self) -> None:
        """Send a sign-in or sign-out command and update the controls."""
        if self.sign_in_button.isChecked():
            username = self.username.text().strip()
            if not username or not self.active_avatar_name:
                self._add_chat_text("Choose a username and avatar before signing in.", "system")
                self.sign_in_button.setChecked(False)
                return
            self.send_message(register_message(self.username.text()))
            self.user_signed_in = True
            self.active_username = username
            self.sign_in_button.setText("Sign out")
            self.username.setEnabled(True)
            self.user_avatar.setEnabled(True)
            self.chat_confirm_button.setEnabled(True)
            self.message_field.setEnabled(True)
            self.message_field.setText("")
            self.message_field.setPlaceholderText("iMessage")
            self.chat_log.setEnabled(True)
            self.attach_button.setEnabled(self.protocol_selector.currentText() == "TCP")
            self.emoji_button.setEnabled(True)
            self._set_active_recipient(self.chat_selector.currentText() or "ALL")
            self._refresh_status_text()
            self._prime_chat_onboarding()
            self.profile_popup.hide()
        else:
            self.send_message(unregister_message(self.active_username))
            self.user_signed_in = False
            self.sign_in_button.setText("Sign in")
            self.username.setEnabled(True)
            self.user_avatar.setEnabled(True)
            self.chat_confirm_button.setEnabled(False)
            self.message_field.setText("Signed out")
            self.message_field.setEnabled(False)
            self.attach_button.setEnabled(False)
            self.emoji_button.setEnabled(False)
            self.chat_log.setEnabled(False)
            self.chat_subtitle.setText("Signed out")
            self._refresh_status_text()
            self.profile_popup.hide()

    def _prime_chat_onboarding(self) -> None:
        """Seed a small amount of local guidance so the first thread feels inhabited."""
        if self._seeded_onboarding or self.chat_log.count() > 1:
            return
        timestamp = self._time_label()
        self._add_chat_text(
            f"[{timestamp}] Texte: Start another client to begin a live local conversation.",
            "incoming",
            conversation="ALL",
        )
        self._add_chat_text(
            f"[{timestamp}] Texte: Try sending two quick messages in a row to see grouped bubbles.",
            "incoming",
            conversation="ALL",
        )
        self._add_chat_text(
            "Use the paperclip for images and the smile button for your OS emoji picker.",
            "system",
            conversation="ALL",
        )
        self._add_media_card(
            sender="Texte",
            path=Path(self._asset_path("messaging.png")),
            caption="Images can appear inline with reactions and thread hints.",
            reactions=["👍", "❤"],
            thread_label="2 replies",
            outgoing=False,
            conversation="ALL",
        )
        self._seeded_onboarding = True

    # Messaging and attachments

    def send_message(self, message: str, host: str | None = None, port: int | None = None) -> None:
        """Send a command or chat message through the selected transport."""
        try:
            host, port = self._server_address(host, port)
        except ValueError:
            self._add_chat_text("Enter a valid port from 1 to 65535.", "system")
            return

        protocol = self.protocol_selector.currentText()
        is_field_message = message.startswith(FIELD)
        payload = outgoing_payload(message)
        if is_field_message and payload.startswith("{FILE}") and protocol != "TCP":
            self._add_chat_text("File transfer is available in TCP mode only.", "system")
            return
        if (
            is_field_message
            and not payload.startswith("{FILE}")
            and not message_has_chat_text(payload)
        ):
            self._add_chat_text("Write a message before sending.", "system")
            return

        if isinstance(self.socket, QtNetwork.QUdpSocket):
            self.socket.writeDatagram(payload.encode(), QtNetwork.QHostAddress(host), port)
        else:
            self.socket.write(frame_message(payload))

        if is_field_message:
            self.message_field.setText("")
            self.message_field.setFocus()

    def receive_message(self) -> None:
        """Append server messages to the chat log."""
        if isinstance(self.socket, QtNetwork.QUdpSocket):
            while self.socket.hasPendingDatagrams():
                datagram = self.socket.receiveDatagram()
                payload = datagram.data()
                if not payload:
                    continue
                self._handle_server_message(qbytearray_to_text(payload).strip())
        else:
            if self.socket.bytesAvailable() > 0:
                self.tcp_buffer += qbytearray_to_text(self.socket.readAll())
                messages, self.tcp_buffer = split_frames(self.tcp_buffer)
                for message in messages:
                    self._handle_server_message(message)

    def chat_target(self) -> None:
        """Enable or disable message entry for the selected chat target."""
        self._set_active_recipient(self.chat_selector.currentText() or "ALL")

    def _send_chat_text(self) -> None:
        text = self.message_field.text()
        if not text.strip():
            return
        self.send_message(FIELD + chat_message(self.chat_selector.currentText() or "ALL", text))

    def _set_active_recipient(self, recipient: str) -> None:
        recipient = recipient or "ALL"
        self._sync_combo_text(self.chat_selector, recipient)
        self._sync_conversation_row(recipient)
        self._sync_pinned_selection(recipient)
        self.chat_title.setText(recipient)
        self.chat_header_avatar.setText(self._avatar_text(recipient))
        if self.user_signed_in:
            self.chat_subtitle.setText(f"Chatting with {recipient}")
        elif self.server_connected:
            self.chat_subtitle.setText("Connected; sign in to start")
        else:
            self.chat_subtitle.setText("Connect, sign in, then start chatting")
        self._render_conversation_history(recipient)
        self._refresh_conversation_rows()

    def _sync_combo_text(self, combo: QtWidgets.QComboBox, text: str) -> None:
        if combo.currentText() == text:
            return
        index = combo.findText(text)
        if index >= 0:
            combo.blockSignals(True)
            combo.setCurrentIndex(index)
            combo.blockSignals(False)

    def _sync_conversation_row(self, text: str) -> None:
        row = self._conversation_row_for(text)
        if row < 0:
            return
        if self.conversation_list.currentRow() == row:
            return
        self.conversation_list.blockSignals(True)
        self.conversation_list.setCurrentRow(row)
        self.conversation_list.blockSignals(False)

    def _sync_pinned_selection(self, recipient: str) -> None:
        for name, tile in self.pinned_tiles.items():
            tile.blockSignals(True)
            tile.setChecked(name == recipient)
            tile.blockSignals(False)

    def attach_picture(self) -> None:
        """Send a selected image attachment over TCP."""
        image_tuple = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Attach an Image",
            str(Path.cwd()),
            "Image files (*.jpg *.png *.gif *.svg)",
        )
        if not image_tuple[0]:
            return

        if self.protocol_selector.currentText() != "TCP":
            self._add_chat_text("Switch to TCP before sending an attachment.", "system")
            return

        path = Path(image_tuple[0])
        data = path.read_bytes()
        if len(data) > MAX_FILE_BYTES:
            limit = MAX_FILE_BYTES // 1_000_000
            self._add_chat_text(f"Attachment is too large. Limit: {limit} MB.", "system")
            return

        recipient = self.chat_selector.currentText() or "ALL"
        self.send_message(FIELD + file_message(recipient, path.name, data))
        self._add_media_card(
            sender=self.username.text().strip() or "You",
            path=path,
            caption=path.name,
            reactions=["Sent"],
            outgoing=True,
            conversation=recipient,
        )

    # Widget signals and avatar selection

    def _connect_signals(self) -> None:
        """Wire socket and widget events once."""
        self.socket.readyRead.connect(self.receive_message)
        app = QtWidgets.QApplication.instance()
        if isinstance(app, QtWidgets.QApplication):
            style_hints = app.styleHints()
            if style_hints is not None and hasattr(style_hints, "colorSchemeChanged"):
                style_hints.colorSchemeChanged.connect(self._handle_os_theme_changed)
        self.setup_button.clicked.connect(self._toggle_setup_sheet)
        self.setup_close_button.clicked.connect(lambda: self._toggle_setup_sheet(False))
        self.new_message_button.clicked.connect(self.focus_current_chat)
        self.server_button.clicked.connect(self.connect_client)
        self.protocol_tcp_button.clicked.connect(lambda: self._select_protocol("TCP"))
        self.protocol_udp_button.clicked.connect(lambda: self._select_protocol("UDP"))
        self.avatar_previous_button.clicked.connect(self.previous_avatar_page)
        self.avatar_next_button.clicked.connect(self.next_avatar_page)
        self.sign_in_button.clicked.connect(self.sign_in)
        self.user_avatar.clicked.connect(self.toggle_profile_popup)
        self.username.textChanged.connect(lambda _text: self._update_profile_action_state())
        self.username.returnPressed.connect(self._commit_username_change)
        self.username.editingFinished.connect(self._commit_username_change)
        if hasattr(self.theme_switch, "themeSelected"):
            self.theme_switch.themeSelected.connect(self._apply_theme_preference)
        self.chat_selector.currentTextChanged.connect(self._set_active_recipient)
        self.conversation_list.currentItemChanged.connect(self._conversation_changed)
        self.message_field.returnPressed.connect(self._send_chat_text)
        self.attach_button.clicked.connect(self.attach_picture)
        self.emoji_button.clicked.connect(self.open_native_emoji_picker)

    def _handle_os_theme_changed(self, _scheme) -> None:
        if self.theme_preference is None:
            self._apply_theme_preference(None)

    def focus_current_chat(self) -> None:
        """Focus the active composer when possible, otherwise focus the search field."""
        if self.message_field.isEnabled():
            self.message_field.setFocus()
        else:
            self.search_field.setFocus()

    def open_native_emoji_picker(self) -> None:
        """Open the operating system emoji picker when one is available."""
        if not self.message_field.isEnabled():
            return
        self.message_field.setFocus()
        if self._show_native_emoji_picker():
            return
        self._add_chat_text("Native emoji picker is not available on this platform.", "system")

    def _show_native_emoji_picker(self) -> bool:
        system = platform.system()
        if system == "Windows":
            return self._show_windows_emoji_picker()
        if system == "Darwin":
            return self._show_macos_emoji_picker()
        return False

    def _show_windows_emoji_picker(self) -> bool:
        try:
            import ctypes

            user32 = ctypes.windll.user32
            keybd_event = user32.keybd_event
            keybd_event(0x5B, 0, 0, 0)
            keybd_event(0xBE, 0, 0, 0)
            keybd_event(0xBE, 0, 0x0002, 0)
            keybd_event(0x5B, 0, 0x0002, 0)
            return True
        except Exception:
            return False

    def _show_macos_emoji_picker(self) -> bool:
        try:
            subprocess.run(
                [
                    "osascript",
                    "-e",
                    'tell application "System Events" to key code 49 using {control down, command down}',
                ],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return True
        except Exception:
            return False

    def _toggle_setup_sheet(self, checked: bool) -> None:
        self.profile_popup.hide()
        self._position_setup_sheet()
        self.setup_sheet.setVisible(checked)
        if checked:
            self.setup_sheet.raise_()
        self.setup_button.setChecked(checked)

    def _position_setup_sheet(self) -> None:
        if not hasattr(self, "sidebar") or not hasattr(self, "setup_sheet"):
            return
        margin = 8
        x = margin
        y = 66
        width = max(260, self.sidebar.width() - (margin * 2))
        height = max(360, self.sidebar.height() - y - margin)
        self.setup_sheet.setGeometry(x, y, width, height)

    def toggle_profile_popup(self) -> None:
        if self.profile_popup.isVisible():
            self.profile_popup.hide()
            return
        self.setup_sheet.setVisible(False)
        self.setup_button.setChecked(False)
        popup_width = max(self.profile_popup.minimumWidth(), self.profile_popup.sizeHint().width())
        x = self.width() - popup_width - 18
        y = self.chat_header.y() + self.chat_header.height() + 8
        self.profile_popup.resize(popup_width, self.profile_popup.sizeHint().height())
        self.profile_popup.move(
            max(12, x),
            y,
        )
        self.profile_popup.show()
        self.profile_popup.raise_()

    def eventFilter(
        self,
        watched: QtCore.QObject | None,
        event: QtCore.QEvent | None,
    ) -> bool:
        if event is None:
            return super().eventFilter(watched, event)
        if event.type() == QtCore.QEvent.Type.MouseButtonPress:
            if self.profile_popup.isVisible():
                mouse_event = event
                if isinstance(mouse_event, QtGui.QMouseEvent):
                    global_pos = mouse_event.globalPosition().toPoint()
                    if not self._click_inside_any_popup(global_pos):
                        self.profile_popup.hide()
                        if self.avatar_selector_panel.isVisible():
                            self.avatar_selector_panel.hide()
            if (self.reaction_bar_popup is not None and self.reaction_bar_popup.isVisible()) or (
                self.message_options_popup is not None and self.message_options_popup.isVisible()
            ):
                mouse_event = event
                if isinstance(mouse_event, QtGui.QMouseEvent):
                    global_pos = mouse_event.globalPosition().toPoint()
                    if not self._click_inside_any_popup(global_pos):
                        self._hide_message_action_popup()
        return super().eventFilter(watched, event)

    def _click_inside_any_popup(self, global_pos: QtCore.QPoint) -> bool:
        widgets = [
            self.profile_popup,
            self.avatar_selector_panel,
            self.user_avatar,
            self.reaction_bar_popup,
            self.message_options_popup,
        ]
        for widget in widgets:
            if widget is not None and widget.isVisible():
                local_pos = widget.mapFromGlobal(global_pos)
                if widget.rect().contains(local_pos):
                    return True
        return False

    def open_avatar_selector(self) -> None:
        """Show or hide the avatar selector."""
        if self.avatar_selector_panel.isVisible():
            self.avatar_selector_panel.hide()
            return
        self._position_avatar_selector_popup()
        self.avatar_selector_panel.show()
        self.avatar_selector_panel.raise_()
        self.avatar_selector_panel.activateWindow()
        self.update_avatar_navigation()

    def _position_avatar_selector_popup(self) -> None:
        if not hasattr(self, "temporary_avatar"):
            return
        anchor = self.temporary_avatar.mapToGlobal(QtCore.QPoint(0, self.temporary_avatar.height()))
        popup_width = max(
            self.avatar_selector_panel.sizeHint().width(),
            self.avatar_selector_panel.minimumWidth(),
        )
        popup_height = self.avatar_selector_panel.sizeHint().height()
        screen = QtGui.QGuiApplication.screenAt(anchor)
        if screen is not None:
            available = screen.availableGeometry()
            x = min(
                max(anchor.x() - popup_width + self.temporary_avatar.width(), available.left()),
                available.right() - popup_width,
            )
            y = min(max(anchor.y() + 8, available.top()), available.bottom() - popup_height)
        else:
            x = anchor.x() - popup_width + self.temporary_avatar.width()
            y = anchor.y() + 8
        self.avatar_selector_panel.resize(popup_width, popup_height)
        self.avatar_selector_panel.move(max(12, x), max(12, y))

    def choose_avatar(self, avatar_name: str) -> None:
        """Use a selected bundled avatar for the visible user identity."""
        icon = self._icon("avatars", f"{avatar_name}.svg")
        self.user_avatar.setIcon(icon)
        self.user_avatar.setObjectName(avatar_name)
        self.temporary_avatar.setIcon(icon)
        self.active_avatar_name = avatar_name
        self.avatar_selector_panel.setVisible(False)
        self.user_avatar.setChecked(False)
        self._update_profile_action_state()
        self._set_presence()

    def previous_avatar_page(self) -> None:
        """Show the previous avatar page when one exists."""
        self._set_avatar_page(self.avatar_selector_widget.currentIndex() - 1)

    def next_avatar_page(self) -> None:
        """Show the next avatar page when one exists."""
        self._set_avatar_page(self.avatar_selector_widget.currentIndex() + 1)

    def _set_avatar_page(self, page_index: int) -> None:
        page_count = self.avatar_selector_widget.count()
        if page_count == 0:
            return
        clamped_index = max(0, min(page_index, page_count - 1))
        self.avatar_selector_widget.setCurrentIndex(clamped_index)
        self.update_avatar_navigation()

    def update_avatar_navigation(self) -> None:
        page_count = self.avatar_selector_widget.count()
        current_page = self.avatar_selector_widget.currentIndex()
        self.avatar_previous_button.setEnabled(current_page > 0)
        self.avatar_next_button.setEnabled(current_page < page_count - 1)

    # Incoming messages and rendering

    def _handle_server_message(self, message: str) -> None:
        file_delivery = parse_file_delivery(message)
        if file_delivery is not None:
            self._save_file_delivery(
                file_delivery.sender, file_delivery.filename, file_delivery.data
            )
            return

        users = users_payload(message)
        if users is not None:
            self._update_users(users)
            return

        text = display_text(message)
        if text is not None:
            if message.startswith(ERROR):
                self._add_chat_text(
                    text,
                    "system",
                    conversation=self.chat_selector.currentText() or "ALL",
                )
                return
            kind, conversation = self._message_route(text)
            self._add_chat_text(text, kind, conversation=conversation)

    def _message_route(self, text: str) -> tuple[str, str]:
        details = self._parse_display_message(text, "incoming")
        sender = str(details.get("sender") or "").strip()
        recipient = str(details.get("recipient") or "").strip()
        username = self.username.text().strip().casefold()
        if recipient and recipient != "ALL":
            if sender.casefold() == username:
                return "outgoing", recipient
            if recipient.casefold() == username:
                return "incoming", sender or recipient
            return "incoming", recipient
        if sender and sender.casefold() == username:
            return "outgoing", "ALL"
        return "incoming", "ALL"

    def _update_users(self, usernames: list[str]) -> None:
        current = self.chat_selector.currentText()
        own_name = self.username.text().strip().casefold()
        recipients = ["ALL"] + [
            username for username in usernames if username.casefold() != own_name
        ]

        self.chat_selector.blockSignals(True)
        self.chat_selector.clear()
        self.chat_selector.addItems(recipients)
        if current in recipients:
            self.chat_selector.setCurrentText(current)
        self.chat_selector.blockSignals(False)
        self._set_conversations(recipients)

    def _set_conversations(self, recipients: list[str]) -> None:
        current_item = self.conversation_list.currentItem()
        current = self._conversation_name(current_item) if current_item is not None else "ALL"
        self.conversation_list.blockSignals(True)
        self.conversation_list.clear()
        for recipient in recipients:
            item = ConversationListItem(recipient)
            row = ConversationRow(
                recipient,
                self._conversation_preview(recipient),
                self._conversation_time(recipient),
                self._avatar_text(recipient),
            )
            item.setSizeHint(row.sizeHint())
            self.conversation_list.addItem(item)
            self.conversation_list.setItemWidget(item, row)
        selected = current if current in recipients else "ALL"
        selected_row = self._conversation_row_for(selected)
        self.conversation_list.setCurrentRow(selected_row if selected_row >= 0 else 0)
        self.conversation_list.blockSignals(False)
        self._rebuild_pinned_conversations(recipients)
        self._set_active_recipient(selected)

    def _conversation_changed(
        self,
        current: QtWidgets.QListWidgetItem | None,
        _previous: QtWidgets.QListWidgetItem | None,
    ) -> None:
        if current is None:
            return
        self._set_active_recipient(self._conversation_name(current))

    def _conversation_name(self, item: QtWidgets.QListWidgetItem) -> str:
        value = item.data(QtCore.Qt.ItemDataRole.UserRole)
        return str(value or item.text() or "ALL")

    def _conversation_row_for(self, name: str) -> int:
        for index in range(self.conversation_list.count()):
            item = self.conversation_list.item(index)
            if item is not None and self._conversation_name(item) == name:
                return index
        return -1

    def _conversation_preview(self, recipient: str) -> str:
        if recipient in self.conversation_previews:
            return self.conversation_previews[recipient]
        if recipient == "ALL":
            return "Local room"
        if self.user_signed_in:
            return "Tap to start chatting"
        return "Sign in to message"

    def _conversation_time(self, recipient: str) -> str:
        if recipient in self.conversation_times:
            return self.conversation_times[recipient]
        return "Now" if recipient == "ALL" else ""

    def _avatar_text(self, recipient: str) -> str:
        stripped = recipient.strip()
        return "#" if stripped == "ALL" else (stripped[:1].upper() or "?")

    def _refresh_conversation_rows(self) -> None:
        palette = getattr(self, "current_palette", theme_palette("Light"))
        if palette is None:
            return
        current_row = self.conversation_list.currentRow()
        for index in range(self.conversation_list.count()):
            item = self.conversation_list.item(index)
            if item is None:
                continue
            row_widget = self.conversation_list.itemWidget(item)
            if isinstance(row_widget, ConversationRow):
                row_widget.apply_palette(palette, selected=index == current_row)
        for name, tile in self.pinned_tiles.items():
            tile.apply_palette(
                palette, selected=name == (self.chat_selector.currentText() or "ALL")
            )

    def _touch_conversation(self, recipient: str, preview: str) -> None:
        cleaned_preview = preview.strip() or self._conversation_preview(recipient)
        self.conversation_previews[recipient] = cleaned_preview[:52]
        self.conversation_times[recipient] = self._time_label()
        self._refresh_conversation_content()

    def _store_conversation_entry(self, recipient: str, entry: dict[str, object]) -> None:
        self.conversation_history.setdefault(recipient or "ALL", []).append(entry)

    def _update_message_reaction(
        self, recipient: str, entry: dict[str, object], reaction: str
    ) -> None:
        reactions = entry_strings(entry, "reactions")
        if reactions == [reaction]:
            reactions = []
        else:
            reactions = [reaction]
        entry["reactions"] = reactions
        self._hide_message_action_popup()
        if self.chat_selector.currentText() == (recipient or "ALL"):
            self._render_conversation_history(recipient)
        self._refresh_conversation_content()

    def _hide_message_action_popup(self) -> None:
        if self.reaction_bar_popup is not None:
            self.reaction_bar_popup.hide()
            self.reaction_bar_popup.deleteLater()
            self.reaction_bar_popup = None
        if self.message_options_popup is not None:
            self.message_options_popup.hide()
            self.message_options_popup.deleteLater()
            self.message_options_popup = None

    def _show_message_action_popup(
        self,
        anchor: QtWidgets.QWidget,
        *,
        entry: dict[str, object],
        sender: str,
        conversation: str,
    ) -> None:
        self._hide_message_action_popup()

        popup = ReactionBarPopup(self)
        body_text = entry_text(entry, "text")
        popup.reactionChosen.connect(
            lambda emoji: self._update_message_reaction(conversation, entry, emoji)
        )

        self.reaction_bar_popup = popup
        popup.adjustSize()
        self._position_message_action_popup(popup, anchor)
        popup.show()
        popup.raise_()
        self._show_message_options_popup(anchor, body_text=body_text, sender=sender)

    def _open_message_reaction_bar(
        self,
        anchor: QtWidgets.QWidget,
        entry: dict[str, object],
        sender: str,
        conversation: str,
    ) -> None:
        self._show_message_action_popup(
            anchor,
            entry=entry,
            sender=sender,
            conversation=conversation,
        )

    def _show_message_options_popup(
        self,
        anchor: QtWidgets.QWidget,
        *,
        body_text: str,
        sender: str,
    ) -> None:
        if self.message_options_popup is not None:
            self.message_options_popup.hide()
            self.message_options_popup.deleteLater()
            self.message_options_popup = None

        popup = MessageOptionsPopup(self)
        popup.replyRequested.connect(lambda: self._prepare_reply(sender, body_text))
        popup.stickerRequested.connect(lambda: self._show_sticker_placeholder(body_text))
        popup.copyRequested.connect(lambda: self._copy_text_to_clipboard(body_text))
        popup.translateRequested.connect(lambda: self._show_translate_placeholder(body_text))
        popup.moreRequested.connect(lambda: self._show_message_details(body_text, sender))

        self.message_options_popup = popup
        popup.adjustSize()
        self._position_message_options_popup(popup, anchor)
        popup.show()
        popup.raise_()

    def _position_message_action_popup(
        self,
        popup: QtWidgets.QWidget,
        anchor: QtWidgets.QWidget,
    ) -> None:
        anchor_top_left = anchor.mapToGlobal(QtCore.QPoint(0, 0))
        anchor_rect = anchor.rect()
        popup_size = popup.sizeHint()
        popup.resize(popup_size)

        x = anchor_top_left.x() + (anchor_rect.width() - popup_size.width()) // 2
        y_above = anchor_top_left.y() - popup_size.height() - 10
        y_below = anchor_top_left.y() + anchor_rect.height() + 8

        screen = QtWidgets.QApplication.screenAt(anchor_top_left)
        available = screen.availableGeometry() if screen is not None else self.geometry()
        y = y_above if y_above >= available.top() + 8 else y_below
        x = max(available.left() + 8, min(x, available.right() - popup_size.width() - 8))
        if y + popup_size.height() > available.bottom() - 8:
            y = max(available.top() + 8, available.bottom() - popup_size.height() - 8)

        popup.move(self.mapFromGlobal(QtCore.QPoint(x, y)))

    def _position_message_options_popup(
        self,
        popup: QtWidgets.QWidget,
        anchor: QtWidgets.QWidget,
    ) -> None:
        anchor_top_left = anchor.mapToGlobal(QtCore.QPoint(0, 0))
        anchor_rect = anchor.rect()
        popup_size = popup.sizeHint()
        popup.resize(popup_size)

        x = anchor_top_left.x()
        y = anchor_top_left.y() + anchor_rect.height() + 14

        screen = QtWidgets.QApplication.screenAt(anchor_top_left)
        available = screen.availableGeometry() if screen is not None else self.geometry()
        x = max(available.left() + 8, min(x, available.right() - popup_size.width() - 8))
        y = max(available.top() + 8, min(y, available.bottom() - popup_size.height() - 8))
        popup.move(self.mapFromGlobal(QtCore.QPoint(x, y)))

    def _position_reaction_badge(
        self,
        container: QtWidgets.QWidget,
        bubble: QtWidgets.QWidget,
        badge: QtWidgets.QLabel,
    ) -> None:
        bubble_top_right = bubble.mapTo(container, QtCore.QPoint(bubble.width(), 0))
        badge_size = badge.sizeHint()
        x = bubble_top_right.x() - int(badge_size.width() * 1.22)
        y = max(0, bubble_top_right.y() - int(badge_size.height() * 0.62))
        badge.move(x, y)
        badge.raise_()

    def _prepare_reply(self, sender: str, body_text: str) -> None:
        self._hide_message_action_popup()
        reply_text = f"> {sender}: {body_text}\n"
        if self.message_field.text().strip():
            self.message_field.setText(f"{self.message_field.text().rstrip()}\n{reply_text}")
        else:
            self.message_field.setText(reply_text)
        self.message_field.setFocus()
        self.message_field.setCursorPosition(len(self.message_field.text()))

    def _show_translate_placeholder(self, body_text: str) -> None:
        self._hide_message_action_popup()
        QtWidgets.QMessageBox.information(
            self,
            "Translate",
            f"Translation is not implemented yet.\n\nMessage:\n{body_text}",
        )

    def _show_sticker_placeholder(self, body_text: str) -> None:
        self._hide_message_action_popup()
        QtWidgets.QMessageBox.information(
            self,
            "Add Sticker",
            f"Sticker placement is not implemented yet.\n\nMessage:\n{body_text}",
        )

    def _copy_text_to_clipboard(self, text: str | None = None) -> None:
        clipboard = QtGui.QGuiApplication.clipboard()
        assert clipboard is not None
        clipboard.setText(text or "")

    def _show_message_details(self, body_text: str, sender: str) -> None:
        self._hide_message_action_popup()
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Message Options")
        dialog.resize(380, 220)

        layout = QtWidgets.QVBoxLayout(dialog)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        title = QtWidgets.QLabel(f"From {sender}")
        title.setStyleSheet("font-size: 11pt; font-weight: 700;")
        layout.addWidget(title)

        message = QtWidgets.QLabel(body_text)
        message.setWordWrap(True)
        message.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)
        layout.addWidget(message, 1)

        buttons = QtWidgets.QHBoxLayout()
        buttons.addStretch(1)
        close_button = QtWidgets.QPushButton("Close")
        close_button.clicked.connect(dialog.accept)
        buttons.addWidget(close_button)
        layout.addLayout(buttons)

        dialog.exec()

    def _render_conversation_history(self, recipient: str) -> None:
        self.chat_log.clear()
        self._last_message_kind = None
        self._last_message_sender = None
        for entry in self.conversation_history.get(recipient or "ALL", []):
            entry_type = str(entry.get("type", "text"))
            if entry_type == "media":
                path_value = entry_text(entry, "path")
                if not path_value:
                    continue
                self._add_media_card(
                    sender=str(entry.get("sender", recipient)),
                    path=Path(path_value),
                    caption=entry_text(entry, "caption"),
                    reactions=entry_strings(entry, "reactions"),
                    thread_label=entry_text(entry, "thread_label") or None,
                    outgoing=entry_bool(entry, "outgoing"),
                    conversation=recipient,
                    store=False,
                )
            elif entry_type == "file":
                self._add_file_card(
                    sender=str(entry.get("sender", recipient)),
                    filename=entry_text(entry, "filename"),
                    byte_count=entry_int(entry, "byte_count"),
                    conversation=recipient,
                    store=False,
                )
            else:
                self._add_chat_text(
                    entry_text(entry, "text"),
                    str(entry.get("kind", "incoming")),
                    conversation=recipient,
                    reactions=entry_strings(entry, "reactions"),
                    entry=entry,
                    store=False,
                )
        self.chat_log.scrollToBottom()

    def _refresh_conversation_content(self) -> None:
        for index in range(self.conversation_list.count()):
            item = self.conversation_list.item(index)
            if item is None:
                continue
            recipient = self._conversation_name(item)
            row_widget = self.conversation_list.itemWidget(item)
            if isinstance(row_widget, ConversationRow):
                row_widget.preview.setText(self._conversation_preview(recipient))
                row_widget.time.setText(self._conversation_time(recipient))
        for name, tile in self.pinned_tiles.items():
            tile.title.setText(name)

    def _time_label(self) -> str:
        now = datetime.now()
        return now.strftime("%I:%M %p").lstrip("0")

    def _rebuild_pinned_conversations(self, recipients: list[str]) -> None:
        while self.pinned_layout.count():
            item = self.pinned_layout.takeAt(0)
            if item is None:
                continue
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        self.pinned_tiles.clear()
        pinned_recipients = [recipient for recipient in recipients if recipient != "ALL"][:6]
        show_pinned = len(pinned_recipients) >= 3
        self.pinned_widget.setVisible(show_pinned)
        self.pinned_title.setVisible(show_pinned)
        if not show_pinned:
            return
        for index, recipient in enumerate(pinned_recipients):
            tile = PinnedConversationTile(
                recipient, self._avatar_text(recipient), self.pinned_widget
            )
            tile.clicked.connect(
                lambda _checked=False, name=recipient: self._set_active_recipient(name)
            )
            row, column = divmod(index, 3)
            self.pinned_layout.addWidget(tile, row, column)
            self.pinned_tiles[recipient] = tile
        self._refresh_conversation_rows()

    def _add_chat_text(
        self,
        text: str,
        kind: str = "incoming",
        *,
        conversation: str | None = None,
        reactions: list[str] | None = None,
        entry: dict[str, object] | None = None,
        store: bool = True,
    ) -> None:
        target_conversation = conversation or "ALL"
        if entry is None:
            entry = {"type": "text", "text": text, "kind": kind, "reactions": list(reactions or [])}
        if store:
            self._store_conversation_entry(target_conversation, entry)

        item = QtWidgets.QListWidgetItem()
        details = self._parse_display_message(text, kind)
        sender_name = str(details["sender"] or self.chat_title.text())
        grouped_with_previous = self._grouped_with_previous(kind, sender_name)
        bubble = QtWidgets.QFrame()
        bubble.setObjectName("Message_Bubble")
        bubble.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground, True)
        body_label = ReactionLabel(str(details["body"] or ""))
        body_label.setWordWrap(True)
        bubble.setMaximumWidth(self._bubble_width())
        body_label.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)

        palette = getattr(self, "current_palette", theme_palette("Dark"))
        if palette is None:
            raise RuntimeError("Dark theme is unavailable.")

        if kind == "system":
            bubble.setStyleSheet(
                f"QFrame#Message_Bubble {{ background: {palette.glass_fill}; "
                "border: none; border-radius: 12px; padding: 6px 12px;"
                "}"
            )
            # Use primary text for system messages to ensure contrast in dark themes
            body_label.setStyleSheet(f"color: {palette.primary_text}; background: transparent;")
            align = QtCore.Qt.AlignmentFlag.AlignHCenter
        elif kind == "outgoing":
            bubble.setStyleSheet(
                f"QFrame#Message_Bubble {{ background: {palette.outgoing_bubble}; "
                "border-radius: 17px; padding: 8px 12px;"
                "}"
            )
            body_label.setStyleSheet("color: #FFFFFF; background: transparent;")
            align = QtCore.Qt.AlignmentFlag.AlignRight
        else:
            bubble.setStyleSheet(
                f"QFrame#Message_Bubble {{ background: {palette.incoming_bubble}; "
                "border: none; border-radius: 17px; padding: 8px 12px;"
                "}"
            )
            body_label.setStyleSheet(f"color: {palette.primary_text}; background: transparent;")
            align = QtCore.Qt.AlignmentFlag.AlignLeft

        bubble_layout = QtWidgets.QVBoxLayout(bubble)
        bubble_layout.setContentsMargins(0, 0, 0, 0)
        bubble_layout.addWidget(body_label)

        current_reactions = entry_strings(entry, "reactions") or list(reactions or [])
        reaction_badge = None

        container = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(container)
        layout.setContentsMargins(0, 18, 0, 4)
        row = QtWidgets.QVBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(1 if grouped_with_previous else 2)

        show_sender = target_conversation == "ALL"
        if kind == "incoming" and details["sender"] and show_sender and not grouped_with_previous:
            sender_label = QtWidgets.QLabel(str(details["sender"]))
            sender_label.setObjectName("Message_Sender")
            # Reserve horizontal space for the avatar so the sender text can't peek out
            sender_row = QtWidgets.QHBoxLayout()
            sender_row.setContentsMargins(0, 0, 0, 0)
            sender_row.setSpacing(0)
            sender_row.addSpacing(36)  # avatar + gap
            sender_row.addWidget(sender_label, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
            row.addLayout(sender_row)

        bubble_row = QtWidgets.QHBoxLayout()
        bubble_row.setContentsMargins(0, 0, 0, 0)
        bubble_row.setSpacing(8 if not grouped_with_previous else 4)
        if align in (QtCore.Qt.AlignmentFlag.AlignHCenter, QtCore.Qt.AlignmentFlag.AlignRight):
            bubble_row.addStretch(1)

        if kind == "incoming" and show_sender:
            if grouped_with_previous:
                bubble_row.addSpacing(28)
            else:
                avatar = QtWidgets.QLabel(self._avatar_text(sender_name))
                avatar.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                avatar.setFixedSize(24, 24)
                avatar.setStyleSheet(
                    # Ensure avatar circle contrasts with current theme
                    f"color: {palette.primary_text}; background: {palette.incoming_bubble}; "
                    "border-radius: 12px; font-weight: 700; font-size: 8.5pt;"
                )
                bubble_row.addWidget(avatar, 0, QtCore.Qt.AlignmentFlag.AlignBottom)

        bubble_row.addWidget(bubble, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        if align in (QtCore.Qt.AlignmentFlag.AlignHCenter, QtCore.Qt.AlignmentFlag.AlignLeft):
            bubble_row.addStretch(1)
        row.addLayout(bubble_row)

        if kind == "outgoing":
            receipt = QtWidgets.QLabel("Read")
            receipt.setObjectName("Message_Meta")
            row.addWidget(receipt, 0, QtCore.Qt.AlignmentFlag.AlignRight)
        elif kind == "system" and details["time"]:
            system_time = QtWidgets.QLabel(str(details["time"]))
            system_time.setObjectName("Message_Meta")
            row.addWidget(system_time, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)

        layout.addLayout(row, 1)

        self.chat_log.addItem(item)
        self.chat_log.setItemWidget(item, container)
        item.setSizeHint(QtCore.QSize(0, container.sizeHint().height() + 4))
        if current_reactions:
            reaction_badge = QtWidgets.QLabel(current_reactions[0], container)
            reaction_badge.setObjectName("Reaction_Badge")
            reaction_badge.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            reaction_badge.setFont(emoji_font(14))
            reaction_badge.show()
            QtCore.QTimer.singleShot(
                0,
                lambda c=container, b=bubble, badge=reaction_badge: self._position_reaction_badge(
                    c, b, badge
                ),
            )
        if isinstance(body_label, ReactionLabel):
            body_label.click_handler = partial(
                self._open_message_reaction_bar,
                bubble,
                entry,
                sender_name,
                target_conversation,
            )
        else:
            body_label.clicked.connect(
                partial(
                    self._open_message_reaction_bar,
                    bubble,
                    entry,
                    sender_name,
                    target_conversation,
                )
            )
        if isinstance(body_label, ReactionLabel):
            body_label.reactionChosen.connect(
                partial(
                    self._update_message_reaction,
                    target_conversation,
                    entry,
                )
            )
        if target_conversation == (self.chat_selector.currentText() or "ALL"):
            self.chat_log.scrollToBottom()
        animate_entry(container)
        self._touch_conversation(target_conversation, str(details["body"] or ""))
        self._remember_last_message(kind, sender_name)

    def _parse_display_message(self, text: str, kind: str) -> dict[str, str | None]:
        if kind == "system":
            return {"time": self._time_label(), "sender": None, "recipient": None, "body": text}
        marker = "] "
        if text.startswith("[") and marker in text:
            time_text, rest = text.split(marker, 1)
            time_text = time_text.removeprefix("[")
            if ": " in rest:
                sender_field, message = rest.split(": ", 1)
                if " -> " in sender_field:
                    sender, recipient = sender_field.split(" -> ", 1)
                else:
                    sender, recipient = sender_field, "ALL"
                return {
                    "time": time_text,
                    "sender": sender,
                    "recipient": recipient,
                    "body": message,
                }
        return {"time": self._time_label(), "sender": None, "recipient": None, "body": text}

    def _grouped_with_previous(self, kind: str, sender: str) -> bool:
        return (
            kind in {"incoming", "outgoing"}
            and self._last_message_kind == kind
            and self._last_message_sender == sender
        )

    def _remember_last_message(self, kind: str, sender: str | None) -> None:
        self._last_message_kind = kind
        self._last_message_sender = sender

    def _open_media_preview(self, path: Path, caption: str) -> None:
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle(caption or path.name)
        dialog.resize(920, 680)

        layout = QtWidgets.QVBoxLayout(dialog)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(10)

        scroll = QtWidgets.QScrollArea(dialog)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)

        image_label = QtWidgets.QLabel()
        image_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        image_label.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.NoTextInteraction)
        image_label.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )

        reader = QtGui.QImageReader(str(path))
        reader.setAutoTransform(True)
        image = reader.read()
        if not image.isNull():
            pixmap = QtGui.QPixmap.fromImage(image)
            max_size = QtCore.QSize(1400, 1100)
            image_label.setPixmap(
                pixmap.scaled(
                    max_size,
                    QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                    QtCore.Qt.TransformationMode.SmoothTransformation,
                )
            )
        else:
            image_label.setText(path.name)

        scroll.setWidget(image_label)
        layout.addWidget(scroll, 1)

        subtitle = QtWidgets.QLabel(caption or path.name)
        subtitle.setObjectName("File_Card_Subtitle")
        subtitle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)

        dialog.exec()

    def _show_thread_preview(self, sender: str, thread_label: str, caption: str) -> None:
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle(thread_label)
        dialog.resize(420, 280)

        layout = QtWidgets.QVBoxLayout(dialog)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        heading = QtWidgets.QLabel(thread_label)
        heading.setStyleSheet("font-size: 12pt; font-weight: 700;")
        layout.addWidget(heading)

        hint = QtWidgets.QLabel(f"{sender} shared: {caption}")
        hint.setWordWrap(True)
        layout.addWidget(hint)

        replies = QtWidgets.QListWidget()
        replies.addItems(
            [
                "Jam: This preview should open as a separate thread pane later.",
                "Texte: For now this dialog proves the affordance is interactive.",
            ]
        )
        layout.addWidget(replies, 1)

        close_button = QtWidgets.QPushButton("Close")
        close_button.clicked.connect(dialog.accept)
        layout.addWidget(close_button, 0, QtCore.Qt.AlignmentFlag.AlignRight)

        dialog.exec()

    def _save_file_delivery(self, sender: str, filename: str, data: bytes) -> None:
        self.download_dir.mkdir(exist_ok=True)
        path = self._unique_download_path(filename)
        path.write_bytes(data)

        self._touch_conversation(sender, f"Sent {filename}")
        if path.suffix.lower() in IMAGE_SUFFIXES:
            self._add_media_card(
                sender=sender,
                path=path,
                caption=path.name,
                reactions=["View"],
                thread_label="Open from downloads",
                outgoing=False,
                conversation=sender,
            )
        else:
            self._add_file_card(sender, path.name, len(data), conversation=sender)

    def _add_file_card(
        self,
        sender: str,
        filename: str,
        byte_count: int,
        *,
        conversation: str | None = None,
        store: bool = True,
    ) -> None:
        target_conversation = conversation or sender or "ALL"
        if store:
            self._store_conversation_entry(
                target_conversation,
                {
                    "type": "file",
                    "sender": sender,
                    "filename": filename,
                    "byte_count": byte_count,
                },
            )
        item = QtWidgets.QListWidgetItem()
        card = QtWidgets.QFrame()
        card.setObjectName("File_Card")
        layout = QtWidgets.QVBoxLayout(card)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(2)

        title = QtWidgets.QLabel(filename)
        title.setObjectName("File_Card_Title")
        subtitle = QtWidgets.QLabel(f"{sender} sent {byte_count} bytes")
        subtitle.setObjectName("File_Card_Subtitle")
        layout.addWidget(title)
        layout.addWidget(subtitle)

        container = QtWidgets.QWidget()
        row = QtWidgets.QHBoxLayout(container)
        row.setContentsMargins(2, 5, 2, 5)
        row.addStretch(1)
        row.addWidget(card)
        row.addStretch(1)

        self.chat_log.addItem(item)
        self.chat_log.setItemWidget(item, container)
        item.setSizeHint(QtCore.QSize(0, card.sizeHint().height() + 14))
        if target_conversation == (self.chat_selector.currentText() or "ALL"):
            self.chat_log.scrollToBottom()
        animate_entry(container)
        self._remember_last_message("incoming", sender)

    def _add_media_card(
        self,
        *,
        sender: str,
        path: Path,
        caption: str,
        reactions: list[str] | None = None,
        thread_label: str | None = None,
        outgoing: bool,
        conversation: str | None = None,
        store: bool = True,
    ) -> None:
        target_conversation = conversation or (
            sender if not outgoing else (self.chat_selector.currentText() or "ALL")
        )
        if store:
            self._store_conversation_entry(
                target_conversation,
                {
                    "type": "media",
                    "sender": sender,
                    "path": str(path),
                    "caption": caption,
                    "reactions": list(reactions or []),
                    "thread_label": thread_label,
                    "outgoing": outgoing,
                },
            )
        item = QtWidgets.QListWidgetItem()
        container = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(container)
        layout.setContentsMargins(0, 6, 0, 6)
        layout.setSpacing(2)

        palette = getattr(self, "current_palette", theme_palette("Light"))
        if palette is None:
            return

        grouped_with_previous = self._grouped_with_previous(
            "outgoing" if outgoing else "incoming",
            sender,
        )
        show_sender = target_conversation == "ALL"
        if not outgoing and show_sender and not grouped_with_previous:
            sender_label = QtWidgets.QLabel(sender)
            sender_label.setObjectName("Message_Sender")
            layout.addWidget(sender_label, 0, QtCore.Qt.AlignmentFlag.AlignLeft)

        row = QtWidgets.QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(8 if not grouped_with_previous else 4)
        if outgoing:
            row.addStretch(1)

        if not outgoing and show_sender:
            if grouped_with_previous:
                row.addSpacing(28)
            else:
                avatar = QtWidgets.QLabel(self._avatar_text(sender))
                avatar.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                avatar.setFixedSize(24, 24)
                avatar.setStyleSheet(
                    f"color: {palette.primary_text}; background: {palette.system_bubble}; "
                    "border-radius: 12px; font-weight: 700; font-size: 8.5pt;"
                )
                row.addWidget(avatar, 0, QtCore.Qt.AlignmentFlag.AlignBottom)

        card = QtWidgets.QFrame()
        card.setObjectName("Media_Card")
        card_layout = QtWidgets.QVBoxLayout(card)
        card_layout.setContentsMargins(10, 10, 10, 10)
        card_layout.setSpacing(8)

        image = ClickableLabel()
        image.setObjectName("Media_Card_Image")
        image.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        image.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        image.setMinimumSize(220, 150)
        image.setMaximumWidth(min(self._bubble_width(), 420))
        image.setScaledContents(False)
        image.clicked.connect(lambda: self._open_media_preview(path, caption))

        reader = QtGui.QImageReader(str(path))
        reader.setAutoTransform(True)
        source_image = reader.read()
        if not source_image.isNull():
            pixmap = QtGui.QPixmap.fromImage(source_image)
            preview_width = min(self._bubble_width(), 420)
            image.setPixmap(
                pixmap.scaled(
                    QtCore.QSize(preview_width, 320),
                    QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                    QtCore.Qt.TransformationMode.SmoothTransformation,
                )
            )
        caption_label = QtWidgets.QLabel(caption)
        caption_label.setWordWrap(True)
        caption_label.setStyleSheet(
            "color: #FFFFFF;" if outgoing else f"color: {palette.primary_text};"
        )
        caption_label.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)

        if outgoing:
            card.setStyleSheet(
                f"QFrame#Media_Card {{ background: {palette.outgoing_bubble}; "
                "border: none; border-radius: 18px; }}"
            )
            image.setStyleSheet("border-radius: 14px; background: rgba(255, 255, 255, 0.08);")
        card_layout.addWidget(image)
        card_layout.addWidget(caption_label)
        row.addWidget(card, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        if not outgoing:
            row.addStretch(1)
        layout.addLayout(row)

        if reactions:
            reactions_row = QtWidgets.QHBoxLayout()
            reactions_row.setContentsMargins(34 if not outgoing else 0, 0, 4 if outgoing else 0, 0)
            reactions_row.setSpacing(6)
            if outgoing:
                reactions_row.addStretch(1)
            for reaction in reactions:
                chip = QtWidgets.QPushButton(reaction)
                chip.setObjectName("Reaction_Chip")
                chip.setCheckable(True)
                chip.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
                reactions_row.addWidget(chip)
            if not outgoing:
                reactions_row.addStretch(1)
            layout.addLayout(reactions_row)

        if thread_label:
            thread = QtWidgets.QPushButton(thread_label)
            thread.setObjectName("Thread_Chip")
            thread.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
            thread.clicked.connect(lambda: self._show_thread_preview(sender, thread_label, caption))
            layout.addWidget(
                thread,
                0,
                QtCore.Qt.AlignmentFlag.AlignRight
                if outgoing
                else QtCore.Qt.AlignmentFlag.AlignLeft,
            )

        self.chat_log.addItem(item)
        self.chat_log.setItemWidget(item, container)
        item.setSizeHint(QtCore.QSize(0, container.sizeHint().height() + 6))
        if target_conversation == (self.chat_selector.currentText() or "ALL"):
            self.chat_log.scrollToBottom()
        animate_entry(container)
        self._touch_conversation(target_conversation, caption)
        self._remember_last_message("outgoing" if outgoing else "incoming", sender)

    def _bubble_width(self) -> int:
        viewport = self.chat_log.viewport()
        if viewport is None:
            return 620
        viewport_width = viewport.width()
        if viewport_width <= 0:
            return 620
        return max(180, min(520, int(viewport_width * 0.58)))

    def closeEvent(self, event: QtGui.QCloseEvent | None) -> None:
        self._disconnect_client_session()
        super().closeEvent(event)

    def resizeEvent(self, event: QtGui.QResizeEvent | None) -> None:
        super().resizeEvent(event)
        self._position_setup_sheet()

    def showEvent(self, event: QtGui.QShowEvent | None) -> None:
        super().showEvent(event)
        theme_name = self.chat_theme.currentText() or "Light"
        self.native_backdrop_enabled = self._apply_native_backdrop(theme_name)
        self.setStyleSheet(self._app_style(self.current_palette))
        if not self._seeded_onboarding:
            self._seeded_onboarding = True
            self.toggle_profile_popup()

    def _unique_download_path(self, filename: str) -> Path:
        base = self.download_dir / Path(filename).name
        if not base.exists():
            return base

        stem = base.stem
        suffix = base.suffix
        for index in range(1, 10_000):
            candidate = self.download_dir / f"{stem}-{index}{suffix}"
            if not candidate.exists():
                return candidate
        raise RuntimeError("Could not create a unique attachment filename.")


def main() -> None:
    """Start the chat client application."""
    app = QtWidgets.QApplication(sys.argv)
    client = ChatClient()
    client.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
