import pandas as pd
from typing import Optional

from pandas import DataFrame


def reading_csv_file(file_path: str) -> Optional[DataFrame]:
    """Читает файл с операциями .csv и возвращает DataFrame."""
    try:
        df = pd.read_csv(file_path, delimiter=';')
        return df
    except FileNotFoundError:
        print(f"Файл не найден: {file_path}")
        return None
    except pd.errors.EmptyDataError:
        print(f"Файл пуст: {file_path}")
        return None
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return None


def reading_xlsx_file(file_path: str) -> Optional[DataFrame]:
    """
    Читает операции из xlsx-файла и обрабатывает исключения.
    """
    try:
        df = pd.read_excel('C:/Users/Acer/PycharmProjects/pythonProject1/transactions_excel.xlsx', engine='openpyxl')
        return df
    except FileNotFoundError:
        print(f"Файл не найден: {'C:/Users/Acer/PycharmProjects/pythonProject1/transactions_excel.xlsx'}")
        return None
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return None
