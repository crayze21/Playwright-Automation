# =============================================================================
# pages/dashboard_page.py  — Playwright version
# =============================================================================

from pages.base_page import BasePage
from locators.locators import DashboardPage as L, URLs
from utils.logger import get_logger

logger = get_logger(__name__)


class DashboardPage(BasePage):

    def open(self) -> "DashboardPage":
        self.go_to(URLs.DASHBOARD)
        self.page.locator(L.PAGE_HEADING).wait_for(timeout=self.timeout)
        return self

    def get_heading(self) -> str:
        return self.page.locator(L.PAGE_HEADING).text_content()

    def is_on_dashboard(self) -> bool:
        return "dashboard.php" in self.page.url

    def get_today_count(self) -> str:
        return self.page.locator(L.COUNT_TODAY).text_content()

    def get_week_count(self) -> str:
        return self.page.locator(L.COUNT_WEEK).text_content()

    def get_month_count(self) -> str:
        return self.page.locator(L.COUNT_MONTH).text_content()

    def get_year_count(self) -> str:
        return self.page.locator(L.COUNT_YEAR).text_content()

    def is_today_box_displayed(self) -> bool:
        return self.page.locator(L.BOX_TODAY).is_visible()

    def is_week_box_displayed(self) -> bool:
        return self.page.locator(L.BOX_WEEK).is_visible()

    def is_month_box_displayed(self) -> bool:
        return self.page.locator(L.BOX_MONTH).is_visible()

    def is_year_box_displayed(self) -> bool:
        return self.page.locator(L.BOX_YEAR).is_visible()
