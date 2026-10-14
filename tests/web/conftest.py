import pytest
from playwright.sync_api import BrowserContext, Page

from src.config import Config
from src.utils.data import generate_unique_email
from src.utils.tracing import start_tracing, stop_tracing
from src.web.application import Application


# a fresh browser context and page for every test
@pytest.fixture
def app(page: Page) -> Application:
    return Application(page)


# the same browser context and page for the whole run
@pytest.fixture(scope="session")
def shared_app(shared_page: Page) -> Application:
    return Application(shared_page)


# tests on the shared page start logged out, even if the previous test failed before its logout,
# and each of them gets its own part of the trace, saved if the test fails
@pytest.fixture(autouse=True)
def prepare_shared_context(request: pytest.FixtureRequest):
    if "shared_app" not in request.fixturenames:
        yield
        return

    shared_context: BrowserContext = request.getfixturevalue("shared_context")
    shared_context.clear_cookies()
    shared_context.tracing.start_chunk()
    yield
    stop_tracing(shared_context, request, chunk=True)


# logs a new user in once per run and keeps the browser state (cookies) of that login
@pytest.fixture(scope="session")
def logged_user_state(new_test_context, configs: Config) -> dict:
    context = new_test_context()
    app = Application(context.new_page())

    app.login_page.open()
    app.login_page.fill_login_form(generate_unique_email(configs.domain), configs.otp_code)
    app.me_page.expect_loaded()

    state = context.storage_state()
    context.close()
    return state


# a fresh browser context and page for every test, already logged in; do not log out in these tests
@pytest.fixture
def logged_app(new_test_context, logged_user_state: dict, request: pytest.FixtureRequest):
    context = new_test_context(storage_state=logged_user_state)
    start_tracing(context)
    yield Application(context.new_page())
    stop_tracing(context, request)
    context.close()
