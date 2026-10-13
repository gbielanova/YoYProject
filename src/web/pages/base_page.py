from playwright.sync_api import Page

from src.web.components.header import Header


class BasePage:
    # address of the page, relative to base_url; set it in pages that can be opened directly
    path: str | None = None

    def __init__(self, page: Page):
        self.page = page
        self.header = Header(page)

    def open(self):
        if self.path is None:
            raise NotImplementedError(f'{type(self).__name__} has no path and cannot be opened directly')
        self.page.goto(self.path)
