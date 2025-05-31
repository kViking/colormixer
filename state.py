from typing import List, Dict, Any
from flet import Page

def add_to_history(page: Page, history: List[Dict[str, Any]], new_color: str, pair=None) -> None:
    entry = {"hex": new_color}
    if pair:
        entry["pair"] = pair
    if not history or (isinstance(history[-1], dict) and history[-1].get("hex") != new_color):
        top_10 = history[-10:] if len(history) >= 10 else history
        if any(entry.get("hex") == new_color for entry in top_10):
            return
        history.append(entry)
        page.session.set("history", history)

def clear_fields(color1, color2):
    color1.value = ""
    color2.value = ""
