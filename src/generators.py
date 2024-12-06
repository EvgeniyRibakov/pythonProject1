from typing import Dict, Generator, List

transactions = [
    {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702",
    },
    {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод со счета на счет",
        "from": "Счет 19708645243227258542",
        "to": "Счет 75651667383060284188",
    },
    {
        "id": 873106923,
        "state": "EXECUTED",
        "date": "2019-03-23T01:09:46.296404",
        "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Перевод со счета на счет",
        "from": "Счет 44812258784861134719",
        "to": "Счет 74489636417521191160",
    },
    {
        "id": 895315941,
        "state": "EXECUTED",
        "date": "2018-08-19T04:27:37.904916",
        "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод с карты на карту",
        "from": "Visa Classic 6831982476737658",
        "to": "Visa Platinum 8990922113665229",
    },
    {
        "id": 594226727,
        "state": "CANCELED",
        "date": "2018-09-12T21:27:25.241689",
        "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Перевод организации",
        "from": "Visa Platinum 1246377376343588",
        "to": "Счет 14211924144426031657",
    },
]


def filter_by_currency(data: List[Dict], currency_code: str, file_type: str) -> List[Dict]:
    """Filters transactions by currency code."""
    # Check if the file type is JSON
    if file_type == "json":
        # Return transactions where currency code matches
        return [
            transaction
            for transaction in data
            if transaction.get("operationAmount", {}).get("currency", {}).get("code") == currency_code
        ]
    else:
        # Return transactions where currency code matches for other file types
        return [transaction for transaction in data if transaction.get("currency_code") == currency_code]


def transaction_descriptions(data: List[Dict]) -> Generator[str, None, None]:
    """Generator that yields transaction descriptions."""
    # Loop through each transaction in data
    for transaction in data:
        # Yield the description of the transaction or an empty string
        yield transaction.get("description", "")


def card_number_generator(start: int, end: int) -> Generator[str, None, None]:
    """Generates card numbers from start to end."""
    # Loop from start to end
    for i in range(start, end + 1):
        # Yield formatted card number
        yield f"0000 0000 0000 {i:04d}"
