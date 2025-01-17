import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "account_card, example",
    [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Счет 73654108430135874305", "Счет **4305"),
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("Счет 64686473678894779589", "Счет **9589"),
        ("MasterCard     7158300734726758", "MasterCard 7158 30** **** 6758"),
    ],
)
def test_mask_account_card(account_card: str, example: str) -> None:
    assert mask_account_card(account_card) == example


@pytest.mark.parametrize(
    "account_card",
    [
        (""),
        ("..."),
        ("Visa Platinum"),
    ],
)
def test_mask_account_card_error_input(account_card: str) -> None:
    assert mask_account_card(account_card) == "Неправильно введен номер или счет карты"


@pytest.mark.parametrize(
    "data, example",
    [("2024-03-11T02:26:18.671407", "11.03.2024"), ("", "Неверный формат даты"), ("5f454dfe", "Неверный формат даты")],
)
def test_get_data(data: str, example: str) -> None:
    assert get_date(data) == example
