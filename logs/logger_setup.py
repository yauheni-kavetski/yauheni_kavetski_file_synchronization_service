from loguru import logger

from config_data import config


def setup_logging():
    logger.remove()  # Убираем дефолтный вывод в stderr
    logger.add(config.LOG_FILE,
               format="synchroniser  {time:YYYY-MM-DD HH:mm:ss,SSS} {level} {message}",
               level="INFO",
               encoding="utf-8",
               rotation="10 MB",
               retention="10 days",
               enqueue=True
               )
