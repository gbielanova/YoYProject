from playwright.sync_api import Page


class Header:
    def __init__(self, page: Page):
        self.page = page
        self.title = page.locator('.yoy-header-title-text')
        self.me_link = page.locator('a[href="/me"]')

    def go_to_me_page(self):
        self.me_link.click()
