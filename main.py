import flet as ft
import random
import colorsys
import re



def hexmixer(color1, color2):
  # Normalize color1 and color2 to hex string
  def normalize(c):
    c = c.strip()
    # (r, g, b) tuple
    if c.startswith('(') and c.endswith(')'):
      rgb = tuple(map(int, c[1:-1].split(',')))
      return "#{:02x}{:02x}{:02x}".format(*rgb)
    # Remove commas for space-separated RGB
    c_no_commas = c.replace(',', ' ')
    if len(c_no_commas.split()) == 3:
      rgb = tuple(map(int, c_no_commas.split()))
      return "#{:02x}{:02x}{:02x}".format(*rgb)
    # Accept only valid 6-digit hex (with or without #)
    hex_pattern = re.compile(r"^#?[0-9a-fA-F]{6}$")
    if hex_pattern.match(c):
      if c.startswith('#'):
        return c.lower()
      else:
        return '#' + c.lower()
    # If not valid, return a clearly invalid string to trigger error handling
    return 'INVALID'

  color1 = normalize(color1)
  color2 = normalize(color2)
  # If either color is invalid, raise ValueError
  if 'INVALID' in (color1, color2):
    raise ValueError('Invalid color input')

  # Mix two hex color codes and return the resulting color.
  r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
  r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
  r = (r1 + r2) // 2
  g = (g1 + g2) // 2
  b = (b1 + b2) // 2
  return "#{:02x}{:02x}{:02x}".format(r, g, b)


def get_complementary_color(hex_color):
  """Return the color wheel opposite (complementary) of the given hex color."""
  # Remove the # and convert to RGB
  rgb = tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))

  # If the color is very close to black or white, just invert it
  if max(rgb) - min(rgb) < 10:
    inv = tuple(255 - c for c in rgb)
    return "#{:02x}{:02x}{:02x}".format(*inv)

  # Convert RGB to HSV
  hsv = colorsys.rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255)

  # Rotate hue by 180 degrees (0.5 in the 0-1 range)
  complementary_hsv = ((hsv[0] + 0.5) % 1.0, hsv[1], hsv[2])

  # Convert back to RGB
  complementary_rgb = colorsys.hsv_to_rgb(*complementary_hsv)

  # Convert to hex
  return "#{:02x}{:02x}{:02x}".format(
    int(complementary_rgb[0] * 255),
    int(complementary_rgb[1] * 255),
    int(complementary_rgb[2] * 255)
  )


def main(page: ft.Page):
  page.title = "Color Mixer"
  page.vertical_alignment= ft.MainAxisAlignment.CENTER
  page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
  initial_bg: str = "#{:06x}".format(random.randint(0, 0xFFFFFF))

  page.bgcolor = initial_bg
  
  # Store all text elements for color updating
  text_elements = []


  def update_text_colors(bg_color):
    """Update all text elements to use the complementary color of the background."""
    complementary = get_complementary_color(bg_color)
    for element in text_elements:
      element.color = complementary
    for element in [color1, color2]:
      element.border_color = complementary
      element.focused_border_color = complementary
    random_fab.foreground_color = bg_color
    random_fab.bgcolor = get_complementary_color(bg_color)
    page.update()


  def change_bg(e=None):
    """Change the background color of the page."""
    try:
      color1_value = str(color1.value).strip()
      color2_value = str(color2.value).strip()
      new_color = initial_bg
      new_color = hexmixer(color1_value, color2_value)
      page.bgcolor = new_color
      mixed_color.value = new_color
      mixed_rgb.value = tuple(int(new_color[i:i+2], 16) for i in (1, 3, 5)).__str__()
      update_text_colors(new_color)
    except Exception as ex:
      pass


  def fab_click(e):
    """Handle FloatingActionButton click to change background color."""
    new_color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
    page.bgcolor = new_color
    mixed_color.value = new_color
    mixed_rgb.value = tuple(int(new_color[i:i+2], 16) for i in (1, 3, 5)).__str__()
    random_fab.foreground_color = new_color
    random_fab.bgcolor = get_complementary_color(new_color)
    update_text_colors(page.bgcolor)


# Components for the page

  random_fab = ft.FloatingActionButton(
    icon=ft.Icons.SHUFFLE,
    on_click=fab_click,
    tooltip="Randomize background color",
  )

  color1 = ft.TextField(
    on_submit=change_bg,
    on_change=change_bg,
    text_align=ft.TextAlign.CENTER,
  )
  text_elements.append(color1)

  color2 = ft.TextField(
    on_submit=change_bg,
    on_change=change_bg,
    text_align=ft.TextAlign.CENTER,
  )
  text_elements.append(color2)
  
  mixed_color = ft.Text(
    value=initial_bg,
    theme_style=ft.TextThemeStyle.DISPLAY_LARGE,
    selectable=True,
  )
  text_elements.append(mixed_color)

  mixed_rgb = ft.Text(
    value=tuple(int(initial_bg[i:i+2], 16) for i in (1, 3, 5)).__str__(),
    theme_style=ft.TextThemeStyle.DISPLAY_LARGE,
    selectable=True,
  )
  text_elements.append(mixed_rgb)

  sanzo_link = ft.IconButton(
    icon=ft.Icons.CREDIT_CARD_SHARP,
    tooltip="Get Swatches",
    visible=False
  )

  update_text_colors(initial_bg)
  
  class DisplayArea(ft.Column):
    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.controls = [
        ft.Container(
          content=ft.Row(
            controls=[
              color1,
              color2
            ],
            alignment=ft.MainAxisAlignment.CENTER,
          ),
          padding=ft.padding.all(20),
        ),
        mixed_color,
        mixed_rgb,
        sanzo_link
      ]

  page.add(
    DisplayArea(
      expand=True,
      alignment=ft.MainAxisAlignment.CENTER,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
  )
  
  page.add(random_fab)

  update_text_colors(initial_bg)
  page.update()


if __name__ == "__main__":
  ft.app(target=main)
