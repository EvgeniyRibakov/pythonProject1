from typing import List
from datetime import datetime


def get_key_state(data: dict, state: str = "EXECUTED") -> list:
    return [item for item in data if item.get("state") == state]


def sorted_dates(data: List[dict], reverse: bool = True) -> List[dict]:
    return sorted(data, key=lambda x: datetime.fromisoformat(x["date"]), reverse=reverse)
