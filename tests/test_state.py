import pytest
from core.state import add_to_history

class DummySession:
    def __init__(self):
        self._data = {}
    def set(self, key, value):
        self._data[key] = value
    def get(self, key, default=None):
        return self._data.get(key, default)

class DummyPage:
    def __init__(self):
        self.session = DummySession()

# Patch the type check for testing
import core.state
core.state.Page = DummyPage

def test_add_to_history():
    page = DummyPage()  # type: ignore
    history = []
    add_to_history(page, history, "#123456")  # type: ignore
    assert history[-1]["hex"] == "#123456"
    # Should not add duplicate
    add_to_history(page, history, "#123456")  # type: ignore
    assert len(history) == 1
    # Should add new color
    add_to_history(page, history, "#abcdef")  # type: ignore
    assert history[-1]["hex"] == "#abcdef"
    # Should store in session
    assert page.session._data["history"] == history
