import json
from typing import Any, Dict, List, Optional

import requests


def read_json_file(file_path: str) -> List[Dict]:
    """
    Читает JSON файл и возвращает данные в виде списка словарей.
    Если файл пустой, содержит не список или не найден, возвращает пустой список.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
            else:
                print("Файл не содержит списка.")
                return []
    except FileNotFoundError:
        print("Файл не найден.")
        return []
    except json.JSONDecodeError:
        print("Файл пустой или содержит не список.")
        return []


def get_currency_rate(currency_code: str, api_key: str) -> Optional[float]:
    """
    Получает курс валюты по коду валюты используя API сайта apilayer.
    """
    url = f"https://api.apilayer.com/exchangerates_data/latest?base=USD&symbols={currency_code}"
    headers = {"apikey": api_key}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        rates = response.json().get("rates", {})
        rate = rates.get(currency_code)
        if rate is not None:
            return float(rate)
    return None


def convert_currency(transaction: Dict[str, Any], rate: float) -> float:
    """
    Конвертирует сумму транзакции из USD или EUR в рубли.
    """
    amount = transaction["amount"]
    return float(round(amount * rate, 2))
