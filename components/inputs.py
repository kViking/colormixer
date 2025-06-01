import flet as ft
from typing import Callable, Any
from color_utils import get_complementary_color

class ColorInput(ft.TextField):
    """Create a text input field for color values."""
    def __init__(self, on_change: Callable, on_submit: Callable, **kwargs: Any):
        super().__init__(
            on_submit=on_submit,
            on_change=on_change,
            text_align=ft.TextAlign.CENTER,
            border_radius=ft.BorderRadius(0,0,0,0),
            width=200,
            **kwargs,
        )

    def set_page(self, page):
        self.page = page

    def update_color(self, color: str) -> None:
        self.color = color
    def update_bg_color(self, color: str) -> None:
        self.bgcolor = color
    def update_focused_border_color(self, color: str) -> None:
        self.focused_border_color = color
    def update_border_color(self, color: str) -> None:
        self.border_color = color

class InputRow(ft.Container):
    """A container for the two color input fields, alignment handled at the container level."""
    def __init__(self, color1: ColorInput, color2: ColorInput, **kwargs: Any):
        super().__init__(
            alignment=kwargs.pop('alignment', None),
            content=ft.Row(
                controls=[color1, color2],
                wrap=True,
            ),
            **kwargs,
        )
