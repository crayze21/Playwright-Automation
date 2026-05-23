# =============================================================================
# pages/new_prescription_page.py  — Playwright version
# =============================================================================
# KEY WIN over Selenium: Select2 dropdowns work with plain .click() and .fill()
# No JS click hacks, no spinner waits, no StaleElementException.
# =============================================================================
from playwright.sync_api import Page

from pages.base_page import BasePage
from locators.locators import NewPrescriptionPage as L, URLs
from utils.logger import get_logger
from utils.test_step import step

logger = get_logger(__name__)

class NewPrescriptionPage(BasePage):

    def open(self) -> "NewPrescriptionPage":
        self.go_to(URLs.NEW_PRESCRIPTION)
        self.page.locator(L.VISIT_DATE).wait_for(timeout=self.timeout)
        return self

    def get_heading(self) -> str:
        return self.page.locator(L.PAGE_HEADING).text_content()

    def is_on_page(self) -> bool:
        return "new_prescription.php" in self.page.url

    # ── Patient Select2 ────────────────────────────────────────────────────────

    def select_patient(self, patient_name: str) -> "NewPrescriptionPage":
        """
        Select2 with Playwright — no JS click, no sleep, no spinner wait.
        Playwright auto-waits for every step.
        """
        self.select2_option(
            trigger_css=L.PATIENT_S2_TRIGGER,
            search_css=L.PATIENT_SEARCH,
            option_text=patient_name
        )
        return self

    # ── Visit fields ───────────────────────────────────────────────────────────

    def set_visit_date(self, date_str: str) -> "NewPrescriptionPage":
        #self.set_date(L.VISIT_DATE, date_str)
        self.page.locator(L.VISIT_DATE).fill(date_str)
        return self

    def set_next_visit_date(self, date_str: str) -> "NewPrescriptionPage":
        #self.set_date(L.NEXT_VISIT_DATE, date_str)
        self.page.locator(L.NEXT_VISIT_DATE).fill(date_str)
        return self

    def enter_bp(self, bp: str) -> "NewPrescriptionPage":
        self.page.locator(L.BP_INPUT).fill(bp)
        return self

    def enter_weight(self, weight: str) -> "NewPrescriptionPage":
        self.page.locator(L.WEIGHT_INPUT).fill(weight)
        return self

    def enter_disease(self, disease: str) -> "NewPrescriptionPage":
        self.page.locator(L.DISEASE_INPUT).fill(disease)
        return self

    # ── Medicine rows ──────────────────────────────────────────────────────────

    def click_add_row(self) -> "NewPrescriptionPage":
        self.page.locator(L.ADD_ROW_BTN).click()
        self.page.wait_for_timeout(300)
        return self

    def get_row_count(self) -> int:
        return self.page.locator(f"{L.MEDICATION_TBODY} tr").count()

    def fill_medicine_row(self, row_index: int, medicine: str,
                          frequency: str, timing: str,
                          qty: str, dosage: str) -> None:
        """
        Fill a medicine row — Playwright version.
        No JS click needed for Select2. No StaleElementException.
        row_index is 1-based.
        """
        row = self.page.locator(f"{L.MEDICATION_TBODY} tr").nth(row_index - 1)

        # Select2 — click the trigger inside this specific row
        row.locator(".select2-selection").click()

        # Type in the global Select2 search input
        search = self.page.locator(L.MEDICINE_SEARCH)
        search.wait_for(state="visible", timeout=self.timeout)
        search.fill(medicine)

        # Wait for and click the matching option
        option = self.page.locator(
            f"li.select2-results__option:not(.select2-results__option--disabled)"
            f":has-text('{medicine}')"
        )
        option.first.wait_for(state="visible", timeout=self.timeout)
        option.first.click()
        logger.info(f"Medicine selected: {medicine}")

        # Frequency — native <select>
        row.locator("select").nth(0).select_option(label=frequency)

        # Timing — native <select>
        row.locator("select").nth(1).select_option(label=timing)

        # QTY
        row.locator("[name='qty[]']").fill(qty)

        # Dosage
        row.locator("[name='dosage[]']").fill(dosage)

        logger.info(
            f"Row {row_index} filled: {medicine} | {frequency} | {timing} | {qty} | {dosage}"
        )

    def delete_medicine_row(self, row_index: int) -> None:
        row = self.page.locator(f"{L.MEDICATION_TBODY} tr").nth(row_index - 1)
        row.locator("button").click()
        self.page.wait_for_timeout(200)

    # ── Submit ─────────────────────────────────────────────────────────────────

    def click_save_prescription(self) -> None:
        self.page.locator(L.SAVE_BTN).click()
        logger.info("Save Prescription clicked")