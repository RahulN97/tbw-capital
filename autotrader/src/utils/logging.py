import logging
from logging import Formatter, Logger, StreamHandler


DEFAULT_LOG_LEVEL: str = "INFO"


def create_logger() -> Logger:
    logger: Logger = logging.getLogger()

    if logger.hasHandlers():
        logger.handlers.clear()

    logger.setLevel(DEFAULT_LOG_LEVEL)

    console_handler: StreamHandler = logging.StreamHandler()
    console_handler.setLevel(DEFAULT_LOG_LEVEL)
    formatter: Formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


logger: logging.Logger = create_logger()
