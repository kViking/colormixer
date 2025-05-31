import pytest
from components.fab import RandomFAB
from components.display import MixedColorText, MixedRGBText
from components.inputs import ColorInput
from components.history import HistoryRow
from typing import Any

class DummyPage:
    def __init__(self):
        self.bgcolor = '#123456'
        self.floating_action_button = None
        self.events = []
    def update(self):
        self.events.append('update')

class DummyEvent:
    pass

def test_random_fab_click():
    page: Any = DummyPage()  # type: ignore
    mixed_color = MixedColorText('#123456', on_click=lambda e: None)
    mixed_rgb = MixedRGBText('#123456', on_click=lambda e: None)
    color1 = ColorInput(on_change=lambda e: None, on_submit=lambda e: None)
    color2 = ColorInput(on_change=lambda e: None, on_submit=lambda e: None)
    history = []
    history_row = HistoryRow(history, lambda c: None)
    called = {}
    def dummy_update_text_colors(arg):
        called['arg'] = arg
    fab = RandomFAB(page, mixed_color, mixed_rgb, color1, color2, dummy_update_text_colors, history, history_row)
    fab._handle_click(DummyEvent())  # type: ignore
    assert history
    assert 'hex' in history[-1]
    assert called['arg'].startswith('#')
