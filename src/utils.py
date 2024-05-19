import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")


def read_json_file(file_path: str) -> List[Dict]:
    """
    Читает JSON файл и возвращает данные в виде списка словарей.
    Если файл пустой, содержит не список или не найден, возвращает пустой список.
    """
    if not Path(file_path).is_file():
        print("Файл не найден.")
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        print("Файл пустой или содержит не список.")
        return []

    if not isinstance(data, list):
        print("Файл не содержит списка.")
        return []

    return data


# --- Функция get_currency_rate для получения курса валют ---
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


def convert_currency(transaction: Dict[str, Any], api_key: str) -> Optional[float]:
    """
    Конвертирует сумму транзакции из исходной валюты в рубли.
    """
    amount = transaction.get("amount")
    if amount is None:
        return None

    currency = transaction.get("currency")
    if currency == "RUB":
        return float(amount)
    elif currency in ["USD", "EUR"]:
        rate = get_currency_rate(currency, api_key)
        if rate is not None:
            return float(round(amount * rate * get_currency_rate("RUB", api_key), 2))
    return None
