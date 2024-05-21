import logging


def mask_cards(masked_card: str) -> str:
    """Принимает номер карты и возвращает изменённый зашифрованный номер"""
    mask_account_card = masked_card[:4] + " " + masked_card[4:6] + "**" + " " + "****" + " " + masked_card[12:]
    return mask_account_card


def mask_bills(masked_bill: str) -> str:
    """Считывает номер счета в банке и возвращает зашифрованный"""
    return "**" + masked_bill[-4:]


# Создание отдельного объекта логгера для модуля masks
masks_logger = logging.getLogger('masks')
masks_logger.setLevel(logging.DEBUG)

# Настройка file_handler для логгера модуля masks
masks_file_handler = logging.FileHandler('masks.log', mode='w')
masks_file_handler.setLevel(logging.DEBUG)

# Настройка форматтера для логгера модуля masks
masks_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
masks_file_handler.setFormatter(masks_formatter)

# Добавление обработчика файлов к логгеру модуля masks
masks_logger.addHandler(masks_file_handler)

# Создание отдельного объекта логгера для модуля external_api
external_api_logger = logging.getLogger('external_api')
external_api_logger.setLevel(logging.DEBUG)

# Настройка file_handler для логгера модуля external_api
external_api_file_handler = logging.FileHandler('external_api.log', mode='w')
external_api_file_handler.setLevel(logging.DEBUG)

# Настройка форматтера для логгера модуля external_api
external_api_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
external_api_file_handler.setFormatter(external_api_formatter)

# Добавление обработчика файлов к логгеру модуля external_api
external_api_logger.addHandler(external_api_file_handler)
