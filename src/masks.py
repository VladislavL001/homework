from typing import Union


def get_mask_card_number(card_number: Union[str]) -> Union[str]:
    """Функция, которая принимает номер карты числом,возвращает строку в формате маски"""
    card_number_card_str = str(card_number)

    if len(card_number_card_str) == 16 and card_number_card_str.isdigit():
        masked_number_card = f"{card_number_card_str[0:4]} {card_number_card_str[4:6]}** **** {card_number_card_str[12:]}"
    else:
        return "Неверно введен номер карты"
    return masked_number_card


def get_mask_account(account_number: Union[str]) -> Union[str]:
    """Функция, которая принимает номер счета числом, а возвращает строку в формате маски"""
    account_number_str = str(account_number)

    if len(account_number_str) != 20:
        return "Неверно введен номер счета"

    masked_number_account = f"**{account_number_str[-4:]}"
    return masked_number_account


