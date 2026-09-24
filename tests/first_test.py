from time import sleep

from playwright.sync_api import Page, expect


def test_login(page: Page):
    page.goto('https://test.yoy.events/')
    expect(page).to_have_title('йой! — події в твоєму місті ')

    page.locator('a[href="/me"]').click()

    expect(page.locator('[data-testid="signin-returntohint"]')).to_have_text('Після входу повернемо тебе назад.')

    page.locator('[data-testid="signin-email-input"]').fill('test1@test.com')
    page.locator('[data-testid="signin-otp-submit-label"]').click()
    page.locator('[data-testid="signin-code-input"]').fill('000000')

    page.locator('[data-testid="signin-code-submit-label"]').click()

    expect(page.locator('[data-testid="me-display-name"]')).to_have_text('test1@test.com')

    page.locator('data-testid="logout-btn"').click()


def test_register_to_event(page: Page):
    page.goto('https://test.yoy.events/')

    conf_name = page.locator('[data-event-card] h3').first.inner_text()

    page.locator('[data-testid="event-card-cover-image"]').first.click()

    expect(page.locator('.yoy-header-title-text')).to_have_text(conf_name)

    page.locator('[data-testid="register-cta"]').click()

    page.locator('#reg_name').fill('Іван')
    page.locator('#reg_lastname').fill('Петренко')
    page.locator('#reg_email').fill('test9@test.com')
    page.locator('#reg_phone').fill('+380000000000')

    page.locator('#sheet_submit_btn').click()

    expect(page.locator('#sheet_confirm_view h3')).to_have_text("Готово! Твій квиток")
    expect(page.locator('[data-testid="ticket-event-title"]')).to_have_text(conf_name)

    # it takes some time to regiter a user, playwright is too fast clicking on the link
    sleep(1)

    page.locator('[href="/me"]').click()

    expect(page.locator('[data-testid="me-display-name"]')).to_have_text('Іван Петренко')
    expect(page.locator('[data-testid="me-display-name"] + div')).to_have_text('test9@test.com')


