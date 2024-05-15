import os
from typing import Any, Dict, Optional

import requests
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()
api_key = os.getenv("API_KEY")


def get_currency_rate(base_currency: str, target_currency: str, api_key: str) -> Optional[float]:
    """
    Получает курс валюты по коду валюты используя API сайта apilayer.
    """
    url = f"https://api.apilayer.com/exchangerates_data/latest?base={base_currency}&symbols={target_currency}"
    headers = {"apikey": api_key}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        rates = response.json().get("rates", {})
        rate = rates.get(target_currency)
        if rate is not None:
            return float(rate)
    return None


def convert_currency(transaction: Dict[str, Any], api_key: str) -> Optional[float]:
    """
    Конвертирует сумму транзакции из исходной валюты в рубли.
    """
    amount = transaction.get("amount")
    if amount is None:
        return None  # Добавляем проверку на None для суммы транзакции

    currency = transaction.get("currency")
    if currency in ["USD", "EUR"]:
        rate = get_currency_rate(currency, "RUB", api_key)
        if rate is not None:
            return float(round(amount * rate, 2))
    return None
