# =============================================================================
# conftest.py  — Playwright version
# =============================================================================
# KEY DIFFERENCE FROM SELENIUM:
#   Selenium: you create the driver manually in every fixture
#   Playwright: pytest-playwright provides browser, context, page fixtures
#               built-in. You just configure them here.
# =============================================================================

import os
import pytest
import logging
from datetime import datetime
from playwright.sync_api import Page, Browser, BrowserContext

from utils.config import Config
from utils.logger import get_logger
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.patients_page import PatientsPage
from pages.new_prescription_page import NewPrescriptionPage
from pages.patient_history_page import PatientHistoryPage
from pages.medicines_page import MedicinesPage
from pages.medicine_details_page import MedicineDetailsPage
from pages.reports_page import ReportsPage
from pages.users_page import UsersPage

logger = get_logger("conftest")

os.makedirs(Config.SCREENSHOT_DIR, exist_ok=True)
os.makedirs(Config.REPORT_DIR,     exist_ok=True)
os.makedirs(Config.LOG_DIR,        exist_ok=True)


# =============================================================================
# PLAYWRIGHT BROWSER CONFIGURATION
# These hook into pytest-playwright's built-in fixture system
# =============================================================================

def pytest_configure(config):
    """Set Playwright browser options via pytest-playwright."""
    pass


@pytest.fixture(scope="session")
def browser_type_launch_args():
    """
    Configure browser launch args — equivalent to ChromeOptions in Selenium.
    Playwright handles browser download automatically (no webdriver-manager).
    """
    return {
        "headless":  Config.HEADLESS,
        "slow_mo":   Config.SLOW_MO,
        "args": [
            "--disable-notifications",
            "--disable-popup-blocking",
        ]
    }


@pytest.fixture(scope="session")
def browser_context_args(browser_type_launch_args):
    """
    Configure browser context — sets viewport, timeout, page load behaviour.
    A 'context' in Playwright = isolated browser session (like incognito).
    """
    return {
        "viewport":            {"width": 1280, "height": 900},
        "ignore_https_errors": True,
    }


# =============================================================================
# PAGE FIXTURE — base authenticated page
# pytest-playwright provides `page` automatically.
# We wrap it to set timeout and handle slow hosting.
# =============================================================================

@pytest.fixture(scope="function")
def auth_page(page: Page) -> Page:
    """
    Provides a Page that is already logged in as admin.
    Equivalent to Selenium's auth_driver fixture.

    Playwright difference: `page` is injected by pytest-playwright,
    no need to create/quit it manually.
    """
    page.set_default_timeout(Config.TIMEOUT)
    page.set_default_navigation_timeout(Config.TIMEOUT)

    login = LoginPage(page)
    for attempt in range(1, 4):
        try:
            login.open()
            break
        except Exception as e:
            logger.warning(f"Login page load attempt {attempt}/3: {e}")
            if attempt == 3:
                raise
            page.wait_for_timeout(3000)

    login.login_as_admin()
    page.wait_for_url("**/dashboard.php", timeout=Config.TIMEOUT)
    logger.info("Logged in as admin — dashboard reached")
    return page


# =============================================================================
# E2E FIXTURE — class-scoped single session
# =============================================================================

@pytest.fixture(scope="class")
def e2e_page(browser: Browser) -> Page:
    """
    Single browser session for the entire E2E class.
    Playwright difference: we manually create context+page here
    because we need class scope (not function scope).
    """
    context = browser.new_context(
        viewport={"width": 1280, "height": 900},
        ignore_https_errors=True
    )
    page = context.new_page()
    page.set_default_timeout(Config.TIMEOUT)
    page.set_default_navigation_timeout(Config.TIMEOUT)

    login = LoginPage(page)
    for attempt in range(1, 4):
        try:
            login.open()
            break
        except Exception as e:
            logger.warning(f"E2E login page attempt {attempt}/3: {e}")
            if attempt == 3:
                context.close()
                raise
            page.wait_for_timeout(3000)

    login.login_as_admin()
    page.wait_for_url("**/dashboard.php", timeout=Config.TIMEOUT)
    logger.info("E2E login successful")

    yield page

    context.close()
    logger.info("E2E browser session closed")


# =============================================================================
# PAGE OBJECT FIXTURES
# =============================================================================

@pytest.fixture
def login_page(page: Page):
    page.set_default_timeout(Config.TIMEOUT)
    return LoginPage(page)

@pytest.fixture
def dashboard_page(auth_page: Page):
    return DashboardPage(auth_page)

@pytest.fixture
def patients_page(auth_page: Page):
    p = PatientsPage(auth_page)
    p.open()
    return p

@pytest.fixture
def new_prescription_page(auth_page: Page):
    p = NewPrescriptionPage(auth_page)
    p.open()
    return p

@pytest.fixture
def patient_history_page(auth_page: Page):
    p = PatientHistoryPage(auth_page)
    p.open()
    return p

@pytest.fixture
def medicines_page(auth_page: Page):
    p = MedicinesPage(auth_page)
    p.open()
    return p

@pytest.fixture
def medicine_details_page(auth_page: Page):
    p = MedicineDetailsPage(auth_page)
    p.open()
    return p

@pytest.fixture
def reports_page(auth_page: Page):
    p = ReportsPage(auth_page)
    p.open()
    return p

@pytest.fixture
def users_page(auth_page: Page):
    p = UsersPage(auth_page)
    p.open()
    return p


# =============================================================================
# AUTO-SCREENSHOT ON FAILURE
# Playwright version — much simpler than Selenium
# =============================================================================

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report  = outcome.get_result()

    if report.when != "call" or not report.failed:
        return

    # Get the page from any fixture that holds it
    page = None
    for fixture_name in ("page", "auth_page", "e2e_page"):
        page = item.funcargs.get(fixture_name)
        if page:
            break

    if not page:
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = item.nodeid.replace("/", "_").replace("::", "_").replace(" ", "_")

    # Screenshot — Playwright makes this one line
    screenshot_path = os.path.join(
        Config.SCREENSHOT_DIR, f"FAIL_{safe_name}_{timestamp}.png"
    )
    try:
        page.screenshot(path=screenshot_path, full_page=True)
        logger.warning(f"Screenshot saved: {screenshot_path}")
    except Exception as e:
        logger.error(f"Could not save screenshot: {e}")

    # Attach to HTML report
    try:
        import pytest_html
        extras = getattr(report, "extras", [])
        extras.append(pytest_html.extras.image(screenshot_path))
        extras.append(pytest_html.extras.text(
            f"URL at failure: {page.url}", name="URL"
        ))
        report.extras = extras
    except ImportError:
        pass

    logger.error(f"Failure URL: {page.url}")


def pytest_runtest_logreport(report):
    if report.when == "call":
        status = "PASS" if report.passed else ("FAIL" if report.failed else "SKIP")
        logger.info(f"{status}  {report.nodeid}  ({report.duration:.2f}s)")
