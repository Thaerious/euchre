import logging
import os

LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

logging.basicConfig(
    level=LEVEL,
    format="[%(levelname)s] %(name)s:%(lineno)d - %(message)s",
)

def get_logger(name=None):
    """Return a logger configured for the given module."""
    return logging.getLogger(name)