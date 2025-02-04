import pytest
from pages.example_page import ExamplePage

@pytest.mark.ui
def test_example_page(ui_setup):
    driver, ui_actions = ui_setup
    ui_actions.open_url("https://www.saucedemo.com/")
    page = ExamplePage(driver)
    assert page.get_example_text() == "Swag Labs"

def test_example_page2(ui_setup):
    driver, ui_actions = ui_setup
    ui_actions.open_url("https://www.saucedemo.com/")
    page = ExamplePage(driver)
    assert page.get_example_text() == "Swag Labs"