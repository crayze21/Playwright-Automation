# =============================================================================
# tests/test_smoke.py  — Playwright version
# Fast sanity checks — one per module, run on every deploy
# Run: pytest -m smoke
# =============================================================================
import pytest
from playwright.sync_api import Page

from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.patients_page import PatientsPage
from pages.medicines_page import MedicinesPage
from pages.medicine_details_page import MedicineDetailsPage
from pages.new_prescription_page import NewPrescriptionPage
from pages.patient_history_page import PatientHistoryPage
from pages.reports_page import ReportsPage
from pages.users_page import UsersPage
from locators.locators import NavBar, URLs
from utils.config import Config

@pytest.mark.smoke
class TestSmoke:

    def test_smoke_login_page_loads(self, login_page):
        login_page.open()
        assert login_page.is_on_login_page()
        assert login_page.page.locator("button[name='login']").is_visible(), \
            "Login button must be visible"

    def test_smoke_valid_login(self, login_page):
        login_page.open()
        login_page.login_as_admin()
        login_page.page.wait_for_url("**/dashboard.php", timeout=Config.TIMEOUT)
        assert "dashboard.php" in login_page.page.url

    def test_smoke_dashboard_loads(self, dashboard_page):
        assert dashboard_page.is_on_dashboard()
        assert dashboard_page.is_today_box_displayed()

    def test_smoke_patients_page_loads(self, auth_page: Page):
        page = PatientsPage(auth_page)
        page.open()
        assert page.is_on_page()
        assert auth_page.locator("#all_patients").is_visible(), \
            "Patients table must be visible"

    def test_smoke_medicines_page_loads(self, auth_page: Page):
        page = MedicinesPage(auth_page)
        page.open()
        assert page.is_on_page()
        assert auth_page.locator("#all_medicines").is_visible(), \
            "Medicines table must be visible"

    def test_smoke_medicine_details_page_loads(self, auth_page: Page):
        page = MedicineDetailsPage(auth_page)
        page.open()
        assert page.is_on_page()
        assert auth_page.locator("#medicine_details").is_visible(), \
            "Medicine details table must be visible"

    def test_smoke_new_prescription_page_loads(self, auth_page: Page):
        page = NewPrescriptionPage(auth_page)
        page.open()
        assert page.is_on_page()
        assert auth_page.locator("#add_row").is_visible(), \
            "Add row button must be visible"

    def test_smoke_patient_history_page_loads(self, auth_page: Page):
        page = PatientHistoryPage(auth_page)
        page.open()
        assert page.is_on_page()
        assert auth_page.locator("#search").is_visible(), \
            "Search button must be visible"

    def test_smoke_reports_page_loads(self, auth_page: Page):
        page = ReportsPage(auth_page)
        page.open()
        assert page.is_on_page()
        assert auth_page.locator("#print_visits").is_visible(), \
            "Generate visits PDF button must be visible"

    def test_smoke_users_page_loads(self, auth_page: Page):
        page = UsersPage(auth_page)
        page.open()
        assert page.is_on_page()
        assert auth_page.locator("#all_users").is_visible(), \
            "Users table must be visible"

    def test_smoke_sidebar_all_links_present(self, dashboard_page):
        for label, locator in [
            ("Dashboard",  NavBar.MENU_DASHBOARD_LINK),
            ("Patients",   NavBar.MENU_PATIENTS_LINK),
            ("Medicines",  NavBar.MENU_MEDICINES_LINK),
            ("Reports",    NavBar.MENU_REPORTS_LINK),
            ("Users",      NavBar.MENU_USERS_LINK),
            ("Logout",     NavBar.LOGOUT_LINK),
        ]:
            assert dashboard_page.page.locator(locator).is_visible(), \
                f"Sidebar link '{label}' must be visible"

    def test_smoke_logout_works(self, auth_page: Page):
        page = DashboardPage(auth_page)
        page.logout()
        assert "index.php" in auth_page.url or auth_page.url.endswith("/"), \
            "Should be on login page after logout"