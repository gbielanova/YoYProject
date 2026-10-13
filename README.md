# YoYProject

Automated UI tests for the [yoy.events](https://test.yoy.events/) test environment, written with
Python, pytest and Playwright using the Page Object pattern.

## What is covered

| Test file | What it checks |
|---|---|
| `tests/web/test_login_page.py` | Signing in with an email code, wrong codes, codes in a wrong format, invalid emails, email length limits |
| `tests/web/test_event_registration.py` | Registering for an event from the home page |
| `tests/web/test_community.py` | Creating a new community |

## Requirements

- Python 3.13 or newer
- Access to the test environment and its test secret

## Setup

1. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Install the browser Playwright uses:

   ```bash
   playwright install chromium
   ```

4. Create a `.env` file in the project root (it is not committed to git):

   ```
   DOMAIN=<domain used for generated test emails>
   TEST_SECRET=<value of the x-yoy-test-secret header>
   OTP_CODE=<fixed login code of the test environment>
   ```

   | Variable | Required | Purpose |
   |---|---|---|
   | `DOMAIN` | yes | Domain for the unique emails the tests generate |
   | `TEST_SECRET` | yes | Sent as the `x-yoy-test-secret` header so the site skips its one-login-per-minute limit |
   | `OTP_CODE` | yes | The login code the test environment accepts |
   | `BASE_URL` | no | Overrides `base_url` from `pytest.ini` |

## Running the tests

Run everything:

```bash
pytest
```

Run one file or one test:

```bash
pytest tests/web/test_login_page.py
pytest tests/web/test_login_page.py -k invalid_email
```

Run against another environment:

```bash
pytest --base-url https://other.yoy.events/
```

The browser window is shown by default (`--headed` in `pytest.ini`). To run without a window:

```bash
pytest -o addopts=""
```

## Project structure

```
src/
  config.py              Config class with the settings read from .env
  utils/data.py          Test data helpers (unique emails, Faker)
  web/
    application.py       Application class that creates all page objects
    pages/               One class per page; all inherit from BasePage
    components/          Parts shared by several pages (header, event registration sheet)
tests/
  conftest.py            Config, browser context and page fixtures
  web/
    conftest.py          app and shared_app fixtures
    test_*.py            The tests
pytest.ini               pytest settings and the base URL
```

## How the tests are built

- **Page objects.** Each page of the site has a class in `src/web/pages/` with its locators and
  actions. `BasePage` gives every page `self.page`, `self.header` and `open()`.
- **Application.** `Application` creates every page object once, so a test reaches them as
  `shared_app.login_page`, `shared_app.me_page` and so on.
- **Fixtures.**

  | Fixture | Lifetime | Use it when |
  |---|---|---|
  | `shared_app` | whole run | Default. All tests share one browser context and page; cookies are cleared before each test |
  | `app` | one test | A test needs a completely fresh browser context |
  | `configs` | whole run | A test needs a value from `.env` |

### Adding a new page

1. Create `src/web/pages/<name>_page.py` with a class that inherits from `BasePage`.
   Set `path` if the page can be opened by its address.
2. Add it to `Application.__init__` in `src/web/application.py`.
3. Use it in a test through `shared_app.<name>_page`.
