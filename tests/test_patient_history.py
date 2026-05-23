# =============================================================================
# tests/test_patient_history.py  — Playwright version
# =============================================================================

import pytest
from locators.locators import PatientHistoryPage as L


class TestPatientHistory:

    def test_patient_history_page_loads(self, patient_history_page):
        assert patient_history_page.is_on_page()
        assert "History" in patient_history_page.get_heading()

    def test_search_section_is_visible(self, patient_history_page):
        assert patient_history_page.page.locator(
            "h3:has-text('Search Patient History')"
        ).is_visible()
        assert patient_history_page.page.locator(L.PATIENT_SELECT).is_visible()
        assert patient_history_page.page.locator(L.SEARCH_BTN).is_visible()

    def test_history_table_has_correct_columns(self, patient_history_page):
        expected = [
            "S.No", "Visit Date", "Disease", "Medicine",
            "Packing", "QTY", "Dosage", "Instruction", "Action"
        ]
        for i, col in enumerate(expected, start=1):
            text = patient_history_page.page.locator(
                f"#patient_history thead th:nth-child({i})"
            ).text_content()
            assert col.lower() in text.lower(), \
                f"Column {i} should be '{col}', got '{text}'"

    def test_search_without_patient_stays_on_page(self, patient_history_page):
        patient_history_page.click_search()
        assert patient_history_page.is_on_page()

    def test_history_table_is_present(self, patient_history_page):
        assert patient_history_page.page.locator(L.TABLE).is_visible()
