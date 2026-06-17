# =============================================================================
# tests/test_functional.py  — Playwright version
# Per-module feature coverage — run daily: pytest -m functional
# =============================================================================
import pytest
import uuid
from playwright.sync_api import Page

from pages.patients_page import PatientsPage
from pages.medicines_page import MedicinesPage
from pages.medicine_details_page import MedicineDetailsPage
from pages.patient_history_page import PatientHistoryPage
from pages.reports_page import ReportsPage
from pages.users_page import UsersPage
from locators.locators import (
    PatientsPage as PL, MedicinesPage as ML,
    MedicineDetailsPage as MDL, ReportsPage as RL, UsersPage as UL
)
from test_data.test_data import (
    LoginData, PatientData, MedicineData,
    MedicineDetailData, ReportData
)
from utils.config import Config

def unique(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:6].upper()}"

# ==============================================================================
# LOGIN
# ==============================================================================

@pytest.mark.functional
class TestFunctionalLogin:

    def test_valid_credentials_redirect_to_dashboard(self, login_page):
        login_page.open()
        login_page.login_as_admin()
        login_page.page.wait_for_url("**/dashboard.php", timeout=Config.TIMEOUT)
        assert "dashboard.php" in login_page.page.url

    def test_invalid_username_shows_error(self, login_page):
        login_page.open()
        login_page.login(LoginData.INVALID_USERNAME, LoginData.VALID_PASSWORD)
        assert login_page.is_on_login_page()
        assert login_page.is_error_displayed()

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

    def test_logout_ends_session(self, auth_page: Page):
        from pages.dashboard_page import DashboardPage
        from locators.locators import URLs
        DashboardPage(auth_page).logout()
        auth_page.goto(URLs.DASHBOARD, wait_until="domcontentloaded",
                       timeout=Config.TIMEOUT)
        auth_page.wait_for_url("**/index.php", timeout=Config.TIMEOUT)
        assert "index.php" in auth_page.url or auth_page.url.endswith("/")

# ==============================================================================
# PATIENTS
# ==============================================================================

@pytest.mark.functional
class TestFunctionalPatients:

    def test_add_patient_valid_data_appears_in_table(self, auth_page: Page):
        page = PatientsPage(auth_page)
        page.open()
        name = unique("FuncPatient")
        page.add_patient(name, "Test Address", "123456", "1990-01-01", "09171234567", "Male")
        auth_page.wait_for_load_state("domcontentloaded")
        assert page.is_patient_in_table(name)

    def test_add_patient_empty_name_stays_on_page(self, patients_page):
        patients_page.add_patient("", "Address", "111", "1990-01-01", "09170000000", "Female")
        assert patients_page.is_on_page()

    def test_patient_table_has_all_columns(self, patients_page):
        for i, col in enumerate(
            ["S.No", "Patient Name", "Address", "CNIC",
             "Date Of Birth", "Phone Number", "Gender", "Action"], start=1
        ):
            text = patients_page.page.locator(
                f"#all_patients thead th:nth-child({i})"
            ).text_content()
            assert col.lower() in text.lower()

    def test_search_filters_to_matching_patient(self, patients_page):
        patients_page.search_patient(PatientData.EXISTING_NAME)
        assert patients_page.is_patient_in_table(PatientData.EXISTING_NAME)

    def test_search_nonexistent_returns_zero_rows(self, patients_page):
        patients_page.search_patient("XYZNOTEXIST999")
        patients_page.page.wait_for_timeout(500)
        assert patients_page.get_row_count() == 1

    def test_all_export_buttons_visible(self, patients_page):
        for label, locator in [
            ("Copy", PL.BTN_COPY), ("CSV", PL.BTN_CSV),
            ("Excel", PL.BTN_EXCEL), ("PDF", PL.BTN_PDF), ("Print", PL.BTN_PRINT),
        ]:
            assert patients_page.page.locator(locator).is_visible(), \
                f"'{label}' button should be visible"

# ==============================================================================
# MEDICINES
# ==============================================================================

@pytest.mark.functional
class TestFunctionalMedicines:

    def test_add_medicine_valid_name_appears_in_table(self, auth_page: Page):
        page = MedicinesPage(auth_page)
        page.open()
        name = unique("FuncMed")
        page.add_medicine(name)
        auth_page.wait_for_load_state("domcontentloaded")
        assert page.is_medicine_in_table(name)

    def test_add_medicine_empty_name_stays_on_page(self, medicines_page):
        medicines_page.add_medicine(MedicineData.EMPTY_NAME)
        assert medicines_page.is_on_page()

    def test_search_filters_medicines(self, medicines_page):
        medicines_page.search_medicine(MedicineData.EXISTING)
        assert medicines_page.is_medicine_in_table(MedicineData.EXISTING)

    def test_seeded_medicines_are_in_table(self, medicines_page):
        for name in ["Amoxicillin", "Losartan", "Mefenamic"]:
            medicines_page.search_medicine(name)
            medicines_page.page.wait_for_timeout(400)
            assert medicines_page.is_medicine_in_table(name)

