from playwright.sync_api import Page

from src.web.pages.CommunityPage import CommunityPage
from src.web.pages.EventPage import EventPage
from src.web.pages.HomePage import HomePage
from src.web.pages.LoginPage import LoginPage
from src.web.pages.MePage import MePage
from src.web.pages.NewCommunityPage import NewCommunityPage


class Application:
    def __init__(self, page: Page):
        self.page = page
        self.home_page = HomePage(page)
        self.login_page = LoginPage(page)
        self.me_page = MePage(page)
        self.event_page = EventPage(page)
        self.new_community_page = NewCommunityPage(page)
        self.community_page = CommunityPage(page)
