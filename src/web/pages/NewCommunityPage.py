from playwright.sync_api import Page


class NewCommunityPage:
    def __init__(self, page: Page):
        self.page = page
        self.name_input = page.get_by_test_id('community-name-input')
        self.slug_input = page.get_by_test_id('community-slug-input')
        self.description_input = page.get_by_test_id('community-description-input')
        self.unlisted_checkbox = page.get_by_test_id('community-unlisted-input')
        self.create_button = page.get_by_test_id('community-create-submit')

    def create_community(self, name: str, slug: str, description: str):
        self.name_input.fill(name)
        self.slug_input.fill(slug)
        self.description_input.fill(description)
        self.unlisted_checkbox.click()
        self.create_button.click()
