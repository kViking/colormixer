import flet as ft
from typing import Callable, Any
from core.color_utils import get_complementary_color, HexToRgb
from typing import cast

class MixedColorText(ft.Row):
    """Display the mixed color hex value, clickable for copy."""
    def __init__(self, initial_bg: str, on_click: Callable, **kwargs: Any):
        super().__init__(
                vertical_alignment=ft.CrossAxisAlignment.START,
                controls = [
                    ft.Text(
                        theme_style=ft.TextThemeStyle.DISPLAY_LARGE,
                        spans=[ft.TextSpan(
                            initial_bg, 
                            on_click=on_click,
                            on_enter=self._on_mouse_enter,
                            on_exit=self._on_mouse_leave,
                        )],
                        **kwargs
                    ),
                    ft.Text(
                        theme_style=ft.TextThemeStyle.BODY_SMALL,
                        value="[BACKGROUND]",
                        visible=False,
                        color=get_complementary_color(initial_bg),
                    )
                ]
        )
    def update_color(self, color: str) -> None:
        text = cast(ft.Text, self.controls[0])
        text.spans[0].style = ft.TextStyle(color=color)
        label = cast(ft.Text, self.controls[1])
        label.color = color

    def update_text(self, new_text: str) -> None:
        text = cast(ft.Text, self.controls[0])
        text.spans[0].text = new_text
        
    def _on_mouse_enter(self, e: ft.ControlEvent) -> None:
        """Handle mouse enter event to show the background label."""
        self.controls[1].visible = True
        e.page.update()
        
    def _on_mouse_leave(self, e: ft.ControlEvent) -> None:
        """Handle mouse leave event to hide the background label."""
        self.controls[1].visible = False
        e.page.update()

class ComplementaryColorText(ft.Row):
    """Display the complementary color, clickable for copy."""
    def __init__(self, complementary_color: str, on_click: Callable, **kwargs: Any):
        super().__init__(
            vertical_alignment=ft.CrossAxisAlignment.START,
            controls=[
                ft.Text(
                    theme_style=ft.TextThemeStyle.DISPLAY_SMALL,
                    spans=[
                        ft.TextSpan(
                            complementary_color,
                            on_click=on_click,
                            style=ft.TextStyle(color=complementary_color),
                            on_enter=self._on_mouse_enter,
                            on_exit=self._on_mouse_leave,
                        )
                    ],
                    **kwargs,
                ),
                ft.Text(
                    theme_style=ft.TextThemeStyle.BODY_SMALL,
                    value="[COMPLEMENTARY]",
                    visible=False,
                    color=complementary_color,
                )
            ]
        )
    def update_color(self, new_color: str) -> None:
        text = cast(ft.Text, self.controls[0])
        text.spans[0].style = ft.TextStyle(color=new_color)
        label = cast(ft.Text, self.controls[1])
        label.color = new_color

    def update_text(self, new_text: str) -> None:
        text = cast(ft.Text, self.controls[0])
        text.spans[0].text = new_text
    def _on_mouse_enter(self, e: ft.ControlEvent) -> None:
        self.controls[1].visible = True
        e.page.update()
    def _on_mouse_leave(self, e: ft.ControlEvent) -> None:
        self.controls[1].visible = False
        e.page.update()

class MixedRGBText(ft.Row):
    """Display the mixed color as an RGB tuple, clickable for copy."""
    def __init__(self, initial_bg: str, on_click: Callable, **kwargs: Any):
        rgb_str = HexToRgb(initial_bg).string
        comp_color = get_complementary_color(initial_bg)
        super().__init__(
            vertical_alignment=ft.CrossAxisAlignment.START,
            controls=[
                ft.Text(
                    theme_style=ft.TextThemeStyle.DISPLAY_LARGE,
                    selectable=True,
                    spans=[ft.TextSpan(text=rgb_str, on_click=on_click, style=ft.TextStyle(color=comp_color),
                        on_enter=self._on_mouse_enter, on_exit=self._on_mouse_leave)],
                    **kwargs,
                ),
                ft.Text(
                    theme_style=ft.TextThemeStyle.BODY_SMALL,
                    value="[RGB]",
                    visible=False,
                    color=comp_color,
                )
            ]
        )
    def update_color(self, color: str) -> None:
        text = cast(ft.Text, self.controls[0])
        text.spans[0].style = ft.TextStyle(color=color)
        label = cast(ft.Text, self.controls[1])
        label.color = color

    def update_text(self, new_text: str) -> None:
        text = cast(ft.Text, self.controls[0])
        text.spans[0].text = new_text
    def _on_mouse_enter(self, e: ft.ControlEvent) -> None:
        self.controls[1].visible = True
        e.page.update()
    def _on_mouse_leave(self, e: ft.ControlEvent) -> None:
        self.controls[1].visible = False
        e.page.update()

class ColorDisplayColumn(ft.Container):
    """A visual grouping for the main color display area."""
    def __init__(self, complementary_color_text, mixed_color, mixed_rgb, combination_row, **kwargs):
        # Remove alignment from kwargs if present to avoid double assignment
        alignment = kwargs.pop('alignment', None)
        super().__init__(
            content=ft.Column(
                controls=[
                    complementary_color_text,
                    mixed_color,
                    mixed_rgb,
                    combination_row,
                ],
                alignment=ft.MainAxisAlignment.END,
                horizontal_alignment=ft.CrossAxisAlignment.START,
            ),
            alignment=alignment,
            **kwargs
        )
