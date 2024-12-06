from typing import Dict, List


def get_key_state(data: dict, state: str = "EXECUTED") -> list:
    """
    Get transactions by state.

    Args:
        data (dict): Dictionary with transaction data.
        state (str): Transaction state to filter by. Default is "EXECUTED".

    Returns:
        list: A list of transactions with the given state.
    """
    return [item for item in data if item.get("state") == state]


def sorted_dates(data: List[Dict], order: str = "increasing") -> List[Dict]:
    """
    Sort transactions by date.

    Args:
        data (List[Dict]): List of transactions.
        order (str): Sort order, "increasing" (default) for oldest first, or "decreasing" for newest first.

    Returns:
        List[Dict]: A sorted list of transactions by date.
    """
    return sorted(data, key=lambda x: x["date"], reverse=(order == "decreasing"))
