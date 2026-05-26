# =============================================================================
# tests/test_regression.py  — Playwright version
# Edge cases and boundary conditions — run before releases: pytest -m regression
# =============================================================================
import pytest
import uuid
from playwright.sync_api import Page

from pages.patients_page import PatientsPage
from pages.medicines_page import MedicinesPage
from pages.new_prescription_page import NewPrescriptionPage
from pages.dashboard_page import DashboardPage
from locators.locators import URLs
from utils.config import Config

def unique(prefix):
    return f"{prefix}_{uuid.uuid4().hex[:6].upper()}"

# ==============================================================================
# SESSION & SECURITY
# ==============================================================================

@pytest.mark.regression
class TestRegressionSession:

    def test_accessing_dashboard_without_login_redirects(self, page: Page):
        """Unauthenticated request to dashboard.php must redirect to login."""
        page.set_default_timeout(Config.TIMEOUT)
        page.goto(URLs.DASHBOARD, wait_until="domcontentloaded", timeout=Config.TIMEOUT)
        page.wait_for_url("**/index.php", timeout=Config.TIMEOUT)
        assert "index.php" in page.url or page.url.endswith("/")

    def test_accessing_patients_without_login_redirects(self, page: Page):
        page.set_default_timeout(Config.TIMEOUT)
        page.goto(URLs.PATIENTS, wait_until="domcontentloaded", timeout=Config.TIMEOUT)
        page.wait_for_url("**/index.php", timeout=Config.TIMEOUT)
        assert "index.php" in page.url or page.url.endswith("/")

    def test_accessing_users_without_login_redirects(self, page: Page):
        page.set_default_timeout(Config.TIMEOUT)
        page.goto(URLs.USERS, wait_until="domcontentloaded", timeout=Config.TIMEOUT)
        page.wait_for_url("**/index.php", timeout=Config.TIMEOUT)
        assert "index.php" in page.url or page.url.endswith("/")

    def test_session_does_not_persist_after_logout(self, auth_page: Page):
        DashboardPage(auth_page).logout()
        auth_page.go_back()
        auth_page.wait_for_timeout(1000)
        assert "dashboard.php" not in auth_page.url, \
            "Session should not be restored via browser back after logout"

    def test_page_title_on_login(self, page: Page):
        page.set_default_timeout(Config.TIMEOUT)
        page.goto(URLs.LOGIN, wait_until="domcontentloaded", timeout=Config.TIMEOUT)
        assert "Toreja" in page.title() or "Clinic" in page.title()

# ==============================================================================
# PATIENTS — EDGE CASES
# ==============================================================================

@pytest.mark.regression
class TestRegressionPatients:

    def test_patient_name_with_special_characters(self, auth_page: Page):
        page = PatientsPage(auth_page)
        page.open()
        name = f"O'Brien-{uuid.uuid4().hex[:4].upper()}"
        page.add_patient(name, "Test St", "REG001", "10/03/1985", "09170000001", "Male")
        auth_page.wait_for_load_state("domcontentloaded")
        # Check partial match — apostrophe may be encoded differently
        assert page.is_patient_in_table("O'Brien") or \
               page.is_patient_in_table("Brien"), \
               f"Patient with special chars '{name}' should be saved"

    def test_patient_search_is_case_insensitive(self, patients_page):
        patients_page.search_patient("mark")
        patients_page.page.wait_for_timeout(500)
        count_lower = patients_page.get_row_count()
        patients_page.search_patient("MARK")
        patients_page.page.wait_for_timeout(500)
        count_upper = patients_page.get_row_count()
        assert count_lower == count_upper, "Search should be case-insensitive"

    def test_search_then_clear_restores_full_table(self, patients_page):
        full_count = patients_page.get_row_count()
        patients_page.search_patient("XYZNOTEXIST")
        patients_page.page.wait_for_timeout(500)
        patients_page.page.locator("#all_patients_filter input").fill("")
        patients_page.page.wait_for_timeout(500)
        assert patients_page.get_row_count() == full_count

    def test_patient_table_survives_page_refresh(self, patients_page):
        count_before = patients_page.get_row_count()
        patients_page.refresh()
        patients_page.page.locator("#all_patients").wait_for(timeout=Config.TIMEOUT)
        count_after = patients_page.get_row_count()
        assert count_after == count_before

    def test_gender_dropdown_has_correct_options(self, patients_page):
        options = patients_page.page.locator(
            "#gender option"
        ).all_text_contents()
        options = [o.strip() for o in options if o.strip()]
        for expected in ["Male", "Female", "Other"]:
            assert expected in options, \
                f"Gender option '{expected}' must be present"

