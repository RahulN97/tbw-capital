import logging
from logging import Formatter, Logger, StreamHandler


class CoreLogger:

    def __init__(self, level: str = "INFO") -> None:
        self.logger: Logger = self._create_logger(level.upper())

    def _create_logger(self, level: str) -> Logger:
        logger: Logger = logging.getLogger()

        if logger.hasHandlers():
            logger.handlers.clear()

        console_handler: StreamHandler = self._create_console_handler(level)
        logger.addHandler(console_handler)

        logger.setLevel(level)

        return logger

    @staticmethod
    def _create_console_handler(level: str) -> StreamHandler:
        console_handler: StreamHandler = StreamHandler()
        console_handler.setLevel(level)
        formatter: Formatter = Formatter("%(asctime)s - %(levelname)s - %(message)s")
        console_handler.setFormatter(formatter)
        return console_handler

    def set_level(self, level: str) -> None:
        self.logger.setLevel(level.upper())

    def warn(self, line: str) -> None:
        self.logger.warn(line)

    def debug(self, line: str) -> None:
        self.logger.debug(line)

    def info(self, line: str) -> None:
        self.logger.info(line)

    def error(self, line: str) -> None:
        self.logger.error(line)


logger: CoreLogger = CoreLogger()
