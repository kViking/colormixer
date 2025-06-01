import pytest
from components.display import MixedColorText, MixedRGBText, ComplementaryColorText
from typing import Any

class DummyStyle:
    def __init__(self, color=None):
        self.color = color

class DummySpan:
    def __init__(self, text):
        self.text = text
        self.style = DummyStyle()

class DummyEvent:
    pass

def test_mixed_color_text():
    mct = MixedColorText('#abcdef', on_click=lambda e: None)
    # Instead of patching, just check the text and that update_color doesn't error
    assert mct.spans[0].text == '#abcdef'
    try:
        mct.update_color('#123456')
    except Exception:
        pytest.fail('update_color raised')

def test_mixed_rgb_text():
    mrt = MixedRGBText('#abcdef', on_click=lambda e: None)
    assert isinstance(mrt.spans[0].text, str)
    try:
        mrt.update_color('#654321')
    except Exception:
        pytest.fail('update_color raised')

def test_complementary_color_text():
    cct = ComplementaryColorText(complementary_color='#abcdef', on_click=lambda e: None)
    assert cct.spans[0].text == '#abcdef'
    try:
        cct.update_color('#654321')
    except Exception:
        pytest.fail('update_color raised')

def test_color_display_column():
    from components.display import MixedColorText, MixedRGBText, ComplementaryColorText, ColorDisplayColumn
    mct = MixedColorText('#123456', on_click=lambda e: None)
    mrt = MixedRGBText('#123456', on_click=lambda e: None)
    cct = ComplementaryColorText('#654321', on_click=lambda e: None)
    class DummyRow:
        pass
    col = ColorDisplayColumn(
        complementary_color_text=cct,
        mixed_color=mct,
        mixed_rgb=mrt,
        combination_row=DummyRow(),
        alignment=None,
    )
    assert hasattr(col, 'content')
