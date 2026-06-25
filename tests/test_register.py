import json
from pathlib import Path

import allure
import pytest

from pages.register_page import RegisterPage


DATA_PATH = Path(__file__).resolve().parents[1] / "test_data" / "register_data.json"

with DATA_PATH.open("r", encoding="utf-8") as fh:
    REGISTER_DATA = json.load(fh)


CASE_IDS = [
    "DK_01", "DK_02", "DK_03", "DK_04", "DK_05", "DK_06", "DK_07",
    "DK_08", "DK_09", "DK_10", "DK_11", "DK_12", "DK_13"
]

@allure.epic("Authentication")
@allure.feature("Register")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize("case_id", CASE_IDS, ids=CASE_IDS)
def test_register_flows(page, base_url, case_id):
    case_data = REGISTER_DATA[case_id]
    test_name = case_data.get("description", "Register flow")

    allure.dynamic.title(f"{case_id} - {test_name}")
    allure.dynamic.story(test_name)
    allure.dynamic.description(f"Validate register flow: {test_name}")

    register_page = RegisterPage(page, base_url)

    register_page.open()
    register_page.fill_form(case_data)
    register_page.agree_terms()
    register_page.submit()

    page.wait_for_timeout(3000)

    page_text = register_page.get_page_text().lower()
    expected = case_data["expect"]

    if expected["type"] == "success_or_error":
        assert any(text.lower() in page_text for text in expected["contains"]), (
            f"Expected one of {expected['contains']} in page content for {case_id}"
        )
    else:
        for text in expected["contains"]:
            assert text.lower() in page_text, (
                f"Expected '{text}' in page content for {case_id}"
            )