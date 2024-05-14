import unittest
from unittest.mock import patch

from src.utils import convert_currency, get_currency_rate


class TestCurrencyUtils(unittest.TestCase):

    @patch("src.utils.requests.get")
    def test_get_currency_rate(self, mock_get: unittest.mock.MagicMock) -> None:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"rates": {"USD": 1.0, "EUR": 0.9}}

        self.assertEqual(get_currency_rate("USD", "test_api_key"), 1.0)
        self.assertEqual(get_currency_rate("EUR", "test_api_key"), 0.9)

        mock_get.return_value.status_code = 404
        self.assertIsNone(get_currency_rate("USD", "test_api_key"))

    def test_convert_currency(self) -> None:
        transaction = {"amount": 100, "currency_code": "USD"}
        rate = 75.0
        self.assertEqual(convert_currency(transaction, rate), 7500.0)


if __name__ == "__main__":
    unittest.main()
