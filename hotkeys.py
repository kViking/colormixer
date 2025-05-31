from color_utils import normalize, HexToRgb
import flet as ft
from typing import Any, Callable

def clamp(val, minval=0, maxval=255):
    return max(minval, min(maxval, val))

def make_hotkey_handler(page: ft.Page, change_bg: Callable[[Any], None]) -> Callable[[ft.KeyboardEvent], None]:
    def on_hotkey(e: ft.KeyboardEvent) -> None:
        if e.shift:
            match e.key:
                case "Arrow Up":
                    hex_color = normalize(page.bgcolor)
                    if hex_color != 'INVALID':
                        r, g, b = HexToRgb(hex_color).tuple
                        new_hex = "#{:02x}{:02x}{:02x}".format(r, g, clamp(b + 10))
                        change_bg({'hex': new_hex})
                case "Arrow Down":
                    hex_color = normalize(page.bgcolor)
                    if hex_color != 'INVALID':
                        r, g, b = HexToRgb(hex_color).tuple
                        new_hex = "#{:02x}{:02x}{:02x}".format(r, g, clamp(b - 10))
                        change_bg({'hex': new_hex})
            return
        match e.key:
            case "Arrow Left":
                hex_color = normalize(page.bgcolor)
                if hex_color != 'INVALID':
                    r, g, b = HexToRgb(hex_color).tuple
                    new_hex = "#{:02x}{:02x}{:02x}".format(clamp(r - 10), g, b)
                    change_bg({'hex': new_hex})
            case "Arrow Right":
                hex_color = normalize(page.bgcolor)
                if hex_color != 'INVALID':
                    r, g, b = HexToRgb(hex_color).tuple
                    new_hex = "#{:02x}{:02x}{:02x}".format(clamp(r + 10), g, b)
                    change_bg({'hex': new_hex})
            case "Arrow Up":
                hex_color = normalize(page.bgcolor)
                if hex_color != 'INVALID':
                    r, g, b = HexToRgb(hex_color).tuple
                    new_hex = "#{:02x}{:02x}{:02x}".format(r, clamp(g + 10), b)
                    change_bg({'hex': new_hex})
            case "Arrow Down":
                hex_color = normalize(page.bgcolor)
                if hex_color != 'INVALID':
                    r, g, b = HexToRgb(hex_color).tuple
                    new_hex = "#{:02x}{:02x}{:02x}".format(r, clamp(g - 10), b)
                    change_bg({'hex': new_hex})
        if e.key == "Tab":
            dialog = ft.AlertDialog(
                title=ft.Text("Hotkeys"),
                content=ft.Text(
                    "Use the arrow keys to adjust the background color:\n"
                    "- Left/Right: Adjust red channel\n"
                    "- Up/Down: Adjust green channel\n"
                    "- Shift + Up/Down: Adjust blue channel\n"
                    "Press Escape to close this dialog."
                ),
                actions=[ft.TextButton("Close", on_click=lambda _: page.close(dialog))],
            )
            page.open(dialog)
            page.update()
        else:
            return
    return on_hotkey
