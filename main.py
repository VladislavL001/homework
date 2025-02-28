from src.generators import filter_by_currency
from src.operations import search_operations
from src.processing import filter_by_state, sort_by_date
from src.transaction_proc import universal_path_file_csv, read_csv, universal_path_file_excel, read_excel
from src.utils import universal_path_file, load_transactions_from_json
from src.widget import mask_account_card, get_date


def main() -> None:
    """Основная логика программы"""

    # Выбор файла с транзакциями
    while True:
        print("Программа: Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
        choice_file_1 = "1. Получить информацию о транзакциях из JSON-файла"
        choice_file_2 = "2. Получить информацию о транзакциях из CSV-файла"
        choice_file_3 = "3. Получить информацию о транзакциях из XLSX-файла"
        print(
            "Выберите необходимый пункт меню:\n", choice_file_1, "\n", choice_file_2, "\n", choice_file_3, "\n", sep=""
        )
        choice_file_input = input("Пользователь: ").strip()

        transactions = []
        if choice_file_input == "1":
            choice_print = "JSON"
            PATH = universal_path_file()
            transactions = load_transactions_from_json(PATH)
        elif choice_file_input == "2":
            choice_print = "CSV"
            PATH = universal_path_file_csv()
            transactions = read_csv(PATH)
        elif choice_file_input == "3":
            choice_print = "XLSX"
            PATH = universal_path_file_excel()
            transactions = read_excel(PATH)
        else:
            print("Программа: Неверно введён код операции. Попробуйте снова.")
            continue  # Повторяем ввод

        print(f"Программа: Для обработки выбран {choice_print}-файл.")

        if not transactions:
            print("Программа: В файле нет транзакций.")
            return

        break

    # Выбор значения для сортировки
    while True:
        print(
            "Программа: Введите статус, по которому необходимо выполнить фильтрацию.\n"
            "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING"
        )
        choice_filter_input = input("Пользователь: ").strip().upper()
        if choice_filter_input not in ["EXECUTED", "CANCELED", "PENDING"]:
            print(f"Программа: Статус операции {choice_filter_input} недоступен.")
            continue

        transactions = filter_by_state(transactions, choice_filter_input)
        if not transactions:
            print(f"Программа: Нет операций со статусом {choice_filter_input}.")
            return
        break

    # Сортировка операций по дате
    while True:
        print("Программа: Отсортировать операции по дате? Да/Нет")
        choice_filter_input = input("Пользователь: ").strip().lower()
        if choice_filter_input == "да":
            print("Программа: Отсортировать по возрастанию или по убыванию?")
            sort = input("Пользователь: ").strip().lower()
            if sort == "по возрастанию":
                transactions = sort_by_date(transactions, False)
                print(1)
                break
            elif sort == "по убыванию":
                transactions = sort_by_date(transactions, True)
                break
            else:
                print(f"Нет операции со статусом {sort}")

        elif choice_filter_input == "нет":
            break
        else:
            print(f"Нет операции со статусом {choice_filter_input}")
            continue

    # Выбор валюты транзакции
    while True:
        print("Программа: Выводить только рублевые транзакции? Да/Нет")
        choice_tran_input = input("Пользователь: ").strip().lower()
        if choice_tran_input == "да":
            transactions = list(filter_by_currency(transactions, "RUB"))
            break
        elif choice_tran_input == "нет":
            break
        else:
            print(f"Нет операции со статусом {choice_tran_input}")
            continue

    # Выбор слова для фильтрации
    while True:
        print("Программа: Отфильтровать список транзакций по определенному слову в описании? Да/Нет")
        choice_filter_input = input("Пользователь: ").strip().lower()
        if choice_filter_input == "да":
            print("Программа: Введите слова для поиска")
            search_query = input("Пользователь: ").strip()
            transactions = search_operations(transactions, search_query)
            break
        if choice_filter_input == "нет":
            break
        else:
            print(f"Нет операции со статусом {choice_filter_input}")
            continue

    # Вывод
    print("\nПрограмма: Распечатываю итоговый список транзакций...")

    if not transactions:
        print("Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"Программа:\n" f"Всего банковских операций в выборке: {len(transactions)}")

    for transaction in transactions:
        print(f"\n{get_date(transaction['date'])} {transaction['description']}")
        if not transaction.get("from"):
            print(f"{mask_account_card(transaction['to'])}")
        else:
            print(
                f"{mask_account_card(str(transaction.get('to', '')))} -> "
                f"{mask_account_card(str(transaction.get('from', '')))}"
            )

        if choice_file_input == str(1):
            amount = transaction.get("operationAmount", {}).get("amount", {})
            currency = transaction.get("operationAmount", {}).get("currency", {}).get("name", {})
        else:
            amount = transaction.get("amount")
            currency = transaction.get("currency_code")

        print(f"Сумма: {amount} {currency}")


if __name__ == "__main__":
    main()
