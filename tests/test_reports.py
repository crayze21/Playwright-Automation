# =============================================================================
# tests/test_reports.py  — Playwright version
# =============================================================================
import pytest
from locators.locators import ReportsPage as RL
from test_data.test_data import ReportData

class TestReports:

    def test_reports_page_loads(self, reports_page):
        assert reports_page.is_on_page()
        assert "Report" in reports_page.get_heading()

    def test_visits_section_is_visible(self, reports_page):
        assert reports_page.is_visits_section_displayed()

    def test_disease_section_is_visible(self, reports_page):
        assert reports_page.is_disease_section_displayed()

    def test_visits_form_fields_visible(self, reports_page):
        for label, locator in [
            ("From date",        RL.PATIENTS_FROM),
            ("To date",          RL.PATIENTS_TO),
            ("Generate PDF btn", RL.GENERATE_VISITS_PDF),
        ]:
            assert reports_page.page.locator(locator).is_visible(), \
                f"'{label}' should be visible"

    def test_disease_form_fields_visible(self, reports_page):
        for label, locator in [
            ("Disease input",    RL.DISEASE_INPUT),
            ("From date",        RL.DISEASE_FROM),
            ("To date",          RL.DISEASE_TO),
            ("Generate PDF btn", RL.GENERATE_DISEASE_PDF),
        ]:
            assert reports_page.page.locator(locator).is_visible(), \
                f"'{label}' should be visible"

    def test_visits_generate_btn_enabled_after_dates_filled(self, reports_page):
        reports_page.set_visits_from_date(ReportData.FROM_DATE)
        reports_page.set_visits_to_date(ReportData.TO_DATE)
        assert reports_page.page.locator(RL.GENERATE_VISITS_PDF).is_enabled()

    def test_disease_generate_btn_enabled_after_all_filled(self, reports_page):
        reports_page.enter_disease(ReportData.DISEASE)
        reports_page.set_disease_from_date(ReportData.FROM_DATE)
        reports_page.set_disease_to_date(ReportData.TO_DATE)
        assert reports_page.page.locator(RL.GENERATE_DISEASE_PDF).is_enabled()