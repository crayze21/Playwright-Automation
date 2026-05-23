# =============================================================================
# pages/reports_page.py  — Playwright version
# =============================================================================

from pages.base_page import BasePage
from locators.locators import ReportsPage as L, URLs
from utils.logger import get_logger

logger = get_logger(__name__)


class ReportsPage(BasePage):

    def open(self) -> "ReportsPage":
        self.go_to(URLs.REPORTS)
        self.page.locator(L.PATIENTS_FROM).wait_for(timeout=self.timeout)
        return self

    def get_heading(self) -> str:
        return self.page.locator(L.PAGE_HEADING).text_content()

    def is_on_page(self) -> bool:
        return "reports.php" in self.page.url

    def set_visits_from_date(self, date_str: str) -> "ReportsPage":
        self.set_date(L.PATIENTS_FROM, date_str)
        return self

    def set_visits_to_date(self, date_str: str) -> "ReportsPage":
        self.set_date(L.PATIENTS_TO, date_str)
        return self

    def click_generate_visits_pdf(self) -> None:
        self.page.locator(L.GENERATE_VISITS_PDF).click()

    def generate_visits_report(self, from_date: str, to_date: str) -> None:
        self.set_visits_from_date(from_date)
        self.set_visits_to_date(to_date)
        self.click_generate_visits_pdf()

    def enter_disease(self, disease: str) -> "ReportsPage":
        self.page.locator(L.DISEASE_INPUT).fill(disease)
        return self

    def set_disease_from_date(self, date_str: str) -> "ReportsPage":
        self.set_date(L.DISEASE_FROM, date_str)
        return self

    def set_disease_to_date(self, date_str: str) -> "ReportsPage":
        self.set_date(L.DISEASE_TO, date_str)
        return self

    def click_generate_disease_pdf(self) -> None:
        self.page.locator(L.GENERATE_DISEASE_PDF).click()

    def generate_disease_report(self, disease: str, from_date: str, to_date: str) -> None:
        self.enter_disease(disease)
        self.set_disease_from_date(from_date)
        self.set_disease_to_date(to_date)
        self.click_generate_disease_pdf()

    def is_visits_section_displayed(self) -> bool:
        return self.page.locator(L.VISITS_HEADING).is_visible()

    def is_disease_section_displayed(self) -> bool:
        return self.page.locator(L.DISEASE_HEADING).is_visible()
