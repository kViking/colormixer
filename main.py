import flet as ft
import random
import colorsys

def hexmixer(color1, color2):
  """Mix two hex color codes and return the resulting color."""
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
    page.update()

  def change_bg(e):
    """Change the background color of the page."""
    color1_value = str(color1.value).strip()
    color2_value = str(color2.value).strip()
    new_color = initial_bg
    new_color = hexmixer(color1_value, color2_value)
    page.bgcolor = new_color
    mixed_color.value = new_color
    mixed_rgb.value = "RGB: " + tuple(int(new_color[i:i+2], 16) for i in (1, 3, 5)).__str__()
    update_text_colors(new_color)
    

# Components for the page

  color1 = ft.TextField(
    on_submit=change_bg,
    text_align=ft.TextAlign.CENTER,
    
  )
  text_elements.append(color1)

  color2 = ft.TextField(
    on_submit=change_bg,
    text_align=ft.TextAlign.CENTER,
  )
  text_elements.append(color2)
  
  mixed_color = ft.Text(
    value=initial_bg,
    style=ft.TextThemeStyle.DISPLAY_LARGE
  )
  text_elements.append(mixed_color)

  mixed_rgb = ft.Text(
    value="RGB: " + tuple(int(initial_bg[i:i+2], 16) for i in (1, 3, 5)).__str__(),
    style=ft.TextThemeStyle.DISPLAY_LARGE
  )
  text_elements.append(mixed_rgb)
  
  instruction_text = ft.Text(
    value="Enter two hex color codes to mix them",
    style=ft.TextThemeStyle.DISPLAY_LARGE
  )
  text_elements.append(instruction_text)

  inmstruction_subtext = ft.Text(
    value="Press Enter to mix",
    style=ft.TextThemeStyle.DISPLAY_MEDIUM
  )

  update_text_colors(initial_bg)
  
  class DisplayArea(ft.Column):
    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.controls = [
        instruction_text,
        inmstruction_subtext,
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
        mixed_rgb
      ]

  page.add(
    DisplayArea(
      expand=True,
      alignment=ft.MainAxisAlignment.CENTER,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
  )
  
  # Initialize text colors
  update_text_colors(initial_bg)
  page.update()


if __name__ == "__main__":
  ft.app(target=main)