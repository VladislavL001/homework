from src.masks import get_mask_card_number, get_mask_account


def mask_account_card(card_type_number: str) -> str:
    """Функция принимает тип и номер карты, возвращает строку с замаскированным номером"""
    new_letters_list = []
    new_number_list = []

    for item_card in card_type_number:
        if item_card.isalpha() or item_card == " ":
            new_letters_list.append(item_card)
        else:
            new_number_list.append(item_card)

    new_number_str = "".join(new_number_list)

    if len(new_number_str) == 16:
        masked_number = get_mask_card_number(new_number_str)
    elif len(new_number_str) == 20:
        masked_number = get_mask_account(new_number_str)
    else:
        return "Неправильно введен номер или счет карты"

    return "".join(new_letters_list) + " " + masked_number
