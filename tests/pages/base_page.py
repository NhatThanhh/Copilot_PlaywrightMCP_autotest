from playwright.sync_api import TimeoutError


class BasePage:
    def __init__(self, page, base_url):
        self.page = page
        self.base_url = base_url

    def goto_home(self):
        self.page.goto(self.base_url)
        try:
            self.page.wait_for_load_state("networkidle", timeout=5000)
        except TimeoutError:
            pass
