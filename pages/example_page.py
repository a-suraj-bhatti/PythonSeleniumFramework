from selenium.webdriver.common.by import By
from .base_page import BasePage

class ExamplePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.example_element = (By.XPATH, '//div[@class="login_logo"]')

    def get_example_text(self):
        element = self.wait_for_element(self.example_element)
        return element.text