import logging
import os

import colorlog

logger = logging.getLogger()


def init_logging(level=logging.INFO, path=None):
    logger.setLevel(logging.INFO)
    # create file handler which logs even debug messages
    
    formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(levelname)s:%(name)s:%(funcName)s%(message)s",
        log_colors={
            "DEBUG": "blue",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_white",
        },
    )
    # create console handler with a provided log level
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
