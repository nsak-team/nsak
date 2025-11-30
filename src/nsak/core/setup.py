import logging

from nsak.core.config import DEBUG


def setup() -> None:
    """
    Set up the nsak core.
    """
    if DEBUG:
        logging.basicConfig(level=logging.DEBUG)
