# =============================================================================
# pages/base_page.py  — Playwright version
# =============================================================================
# KEY DIFFERENCE FROM SELENIUM:
#   Selenium: driver.find_element(By.ID, "x").click()
#   Playwright: page.locator("#x").click()   ← auto-waits, no WebDriverWait needed
# =============================================================================
import time
import logging
from playwright.sync_api import Page, expect

from locators.locators import NavBar, URLs
from utils.config import Config
from utils.logger import get_logger

logger = get_logger(__name__)

class BasePage:
    """
    Parent class for all Playwright Page Objects.
    page.locator() auto-waits for elements — no explicit waits needed
    for standard interactions.
    """

    def __init__(self, page: Page):
        self.page    = page
        self.timeout = Config.TIMEOUT   # default timeout in ms

    # ── Navigation ─────────────────────────────────────────────────────────────

    def go_to(self, url: str, retries: int = 3) -> None:
        """Navigate with retry — handles slow shared hosting."""
        for attempt in range(1, retries + 1):
            try:
                logger.info(f"Navigating to: {url}  (attempt {attempt}/{retries})")
                # wait_until='domcontentloaded' = Playwright's equivalent of
                # Selenium's 'eager' page load strategy
                self.page.goto(url, wait_until="domcontentloaded",
                               timeout=self.timeout)
                logger.info(f"Page loaded: {url}")
                return
            except Exception as e:
                logger.warning(f"Navigation timeout attempt {attempt}: {e}")
                if attempt == retries:
                    raise
                time.sleep(3)

    def get_current_url(self) -> str:
        return self.page.url

    def get_page_title(self) -> str:
        return self.page.title()

    def refresh(self) -> None:
        self.page.reload(wait_until="domcontentloaded")

    # ── Select2 helper — the #1 Playwright advantage over Selenium ─────────────

    def select2_option(self, trigger_css: str, search_css: str,
                       option_text: str) -> None:
        """
        Handle any Select2 dropdown.
        Playwright's auto-wait means no time.sleep() or JS click hacks needed.
        """
        # Click the trigger to open the dropdown
        self.page.locator(trigger_css).click()

        # Type into the search box — Playwright waits for it automatically
        search = self.page.locator(search_css)
        search.wait_for(state="visible", timeout=self.timeout)
        search.fill(option_text)

        # Wait for results (searching state disappears automatically)
        # Then click the matching option
        option = self.page.locator(
            f"li.select2-results__option:not(.select2-results__option--disabled)"
            f":has-text('{option_text}')"
        )
        option.first.wait_for(state="visible", timeout=self.timeout)
        option.first.click()
        logger.info(f"Select2 option selected: {option_text}")

    def set_date(self, selector: str, date_value: str) -> None:
        """
        Set a native <input type='date'> field via JavaScript.
        date_value MUST be in YYYY-MM-DD format — e.g. '2026-04-23'
        The browser will display it as dd/mm/yyyy automatically.

        We use JS because Playwright's fill() rejects DD/MM/YYYY as
        'Malformed value' on native date inputs — they always store YYYY-MM-DD.
        """
        self.page.evaluate(
            """([selector, value]) => {
                const el = document.querySelector(selector);
                if (el) {
                    const nativeInputValueSetter = Object.getOwnPropertyDescriptor(
                        window.HTMLInputElement.prototype, 'value'
                    ).set;
                    nativeInputValueSetter.call(el, value);
                    el.dispatchEvent(new Event('input', {bubbles: true}));
                    el.dispatchEvent(new Event('change', {bubbles: true}));
                }
            }""",
            [selector, date_value]
        )
        logger.debug(f"Date set via JS: {date_value} → {selector}")

    # ── Sidebar navigation ─────────────────────────────────────────────────────

    def go_to_new_prescription(self) -> None:
        self.page.locator(NavBar.MENU_PATIENTS_LINK).click()
        self.page.locator(NavBar.SUBMENU_NEW_RX).click()

    def go_to_add_patients(self) -> None:
        self.page.locator(NavBar.MENU_PATIENTS_LINK).click()
        self.page.locator(NavBar.SUBMENU_PATIENTS).click()

    def go_to_patient_history(self) -> None:
        self.page.locator(NavBar.MENU_PATIENTS_LINK).click()
        self.page.locator(NavBar.SUBMENU_HISTORY).click()

    def go_to_add_medicine(self) -> None:
        self.page.locator(NavBar.MENU_MEDICINES_LINK).click()
        self.page.locator(NavBar.SUBMENU_ADD_MED).click()

    def go_to_medicine_details(self) -> None:
        self.page.locator(NavBar.MENU_MEDICINES_LINK).click()
        self.page.locator(NavBar.SUBMENU_MED_DETAILS).click()

    def go_to_reports(self) -> None:
        self.page.locator(NavBar.MENU_REPORTS_LINK).click()
        self.page.locator(NavBar.SUBMENU_REPORTS).click()

    def go_to_users(self) -> None:
        self.page.locator(NavBar.MENU_USERS_LINK).click()

    def logout(self) -> None:
        self.page.locator(NavBar.LOGOUT_LINK).click()
        self.page.wait_for_url("**/index.php", timeout=self.timeout)
        logger.info("Logged out")

    def get_welcome_text(self) -> str:
        return self.page.locator(NavBar.WELCOME_TEXT).text_content()

    def is_logged_in(self) -> bool:
        try:
            return "Welcome" in self.page.locator(NavBar.WELCOME_TEXT).text_content()
        except Exception:
            return False