# ==============================================================================
# MEDICINES — EDGE CASES
# ==============================================================================

@pytest.mark.regression
class TestRegressionMedicines:

    def test_medicine_name_with_numbers(self, auth_page: Page):
        page = MedicinesPage(auth_page)
        page.open()
        name = f"Med500mg_{uuid.uuid4().hex[:4].upper()}"
        page.add_medicine(name)
        auth_page.wait_for_load_state("domcontentloaded")
        assert page.is_medicine_in_table(name)

    def test_medicine_search_then_clear_restores_all(self, medicines_page):
        full_count = medicines_page.get_row_count()
        medicines_page.search_medicine("ZZZNOTEXIST")
        medicines_page.page.wait_for_timeout(500)
        medicines_page.page.locator("#all_medicines_filter input").fill("")
        medicines_page.page.wait_for_timeout(500)
        assert medicines_page.get_row_count() == full_count

    def test_partial_search_matches_multiple(self, medicines_page):
        medicines_page.search_medicine("Anti")
        medicines_page.page.wait_for_timeout(500)
        assert medicines_page.get_row_count() >= 2, \
            "Searching 'Anti' should match Antibiotic and Antihistamine"

# ==============================================================================
# PRESCRIPTION — EDGE CASES
# ==============================================================================

@pytest.mark.regression
class TestRegressionPrescription:

    def test_save_without_patient_stays_on_page(self, new_prescription_page):
        new_prescription_page.enter_disease("Regression Test Disease")
        new_prescription_page.set_visit_date("23/04/2026")
        new_prescription_page.click_save_prescription()
        assert new_prescription_page.is_on_page()

    def test_multiple_medicine_rows_can_be_added(self, new_prescription_page):
        for _ in range(3):
            new_prescription_page.click_add_row()
            new_prescription_page.page.wait_for_timeout(300)
        assert new_prescription_page.get_row_count() >= 3

    def test_delete_row_reduces_count(self, new_prescription_page):
        new_prescription_page.click_add_row()
        new_prescription_page.page.wait_for_timeout(300)
        new_prescription_page.click_add_row()
        new_prescription_page.page.wait_for_timeout(300)
        count_before = new_prescription_page.get_row_count()
        new_prescription_page.delete_medicine_row(count_before)
        new_prescription_page.page.wait_for_timeout(300)
        assert new_prescription_page.get_row_count() == count_before - 1

# ==============================================================================
# NAVIGATION — REGRESSION
# ==============================================================================

@pytest.mark.regression
class TestRegressionNavigation:

    def test_all_menu_links_navigate_correctly(self, auth_page: Page):
        from locators.locators import NavBar
        dashboard = DashboardPage(auth_page)

        expected = [
            (dashboard.go_to_add_patients,     "patients.php"),
            (dashboard.go_to_new_prescription, "new_prescription.php"),
            (dashboard.go_to_patient_history,  "patient_history.php"),
            (dashboard.go_to_add_medicine,     "medicines.php"),
            (dashboard.go_to_medicine_details, "medicine_details.php"),
            (dashboard.go_to_reports,          "reports.php"),
            (dashboard.go_to_users,            "users.php"),
        ]

        for nav_action, expected_url in expected:
            auth_page.goto(URLs.DASHBOARD, wait_until="domcontentloaded",
                           timeout=Config.TIMEOUT)
            auth_page.locator("aside.main-sidebar").wait_for(timeout=Config.TIMEOUT)
            nav_action()
            auth_page.wait_for_url(f"**/{expected_url}", timeout=Config.TIMEOUT)
            assert expected_url in auth_page.url, \
                f"Navigation to '{expected_url}' failed, got: {auth_page.url}"

    def test_footer_copyright_text_present(self, dashboard_page):
        footer = dashboard_page.page.locator("footer.main-footer").text_content()
        assert "2026" in footer or "Clinic" in footer

    def test_brand_logo_links_to_dashboard(self, auth_page: Page):
        from locators.locators import NavBar
        auth_page.goto(URLs.PATIENTS, wait_until="domcontentloaded",
                       timeout=Config.TIMEOUT)
        auth_page.locator("aside.main-sidebar").wait_for(timeout=Config.TIMEOUT)
        auth_page.locator(NavBar.BRAND_LINK).click()
        auth_page.wait_for_url("**/dashboard.php", timeout=Config.TIMEOUT)
        assert "dashboard.php" in auth_page.url