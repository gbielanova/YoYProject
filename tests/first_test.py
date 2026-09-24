import uuid
from time import sleep

from playwright.sync_api import Page, expect


def test_register_a_user(page: Page, configs: dict):
    email = generate_unique_email(configs['domain'])

    navigate_to_page(page, configs['base_url'], 'me')

    expect(page.locator('[data-testid="signin-returntohint"]')).to_have_text('Після входу повернемо тебе назад.')

    fill_login_form(page, email)

    check_me_user_info(page, email, "")

    logout(page)


def test_register_to_event(page: Page, configs: dict):
    email = generate_unique_email(configs['domain'])

    navigate_to_page(page, configs['base_url'])

    conf_name = page.locator('[data-event-card] h3').first.inner_text()

    page.locator('[data-testid="event-card-cover-image"]').first.click()

    expect(page.locator('.yoy-header-title-text')).to_have_text(conf_name)

    page.locator('[data-testid="register-cta"]').click()

    fill_event_register_form(email, page)

    expect(page.locator('#sheet_confirm_view h3')).to_have_text("Готово! Твій квиток")
    expect(page.locator('[data-testid="ticket-event-title"]')).to_have_text(conf_name)

    # it takes some time to register a user, playwright is too fast clicking on the link
    sleep(1)

    go_to_me_page(page)
    check_me_user_info(page, email, 'Іван Петренко')
    logout(page)


def fill_event_register_form(email: str, page: Page):
    page.locator('#reg_name').fill('Іван')
    page.locator('#reg_lastname').fill('Петренко')
    page.locator('#reg_email').fill(email)
    page.locator('#reg_phone').fill('+380000000000')
    page.locator('#sheet_submit_btn').click()


def check_me_user_info(page: Page, email: str, name: str):
    if name == '':
        expect(page.locator('[data-testid="me-display-name"]')).to_have_text(email)
    else:
        expect(page.locator('[data-testid="me-display-name"]')).to_have_text(name)
        expect(page.locator('[data-testid="me-display-name"] + div')).to_have_text(email)


def navigate_to_page(page: Page, base_url:str, url=''):
    page.goto(base_url + url)


def logout(page: Page):
    page.locator('[data-testid="logout-btn"]').click()


def go_to_me_page(page: Page):
    page.locator('a[href="/me"]').click()


def generate_unique_email(domain, prefix: str = "gb_test") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}@{domain}"


def fill_login_form(page: Page, email: str):
    page.locator('[data-testid="signin-email-input"]').fill(email)
    page.locator('[data-testid="signin-otp-submit-label"]').click()

    # code validation will be failed if user wasn't reated yet
    sleep(1)

    page.locator('[data-testid="signin-code-input"]').fill('000000')
    page.locator('[data-testid="signin-code-submit-label"]').click()
