import logging
from core.config import settings
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path


def log_level_value(log_level: str) -> int:
    return logging.getLevelNamesMapping()[log_level.upper()]


def configure_logging():
    logging.basicConfig(
        level=log_level_value(settings.LOG_LEVEL),
        format="[%(asctime)s.%(msecs)03d] %(module)15s:%(funcName)15s:%(lineno)-4d %(levelname)7s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def init_logger(service_name: str) -> logging.Logger:
    logger = logging.getLogger(service_name)
    level = log_level_value(settings.LOG_LEVEL)
    logger.setLevel(level)
    formatter = logging.Formatter(
        "[%(asctime)s.%(msecs)03d] %(module)15s:%(funcName)15s:%(lineno)-4d %(levelname)7s - %(message)s",
        "%Y-%m-%d %H:%M:%S",
    )
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if len(settings.LOG_PATH):
        log_path = Path(f"{settings.LOG_PATH}/{service_name}.log")
        rotating_handler = TimedRotatingFileHandler(
            log_path,
            when="midnight",
            encoding="utf-8",
        )
        rotating_handler.setLevel(level)
        rotating_handler.setFormatter(formatter)
        logger.addHandler(rotating_handler)

    return logger
