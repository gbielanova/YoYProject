from src.utils.data import fake, generate_unique_email
from src.web.Application import Application
from tests.conftest import Config


def test_create_new_community(shared_app: Application, configs: Config):
    email = generate_unique_email(configs.domain)
    community_name = f'{fake.street_name()} community'
    community_slug = fake.slug()
    community_description = fake.sentence()

    shared_app.login_page.open()
    shared_app.login_page.is_loaded()
    shared_app.login_page.fill_login_form(email)

    shared_app.me_page.is_loaded()
    shared_app.me_page.open_new_community()
    shared_app.new_community_page.is_loaded()

    shared_app.new_community_page.create_community(community_name, community_slug, community_description)

    shared_app.community_page.check_community_info(community_name, community_slug, community_description)

    shared_app.community_page.header.go_to_me_page()
    shared_app.me_page.logout()
