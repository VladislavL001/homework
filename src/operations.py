import re
from collections import Counter


def search_operations(operations: list[dict], search_query: str) -> list[dict]:
    """Функция ищет операции по строке в описании"""
    pattern = re.compile(search_query, re.IGNORECASE)
    result = []
    for operation in operations:
        description = operation.get("description", "")
        if re.search(pattern, description):
            result.append(operation)

    return result


def categorize_operations(operations: list[dict], categories: list[str]) -> dict[str, int]:
    """Функция подсчитывает количество операций в каждой категории."""
    categorize_transaction_list = []
    for operation in operations:
        description = operation.get("description", "").lower()
        for category in categories:
            if category.lower() in description:
                categorize_transaction_list.append(category)
                break

    result = Counter(categorize_transaction_list)
    return result
