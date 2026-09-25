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


def test_register_a_user_with_invalid_code(page: Page, configs: Config):
    email = generate_unique_email(configs.domain)

    navigate_to_page(page, configs.base_url, 'me')

    expect(page.locator('[data-testid="signin-returntohint"]')).to_have_text('Після входу повернемо тебе назад.')

    fake = Faker("en_US")
    code = fake.numerify('######')

    fill_login_form(page, email, code=code)

    expect(page.locator('[data-testid="signin-new-code-msg"]')).to_have_text("Код недійсний або прострочений. Запроси новий код.")

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


def test_create_new_community(page: Page, configs: Config):
    email = generate_unique_email(configs.domain)

    navigate_to_page(page, configs.base_url, 'me')

    fill_login_form(page, email)

    expect(page.locator('[href="/communities/new"]')).to_have_text('Нова спільнота')
    page.locator('[href="/communities/new"]').click()

    fake = Faker("en_US")
    community_name = f'{fake.street_name()} community'
    community_url = fake.slug()
    community_description = fake.sentence()

    fill_community_info(community_description, community_name, community_url, page)

    assert community_url in page.url
    expect(page.locator('[data-testid="community-title"]')).to_have_text(community_name)
    expect(page.locator('[data-testid="community-title"]+div')).to_have_text(f'@{community_url}')
    expect(page.locator('[data-testid="community-description"]')).to_have_text(community_description)

    go_to_me_page(page)
    logout(page)


def fill_community_info(community_description: str, community_name: str, community_url: str, page: Page):
    page.locator('[data-testid="community-name-input"]').fill(community_name)
    page.locator('[data-testid="community-slug-input"]').fill(community_url)
    page.locator('[data-testid="community-description-input"]').fill(community_description)
    page.locator('[data-testid="community-unlisted-input"]').click()
    page.locator('[data-testid="community-create-submit"]').click()


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
    page.locator('[data-testid="signin-code-input"]').fill(code)
    page.locator('[data-testid="signin-code-submit-label"]').click()
