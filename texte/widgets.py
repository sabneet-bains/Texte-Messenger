"""Small reusable widgets that give Texte its Messages-style shape."""

from collections.abc import Callable

from PyQt6 import QtCore, QtGui, QtSvg, QtWidgets

from texte.themes import ThemePalette


def emoji_font(point_size: int = 14) -> QtGui.QFont:
    font = QtGui.QFont()
    for family in ("Segoe UI Emoji", "Apple Color Emoji", "Noto Color Emoji", "Segoe UI Symbol"):
        if family in QtGui.QFontDatabase.families():
            font.setFamily(family)
            break
    font.setPointSize(point_size)
    return font


class ClickableLabel(QtWidgets.QLabel):
    """QLabel variant that emits a signal when clicked."""

    clicked = QtCore.pyqtSignal()

    def mousePressEvent(self, event: QtGui.QMouseEvent | None) -> None:
        if event is not None and event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.clicked.emit()
            event.accept()
            return
        super().mousePressEvent(event)


class ReactionLabel(QtWidgets.QLabel):
    """Selectable text label with a reaction context menu."""

    clicked = QtCore.pyqtSignal()
    reactionChosen = QtCore.pyqtSignal(str)

    def __init__(self, text: str = "", parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(text, parent)
        self.click_handler: Callable[[], None] | None = None

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent | None) -> None:
        if event is not None and event.button() == QtCore.Qt.MouseButton.LeftButton:
            if callable(self.click_handler):
                self.click_handler()
            else:
                self.clicked.emit()
            event.accept()
            return
        super().mouseReleaseEvent(event)

    def contextMenuEvent(self, event: QtGui.QContextMenuEvent | None) -> None:
        if event is None:
            return

        menu = QtWidgets.QMenu(self)

        try:
            selected_text = self.selectedText()
        except Exception:
            selected_text = ""

        if selected_text:
            copy_action = menu.addAction("Copy")
            assert copy_action is not None
            copy_action.triggered.connect(self._copy_selected_text(selected_text))

        try:
            has_all_text = bool(self.text())
            has_selection_api = True
        except Exception:
            has_all_text = False
            has_selection_api = False

        if has_selection_api and has_all_text:
            select_all_action = menu.addAction("Select All")
            assert select_all_action is not None
            select_all_action.triggered.connect(lambda: self.setSelection(0, len(self.text())))

        if menu.actions():
            menu.addSeparator()

        react_menu = menu.addMenu("React")
        assert react_menu is not None
        for emoji in ("👍", "❤", "😂", "😮", "😢", "👎"):
            action = react_menu.addAction(emoji)
            assert action is not None
            action.triggered.connect(
                lambda _checked=False, value=emoji: self.reactionChosen.emit(value)
            )

        menu.exec(event.globalPos())

    def _copy_selected_text(self, text: str) -> Callable[[], None]:
        clipboard = QtGui.QGuiApplication.clipboard()
        assert clipboard is not None
        return lambda: clipboard.setText(text)


class MessageActionPopup(QtWidgets.QFrame):
    """Floating bubble popover with emoji reactions and message actions."""

    reactionChosen = QtCore.pyqtSignal(str)
    replyRequested = QtCore.pyqtSignal()
    copyRequested = QtCore.pyqtSignal()
    translateRequested = QtCore.pyqtSignal()
    moreRequested = QtCore.pyqtSignal()

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("Message_Action_Popup")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground, True)
        self.hide()

        outer = QtWidgets.QVBoxLayout(self)
        outer.setContentsMargins(10, 10, 10, 10)
        outer.setSpacing(8)

        reactions_row = QtWidgets.QHBoxLayout()
        reactions_row.setContentsMargins(0, 0, 0, 0)
        reactions_row.setSpacing(6)
        for emoji in ("❤", "👍", "👎", "😂", "😮", "😢"):
            button = QtWidgets.QToolButton(self)
            button.setText(emoji)
            button.setObjectName("Message_Action_Emoji")
            button.setAutoRaise(True)
            button.clicked.connect(
                lambda _checked=False, value=emoji: self.reactionChosen.emit(value)
            )
            reactions_row.addWidget(button)
        outer.addLayout(reactions_row)

        actions = QtWidgets.QFrame(self)
        actions.setObjectName("Message_Action_List")
        action_layout = QtWidgets.QVBoxLayout(actions)
        action_layout.setContentsMargins(0, 0, 0, 0)
        action_layout.setSpacing(0)

        def add_action(text: str, signal: QtCore.pyqtBoundSignal) -> None:
            button = QtWidgets.QToolButton(actions)
            button.setText(text)
            button.setObjectName("Message_Action_Button")
            button.setAutoRaise(True)
            button.clicked.connect(lambda _checked=False: signal.emit())
            action_layout.addWidget(button)

        add_action("Reply", self.replyRequested)
        add_action("Copy", self.copyRequested)
        add_action("Translate", self.translateRequested)
        add_action("More…", self.moreRequested)

        outer.addWidget(actions)


