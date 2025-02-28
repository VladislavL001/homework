import re
from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(card_type_number: str) -> str:
    """Функция принимает тип и номер карты, возвращает строку с замаскированным номером"""
    pattern = r"(\d+)|(\s+)|([^\d\s]+)"
    matches = re.findall(pattern, card_type_number)

    result: dict[str, list[str]] = {"words": [], "spaces": [], "numbers": []}

    for match in matches:
        if match[0]:  # Если совпадение в группе для цифр
            result["numbers"].append(match[0])
        elif match[1]:  # Если совпадение в группе для пробелов
            result["spaces"].append(match[1])
        elif match[2]:  # Если совпадение в группе для слов
            result["words"].append(match[2])

    words_str = " ".join(result["words"])
    number_str = "".join(result["numbers"])

    if len(number_str) == 16:
        masked_number = get_mask_card_number(number_str)
    elif len(number_str) == 20:
        masked_number = get_mask_account(number_str)
    else:
        return "Неправильно введен номер или счет карты"

    return words_str + " " + masked_number


def get_date(data_form: str) -> str:
    """Функция преобразует формат даты в ДД.ММ.ГГГГ"""
    try:
        parsed_date = datetime.fromisoformat(data_form.replace("Z", ""))
        return parsed_date.strftime("%d.%m.%Y")
    except ValueError:

        try:
            parsed_date = datetime.strptime(data_form, "%Y-%m-%d %H:%M:%S")
            return parsed_date.strftime("%d.%m.%Y")
        except ValueError:
            return "Неверный формат даты"
