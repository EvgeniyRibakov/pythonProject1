import json
import logging
import os
from pathlib import Path
from typing import Dict, List

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


def convert_currency(amount: float, from_currency: str) -> float:
    """Конвертирует указанную сумму из одной валюты в рубли"""
    if from_currency == "RUB":
        return amount  # Если валюта уже в рублях, возвращаем сумму без конвертации

    # Определяем URL для запроса к API
    url = f"https://api.exchangeratesapi.io/latest?base={from_currency}&symbols=RUB"

    # Отправляем запрос к API
    response = requests.get(url)

    # Проверяем успешность запроса
    if response.status_code == 200:
        data = response.json()
        exchange_rate = data["rates"]["RUB"]
        return float(amount * exchange_rate)
    else:
        raise ValueError(f"Failed to fetch exchange rates: {response.status_code}")


def transaction_amount_in_rub(transaction: dict) -> float:
    """Конвертирует сумму транзакции в рубли"""
    amount = float(transaction.get("operationAmount", {}).get("amount", 0))
    currency = transaction.get("operationAmount", {}).get("currency", {}).get("code")

    if amount == 0 or currency is None:
        raise ValueError("Transaction data is incomplete")

    return convert_currency(amount, currency)


# Создание отдельного объекта логгера для модуля utils
utils_logger = logging.getLogger('utils')
utils_logger.setLevel(logging.INFO)  # Установка уровня логирования на INFO

# Настройка file_handler для логгера модуля utils
utils_file_handler = logging.FileHandler('utils.log', mode='w')
utils_file_handler.setLevel(logging.INFO)  # Установка уровня логирования обработчика на INFO

# Настройка форматтера для логгера модуля utils
utils_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
utils_file_handler.setFormatter(utils_formatter)

# Добавление обработчика файлов к логгеру модуля utils
utils_logger.addHandler(utils_file_handler)


# Функция модуля utils с логированием успешного случая использования
def successful_function_utils() -> None:
    """
    Записывает сообщение в лог, указывая на успешное выполнение функции модуля utils.
    """
    utils_logger.info('Успешное выполнение функции модуля utils')


def error_function_utils() -> None:
    """
    Функция модуля utils с логированием ошибочного случая использования
    """
    try:
        result = 10 / 0
    except Exception as e:
        utils_logger.error('Ошибка')
