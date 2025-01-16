import re
from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(card_type_number: str) -> str:
    """Функция принимает тип и номер карты, возвращает строку с замаскированным номером"""
    pattern = r'(\d+)|(\s+)|([^\d\s]+)'
    matches = re.findall(pattern, card_type_number)

    result = {
        "words": [],
        "spaces": [],
        "numbers": []
    }

    for match in matches:
        if match[0]:  # Если совпадение в группе для цифр
            result["numbers"].append(match[0])
        elif match[1]:  # Если совпадение в группе для пробелов
            result["spaces"].append(match[1])
        elif match[2]:  # Если совпадение в группе для слов
            result["words"].append(match[2])

    words_str = " ".join(result.get ("words"))
    number_str = "".join(result.get ("numbers"))

    if len(number_str) == 16:
        masked_number = get_mask_card_number(number_str)
    elif len(number_str) == 20:
        masked_number = get_mask_account(number_str)
    else:
        return "Неправильно введен номер или счет карты"

    return words_str + " " + masked_number


def get_date(data_form: str) -> str:
    """Функция преобразует формат даты в ДД.ММ.ГГГГ"""
    data_new_form = f"{data_form[8:10]}.{data_form[5:7]}.{data_form[0:4]}"
    return data_new_form

print (mask_account_card ("Visa Platinum 7000792289606361"))