import flet as ft
import random
import json
import os
from typing import Optional, List, Dict, Any
from components import ColorInput, MixedColorText, MixedRGBText, RandomFAB, InputRow, SwatchRow, HistoryRow, ComplementaryColorText
from color_utils import normalize, hexmixer, find_closest_swatch, get_complementary_color, HexToRgb
from state import add_to_history
import hotkeys
from config import CONFIG

# --- Load Config ---
config = CONFIG

# --- Load Swatches ---
with open(os.path.join(os.path.dirname(__file__), config['swatches_file']), 'r') as file:
    swatches = json.load(file)

# --- Main App ---
def main(page: ft.Page) -> None:
    """Main entry point for the Color Mixer app."""
    # Font and theme
    page.fonts = {
        config['font_family']: config['font_path'],
    }
    page.theme = ft.Theme(font_family=config['theme']['font_family']) # Type: ignore
    page.title = "Color Mixer"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    initial_bg = "#{:06x}".format(random.randint(0, 0xFFFFFF))
    page.bgcolor = initial_bg

    # --- UI State ---
    # Use session-based history if available
    history: List[Dict[str, Any]] = page.session.get("history") or []
    text_elements: List[Any] = []

    # --- UI Logic ---
    def text_click(e: ft.ControlEvent) -> None:
        """Copy text to clipboard and show a snackbar notification."""
        page.set_clipboard(e.control.text)
        page.open(ft.SnackBar(
            content=ft.Text(
                value=f"Copied {e.control.text}",
                color=page.bgcolor
            ),
            bgcolor=get_complementary_color(page.bgcolor),
        ))

    def build_swatch_row(color: Optional[str] = None) -> None:
        """Update the swatch row based on the current or given color."""
        match = find_closest_swatch(color or page.bgcolor, swatches)
        if match is not None:
            swatch_row.update_swatch_row(
                match,
                page,
                lambda c, m: swatch_row.make_bottom_sheet(c, m, swatches, change_bg, text_click),
            )
        else:
            swatch_row.update_swatch_row(
                {'hex': '#000000', 'name': None, 'combinations': []},
                page,
                lambda c, m: swatch_row.make_bottom_sheet(c, m, swatches, change_bg, text_click),
            )

    def update_text_colors(color_info: Optional[Any] = None) -> None:
        # Accepts either a list of colors or a single bg_color string
        if isinstance(color_info, list):
            palette = [c for c in color_info if c != page.bgcolor] or color_info
            for element in text_elements:
                if hasattr(element, 'update_color'):
                    element.update_color(random.choice(palette))
                else:
                    element.color = random.choice(palette)
            for field in [color1, color2]:
                field.update_bg_color(random.choice(palette))
                field.update_focused_border_color(random.choice(palette))
                field.update_color(get_complementary_color(field.value) if normalize(field.value) != 'INVALID' else random.choice(palette))
            random_fab.update_color(random.choice(palette))
            complementary_color_text.update_color(random.choice(palette))
            build_swatch_row(page.bgcolor)
            swatch_row_color = random.choice(palette)
            for combo in swatch_row.controls:
                if isinstance(combo, ft.Text) and combo.spans:
                    combo.spans[0].style = ft.TextStyle(color=swatch_row_color)
        elif isinstance(color_info, str):
            complementary = get_complementary_color(color_info)
            for element in text_elements:
                if hasattr(element, 'update_color'):
                    element.update_color(complementary)
                else:
                    element.color = complementary
            for field in [color1, color2]:
                field.update_bg_color(color_info)
                field.update_border_color(complementary)
                field.update_focused_border_color(complementary)
                field.update_color(get_complementary_color(field.value) if normalize(field.value) != 'INVALID' else complementary)
            random_fab.update_color(complementary)
            complementary_color_text.update_color(complementary)
            build_swatch_row(color_info)
        page.update()

    def change_bg(color: Optional[Any] = None, clear_fields: bool = False) -> None:
        """Change the background color and update history and UI as needed."""
        if not color:
            for field in [color1, color2]:
                norm = normalize(field.value)
                if norm == 'INVALID':
                    field.bgcolor = page.bgcolor
                    page.update()
                else:
                    field.bgcolor = norm
                    field.color = get_complementary_color(field.bgcolor)
                    page.update()
        elif clear_fields:
            color1.value = ""
            color2.value = ""
            page.update()

        try:
            c1 = c2 = ''
            pair = None
            if not color:
                c1 = (color1.value or '').strip()
                c2 = (color2.value or '').strip()
                new_color = hexmixer(c1, c2)
                pair = (c1, c2)
            else:
                # If color is a dict (from history or swatch), extract hex and pair
                if isinstance(color, dict):
                    new_color = color.get("hex", "")
                    pair = color.get("pair", None)
                    # If pair exists, populate text fields
                    if pair:
                        color1.value, color2.value = pair
                else:
                    new_color = normalize(color)
                    page.update()
                    # DO NOT early return here

            page.bgcolor = new_color
            mixed_color.spans[0].text = new_color
            mixed_rgb.spans[0].text = HexToRgb(new_color).string
            if isinstance(color, dict) and "colors" in color and color["colors"]:
                update_text_colors(color["colors"])
            else:
                update_text_colors(new_color)
            # Only add to history if not already present
            add_to_history(page, history, new_color, pair if not color and c1 and c2 else None)
            history_row.update_history(history)
            page.update()
        except Exception as e:
            import traceback
            traceback.print_exc()
            return

    # --- Hotkeys ---
    page.on_keyboard_event = hotkeys.make_hotkey_handler(page, change_bg)

    # --- UI Components (stateless) ---
    color1 = ColorInput(border_color=get_complementary_color(initial_bg), on_change=lambda e: change_bg(), on_submit=lambda e: change_bg())
    color2 = ColorInput(border_color=get_complementary_color(initial_bg), on_change=lambda e: change_bg(), on_submit=lambda e: change_bg())
    input_row = InputRow(color1, color2)

    mixed_color = MixedColorText(initial_bg, on_click=text_click)
    mixed_rgb = MixedRGBText(initial_bg, on_click=text_click)
    complementary_color_text = ComplementaryColorText(
        complementary_color=get_complementary_color(initial_bg),
        on_click=text_click
    )

    # --- UI Components (stateful) ---
    swatch_row = SwatchRow()
    history_row = HistoryRow(
        history=history,
        change_bg=change_bg
    )

    # --- Random FAB ---
    random_fab = RandomFAB(
        page=page,
        mixed_color=mixed_color,
        mixed_rgb=mixed_rgb,
        color1=color1,
        color2=color2,
        update_text_colors=update_text_colors,
        history=history,
        history_row=history_row
    )
    text_elements.extend([color1, color2, mixed_color, mixed_rgb])

    # --- Layout ---
    class DisplayArea(ft.Column):
        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)
            self.expand = True
            self.alignment = ft.MainAxisAlignment.SPACE_BETWEEN
            self.controls = [
                history_row,
                ft.Container(content=input_row, expand=True, alignment=ft.alignment.center),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            complementary_color_text,
                            mixed_color, 
                            mixed_rgb,
                            swatch_row, 
                        ],
                        alignment=ft.MainAxisAlignment.END,
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        # expand=True,
                    ),
                    alignment=ft.alignment.bottom_left,
                )
            ]

    page.add(ft.SafeArea(content=DisplayArea(expand=True), expand=True))
    page.floating_action_button = random_fab
    history.append(
        {
            "hex": initial_bg,
            "pair": (color1.value, color2.value) if color1.value and color2.value else None
        }
    )
    history_row.update_history(history)
    update_text_colors(initial_bg)
    page.update()

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
