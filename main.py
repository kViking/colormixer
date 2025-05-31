import flet as ft
import random
import colorsys
import re
import json
from typing import Optional, List, Dict, Any
from components import ColorInput, MixedColorText, MixedRGBText, RandomFAB, InputRow, SwatchRow, HistoryRow, ComplementaryColorText

# --- Load Swatches ---
with open('swatches.json', 'r') as file:
    swatches = json.load(file)


# --- Color Normalization and Mixing ---
def normalize(c: Optional[str]) -> str:
    """Normalize a color string to a hex format or return 'INVALID'."""
    if not c:
        return 'INVALID'
    c = c.strip()
    if c.startswith('(') and c.endswith(')'):
        rgb = tuple(map(int, c[1:-1].split(',')))
        return "#{:02x}{:02x}{:02x}".format(*rgb)
    c_no_commas = c.replace(',', ' ')
    if len(c_no_commas.split()) == 3:
        rgb = tuple(map(int, c_no_commas.split()))
        return "#{:02x}{:02x}{:02x}".format(*rgb)
    hex_pattern = re.compile(r"^#?[0-9a-fA-F]{6}$")
    if hex_pattern.match(c):
        return c.lower() if c.startswith('#') else '#' + c.lower()
    return 'INVALID'

def hexmixer(color1: Optional[str], color2: Optional[str]) -> str:
    """Mix two hex colors and return the resulting hex color."""
    color1 = normalize(color1)
    color2 = normalize(color2)
    if 'INVALID' in (color1, color2):
        raise ValueError('Invalid color input')
    r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
    r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
    r, g, b = (r1 + r2) // 2, (g1 + g2) // 2, (b1 + b2) // 2
    return "#{:02x}{:02x}{:02x}".format(r, g, b)

