import logging

# --- Логирование модуля masks ---
masks_logger = logging.getLogger("masks")
masks_logger.setLevel(logging.DEBUG)

# Создаем обработчик для записи логов в файл
masks_file_handler = logging.FileHandler("masks.log")

# Создаем форматтер для логов
masks_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Устанавливаем форматтер для обработчика
masks_file_handler.setFormatter(masks_formatter)

# Добавляем обработчик к логгеру
masks_logger.addHandler(masks_file_handler)


# --- Конец логирования модуля masks ---


def mask_cards(masked_card: str) -> str:
    """Принимает номер карты и возвращает изменённый зашифрованный номер"""
    masks_logger.debug(f"Маскировка номера карты: {masked_card}")  # Логирование начала
    try:
        mask_account_card = (
            masked_card[:4] + " " + masked_card[4:6] + "" + "**" + " " + "****" + " " + masked_card[12:]
        )
        masks_logger.debug(f"Замаскированный номер карты: {mask_account_card}")  # Логирование результата
        return mask_account_card
    except Exception as e:
        masks_logger.error(f"Ошибка при маскировке номера карты: {e}")  # Логирование ошибки
        raise


def mask_bills(masked_bill: str) -> str:
    """Считывает номер счета в банке и возвращает зашифрованный"""
    masks_logger.debug(f"Маскировка номера счета: {masked_bill}")
    try:
        masked_bill = "" + "**" + masked_bill[-4:]
        masks_logger.debug(f"Замаскированный номер счета: {masked_bill}")
        return masked_bill
    except Exception as e:
        masks_logger.error(f"Ошибка при маскировке номера счета: {e}")
        raise
