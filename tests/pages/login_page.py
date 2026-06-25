from playwright.sync_api import TimeoutError
from .base_page import BasePage


class LoginPage(BasePage):
    LOGIN_LINK = 'a[href="/vn/login"]'
    MAIN = 'main'
    EMAIL = 'input#email'
    PASSWORD = 'input#password'
    SUBMIT = 'button:has-text("Đăng nhập")'

    def open(self):
        self.goto_home()
        login_link = self.page.locator(self.LOGIN_LINK)
        if login_link.count() > 0:
            login_link.first.click()
        try:
            self.page.wait_for_load_state("networkidle", timeout=5000)
        except TimeoutError:
            pass
        return self

    def submit(self, email_value, password_value):
        main = self.page.locator(self.MAIN)
        email_input = main.locator(self.EMAIL)
        password_input = main.locator(self.PASSWORD)
        submit_btn = main.locator(self.SUBMIT)

        if email_value is not None:
            email_input.fill(email_value)
        if password_value is not None:
            password_input.fill(password_value)

        submit_btn.first.click()
        return main

    def login(self, email_value, password_value):
        self.open()
        return self.submit(email_value, password_value)
    

    def is_login_link_visible(self):
        link = self.page.locator(self.LOGIN_LINK)
        if link.count() == 0:
            return False
        try:
            return link.first.is_visible()
        except Exception:
            return False
