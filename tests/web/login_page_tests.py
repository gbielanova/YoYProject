from playwright.sync_api import Page

from src.utils.data import fake, generate_unique_email
from src.web.pages.LoginPage import LoginPage
from src.web.pages.MePage import MePage
from tests.conftest import Config


def test_register_a_user(page: Page, configs: Config):
    email = generate_unique_email(configs.domain)

    login_page = LoginPage(page)
    login_page.open()
    login_page.is_loaded()
    login_page.fill_login_form(email)

    me_page = MePage(page)
    me_page.check_user_info(email)
    me_page.logout()


def test_register_a_user_with_invalid_code(page: Page, configs: Config):
    email = generate_unique_email(configs.domain)
    code = fake.numerify('######')

    login_page = LoginPage(page)
    login_page.open()
    login_page.is_loaded()
    login_page.fill_login_form(email, code=code)

    login_page.check_invalid_code_error()
