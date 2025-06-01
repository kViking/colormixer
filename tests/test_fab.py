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
        class SessionDict(dict):
            def get(self, key, default=None):
                return super().get(key, default)
            def set(self, key, value):
                self[key] = value
        self.session = SessionDict()  # Provide get/set methods for compatibility
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
    complementary_color_text = MixedColorText('#654321', on_click=lambda e: None)  # Dummy for required arg
    fab = RandomFAB(page, mixed_color, mixed_rgb, color1, color2, dummy_update_text_colors, history, history_row, complementary_color_text)
    fab._handle_click(DummyEvent())  # type: ignore
    # The RandomFAB does not append to history directly; test that update_text_colors was called with a hex string
    assert 'arg' in called
    assert isinstance(called['arg'], str)
    assert called['arg'].startswith('#')
