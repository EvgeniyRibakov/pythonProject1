import os
import re
from typing import Any, Dict, List

from src.generators import filter_by_currency, transaction_descriptions
from src.processing import sorted_dates
from src.read_csv_and_xlsx import read_csv_data, read_xlsx_data
from src.utils import read_json_file
from src.widget import convert_date_string, mask_checcking


def filter_by_having_str(transactions: List[Dict[str, Any]], search_string: str) -> List[Dict[str, Any]]:
    """
    Find transactions with a word in the description.

    Args:
        transactions (List[Dict[str, Any]]): List of transactions.
        search_string (str): The word to find in the description.

    Returns:
        List[Dict[str, Any]]: Transactions that have the word.
    """
    return [
        transaction
        for transaction in transactions
        if "description" in transaction and re.search(search_string, transaction["description"])
    ]


def summary_amount(transaction: dict) -> float:
    """
    Calculate the total amount in RUB.

    Args:
        transaction (dict): A transaction with currency and amount.

    Returns:
        float: Total in RUB. Converts EUR and USD to RUB.
    """

    total = 0.0
    currency = transaction.get("operationAmount", {}).get("currency", {}).get("code")
    amount = float(transaction.get("operationAmount", {}).get("amount", 0.0))

    if currency == "RUB":
        total += amount
    elif currency == "EUR":
        total += amount * 94
    elif currency == "USD":
        total += amount * 88

    return total


def return_type_of_file() -> tuple[List[Dict], str]:
    """
    Ask the user to choose a file type and return data.

    Returns:
        tuple[List[Dict], str]: A list of transactions and file type.
    """

    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из json файла")
    print("2. Получить информацию о транзакциях из csv файла")
    print("3. Получить информацию о транзакциях из xlsx файла")
    choice = input("Введите номер пункта меню: ")

    base_path = os.path.join(os.path.dirname(__file__), "..", "data")

    if choice == "1":
        file_path = os.path.join(base_path, "operations.json")
        return read_json_file(file_path), "json"
    elif choice == "2":
        file_path = os.path.join(base_path, "transactions.csv")
        return read_csv_data(file_path), "csv"
    elif choice == "3":
        file_path = os.path.join(base_path, "transactions_excel.xlsx")
        return read_xlsx_data(file_path), "excel"
    else:
        print("Статус операции недоступен")
        return return_type_of_file()


def sort_transactions_by_status(data: List[Dict]) -> List[Dict]:
    """
    Filter transactions by status like EXECUTED, CANCELED.

    Args:
        data (List[Dict]): Transactions data.

    Returns:
        List[Dict]: Transactions with the chosen status.
    """

    print("Выберите статус, по которому необходимо выполнить фильтрацию.")
    status = input("Доступные для сортировки статусы: EXECUTED, CANCELED, PENDING\n").upper()

    if status not in ("EXECUTED", "CANCELED", "PENDING"):
        print("Некорректный статус, повторите ввод.")
        return sort_transactions_by_status(data)

    filtered_data = [transaction for transaction in data if transaction.get("state") == status]
    print(f"Транзакции после фильтрации по статусу ({status}): {len(filtered_data)} найдено")
    return filtered_data


def filter_by_date_and_currency(data: List[Dict], file_type: str) -> List[Dict[Any, Any]]:
    """
    Filter transactions by date and currency.

    Args:
        data (List[Dict]): Transactions data.
        file_type (str): File type (e.g., json, csv, excel).

    Returns:
        List[Dict]: Filtered transactions.
    """

    to_sort = input("Фильтровать операции по дате?\n")
    if to_sort.lower() == "да":
        time = input("По возрастанию или по убыванию?\n")
        if time.lower() == "по возрастанию":
            data = sorted_dates(data)
        elif time.lower() == "по убыванию":
            data = sorted_dates(data, "decreasing")
        else:
            print("Некорректное значение, повторите ввод.")
            return filter_by_date_and_currency(data, file_type)
    elif to_sort.lower() == "нет":
        pass
    else:
        print("Некорректный ответ, повторите ввод.")
        return filter_by_date_and_currency(data, file_type)

    to_sort = input("Выводить только рублевые транзакции?\n")
    if to_sort.lower() == "да":
        filtered_data = filter_by_currency(data, "RUB", file_type)
        return filtered_data
    elif to_sort.lower() == "нет":
        return data
    else:
        print("Некорректный ответ, повторите ввод.")
        return filter_by_date_and_currency(data, file_type)


def sort_by_keyword(data: List[Dict]) -> List[Dict]:
    """
    Find transactions with a key word.

    Args:
        data (List[Dict]): Transactions data.

    Returns:
        List[Dict]: Transactions with the word in the description.
    """

    to_sort = input("Отсортировать список операций по определённому слову в описании?\n")
    if to_sort.lower() == "да":
        to_find = input("Введите?\n")
        return filter_by_having_str(data, to_find)
    elif to_sort.lower() == "нет":
        return data
    else:
        print("Некорректный ввод, повторитe")
        return sort_by_keyword(data)


def output_operations(data: List[Dict]) -> None:
    """
    Print all transactions after filtering.

    Args:
        data (List[Dict]): Transactions data.
    """

    print("Распечатываю итоговый список транзакций...")
    if data and len(data) != 0:
        print(f"\nВсего банковских операций в выборке: {len(data)}\n")
        for operation in data:
            print(
                convert_date_string(operation["date"]),
                next(transaction_descriptions(data)),
            )
            if re.search("Перевод", operation["description"]):
                print(mask_checcking(operation["from"]), " -> ", mask_checcking(operation["to"]))
            else:
                print(mask_checcking(operation["to"]))

            # Проверка и вывод суммы транзакции
            try:
                amount = operation.get("amount", 0.0)
                currency = operation.get("currency_code", "N/A")
                print(f"Сумма: {amount} {currency}")
            except Exception as e:
                print(f"Ошибка при обработке суммы: {e}")
    else:
        print("Не найдено подходящих транзакций под ваши условия фильтрации")


def main() -> None:
    """
    The main function to run the program. It loads data, filters transactions, and prints them.
    """
    data, file_type = return_type_of_file()
    print(f"Загружено {len(data)} транзакций из файла {file_type}")

    data = sort_transactions_by_status(data)
    data = filter_by_date_and_currency(data, file_type)
    data = sort_by_keyword(data)
    output_operations(data)


if __name__ == "__main__":
    main()
