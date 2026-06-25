from playwright.sync_api import TimeoutError, expect

from .base_page import BasePage


class RegisterPage(BasePage):
    REGISTER_LINKS = [
        'a[href="/vn/register"]',
        'a[href="/vn/login"]',
    ]
    EMAIL = 'input#email'
    PASSWORD = 'input#password'
    PHONE = 'input#register_phone'
    FULL_NAME = 'input#fullName'
    DATE_OF_BIRTH = 'input#date_of_birth'
    GENDER = 'select[name="gender"]'
    TERMS_CHECKBOX = 'label:has-text("Tôi trên 16 tuổi")'
    SUBMIT = 'button:has-text("Tạo Tài Khoản Mới")'

    def open(self):
        self.goto_home()

        register_link = self.page.locator('a, button').filter(has_text='Đăng ký').first
        try:
            register_link.click()
        except Exception:
            self.page.goto(f"{self.base_url}/register")

        try:
            self.page.wait_for_load_state('networkidle', timeout=8000)
        except TimeoutError:
            pass

        return self

    def fill_form(self, data):
        self.page.locator(self.EMAIL).fill(data['email'])
        self.page.locator(self.PASSWORD).fill(data['password'])
        self.page.locator(self.PHONE).fill(data['phone'])
        self.page.locator(self.FULL_NAME).fill(data['full_name'])
        self.page.locator(self.DATE_OF_BIRTH).fill(data['date_of_birth'])

        gender_value = data['gender']
        if gender_value:
            self.page.locator(self.GENDER).select_option(label=gender_value)

        return self

    def agree_terms(self):
        self.page.locator(self.TERMS_CHECKBOX).click()
        return self

    def submit(self):
        submit_button = self.page.locator(self.SUBMIT).first
        expect(submit_button).to_be_visible(timeout=10000)
        submit_button.click()

        try:
            self.page.wait_for_load_state('networkidle', timeout=10000)
        except TimeoutError:
            pass

        return self

    def get_page_text(self):
        return self.page.locator('body').inner_text()
