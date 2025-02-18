from unittest.mock import Mock, patch

import pandas as pd
import pytest

from src.transaction_proc import read_csv, read_excel


# Фикстура для данных CSV и Excel
@pytest.fixture
def mock_data() -> pd.DataFrame:
    """
    Фикстура для тестирования данных CSV.
    """
    return pd.DataFrame(
        {
            "id": [650703, 3598919, 593027, 366176, 5380041],
            "state": ["EXECUTED", "EXECUTED", "CANCELED", "EXECUTED", "CANCELED"],
            "date": [
                "2023-09-05T11:30:32Z",
                "2020-12-06T23:00:58Z",
                "2023-07-22T05:02:01Z",
                "2020-08-02T09:35:18Z",
                "2021-02-01T11:54:58Z",
            ],
            "amount": [16210, 29740, 30368, 29482, 23789],
            "currency_name": ["Sol", "Peso", "Shilling", "Rupiah", "Peso"],
            "currency_code": ["PEN", "COP", "TZS", "IDR", "UYU"],
            "from": [
                "Счет 58803664561298323391",
                "Discover 3172601889670065",
                "Visa 1959232722494097",
                "Discover 0325955596714937",
                "",
            ],
            "to": [
                "Счет 39745660563456619397",
                "Discover 0720428384694643",
                "Visa 6804119550473710",
                "Visa 3820488829287420",
                "Счет 23294994494356835683",
            ],
            "description": [
                "Перевод организации",
                "Перевод с карты на карту",
                "Перевод с карты на карту",
                "Перевод с карты на карту",
                "Открытие вклада",
            ],
        }
    )


# Тестируем успешное чтение CSV
@patch("src.transaction_proc.os.path.exists", return_value=True)
@patch("src.transaction_proc.pd.read_csv")
def test_read_csv_success(mock_read_csv: Mock, mock_exists: Mock, mock_data: pd.DataFrame) -> None:
    """
    Тестируем успешное чтение CSV-файла.
    Мокируем `pd.read_csv` для возврата тестового DataFrame.
    """
    mock_read_csv.return_value = mock_data

    expected_result = [
        {
            "id": 650703,
            "state": "EXECUTED",
            "date": "2023-09-05T11:30:32Z",
            "amount": 16210,
            "currency_name": "Sol",
            "currency_code": "PEN",
            "from": "Счет 58803664561298323391",
            "to": "Счет 39745660563456619397",
            "description": "Перевод организации",
        },
        {
            "id": 3598919,
            "state": "EXECUTED",
            "date": "2020-12-06T23:00:58Z",
            "amount": 29740,
            "currency_name": "Peso",
            "currency_code": "COP",
            "from": "Discover 3172601889670065",
            "to": "Discover 0720428384694643",
            "description": "Перевод с карты на карту",
        },
        {
            "id": 593027,
            "state": "CANCELED",
            "date": "2023-07-22T05:02:01Z",
            "amount": 30368,
            "currency_name": "Shilling",
            "currency_code": "TZS",
            "from": "Visa 1959232722494097",
            "to": "Visa 6804119550473710",
            "description": "Перевод с карты на карту",
        },
        {
            "id": 366176,
            "state": "EXECUTED",
            "date": "2020-08-02T09:35:18Z",
            "amount": 29482,
            "currency_name": "Rupiah",
            "currency_code": "IDR",
            "from": "Discover 0325955596714937",
            "to": "Visa 3820488829287420",
            "description": "Перевод с карты на карту",
        },
        {
            "id": 5380041,
            "state": "CANCELED",
            "date": "2021-02-01T11:54:58Z",
            "amount": 23789,
            "currency_name": "Peso",
            "currency_code": "UYU",
            "from": "",
            "to": "Счет 23294994494356835683",
            "description": "Открытие вклада",
        },
    ]

    result = read_csv("test_file.csv", sep=";")
    assert result == expected_result, f"Expected {expected_result}, but got {result}"

    mock_exists.assert_called_once_with("test_file.csv")
    mock_read_csv.assert_called_once_with("test_file.csv", sep=";")


# Тестируем ситуацию, когда файл не найден
@patch("src.transaction_proc.os.path.exists", return_value=False)
def test_file_not_found_csv(mock_exists: Mock) -> None:
    """
    Проверяем, что при отсутствии файла возникает исключение FileNotFoundError.
    """
    try:
        read_csv("test_file.csv", sep=";")
    except FileNotFoundError:
        pass  # Ожидаем, что ошибка будет вызвана
    else:
        assert False, "Expected FileNotFoundError, but no exception was raised"

    mock_exists.assert_called_once_with("test_file.csv")


