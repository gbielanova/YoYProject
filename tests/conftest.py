import os
from dataclasses import dataclass

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page, Route

load_dotenv()


@dataclass(frozen=True)
class Config:
    domain: str


@pytest.fixture(scope="session")
def configs():
    return Config(
        domain=os.getenv("DOMAIN")
    )


TEST_SECRET_HEADER = {"x-yoy-test-secret": "111111"}


# the header lets the site skip its limit of one login per minute
@pytest.fixture(autouse=True)
def add_test_header(page: Page):
    def handle(route: Route):
        route.continue_(headers={**route.request.headers, **TEST_SECRET_HEADER})

    page.route("**/auth/email-otp/request*", handle)
