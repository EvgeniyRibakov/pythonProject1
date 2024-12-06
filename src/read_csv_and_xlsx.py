import csv
from typing import Any, Dict, List

import pandas as pd

# from src.logger import logger


def read_csv_data(file_path: str) -> List[Dict[str, Any]]:
    """
    Read data from a CSV file.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries with data from the file. Each row is a dictionary.
    """
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
    """
    Read data from an XLSX file.

    Args:
        file_path (str): Path to the XLSX file.

    Returns:
        List[Dict]: A list of dictionaries with data from the file. Each row is a dictionary. If the file is not found, it returns an empty list.
    """
    try:
        data_frame = pd.read_excel(file_path)
        return data_frame.to_dict("records")
    except FileNotFoundError:
        print("Файл не найден.")
        return []
