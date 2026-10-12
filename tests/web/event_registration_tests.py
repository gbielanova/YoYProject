from time import sleep

from src.utils.data import fake, generate_unique_email
from src.web.Application import Application
from tests.conftest import Config


def test_register_to_event(shared_app: Application, configs: Config):
    email = generate_unique_email(configs.domain)
    first_name = fake.first_name()
    last_name = fake.last_name()

    shared_app.home_page.open()
    shared_app.home_page.is_loaded()
    event_name = shared_app.home_page.get_first_event_name()
    shared_app.home_page.open_first_event()

    shared_app.event_page.is_loaded(event_name)
    shared_app.event_page.open_registration()
    shared_app.event_page.registration_sheet.fill_form(email, first_name, last_name)
    shared_app.event_page.registration_sheet.check_ticket(event_name)

    shared_app.login_page.open()
    shared_app.login_page.is_loaded()
    shared_app.login_page.fill_login_form(email)

    shared_app.me_page.is_loaded()
    shared_app.me_page.check_user_info(email, f'{first_name} {last_name}')
    shared_app.me_page.logout()
