import flet as ft
import random
import colorsys
import re
import json
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

def get_complementary_color(hex_color):
    hex_color = normalize(hex_color)
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))
    if max(rgb) - min(rgb) < 10:
        inv = tuple(255 - c for c in rgb)
        return "#{:02x}{:02x}{:02x}".format(*inv)
    hsv = colorsys.rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255)
    complementary_hsv = ((hsv[0] + 0.5) % 1.0, hsv[1], hsv[2])
    complementary_rgb = colorsys.hsv_to_rgb(*complementary_hsv)
    return "#{:02x}{:02x}{:02x}".format(
        int(complementary_rgb[0] * 255),
        int(complementary_rgb[1] * 255),
        int(complementary_rgb[2] * 255)
    )

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

    # --- UI Components ---
    def text_click(e):
        page.set_clipboard(e.control.text)
        print(f"Copied {e.control.text} to clipboard")

    color1 = ft.TextField(
        on_submit=lambda e: change_bg(),
        on_change=lambda e: change_bg(),
        text_align=ft.TextAlign.CENTER,
        width=200,
    )
    color2 = ft.TextField(
        on_submit=lambda e: change_bg(),
        on_change=lambda e: change_bg(),
        text_align=ft.TextAlign.CENTER,
        width=200,
    )
    text_elements.extend([color1, color2])

    mixed_color = ft.Text(
        theme_style=ft.TextThemeStyle.DISPLAY_LARGE,
        selectable=True,
        spans=[ft.TextSpan(initial_bg, on_click=text_click)]
    )
    mixed_rgb = ft.Text(
        theme_style=ft.TextThemeStyle.DISPLAY_LARGE,
        selectable=True,
        spans=[ft.TextSpan(tuple(int(initial_bg[i:i+2], 16) for i in (1, 3, 5)).__str__(), on_click=text_click)]
    )
    text_elements.extend([mixed_color, mixed_rgb])

    random_fab = ft.FloatingActionButton(
        icon=ft.Icons.SHUFFLE,
        on_click=lambda e: fab_click(),
        tooltip="Randomize background color",
    )

    input_row = ft.Row(
        controls=[color1, color2],
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True,
        wrap=True,
    )

    swatch_row = ft.Row(
        alignment=ft.MainAxisAlignment.START,
        controls=[]
    )

    class ColorSwatch(ft.Container):
        def __init__(self, color, name, **kwargs):
            super().__init__(
                bgcolor=color,
                expand=True,  # Allow expansion in parent
                alignment=ft.alignment.center,
                **kwargs
            )
            self.bgcolor = color
            self.content = ft.Column(
                alignment=ft.MainAxisAlignment.END,
                horizontal_alignment=ft.CrossAxisAlignment.END,
                expand=True,  # Allow vertical expansion
                controls=[
                    ft.Text(
                        spans=[
                            ft.TextSpan(
                                color,
                                on_click=text_click,
                                style=ft.TextStyle(
                                    color=get_complementary_color(color)
                                )
                            )
                        ],
                        expand=True  # Allow horizontal expansion for text
                    ),
                    ft.Text(name, color=get_complementary_color(color), ),
                ],
            )
            def click_handler(e):
                change_bg(color)
                
            self.on_click = lambda e: change_bg(color)


    # --- UI Logic ---
    def make_bottom_sheet(combination, match):
      combo_row = ft.Row(expand=True, alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=0)
      sheet = ft.BottomSheet(
        ft.Column(
           controls=[
              combo_row,
              ft.Text(f"combination {combination}", style=ft.TextStyle(color=get_complementary_color(match['hex']))),
           ],
           expand=True,
        ),
        bgcolor=match['hex'],
      )
      for swatch in swatches:
        if combination in swatch['combinations']:
            color = swatch['hex']
            name = swatch['name']
            combo_row.controls.append(ColorSwatch(color, name))
      return sheet
    
    def build_swatch_row(color=None):
      match = find_closest_swatch(color or page.bgcolor)
      if match:
        swatch_row.controls.clear()
        for combo in match['combinations']:
          swatch_row.controls.append(
             ft.Text(
                spans=[
                   ft.TextSpan(
                      combo,
                      style=ft.TextStyle(color=get_complementary_color(page.bgcolor)),
                      on_click=lambda e, c=combo: page.open(make_bottom_sheet(c, match)),
                   )
                ]
             )
          )
        page.update()
      else:
        swatch_row.controls.clear()
        page.update()


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
            update_text_colors(new_color)
        except Exception:
            pass

    def fab_click():
        new_color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        page.bgcolor = new_color
        mixed_color.spans[0].text = new_color
        mixed_rgb.spans[0].text = tuple(int(new_color[i:i+2], 16) for i in (1, 3, 5)).__str__()
        color1.value = ""
        color2.value = ""
        update_text_colors(new_color)
        page.update()

    # --- Layout ---
    class DisplayArea(ft.Column):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.expand = True
            self.controls = [
                ft.Container(content=input_row, expand=True, alignment=ft.alignment.top_center),
                ft.Container(
                    content=ft.Column(
                        controls=[swatch_row, mixed_color, mixed_rgb],
                        alignment=ft.MainAxisAlignment.END,
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        expand=True,
                    ),
                    alignment=ft.alignment.bottom_left,
                )
            ]

    page.add(ft.SafeArea(content=DisplayArea(expand=True), expand=True))
    page.floating_action_button = random_fab
    update_text_colors(initial_bg)
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
