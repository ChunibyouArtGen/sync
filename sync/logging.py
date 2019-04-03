import logging
import os
import colorlog

logger = logging.getLogger()


def init_logging(level=logging.INFO, path=None):
    if path is None:
        path = os.path.join(os.getcwd(), "log.txt")

    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = None
    formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(levelname)s:%(name)s:%(message)s",
        log_colors={
            "DEBUG": "blue",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_white",
        },
    )
    try:
        fh = logging.FileHandler(path)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    except Exception:
        logger.debug("Failed to create log file")
    # create console handler with a provided log level
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
