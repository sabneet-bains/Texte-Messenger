"""Small client-side helpers shared across the Texte UI."""

from typing import cast

from PyQt6 import QtCore, QtWidgets


class ConversationListItem(QtWidgets.QListWidgetItem):
    """List item that preserves its logical text for tests while rendering empty."""

    def __init__(self, display_text: str) -> None:
        super().__init__()
        self._display_text = display_text
        super().setText("")
        self.setData(QtCore.Qt.ItemDataRole.UserRole, display_text)

    def text(self) -> str:
        return self._display_text


def strings_from(value: object) -> list[str]:
    if isinstance(value, list | tuple | set):
        return [str(item) for item in value]
    return []


def entry_text(entry: dict[str, object], key: str, default: str = "") -> str:
    value = entry.get(key)
    return value if isinstance(value, str) else default


def entry_bool(entry: dict[str, object], key: str, default: bool = False) -> bool:
    value = entry.get(key)
    return value if isinstance(value, bool) else default


def entry_int(entry: dict[str, object], key: str, default: int = 0) -> int:
    value = entry.get(key)
    return value if isinstance(value, int) else default


def entry_strings(entry: dict[str, object], key: str) -> list[str]:
    return strings_from(entry.get(key))


def qbytearray_to_bytes(data: QtCore.QByteArray) -> bytes:
    return cast(bytes, data.data())


def qbytearray_to_text(data: QtCore.QByteArray) -> str:
    return qbytearray_to_bytes(data).decode(errors="ignore")


def scrollbar_or_raise(area: QtWidgets.QAbstractScrollArea) -> QtWidgets.QScrollBar:
    scrollbar = area.verticalScrollBar()
    assert scrollbar is not None
    return scrollbar
