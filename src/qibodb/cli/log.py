"""Logging settings."""
import logging

from rich.console import Console
from rich.logging import RichHandler
from rich.traceback import install

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(console=Console(stderr=True))],
)
install()
