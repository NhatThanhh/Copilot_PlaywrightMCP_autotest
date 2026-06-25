import json
from pathlib import Path
import allure
from playwright.sync_api import expect
from pages.login_page import LoginPage


DATA_PATH = Path(__file__).resolve().parents[1] / "test_data" / "login_data.json"
with open(DATA_PATH, 'r', encoding='utf-8') as f:
    LOGIN_DATA = json.load(f)


@allure.feature("Login")
@allure.story("Authentication")
@allure.severity(allure.severity_level.CRITICAL)
def run_case(page, base_url, case_id):
    data = LOGIN_DATA[case_id]
    lp = LoginPage(page, base_url)
    main = lp.login(data.get('email'), data.get('password'))
    expect_cfg = data.get('expect', {})
    if expect_cfg.get('type') == 'success':
        # success: wait for the page to finish processing the login
        try:
            lp.page.wait_for_load_state('networkidle', timeout=8000)
        except Exception:
            pass

        # then wait for header Login link to disappear (or assert as fallback)
        try:
            expect(lp.page.locator(lp.LOGIN_LINK).first).not_to_be_visible(timeout=5000)
        except Exception:
            assert not lp.is_login_link_visible()
        return

    contains = expect_cfg.get('contains')
    if contains:
        expect(main).to_contain_text(contains, timeout=5000)
        return

    any_of = expect_cfg.get('any_of')
    if any_of:
        found = False
        for m in any_of:
            try:
                expect(main).to_contain_text(m, timeout=2000)
                found = True
                break
            except Exception:
                continue
        assert found, f"No expected validation in any_of for {case_id}"


@allure.epic("Authentication")
@allure.story("Login")
@allure.title("DN_01 - Valid account login")
@allure.severity(allure.severity_level.CRITICAL)
def test_DN_01_login_valid_account(page, base_url):
    run_case(page, base_url, 'DN_01')


@allure.epic("Authentication")
@allure.story("Login")
@allure.title("DN_02 - Unregistered email")
@allure.severity(allure.severity_level.NORMAL)
def test_DN_02_unregistered_email(page, base_url):
    run_case(page, base_url, 'DN_02')


@allure.epic("Authentication")
@allure.story("Login")
@allure.title("DN_03 - Invalid email format")
@allure.severity(allure.severity_level.NORMAL)
def test_DN_03_invalid_email_format(page, base_url):
    run_case(page, base_url, 'DN_03')


@allure.epic("Authentication")
@allure.story("Login")
@allure.title("DN_04 - Empty email")
@allure.severity(allure.severity_level.NORMAL)
def test_DN_04_empty_email(page, base_url):
    run_case(page, base_url, 'DN_04')


@allure.epic("Authentication")
@allure.story("Login")
@allure.title("DN_05 - Empty password")
@allure.severity(allure.severity_level.NORMAL)
def test_DN_05_empty_password(page, base_url):
    run_case(page, base_url, 'DN_05')


@allure.epic("Authentication")
@allure.story("Login")
@allure.title("DN_06 - Wrong password")
@allure.severity(allure.severity_level.NORMAL)
def test_DN_06_wrong_password(page, base_url):
    run_case(page, base_url, 'DN_06')


@allure.epic("Authentication")
@allure.story("Login")
@allure.title("DN_07 - Password case sensitivity")
@allure.severity(allure.severity_level.NORMAL)
def test_DN_07_wrong_password_case_sensitive(page, base_url):
    run_case(page, base_url, 'DN_07')


@allure.epic("Authentication")
@allure.story("Login")
@allure.title("DN_08 - Password leading space")
@allure.severity(allure.severity_level.NORMAL)
def test_DN_08_password_leading_space(page, base_url):
    run_case(page, base_url, 'DN_08')


@allure.epic("Authentication")
@allure.story("Login")
@allure.title("DN_09 - Empty email and password")
@allure.severity(allure.severity_level.NORMAL)
def test_DN_09_empty_email_and_password(page, base_url):
    run_case(page, base_url, 'DN_09')


@allure.epic("Authentication")
@allure.story("Login")
@allure.title("DN_10 - Email leading space")
@allure.severity(allure.severity_level.NORMAL)
def test_DN_10_email_leading_space(page, base_url):
    run_case(page, base_url, 'DN_10')
