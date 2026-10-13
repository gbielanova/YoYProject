from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    base_url: str
    domain: str
    test_secret: str
    otp_code: str
