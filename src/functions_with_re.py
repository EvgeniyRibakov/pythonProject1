import re
from typing import Dict, List, Pattern


def search_transactions(transactions: List[Dict[str, str]], search_string: str) -> List[Dict[str, str]]:
    """
    Фильтрует список банковских операций по строке поиска в описании
    """
    search_pattern: Pattern[str] = re.compile(re.escape(search_string), re.IGNORECASE)
    return [transaction for transaction in transactions if search_pattern.search(transaction.get("description", ""))]


def categorize_transactions(transactions: List[Dict[str, str]], categories: Dict[str, str]) -> Dict[str, int]:
    """
    Категоризирует банковские операции и подсчитывает количество операций в каждой категории
    """
    category_counts: Dict[str, int] = {category: 0 for category in categories.values()}
    for transaction in transactions:
        description = transaction["description"]
        for keyword, category in categories.items():
            if keyword.lower() in description.lower():
                category_counts[category] += 1
                break
    return category_counts
