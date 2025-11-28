import logging

from src.core import config


def setup() -> None:
    """
    Setup the nsak core.
    """
    if config.DEBUG:
        logging.basicConfig(level=logging.DEBUG)
