import logging
import os


def get_module_logger(mod_name) -> logging.Logger:
    """
    To use this, do logger = get_module_logger(__name__)
    """
    logger = logging.getLogger(mod_name)
    stream_handler = logging.StreamHandler()

    # TODO: create new log file when current file gets big
    base_path = os.path.dirname(__file__)
    log_path = os.path.abspath(os.path.join(base_path, "..", "..", "logs/rss_log.log"))
    file_handler = logging.FileHandler(log_path)

    formatter = logging.Formatter(
        '%(asctime)s [%(name)-12s] %(levelname)-5s %(message)s')
    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)
    return logger
