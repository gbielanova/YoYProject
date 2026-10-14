import os

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Browser, BrowserContext, Route

from src.config import Config

load_dotenv()


@pytest.fixture(scope="session")
def configs(base_url):
    return Config(
        base_url=os.getenv("BASE_URL", base_url),
        domain=os.getenv("DOMAIN"),
        test_secret=os.environ["TEST_SECRET"],
        otp_code=os.environ["OTP_CODE"],
    )


# the header lets the site skip its limit of one login per minute
def add_test_header(context: BrowserContext, test_secret: str):
    def handle(route: Route):
        route.continue_(headers={**route.request.headers, "x-yoy-test-secret": test_secret})

    context.route("**/auth/email-otp/request*", handle)


# a new context for every test (the default of pytest-playwright), with the test header added
@pytest.fixture
def context(context: BrowserContext, configs: Config) -> BrowserContext:
    add_test_header(context, configs.test_secret)
    return context


# creates a browser context with the project settings and the test header; extra options can be passed in
@pytest.fixture(scope="session")
def new_test_context(browser: Browser, browser_context_args: dict, configs: Config):
    def create(**options) -> BrowserContext:
        context = browser.new_context(**{**browser_context_args, **options})
        add_test_header(context, configs.test_secret)
        return context

    return create


# one context for the whole run: cookies and login state are kept between tests
@pytest.fixture(scope="session")
def shared_context(new_test_context):
    context = new_test_context()
    yield context
    context.close()


# one page for the whole run, opened in the shared context
@pytest.fixture(scope="session")
def shared_page(shared_context: BrowserContext):
    page = shared_context.new_page()
    yield page
    page.close()
