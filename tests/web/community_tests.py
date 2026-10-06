from playwright.sync_api import Page

from src.utils.data import fake, generate_unique_email
from src.web.pages.CommunityPage import CommunityPage
from src.web.pages.LoginPage import LoginPage
from src.web.pages.MePage import MePage
from src.web.pages.NewCommunityPage import NewCommunityPage
from tests.conftest import Config


def test_create_new_community(page: Page, configs: Config):
    email = generate_unique_email(configs.domain)
    community_name = f'{fake.street_name()} community'
    community_slug = fake.slug()
    community_description = fake.sentence()

    login_page = LoginPage(page)
    login_page.open()
    login_page.fill_login_form(email)

    me_page = MePage(page)
    me_page.open_new_community()

    NewCommunityPage(page).create_community(community_name, community_slug, community_description)

    community_page = CommunityPage(page)
    community_page.check_community_info(community_name, community_slug, community_description)

    community_page.header.go_to_me_page()
    me_page.logout()
