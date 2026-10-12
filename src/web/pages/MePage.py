from playwright.sync_api import Page, expect

from src.web.components.Header import Header


class MePage:
    def __init__(self, page: Page):
        self.page = page
        self.header = Header(page)

        self.identity_section = page.get_by_test_id('me-identity')
        self.display_name = page.get_by_test_id('me-display-name')
        self.email = page.locator('[data-testid="me-display-name"] + div')

        self.communities_section = page.get_by_test_id('me-communities')
        self.communities_title = self.communities_section.get_by_text('Мої спільноти', exact=True)
        self.new_community_link = self.communities_section.locator('[href="/communities/new"]')

        self.actions_section = page.get_by_test_id('me-actions')
        self.edit_profile_link = self.actions_section.locator('[href="/me/profile/edit"]')
        self.saved_participants_link = self.actions_section.locator('[href="/me/saved-participants"]')
        self.settings_link = self.actions_section.locator('[href="/me/settings"]')
        self.notifications_item = self.actions_section.get_by_text('Сповіщення', exact=True)

        self.logout_button = page.get_by_test_id('logout-btn')
        self.logout_all_button = page.get_by_test_id('logout-all-btn')

    def is_loaded(self):
        expect(self.header.title).to_have_text('Я')
        self.header.is_loaded()

        for element in [
            self.identity_section,
            self.display_name,
            self.communities_section,
            self.communities_title,
            self.new_community_link,
            self.actions_section,
            self.edit_profile_link,
            self.saved_participants_link,
            self.settings_link,
            self.notifications_item,
            self.logout_button,
            self.logout_all_button,
        ]:
            expect(element).to_be_visible()

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
