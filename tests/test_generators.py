from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


# Тесты для функции filter_by_currency
def test_filter_by_currency_with_matching_currency() -> None:
    """Тестирование функции filter_by_currency с совпадающей валютой"""
    transactions = [
        {"operationAmount": {"currency": {"code": "USD"}}},
        {"operationAmount": {"currency": {"code": "EUR"}}},
        {"operationAmount": {"currency": {"code": "USD"}}},
    ]
    currency = "USD"
    filtered_transactions = list(filter_by_currency(transactions, currency))
    assert filtered_transactions == [
        {"operationAmount": {"currency": {"code": "USD"}}},
        {"operationAmount": {"currency": {"code": "USD"}}},
    ]


def test_filter_by_currency_with_non_matching_currency() -> None:
    """Тестирование функции filter_by_currency с несовпадающей валютой"""
    transactions = [
        {"operationAmount": {"currency": {"code": "USD"}}},
        {"operationAmount": {"currency": {"code": "EUR"}}},
        {"operationAmount": {"currency": {"code": "USD"}}},
    ]
    currency = "GBP"
    filtered_transactions = list(filter_by_currency(transactions, currency))
    assert filtered_transactions == []


# Тесты для функции transaction_descriptions
def test_transaction_descriptions_with_descriptions() -> None:
    """Тестирование функции transaction_descriptions с наличием описаний"""
    transactions = [
        {"description": "Покупка в магазине"},
        {"description": "Онлайн платеж"},
        {"description": "Перевод другу"},
    ]
    expected_descriptions = [
        "Покупка в магазине",
        "Онлайн платеж",
        "Перевод другу",
    ]
    actual_descriptions = list(transaction_descriptions(transactions))
    assert actual_descriptions == expected_descriptions


def test_transaction_descriptions_without_descriptions() -> None:
    """Тестирование функции transaction_descriptions без описаний"""
    transactions = [
        {"amount": "100", "currency": "USD"},
        {"amount": "50", "currency": "EUR"},
        {"amount": "200", "currency": "USD"},
    ]
    expected_descriptions = [
        "No description available",
        "No description available",
        "No description available",
    ]
    actual_descriptions = list(transaction_descriptions(transactions))
    assert actual_descriptions == expected_descriptions


# Тесты для функции card_number_generator
def test_card_number_generator_with_valid_range() -> None:
    """Тестирование функции card_number_generator с допустимым диапазоном"""
    start = 1000
    end = 1003
    expected_card_numbers = [
        "0000 0000 0000 1000",
        "0000 0000 0000 1001",
        "0000 0000 0000 1002",
        "0000 0000 0000 1003",
    ]
    actual_card_numbers = list(card_number_generator(start, end))
    assert actual_card_numbers == expected_card_numbers


def test_card_number_generator_with_invalid_range() -> None:
    """Тестирование функции card_number_generator с недопустимым диапазоном"""
    start = 10
    end = 5
    actual_card_numbers = list(card_number_generator(start, end))
    assert actual_card_numbers == []
