from playwright.sync_api import Page

from src.web.pages.community_page import CommunityPage
from src.web.pages.event_page import EventPage
from src.web.pages.home_page import HomePage
from src.web.pages.login_page import LoginPage
from src.web.pages.me_page import MePage
from src.web.pages.new_community_page import NewCommunityPage


class Application:
    def __init__(self, page: Page):
        self.page = page
        self.home_page = HomePage(page)
        self.login_page = LoginPage(page)
        self.me_page = MePage(page)
        self.event_page = EventPage(page)
        self.new_community_page = NewCommunityPage(page)
        self.community_page = CommunityPage(page)
