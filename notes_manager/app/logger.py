import logging
from logging.handlers import RotatingFileHandler

from app.config import (
    LOG_FILE,
    LOG_MAX_BYTES,
    LOG_BACKUP_COUNT,
)


def setup_logging(level="INFO"):
    logger = logging.getLogger()

    logger.setLevel(
        logging.DEBUG
        if level == "DEBUG"
        else logging.INFO
    )

    if logger.handlers:
        return logger

    handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=LOG_MAX_BYTES,
        backupCount=LOG_BACKUP_COUNT,
        encoding="utf-8"
    )

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger