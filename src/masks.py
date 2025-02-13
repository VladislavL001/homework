import logging
import os
from typing import Union

logging.basicConfig(
    filename=os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs", "masks.log"),
    filemode="w",
    format="%(asctime)s\n%(name)s:%(levelname)s\n%(message)s\n",
    level=logging.INFO,
    encoding="utf-8"
)

logger = logging.getLogger("masks.py")


def get_mask_card_number(card_number: Union[str]) -> Union[str]:
    """Функция, которая принимает номер карты числом, возвращает строку в формате маски"""
    card_number_card_str = str(card_number)
    logger.info(f"Получен номер карты: {card_number_card_str}")

    logger.info("Проверка соответствия номера карты формату")
    if len(card_number_card_str) == 16 and card_number_card_str.isdigit():
        logger.info("Карта соответствует формату. Делаю маску")
        masked_number_card = (
            f"{card_number_card_str[0:4]} {card_number_card_str[4:6]}** **** {card_number_card_str[12:]}"
        )
    else:
        logger.error("Карта не соответствует формату")
        return "Неверно введен номер карты"

    logger.info("Возврат номера карты с маской")
    return masked_number_card


def get_mask_account(account_number: Union[str]) -> Union[str]:
    """Функция, которая принимает номер счета числом, а возвращает строку в формате маски"""
    account_number_str = str(account_number)
    logger.info(f"Получен номер счета: {account_number_str}")

    logger.info("Проверка соответствия номера счета формату")
    if len(account_number_str) == 20 and account_number_str.isdigit():
        logger.info("Номер счета соответствует формату. Делаю маску")
        masked_number_account = f"**{account_number_str[-4:]}"
    else:
        logger.error("Номер счет не соответствует формату")
        return "Неверно введен номер счета"

    logger.info("Возврат счет с маской")
    return masked_number_account
