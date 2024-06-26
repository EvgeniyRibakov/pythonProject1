from src.masks import mask_bills, mask_cards


def convert_date_string(date_string: str) -> str:
    """Конвертирует строку даты из формата ISO 8601 в формат "дд.мм.гггг"""
    try:
        date_parts = date_string.split("T")[0].split("-")
        if len(date_parts) == 3:
            return f"{date_parts[2]}.{date_parts[1]}.{date_parts[0]}"
        else:
            return "Invalid date format"
    except IndexError:
        return "Invalid date format"


def mask_checcking(user_input: str) -> str:
    """Принимает карту/счет и номер и возвращает маску в зависимости от типа"""
    a = user_input.split(" ")
    if len(a) > 1:
        if a[0] == "Maestro" or a[0] == "MasterCard" or a[0] == "Visa":
            for i in a:
                if i.isdigit():
                    card = mask_cards(i)
            return " ".join([i for i in a if i.isalpha()]) + " " + card
        elif a[0] == "Счет":
            return a[0] + " " + mask_bills(a[1])
    return user_input
