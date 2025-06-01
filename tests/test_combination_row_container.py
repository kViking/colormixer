import pytest
from components.swatches import CombinationRowContainer

def test_combination_row_container():
    container = CombinationRowContainer()
    # Should have a combination_row attribute
    assert hasattr(container, 'combination_row')
    # Should be a Flet Container with content set
    assert hasattr(container, 'content')
    assert container.content == container.combination_row
