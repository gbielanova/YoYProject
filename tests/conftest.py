import os
import time
from dataclasses import dataclass

import pytest
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    base_url: str
    domain: str


@pytest.fixture(scope="session")
def configs():
    return Config(
        base_url=os.getenv("BASE_URL"),
        domain=os.getenv("DOMAIN")
    )


# the site allows only one login per minute
LOGIN_COOLDOWN_SEC = 61
_last_login = [0.0]


@pytest.fixture
def login_cooldown():
    wait = LOGIN_COOLDOWN_SEC - (time.monotonic() - _last_login[0])
    if wait > 0:
        time.sleep(wait)
    yield
    _last_login[0] = time.monotonic()
