from typing import List, Dict, Any
from flet import Page

def add_to_history(page: Page, history: List[Dict[str, Any]], new_color: str, pair=None) -> None:
    entry = {"hex": new_color}
    if pair:
        entry["pair"] = pair
    if not history or (isinstance(history[-1], dict) and history[-1].get("hex") != new_color):
        top_10 = history[-10:] if len(history) >= 10 else history
        if any(entry.get("hex") == new_color for entry in top_10):
            return
        history.append(entry)
        page.session.set("history", history)

def clear_fields(color1, color2):
    color1.value = ""
    color2.value = ""

def set_current_state(page, bgcolor, complementary, palette=None, palette_colors=None):
    current = page.session.get('current') or {}
    current.update({
        'bgcolor': bgcolor,
        'complementary': complementary,
        'palette': palette,
        'palette_colors': palette_colors or []
    })
    page.session.set('current', current)

def get_current_state(page):
    val = page.session.get('current')
    return val if val is not None else {}

# Palette state management

def get_palette(page) -> list[str]:
    """Get the current palette from session, or return an empty list."""
    return page.session.get('palette') or []

def add_to_palette(page, color: str) -> list[str]:
    """Add a color to the palette if not present. Returns updated palette."""
    palette = get_palette(page)
    if color not in palette:
        palette.append(color)
        page.session.set('palette', palette)
    return palette

def remove_from_palette(page, color: str) -> list[str]:
    """Remove a color from the palette. Returns updated palette."""
    palette = get_palette(page)
    if color in palette:
        palette.remove(color)
        page.session.set('palette', palette)
    return palette
