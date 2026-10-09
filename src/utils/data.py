import uuid

from faker import Faker

fake = Faker("en_US")


def generate_unique_email(domain: str, prefix: str = "gb_test") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}@{domain}"
