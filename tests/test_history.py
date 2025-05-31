import pytest
from components.history import HistoryRow, HistoryItem
from typing import Any

class DummyEvent:
    pass

def test_history_row_update():
    history = [
        {"hex": "#111111"},
        {"hex": "#222222"},
        {"hex": "#333333"},
    ]
    called = {}
    def dummy_change_bg(arg, clear_fields=False):
        called['arg'] = arg
    row = HistoryRow(history, dummy_change_bg)
    row.update_history(history)
    assert len(row.controls) == 3
    # Simulate click
    item = row.controls[0]
    item.on_click(DummyEvent())  # type: ignore
    assert 'arg' in called

def test_history_item():
    called = {}
    def dummy_change_bg(arg, clear_fields=False):
        called['arg'] = arg
    item = HistoryItem({"hex": "#abcdef"}, dummy_change_bg)
    item.on_click(DummyEvent())  # type: ignore
    assert called['arg']['hex'] == '#abcdef'
