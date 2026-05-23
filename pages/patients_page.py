# =============================================================================
# pages/patients_page.py  — Playwright version
# =============================================================================

from pages.base_page import BasePage
from locators.locators import PatientsPage as L, URLs
from utils.logger import get_logger
from utils.test_step import step

logger = get_logger(__name__)


class PatientsPage(BasePage):

    def open(self) -> "PatientsPage":
        self.go_to(URLs.PATIENTS)
        self.page.locator(L.TABLE).wait_for(timeout=self.timeout)
        return self

    def get_heading(self) -> str:
        return self.page.locator(L.PAGE_HEADING).text_content()

    def is_on_page(self) -> bool:
        return "patients.php" in self.page.url

    # ── Individual form field methods ──────────────────────────────────────────

    def enter_patient_name(self, name: str) -> "PatientsPage":
        self.page.locator(L.PATIENT_NAME).fill(name)
        return self

    def enter_address(self, address: str) -> "PatientsPage":
        self.page.locator(L.ADDRESS).fill(address)
        return self

    def enter_cnic(self, cnic: str) -> "PatientsPage":
        self.page.locator(L.CNIC).fill(cnic)
        return self

    def enter_date_of_birth(self, dob: str) -> "PatientsPage":
        """Set DOB via JS — bypasses custom date picker."""
        self.set_date(L.DATE_OF_BIRTH, dob)
        return self

    def enter_phone_number(self, phone: str) -> "PatientsPage":
        self.page.locator(L.PHONE_NUMBER).fill(phone)
        return self

    def select_gender(self, gender: str) -> "PatientsPage":
        self.page.locator(L.GENDER).select_option(label=gender)
        return self

    def click_save(self) -> None:
        self.page.locator(L.SAVE_BTN).click()

    # ── Bulk convenience method with step logging ──────────────────────────────

    def add_patient(self, name: str, address: str, cnic: str, dob: str, phone: str, gender: str) -> None:
        logger.info(f"Adding patient: {name}")
        with step("Enter patient name"):
            self.page.locator(L.PATIENT_NAME).fill(name)
        with step("Enter address"):
            self.page.locator(L.ADDRESS).fill(address)
        with step("Enter CNIC"):
            self.page.locator(L.CNIC).fill(cnic)
        with step("Set date of birth"):
            self.set_date(L.DATE_OF_BIRTH, dob)
        with step("Enter phone number"):
            self.page.locator(L.PHONE_NUMBER).fill(phone)
        with step("Select gender"):
            self.page.locator(L.GENDER).select_option(label=gender)
        with step("Click Save button"):
            self.page.locator(L.SAVE_BTN).click()

    # ── DataTable interactions ─────────────────────────────────────────────────

    def search_patient(self, keyword: str) -> None:
        self.page.locator(L.SEARCH_INPUT).fill(keyword)
        # Playwright waits for DOM updates automatically
        self.page.wait_for_timeout(500)

    def get_row_count(self) -> int:
        rows = self.page.locator(f"{L.TABLE} tbody tr")
        return rows.count()

    def get_page_info_text(self) -> str:
        return self.page.locator(L.PAGE_INFO).text_content()

    def is_patient_in_table(self, name: str) -> bool:
        self.search_patient(name)
        self.page.wait_for_timeout(500)
        cells = self.page.locator(f"{L.TABLE} tbody tr td:nth-child(2)")
        for i in range(cells.count()):
            if name.lower() in cells.nth(i).text_content().lower():
                return True
        return False

    def get_cell_text(self, row: int, col: int) -> str:
        return self.page.locator(
            f"{L.TABLE} tbody tr:nth-child({row}) td:nth-child({col})"
        ).text_content()
