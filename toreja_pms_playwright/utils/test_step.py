# =============================================================================
# utils/test_step.py
# =============================================================================

import time
import logging
from contextlib import contextmanager

from utils.logger import get_logger

logger = get_logger("step")


@contextmanager
def step(description: str, level: int = logging.INFO):
    start = time.time()
    logger.log(level, f"┌─ {description}")
    try:
        yield
        elapsed = time.time() - start
        logger.log(level, f"└─ PASS  {description}  ({elapsed:.2f}s)")
    except Exception as exc:
        elapsed = time.time() - start
        logger.error(f"└─ FAIL  {description}  ({elapsed:.2f}s)")
        logger.error(f"   {type(exc).__name__}: {exc}")
        raise
