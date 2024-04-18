from src.processing import get_key_state, sorted_dates
import pytest


@pytest.fixture
def sample_data():
    return [
        {"id": 86525874, "state": "EXECUTED", "date": "2019-03-30t11:29:12.645712"},
        {"id": 907562709, "state": "EXECUTED", "date": "2017-09-07t04:49:28.697104"},
        {"id": 53791408, "state": "EXECUTED", "date": "2018-12-01t18:36:18.158917"},
        {"id": 159758235, "state": "EXECUTED", "date": "2016-07-14t07:08:04.258796"}
    ]


def test_get_key_state(sample_data):
    result = get_key_state(sample_data, state="EXECUTED")
    for item in result:
        assert item["state"] == "EXECUTED"


def test_sorted_dates(sample_data):
    expected_sorted_data = [
        {"id": 86525874, "state": "EXECUTED", "date": "2019-03-30t11:29:12.645712"},
        {"id": 53791408, "state": "EXECUTED", "date": "2018-12-01t18:36:18.158917"},
        {"id": 907562709, "state": "EXECUTED", "date": "2017-09-07t04:49:28.697104"},
        {"id": 159758235, "state": "EXECUTED", "date": "2016-07-14t07:08:04.258796"}
    ]
    result = sorted_dates(sample_data, True)
    assert result == expected_sorted_data

    reversed_sorted_data = [
        {"id": 159758235, "state": "EXECUTED", "date": "2016-07-14t07:08:04.258796"},
        {"id": 907562709, "state": "EXECUTED", "date": "2017-09-07t04:49:28.697104"},
        {"id": 53791408, "state": "EXECUTED", "date": "2018-12-01t18:36:18.158917"},
        {"id": 86525874, "state": "EXECUTED", "date": "2019-03-30t11:29:12.645712"}
    ]
    result_reverse = sorted_dates(sample_data)
    assert result_reverse == reversed_sorted_data
