import json
import logging
import os
from pathlib import Path
from typing import Dict, List

import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")

# --- Логирование модуля utils ---
utils_logger = logging.getLogger("utils")
utils_logger.setLevel(logging.DEBUG)  # Устанавливаем уровень логирования

# Создаем обработчик для записи логов в файл
utils_file_handler = logging.FileHandler("utils.log")

# Создаем форматтер для логов
utils_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Устанавливаем форматтер для обработчика
utils_file_handler.setFormatter(utils_formatter)

# Добавляем обработчик к логгеру
utils_logger.addHandler(utils_file_handler)


def read_json_file(file_path: str) -> List[Dict]:
    """
    Читает JSON файл и возвращает данные в виде списка словарей.
    Если файл пустой, содержит не список или не найден, возвращает пустой список.
    """
    utils_logger.debug(f"Чтение JSON файла: {file_path}")  # Логгирование начала операции
    if not Path(file_path).is_file():
        utils_logger.error(f"Файл не найден: {file_path}")  # Логгирование ошибки
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        utils_logger.error(f"Файл пустой или содержит не список: {file_path}")  # Логгирование ошибки
        return []

    if not isinstance(data, list):
        utils_logger.warning(f"Файл не содержит списка: {file_path}")  # Логгирование предупреждения
        return []

    utils_logger.debug(f"JSON файл успешно прочитан: {file_path}")  # Логгирование успешного завершения
    return data


def convert_currency(amount: float, from_currency: str) -> float:
    """Конвертирует указанную сумму из одной валюты в рубли"""
    utils_logger.debug(f"Конвертация валюты: {amount} {from_currency} -> RUB")  # Логгирование начала
    if from_currency == "RUB":
        utils_logger.debug(f"Валюта уже в рублях: {amount}")
        return amount  # Если валюта уже в рублях, возвращаем сумму без конвертации

    # Определяем URL для запроса к API
    url = f"https://api.exchangeratesapi.io/latest?base={from_currency}&symbols=RUB"

    # Отправляем запрос к API
    utils_logger.debug(f"Отправка запроса к API: {url}")
    response = requests.get(url)

    # Проверяем успешность запроса
    if response.status_code == 200:
        utils_logger.debug(f"Запрос к API успешен: {response.status_code}")
        data = response.json()
        exchange_rate = data["rates"]["RUB"]
        utils_logger.debug(f"Курс валюты: {exchange_rate}")
        return float(amount * exchange_rate)
    else:
        utils_logger.error(f"Ошибка при получении курсов валют: {response.status_code}")  # Логгирование ошибки
        raise ValueError(f"Failed to fetch exchange rates: {response.status_code}")


def transaction_amount_in_rub(transaction: dict) -> float:
    """Конвертирует сумму транзакции в рубли"""
    utils_logger.debug(f"Конвертация суммы транзакции в рубли: {transaction}")  # Логгирование начала
    amount = float(transaction.get("operationAmount", {}).get("amount", 0))
    currency = transaction.get("operationAmount", {}).get("currency", {}).get("code")

    if amount == 0 or currency is None:
        utils_logger.error("Неполные данные транзакции")
        raise ValueError("Transaction data is incomplete")

    utils_logger.debug(f"Конвертация суммы: {amount} {currency} -> RUB")
    return convert_currency(amount, currency)
