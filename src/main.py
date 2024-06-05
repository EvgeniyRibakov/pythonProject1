import json
import csv
import pandas as pd


def load_json_transactions(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Файл не найден: {file_path}")
    except json.JSONDecodeError:
        print(f"Ошибка декодирования JSON в файле: {file_path}")


def load_csv_transactions(file_path):
    transactions = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Преобразование строки в словарь с соответствующими ключами
            transaction = {
                'id': row['id'],
                'state': row['state'],
                'date': row['date'],
                'amount': row['amount'],
                'currency_name': row['currency_name'],
                'currency_code': row['currency_code'],
                'from': row['from'],
                'to': row['to'],
                'description': row['description']
            }
            transactions.append(transaction)
    return transactions


def load_xlsx_transactions():
    file_path = "../data/transactions_excel.xlsx"
    df = pd.read_excel(file_path)
    transactions = df.to_dict('records')
    return transactions


def filter_transactions_by_status(transactions, status):
    # Фильтрация транзакций с проверкой наличия ключа 'status'
    if transactions is None:
        return []  # Возвращаем пустой список, если transactions равно None
    return [transaction for transaction in transactions if
            'status' in transaction and transaction['status'].upper() == status.upper()]


def display_transactions(transactions):
    # Вывод информации о транзакциях
    for transaction in transactions:
        print(f"Дата: {transaction['date']}, Сумма: {transaction['amount']}, Статус: {transaction['status']}")


def sort_transactions(transactions, order):
    # Сортировка транзакций по дате
    return sorted(transactions, key=lambda x: x['date'], reverse=(order == 'по убыванию'))


def filter_rub_transactions(transactions):
    # Фильтрация транзакций по валюте (рубли)
    return [transaction for transaction in transactions if transaction['currency'] == 'RUB']


def filter_by_keyword(transactions, keyword):
    # Фильтрация транзакций по ключевому слову в описании
    return [transaction for transaction in transactions if keyword.lower() in transaction['description'].lower()]


def get_valid_status():
    valid_statuses = ['EXECUTED', 'CANCELED', 'PENDING']
    while True:
        status = input('Статус: ').upper()
        if status in valid_statuses:
            return status
        else:
            print(f'Статус операции "{status}" недоступен.')
            print('Введите статус по которому необходимо выполнить фильтрацию.')
            print('Доступные для фильтровки статусы: ' + ', '.join(valid_statuses))


def main():
    print('Привет! Добро пожаловать в программу работы с банковскими транзакциями.')
    print('Выберите необходимый пункт меню:')
    print('1. Получить информацию о транзакциях из json файла')
    print('2. Получить информацию о транзакциях из csv файла')
    print('3. Получить информацию о транзакциях из xlsx файла')

    choice = input('Введите номер пункта меню: ')

    if choice == '1':
        file_path = '../data/operations.json'
        transactions = load_json_transactions(file_path)

    elif choice == '2':
        file_path = '../data/transactions.csv'  # Указываем путь к файлу
        transactions = load_csv_transactions(file_path)

    elif choice == '3':
        file_path = '../data/transactions_excel.xlsx'  # Указываем путь к файлу
        transactions = load_xlsx_transactions()

    print('Введите статус по которому необходимо выполнить фильтрацию.')
    print('Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING')
    status = get_valid_status()

    filtered_transactions = filter_transactions_by_status(transactions, status)
    print(f'Операции отфильтрованы по статусу "{status}"')

    # Запрос о сортировке
    if input('Отсортировать операции по дате? Да/Нет: ').lower() == 'да':
        order = input('Отсортировать по возрастанию или по убыванию? ').lower()
        filtered_transactions = sort_transactions(filtered_transactions, order)

    # Фильтрация по валюте
    if input('Выводить только рублевые тразакции? Да/Нет: ').lower() == 'да':
        filtered_transactions = filter_rub_transactions(filtered_transactions)

    # Фильтрация по слову в описании
    if input('Отфильтровать список транзакций по определенному слову в описании? Да/Нет: ').lower() == 'да':
        keyword = input('Введите слово для поиска в описании: ')
        filtered_transactions = filter_by_keyword(filtered_transactions, keyword)

    # Вывод итогового списка транзакций
    if filtered_transactions:
        print('Распечатываю итоговый список транзакций...')
        display_transactions(filtered_transactions)
        print(f'Всего банковских операций в выборке: {len(filtered_transactions)}')
    else:
        print('Не найдено ни одной транзакции подходящей под ваши условия фильтрации')


if __name__ == '__main__':
    main()
