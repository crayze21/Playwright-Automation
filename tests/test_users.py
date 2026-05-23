# =============================================================================
# tests/test_users.py  — Playwright version
# =============================================================================
import pytest
import uuid
from playwright.sync_api import Page

from pages.users_page import UsersPage
from locators.locators import UsersPage as UL
from test_data.test_data import UserData

class TestUsers:

    def test_users_page_loads(self, users_page):
        assert users_page.is_on_page()
        assert "User" in users_page.get_heading()

    def test_add_user_form_fields_visible(self, users_page):
        for label, locator in [
            ("Display Name", UL.DISPLAY_NAME),
            ("Username",     UL.USERNAME),
            ("Password",     UL.PASSWORD),
            ("Profile Pic",  UL.PROFILE_PIC),
            ("Save Button",  UL.SAVE_BTN),
        ]:
            assert users_page.page.locator(locator).is_visible(), \
                f"'{label}' should be visible"

    def test_add_user_valid_data(self, auth_page: Page):
        page = UsersPage(auth_page)
        page.open()
        uid = uuid.uuid4().hex[:6].lower()
        page.add_user(f"Test User {uid}", f"testuser_{uid}", "testpass123")
        auth_page.wait_for_load_state("domcontentloaded")
        assert page.get_row_count() >= 1

    def test_add_user_empty_username_stays_on_page(self, users_page):
        users_page.add_user("Display Name", "", "somepassword")
        assert users_page.is_on_page()

    def test_add_user_empty_password_stays_on_page(self, users_page):
        users_page.add_user("Display Name", "someuser", "")
        assert users_page.is_on_page()

    def test_users_table_has_correct_columns(self, users_page):
        for i, col in enumerate(
            ["S.No", "Picture", "Display Name", "Username", "Action"], start=1
        ):
            text = users_page.page.locator(
                f"#all_users thead th:nth-child({i})"
            ).text_content()
            assert col.lower() in text.lower()

    def test_seeded_admin_user_exists(self, users_page):
        rows = users_page.page.locator("#all_users tbody tr").all_text_contents()
        assert any("admin" in r.lower() for r in rows), \
            "Admin user should exist in the users table"

    def test_all_users_heading_visible(self, users_page):
        assert users_page.page.locator(
            "h3:has-text('All Users')"
        ).is_visible()