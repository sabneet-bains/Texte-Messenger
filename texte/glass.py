"""Compatibility glass helpers for the Texte client."""

from PyQt6 import QtCore, QtWidgets


def animate_entry(widget: QtWidgets.QWidget) -> None:
    """Apply a subtle opacity animation when a widget enters."""
    effect = QtWidgets.QGraphicsOpacityEffect(widget)
    effect.setOpacity(0.0)
    widget.setGraphicsEffect(effect)

    animation = QtCore.QPropertyAnimation(effect, b"opacity", widget)
    animation.setDuration(150)
    animation.setStartValue(0.0)
    animation.setEndValue(1.0)
    animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
    animation.finished.connect(lambda: widget.setGraphicsEffect(None))
    widget._texte_animation = animation  # type: ignore[attr-defined]
    animation.start(QtCore.QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)