def find_closest_swatch(color: Optional[str]) -> Optional[dict]:
    """Find the closest swatch to the given color. Returns None if not close enough."""
    color = normalize(color)
    if color == 'INVALID':
        return None
    closest_swatch = None
    closest_distance = float('inf')
    for swatch in swatches:
        swatch_color = normalize(swatch['hex'])
        if swatch_color == 'INVALID':
            continue
        r1, g1, b1 = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
        r2, g2, b2 = int(swatch_color[1:3], 16), int(swatch_color[3:5], 16), int(swatch_color[5:7], 16)
        distance = ((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2) ** 0.5
        if distance < closest_distance:
            closest_distance = distance
            closest_swatch = swatch
    if closest_distance > 20:  # Threshold for "close enough"
        return None
    return closest_swatch

# --- Main App ---
def main(page: ft.Page) -> None:
    """Main entry point for the Color Mixer app."""
    # Font and theme
    page.fonts = {
        "VCR OSD Mono": "VCR_OSD_MONO.ttf",
    }
    page.theme = ft.Theme(font_family="VCR OSD Mono") #Type: ignore
    page.title = "Color Mixer"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    initial_bg = "#{:06x}".format(random.randint(0, 0xFFFFFF))
    page.bgcolor = initial_bg

    # --- UI State ---
    text_elements: List[Any] = []
    history: List[Dict[str, Any]] = []
    

    # --- UI Components ---
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

    color1 = ColorInput(on_change=lambda e: change_bg(), on_submit=lambda e: change_bg())
    color2 = ColorInput(on_change=lambda e: change_bg(), on_submit=lambda e: change_bg())
    text_elements.extend([color1, color2])
    mixed_color = MixedColorText(initial_bg, on_click=text_click)
    mixed_rgb = MixedRGBText(initial_bg, on_click=text_click)
    text_elements.extend([mixed_color, mixed_rgb])

    input_row = InputRow(color1, color2)
    # swatch_row instantiation moved below, after get_complementary_color is defined

    # --- UI Logic ---
    def build_swatch_row(color: Optional[str] = None) -> None:
        """Update the swatch row based on the current or given color."""
        match = find_closest_swatch(color or page.bgcolor)
        swatch_row.update_swatch_row(
            match,
            page,
            lambda c, m: swatch_row.make_bottom_sheet(c, m, swatches, get_complementary_color, change_bg)
        )

    def _update_field_colors(field, palette):
        field.border_color = random.choice(palette)
        field.focused_border_color = random.choice(palette)
        field.bgcolor = random.choice(palette)
        norm = normalize(field.value)
        if norm != 'INVALID':
            field.bgcolor = norm
            field.color = get_complementary_color(norm)

    def update_text_colors(bg_color: Optional[str] = None, colors: Optional[List[str]] = None) -> None:
        """Update text and border colors for all UI elements based on the background color or a color list.
        If 'colors' is provided, random colors are chosen for UI elements, avoiding the current background color.
        If 'bg_color' is provided, complementary colors are used for contrast.
        """
        if colors:
            palette = [c for c in colors if c != page.bgcolor] or colors
            for element in text_elements:
                element.color = random.choice(palette)
            for field in [color1, color2]:
                _update_field_colors(field, palette)
            random_fab.foreground_color = page.bgcolor
            fab_filtered = [c for c in palette if c != page.bgcolor]
            random_fab.bgcolor = random.choice(fab_filtered) if fab_filtered else random.choice(palette)
            complementary_color_text.update_color(get_complementary_color(random.choice(palette)))
            build_swatch_row(bg_color)
            swatch_row_color = random.choice(palette)
            for combo in swatch_row.controls:
                if isinstance(combo, ft.Text) and combo.spans:
                    combo.spans[0].style = ft.TextStyle(color=swatch_row_color)
        elif bg_color:
            complementary = get_complementary_color(bg_color)
            for element in text_elements:
                element.color = complementary
            for field in [color1, color2]:
                field.border_color = complementary
                field.focused_border_color = complementary
                norm = normalize(field.value)
                if norm != 'INVALID':
                    field.bgcolor = norm
                    field.color = get_complementary_color(norm)
                else:
                    field.bgcolor = bg_color
                    field.color = complementary
            random_fab.foreground_color = bg_color
            random_fab.bgcolor = complementary
            complementary_color_text.update_color(complementary)
            build_swatch_row(bg_color)
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
                    return

            page.bgcolor = new_color
            mixed_color.spans[0].text = new_color
            mixed_rgb.spans[0].text = tuple(int(new_color[i:i+2], 16) for i in (1, 3, 5)).__str__()
            if isinstance(color, dict) and "colors" in color and color["colors"]:
                update_text_colors(colors=color["colors"])
            else:
                update_text_colors(bg_color=new_color)
            # Only add to history if not already present
            if len(history) == 0 or (isinstance(history[-1], dict) and history[-1].get("hex") != new_color):
                top_10 = history[-10:] if len(history) >= 10 else history
                if any(entry.get("hex") == new_color for entry in top_10):
                    return
                entry = {"hex": new_color}
                if not color and c1 and c2:
                    entry["pair"] = (c1, c2)
                elif pair:
                    entry["pair"] = pair
                history.append(entry)
                history_row.update_history(history)
                page.update()
        except Exception as e:
            import traceback
            traceback.print_exc()
            return

    def get_complementary_color(hex_color: Optional[str]) -> str:
        """Return a complementary color for the given hex color, ensuring sufficient contrast."""
        def luminance(rgb: tuple) -> float:
            def channel(c: float) -> float:
                c = c / 255.0
                return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
            r, g, b = rgb
            return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)

        def contrast(rgb1: tuple, rgb2: tuple) -> float:
            l1 = luminance(rgb1)
            l2 = luminance(rgb2)
            lighter = max(l1, l2)
            darker = min(l1, l2)
            return (lighter + 0.05) / (darker + 0.05)

        hex_color = normalize(hex_color)
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))
        if max(rgb) - min(rgb) < 10:
            inv = tuple(255 - c for c in rgb)
            comp_rgb = inv
        else:
            hsv = colorsys.rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255)
            complementary_hsv = ((hsv[0] + 0.5) % 1.0, hsv[1], hsv[2])
            comp_rgb = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(*complementary_hsv))

        # If contrast is insufficient, adjust value (lightness) of the complementary color
        if contrast(rgb, comp_rgb) < 4.5:
            # Try increasing and decreasing value in small steps
            h, s, v = colorsys.rgb_to_hsv(*[c/255 for c in comp_rgb])
            best_rgb = comp_rgb
            best_contrast = contrast(rgb, comp_rgb)
            for delta in [0.05 * i for i in range(1, 11)]:
                for new_v in [min(1.0, v + delta), max(0.0, v - delta)]:
                    adj_rgb = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(h, s, new_v))
                    cval = contrast(rgb, adj_rgb)
                    if cval > best_contrast:
                        best_contrast = cval
                        best_rgb = adj_rgb
                    if cval >= 4.5:
                        return "#{:02x}{:02x}{:02x}".format(*adj_rgb)
            # If no adjustment meets threshold, return the best found
            comp_rgb = best_rgb
        return "#{:02x}{:02x}{:02x}".format(*comp_rgb)
    
    def clamp(val, minval=0, maxval=255):
        return max(minval, min(maxval, val))

    # --- Hotkeys ---
    def on_hotkey(e: ft.KeyboardEvent) -> None:
        """Handle hotkeys for changing background color."""
        if e.shift:
            match e.key:
                case "Arrow Up":
                    new_color = normalize(page.bgcolor)
                    if new_color != 'INVALID':
                        r, g, b = int(new_color[1:3], 16), int(new_color[3:5], 16), int(new_color[5:7], 16)
                        new_hex = "#{:02x}{:02x}{:02x}".format(r, g, clamp(b + 10))
                        change_bg({'hex': new_hex})
                case "Arrow Down":
                    new_color = normalize(page.bgcolor)
                    if new_color != 'INVALID':
                        r, g, b = int(new_color[1:3], 16), int(new_color[3:5], 16), int(new_color[5:7], 16)
                        new_hex = "#{:02x}{:02x}{:02x}".format(r, g, clamp(b - 10))
                        change_bg({'hex': new_hex})
            return

        match e.key:
            case "Arrow Left":
                new_color = normalize(page.bgcolor)
                if new_color != 'INVALID':
                    r, g, b = int(new_color[1:3], 16), int(new_color[3:5], 16), int(new_color[5:7], 16)
                    new_hex = "#{:02x}{:02x}{:02x}".format(clamp(r - 10), g, b)
                    change_bg({'hex': new_hex})
            case "Arrow Right":
                new_color = normalize(page.bgcolor)
                if new_color != 'INVALID':
                    r, g, b = int(new_color[1:3], 16), int(new_color[3:5], 16), int(new_color[5:7], 16)
                    new_hex = "#{:02x}{:02x}{:02x}".format(clamp(r + 10), g, b)
                    change_bg({'hex': new_hex})
            case "Arrow Up":
                new_color = normalize(page.bgcolor)
                if new_color != 'INVALID':
                    r, g, b = int(new_color[1:3], 16), int(new_color[3:5], 16), int(new_color[5:7], 16)
                    new_hex = "#{:02x}{:02x}{:02x}".format(r, clamp(g + 10), b)
                    change_bg({'hex': new_hex})
            case "Arrow Down":
                new_color = normalize(page.bgcolor)
                if new_color != 'INVALID':
                    r, g, b = int(new_color[1:3], 16), int(new_color[3:5], 16), int(new_color[5:7], 16)
                    new_hex = "#{:02x}{:02x}{:02x}".format(r, clamp(g - 10), b)
                    change_bg({'hex': new_hex})

        if e.key == "Tab" or e.key == "%":
            """Show hotkey help dialog."""
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
                
    page.on_keyboard_event = on_hotkey

    complementary_color_text = ComplementaryColorText(
        get_complementary_color(initial_bg),
        on_click=text_click
    )
    swatch_row = SwatchRow(get_complementary_color)
    
    history_row = HistoryRow(
        history=history,
        change_bg=change_bg,
        get_complementary_color=get_complementary_color
    )

    # Now that update_text_colors is defined, instantiate RandomFAB
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
    update_text_colors(bg_color=initial_bg)
    page.update()

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
