import os

import pytest
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture(scope="session")
def configs():
    return {
        "base_url": os.getenv("BASE_URL"),
        "domain": os.getenv("DOMAIN"),
    }
