from time import sleep

from src.utils.data import fake, generate_unique_email
from src.web.Application import Application
from tests.conftest import Config


def test_register_to_event(app: Application, configs: Config):
    email = generate_unique_email(configs.domain)
    first_name = fake.first_name()
    last_name = fake.last_name()

    app.home_page.open()
    app.home_page.is_loaded()
    event_name = app.home_page.get_first_event_name()
    app.home_page.open_first_event()

    app.event_page.is_loaded(event_name)
    app.event_page.open_registration()
    app.event_page.registration_sheet.fill_form(email, first_name, last_name)
    app.event_page.registration_sheet.check_ticket(event_name)

    # need time to create and log in a user
    sleep(1)

    app.event_page.header.go_to_me_page()

    app.me_page.check_user_info(email, f'{first_name} {last_name}')
    app.me_page.logout()
