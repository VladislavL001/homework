from unittest.mock import Mock, patch

import pytest

from src.external_api import get_exchange_rate  # Импортируем твою функцию


@patch("requests.request")
def test_get_exchange_rate_usd_success(mock_request: Mock) -> None:
    """Тест на успешное получение курса для USD"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"info": {"rate": 0.01}}
    mock_request.return_value = mock_response
    result = get_exchange_rate("1", "USD")
    assert result == 0.01


@patch("requests.request")
def test_get_exchange_rate_invalid_currency(mock_request: Mock, capsys: pytest.CaptureFixture) -> None:
    """Тест на неверную подачу валюты"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    mock_request.return_value = mock_response
    result = get_exchange_rate("1", "ZXC")
    captured = capsys.readouterr()
    assert captured.out == "❌ Ошибка в ответе API: отсутствуют ключи 'info' или 'rate'.\n"
    assert result is None


@patch("requests.request")
def test_get_exchange_rate_api_failure(mock_request: Mock, capsys: pytest.CaptureFixture) -> None:
    mock_response = Mock()
    mock_response.status_code = 500
    mock_response.json.return_value = {}
    mock_request.return_value = mock_response
    result = get_exchange_rate("1", "USD")
    captured = capsys.readouterr()
    assert captured.out == "❌ Ошибка при запросе API. Статус код: 500\n"
    assert result is None
