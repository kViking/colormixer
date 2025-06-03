import flet as ft
from typing import List, Dict, Any, Callable, Optional
from core.color_utils import get_complementary_color
import math

class HistoryRow(ft.Row):
    """Display the color mixing history as clickable items."""
    def __init__(self, history: List[Dict[str, Any]], change_bg: Callable, **kwargs: Any):
        super().__init__(
            controls=[
                HistoryItem(
                    item,
                    change_bg=change_bg,
                    width=65,
                )
                for item in history
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.START,
            scroll=ft.ScrollMode.AUTO,
            spacing=0,
            height=65,
            **kwargs,
        )
        self.history = history[::-1]
        self.change_bg = change_bg

    def update_history(self, history: List[Dict[str, Any]]) -> None:
        self.controls.clear()
        history = history[::-1]
        for item in history:
            self.controls.append(
                HistoryItem(item, self.change_bg, height=65, width=65)
            )

class HistoryItem(ft.Container):
    """Restore a previously selected color when clicked."""
    def __init__(
        self,
        item: Dict[str, Any],
        change_bg: Callable,
        rotate_text: bool = True,
        text_click: Optional[Callable[[ft.ControlEvent], None]] = None,
        **kwargs: Any
    ):
        super().__init__(**kwargs)
        self.item = item
        hex_color = item['hex'] if isinstance(item, dict) and 'hex' in item else str(item)
        self.complementary_color = get_complementary_color(hex_color)
        self.bgcolor = hex_color
        # height and width removed for reusability
        text_value = hex_color
        self.content = ft.Text(
            spans=[
                ft.TextSpan(
                    text=text_value,
                    style=ft.TextStyle(color=self.complementary_color),
                    on_click=text_click
                )
            ],
            text_align=ft.TextAlign.CENTER,
            color=self.complementary_color,
            rotate=ft.Rotate(angle=math.pi / 2) if rotate_text else None,
        )
        self.change_bg = change_bg
        self.on_click = lambda e: self.change_bg(self.item, clear_fields=True)
