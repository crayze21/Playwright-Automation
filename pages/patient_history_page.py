# =============================================================================
# pages/patient_history_page.py  — Playwright version
# =============================================================================

from pages.base_page import BasePage
from locators.locators import PatientHistoryPage as L, URLs
from utils.logger import get_logger

logger = get_logger(__name__)


class PatientHistoryPage(BasePage):

    def open(self) -> "PatientHistoryPage":
        self.go_to(URLs.PATIENT_HISTORY)
        self.page.locator(L.SEARCH_BTN).wait_for(timeout=self.timeout)
        return self

    def get_heading(self) -> str:
        return self.page.locator(L.PAGE_HEADING).text_content()

    def is_on_page(self) -> bool:
        return "patient_history.php" in self.page.url

    def select_patient(self, patient_name: str) -> "PatientHistoryPage":
        """Select2 — clean Playwright version, no JS hacks."""
        self.select2_option(
            trigger_css=L.PATIENT_S2_TRIGGER,
            search_css=L.PATIENT_SEARCH,
            option_text=patient_name
        )
        return self

    def click_search(self) -> None:
        self.page.locator(L.SEARCH_BTN).click()
        self.page.locator(L.HISTORY_TBODY).wait_for(timeout=self.timeout)
        logger.info("History search clicked")

    def search_patient_history(self, patient_name: str) -> None:
        self.select_patient(patient_name)
        self.click_search()
        logger.info(f"History search completed for: {patient_name}")

    def get_result_row_count(self) -> int:
        rows = self.page.locator(f"{L.TABLE} tbody tr")
        return rows.count()

    def is_table_empty(self) -> bool:
        return self.get_result_row_count() == 0

    def get_cell_text(self, row: int, col: int) -> str:
        return self.page.locator(
            f"{L.TABLE} tbody tr:nth-child({row}) td:nth-child({col})"
        ).text_content()
