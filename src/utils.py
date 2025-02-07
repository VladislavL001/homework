import json
import os
from typing import Union

from src.external_api import get_exchange_rate


def universal_path_file() -> str:
    """Функция находит абсолютный путь до файла "operations.json" независимо от ОС."""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(base_dir, "data", "operations.json")
    return file_path


def load_transactions_from_json(file_path: str) -> list[dict]:
    """Функция принимает json файл и возвращает список."""
    try:
        with open(file_path, "r", encoding="utf-8") as data_file_json:
            data_py = json.load(data_file_json)
    except FileNotFoundError:
        print("❌ Файл не найден по пути:", file_path)
        return []
    except json.JSONDecodeError:
        print("❌ Ошибка декодирования JSON.")
        return []

    return data_py if isinstance(data_py, list) else []  # Тотальная обработка исключений


def convert_to_rub(data: Union[list[dict], dict]) -> Union[list[dict], float]:
    """Конвертация валютных транзакций в рубли."""
    usd_rate = get_exchange_rate("1", "USD")
    eur_rate = get_exchange_rate("1", "EUR")

    # Принимает список словарей
    if isinstance(data, list):
        list_filter_transactions = []
        for i in data:
            temp_dict = {}

            operation_amount = i.get("operationAmount")
            if not operation_amount:  # Если нет ключа operationAmount или его значение None, пропускаем
                continue

            key_currency_code = i.get("operationAmount", {}).get("currency", {}).get("code", {})
            currency_amount = float(operation_amount.get("amount"))

            # Если валюта в рублях
            if key_currency_code == "RUB":
                temp_dict["id"] = i["id"]
                temp_dict["amount"] = currency_amount
                list_filter_transactions.append(temp_dict)

            # Если валюта в долларах
            elif key_currency_code == "USD":
                temp_dict["id"] = i["id"]
                amount_rub = round(currency_amount / usd_rate, 2)
                temp_dict["amount"] = amount_rub
                list_filter_transactions.append(temp_dict)

            # Если валюта в евро
            elif key_currency_code == "EUR":
                temp_dict["id"] = i["id"]
                amount_rub = round(currency_amount / eur_rate, 2)
                temp_dict["amount"] = amount_rub
                list_filter_transactions.append(temp_dict)

        return list_filter_transactions

    # Принимает одинокий словарь
    elif isinstance(data, dict):
        key_currency_code = data.get("operationAmount", {}).get("currency", {}).get("code")
        currency_amount = float(data["operationAmount"]["amount"])

        # Если валюта в рублях
        if key_currency_code == "RUB":
            return currency_amount

        # Если валюта в долларах
        elif key_currency_code == "USD":
            return round(currency_amount / usd_rate, 2)

        # Если валюта в евро
        elif key_currency_code == "EUR":
            return round(currency_amount / eur_rate, 2)

    return []  # Если данные не соответствуют формату


transactions = load_transactions_from_json(
    universal_path_file()
)  # Передача пути в функцию load_transactions_from_json
func = convert_to_rub(transactions)

print(transactions)
