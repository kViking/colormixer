import pytest
import os

def test_inno_setup_script_exists():
    assert os.path.exists('inno-colormixer.iss')

def test_wbuild_script_exists():
    assert os.path.exists('wbuild.sh')
