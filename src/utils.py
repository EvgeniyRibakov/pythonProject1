import json
import logging
import os
from typing import Any, Dict, List

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

logger = logging.getLogger(__name__)


def read_json_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Read a JSON file and return data.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        List[Dict[str, Any]]: A list of data from the file or an empty list if the file is not valid.
    """

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            logger.debug(f"Чтение JSON файла: {file_path}")
            data = json.load(file)
            if isinstance(data, list):
                return data
            else:
                logger.error(f"Неверный формат данных: ожидается список, получен {type(data)}")
                return []
    except FileNotFoundError:
        logger.error(f"Файл не найден: {file_path}")
        return []
    except json.JSONDecodeError:
        logger.error(f"Ошибка декодирования JSON файла: {file_path}")
        return []


def convert_currency(amount: float, from_currency: str) -> float:
    """
    Convert an amount from one currency to RUB.

    Args:
        amount (float): The amount to convert.
        from_currency (str): The currency to convert from.

    Returns:
        float: The amount converted to RUB.

    Raises:
        ValueError: If the API request fails.
    """
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
    """
    Convert the transaction amount to RUB.

    Args:
        transaction (dict): A transaction with an amount and currency.

    Returns:
        float: The transaction amount in RUB.

    Raises:
        ValueError: If transaction data is incomplete or invalid.
    """
    utils_logger.debug(f"Конвертация суммы транзакции в рубли: {transaction}")  # Логгирование начала
    amount = float(transaction.get("operationAmount", {}).get("amount", 0))
    currency = transaction.get("operationAmount", {}).get("currency", {}).get("code")

    if amount == 0 or currency is None:
        utils_logger.error("Неполные данные транзакции")
        raise ValueError("Transaction data is incomplete")

    utils_logger.debug(f"Конвертация суммы: {amount} {currency} -> RUB")
    return convert_currency(amount, currency)
