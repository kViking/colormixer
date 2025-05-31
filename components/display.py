import flet as ft
from typing import Callable, Any
from color_utils import get_complementary_color, hex_to_rgb

class MixedColorText(ft.Text):
    """Display the mixed color hex value, clickable for copy."""
    def __init__(self, initial_bg: str, on_click: Callable, **kwargs: Any):
        super().__init__(
            theme_style=ft.TextThemeStyle.DISPLAY_LARGE,
            spans=[ft.TextSpan(initial_bg, on_click=on_click)],
            **kwargs,
        )
    def update_color(self, color: str) -> None:
        self.spans[0].style = ft.TextStyle(color=color)

class ComplementaryColorText(ft.Text):
    """Display the complementary color, clickable for copy."""
    def __init__(self, complementary_color: str, on_click: Callable, **kwargs: Any):
        super().__init__(
            theme_style=ft.TextThemeStyle.DISPLAY_SMALL,
            spans=[
                ft.TextSpan(
                    complementary_color,
                    on_click=on_click,
                    style=ft.TextStyle(color=complementary_color),
                )
            ],
            **kwargs,
        )
    def update_color(self, new_color: str) -> None:
        self.spans[0].style = ft.TextStyle(color=new_color)

class MixedRGBText(ft.Text):
    """Display the mixed color as an RGB tuple, clickable for copy."""
    def __init__(self, initial_bg: str, on_click: Callable, **kwargs: Any):
        rgb_str = hex_to_rgb(initial_bg)
        super().__init__(
            theme_style=ft.TextThemeStyle.DISPLAY_LARGE,
            selectable=True,
            spans=[ft.TextSpan(text=rgb_str, on_click=on_click, style=ft.TextStyle(color=get_complementary_color(initial_bg)))],
            **kwargs,
        )
    def update_color(self, color) -> None:
        self.spans[0].style = ft.TextStyle(color=color)
