from playwright.sync_api import Page, expect


class Header:
    def __init__(self, page: Page):
        self.page = page
        self.title = page.locator('.yoy-header-title-text')

        self.nav = page.get_by_test_id('bottom-nav')
        self.overview_link = self.nav.get_by_role('link', name='Огляд', exact=True)
        self.events_link = self.nav.get_by_role('link', name='Події', exact=True)
        self.communities_link = self.nav.get_by_role('link', name='Спільноти', exact=True)
        self.tickets_link = self.nav.get_by_role('link', name='Квитки', exact=True)
        self.me_link = self.nav.get_by_role('link', name='Я', exact=True)

    def is_loaded(self):
        expect(self.nav).to_be_visible()

        for link in [self.overview_link, self.events_link, self.communities_link, self.tickets_link, self.me_link]:
            expect(link).to_be_visible()

    def go_to_me_page(self):
        self.me_link.click()
