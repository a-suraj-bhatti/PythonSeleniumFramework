from pages.example_page import ExamplePage
from typing import Optional
from selenium.webdriver.remote.webdriver import WebDriver

class PageFactory:
    def __init__(self, driver: Optional[WebDriver] = None):
        self._driver = driver
    
    @property
    def driver(self) -> WebDriver:
        return self._driver

    @driver.setter
    def driver(self, value: WebDriver) -> None:
        self._driver = value
    
    @property
    def example_page(self) -> ExamplePage:
        return ExamplePage(self.driver)

# Instead of a singleton, create a factory function
def create_page_factory(driver: Optional[WebDriver] = None) -> PageFactory:
    return PageFactory(driver)

# Add additional properties for other pages as needed. 