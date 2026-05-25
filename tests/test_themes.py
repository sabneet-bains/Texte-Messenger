from dataclasses import fields

from texte.themes import THEMES, ThemePalette, theme_palette


def test_expected_themes_are_available() -> None:
    assert list(THEMES) == ["Light", "Dark"]


def test_theme_lookup_returns_palette() -> None:
    palette = theme_palette("Light")

    assert isinstance(palette, ThemePalette)
    assert palette.accent_blue == "#0A84FF"


def test_unknown_theme_returns_none() -> None:
    assert theme_palette("Unknown") is None


def test_each_theme_has_all_palette_fields() -> None:
    expected_fields = {field.name for field in fields(ThemePalette)}

    for palette in THEMES.values():
        assert set(palette.__dataclass_fields__) == expected_fields
        assert all(getattr(palette, field) for field in expected_fields)
