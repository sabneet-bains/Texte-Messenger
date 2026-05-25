from pathlib import Path


def test_client_ui_uses_layouts_instead_of_fixed_geometry() -> None:
    source = Path("texte/ui.py").read_text(encoding="utf-8")

    assert "setGeometry(" not in source
    assert "QVBoxLayout" in source
    assert "QHBoxLayout" in source


def test_glass_layer_uses_intentional_subtle_animation() -> None:
    source = Path("texte/glass.py").read_text(encoding="utf-8")

    assert "QPropertyAnimation" in source
    assert "setDuration(150)" in source
