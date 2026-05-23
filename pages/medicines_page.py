# =============================================================================
# pages/medicines_page.py  — Playwright version
# =============================================================================
from pages.base_page import BasePage
from locators.locators import MedicinesPage as L, URLs
from utils.logger import get_logger
from utils.test_step import step

logger = get_logger(__name__)

class MedicinesPage(BasePage):

    def open(self) -> "MedicinesPage":
        self.go_to(URLs.MEDICINES)
        self.page.locator(L.TABLE).wait_for(timeout=self.timeout)
        return self

    def get_heading(self) -> str:
        return self.page.locator(L.PAGE_HEADING).text_content()

    def is_on_page(self) -> bool:
        return "medicines.php" in self.page.url

    def enter_medicine_name(self, name: str) -> "MedicinesPage":
        self.page.locator(L.MEDICINE_NAME).fill(name)
        return self

    def click_save(self) -> None:
        self.page.locator(L.SAVE_BTN).click()

    def add_medicine(self, name: str) -> None:
        logger.info(f"Adding medicine: {name}")
        with step("Enter medicine name"):
            self.page.locator(L.MEDICINE_NAME).fill(name)
        with step("Click Save"):
            self.page.locator(L.SAVE_BTN).click()

    def search_medicine(self, keyword: str) -> None:
        self.page.locator(L.SEARCH_INPUT).fill(keyword)
        self.page.wait_for_timeout(500)

    def get_row_count(self) -> int:
        return self.page.locator(f"{L.TABLE} tbody tr").count()

    def get_page_info_text(self) -> str:
        return self.page.locator(L.PAGE_INFO).text_content()

    def is_medicine_in_table(self, name: str) -> bool:
        self.search_medicine(name)
        self.page.wait_for_timeout(500)
        cells = self.page.locator(f"{L.TABLE} tbody tr td:nth-child(2)")
        for i in range(cells.count()):
            if name.lower() in cells.nth(i).text_content().lower():
                return True
        return False