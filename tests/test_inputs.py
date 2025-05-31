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
