import flet as ft
from typing import Callable, Any
from color_utils import get_complementary_color, HexToRgb

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
        rgb_str = HexToRgb(initial_bg).string
        super().__init__(
            theme_style=ft.TextThemeStyle.DISPLAY_LARGE,
            selectable=True,
            spans=[ft.TextSpan(text=rgb_str, on_click=on_click, style=ft.TextStyle(color=get_complementary_color(initial_bg)))],
            **kwargs,
        )
    def update_color(self, color) -> None:
        self.spans[0].style = ft.TextStyle(color=color)

class ColorDisplayColumn(ft.Container):
    """A visual grouping for the main color display area."""
    def __init__(self, complementary_color_text, mixed_color, mixed_rgb, swatch_row, **kwargs):
        # Remove alignment from kwargs if present to avoid double assignment
        alignment = kwargs.pop('alignment', None)
        super().__init__(
            content=ft.Column(
                controls=[
                    complementary_color_text,
                    mixed_color,
                    mixed_rgb,
                    swatch_row,
                ],
                alignment=ft.MainAxisAlignment.END,
                horizontal_alignment=ft.CrossAxisAlignment.START,
            ),
            alignment=alignment,
            **kwargs
        )
