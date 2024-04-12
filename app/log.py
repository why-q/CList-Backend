from loguru import logger

from app.config import settings


def init_loguru():
    print(settings.LOG)
    logger.add(settings.LOG.PATH, level=settings.LOG.LEVEL, rotation="10MB")
