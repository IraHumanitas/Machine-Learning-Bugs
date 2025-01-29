import logging

def setup_logger():
    logger = logging.getLogger("TestLogger")
    handler = logging.FileHandler('test_log.txt')  
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

def log_message(logger, level, message):
    if level == "info":
        logger.info(message)
    elif level == "error":
        logger.error(message)
    elif level == "debug":
        logger.debug(message)
    else:
        logger.warning(message)
