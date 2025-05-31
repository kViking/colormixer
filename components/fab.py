import flet as ft
from typing import Callable, List, Dict, Any
from color_utils import get_complementary_color
from .display import MixedColorText, MixedRGBText
from .inputs import ColorInput
from .history import HistoryRow

class RandomFAB(ft.FloatingActionButton):
    """Randomize the background color and update history."""
    def __init__(
        self, page: ft.Page, mixed_color: MixedColorText, mixed_rgb: MixedRGBText, color1: ColorInput, color2: ColorInput,
        update_text_colors: Callable, history: List[Dict[str, Any]], history_row: HistoryRow, **kwargs: Any
    ):
        super().__init__(
            icon=ft.Icons.SHUFFLE,
            on_click=self._handle_click,
            tooltip="Randomize background color",
            **kwargs,
        )
        self.page = page
        self.mixed_color = mixed_color
        self.mixed_rgb = mixed_rgb
        self.color1 = color1
        self.color2 = color2
        self.update_text_colors = update_text_colors
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
        if self.page is not None:
            self.page.bgcolor = new_color
        try:
            self.mixed_color.spans[0].text = new_color
            self.mixed_rgb.spans[0].text = str(tuple(int(new_color[i:i+2], 16) for i in (1, 3, 5)))
        except (AttributeError, IndexError):
            pass
        for field in (self.color1, self.color2):
            field.value = ""
        if not self.history or self.history[-1] != new_color:
            self.history.append({'hex': new_color})
            self.history_row.update_history(self.history)
        self.update_text_colors(new_color)
        if self.page is not None:
            self.page.update()
