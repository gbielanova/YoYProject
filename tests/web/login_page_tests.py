from src.utils.data import fake, generate_unique_email
from src.web.Application import Application
from tests.conftest import Config


def test_register_a_user(app: Application, configs: Config):
    email = generate_unique_email(configs.domain)

    app.login_page.open()
    app.login_page.is_loaded()
    app.login_page.fill_login_form(email)

    app.me_page.check_user_info(email)
    app.me_page.logout()


def test_register_a_user_with_invalid_code(app: Application, configs: Config):
    email = generate_unique_email(configs.domain)
    code = fake.numerify('######')

    app.login_page.open()
    app.login_page.is_loaded()
    app.login_page.fill_login_form(email, code=code)

    app.login_page.check_invalid_code_error()
