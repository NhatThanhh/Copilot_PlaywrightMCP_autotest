import json
from pathlib import Path

import allure
import pytest

from pages.search_page import SearchPage


DATA_FILE = Path(__file__).resolve().parents[1] / "test_data" / "search_data.json"
CASE_NAMES = [f"TK_{index:02d}" for index in range(1, 11)]


@allure.epic("MUJI Vietnam")
@allure.feature("Search")
@pytest.mark.parametrize("case_name", CASE_NAMES, ids=CASE_NAMES)
def test_search_cases(page, base_url, case_name):
    with DATA_FILE.open("r", encoding="utf-8") as fh:
        test_data = json.load(fh)[case_name]

    test_name = test_data.get("test_name", case_name)
    keyword = test_data["keyword"]
    assertion_type = test_data["assertion"]
    expected_display_value = test_data.get("expected_display_value", keyword)
    expected_contains = test_data.get("expected_contains", [])
    expected_home_url = test_data.get("expected_home_url", base_url)

    allure.dynamic.title(f"{case_name} - {test_name}")
    allure.dynamic.story(test_name)
    allure.dynamic.severity(allure.severity_level.NORMAL)

    search_page = SearchPage(page, base_url)
    search_page.search(keyword)

    if assertion_type == "no_result":
        search_page.expect_no_result_message()

    elif assertion_type == "home_page":
        search_page.expect_on_home_page(expected_home_url)

    else:
        search_page.expect_search_input_value(expected_display_value)
        search_page.expect_titles_related_to_keywords(expected_contains)