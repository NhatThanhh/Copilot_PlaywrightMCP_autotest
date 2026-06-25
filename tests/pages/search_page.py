from playwright.sync_api import TimeoutError, expect
from .base_page import BasePage


class SearchPage(BasePage):
    SEARCH_INPUT = "input#search"

    PRODUCT_TITLE_SELECTORS = [
        ".product-item-name",
        ".product-name",
        ".product-title",
        ".product-item a",
        "a[href*='/vn/products/']",
        "h3",
        "h2",
    ]

    NO_RESULT_TEXT = "Không tìm thấy kết quả nào"

    def open_home(self):
        self.goto_home()
        return self

    def search(self, keyword):
        self.open_home()

        search_input = self.page.locator(self.SEARCH_INPUT)
        expect(search_input).to_be_visible(timeout=10000)

        search_input.click()
        search_input.fill(keyword)
        self.page.keyboard.press("Enter")

        try:
            self.page.wait_for_load_state("networkidle", timeout=10000)
        except TimeoutError:
            pass

        return self

    def get_search_input_value(self):
        return self.page.locator(self.SEARCH_INPUT).input_value()

    def get_product_titles(self):
        for selector in self.PRODUCT_TITLE_SELECTORS:
            locator = self.page.locator(selector)
            count = locator.count()

            if count == 0:
                continue

            titles = []
            for i in range(count):
                item = locator.nth(i)
                try:
                    if item.is_visible():
                        text = item.inner_text().strip()
                        if text:
                            titles.append(text)
                except Exception:
                    continue

            if titles:
                return titles

        return []

    def expect_search_input_value(self, expected_value):
        expect(self.page.locator(self.SEARCH_INPUT)).to_have_value(
            expected_value,
            timeout=10000
        )

    def expect_titles_related_to_keywords(self, expected_keywords):
        titles = self.get_product_titles()

        assert titles, "No product titles were found on the search result page"

        normalized_titles = [title.lower() for title in titles]
        normalized_keywords = [keyword.lower() for keyword in expected_keywords]

        matched_titles = [
            title for title in normalized_titles
            if any(keyword in title for keyword in normalized_keywords)
        ]

        assert matched_titles, (
            f"No product title is related to expected keywords: {expected_keywords}. "
            f"Actual titles: {titles[:5]}"
        )

    def expect_on_home_page(self, expected_url):
        actual_url = self.page.url.rstrip("/")
        expected_url = expected_url.rstrip("/")
        assert actual_url == expected_url, (
            f"Expected to remain on home page {expected_url}, but got {actual_url}"
        )

    def expect_no_result_message(self):
        expect(self.page.locator("body")).to_contain_text(
            self.NO_RESULT_TEXT,
            timeout=10000
        )