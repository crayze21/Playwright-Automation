# =============================================================================
# tests/test_new_prescription.py  — Playwright version
# =============================================================================

import pytest
from locators.locators import NewPrescriptionPage as L
from test_data.test_data import PrescriptionData


class TestNewPrescription:

    def test_new_prescription_page_loads(self, new_prescription_page):
        assert new_prescription_page.is_on_page()
        assert "Prescription" in new_prescription_page.get_heading()

    def test_add_row_button_adds_medicine_row(self, new_prescription_page):
        initial = new_prescription_page.get_row_count()
        new_prescription_page.click_add_row()
        assert new_prescription_page.get_row_count() == initial + 1

    def test_visit_date_field_accepts_value(self, new_prescription_page):
        new_prescription_page.set_visit_date(PrescriptionData.VISIT_DATE)
        val = new_prescription_page.page.locator(L.VISIT_DATE).get_attribute("value")
        assert val != "" and val is not None

    def test_bp_and_weight_fields_accept_input(self, new_prescription_page):
        new_prescription_page.enter_bp(PrescriptionData.BP)
        new_prescription_page.enter_weight(PrescriptionData.WEIGHT)
        assert new_prescription_page.page.locator(L.BP_INPUT).input_value() == PrescriptionData.BP
        assert new_prescription_page.page.locator(L.WEIGHT_INPUT).input_value() == PrescriptionData.WEIGHT

    def test_disease_field_accepts_input(self, new_prescription_page):
        new_prescription_page.enter_disease(PrescriptionData.DISEASE)
        assert new_prescription_page.page.locator(L.DISEASE_INPUT).input_value() == PrescriptionData.DISEASE

    def test_delete_medicine_row_reduces_count(self, new_prescription_page):
        new_prescription_page.click_add_row()
        new_prescription_page.click_add_row()
        count_before = new_prescription_page.get_row_count()
        new_prescription_page.delete_medicine_row(count_before)
        assert new_prescription_page.get_row_count() == count_before - 1

    def test_form_fields_are_present(self, new_prescription_page):
        for label, locator in [
            ("Patient Select",  L.PATIENT_SELECT),
            ("Visit Date",      L.VISIT_DATE),
            ("Next Visit Date", L.NEXT_VISIT_DATE),
            ("BP",              L.BP_INPUT),
            ("Weight",          L.WEIGHT_INPUT),
            ("Disease",         L.DISEASE_INPUT),
            ("Add Row Button",  L.ADD_ROW_BTN),
            ("Save Button",     L.SAVE_BTN),
        ]:
            assert new_prescription_page.page.locator(locator).is_visible(), \
                f"'{label}' should be visible on the prescription form"

    def test_save_without_patient_stays_on_page(self, new_prescription_page):
        new_prescription_page.set_visit_date(PrescriptionData.VISIT_DATE)
        new_prescription_page.enter_disease(PrescriptionData.DISEASE)
        new_prescription_page.click_save_prescription()
        assert new_prescription_page.is_on_page()
