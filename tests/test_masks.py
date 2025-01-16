import pytest
from src.masks import get_mask_account, get_mask_card_number

@pytest.fixture
def number_card_example():
    return "7000792289606361"

def test_get_mask_card_number(number_card_example):
    assert get_mask_card_number(number_card_example) == "7000 79** **** 6361"


@pytest.fixture
def error_number_card():
    return "Неверно введен номер карты"

@pytest.mark.parametrize ("number_card",
                          [(7000792289606361454),
                           (3700079228960),
                           ("sdsdwew"),
                           ("баоваав"),
                           (" , "),
                           ("................"),
                           ("")])
def test_get_mask_card_number_error_number(number_card, error_number_card):
    assert get_mask_card_number (number_card) == error_number_card


