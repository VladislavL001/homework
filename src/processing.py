def filter_by_state(records: list, state: str = "EXECUTED") -> list:
    """Функция возвращает словари у которых ключ соответсвует state"""
    filtered_records = []
    for record in records:
        if record.get("state") == state:
            filtered_records.append(record)
    return filtered_records


def sort_by_date(records: list, descending: bool = True) -> list:
    """Сортирует список словарей по ключу date"""
    sort_records = sorted(records, key=lambda record: record["date"], reverse=descending)
    return sort_records
