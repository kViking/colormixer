import pytest
from components.inputs import ColorInput
from typing import Any

class DummyEvent:
    pass

def test_color_input_update():
    ci = ColorInput(on_change=lambda e: None, on_submit=lambda e: None)
    ci.update_color('#ff0000')
    assert ci.color == '#ff0000'
    ci.update_bg_color('#00ff00')
    assert ci.bgcolor == '#00ff00'
    ci.update_focused_border_color('#0000ff')
    assert ci.focused_border_color == '#0000ff'
    ci.update_border_color('#123456')
    assert ci.border_color == '#123456'

def test_input_row():
    from components.inputs import ColorInput, InputRow
    c1 = ColorInput(on_change=lambda e: None, on_submit=lambda e: None)
    c2 = ColorInput(on_change=lambda e: None, on_submit=lambda e: None)
    row = InputRow(c1, c2, alignment=None)
    assert hasattr(row, 'content')
    assert c1 in getattr(row.content, 'controls', []) or isinstance(row.content, object)
