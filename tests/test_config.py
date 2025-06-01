import pytest
import config

def test_config_structure():
    assert isinstance(config.CONFIG, dict)
    assert 'swatches_file' in config.CONFIG
    assert 'font_family' in config.CONFIG
    assert 'font_path' in config.CONFIG
