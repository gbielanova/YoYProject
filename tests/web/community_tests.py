from src.utils.data import fake, generate_unique_email
from src.web.Application import Application
from tests.conftest import Config


def test_create_new_community(app: Application, configs: Config):
    email = generate_unique_email(configs.domain)
    community_name = f'{fake.street_name()} community'
    community_slug = fake.slug()
    community_description = fake.sentence()

    app.login_page.open()
    app.login_page.fill_login_form(email)

    app.me_page.open_new_community()

    app.new_community_page.create_community(community_name, community_slug, community_description)

    app.community_page.check_community_info(community_name, community_slug, community_description)

    app.community_page.header.go_to_me_page()
    app.me_page.logout()
