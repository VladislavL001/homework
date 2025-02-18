import os

import pandas as pd


def universal_path_file_csv() -> str:
    """Функция находит абсолютный путь до файла "transactions.csv" независимо от ОС."""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(base_dir, "data", "transactions.csv")
    return file_path


def read_csv(file_path: str, sep: str = ";") -> list:
    """Функция принимает csv файл и возвращает список словарей."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл {file_path} не найден.")
    try:
        df = pd.read_csv(file_path, sep=sep)
        data_dict = df.to_dict("records")

        return data_dict
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return []


read_csv(universal_path_file_csv())


def universal_path_file_excel() -> str:
    """Функция находит абсолютный путь до файла "transactions_excel.xlsx" независимо от ОС."""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(base_dir, "data", "transactions_excel.xlsx")
    return file_path


def read_excel(file_path: str) -> list:
    """Функция принимает csv файл и возвращает список словарей."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл {file_path} не найден.")
    try:
        df = pd.read_excel(file_path)
        data_dict = df.to_dict("records")
        return data_dict
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return []


read_excel(universal_path_file_excel())
