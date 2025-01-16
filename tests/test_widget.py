import pytest
from src.widget import mask_account_card, get_date

@pytest.mark.parametrize("account_card, example",[("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
                                                  ("Счет 73654108430135874305", "Счет **4305"),
                                                  ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
                                                  ("Счет 64686473678894779589", "Счет **9589"),
                                                  ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758")
                                                  ])
def test_mask_account_card (account_card, example):
    assert mask_account_card(account_card) == example

def test_mask_account_card_error_input():
    pass