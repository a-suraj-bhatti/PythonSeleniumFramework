import pytest
from pages.page_factory import page
from tests.base_ui_test import BaseUITest

@pytest.mark.ui
class TestExamplePage(BaseUITest):
    def test_example_page(self):
        # No need to unpack: self.driver and self.ui_actions are automatically injected.
        self.ui_actions.open_url("https://www.saucedemo.com/")
        assert page.example_page.get_example_text() == "Swag Labs"

    def test_example_page2(self):
        self.ui_actions.open_url("https://www.saucedemo.com/")
        assert page.example_page.get_example_text() == "Swag Labs1"