# ==============================================================================
# MEDICINE DETAILS
# ==============================================================================

@pytest.mark.functional
class TestFunctionalMedicineDetails:

    def test_add_medicine_detail_valid_data(self, medicine_details_page):
        medicine_details_page.add_medicine_detail(
            MedicineDetailData.MEDICINE, MedicineDetailData.PACKING
        )
        medicine_details_page.page.wait_for_load_state("domcontentloaded")
        assert medicine_details_page.get_row_count() >= 1

    def test_medicine_details_table_columns(self, medicine_details_page):
        for i, col in enumerate(["S.No", "Medicine Name", "Packing", "Action"], start=1):
            text = medicine_details_page.page.locator(
                f"#medicine_details thead th:nth-child({i})"
            ).text_content()
            assert col.lower() in text.lower()

    def test_search_filters_medicine_details(self, medicine_details_page):
        medicine_details_page.search(MedicineDetailData.MEDICINE)
        medicine_details_page.page.wait_for_timeout(500)
        assert medicine_details_page.get_row_count() >= 1

    def test_medicine_dropdown_contains_seeded_options(self, medicine_details_page):
        options = medicine_details_page.page.locator(
            f"{MDL.MEDICINE_SELECT} option"
        ).all_text_contents()
        assert any("Amoxicillin" in o for o in options)

# ==============================================================================
# PATIENT HISTORY
# ==============================================================================

@pytest.mark.functional
class TestFunctionalPatientHistory:

    def test_page_loads_with_search_form(self, patient_history_page):
        assert patient_history_page.is_on_page()
        from locators.locators import PatientHistoryPage as PHL
        assert patient_history_page.page.locator(PHL.PATIENT_SELECT).is_visible()
        assert patient_history_page.page.locator(PHL.SEARCH_BTN).is_visible()

    def test_search_without_patient_stays_on_page(self, patient_history_page):
        patient_history_page.click_search()
        assert patient_history_page.is_on_page()

    def test_history_table_has_all_columns(self, patient_history_page):
        for i, col in enumerate(
            ["S.No", "Visit Date", "Disease", "Medicine",
             "Packing", "QTY", "Dosage", "Instruction", "Action"], start=1
        ):
            text = patient_history_page.page.locator(
                f"#patient_history thead th:nth-child({i})"
            ).text_content()
            assert col.lower() in text.lower()

# ==============================================================================
# REPORTS
# ==============================================================================

@pytest.mark.functional
class TestFunctionalReports:

    def test_page_loads_with_both_sections(self, reports_page):
        assert reports_page.is_visits_section_displayed()
        assert reports_page.is_disease_section_displayed()

    def test_visits_report_all_fields_present(self, reports_page):
        for label, locator in [
            ("From date", RL.PATIENTS_FROM), ("To date", RL.PATIENTS_TO),
            ("Generate PDF", RL.GENERATE_VISITS_PDF),
        ]:
            assert reports_page.page.locator(locator).is_visible()

    def test_disease_report_all_fields_present(self, reports_page):
        for label, locator in [
            ("Disease", RL.DISEASE_INPUT), ("From date", RL.DISEASE_FROM),
            ("To date", RL.DISEASE_TO), ("Generate PDF", RL.GENERATE_DISEASE_PDF),
        ]:
            assert reports_page.page.locator(locator).is_visible()

# ==============================================================================
# USERS
# ==============================================================================

@pytest.mark.functional
class TestFunctionalUsers:

    def test_add_user_valid_data_appears_in_table(self, auth_page: Page):
        page = UsersPage(auth_page)
        page.open()
        uid = unique("funcuser").lower()
        page.add_user(f"Func User {uid}", uid[:15], "funcpass123")
        auth_page.wait_for_load_state("domcontentloaded")
        assert page.get_row_count() >= 1

    def test_add_user_empty_username_stays_on_page(self, users_page):
        users_page.add_user("Display Name", "", "somepassword")
        assert users_page.is_on_page()

    def test_add_user_empty_password_stays_on_page(self, users_page):
        users_page.add_user("Display Name", "someuser", "")
        assert users_page.is_on_page()

    def test_users_table_has_all_columns(self, users_page):
        for i, col in enumerate(
            ["S.No", "Picture", "Display Name", "Username", "Action"], start=1
        ):
            text = users_page.page.locator(
                f"#all_users thead th:nth-child({i})"
            ).text_content()
            assert col.lower() in text.lower()

    def test_seeded_admin_user_exists(self, users_page):
        rows = users_page.page.locator("#all_users tbody tr").all_text_contents()
        assert any("admin" in r.lower() for r in rows)