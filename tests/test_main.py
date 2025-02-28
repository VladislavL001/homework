from unittest.mock import Mock, patch

import pytest
from _pytest.capture import CaptureFixture

from main import main


@pytest.fixture
def data() -> list[dict]:
    return [
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
        {
            "id": 587085106,
            "state": "EXECUTED",
            "date": "2018-03-23T10:45:06.972075",
            "operationAmount": {"amount": "48223.05", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Открытие вклада",
            "to": "Счет 41421565395219882431",
        },
    ]


@pytest.fixture
def data_csv() -> list[dict]:
    return [
        {
            "id": 441945886,
            "state": "EXECUTED",
            "date": "2019-08-26T10:50:58.294041",
            "amount": "31957.58",
            "currency_name": "руб.",
            "currency_code": "RUB",
            "description": "Перевод организации",
            "from": "Maestro 1596837868705199",
            "to": "Счет 64686473678894779589",
        },
        {
            "id": 41428829,
            "state": "EXECUTED",
            "date": "2019-07-03T18:35:29.512364",
            "amount": "8221.37",
            "currency_name": "USD",
            "currency_code": "USD",
            "description": "Перевод организации",
            "from": "MasterCard 7158300734726758",
            "to": "Счет 35383033474447895560",
        },
        {
            "id": 587085106,
            "state": "EXECUTED",
            "date": "2018-03-23T10:45:06.972075",
            "amount": "48223.05",
            "currency_name": "руб.",
            "currency_code": "RUB",
            "description": "Открытие вклада",
            "to": "Счет 41421565395219882431",
        },
    ]


@patch(
    "builtins.input",
    side_effect=[
        "1",  # Выбор JSON-файла
        "EXECUTED",  # Фильтр по статусу
        "да",  # Сортировка по дате
        "по убыванию",
        "нет",  # Фильтр по рублям
        "да",  # Фильтр по слову
        "Перевод",  # Ввод слова для поиска
    ],
)
def test_main_valid_json(data: list[dict], capsys: CaptureFixture) -> None:
    main()
    captured = capsys.readouterr()
    output = captured.out
    assert "26.08.2019 Перевод организации" in output
    assert "Счет **9589 -> Maestro 1596 83** **** 5199" in output
    assert "Сумма: 31957.58 руб." in output


@patch(
    "builtins.input",
    side_effect=[
        "2",  # Выбор CSV-файла
        "EXECUTED",  # Фильтр по статусу
        "да",  # Сортировка по дате
        "по убыванию",
        "нет",  # Фильтр по рублям (чтобы оставить USD)
        "да",  # Фильтр по слову
        "Перевод",  # Ввод слова для поиска
    ],
)
@patch("main.read_csv")
def test_main_valid_csv(
    mock_filter_state: Mock, mock_read_csv: Mock, data_csv: list[dict], capsys: CaptureFixture
) -> None:
    """Тест для CSV-файла с ответами 'да' на все фильтры, кроме фильтра по рублям."""
    mock_read_csv.return_value = data_csv

    mock_filter_state.return_value = data_csv

    main()

    captured = capsys.readouterr()
    output = captured.out

    assert "03.07.2019 Перевод организации" in output
    assert "Счет **5560 -> MasterCard 7158 30** **** 6758" in output
    assert "Сумма: 8221.37 USD" in output


@patch(
    "builtins.input",
    side_effect=[
        "3",  # Выбор CSV-файла
        "EXECUTED",  # Фильтр по статусу
        "да",  # Сортировка по дате
        "по убыванию",
        "нет",  # Фильтр по рублям (чтобы оставить USD)
        "да",  # Фильтр по слову
        "Перевод",  # Ввод слова для поиска
    ],
)
@patch("main.read_excel")
def test_main_valid_excel(
    mock_filter_state: Mock, mock_read_excel: Mock, data_csv: list[dict], capsys: CaptureFixture
) -> None:
    """Тест для CSV-файла с ответами 'да' на все фильтры, кроме фильтра по рублям."""
    mock_read_excel.return_value = data_csv

    mock_filter_state.return_value = data_csv

    main()

    captured = capsys.readouterr()
    output = captured.out

    assert "03.07.2019 Перевод организации" in output
    assert "Счет **5560 -> MasterCard 7158 30** **** 6758" in output
    assert "Сумма: 8221.37 USD" in output
