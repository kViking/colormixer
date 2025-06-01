import pytest
import types
import main
from typing import Any

class DummyPage:
    def __init__(self):
        self.fonts = {}
        self.theme = None
        self.title = None
        self.vertical_alignment = None
        self.bgcolor = '#123456'
        self.controls = []
        self.floating_action_button = None
        self.events = []
        class SessionDict(dict):
            def get(self, key, default=None):
                return super().get(key, default)
            def set(self, key, value):
                self[key] = value
        self.session = SessionDict()  # Provide get/set methods for compatibility
    def add(self, control):
        self.controls.append(control)
    def open(self, dialog):
        self.events.append('open')
    def set_clipboard(self, text):
        self.events.append(f'clipboard:{text}')
    def update(self):
        self.events.append('update')

def test_main_runs(monkeypatch):
    # Patch out config and random
    monkeypatch.setattr(main, 'CONFIG', {
        'font_family': 'VCR OSD Mono',
        'font_path': 'VCR_OSD_MONO.ttf',
        'theme': {'font_family': 'VCR OSD Mono'},
        'swatches_file': 'swatches.json',
    })
    monkeypatch.setattr(main, 'json', types.SimpleNamespace(load=lambda f: [
        {"hex": "#ff0000", "name": "Red", "combinations": ["A"]},
        {"hex": "#00ff00", "name": "Green", "combinations": ["B"]},
    ]))
    monkeypatch.setattr(main.random, 'randint', lambda a, b: 0x123456)
    # Run main
    page: Any = DummyPage()  # type: ignore
    main.main(page)
    # Check that UI was built and updated
    assert page.bgcolor == '#123456'
    assert any('update' in e for e in page.events)
    assert page.floating_action_button is not None
    assert page.controls
