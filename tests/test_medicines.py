# =============================================================================
# tests/test_medicines.py  — Playwright version
# =============================================================================

import pytest
import uuid
from playwright.sync_api import Page

from pages.medicines_page import MedicinesPage
from locators.locators import MedicinesPage as ML
from test_data.test_data import MedicineData


class TestMedicines:

    def test_medicines_page_loads(self, medicines_page):
        assert medicines_page.is_on_page()
        assert "Medicine" in medicines_page.get_heading()

    def test_add_medicine_valid_name_appears_in_table(self, auth_page: Page):
        page = MedicinesPage(auth_page)
        page.open()
        name = f"TestMed_{uuid.uuid4().hex[:6].upper()}"
        page.add_medicine(name)
        auth_page.wait_for_load_state("domcontentloaded")
        assert page.is_medicine_in_table(name)

    def test_add_medicine_empty_name_stays_on_page(self, medicines_page):
        medicines_page.add_medicine(MedicineData.EMPTY_NAME)
        assert medicines_page.is_on_page()

    def test_medicines_table_has_correct_columns(self, medicines_page):
        for i, col in enumerate(["S.No", "Medicine Name", "Action"], start=1):
            text = medicines_page.page.locator(
                f"#all_medicines thead th:nth-child({i})"
            ).text_content()
            assert col.lower() in text.lower()

    def test_search_filters_medicines(self, medicines_page):
        medicines_page.search_medicine(MedicineData.EXISTING)
        assert medicines_page.is_medicine_in_table(MedicineData.EXISTING)

    def test_seeded_medicines_exist_in_table(self, medicines_page):
        for name in ["Amoxicillin", "Losartan", "Mefenamic"]:
            medicines_page.search_medicine(name)
            medicines_page.page.wait_for_timeout(400)
            assert medicines_page.is_medicine_in_table(name), \
                f"Seeded medicine '{name}' should exist"

    def test_add_medicine_form_fields_present(self, medicines_page):
        assert medicines_page.page.locator(ML.MEDICINE_NAME).is_visible()
        assert medicines_page.page.locator(ML.SAVE_BTN).is_visible()

    def test_page_info_shows_entry_count(self, medicines_page):
        info = medicines_page.get_page_info_text()
        assert "entries" in info.lower()
