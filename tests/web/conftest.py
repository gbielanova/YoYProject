import pytest
from playwright.sync_api import BrowserContext, Page

from src.web.Application import Application


# a fresh browser context and page for every test
@pytest.fixture
def app(page: Page) -> Application:
    return Application(page)


# the same browser context and page for the whole run
@pytest.fixture(scope="session")
def shared_app(shared_page: Page) -> Application:
    return Application(shared_page)


# tests on the shared page start logged out, even if the previous test failed before its logout
@pytest.fixture(autouse=True)
def clear_shared_cookies(request: pytest.FixtureRequest):
    if "shared_app" in request.fixturenames:
        shared_context: BrowserContext = request.getfixturevalue("shared_context")
        shared_context.clear_cookies()
