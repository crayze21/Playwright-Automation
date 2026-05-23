# =============================================================================
# tests/test_patients.py  — Playwright version
# =============================================================================
import pytest
import uuid
from playwright.sync_api import Page

from pages.patients_page import PatientsPage
from locators.locators import PatientsPage as PL
from test_data.test_data import PatientData
from utils.config import Config

class TestPatients:

    def test_patients_page_loads(self, patients_page):
        assert patients_page.is_on_page()
        assert "Patient" in patients_page.get_heading()

    def test_add_patient_valid_data(self, auth_page: Page):
        page = PatientsPage(auth_page)
        page.open()
        d = PatientData.VALID
        uid = uuid.uuid4().hex[:6].upper()
        name = f"{d['name']}_{uid}"
        page.add_patient(name, d["address"], d["cnic"], d["dob"], d["phone"], d["gender"])
        auth_page.wait_for_load_state("domcontentloaded")
        assert page.is_patient_in_table(name), \
            f"Patient '{name}' should appear in table after adding"

    def test_add_patient_empty_name_stays_on_page(self, patients_page):
        patients_page.add_patient("", "Address", "111", "1990-01-01", "09170000000", "Female")
        assert patients_page.is_on_page()

    def test_patients_table_has_correct_columns(self, patients_page):
        expected = [
            "S.No", "Patient Name", "Address", "CNIC",
            "Date Of Birth", "Phone Number", "Gender", "Action"
        ]
        for i, col in enumerate(expected, start=1):
            text = patients_page.page.locator(
                f"#all_patients thead th:nth-child({i})"
            ).text_content()
            assert col.lower() in text.lower(), \
                f"Column {i} should be '{col}', got '{text}'"

    def test_search_filters_to_matching_patient(self, patients_page):
        patients_page.search_patient(PatientData.EXISTING_NAME)
        assert patients_page.is_patient_in_table(PatientData.EXISTING_NAME)

    def test_search_nonexistent_returns_zero_rows(self, patients_page):
        patients_page.search_patient("XYZNOTEXIST999")
        patients_page.page.wait_for_timeout(500)
        assert patients_page.get_row_count() == 0

    def test_page_info_shows_entry_count(self, patients_page):
        info = patients_page.get_page_info_text()
        assert "entries" in info.lower()

    def test_export_buttons_visible(self, patients_page):
        for label, locator in [
            ("Copy",  PL.BTN_COPY),
            ("CSV",   PL.BTN_CSV),
            ("Excel", PL.BTN_EXCEL),
            ("PDF",   PL.BTN_PDF),
            ("Print", PL.BTN_PRINT),
        ]:
            assert patients_page.page.locator(locator).is_visible(), \
                f"'{label}' button should be visible"

    def test_add_patient_form_all_fields_present(self, patients_page):
        for label, locator in [
            ("Patient Name", PL.PATIENT_NAME),
            ("Address",      PL.ADDRESS),
            ("CNIC",         PL.CNIC),
            ("Phone Number", PL.PHONE_NUMBER),
            ("Gender",       PL.GENDER),
            ("Save Button",  PL.SAVE_BTN),
        ]:
            assert patients_page.page.locator(locator).is_visible(), \
                f"'{label}' field should be visible"