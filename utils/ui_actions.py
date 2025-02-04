from selenium import webdriver

class UIActions:
    def __init__(self, driver):
        self.driver = driver

    def open_url(self, url):
        self.driver.get(url)

    def quit_browser(self):
        self.driver.quit()