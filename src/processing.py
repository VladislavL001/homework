def filter_by_state(records: list, state: str = "EXECUTED") -> list:
    """Функция возвращает словари, у которых ключ 'state' соответствует заданному значению."""
    filtered_records = [record for record in records if record.get("state") == state]
    return filtered_records


def sort_by_date(records: list, descending: bool = True) -> list:
    """Сортирует список словарей по ключу data"""
    sort_records = sorted(records, key=lambda record: record["data"], reverse=descending)
    return sort_records
