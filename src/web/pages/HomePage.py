from playwright.sync_api import Page, expect


class HomePage:
    def __init__(self, page: Page):
        self.page = page
        self.event_cards = page.locator('[data-event-card]')

    def open(self):
        self.page.goto('/')

    def is_loaded(self):
        expect(self.event_cards.first).to_be_visible()

    def get_first_event_name(self) -> str:
        return self.event_cards.first.locator('h3').inner_text()

    def open_first_event(self):
        self.event_cards.first.click()
