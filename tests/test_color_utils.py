import pytest
from color_utils import normalize, hexmixer, get_complementary_color, find_closest_swatch, CloseSwatch

@pytest.mark.parametrize("input_color,expected", [
    ("#ffffff", "#ffffff"),
    ("ffffff", "#ffffff"),
    ("(255,255,255)", "#ffffff"),
    ("255,255,255", "#ffffff"),
    ("255 255 255", "#ffffff"),
    (None, "INVALID"),
    ("notacolor", "INVALID"),
])
def test_normalize(input_color, expected):
    assert normalize(input_color) == expected

def test_hexmixer():
    assert hexmixer("#ffffff", "#000000") == "#7f7f7f"
    assert hexmixer("#ff0000", "#00ff00") == "#7f7f00"
    with pytest.raises(ValueError):
        hexmixer("INVALID", "#000000")

def test_get_complementary_color():
    assert get_complementary_color("#ffffff").startswith("#")
    assert get_complementary_color("#000000").startswith("#")

def test_find_closest_swatch():
    swatches = [
        {"hex": "#ff0000", "name": "Red", "combinations": ["A"]},
        {"hex": "#00ff00", "name": "Green", "combinations": ["B"]},
        {"hex": "#0000ff", "name": "Blue", "combinations": ["C"]},
    ]
    result = find_closest_swatch("#ff0001", swatches)
    assert isinstance(result, dict)
    assert result["hex"] == "#ff0000"
    assert "name" in result
    assert "combinations" in result
    assert find_closest_swatch("#123456", swatches) is None
