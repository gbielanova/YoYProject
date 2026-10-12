from playwright.sync_api import Page, expect

from src.web.components.EventRegistrationSheet import EventRegistrationSheet
from src.web.components.Header import Header


class EventPage:
    def __init__(self, page: Page):
        self.page = page
        self.header = Header(page)
        self.registration_sheet = EventRegistrationSheet(page)
        self.register_button = page.get_by_test_id('register-cta')

    def is_loaded(self, event_name: str):
        expect(self.header.title).to_have_text(event_name)

    def open_registration(self):
        self.register_button.click()
