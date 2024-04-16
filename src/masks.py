def mask_cards(masked_card: str) -> str:
    '''Принимает номер карты и возвращает изменённый зашифрованный номер
    и считывает номер счета в банке и возвращает зашифрованный
    '''
    mask_account_card = (
            masked_card[:4]
            + " "
            + masked_card[4:6]
            + "**"
            + " "
            + "****"
            + " "
            + masked_card[12:]
    )
    return mask_account_card


def mask_bills(masked_bill: str) -> str:
    return "**" + masked_bill[-4:]
    
