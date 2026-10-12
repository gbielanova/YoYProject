import pytest
from playwright.sync_api import Page

from src.web.Application import Application


@pytest.fixture
def app(page: Page) -> Application:
    return Application(page)
