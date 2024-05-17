import unittest
from unittest.mock import mock_open, patch
from src.utils import convert_currency, get_currency_rate, read_json_file
from typing import Any


class TestYourModule(unittest.TestCase):

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data='[{"amount": 100, "currency": "USD"}, {"amount": 50, "currency": "EUR"}]',
    )
    def test_read_json_file_success(self, mock_file: Any) -> None:
        file_path = "test.json"
        currency = "RUB"
        result = read_json_file(file_path, currency)
        mock_file.assert_called_once_with("test.json", "r", encoding="utf-8")
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

    @patch("builtins.open", new_callable=mock_open, read_data="{}")
    def test_read_json_file_empty(self, mock_file: Any) -> None:
        file_path = "test.json"
        currency = "RUB"
        result = read_json_file(file_path, currency)
        self.assertEqual(result, [])

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_read_json_file_not_found(self, mock_file: Any) -> None:
        file_path = "non_existent_file.json"
        currency = "RUB"
        result = read_json_file(file_path, currency)
        self.assertEqual(result, [])

    @patch("builtins.open", new_callable=mock_open, read_data="invalid json")
    def test_read_json_file_invalid_json(self, mock_file: Any) -> None:
        file_path = "test.json"
        currency = "RUB"
        result = read_json_file(file_path, currency)
        self.assertEqual(result, [])

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
