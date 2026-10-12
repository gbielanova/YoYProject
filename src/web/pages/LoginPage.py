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
        self.email_error = page.get_by_test_id('signin-email-error')
        self.send_code_button = page.get_by_test_id('signin-otp-submit-label')
        self.code_input = page.get_by_test_id('signin-code-input')
        self.submit_code_button = page.get_by_test_id('signin-code-submit-label')
        self.code_submit = page.get_by_test_id('signin-code-submit')
        self.invalid_code_message = page.get_by_test_id('signin-new-code-msg')

    def open(self):
        self.page.goto('me')

    def is_loaded(self):
        expect(self.header.title).to_have_text("Увійти")
        expect(self.email_field).to_be_visible()
        expect(self.return_hint).to_have_text('Після входу повернемо тебе назад.')

    def request_code(self, email: str):
        self.email_input.fill(email)
        self.send_code_button.click()

    def request_code_and_wait_for_response(self, email: str):
        with self.page.expect_response("**/auth/email-otp/request*") as response_info:
            self.request_code(email)
        return response_info.value

    def enter_code(self, code: str):
        # work unstable without it
        sleep(1)

        self.code_input.fill(code)

    def fill_login_form(self, email: str, code: str = "111111"):
        self.request_code(email)
        self.enter_code(code)
        self.submit_code_button.click()

    def check_invalid_code_error(self):
        expect(self.invalid_code_message).to_contain_text("Код недійсний або прострочений.")

    def check_invalid_email_error(self, message: str = 'Введи справжній email.'):
        expect(self.email_error).to_have_text(message)
        expect(self.code_input).to_be_hidden()

    def check_code_step_is_opened(self):
        expect(self.code_input).to_be_visible()
        expect(self.email_error).to_be_hidden()

    def check_code_cannot_be_submitted(self, expected_value: str):
        expect(self.code_input).to_have_value(expected_value)
        expect(self.code_submit).to_be_disabled()

    def check_code_can_be_submitted(self, expected_value: str):
        expect(self.code_input).to_have_value(expected_value)
        expect(self.code_submit).to_be_enabled()
