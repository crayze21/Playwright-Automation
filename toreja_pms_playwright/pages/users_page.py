# =============================================================================
# pages/users_page.py  — Playwright version
# =============================================================================

from pages.base_page import BasePage
from locators.locators import UsersPage as L, URLs
from utils.logger import get_logger

logger = get_logger(__name__)


class UsersPage(BasePage):

    def open(self) -> "UsersPage":
        self.go_to(URLs.USERS)
        self.page.locator(L.TABLE).wait_for(timeout=self.timeout)
        return self

    def get_heading(self) -> str:
        return self.page.locator(L.PAGE_HEADING).text_content()

    def is_on_page(self) -> bool:
        return "users.php" in self.page.url

    def enter_display_name(self, name: str) -> "UsersPage":
        self.page.locator(L.DISPLAY_NAME).fill(name)
        return self

    def enter_username(self, username: str) -> "UsersPage":
        self.page.locator(L.USERNAME).fill(username)
        return self

    def enter_password(self, password: str) -> "UsersPage":
        self.page.locator(L.PASSWORD).fill(password)
        return self

    def click_save(self) -> None:
        self.page.locator(L.SAVE_BTN).click()

    def add_user(self, display_name: str, username: str, password: str) -> None:
        self.enter_display_name(display_name)
        self.enter_username(username)
        self.enter_password(password)
        self.click_save()
        logger.info(f"Add user submitted: {username}")

    def get_row_count(self) -> int:
        return self.page.locator(f"{L.TABLE} tbody tr").count()

    def get_cell_text(self, row: int, col: int) -> str:
        return self.page.locator(
            f"{L.TABLE} tbody tr:nth-child({row}) td:nth-child({col})"
        ).text_content()
