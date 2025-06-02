import pytest
import core.config

def test_config_structure():
    assert isinstance(core.config.CONFIG, dict)
    assert 'swatches_file' in core.config.CONFIG
    assert 'font_family' in core.config.CONFIG
    assert 'font_path' in core.config.CONFIG
