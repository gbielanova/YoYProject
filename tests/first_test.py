from playwright.sync_api import Page, expect


def test_open_home_page(page: Page):
    page.goto('https://testomat.io')

    expect(page.locator(".login-item").last).to_be_visible()
    expect(page).to_have_title("AI Test Management Tool | Testomat.io")

