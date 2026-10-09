from playwright.sync_api import Page, expect


class EventRegistrationSheet:
    def __init__(self, page: Page):
        self.page = page
        self.first_name_input = page.locator('#reg_name')
        self.last_name_input = page.locator('#reg_lastname')
        self.email_input = page.locator('#reg_email')
        self.phone_input = page.locator('#reg_phone')
        self.submit_button = page.locator('#sheet_submit_btn')
        self.confirm_title = page.locator('#sheet_confirm_view h3')
        self.ticket_event_title = page.get_by_test_id('ticket-event-title')

    def fill_form(self, email: str, first_name: str = '', last_name: str = '', phone: str = '+380000000000'):
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.email_input.fill(email)
        self.phone_input.fill(phone)
        self.submit_button.click()

    def check_ticket(self, event_name: str):
        expect(self.confirm_title).to_have_text("Готово! Твій квиток")
        expect(self.ticket_event_title).to_have_text(event_name)
