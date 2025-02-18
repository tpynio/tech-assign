import logging
from core.config import settings


def log_level_value(log_level: str) -> int:
    return logging.getLevelNamesMapping()[log_level.upper()]


def configure_logging():
    logging.basicConfig(
        level=log_level_value(settings.LOG_LEVEL),
        format="[%(asctime)s.%(msecs)03d] %(module)15s:%(funcName)15s:%(lineno)-4d %(levelname)7s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
