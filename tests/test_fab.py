import pytest
from components.fab import RandomFAB
from components.history import HistoryRow
from typing import Any
from types import SimpleNamespace

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
    def __init__(self, page=None):
        self.page = page

def test_random_fab_click():
    page: Any = DummyPage()  # type: ignore
    history = []
    history_row = HistoryRow(history, lambda c: None)
    called = {}
    def dummy_change_bg(arg, *args, **kwargs):
        called['arg'] = arg
    fab = RandomFAB(page, update_text_colors=dummy_change_bg, history=history, history_row=history_row)
    # Use a mock object with a .page attribute to simulate Flet's ControlEvent
    class MockEvent:
        def __init__(self, page):
            self.page = page
    event = MockEvent(page)
    fab._handle_click(event)  # type: ignore
    # The RandomFAB does not append to history directly; test that change_bg was called with a hex string
    assert 'arg' in called
    assert isinstance(called['arg'], str)
    assert called['arg'].startswith('#')
    from components.display import MixedColorText
    mct = MixedColorText('#123456', on_click=lambda e: None)
    label = mct.controls[1]
    import flet as ft
    if isinstance(label, ft.Text):
        assert getattr(label, 'value', None) == '[BACKGROUND]'
