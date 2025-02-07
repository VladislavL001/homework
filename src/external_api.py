import os
from typing import Union

import requests
from dotenv import load_dotenv


def get_exchange_rate(amount: str, base_currency: str, conversion_currency: str = "RUB") -> Union[float]:
    "Функция вовзращает валютные коэф. для перевода в рубли"
    load_dotenv()
    API_KEY = os.getenv("API_KEY")
    url = (
        f"https://api.apilayer.com/exchangerates_data/convert?to={base_currency}&from={conversion_currency}"
        f"&amount={amount}"
    )
    payload: dict = {}
    headers = {"apikey": API_KEY}
    response = requests.request("GET", url, headers=headers, data=payload)

    result = float(response.json()["info"]["rate"])
    return result
