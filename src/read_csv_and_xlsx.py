import pandas as pd


# Функция для считывания данных из CSV файла и преобразования их в список словарей
def read_csv_data(file_path: str) -> list:
    try:
        data_frame = pd.read_csv(file_path)
        return data_frame.to_dict("records")
    except FileNotFoundError:
        print("Файл не найден.")
        return []


# Функция для считывания данных из XLSX файла и преобразования их в список словарей
def read_xlsx_data(file_path: str) -> list:
    try:
        data_frame = pd.read_excel(file_path)
        return data_frame.to_dict("records")
    except FileNotFoundError:
        print("Файл не найден.")
        return []


# Пример использования функций
print(read_csv_data("../data/transactions.csv"))
print(read_xlsx_data("../data/transactions_excel.xlsx"))
