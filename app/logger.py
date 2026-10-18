
import logging


class Logger:
    """Centralized logging for the enhanced calculator."""

    @staticmethod
    def info(message: str) -> None:
        logging.info(message)

    @staticmethod
    def warning(message: str) -> None:
        logging.warning(message)

    @staticmethod
    def error(message: str) -> None:
        logging.error(message)

    @staticmethod
    def exception(message: str) -> None:
        logging.exception(message)
