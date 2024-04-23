from src.generators import filter_by_currency, transaction_descriptions, card_number_generator


def test_matching_currency():
    '''Тестирование случая, когда есть транзакции с указанной валютой'''
    transactions = [
        {"amount": "100", "currency": "USD"},
        {"amount": "50", "currency": "EUR"},
        {"amount": "200", "currency": "USD"}
    ]
    currency = "USD"
    filtered_transactions = list(filter_by_currency(transactions, currency))
    assert filtered_transactions == [
        {"amount": "100", "currency": "USD"},
        {"amount": "200", "currency": "USD"}
    ]


def test_transaction_descriptions():
    '''Тестирование генератора для списка транзакций с описаниями'''
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

    def test_card_number_generator():
        '''Тестирование генератора номеров карт'''
        start = 1000
        end = 1003
        expected_card_numbers = [
            "0000 0000 0000 1000",
            "0000 0000 0000 1001",
            "0000 0000 0000 1002",
            "0000 0000 0000 1003"
        ]

        actual_card_numbers = list(card_number_generator(start, end))
        assert actual_card_numbers == expected_card_numbers
