import uuid

from faker import Faker

fake = Faker("en_US")


def generate_unique_email(domain: str, prefix: str = "gb_test") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}@{domain}"


def generate_email_of_length(domain: str, length: int) -> str:
    local_part_length = length - len(domain) - 1
    unique_part = uuid.uuid4().hex[:8]
    return f"{unique_part}{'a' * (local_part_length - len(unique_part))}@{domain}"
