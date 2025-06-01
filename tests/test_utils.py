import pytest
import importlib.util

def test_utils_session_importable():
    import sys
    import os
    # Ensure utils is in sys.path
    utils_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils'))
    if utils_path not in sys.path:
        sys.path.insert(0, utils_path)
    spec = importlib.util.find_spec('session')
    assert spec is not None
    if spec.loader is not None:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        assert hasattr(module, '__file__')
    else:
        pytest.skip('spec.loader is None, cannot import module')
