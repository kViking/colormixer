import flet as ft
from typing import Callable, Any
from core.color_utils import get_complementary_color

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

class AddToPaletteButton(ft.IconButton):
    """IconButton for adding a color to the palette, with color update support."""
    def __init__(self, icon=ft.Icons.ADD_OUTLINED, icon_color=None, **kwargs):
        super().__init__(icon=icon, icon_color=icon_color, **kwargs)
    def update_color(self, color: str) -> None:
        self.icon_color = color

class InputRow(ft.Row):
    """A row containing the two color input fields and (optionally) the user palette column."""
    def __init__(self, color1, color2, user_palette=None, **kwargs):
        controls = [
            ft.Container(),  # Dummy empty container for spacing or layout
            ft.Container(
                padding=ft.Padding(35, 0, 0, 0),
                content=ft.Row([color1, color2], alignment=ft.MainAxisAlignment.CENTER),
                alignment=ft.alignment.center,
                border_radius=ft.BorderRadius(0, 0, 0, 0),
            )
        ]
        # Only add the palette column, not the add button, to the input row
        if user_palette is not None:
            controls.append(user_palette)
        # Remove alignment from kwargs if present to avoid double assignment
        kwargs.pop('alignment', None)
        super().__init__(
            controls=controls,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            **kwargs,
        )
