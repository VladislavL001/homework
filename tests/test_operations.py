from src.operations import search_operations, categorize_operations
import pytest

@pytest.fixture
def data() -> list[dict]:
    """Данные для тестов"""
    data_list =  [
            {"id": 1, "description": "Перевод с карты на карту", "amount": 100},
            {"id": 2, "description": "Открытие вклада", "amount": 200},
            {"id": 3, "description": "Перевод на счет", "amount": 300},
            {"id": 4, "description": "Погашение кредита", "amount": 150},
        ]
    return data_list


def test_search_operations_found(data: list[dict]) -> None:
    """Функция находит операции по строке в описании"""
    search_query = "перевод"
    expected_result = [
        {"id": 1, "description": "Перевод с карты на карту", "amount": 100},
        {"id": 3, "description": "Перевод на счет", "amount": 300}
    ]
    result = search_operations(data, search_query)
    assert result == expected_result


def test_search_operations_not_found(data: list[dict]) -> None:
    """Функция не находит операций по строке в описании"""
    search_query = "депозит"
    expected_result = []
    result = search_operations(data, search_query)
    assert result == expected_result


def test_search_operations_case_insensitive(data: list[dict]) -> None:
    """Функция не чувствительна к регистру"""
    search_query = "ПЕРЕВОД"
    expected_result = [
        {"id": 1, "description": "Перевод с карты на карту", "amount": 100},
        {"id": 3, "description": "Перевод на счет", "amount": 300},
    ]
    result = search_operations(data, search_query)
    assert result == expected_result

def test_search_operations_empty_query(data: list[dict]) -> None:
    """Пустой запрос возвращает все операции"""
    search_query = ""
    expected_result = data
    result = search_operations(data, search_query)
    assert result == expected_result


def test_categorize_operations_success(data):
    """Тестируем правильную работу функции для существующих категорий"""
    categories = ["перевод", "кредит"]
    expected = {'перевод': 2, 'кредит': 1}
    result = categorize_operations(data, categories)
    assert result == expected

def test_categorize_operations_no_match(data):
    """Тестируем ситуацию, когда нет совпадений с категориями"""
    categories = ["брокерский счет"]
    expected = {}
    result = categorize_operations(data, categories)
    assert result == expected

def test_categorize_operations_empty_list(data: list[dict]):
    """Тестируем ситуацию с пустым списком операций"""
    result = categorize_operations([], ["кредит"])
    assert result == {}


def test_categorize_operations_empty_categories(data):
    """Тестируем ситуацию с пустым списком категорий"""
    result = categorize_operations(data, [])
    assert result == {}

def test_categorize_operations_case_insensitive(data):
    """Тестируем нечувствительность к регистру"""
    categories = ["Перевод", "кредИТ"]
    expected = {'Перевод': 2, 'кредИТ': 1}
    result = categorize_operations(data, categories)
    assert result == expected