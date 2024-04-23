import pytest

from src.widget import convert_date_string, mask_checcking


@pytest.mark.parametrize(
    "input_date, expected_output",
    [
        ("2018-07-11T02:26:18.671407", "11.07.2018"),
        ("2018-04-16T02:26:18.671407", "16.04.2018"),
        ("2015-08-29T02:26:18.671407", "29.08.2015"),
    ],
)
def test_convert_date_string(input_date: str, expected_output: str) -> None:
    assert convert_date_string(input_date) == expected_output


def test_mask_checcking() -> None:
    assert mask_checcking("Счет 73654108430135874305") == "Счет **4305"
    assert mask_checcking("Visa Classic 6831982476737658") == "Visa Classic 6831 98** **** 7658"
