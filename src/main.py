import json
import csv
import pandas as pd


def load_json_transactions(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Файл не найден: {file_path}")
        return None  # Добавлено возвращение None в случае ошибки
    except json.JSONDecodeError:
        print(f"Ошибка декодирования JSON в файле: {file_path}")
        return None  # Добавлено возвращение None в случае ошибки


def load_csv_transactions(file_path):
    transactions = []
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                if all(key in row for key in
                       ['id', 'state', 'date', 'amount', 'currency_name', 'currency_code', 'from', 'to',
                        'description']):
                    transaction = {
                        'id': row['id'],
                        'state': row['state'].upper(),
                        'date': row['date'],
                        'amount': row['amount'],
                        'currency_name': row['currency_name'],
                        'currency_code': row['currency_code'],
                        'from': row['from'],
                        'to': row['to'],
                        'description': row['description']
                    }
                    transactions.append(transaction)
                else:
                    print(f"Ошибка: в строке отсутствует один из необходимых ключей.")
        return transactions
    except FileNotFoundError:
        print(f"Файл не найден: {file_path}")
        return None  # Добавлено возвращение None в случае ошибки


def load_xlsx_transactions(file_path):
    try:
        df = pd.read_excel(file_path)
        transactions = df.to_dict('records')
        for transaction in transactions:
            if isinstance(transaction['state'], str):
                transaction['state'] = transaction['state'].upper()
            else:
                transaction['state'] = str(transaction['state']).upper()
        return transactions
    except FileNotFoundError:
        print(f"Файл не найден: {file_path}")
        return None  # Добавлено возвращение None в случае ошибки


# Функция для фильтрации транзакций по статусу
def filter_transactions_by_status(transactions, status):
    # Фильтрация транзакций с проверкой наличия ключа 'state'
    if transactions is None:
        return []  # Возвращаем пустой список, если transactions равно None
    return [transaction for transaction in transactions if
            'state' in transaction and transaction['state'] == status.upper()]


def display_transactions(transactions):
    # Вывод информации о транзакциях
    for transaction in transactions:
        # Проверка наличия ключа 'operationAmount' и вложенного ключа 'amount' перед их использованием
        if 'operationAmount' in transaction and 'amount' in transaction['operationAmount']:
            amount = transaction['operationAmount']['amount']
            print(
                f"ID: {transaction['id']}, Дата: {transaction['date']}, Сумма: {amount}, Статус: {transaction['state']}")
        else:
            print(f"Ошибка: в транзакции с ID {transaction['id']} отсутствует информация о сумме.")


# Функция для сортировки транзакций по дате
def sort_transactions(transactions, order):
    return sorted(transactions, key=lambda x: x['date'], reverse=(order == 'по убыванию'))


def filter_rub_transactions(transactions):
    filtered_transactions = []
    for transaction in transactions:
        # Проверяем, существует ли ключ 'operationAmount' и его вложенный ключ 'currency'
        if 'operationAmount' in transaction and 'currency' in transaction['operationAmount']:
            if transaction['operationAmount']['currency']['code'] == 'RUB':
                filtered_transactions.append(transaction)
    return filtered_transactions


# Функция для фильтрации транзакций по ключевому слову в описании
def filter_by_keyword(transactions, keyword):
    return [transaction for transaction in transactions if keyword.lower() in transaction['description'].lower()]


# Функция для получения корректного статуса
def get_valid_status(valid_statuses):
    while True:
        status = input('Статус: ').upper()
        if status in valid_statuses:
            return status
        else:
            print(f'Статус операции "{status}" недоступен.')
            print('Введите статус по которому необходимо выполнить фильтрацию.')
            print('Доступные для фильтровки статусы: ' + ', '.join(valid_statuses))


# Функция для определения формата файла и его чтения
def read_file(file_path):
    if file_path.endswith('.json'):
        return load_json_transactions(file_path)
    elif file_path.endswith('.csv'):
        return load_csv_transactions(file_path)
    elif file_path.endswith('.xlsx'):
        return load_xlsx_transactions(file_path)
    else:
        print('Неподдерживаемый формат файла')
        return None


# Основная функция программы
def main():
    print('Привет! Добро пожаловать в программу работы с банковскими транзакциями.')
    print('Выберите необходимый пункт меню:')
    print('1. Получить информацию о транзакциях из json файла')
    print('2. Получить информацию о транзакциях из csv файла')
    print('3. Получить информацию о транзакциях из xlsx файла')

    choice = input('Введите номер пункта меню: ')

    if choice == '1':
        file_path = '../data/operations.json'
        transactions = read_file(file_path)

    elif choice == '2':
        file_path = '../data/transactions.csv'  # Указываем путь к файлу
        transactions = read_file(file_path)

    elif choice == '3':
        file_path = '../data/transactions_excel.xlsx'  # Указываем путь к файлу
        transactions = read_file(file_path)

    valid_statuses = ['EXECUTED', 'CANCELED', 'PENDING']
    print('Введите статус по которому необходимо выполнить фильтрацию.')
    status = get_valid_status(valid_statuses)

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


# Точка входа в программу
if __name__ == '__main__':
    main()
