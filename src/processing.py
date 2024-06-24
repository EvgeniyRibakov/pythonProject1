from typing import Dict, List


def get_key_state(data: dict, state: str = "EXECUTED") -> list:
    return [item for item in data if item.get("state") == state]


def sorted_dates(data: List[Dict], order: str = "increasing") -> List[Dict]:
    """Сортирует транзакции по дате"""
    return sorted(data, key=lambda x: x["date"], reverse=(order == "decreasing"))
