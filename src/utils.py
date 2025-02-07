import json
import os

def universal_path_file() -> str:
    """ Функция находит абсолютный путь до файла "operations.json" независимо от ОС. """

    base_dir = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(base_dir, "data", "operations.json")
    return file_path

def load_transactions_from_json(file_path:str) -> list[dict]:
    """ Функция принимает json файл и возвращает список. """

    try:
        with open(file_path, "r", encoding= "utf-8") as data_file_json:
            data_py = json.load(data_file_json)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    return data_py if isinstance(data_py, list) else [] # Тотальная обработка исключений

load_transactions_from_json(universal_path_file()) #Передача пути в функцию load_transactions_from_json




