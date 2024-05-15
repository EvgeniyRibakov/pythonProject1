import unittest
from unittest.mock import Mock, patch

from src.utils import convert_currency, get_currency_rate


class TestCurrencyConversion(unittest.TestCase):
    @patch("src.utils.requests.get")
    def test_get_currency_rate(self, mock_get: Mock) -> None:
        # Создаем фиктивный ответ, который будет возвращен методом requests.get
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"rates": {"RUB": 75.0}}
        mock_get.return_value = mock_response

        # Вызываем функцию, используя фиктивные данные
        rate = get_currency_rate("USD", "RUB", "fake_api_key")
        if rate is not None:
            self.assertEqual(rate, 75.0)  # type: ignore

    @patch("src.utils.get_currency_rate")
    def test_convert_currency(self, mock_get_rate: Mock) -> None:
        # Создаем фиктивное значение курса, которое будет возвращено функцией get_currency_rate
        mock_get_rate.return_value = 75.0

        # Вызываем функцию конвертации с фиктивным курсом
        transaction = {"amount": 100, "currency": "USD"}
        result = convert_currency(transaction, "fake_api_key")
        if result is not None:
            self.assertEqual(result, 7500.0)  # type: ignore


if __name__ == "__main__":
    unittest.main()
