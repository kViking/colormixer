import pytest
from hotkeys import make_hotkey_handler
from typing import Any

class DummyPage:
    def __init__(self):
        self.bgcolor = '#123456'
        self.events = []
    def update(self):
        self.events.append('update')

def test_make_hotkey_handler_runs():
    called = {'flag': False}
    def dummy_change_bg(arg, clear_fields=False):
        called['flag'] = True
    page: Any = DummyPage()  # type: ignore
    handler = make_hotkey_handler(page, dummy_change_bg)
    e = type('E', (), {'key': 'Arrow Up', 'shift': False})()
    handler(e)  # type: ignore
    assert called['flag']
