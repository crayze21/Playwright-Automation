# =============================================================================
# utils/logger.py
# =============================================================================
import logging
import os
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler

from utils.config import Config

class _Colours:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    GREY    = "\033[90m"
    CYAN    = "\033[96m"
    YELLOW  = "\033[93m"
    RED     = "\033[91m"
    MAGENTA = "\033[95m"
    LEVEL   = {
        "DEBUG":    GREY,
        "INFO":     CYAN,
        "WARNING":  YELLOW,
        "ERROR":    RED,
        "CRITICAL": MAGENTA + BOLD,
    }

class _ColouredFormatter(logging.Formatter):
    FMT  = "%(asctime)s  %(levelname)-8s  %(name)s  %(message)s"
    DATE = "%H:%M:%S"

    def format(self, record):
        colour = _Colours.LEVEL.get(record.levelname, _Colours.RESET)
        record.levelname = f"{colour}{record.levelname}{_Colours.RESET}"
        return logging.Formatter(self.FMT, datefmt=self.DATE).format(record)

class _PlainFormatter(logging.Formatter):
    FMT  = "%(asctime)s  %(levelname)-8s  %(name)-30s  %(message)s"
    DATE = "%Y-%m-%d %H:%M:%S"
    def __init__(self): super().__init__(fmt=self.FMT, datefmt=self.DATE)

def _build_root_logger():
    root = logging.getLogger("pms_pw")
    root.setLevel(logging.DEBUG)
    if root.handlers:
        return root

    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    console.setFormatter(_ColouredFormatter())
    root.addHandler(console)

    os.makedirs(Config.LOG_DIR, exist_ok=True)
    timestamp   = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_handler = RotatingFileHandler(
        os.path.join(Config.LOG_DIR, f"test_run_{timestamp}.log"),
        maxBytes=5 * 1024 * 1024, backupCount=10, encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(_PlainFormatter())
    root.addHandler(file_handler)
    return root

_ROOT_LOGGER = _build_root_logger()

def get_logger(name: str) -> logging.Logger:
    return _ROOT_LOGGER.getChild(name)