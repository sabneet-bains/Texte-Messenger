"""Design tokens for the Texte client."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ThemePalette:
    app_background: str
    sidebar_background: str
    glass_fill: str
    glass_border: str
    glass_highlight: str
    separator: str
    hover_fill: str
    selected_fill: str
    control_fill: str
    primary_text: str
    secondary_text: str
    accent_blue: str
    accent_blue_dark: str
    success: str
    error: str
    danger_fill: str
    incoming_bubble: str
    outgoing_bubble: str
    system_bubble: str
    composer_fill: str
    field_fill: str
    shadow: str


THEMES = {
    "Light": ThemePalette(
        app_background="#FFFFFF",
        sidebar_background="#F7F7F8",
        glass_fill="#F2F2F7",
        glass_border="#E2E2E7",
        glass_highlight="#FFFFFF",
        separator="#DADAE0",
        hover_fill="#EFEFF4",
        selected_fill="#0A84FF",
        control_fill="#F2F2F7",
        primary_text="#111827",
        secondary_text="#6B7280",
        accent_blue="#0A84FF",
        accent_blue_dark="#0066CC",
        success="#34C759",
        error="#FF3B30",
        danger_fill="#FF5F7E",
        incoming_bubble="#E9E9EB",
        outgoing_bubble="#0A84FF",
        system_bubble="#F2F2F7",
        composer_fill="#FFFFFF",
        field_fill="#FFFFFF",
        shadow="#D1D5DB",
    ),
    "Dark": ThemePalette(
        app_background="#0F1724",
        sidebar_background="#121C2B",
        glass_fill="#1A2638",
        glass_border="#2A3850",
        glass_highlight="#31405A",
        separator="#233247",
        hover_fill="#182334",
        selected_fill="#2D9CFF",
        control_fill="#182334",
        primary_text="#F5F7FB",
        secondary_text="#9DAAC0",
        accent_blue="#3AA6FF",
        accent_blue_dark="#81C7FF",
        success="#64D3A0",
        error="#FF6F8D",
        danger_fill="#DF5874",
        incoming_bubble="#1B2739",
        outgoing_bubble="#1F7AE0",
        system_bubble="#162133",
        composer_fill="#131E2D",
        field_fill="#1A2638",
        shadow="#050A12",
    ),
}


def theme_palette(name: str) -> ThemePalette | None:
    return THEMES.get(name)
