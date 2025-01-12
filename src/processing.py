def filter_by_state(records: list[dict], state: [str] = "EXECUTED") -> list[dict]:
    """Функция возвращает словари у которых ключ соответсвует state"""
    filtered_records = []
    for record in records:
        if record.get("state") == state:
            filtered_records.append(record)
    return filtered_records


def sort_by_date(records: list[dict], descending: [bool] = True) -> list[dict]:
    """Сортирует список словарей по ключу date"""
    sort_records = sorted(records, key=lambda record: record.get("date"), reverse=descending)
    return sort_records