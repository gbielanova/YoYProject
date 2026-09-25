import uuid
from time import sleep

from faker import Faker
from playwright.sync_api import Page, expect

from tests.conftest import Config


def test_register_a_user(page: Page, configs: Config):
    email = generate_unique_email(configs.domain)

    navigate_to_page(page, configs.base_url, 'me')

    expect(page.locator('[data-testid="signin-returntohint"]')).to_have_text('Після входу повернемо тебе назад.')

    fill_login_form(page, email)

    check_me_user_info(page, email, "")

    logout(page)


def test_register_to_event(page: Page, configs: Config):
    email = generate_unique_email(configs.domain)
    fake = Faker()
    first_name = fake.first_name()
    last_name = fake.last_name()

    navigate_to_page(page, configs.base_url)

    conf_name = page.locator('[data-event-card] h3').first.inner_text()

    page.locator('[data-event-card]').first.click()

    expect(page.locator('.yoy-header-title-text')).to_have_text(conf_name)

    page.locator('[data-testid="register-cta"]').click()

    fill_event_register_form(email, page, first_name, last_name)

    expect(page.locator('#sheet_confirm_view h3')).to_have_text("Готово! Твій квиток")
    expect(page.locator('[data-testid="ticket-event-title"]')).to_have_text(conf_name)

    go_to_me_page(page)
    check_me_user_info(page, email, f'{first_name} {last_name}')
    logout(page)


def fill_event_register_form(email: str, page: Page, first_name: str = '', last_name: str = ''):
    page.locator('#reg_name').fill(first_name)
    page.locator('#reg_lastname').fill(last_name)
    page.locator('#reg_email').fill(email)
    page.locator('#reg_phone').fill('+380000000000')
    page.locator('#sheet_submit_btn').click()


def check_me_user_info(page: Page, email: str, name: str):
    if name == '':
        expect(page.locator('[data-testid="me-display-name"]')).to_have_text(email)
    else:
        expect(page.locator('[data-testid="me-display-name"]')).to_have_text(name)
        expect(page.locator('[data-testid="me-display-name"] + div')).to_have_text(email)


def navigate_to_page(page: Page, base_url: str, url=''):
    page.goto(base_url + url)


def logout(page: Page):
    page.locator('[data-testid="logout-btn"]').click()


def go_to_me_page(page: Page):
    page.locator('a[href="/me"]').click()


def generate_unique_email(domain, prefix: str = "gb_test") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}@{domain}"


def fill_login_form(page: Page, email: str, code: str = "111111"):
    page.locator('[data-testid="signin-email-input"]').fill(email)
    page.locator('[data-testid="signin-otp-submit-label"]').click()

    # code validation will be failed if user wasn't reated yet
    sleep(1)

    page.locator('[data-testid="signin-code-input"]').fill(code)
    page.locator('[data-testid="signin-code-submit-label"]').click()
