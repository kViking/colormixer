import pytest
from components.swatches import CombinationRow, ColorSwatch
from color_utils import get_complementary_color, CloseSwatch
from typing import Any

class DummyPage:
    def __init__(self):
        self.bgcolor = '#ffffff'
        self.updated = False
        self.opened = []
    def update(self):
        self.updated = True
    def open(self, obj):
        self.opened.append(obj)

class DummyControlEvent:
    def __init__(self, text):
        self.control = type('C', (), {'text': text})()

@pytest.mark.filterwarnings('ignore')
def test_combination_row_update(monkeypatch):
    page: Any = DummyPage()  # type: ignore
    combination_row = CombinationRow()
    match: CloseSwatch = {'hex': '#ff0000', 'name': 'Red', 'combinations': ['A', 'B']}
    called = {}
    def dummy_bottom_sheet(c, m, *args, **kwargs):
        called['combo'] = c
        called['match'] = m
        return object()
    combination_row.update_combination_row(match, page, dummy_bottom_sheet)  # type: ignore
    assert len(combination_row.controls) == 2
    # Simulate click
    e = DummyControlEvent('A')
    combination_row._handle_combo_click(e)  # type: ignore
    assert called['combo'] == 'A'
    assert called['match'] == match

@pytest.mark.filterwarnings('ignore')
def test_color_swatch_click(monkeypatch):
    called = {}
    def dummy_change_bg(arg):
        called['arg'] = arg
    swatch = ColorSwatch('#00ff00', 'Green', change_bg=dummy_change_bg, on_click=lambda e: None, palette=['#00ff00'], combination='B')
    class DummyControlEvent:
        pass
    swatch._handle_click(DummyControlEvent())  # type: ignore
    assert called['arg']['hex'] == '#00ff00'
    assert called['arg']['palette_colors'] == ['#00ff00']
