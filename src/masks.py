import logging

# --- Logging for masks module ---
masks_logger = logging.getLogger("masks")  # Create a logger called "masks" to collect log messages
masks_logger.setLevel(logging.DEBUG)  # Set the log level to "DEBUG", which means we will log all messages

# Create a file handler to write the log messages to a file
masks_file_handler = logging.FileHandler("masks.log")

# Create a formatter for the log messages. This defines the structure of the log message.
masks_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Set the formatter to the file handler so the logs follow the chosen format
masks_file_handler.setFormatter(masks_formatter)

# Add the file handler to the logger. This tells the logger to write the log messages to the file.
masks_logger.addHandler(masks_file_handler)


# --- End of logging for masks module ---


def mask_cards(masked_card: str) -> str:
    """
    Mask the credit card number.

    Args:
        masked_card (str): The credit card number to mask.

    Returns:
        str: The masked credit card number.

    Raises:
        Exception: If an error occurs during masking.
    """
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
    """
    Mask the bank account number.

    Args:
        masked_bill (str): The bank account number to mask.

    Returns:
        str: The masked bank account number.

    Raises:
        Exception: If an error occurs during masking.
    """
    masks_logger.debug(f"Маскировка номера счета: {masked_bill}")
    try:
        masked_bill = "" + "**" + masked_bill[-4:]
        masks_logger.debug(f"Замаскированный номер счета: {masked_bill}")
        return masked_bill
    except Exception as e:
        masks_logger.error(f"Ошибка при маскировке номера счета: {e}")
        raise
