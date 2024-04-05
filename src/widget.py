def convert_date_string(date_string):
    """Конвертирует строку даты из формата ISO 8601 в формат "дд.мм.гггг"""
    date_parts = date_string.split('T')[0].split('-')
    return f"{date_parts[2]}.{date_parts[1]}.{date_parts[0]}"



def mask_checcking(user_input: str) -> str:
    if a[0] == 'M' or a[0] == 'V':
        return 'card'
    elif a[0] == 'С':
        return 'account'



a = input()
print(mask_checcking(a))