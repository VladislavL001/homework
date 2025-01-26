import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


@pytest.fixture
def all_transactions() -> list:
    """Все транзакции"""
    return [
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
            "id": 728394012,
            "state": "EXECUTED",
            "date": "2021-11-25T08:30:15.987654",
            "operationAmount": {"amount": "4200.00", "currency": {"name": "GBP", "code": "GBP"}},
            "description": "Перевод заработной платы",
            "from": "Счет 44455566677788899900",
            "to": "Счет 11122233344455566677",
        },
    ]


@pytest.fixture
def usd_transactions() -> list:
    """Транзакции в USD"""
    return [
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
    ]


def test_filter_by_currency_valid(all_transactions: dict, usd_transactions: list) -> None:
    """Тест для проверки фильтрации транзакций по USD"""
    result = list(filter_by_currency(all_transactions, "USD"))
    assert len(result) == 2
    for i in result:
        assert i["operationAmount"]["currency"]["code"] == "USD"


def test_filter_by_currency_no_match(all_transactions: dict) -> None:
    """Тест для проверки обработки случая, если транзакций с заданной валютой нет"""
    result = filter_by_currency(all_transactions, "RUB")
    for _ in range(2):
        assert next(result, "Транзакции не найдены") == "Транзакции не найдены"  # Cтандартный параметр функции next
        # при вызове генератора


def test_filter_by_currency_empty_list() -> None:
    """Тест для проверки обработки пустого списка транзакций"""
    result = list(filter_by_currency([], "USD"))
    assert result == []


@pytest.mark.parametrize("example", [["Перевод организации", "Перевод со счета на счет", "Перевод заработной платы"]])
def test_transaction_descriptions_valid(all_transactions: list, example: list) -> None:
    """Тест на проверку фильтрации"""
    result = list(transaction_descriptions(all_transactions))
    assert result == example


def test_transaction_descriptions_empty_list() -> None:
    """Тест для проверки обработки пустого списка транзакций"""
    result = list(transaction_descriptions([]))
    assert result == []


@pytest.mark.parametrize(
    "start, end, expected",
    [
        (1, 3, ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"]),
    ],
)
def test_card_number_generator_valid(start: int, end: int, expected: list[str]) -> None:
    """Тест для проверки генератора на вывод верных значений"""
    result = list(card_number_generator(start, end))
    assert result == expected


def test_card_number_generator_valid_max_number() -> None:
    """Тест крайних значений"""
    result = list(card_number_generator(-1, 5))
    assert result == []
    result = list(card_number_generator(1, 10000000000000000))
    assert result == []
