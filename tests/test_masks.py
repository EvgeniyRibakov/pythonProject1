from src.masks import mask_bills, mask_cards


def test_mask_cards():
    assert mask_cards('1596837868705199') == '1596 83** **** 5199'


def test_mask_bills():
    assert mask_bills('64686473678894779589') == '**9589'
