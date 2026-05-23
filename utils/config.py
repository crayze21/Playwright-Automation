# =============================================================================
# utils/config.py
# =============================================================================

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    BASE_URL   = os.getenv("BASE_URL",        "https://torejamedicalclinic.kesug.com")
    USERNAME   = os.getenv("ADMIN_USERNAME",   "admin")
    PASSWORD   = os.getenv("ADMIN_PASSWORD",   "admin123")
    BROWSER    = os.getenv("BROWSER",          "chromium")
    HEADLESS   = os.getenv("HEADLESS",         "false").lower() == "true"
    SLOW_MO    = int(os.getenv("SLOW_MO",      "0"))
    TIMEOUT    = int(os.getenv("TIMEOUT",      "60000"))   # ms — 60s default

    ROOT_DIR       = os.path.dirname(os.path.dirname(__file__))
    SCREENSHOT_DIR = os.path.join(ROOT_DIR, "screenshots")
    REPORT_DIR     = os.path.join(ROOT_DIR, "reports")
    LOG_DIR        = os.path.join(ROOT_DIR, "logs")
