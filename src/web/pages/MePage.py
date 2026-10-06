from playwright.sync_api import Page, expect


class MePage:
    def __init__(self, page: Page):
        self.page = page
        self.display_name = page.get_by_test_id('me-display-name')
        self.email = page.locator('[data-testid="me-display-name"] + div')
        self.new_community_link = page.locator('[href="/communities/new"]')
        self.logout_button = page.get_by_test_id('logout-btn')

    def check_user_info(self, email: str, name: str = ''):
        if name == '':
            expect(self.display_name).to_have_text(email)
        else:
            expect(self.display_name).to_have_text(name)
            expect(self.email).to_have_text(email)

    def open_new_community(self):
        expect(self.new_community_link).to_have_text('Нова спільнота')
        self.new_community_link.click()

    def logout(self):
        self.logout_button.click()
