import json
import csv
import pandas as pd
from src.read_csv_and_xlsx import read_csv_data, read_xlsx_data
from src.utils import read_json_file, transaction_amount_in_rub, convert_currency
from src.masks import mask_bills, mask_cards
from src.processing import get_key_state, sorted_dates

# Функция для фильтрации транзакций по статусу
def filter_transactions_by_status(transactions, status):
    # Фильтрация транзакций с проверкой наличия ключа 'state'
    if transactions is None:
        return []  # Возвращаем пустой список, если transactions равно None
    return [transaction for transaction in transactions if
            'state' in transaction and transaction['state'] == status.upper()]

# Основная функция программы
def main():
    print('Привет! Добро пожаловать в программу работы с банковскими транзакциями.')
    print('Выберите необходимый пункт меню:')
    print('1. Получить информацию о транзакциях из json файла')
    print('2. Получить информацию о транзакциях из csv файла')
    print('3. Получить информацию о транзакциях из xlsx файла')

    choice = input('Введите номер пункта меню: ')
    transactions = None

    if choice == '1':
        file_path = '../data/operations.json'
        transactions = read_json_file(file_path)

    elif choice == '2':
        file_path = '../data/transactions.csv'
        transactions = read_csv_data(file_path)

    elif choice == '3':
        file_path = '../data/transactions_excel.xlsx'
        transactions = read_xlsx_data(file_path)

    if transactions is not None:
        valid_statuses = ['EXECUTED', 'CANCELED', 'PENDING']
        print('Введите статус по которому необходимо выполнить фильтрацию.')
        print('Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING')
        status = input().upper()
        filtered_transactions = filter_transactions_by_status(transactions, status)
        print(f'Операции отфильтрованы по статусу "{status}"')
        print(transactions)
    else:
        print('Не удалось загрузить транзакции.')

# Точка входа в программу
if __name__ == '__main__':
    main()
