import unittest
from unittest.mock import patch, mock_open, Mock
from src.read_csv_and_xlsx import reading_csv_file, reading_xlsx_file
from pandas import DataFrame
import pandas as pd
from typing import Any

mock_csv_data = 'id,state,date,amount,currency_name,currency_code,from,to,description\n' \
                '650703,EXECUTED,2023-09-05T11:30:32Z,16210,Sol,PEN,Счет 58803664561298323391,Счет ...'


class TestReadFiles(unittest.TestCase):
    """Тесты для функций чтения CSV и XLSX файлов."""

    def setUp(self) -> None:
        # Создаем мок данных для XLSX файла
        self.mock_xlsx_data = pd.DataFrame({
            'id': [650703],
            'state': ['EXECUTED'],
            'date': ['2023-09-05T11:30:32Z'],
            'amount': [16210],
            'currency_name': ['Sol'],
            'currency_code': ['PEN'],
            'from': ['Счет 58803664561298323391'],
            'to': ['Счет ...'],
            'description': ['...']
        })

    @patch('pandas.read_csv')
    @patch('builtins.open', new_callable=mock_open, read_data=mock_csv_data)
    def test_reading_csv_file_found(self, mock_file: Any, mock_read_csv: Any) -> None:
        """Проверяет, что функция reading_csv_file() возвращает DataFrame при наличии файла."""
        mock_read_csv.return_value = DataFrame({
            'id': [1],
            'state': ['EXECUTED'],
            'date': ['2023-09-05T11:30:32Z'],
            'amount': [16210],
            'currency_name': ['Sol'],
            'currency_code': ['PEN'],
            'from': ['Счет 58803664561298323391'],
            'to': ['Счет ...'],
            'description': ['...']
        })
        actual_df = reading_csv_file('tests/transactions.csv')
        self.assertIsInstance(actual_df, DataFrame)

    @patch('src.read_csv_and_xlsx.pd.read_excel')
    def test_reading_xlsx_file_found(self, mock_read_excel: Mock) -> None:
        """Проверяет, что функция reading_xlsx_file() возвращает DataFrame при наличии файла."""
        mock_read_excel.return_value = self.mock_xlsx_data
        expected_df_type = type(DataFrame())
        actual_df = reading_xlsx_file('tests/transactions.xlsx')
        self.assertIsInstance(actual_df, expected_df_type)


if __name__ == '__main__':
    unittest.main()
