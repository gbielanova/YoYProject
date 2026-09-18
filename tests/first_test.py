from playwright.sync_api import Page, expect


def test_login(page: Page):
    page.goto('https://test.yoy.events/')
    expect(page).to_have_title('йой! — події в твоєму місті ')

    page.locator('a[href="/me"]').click()

    expect(page.locator('[data-testid="signin-returntohint"]')).to_have_text('Після входу повернемо тебе назад.')

    page.locator('[data-testid="signin-email-input"]').fill('test@test.com')
    page.locator('[data-testid="signin-otp-submit-label"]').click()
    page.locator('[data-testid="signin-code-input"]').fill('000000')

    page.locator('[data-testid="signin-code-submit-label"]').click()

    expect(page.locator('[data-testid="me-display-name"]')).to_have_text('test@test.com')
