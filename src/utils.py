import json
import logging
import os
from typing import Any, Union

from src.external_api import get_exchange_rate

logging.basicConfig(
    filename=os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs", "utils.log"),
    filemode="w",
    format="%(asctime)s\n%(name)s:%(levelname)s\n%(message)s\n",
    level=logging.INFO,
    encoding="utf-8",
)

logger = logging.getLogger("utils.log")


def universal_path_file() -> str:
    """Функция находит абсолютный путь до файла "operations.json" независимо от ОС."""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(base_dir, "data", "operations.json")
    logger.info(f"Создан путь до файла {file_path}")
    return file_path


def load_transactions_from_json(file_path: str) -> list[dict]:
    """Функция принимает json файл и возвращает список."""
    try:
        logger.info("Открытие json файла")
        with open(file_path, "r", encoding="utf-8") as data_file_json:
            data_py = json.load(data_file_json)
            logger.info("Файл открыт, данные сохранены")
    except FileNotFoundError:
        logger.error(f"❌ Файл не найден по пути:{file_path}")
        return []
    except json.JSONDecodeError:
        logger.error("❌ Ошибка декодирования JSON.")
        return []

    logger.info("Вывод результата в консоль")
    return data_py if isinstance(data_py, list) else []  # Тотальная обработка исключений


def convert_to_rub(data: Union[list[dict], dict, Any]) -> Union[list[dict], float, None]:
    """Конвертация валютных транзакций в рубли."""

    logger.info("Получение курсов валют")
    usd_rate = get_exchange_rate("1", "USD")
    eur_rate = get_exchange_rate("1", "EUR")

    # Проверка на ошибки при получении курсов валют
    if usd_rate is None or eur_rate is None:
        logger.error("❌ Ошибка получения валютных курсов.")
        return []

    logger.info("Курсы валют получены")

    # Принимает список словарей
    if isinstance(data, list):
        logger.info("Принят список словарей")
        list_filter_transactions = []
        for i in data:
            if not isinstance(i, dict):
                logger.error(f"❌ Пропускаем некорректный элемент: {i}")
                continue

            temp_dict = {}
            operation_amount = i.get("operationAmount")
            if not operation_amount:  # Если нет ключа operationAmount или его значение None, пропускаем
                logger.warning(f"Отсутствует ключ 'operationAmount' у элемента {i}")
                continue

            try:
                key_currency_code = operation_amount.get("currency", {}).get("code")
                currency_amount = float(operation_amount.get("amount"))
            except (ValueError, TypeError) as e:
                logger.error(f"❌ Ошибка преобразования данных транзакции: {e}")
                continue

            # Если валюта в рублях
            if key_currency_code == "RUB":
                temp_dict["id"] = i.get("id")
                temp_dict["amount"] = currency_amount
                list_filter_transactions.append(temp_dict)

            # Если валюта в долларах
            elif key_currency_code == "USD":
                temp_dict["id"] = i.get("id")
                amount_rub = round(currency_amount / usd_rate, 2)
                temp_dict["amount"] = amount_rub
                list_filter_transactions.append(temp_dict)

            # Если валюта в евро
            elif key_currency_code == "EUR":
                temp_dict["id"] = i.get("id")
                amount_rub = round(currency_amount / eur_rate, 2)
                temp_dict["amount"] = amount_rub
                list_filter_transactions.append(temp_dict)

        logger.info("Вывод списка словарей с id транзакции и суммой в рублях")
        return list_filter_transactions

    # Принимает одинокий словарь
    elif isinstance(data, dict):
        logger.info("Принят словарь")
        try:
            key_currency_code = data.get("operationAmount", {}).get("currency", {}).get("code")
            logger.info(f"Код валюты {key_currency_code}")
            currency_amount = float(data["operationAmount"]["amount"])
            logger.info(f"Сумма транзакции {currency_amount}")
        except (ValueError, TypeError) as e:
            logger.error(f"❌ Ошибка преобразования данных транзакции: {e}")
            return None

        # Если валюта в рублях
        if key_currency_code == "RUB":
            return currency_amount

        # Если валюта в долларах
        elif key_currency_code == "USD":
            return round(currency_amount / usd_rate, 2)

        # Если валюта в евро
        elif key_currency_code == "EUR":
            return round(currency_amount / eur_rate, 2)

    # Если данные не соответствуют ни одному из типов
    logger.error("❌ Ошибка: данные не являются списком или словарем.")
    return []
