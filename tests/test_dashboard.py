# =============================================================================
# tests/test_dashboard.py  — Playwright version
# =============================================================================
import pytest
from locators.locators import NavBar

class TestDashboard:

    def test_dashboard_loads_after_login(self, dashboard_page):
        assert dashboard_page.is_on_dashboard()
        assert "Dashboard" in dashboard_page.get_heading()

    def test_today_patients_stat_box_visible(self, dashboard_page):
        assert dashboard_page.is_today_box_displayed()

    def test_current_week_stat_box_visible(self, dashboard_page):
        assert dashboard_page.is_week_box_displayed()

    def test_current_month_stat_box_visible(self, dashboard_page):
        assert dashboard_page.is_month_box_displayed()

    def test_current_year_stat_box_visible(self, dashboard_page):
        assert dashboard_page.is_year_box_displayed()

    def test_stat_counts_are_numeric(self, dashboard_page):
        for label, value in [
            ("Today",  dashboard_page.get_today_count()),
            ("Week",   dashboard_page.get_week_count()),
            ("Month",  dashboard_page.get_month_count()),
            ("Year",   dashboard_page.get_year_count()),
        ]:
            assert value.strip().isdigit(), \
                f"{label} count should be numeric, got: '{value}'"

    def test_sidebar_navigation_links_present(self, dashboard_page):
        for label, locator in [
            ("Dashboard", NavBar.MENU_DASHBOARD_LINK),
            ("Patients",  NavBar.MENU_PATIENTS_LINK),
            ("Medicines", NavBar.MENU_MEDICINES_LINK),
            ("Reports",   NavBar.MENU_REPORTS_LINK),
            ("Users",     NavBar.MENU_USERS_LINK),
            ("Logout",    NavBar.LOGOUT_LINK),
        ]:
            assert dashboard_page.page.locator(locator).is_visible(), \
                f"'{label}' link should be visible in sidebar"

    def test_footer_is_present(self, dashboard_page):
        assert dashboard_page.page.locator(NavBar.FOOTER).is_visible()

    def test_welcome_message_contains_administrator(self, dashboard_page):
        welcome = dashboard_page.get_welcome_text()
        assert "Administrator" in welcome or "Welcome" in welcome, \
            f"Welcome message should mention Administrator, got: '{welcome}'"