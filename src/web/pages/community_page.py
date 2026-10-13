import re

from playwright.sync_api import Page, expect

from src.web.pages.base_page import BasePage


class CommunityPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.title = page.get_by_test_id('community-title')
        self.slug = page.locator('[data-testid="community-title"] + div')
        self.description = page.get_by_test_id('community-description')

    def check_community_info(self, name: str, slug: str, description: str):
        expect(self.page).to_have_url(re.compile(re.escape(slug)))
        expect(self.title).to_have_text(name)
        expect(self.slug).to_have_text(f'@{slug}')
        expect(self.description).to_have_text(description)
