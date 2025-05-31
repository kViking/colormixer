import re
from typing import Optional
import colorsys

def normalize(color: Optional[str]) -> str:
    """Normalize a color string to a hex format or return 'INVALID'."""
    if not color:
        return 'INVALID'
    color = color.strip()
    if color.startswith('(') and color.endswith(')'):
        rgb = tuple(map(int, color[1:-1].split(',')))
        return "#{:02x}{:02x}{:02x}".format(*rgb)
    color_no_commas = color.replace(',', ' ')
    if len(color_no_commas.split()) == 3:
        rgb = tuple(map(int, color_no_commas.split()))
        return "#{:02x}{:02x}{:02x}".format(*rgb)
    hex_pattern = re.compile(r"^#?[0-9a-fA-F]{6}$")
    if hex_pattern.match(color):
        return color.lower() if color.startswith('#') else '#' + color.lower()
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

def find_closest_swatch(color: Optional[str], swatches) -> Optional[dict]:
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

def hex_to_rgb(hex_color: Optional[str]) -> str:
    """Convert a hex color to an RGB tuple."""
    hex_color = normalize(hex_color)
    if hex_color == 'INVALID':
        raise ValueError('Invalid hex color input')
    rgb = (int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16))
    return f"({rgb[0]}, {rgb[1]}, {rgb[2]})"