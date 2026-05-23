# =============================================================================
# pages/medicine_details_page.py  — Playwright version
# =============================================================================
from pages.base_page import BasePage
from locators.locators import MedicineDetailsPage as L, URLs
from utils.logger import get_logger

logger = get_logger(__name__)

class MedicineDetailsPage(BasePage):

    def open(self) -> "MedicineDetailsPage":
        self.go_to(URLs.MEDICINE_DETAILS)
        self.page.locator(L.TABLE).wait_for(timeout=self.timeout)
        return self

    def is_on_page(self) -> bool:
        return "medicine_details.php" in self.page.url

    def get_heading(self) -> str:
        return self.page.locator(L.PAGE_HEADING).text_content()

    def select_medicine(self, medicine_name: str) -> "MedicineDetailsPage":
        self.page.locator(L.MEDICINE_SELECT).select_option(label=medicine_name)
        return self

    def enter_packing(self, packing: str) -> "MedicineDetailsPage":
        self.page.locator(L.PACKING_INPUT).fill(packing)
        return self

    def click_save(self) -> None:
        self.page.locator(L.SAVE_BTN).click()

    def add_medicine_detail(self, medicine_name: str, packing: str) -> None:
        self.select_medicine(medicine_name)
        self.enter_packing(packing)
        self.click_save()
        logger.info(f"Medicine detail added: {medicine_name} / packing: {packing}")

    def search(self, keyword: str) -> None:
        self.page.locator(L.SEARCH_INPUT).fill(keyword)
        self.page.wait_for_timeout(500)

    def get_row_count(self) -> int:
        return self.page.locator(f"{L.TABLE} tbody tr").count()

    def get_page_info_text(self) -> str:
        return self.page.locator(L.PAGE_INFO).text_content()

    def get_cell_text(self, row: int, col: int) -> str:
        return self.page.locator(
            f"{L.TABLE} tbody tr:nth-child({row}) td:nth-child({col})"
        ).text_content()