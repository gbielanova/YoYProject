import os
from dataclasses import dataclass

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Browser, BrowserContext, Page, Route

load_dotenv()


@dataclass(frozen=True)
class Config:
    base_url: str
    domain: str


@pytest.fixture(scope="session")
def configs(base_url):
    return Config(
        base_url=os.getenv("BASE_URL", base_url),
        domain=os.getenv("DOMAIN")
    )


TEST_SECRET_HEADER = {"x-yoy-test-secret": "111111"}


# the header lets the site skip its limit of one login per minute
def add_test_header(context: BrowserContext):
    def handle(route: Route):
        route.continue_(headers={**route.request.headers, **TEST_SECRET_HEADER})

    context.route("**/auth/email-otp/request*", handle)


# a new context for every test (the default of pytest-playwright), with the test header added
@pytest.fixture
def context(context: BrowserContext) -> BrowserContext:
    add_test_header(context)
    return context


# one context for the whole run: cookies and login state are kept between tests
@pytest.fixture(scope="session")
def shared_context(browser: Browser, browser_context_args: dict):
    context = browser.new_context(**browser_context_args)
    add_test_header(context)
    yield context
    context.close()


# one page for the whole run, opened in the shared context
@pytest.fixture(scope="session")
def shared_page(shared_context: BrowserContext):
    page = shared_context.new_page()
    yield page
    page.close()