# Тестируем ошибку при чтении CSV
@patch("src.transaction_proc.os.path.exists", return_value=True)
@patch("src.transaction_proc.pd.read_csv", side_effect=Exception("Ошибка чтения файла"))
def test_read_csv_error(mock_read_csv: Mock, mock_exists: Mock) -> None:
    """
    Тестируем ошибку при чтении CSV-файла.
    Возвращаем пустой список при ошибке.
    """
    result = read_csv("test_file.csv", sep=";")
    assert result == [], f"Expected [], but got {result}"

    mock_exists.assert_called_once_with("test_file.csv")
    mock_read_csv.assert_called_once_with("test_file.csv", sep=";")


# Тестируем успешное чтение Excel
@patch("pandas.read_excel")
@patch("os.path.exists", return_value=True)
def test_read_excel_success(mock_exists: Mock, mock_read_excel: Mock, mock_data: pd.DataFrame) -> None:
    """
    Тестируем успешное чтение Excel-файла.
    """
    mock_read_excel.return_value = mock_data

    expected_result = [
        {
            "id": 650703,
            "state": "EXECUTED",
            "date": "2023-09-05T11:30:32Z",
            "amount": 16210,
            "currency_name": "Sol",
            "currency_code": "PEN",
            "from": "Счет 58803664561298323391",
            "to": "Счет 39745660563456619397",
            "description": "Перевод организации",
        },
        {
            "id": 3598919,
            "state": "EXECUTED",
            "date": "2020-12-06T23:00:58Z",
            "amount": 29740,
            "currency_name": "Peso",
            "currency_code": "COP",
            "from": "Discover 3172601889670065",
            "to": "Discover 0720428384694643",
            "description": "Перевод с карты на карту",
        },
        {
            "id": 593027,
            "state": "CANCELED",
            "date": "2023-07-22T05:02:01Z",
            "amount": 30368,
            "currency_name": "Shilling",
            "currency_code": "TZS",
            "from": "Visa 1959232722494097",
            "to": "Visa 6804119550473710",
            "description": "Перевод с карты на карту",
        },
        {
            "id": 366176,
            "state": "EXECUTED",
            "date": "2020-08-02T09:35:18Z",
            "amount": 29482,
            "currency_name": "Rupiah",
            "currency_code": "IDR",
            "from": "Discover 0325955596714937",
            "to": "Visa 3820488829287420",
            "description": "Перевод с карты на карту",
        },
        {
            "id": 5380041,
            "state": "CANCELED",
            "date": "2021-02-01T11:54:58Z",
            "amount": 23789,
            "currency_name": "Peso",
            "currency_code": "UYU",
            "from": "",
            "to": "Счет 23294994494356835683",
            "description": "Открытие вклада",
        },
    ]

    result = read_excel("test_file.xlsx")
    assert result == expected_result, f"Expected {expected_result}, but got {result}"

    mock_exists.assert_called_once_with("test_file.xlsx")
    mock_read_excel.assert_called_once_with("test_file.xlsx")


# Тестируем случай, когда файл Excel не найден
@patch("os.path.exists")
def test_file_not_found_excel(mock_exists: Mock) -> None:
    """
    Тестируем, что при отсутствии Excel-файла вызывается исключение FileNotFoundError.
    """
    mock_exists.return_value = False
    try:
        read_excel("non_existent_file.xlsx")
    except FileNotFoundError:
        pass  # Ожидаем, что ошибка будет вызвана
    else:
        assert False, "Expected FileNotFoundError, but no exception was raised"


# Тестируем ошибку при чтении Excel-файла
@patch("pandas.read_excel")
@patch("os.path.exists", return_value=True)  # Мокируем os.path.exists, чтобы файл "существовал"
def test_read_excel_error(mock_exists: Mock, mock_read_excel: Mock) -> None:
    """
    Тестируем ошибку при чтении Excel-файла.
    """

    mock_read_excel.side_effect = Exception("Ошибка чтения файла Excel")

    result = read_excel("test_file.xlsx")
    assert result == [], f"Expected [], but got {result}"

    mock_exists.assert_called_once_with("test_file.xlsx")
    mock_read_excel.assert_called_once_with("test_file.xlsx")


@patch("os.path.exists")
@patch("pandas.read_excel")
def test_file_exists(mock_read_excel: Mock, mock_exists: Mock) -> None:
    """
    Тестируем, что файл существует.
    """
    mock_exists.return_value = True

    mock_read_excel.return_value = pd.DataFrame([{"id": 1, "name": "test"}])

    expected_result = [{"id": 1, "name": "test"}]  # Пример ожидаемого результата

    result = read_excel("test_file.xlsx")

    assert result == expected_result, f"Expected {expected_result}, but got {result}"

    mock_exists.assert_called_once_with("test_file.xlsx")
    mock_read_excel.assert_called_once_with("test_file.xlsx")
