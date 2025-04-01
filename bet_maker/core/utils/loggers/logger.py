from functools import lru_cache

from core.utils.loggers.base_logger import BaseLogger
from core.utils.loggers.default_logger import DefaultLogger


@lru_cache
def get_logger(name: str | None = None) -> BaseLogger:
    """
    Get correct logger instance based on environment.
    PS: this time only the default logger is needed.
    """
    return DefaultLogger(name)