class ReactionBarPopup(QtWidgets.QFrame):
    """Compact iMessage-style reaction strip."""

    reactionChosen = QtCore.pyqtSignal(str)

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("Reaction_Bar_Popup")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground, True)
        self.hide()
        self.setMinimumHeight(58)

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(14, 8, 14, 8)
        layout.setSpacing(10)

        for emoji in ("❤️", "👍", "👎", "😂", "‼️", "❓"):
            button = QtWidgets.QPushButton(self)
            button.setText(emoji)
            button.setObjectName("Reaction_Bar_Emoji")
            button.setFont(emoji_font(18))
            button.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
            button.setFlat(True)
            button.clicked.connect(
                lambda _checked=False, value=emoji: self.reactionChosen.emit(value)
            )
            layout.addWidget(button)


class MessageOptionsPopup(QtWidgets.QFrame):
    """Secondary popover for message actions like reply, copy, translate."""

    replyRequested = QtCore.pyqtSignal()
    stickerRequested = QtCore.pyqtSignal()
    copyRequested = QtCore.pyqtSignal()
    translateRequested = QtCore.pyqtSignal()
    moreRequested = QtCore.pyqtSignal()

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("Message_Options_Popup")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground, True)
        self.hide()
        self.setMinimumWidth(260)

        outer = QtWidgets.QVBoxLayout(self)
        outer.setContentsMargins(8, 8, 8, 8)
        outer.setSpacing(4)

        for text, signal in (
            ("Reply", self.replyRequested),
            ("Add Sticker", self.stickerRequested),
            ("Copy", self.copyRequested),
            ("Translate", self.translateRequested),
            ("More…", self.moreRequested),
        ):
            button = QtWidgets.QPushButton(text, self)
            button.setObjectName("Message_Options_Button")
            button.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(lambda _checked=False, sig=signal: sig.emit())
            outer.addWidget(button)


class TransientScrollStyle(QtWidgets.QProxyStyle):
    """Ask Qt to prefer transient platform scrollbars when supported."""

    def styleHint(
        self,
        hint: QtWidgets.QStyle.StyleHint,
        option: QtWidgets.QStyleOption | None = None,
        widget: QtWidgets.QWidget | None = None,
        return_data: QtWidgets.QStyleHintReturn | None = None,
    ) -> int:
        if hint == QtWidgets.QStyle.StyleHint.SH_ScrollBar_Transient:
            return 1
        return super().styleHint(hint, option, widget, return_data)


class SmoothListWidget(QtWidgets.QListWidget):
    """QListWidget with pixel-based smooth wheel scrolling."""

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)
        self.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scrollbar = self.verticalScrollBar()
        assert scrollbar is not None
        scrollbar.setSingleStep(18)
        self._wheel_animation = QtCore.QPropertyAnimation(scrollbar, b"value", self)
        self._wheel_animation.setDuration(140)
        self._wheel_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)

    def wheelEvent(self, event: QtGui.QWheelEvent | None) -> None:
        if event is None:
            return
        angle_delta = event.angleDelta().y()
        if angle_delta == 0:
            super().wheelEvent(event)
            return
        scrollbar = self.verticalScrollBar()
        assert scrollbar is not None
        step = max(40, scrollbar.singleStep() * 4)
        target = scrollbar.value() - int(angle_delta / 120) * step
        target = max(scrollbar.minimum(), min(target, scrollbar.maximum()))
        self._wheel_animation.stop()
        self._wheel_animation.setStartValue(scrollbar.value())
        self._wheel_animation.setEndValue(target)
        self._wheel_animation.start()
        event.accept()


class InvisibleItemDelegate(QtWidgets.QStyledItemDelegate):
    """Delegate that suppresses default item painting so item widgets fully control rendering."""

    def paint(
        self,
        painter: QtGui.QPainter | None,
        option: QtWidgets.QStyleOptionViewItem,
        index: QtCore.QModelIndex,
    ) -> None:
        # Intentionally do nothing; the associated item widget renders the row.
        if painter is None:
            return
        return

    def sizeHint(
        self,
        option: QtWidgets.QStyleOptionViewItem,
        index: QtCore.QModelIndex,
    ) -> QtCore.QSize:
        return super().sizeHint(option, index)


