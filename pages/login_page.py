# =============================================================================
# pages/login_page.py  — Playwright version
# =============================================================================

from playwright.sync_api import Page

from pages.base_page import BasePage
from locators.locators import LoginPage as L, URLs
from utils.config import Config
from utils.logger import get_logger

logger = get_logger(__name__)


class LoginPage(BasePage):

    def open(self) -> "LoginPage":
        self.go_to(URLs.LOGIN)
        # Playwright auto-waits for the element — no explicit wait needed
        self.page.locator(L.USERNAME_INPUT).wait_for(timeout=self.timeout)
        return self

    def enter_username(self, username: str) -> "LoginPage":
        self.page.locator(L.USERNAME_INPUT).fill(username)
        return self

    def enter_password(self, password: str) -> "LoginPage":
        self.page.locator(L.PASSWORD_INPUT).fill(password)
        return self

    def click_login(self) -> None:
        self.page.locator(L.LOGIN_BUTTON).click()

    def login(self, username: str, password: str) -> None:
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
        logger.info(f"Login attempted: {username}")

    def login_as_admin(self) -> None:
        self.login(Config.USERNAME, Config.PASSWORD)

    def get_error_message(self) -> str:
        try:
            return self.page.locator(L.ERROR_MESSAGE).text_content() or ""
        except Exception:
            return ""

    def is_error_displayed(self) -> bool:
        return self.page.locator(L.ERROR_MESSAGE).is_visible()

    def is_on_login_page(self) -> bool:
        return "index.php" in self.page.url or self.page.url.endswith("/")
