from pages.example_page import ExamplePage

class PageFactory:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._driver = None
        return cls._instance
    
    @property
    def driver(self):
        return self._driver

    @driver.setter
    def driver(self, value):
        self._driver = value
    
    @property
    def example_page(self):
        return ExamplePage(self.driver)

# Create a single instance to be imported
page = PageFactory()

# Add additional properties for other pages as needed. 