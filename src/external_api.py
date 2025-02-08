import os
from typing import Union

import requests
from dotenv import load_dotenv


def get_exchange_rate(amount: str, base_currency: str, conversion_currency: str = "RUB") -> Union[float, None]:
    """Функция возвращает валютные коэф. для перевода в рубли"""
    load_dotenv()
    API_KEY = os.getenv("API_KEY")
    url = (
        f"https://api.apilayer.com/exchangerates_data/convert?to={base_currency}&from={conversion_currency}"
        f"&amount={amount}"
    )
    payload: dict = {}
    headers = {"apikey": API_KEY}
    try:
        response = requests.request("GET", url, headers=headers, data=payload)

        if response.status_code != 200:
            print(f"❌ Ошибка при запросе API. Статус код: {response.status_code}")
            return None

        data = response.json()

        # Проверка, что в ответе есть необходимые ключи
        if "info" not in data or "rate" not in data["info"]:
            print("❌ Ошибка в ответе API: отсутствуют ключи 'info' или 'rate'.")
            return None

        # Преобразуем в float
        result = float(data["info"]["rate"])
        return result

    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка запроса: {e}")
        return None

    except ValueError as e:
        print(f"❌ Ошибка преобразования в float: {e}")
        return None
