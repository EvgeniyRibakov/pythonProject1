from typing import Any, Dict, List

import pytest

from src.processing import get_key_state, sorted_dates


# Фикстура для предоставления тестовых данных
@pytest.fixture
def sample_data() -> List[Dict[str, Any]]:
    return [
        {"id": 86525874, "state": "EXECUTED", "date": "2019-03-30t11:29:12.645712"},
        {"id": 907562709, "state": "EXECUTED", "date": "2017-09-07t04:49:28.697104"},
        {"id": 53791408, "state": "EXECUTED", "date": "2018-12-01t18:36:18.158917"},
        {"id": 159758235, "state": "EXECUTED", "date": "2016-07-14t07:08:04.258796"},
    ]


# Тест функции get_key_state
def test_get_key_state(sample_data: Dict[Any, Any]) -> None:
    result = get_key_state(sample_data, state="EXECUTED")
    for item in result:
        assert item["state"] == "EXECUTED"


# Тест функции sorted_dates
def test_sorted_dates(sample_data: List[Dict[str, Any]]) -> None:
    expected_sorted_data = [
        {"id": 86525874, "state": "EXECUTED", "date": "2019-03-30t11:29:12.645712"},
        {"id": 53791408, "state": "EXECUTED", "date": "2018-12-01t18:36:18.158917"},
        {"id": 907562709, "state": "EXECUTED", "date": "2017-09-07t04:49:28.697104"},
        {"id": 159758235, "state": "EXECUTED", "date": "2016-07-14t07:08:04.258796"},
    ]
    # Сортировка данных и проверка соответствия ожидаемому результату
    result = sorted_dates(sample_data)
    assert result == expected_sorted_data

    # Обратная сортировка данных и проверка соответствия ожидаемому результату
    reversed_sorted_data = [
        {"id": 159758235, "state": "EXECUTED", "date": "2016-07-14t07:08:04.258796"},
        {"id": 907562709, "state": "EXECUTED", "date": "2017-09-07t04:49:28.697104"},
        {"id": 53791408, "state": "EXECUTED", "date": "2018-12-01t18:36:18.158917"},
        {"id": 86525874, "state": "EXECUTED", "date": "2019-03-30t11:29:12.645712"},
    ]
    result_reverse = sorted_dates(sample_data)
    assert result_reverse == reversed_sorted_data
