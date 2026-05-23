# =============================================================================
# tests/test_medicine_details.py  — Playwright version
# =============================================================================

import pytest
from locators.locators import MedicineDetailsPage as MDL
from test_data.test_data import MedicineDetailData


class TestMedicineDetails:

    def test_medicine_details_page_loads(self, medicine_details_page):
        assert medicine_details_page.is_on_page()
        assert "Medicine" in medicine_details_page.get_heading()

    def test_add_medicine_detail_valid_data(self, medicine_details_page):
        medicine_details_page.add_medicine_detail(
            MedicineDetailData.MEDICINE, MedicineDetailData.PACKING
        )
        medicine_details_page.page.wait_for_load_state("domcontentloaded")
        assert medicine_details_page.get_row_count() >= 1

    def test_form_fields_are_present(self, medicine_details_page):
        for label, locator in [
            ("Medicine Select", MDL.MEDICINE_SELECT),
            ("Packing Input",   MDL.PACKING_INPUT),
            ("Save Button",     MDL.SAVE_BTN),
        ]:
            assert medicine_details_page.page.locator(locator).is_visible(), \
                f"'{label}' should be visible"

    def test_medicine_details_table_present(self, medicine_details_page):
        assert medicine_details_page.page.locator(MDL.TABLE).is_visible()

    def test_table_has_correct_columns(self, medicine_details_page):
        for i, col in enumerate(["S.No", "Medicine Name", "Packing", "Action"], start=1):
            text = medicine_details_page.page.locator(
                f"#medicine_details thead th:nth-child({i})"
            ).text_content()
            assert col.lower() in text.lower()

    def test_search_medicine_details(self, medicine_details_page):
        medicine_details_page.search(MedicineDetailData.MEDICINE)
        medicine_details_page.page.wait_for_timeout(500)
        assert medicine_details_page.get_row_count() >= 1

    def test_medicine_dropdown_contains_seeded_options(self, medicine_details_page):
        options = medicine_details_page.page.locator(
            f"{MDL.MEDICINE_SELECT} option"
        ).all_text_contents()
        assert any("Amoxicillin" in o for o in options), \
            "Medicine dropdown should contain seeded medicines"
