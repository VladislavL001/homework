from typing import Any, Iterator


def filter_by_currency(transactions_def: Any, currency_code: str = "USD") -> Iterator:
    return (
        transaction_def
        for transaction_def in transactions_def
        if transaction_def["operationAmount"]["currency"]["code"] == currency_code
    )


def transaction_descriptions(transactions_def: Any) -> Iterator:
    for transaction_def in transactions_def:
        yield transaction_def["description"]


def card_number_generator():
    pass


all_transactions = [
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


currency = filter_by_currency(all_transactions, "USD")
for _ in range(2):
    check_error = next(currency, "Транзакции не найдены")
    print(check_error)
    if check_error == "Транзакции не найдены":
        break


descriptions = transaction_descriptions(all_transactions)
for _ in range(3):
    print(next(descriptions))