class ThemeModeSwitch(QtWidgets.QWidget):
    """Single-track light/dark switch with a sliding icon thumb."""

    themeSelected = QtCore.pyqtSignal(str)

    def __init__(
        self,
        light_icon_path: str,
        dark_icon_path: str,
        parent: QtWidgets.QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("Theme_Mode_Switch")
        self.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.setFixedSize(88, 44)

        self._theme: str = "Light"
        self._light_renderer = QtSvg.QSvgRenderer(light_icon_path, self)
        self._dark_renderer = QtSvg.QSvgRenderer(dark_icon_path, self)

    @property
    def theme(self) -> str:
        return self._theme

    def set_theme(self, theme: str) -> None:
        normalized = "Dark" if theme == "Dark" else "Light"
        if normalized == self._theme:
            self.update()
            return
        self._theme = normalized
        self.update()

    def mousePressEvent(self, event: QtGui.QMouseEvent | None) -> None:
        if event is not None and event.button() == QtCore.Qt.MouseButton.LeftButton:
            next_theme = "Dark" if self._theme == "Light" else "Light"
            self._theme = next_theme
            self.themeSelected.emit(next_theme)
            self.update()
            event.accept()
            return
        super().mousePressEvent(event)

    def paintEvent(self, event: QtGui.QPaintEvent | None) -> None:
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = self.rect().adjusted(1, 1, -1, -1)
        radius = rect.height() / 2

        if self._theme == "Light":
            track_fill = QtGui.QColor("#FCE9A2")
            track_border = QtGui.QColor("#F3DD84")
            thumb_fill = QtGui.QColor("#F8C930")
            thumb_x = rect.left() + 3
            renderer = self._light_renderer
        else:
            track_fill = QtGui.QColor("#133A4A")
            track_border = QtGui.QColor("#1D5064")
            thumb_fill = QtGui.QColor("#39A8E8")
            thumb_x = rect.right() - rect.height() + 1
            renderer = self._dark_renderer

        painter.setPen(QtGui.QPen(track_border, 1))
        painter.setBrush(track_fill)
        painter.drawRoundedRect(QtCore.QRectF(rect), radius, radius)

        thumb_size = rect.height() - 6
        thumb_rect = QtCore.QRectF(thumb_x, rect.top() + 3, thumb_size, thumb_size)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(thumb_fill)
        painter.drawEllipse(thumb_rect)

        icon_rect = thumb_rect.adjusted(9, 9, -9, -9)
        renderer.render(painter, icon_rect)

        super().paintEvent(event)


class ConversationRow(QtWidgets.QFrame):
    """A compact sidebar row with avatar, title, preview, and time."""

    def __init__(
        self,
        name: str,
        preview: str,
        time_text: str,
        avatar_text: str,
        parent: QtWidgets.QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.name = name
        self.setObjectName("Conversation_Row")
        self.setMinimumHeight(58)

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(10, 7, 10, 7)
        layout.setSpacing(10)

        self.avatar = QtWidgets.QLabel(avatar_text)
        self.avatar.setObjectName("Conversation_Avatar")
        self.avatar.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.avatar.setFixedSize(34, 34)

        text_stack = QtWidgets.QVBoxLayout()
        text_stack.setContentsMargins(0, 0, 0, 0)
        text_stack.setSpacing(1)

        top_row = QtWidgets.QHBoxLayout()
        top_row.setContentsMargins(0, 0, 0, 0)
        top_row.setSpacing(8)

        self.title = QtWidgets.QLabel(name)
        self.title.setObjectName("Conversation_Name")
        self.title.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.NoTextInteraction)

        self.time = QtWidgets.QLabel(time_text)
        self.time.setObjectName("Conversation_Time")
        self.time.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter
        )

        top_row.addWidget(self.title, 1)
        top_row.addWidget(self.time)

        self.preview = QtWidgets.QLabel(preview)
        self.preview.setObjectName("Conversation_Preview")
        self.preview.setWordWrap(False)
        self.preview.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.NoTextInteraction)

        text_stack.addLayout(top_row)
        text_stack.addWidget(self.preview)

        layout.addWidget(self.avatar)
        layout.addLayout(text_stack, 1)

    def apply_palette(self, palette: ThemePalette, *, selected: bool) -> None:
        """Apply the current theme without relying on fragile nested QSS selectors."""

        def _hex_luminance(hex_color: str) -> int:
            # hex_color expected like '#RRGGBB'
            try:
                h = hex_color.lstrip("#")
                r = int(h[0:2], 16)
                g = int(h[2:4], 16)
                b = int(h[4:6], 16)
                # Simple perceived luminance
                return int(0.299 * r + 0.587 * g + 0.114 * b)
            except Exception:
                return 0

        if selected:
            # Use a softer selected background on light themes to avoid a jarring saturated bar
            app_lum = _hex_luminance(palette.app_background)
            if app_lum > 180:
                # light theme: soft pale-blue highlight
                row_background = "#D9ECFF"
            else:
                # dark theme: use a low-opacity tint of the accent blue for a calmer highlight
                try:
                    h = palette.accent_blue.lstrip("#")
                    ar = int(h[0:2], 16)
                    ag = int(h[2:4], 16)
                    ab = int(h[4:6], 16)
                    row_background = f"rgba({ar},{ag},{ab},0.14)"
                except Exception:
                    row_background = palette.selected_fill
            title_color = palette.primary_text
            muted_color = palette.secondary_text
            avatar_background = palette.accent_blue
            avatar_color = "#FFFFFF"
        else:
            row_background = "transparent"
            title_color = palette.primary_text
            muted_color = palette.secondary_text
            avatar_background = palette.system_bubble
            avatar_color = palette.primary_text

        self.setStyleSheet(
            f"""
            QFrame#Conversation_Row {{
                background: {row_background};
                border-radius: 12px;
                border: none;
            }}
            QLabel#Conversation_Avatar {{
                color: {avatar_color};
                background: {avatar_background};
                border-radius: 17px;
                font-weight: 700;
                font-size: 9.5pt;
            }}
            QLabel#Conversation_Name {{
                color: {title_color};
                font-size: 9.5pt;
                font-weight: 700;
            }}
            QLabel#Conversation_Time,
            QLabel#Conversation_Preview {{
                color: {muted_color};
                font-size: 8pt;
            }}
            """
        )


