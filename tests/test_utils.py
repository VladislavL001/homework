import json
import os
from unittest.mock import Mock, mock_open, patch

from src.utils import convert_to_rub, load_transactions_from_json, universal_path_file


def test_universal_path_file_returns_string() -> None:
    """Проверяем, что функция возвращает строку."""
    result = universal_path_file()
    assert isinstance(result, str)


def test_universal_path_file_returns_absolute_path() -> None:
    """Проверяем, что возвращаемый путь является абсолютным."""
    result = universal_path_file()
    assert os.path.isabs(result)


def test_universal_path_file_contains_correct_subpath() -> None:
    """Проверяем, что путь содержит 'data/operations.json'."""
    result = universal_path_file()
    expected_subpath = os.path.join("data", "operations.json")
    assert expected_subpath in result


def test_load_transactions_valid_json() -> None:
    """Тест проверяет работу функции с верными данными"""
    mock_data = json.dumps(
        [
            {
                "id": 441945886,
                "state": "EXECUTED",
                "date": "2019-08-26T10:50:58.294041",
                "operationAmount": {"amount": "31957.58", "currency": {"name": "руб.", "code": "RUB"}},
                "description": "Перевод организации",
                "from": "Maestro 1596837868705199",
                "to": "Счет 64686473678894779589",
            },
            {
                "id": 41428829,
                "state": "EXECUTED",
                "date": "2019-07-03T18:35:29.512364",
                "operationAmount": {"amount": "8221.37", "currency": {"name": "USD", "code": "USD"}},
                "description": "Перевод организации",
                "from": "MasterCard 7158300734726758",
                "to": "Счет 35383033474447895560",
            },
        ]
    )  # JSON строка
    with patch("builtins.open", mock_open(read_data=mock_data)):
        result = load_transactions_from_json("fake_path.json")
    expected_result = json.loads(mock_data)
    assert result == expected_result


def test_load_transactions_empty_json() -> None:
    """Тест проверяется результаты вывода при пустом JSON файле"""
    mock_data = json.dumps([])  # JSON строка
    with patch("builtins.open", mock_open(read_data=mock_data)):
        result = load_transactions_from_json("fake_path.json")
    expected_result: list[None] = []
    assert result == expected_result


def test_load_transactions_file_not_found() -> None:
    """Тест на ошибку к файлу JSON"""
    fake_path = "non_existent_file.json"

    with patch("builtins.open", side_effect=FileNotFoundError):
        result = load_transactions_from_json(fake_path)

    assert result == []


def test_load_transactions_json_decode_error() -> None:
    """Тест на ошибку JSON"""
    fake_path = "fake_file.json"

    with patch("builtins.open", mock_open(read_data="{invalid_json:}")):
        result = load_transactions_from_json(fake_path)

    assert result == []


@patch("src.utils.get_exchange_rate")
def test_convert_to_rub_list(mock_get_exchange_rate: Mock) -> None:
    """Проверка работы работоспособности при передаче в функцию списка словарей"""
    mock_get_exchange_rate.return_value = 0.01  # Курсы USD и EUR к рублю

    data = [
        {"id": 1, "operationAmount": {"amount": "100", "currency": {"code": "USD"}}},
        {"id": 2, "operationAmount": {"amount": "200", "currency": {"code": "EUR"}}},
        {"id": 3, "operationAmount": {"amount": "300", "currency": {"code": "RUB"}}},
    ]

    expected = [{"id": 1, "amount": 10000}, {"id": 2, "amount": 20000}, {"id": 3, "amount": 300.0}]

    result = convert_to_rub(data)
    assert result == expected


@patch("src.utils.get_exchange_rate")
def test_convert_to_rub_dict(mock_get_exchange_rate: Mock) -> None:
    """Проверка работы работоспособности при передаче в функцию словаря"""
    mock_get_exchange_rate.return_value = 0.01  # Курсы USD и EUR к рублю

    data = {"id": 1, "operationAmount": {"amount": "100", "currency": {"code": "USD"}}}
    expected = 10000

    result = convert_to_rub(data)
    assert result == expected


@patch("src.utils.get_exchange_rate")
def test_convert_to_rub_invalid_data(mock_get_exchange_rate: Mock) -> None:
    """Тест на неверный формат данных"""
    mock_get_exchange_rate.return_value = 0.01
    result = convert_to_rub("invalid_data")
    assert result == []


@patch("src.utils.get_exchange_rate")
def test_convert_to_rub_error_get_exchange_rate(mock_get_exchange_rate: Mock) -> None:
    """Тест если не поступил курс валют"""
    mock_get_exchange_rate.return_value = None
    data = {"id": 1, "operationAmount": {"amount": "100", "currency": {"code": "USD"}}}
    result = convert_to_rub(data)
    assert result == []


@patch("src.utils.get_exchange_rate")
def test_convert_to_rub_invalid_transaction(mock_get_exchange_rate: Mock) -> None:
    """Тест если amount имеет некорректный формат"""
    mock_get_exchange_rate.return_value = 0.01
    data = [{"id": 1, "operationAmount": {"amount": "abc", "currency": {"code": "USD"}}}]  # Некорректная сумма
    result = convert_to_rub(data)
    assert result == []


@patch("src.utils.get_exchange_rate")
def test_convert_to_rub_missing_key(mock_get_exchange_rate: Mock) -> None:
    """Тест если отсутствует ключ amount"""
    mock_get_exchange_rate.return_value = 0.01
    data = [{"id": 1}]
    result = convert_to_rub(data)
    assert result == []
