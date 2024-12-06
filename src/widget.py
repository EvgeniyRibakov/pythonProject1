from src.masks import mask_bills, mask_cards


def convert_date_string(date_string: str) -> str:
    """
    Convert a date string from ISO 8601 format to "dd.mm.yyyy" format.

    Args:
        date_string (str): A date in ISO 8601 format (e.g., "2023-10-17T15:23:45").

    Returns:
        str: The converted date in "dd.mm.yyyy" format or "Invalid date format" if the input is not valid.
    """
    try:
        date_parts = date_string.split("T")[0].split("-")
        if len(date_parts) == 3:
            return f"{date_parts[2]}.{date_parts[1]}.{date_parts[0]}"
        else:
            return "Invalid date format"
    except IndexError:
        return "Invalid date format"


def mask_checcking(user_input: str) -> str:
    """
    Mask a card or account number based on its type.

    Args:
        user_input (str): The input string containing a card or account number.

    Returns:
        str: A masked string for a card or account, or the original input if it is not valid.
    """

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
