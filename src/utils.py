import logging


def get_logger(logger_name):
    file_handler = logging.FileHandler('./logs/log.log', encoding='utf-8')
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    file_handler.setLevel(logging.INFO)
    logger = logging.getLogger(logger_name)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)
    return logger
