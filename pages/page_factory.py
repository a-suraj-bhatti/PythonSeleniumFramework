from pages.example_page import ExamplePage
from tests.base_ui_test import BaseUITest

class PageFactory:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @property
    def driver(self):
        return BaseUITest.driver
    
    @property
    def example_page(self):
        return ExamplePage(self.driver)

# Create a single instance to be imported
page = PageFactory()

# Add additional properties for other pages as needed. 