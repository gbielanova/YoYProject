from playwright.sync_api import Page, expect

from src.web.components.event_registration_sheet import EventRegistrationSheet
from src.web.pages.base_page import BasePage


class EventPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.registration_sheet = EventRegistrationSheet(page)
        self.register_button = page.get_by_test_id('register-cta')

    def expect_loaded(self, event_name: str):
        expect(self.header.title).to_have_text(event_name)

    def open_registration(self):
        self.register_button.click()
