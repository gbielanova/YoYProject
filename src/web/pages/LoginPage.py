from time import sleep

from playwright.sync_api import Page, expect

from src.web.components.Header import Header


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.header = Header(page)
        self.email_field = page.locator('#signin-email')
        self.return_hint = page.get_by_test_id('signin-returntohint')
        self.email_input = page.get_by_test_id('signin-email-input')
        self.send_code_button = page.get_by_test_id('signin-otp-submit-label')
        self.code_input = page.get_by_test_id('signin-code-input')
        self.submit_code_button = page.get_by_test_id('signin-code-submit-label')
        self.invalid_code_message = page.get_by_test_id('signin-new-code-msg')

    def open(self):
        self.page.goto('me')

    def is_loaded(self):
        expect(self.header.title).to_have_text("Увійти")
        expect(self.email_field).to_be_visible()
        expect(self.return_hint).to_have_text('Після входу повернемо тебе назад.')

    def fill_login_form(self, email: str, code: str = "111111"):
        self.email_input.fill(email)
        self.send_code_button.click()

        # work unstable without it
        sleep(1)

        self.code_input.fill(code)
        self.submit_code_button.click()

    def check_invalid_code_error(self):
        expect(self.invalid_code_message).to_contain_text("Код недійсний або прострочений.")
