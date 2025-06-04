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
    # InputRow is a Row, so check controls directly
    assert hasattr(row, 'controls')
    # The second control is a Container with a Row containing [c1, c2]
    found = False
    for control in row.controls:
        content = getattr(control, 'content', None)
        controls = getattr(content, 'controls', None)
        if controls and c1 in controls and c2 in controls:
            found = True
    assert found, 'ColorInput not found in InputRow controls/content'