class PinnedConversationTile(QtWidgets.QPushButton):
    """Compact tile used for pinned conversations in the sidebar."""

    def __init__(
        self,
        name: str,
        avatar_text: str,
        parent: QtWidgets.QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.name = name
        self.setObjectName("Pinned_Conversation_Tile")
        self.setCheckable(True)
        self.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Fixed,
        )
        self.setMinimumHeight(84)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        avatar_wrap = QtWidgets.QHBoxLayout()
        avatar_wrap.setContentsMargins(0, 0, 0, 0)

        self.avatar = QtWidgets.QLabel(avatar_text)
        self.avatar.setObjectName("Pinned_Conversation_Avatar")
        self.avatar.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.avatar.setFixedSize(40, 40)

        avatar_wrap.addStretch(1)
        avatar_wrap.addWidget(self.avatar)
        avatar_wrap.addStretch(1)

        footer = QtWidgets.QHBoxLayout()
        footer.setContentsMargins(0, 0, 0, 0)
        footer.setSpacing(5)

        self.status_dot = QtWidgets.QLabel()
        self.status_dot.setObjectName("Pinned_Conversation_Dot")
        self.status_dot.setFixedSize(8, 8)

        self.title = QtWidgets.QLabel(name)
        self.title.setObjectName("Pinned_Conversation_Name")
        self.title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.title.setWordWrap(True)

        footer.addStretch(1)
        footer.addWidget(self.status_dot, 0, QtCore.Qt.AlignmentFlag.AlignVCenter)
        footer.addWidget(self.title, 0, QtCore.Qt.AlignmentFlag.AlignVCenter)
        footer.addStretch(1)

        layout.addLayout(avatar_wrap)
        layout.addLayout(footer)

    def apply_palette(self, palette: ThemePalette, *, selected: bool) -> None:
        if selected:
            tile_background = "#D9ECFF"
            tile_border = "#B9DBFF"
            title_color = palette.primary_text
            avatar_background = palette.accent_blue
            avatar_color = "#FFFFFF"
            dot_color = palette.accent_blue
        else:
            tile_background = palette.app_background
            tile_border = palette.separator
            title_color = palette.primary_text
            avatar_background = palette.system_bubble
            avatar_color = palette.primary_text
            dot_color = palette.accent_blue

        self.setStyleSheet(
            f"""
            QPushButton#Pinned_Conversation_Tile {{
                background: {tile_background};
                border: 1px solid {tile_border};
                border-radius: 14px;
                text-align: center;
            }}
            QPushButton#Pinned_Conversation_Tile:hover {{
                border-color: {palette.accent_blue};
            }}
            QLabel#Pinned_Conversation_Avatar {{
                color: {avatar_color};
                background: {avatar_background};
                border-radius: 20px;
                font-size: 11pt;
                font-weight: 800;
            }}
            QLabel#Pinned_Conversation_Name {{
                color: {title_color};
                font-size: 8.5pt;
                font-weight: 700;
            }}
            QLabel#Pinned_Conversation_Dot {{
                background: {dot_color};
                border-radius: 4px;
            }}
            """
        )
