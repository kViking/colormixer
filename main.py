import flet as ft
import random
import colorsys
import re
import json
from components import ColorInput, MixedColorText, MixedRGBText, RandomFAB, InputRow, SwatchRow, HistoryRow
# --- Load Swatches ---
with open('swatches.json', 'r') as file:
    swatches = json.load(file)


# --- Color Normalization and Mixing ---
def normalize(c):
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

def hexmixer(color1, color2):
    color1 = normalize(color1)
    color2 = normalize(color2)
    if 'INVALID' in (color1, color2):
        raise ValueError('Invalid color input')
    r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
    r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
    r, g, b = (r1 + r2) // 2, (g1 + g2) // 2, (b1 + b2) // 2
    return "#{:02x}{:02x}{:02x}".format(r, g, b)

def find_closest_swatch(color):
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
def main(page: ft.Page):
    # Font and theme
    page.fonts = {
        "VCR OSD Mono": "VCR_OSD_Mono.ttf",
    }
    page.theme = ft.Theme(font_family="VCR OSD Mono")
    page.title = "Color Mixer"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    initial_bg = "#{:06x}".format(random.randint(0, 0xFFFFFF))
    page.bgcolor = initial_bg


    # --- UI State ---
    text_elements = []
    history = []

    # --- UI Components ---
    def text_click(e):
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
    def build_swatch_row(color=None):
        match = find_closest_swatch(color or page.bgcolor)
        swatch_row.update_swatch_row(
            match,
            page,
            lambda c, m: swatch_row.make_bottom_sheet(c, m, swatches, get_complementary_color, change_bg)
        )

    def update_text_colors(bg_color):
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
        page.update()
        build_swatch_row(bg_color)

    def change_bg(color=None):
        for field in [color1, color2]:
            if field.value and not normalize(field.value) == 'INVALID':
                field.bgcolor = normalize(field.value)
                page.update()
        try:
            if not color:
                c1 = (color1.value or '').strip()
                c2 = (color2.value or '').strip()
                new_color = hexmixer(c1, c2)
            else:
                new_color = normalize(color)
            if not new_color == 'INVALID':
                page.bgcolor = new_color
                mixed_color.spans[0].text = new_color
                mixed_rgb.spans[0].text = tuple(int(new_color[i:i+2], 16) for i in (1, 3, 5)).__str__()
                if len(history) == 0 or history[-1] != new_color:
                    history.append(new_color)
                    history_row.update_history(history)
                update_text_colors(new_color)
        except Exception:
            pass

    def get_complementary_color(hex_color):
        def luminance(rgb):
            def channel(c):
                c = c / 255.0
                return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
            r, g, b = rgb
            return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)

        def contrast(rgb1, rgb2):
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
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.expand = True
            self.alignment = ft.MainAxisAlignment.SPACE_BETWEEN
            self.controls = [
                history_row,
                ft.Container(content=input_row, expand=True, alignment=ft.alignment.center),
                ft.Container(
                    content=ft.Column(
                        controls=[swatch_row, mixed_color, mixed_rgb],
                        alignment=ft.MainAxisAlignment.END,
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        # expand=True,
                    ),
                    alignment=ft.alignment.bottom_left,
                )
            ]

    page.add(ft.SafeArea(content=DisplayArea(expand=True), expand=True))
    page.floating_action_button = random_fab
    history.append(initial_bg)
    history_row.update_history(history)
    update_text_colors(initial_bg)
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
