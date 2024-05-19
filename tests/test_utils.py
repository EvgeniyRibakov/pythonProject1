import unittest
from typing import Any, List, Dict
from unittest.mock import mock_open, patch

from src.utils import convert_currency, get_currency_rate, read_json_file


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

    @patch("requests.get")
    def test_get_currency_rate_success(self, mock_get: Any) -> None:
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {"rates": {"RUB": 75.0}}
        currency_code = "RUB"
        api_key = "test_api_key"
        result = get_currency_rate(currency_code, api_key)
        self.assertEqual(result, 75.0)

    @patch("requests.get")
    def test_get_currency_rate_failure(self, mock_get: Any) -> None:
        mock_response = mock_get.return_value
        mock_response.status_code = 400
        currency_code = "RUB"
        api_key = "test_api_key"
        result = get_currency_rate(currency_code, api_key)
        self.assertIsNone(result)

    @patch("src.utils.get_currency_rate")
    def test_convert_currency_rub(self, mock_get_rate: Any) -> None:
        mock_get_rate.return_value = 75.0
        transaction = {"amount": 1500, "currency": "RUB"}
        api_key = "test_api_key"
        result = convert_currency(transaction, api_key)
        self.assertEqual(result, 1500.0)

    @patch("src.utils.get_currency_rate")
    def test_convert_currency_usd(self, mock_get_rate: Any) -> None:
        mock_get_rate.side_effect = [1.0, 75.0]
        transaction = {"amount": 100, "currency": "USD"}
        api_key = "test_api_key"
        result = convert_currency(transaction, api_key)
        self.assertEqual(result, 7500.0)

    @patch("src.utils.get_currency_rate")
    def test_convert_currency_eur(self, mock_get_rate: Any) -> None:
        mock_get_rate.side_effect = [1.1, 75.0]
        transaction = {"amount": 50, "currency": "EUR"}
        api_key = "test_api_key"
        result = convert_currency(transaction, api_key)
        self.assertEqual(result, 4125.0)

    @patch("src.utils.get_currency_rate")
    def test_convert_currency_none_amount(self, mock_get_rate: Any) -> None:
        transaction = {"amount": None, "currency": "USD"}
        api_key = "test_api_key"
        result = convert_currency(transaction, api_key)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
