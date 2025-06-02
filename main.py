import flet as ft
import random
import json
import os
from typing import Optional, List, Dict, Any
from components import ColorInput, MixedColorText, MixedRGBText, RandomFAB, InputRow, CombinationRow, CombinationRowContainer, HistoryRow, ComplementaryColorText, ColorDisplayColumn
from core.color_utils import *
from core.state import add_to_history, set_current_state, get_current_state
import core.hotkeys
from core.config import CONFIG
from components.display import MixedColorText, MixedRGBText, ComplementaryColorText, ColorDisplayColumn
from components.fab import RandomFAB
from components.inputs import ColorInput, InputRow
from components.swatches import CombinationRow, CombinationRowContainer
from components.history import HistoryRow
from core.color_utils import normalize, hexmixer, find_closest_swatch, get_complementary_color, HexToRgb
from core.state import add_to_history, set_current_state, get_current_state
import core.hotkeys
from core.config import CONFIG

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
    page.theme = ft.Theme()
    page.theme.font_family = config.get('theme', {}).get('font_family', 'VCR_OSD_MONO')
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

    def build_combination_row(color: Optional[str] = None) -> None:
        """Update the combination row based on the current or given color."""
        match = find_closest_swatch(color or page.bgcolor, swatches)
        if match is not None:
            combination_row.update_combination_row(
                match,
                page,
                lambda c, m: combination_row.make_bottom_sheet(c, m, swatches, change_bg, text_click),
            )
        else:
            combination_row.update_combination_row(
                {'hex': '#000000', 'name': None, 'combinations': []},
                page,
                lambda c, m: combination_row.make_bottom_sheet(c, m, swatches, change_bg, text_click),
            )

    def _update_text_colors(color_info: Optional[Any] = None, palette: Optional[int] = None, palette_colors: Optional[list] = None) -> None:
        # Accepts either a list of colors or a single bg_color string
        if isinstance(color_info, list):
            palette_colors = color_info
            palette_list = [c for c in palette_colors if c != page.bgcolor] or palette_colors
            for element in text_elements:
                if hasattr(element, 'update_color'):
                    element.update_color(random.choice(palette_list))
                else:
                    element.color = random.choice(palette_list)
            for field in [color1, color2]:
                field.update_bg_color(random.choice(palette_list))
                field.update_focused_border_color(random.choice(palette_list))
                field.update_color(get_complementary_color(field.value) if normalize(field.value) != 'INVALID' else random.choice(palette_list))
            random_fab.update_color(random.choice(palette_list))
            complementary_color_text.update_color(random.choice(palette_list))
            build_combination_row(page.bgcolor)
            combination_row_color = random.choice(palette_list)
            for combo in combination_row.controls:
                if isinstance(combo, ft.Text) and combo.spans:
                    combo.spans[0].style = ft.TextStyle(color=combination_row_color) if combo.spans[0].text != palette else ft.TextStyle(
                        bgcolor=combination_row_color, 
                        color=page.bgcolor
                    )
            # Store palette and palette_colors in session state
            set_current_state(page, page.bgcolor, get_complementary_color(page.bgcolor), palette, palette_colors)
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
            build_combination_row(color_info)
            # Store only color, not palette
            set_current_state(page, color_info, complementary, None, None)
            if palette is not None and palette_colors is not None:
                # Update the combination row with the palette colors
                for combo in combination_row.controls:
                    if isinstance(combo, ft.Text) and combo.spans and combo.spans[0].text == palette:
                        combo.spans[0].style = ft.TextStyle(
                            bgcolor=get_complementary_color(page.bgcolor), 
                            color=page.bgcolor
                        )
        page.update()

    def change_bg(color: Optional[Any] = None, clear_fields: bool = False, palette: Optional[int] = None, palette_colors: Optional[list] = None) -> None:
        """Change the background color and update history and UI as needed."""
        if not color:
            for field in [color1, color2]:
                norm = normalize(field.value)
                if norm == 'INVALID':
                    pass
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
                if isinstance(color, dict):
                    new_color = color.get("hex", "")
                    pair = color.get("pair", None)
                    if pair:
                        color1.value, color2.value = pair
                    # Accept palette and palette_colors from dict if present
                    palette = color.get("palette", palette)
                    palette_colors = color.get("palette_colors", color.get("colors", palette_colors))
                else:
                    new_color = normalize(color)
                    page.update()
            complementary = get_complementary_color(new_color)
            set_current_state(page, new_color, complementary, palette, palette_colors)
            page.bgcolor = new_color
            mixed_color.update_text(new_color)
            mixed_color.update_color(complementary)
            mixed_rgb.update_text(HexToRgb(new_color).string)
            mixed_rgb.update_color(complementary)
            complementary_color_text.update_text(complementary)
            complementary_color_text.update_color(complementary)
            if palette and palette_colors:
                _update_text_colors(palette_colors, palette, palette_colors)
            else:
                _update_text_colors(new_color)
            add_to_history(page, history, new_color, pair if not color and c1 and c2 else None)
            history_row.update_history(history)
            page.update()
        except Exception as e:
            import traceback
            traceback.print_exc()
            return

    # --- Hotkeys ---
    page.on_keyboard_event = core.hotkeys.make_hotkey_handler(page, change_bg)

    # --- UI Components (stateless) ---
    color1 = ColorInput(border_color=get_complementary_color(initial_bg), on_change=lambda e: change_bg(), on_submit=lambda e: change_bg())
    color2 = ColorInput(border_color=get_complementary_color(initial_bg), on_change=lambda e: change_bg(), on_submit=lambda e: change_bg())
    color1.set_page(page)
    color2.set_page(page)

    mixed_color = MixedColorText(initial_bg, on_click=text_click)
    mixed_rgb = MixedRGBText(initial_bg, on_click=text_click)
    complementary_color_text = ComplementaryColorText(
        complementary_color=get_complementary_color(initial_bg),
        on_click=text_click
    )

    # --- UI Components (stateful) ---
    input_row = InputRow(color1, color2, alignment=ft.alignment.center)
    input_row_container = ft.Container(
        content=input_row,
        alignment=ft.alignment.center,
        border_radius=ft.BorderRadius(0, 0, 0, 0)
    )
    combination_row_container = CombinationRowContainer()
    combination_row = combination_row_container.combination_row
    history_row = HistoryRow(
        history=history,
        change_bg=change_bg
    )
    display_text = ColorDisplayColumn(
        complementary_color_text=complementary_color_text,
        mixed_color=mixed_color,
        mixed_rgb=mixed_rgb,
        combination_row=combination_row,  # Use standardized argument name
        alignment=ft.alignment.bottom_right,
    )

    # --- Random FAB ---
    random_fab = RandomFAB(
        page=page,
        update_text_colors=change_bg,  # Pass change_bg as the callback
        history=history,
        history_row=history_row,
    )
    text_elements.extend([color1, color2, mixed_color, mixed_rgb])

    # --- Layout ---
    class DisplayArea(ft.Column):
        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)
            self.alignment = ft.MainAxisAlignment.SPACE_BETWEEN
            self.controls = [
                history_row,
                input_row_container,
                display_text,
            ]

    page.add(ft.SafeArea(content=DisplayArea(), expand=True))
    history.append(
        {
            "hex": initial_bg,
            "pair": (color1.value, color2.value) if color1.value and color2.value else None
        }
    )
    history_row.update_history(history)
    _update_text_colors(initial_bg)    

    page.floating_action_button = random_fab

    page.update()

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
