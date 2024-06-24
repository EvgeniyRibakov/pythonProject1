import csv
from typing import Any, Dict, List

import pandas as pd

# from src.logger import logger


def read_csv_data(file_path: str) -> List[Dict[str, Any]]:
    data = []
    try:
        with open(file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        print("Файл не найден.")
    return data


def read_xlsx_data(file_path: str) -> List[Dict]:
    """Чтение данных из xlsx файла"""
    try:
        data_frame = pd.read_excel(file_path)
        return data_frame.to_dict("records")
    except FileNotFoundError:
        print("Файл не найден.")
        return []
