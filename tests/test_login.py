# =============================================================================
# tests/test_login.py  — Playwright version
# =============================================================================
import pytest
from playwright.sync_api import Page

from pages.login_page import LoginPage
from locators.locators import URLs
from test_data.test_data import LoginData
from utils.config import Config

class TestLogin:

    def test_valid_login_redirects_to_dashboard(self, login_page):
        login_page.open()
        login_page.login_as_admin()
        login_page.page.wait_for_url("**/dashboard.php", timeout=Config.TIMEOUT)
        assert "dashboard.php" in login_page.page.url

    def test_invalid_username_shows_error(self, login_page):
        login_page.open()
        login_page.login(LoginData.INVALID_USERNAME, LoginData.VALID_PASSWORD)
        assert login_page.is_on_login_page()
        assert login_page.is_error_displayed(), \
            "Error message should appear for invalid username"

    def test_invalid_password_shows_error(self, login_page):
        login_page.open()
        login_page.login(LoginData.VALID_USERNAME, LoginData.INVALID_PASSWORD)
        assert login_page.is_on_login_page()
        assert login_page.is_error_displayed()

    def test_empty_username_prevented(self, login_page):
        login_page.open()
        login_page.login("", LoginData.VALID_PASSWORD)
        assert login_page.is_on_login_page()

    def test_empty_password_prevented(self, login_page):
        login_page.open()
        login_page.login(LoginData.VALID_USERNAME, "")
        assert login_page.is_on_login_page()

    def test_both_fields_empty_prevented(self, login_page):
        login_page.open()
        login_page.login("", "")
        assert login_page.is_on_login_page()

    def test_logout_ends_session(self, auth_page: Page):
        from pages.dashboard_page import DashboardPage
        DashboardPage(auth_page).logout()
        # Try accessing dashboard — should redirect back to login
        auth_page.goto(URLs.DASHBOARD, wait_until="domcontentloaded",
                       timeout=Config.TIMEOUT)
        auth_page.wait_for_url("**/index.php", timeout=Config.TIMEOUT)
        assert "index.php" in auth_page.url or auth_page.url.endswith("/")

    def test_page_title_on_login(self, login_page):
        login_page.open()
        title = login_page.get_page_title()
        assert "Toreja" in title or "Clinic" in title

    def test_logo_is_displayed(self, login_page):
        login_page.open()
        assert login_page.page.locator("#system-logo").is_visible()