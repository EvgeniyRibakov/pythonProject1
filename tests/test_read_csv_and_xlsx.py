import unittest
from unittest.mock import MagicMock, mock_open, patch

import pandas as pd

from src.read_csv_and_xlsx import read_csv_data, read_xlsx_data  # Замените на имя вашего модуля


class TestFileReadingFunctions(unittest.TestCase):
    def setUp(self) -> None:
        self.csv_data = [{"name": "Alice", "amount": 100}, {"name": "Bob", "amount": 200}]
        self.xlsx_data = [{"name": "Charlie", "amount": 300}, {"name": "David", "amount": 400}]

    @patch("pandas.read_csv")
    def test_read_csv_data(self, mock_read_csv: MagicMock) -> None:
        mock_read_csv.return_value = pd.DataFrame(self.csv_data)
        result = read_csv_data("fake_path.csv")
        self.assertEqual(result, self.csv_data)

    @patch("pandas.read_excel")
    def test_read_xlsx_data(self, mock_read_excel: MagicMock) -> None:
        mock_read_excel.return_value = pd.DataFrame(self.xlsx_data)
        result = read_xlsx_data("fake_path.xlsx")
        self.assertEqual(result, self.xlsx_data)

    @patch("builtins.open", new_callable=mock_open, read_data="data")
    @patch("pandas.read_csv")
    def test_read_csv_file_not_found(self, mock_read_csv: MagicMock, mock_file: MagicMock) -> None:
        mock_read_csv.side_effect = FileNotFoundError
        result = read_csv_data("nonexistent.csv")
        self.assertEqual(result, [])

    @patch("builtins.open", new_callable=mock_open, read_data="data")
    @patch("pandas.read_excel")
    def test_read_xlsx_file_not_found(self, mock_read_excel: MagicMock, mock_file: MagicMock) -> None:
        mock_read_excel.side_effect = FileNotFoundError
        result = read_xlsx_data("nonexistent.xlsx")
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
