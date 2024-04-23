def get_key_state(data: dict, state: str = "EXECUTED") -> list:
    return [item for item in data if item.get("state") == state]


def sorted_dates(data: list[dict], reverse: bool = False) -> list[dict]:
    sorted_data = sorted(data, key=lambda x: x["date"], reverse=reverse)
    return sorted_data
