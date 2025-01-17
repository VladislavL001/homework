import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.fixture
def number_card_example() -> str:
    return "7000792289606361"


def test_get_mask_card_number(number_card_example: str) -> None:
    assert get_mask_card_number(number_card_example) == "7000 79** **** 6361"


@pytest.fixture
def error_number_card() -> str:
    return "Неверно введен номер карты"


@pytest.mark.parametrize(
    "number_card",
    [("7000792289606361454"), ("3700079228960"), ("sdsdwew"), ("баоваав"), (" , "), ("................"), ("")],
)
def test_get_mask_card_number_error_number(number_card: str, error_number_card: str) -> None:
    assert get_mask_card_number(number_card) == error_number_card


@pytest.fixture
def account_number_example() -> str:
    return "73654108430135874305"


def test_get_mask_account(account_number_example: str) -> None:
    assert get_mask_account(account_number_example) == "**4305"


@pytest.fixture
def error_account_number() -> str:
    return "Неверно введен номер счета"


@pytest.mark.parametrize(
    "account_number",
    [(7365410843013587430555), (73654108430135874), ("sdsdwew"), ("баоваав"), (" , "), ("...................."), ("")],
)
def test_get_mask_account_error_number(account_number: str, error_account_number: str) -> None:
    assert get_mask_account(account_number) == error_account_number
