import pytest

from src.utils.data import fake, generate_email_of_length, generate_unique_email
from src.web.application import Application
from src.config import Config


def test_register_a_user(shared_app: Application, configs: Config):
    email = generate_unique_email(configs.domain)

    shared_app.login_page.open()
    shared_app.login_page.expect_loaded()
    shared_app.login_page.fill_login_form(email, configs.otp_code)

    shared_app.me_page.check_user_info(email)
    shared_app.me_page.logout()


# class: 6 digits but not the valid code
@pytest.mark.parametrize(
    "code",
    [
        pytest.param("000000", id="lowest_value"),
        pytest.param("111110", id="just_below_valid"),
        pytest.param("111112", id="just_above_valid"),
        pytest.param("999999", id="highest_value"),
        pytest.param(fake.numerify('######'), id="random_value"),
    ],
)
def test_register_a_user_with_wrong_code(shared_app: Application, configs: Config, code: str):
    email = generate_unique_email(configs.domain)

    shared_app.login_page.open()
    shared_app.login_page.expect_loaded()
    shared_app.login_page.fill_login_form(email, code=code)

    shared_app.login_page.check_invalid_code_error()


# classes: fewer than 6 digits, and characters that are not digits (the field removes them)
@pytest.mark.parametrize(
    "code, expected_value",
    [
        pytest.param("", "", id="empty"),
        pytest.param("1", "1", id="one_digit"),
        pytest.param("11111", "11111", id="five_digits"),
        pytest.param("abcdef", "", id="letters"),
        pytest.param("!@#$%^", "", id="special_characters"),
        pytest.param("      ", "", id="spaces"),
        pytest.param("11a111", "11111", id="letter_among_digits"),
    ],
)
def test_code_with_wrong_format_cannot_be_submitted(shared_app: Application, configs: Config, code: str, expected_value: str):
    email = generate_unique_email(configs.domain)

    shared_app.login_page.open()
    shared_app.login_page.expect_loaded()
    shared_app.login_page.request_code(email)
    shared_app.login_page.enter_code(code)

    shared_app.login_page.check_code_cannot_be_submitted(expected_value)


# class: more than 6 digits (the field keeps only the first 6)
@pytest.mark.parametrize(
    "code, expected_value",
    [
        pytest.param("0000001", "000000", id="seven_digits"),
        pytest.param("000000123456", "000000", id="twelve_digits"),
    ],
)
def test_code_longer_than_six_digits_is_cut(shared_app: Application, configs: Config, code: str, expected_value: str):
    email = generate_unique_email(configs.domain)

    shared_app.login_page.open()
    shared_app.login_page.expect_loaded()
    shared_app.login_page.request_code(email)
    shared_app.login_page.enter_code(code)

    shared_app.login_page.check_code_can_be_submitted(expected_value)


# classes: empty email, no "@", shorter than 5 characters
@pytest.mark.parametrize(
    "email",
    [
        pytest.param("", id="empty"),
        pytest.param("   ", id="spaces_only"),
        pytest.param("userexample.com", id="no_at_sign"),
        pytest.param("a@bc", id="four_characters"),
    ],
)
def test_login_with_invalid_email(shared_app: Application, email: str):
    shared_app.login_page.open()
    shared_app.login_page.expect_loaded()
    shared_app.login_page.request_code(email)

    shared_app.login_page.check_invalid_email_error()


# boundary: 5 characters is the shortest email the form accepts (4 is covered above)
@pytest.mark.parametrize(
    "email",
    [
        pytest.param("a@b.c", id="five_characters"),
        pytest.param("a@b.cd", id="six_characters"),
    ],
)
def test_login_with_shortest_valid_email(shared_app: Application, email: str):
    shared_app.login_page.open()
    shared_app.login_page.expect_loaded()
    response = shared_app.login_page.request_code_and_wait_for_response(email)

    assert response.ok
    shared_app.login_page.check_code_step_is_opened()


# boundary: 254 characters is the longest email address the standard allows
def test_login_with_longest_valid_email(shared_app: Application, configs: Config):
    email = generate_email_of_length(configs.domain, 254)

    shared_app.login_page.open()
    shared_app.login_page.expect_loaded()
    response = shared_app.login_page.request_code_and_wait_for_response(email)

    assert response.ok
    shared_app.login_page.check_code_step_is_opened()
