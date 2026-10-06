from time import sleep

from playwright.sync_api import Page

from src.utils.data import fake, generate_unique_email
from src.web.pages.EventPage import EventPage
from src.web.pages.HomePage import HomePage
from src.web.pages.MePage import MePage
from tests.conftest import Config


def test_register_to_event(page: Page, configs: Config):
    email = generate_unique_email(configs.domain)
    first_name = fake.first_name()
    last_name = fake.last_name()

    home_page = HomePage(page)
    home_page.open()
    home_page.is_loaded()
    event_name = home_page.get_first_event_name()
    home_page.open_first_event()

    event_page = EventPage(page)
    event_page.is_loaded(event_name)
    event_page.open_registration()
    event_page.registration_sheet.fill_form(email, first_name, last_name)
    event_page.registration_sheet.check_ticket(event_name)

    # need time to create and log in a user
    sleep(1)

    event_page.header.go_to_me_page()

    me_page = MePage(page)
    me_page.check_user_info(email, f'{first_name} {last_name}')
    me_page.logout()
