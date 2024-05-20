import unittest
from typing import Any, Dict, List
from unittest.mock import Mock, mock_open, patch

from src.utils import convert_currency, read_json_file, transaction_amount_in_rub


class TestReadJsonFile(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data="[]")
    def test_read_empty_json(self, mock_file: Any) -> None:
        data = read_json_file("dummy/path")
        self.assertEqual(data, [])

    @patch("builtins.open", new_callable=mock_open, read_data='{"key": "value"}')
    def test_read_non_list_json(self, mock_file: Any) -> None:
        data = read_json_file("dummy/path")
        self.assertEqual(data, [])

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_read_nonexistent_file(self, mock_open: Any) -> None:
        data = read_json_file("nonexistent/path")
        self.assertEqual(data, [])

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data='[{"id": 441945886, "state": "EXECUTED", "date": "2019-08-26T10:50:58.294041", "operationAmount": {'
        '"amount": "31957.58", "currency": {"name": "руб.", "code": "RUB"}}}]',
    )
    def test_read_valid_json(self, mock_file: Any) -> None:
        expected_data: List[Dict[str, str]] = []
        data = read_json_file("dummy/path")
        self.assertEqual(data, expected_data)

    @patch("src.utils.requests.get")
    def test_convert_currency(self, mock_get: Any) -> None:
        # Подготовка мок объекта response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"rates": {"RUB": 70.0}}  # Мок данные от API
        mock_get.return_value = mock_response

        # Вызов функции и проверка результата
        converted_amount = convert_currency(100, "USD")
        self.assertEqual(converted_amount, 7000)

    def test_transaction_amount_in_rub(self: Any) -> None:
        # Подготовка данных для транзакции
        transaction_data = {"operationAmount": {"amount": 100, "currency": {"code": "USD"}}}

        # Вызов функции и проверка результата
        with patch("src.utils.convert_currency") as mock_convert_currency:
            mock_convert_currency.return_value = 7000  # Мокирование результата конвертации
            result = transaction_amount_in_rub(transaction_data)
            self.assertEqual(result, 7000)


if __name__ == "__main__":
    unittest.main()
