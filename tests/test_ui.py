import pytest
from tests.base_ui_test import BaseUITest

@pytest.mark.ui
class TestExamplePage(BaseUITest):
    def test_example_page(self):
        # Use self.page instead of the global page
        self.ui_actions.open_url("https://www.saucedemo.com/")
        assert self.page.example_page.get_example_text() == "Swag Labs"

    def test_example_page2(self):
        self.ui_actions.open_url("https://www.saucedemo.com/")
        assert self.page.example_page.get_example_text() == "Swag Labs"