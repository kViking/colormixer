import pytest
from components.display import MixedColorText, MixedRGBText, ComplementaryColorText, ColorDisplayColumn
from core.color_utils import get_complementary_color
import flet as ft
from typing import cast

def get_text_color(text_ctrl):
    # Helper to get color from TextStyle or None
    style = text_ctrl.style
    if style and hasattr(style, 'color'):
        return style.color
    return None

def get_span_color(span):
    style = span.style
    if style and hasattr(style, 'color'):
        return style.color
    return None

def test_mixed_color_text():
    mct = MixedColorText('#abcdef', on_click=lambda e: None)
    text = cast(ft.Text, mct.controls[0])
    label = cast(ft.Text, mct.controls[1])
    assert text.spans[0].text == '#abcdef'
    assert label.value == 'BACKGROUND'
    assert get_text_color(label) == get_complementary_color('#abcdef')
    try:
        mct.update_color('#123456')
        assert get_span_color(text.spans[0]) == '#123456'
        assert get_text_color(label) == '#123456'
    except Exception:
        pytest.fail('update_color raised')

def test_mixed_rgb_text():
    mrt = MixedRGBText('#abcdef', on_click=lambda e: None)
    text = cast(ft.Text, mrt.controls[0])
    label = cast(ft.Text, mrt.controls[1])
    assert isinstance(text.spans[0].text, str)
    assert label.value == 'RGB'
    assert get_text_color(label) == get_complementary_color('#abcdef')
    try:
        mrt.update_color('#654321')
        assert get_span_color(text.spans[0]) == '#654321'
        assert get_text_color(label) == '#654321'
    except Exception:
        pytest.fail('update_color raised')

def test_complementary_color_text():
    cct = ComplementaryColorText(complementary_color='#abcdef', on_click=lambda e: None)
    text = cast(ft.Text, cct.controls[0])
    label = cast(ft.Text, cct.controls[1])
    assert text.spans[0].text == '#abcdef'
    assert label.value == 'COMPLEMENTARY'
    assert get_text_color(label) == '#abcdef'
    try:
        cct.update_color('#654321')
        assert get_span_color(text.spans[0]) == '#654321'
        assert get_text_color(label) == '#654321'
    except Exception:
        pytest.fail('update_color raised')

def test_color_display_column():
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
