import flet as ft
from typing import Callable, List, Dict, Any
from core.color_utils import get_complementary_color
from core.state import add_to_history
from .history import HistoryRow

class RandomFAB(ft.FloatingActionButton):
    """Randomize the background color and update history."""
    def __init__(
        self, page: ft.Page, update_text_colors: Callable, history: List[Dict[str, Any]], history_row: HistoryRow, **kwargs: Any
    ):
        super().__init__(
            icon=ft.Icons.SHUFFLE,
            on_click=self._handle_click,
            tooltip="Randomize background color",
            **kwargs,
        )
        self.page = page
        self.change_bg = update_text_colors  # Rename for clarity
        self.history = history
        self.history_row = history_row
        self.on_click = self._handle_click

    def update_color(self, color: str) -> None:
        self.bgcolor = color
        if hasattr(self, 'page') and self.page is not None and hasattr(self.page, 'bgcolor') and isinstance(self.page.bgcolor, str):
            self.foreground_color = self.page.bgcolor
        else:
            self.foreground_color = get_complementary_color(color)

    def _handle_click(self, e: ft.ControlEvent) -> None:
        import random
        new_color = f"#{random.randint(0, 0xFFFFFF):06x}"
        e.page.bgcolor = new_color
        add_to_history(e.page, self.history, new_color)
        self.history_row.update_history(self.history)
        self.change_bg(new_color)
        e.page.update()
