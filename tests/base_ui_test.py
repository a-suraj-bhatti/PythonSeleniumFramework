# tests/base_ui_test.py
from selenium.webdriver.remote.webdriver import WebDriver
from utils.ui_actions import UIActions

class BaseUITest:
    driver: WebDriver
    ui_actions: UIActions