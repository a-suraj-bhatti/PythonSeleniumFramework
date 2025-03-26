# tests/base_ui_test.py
from selenium.webdriver.remote.webdriver import WebDriver
from utils.ui_actions import UIActions
from pages.page_factory import PageFactory

class BaseUITest:
    driver: WebDriver
    ui_actions: UIActions
    page: PageFactory