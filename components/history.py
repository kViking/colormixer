import flet as ft
from typing import List, Dict, Any, Callable
from color_utils import get_complementary_color
import math

class HistoryRow(ft.Row):
    """Display the color mixing history as clickable items."""
    def __init__(self, history: List[Dict[str, Any]], change_bg: Callable, **kwargs: Any):
        super().__init__(
            controls=[
                HistoryItem(
                    item,
                    change_bg=change_bg,
                )
                for item in history
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.START,
            scroll=ft.ScrollMode.AUTO,
            spacing=0,
            **kwargs,
        )
        self.history = history[::-1]
        self.change_bg = change_bg

    def update_history(self, history: List[Dict[str, Any]]) -> None:
        self.controls.clear()
        history = history[::-1]
        for item in history:
            self.controls.append(
                HistoryItem(item, self.change_bg)
            )

class HistoryItem(ft.Container):
    """Restore a previously selected color when clicked."""
    def __init__(self, item: Dict[str, Any], change_bg: Callable, **kwargs: Any):
        super().__init__(**kwargs)
        self.item = item
        hex_color = item['hex'] if isinstance(item, dict) and 'hex' in item else str(item)
        self.complementary_color = get_complementary_color(hex_color)
        self.on_click = lambda e: change_bg(self.item, clear_fields=True)
        self.bgcolor = hex_color
        self.alignment = ft.alignment.center
        text_value = hex_color
        self.content = ft.Text(
            value=text_value,
            text_align=ft.TextAlign.CENTER,
            color=self.complementary_color,
            height=65,
            width=65,
            rotate=ft.Rotate(angle=math.pi / 2),
        )
