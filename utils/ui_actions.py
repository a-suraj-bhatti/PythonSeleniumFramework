from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from typing import Optional, Union, List
import yaml
import os

class UIActions:
    def __init__(self, driver):
        self.driver = driver
        self.default_timeout = self._get_default_timeout()
        self.actions = ActionChains(self.driver)

    def _get_default_timeout(self) -> int:
        """Read default timeout from config file"""
        try:
            config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'config.yaml')
            with open(config_path, 'r') as file:
                config = yaml.safe_load(file)
                return config.get('selenium', {}).get('timeout', 10)  # Default to 10 if not specified
        except Exception as e:
            print(f"Warning: Could not load timeout from config file: {e}")
            return 10

    def set_default_timeout(self, timeout: int) -> None:
        """Set a new default timeout"""
        self.default_timeout = timeout

    def _wait_for_element(self, locator: tuple, timeout: Optional[int] = None) -> any:
        """Wait for element to be present and visible"""
        wait_timeout = timeout if timeout is not None else self.default_timeout
        return WebDriverWait(self.driver, wait_timeout).until(
            EC.presence_of_element_located(locator)
        )

    def _wait_for_elements(self, locator: tuple, timeout: Optional[int] = None) -> List:
        """Wait for elements to be present"""
        wait_timeout = timeout if timeout is not None else self.default_timeout
        return WebDriverWait(self.driver, wait_timeout).until(
            EC.presence_of_all_elements_located(locator)
        )

    def _wait_for_clickable(self, locator: tuple, timeout: Optional[int] = None) -> any:
        """Wait for element to be clickable"""
        wait_timeout = timeout if timeout is not None else self.default_timeout
        return WebDriverWait(self.driver, wait_timeout).until(
            EC.element_to_be_clickable(locator)
        )

    # Basic Navigation
    def open_url(self, url: str) -> None:
        """Navigate to specified URL"""
        self.driver.get(url)

    def refresh_page(self) -> None:
        """Refresh current page"""
        self.driver.refresh()

    def go_back(self) -> None:
        """Navigate back"""
        self.driver.back()

    def go_forward(self) -> None:
        """Navigate forward"""
        self.driver.forward()

    # Click Actions
    def click(self, locator: tuple, timeout: Optional[int] = None) -> None:
        """Click element with automatic wait"""
        element = self._wait_for_clickable(locator, timeout)
        try:
            element.click()
        except ElementClickInterceptedException:
            # If regular click fails, try JavaScript click
            self.driver.execute_script("arguments[0].click();", element)

    def double_click(self, locator: tuple, timeout: Optional[int] = None) -> None:
        """Double click element"""
        element = self._wait_for_clickable(locator, timeout)
        self.actions.double_click(element).perform()

    def right_click(self, locator: tuple, timeout: Optional[int] = None) -> None:
        """Right click element"""
        element = self._wait_for_clickable(locator, timeout)
        self.actions.context_click(element).perform()

    # Input Actions
    def type_text(self, locator: tuple, text: str, clear_first: bool = True, timeout: Optional[int] = None) -> None:
        """Type text into element"""
        element = self._wait_for_element(locator, timeout)
        if clear_first:
            element.clear()
        element.send_keys(text)

    def clear_text(self, locator: tuple, timeout: Optional[int] = None) -> None:
        """Clear text from element"""
        element = self._wait_for_element(locator, timeout)
        element.clear()

    def press_key(self, locator: tuple, key: str, timeout: Optional[int] = None) -> None:
        """Press specific key on element"""
        element = self._wait_for_element(locator, timeout)
        element.send_keys(getattr(Keys, key.upper()))

    # Mouse Actions
    def hover(self, locator: tuple, timeout: Optional[int] = None) -> None:
        """Hover over element"""
        element = self._wait_for_element(locator, timeout)
        self.actions.move_to_element(element).perform()

    def drag_and_drop(self, source_locator: tuple, target_locator: tuple, timeout: Optional[int] = None) -> None:
        """Drag and drop element"""
        source = self._wait_for_element(source_locator, timeout)
        target = self._wait_for_element(target_locator, timeout)
        self.actions.drag_and_drop(source, target).perform()

    # Frame Handling
    def switch_to_frame(self, frame_reference: Union[str, int, tuple], timeout: Optional[int] = None) -> None:
        """Switch to frame by index, name/ID, or locator"""
        if isinstance(frame_reference, tuple):
            frame = self._wait_for_element(frame_reference, timeout)
            self.driver.switch_to.frame(frame)
        else:
            self.driver.switch_to.frame(frame_reference)

    def switch_to_default_content(self) -> None:
        """Switch back to default content"""
        self.driver.switch_to.default_content()

    # Window Handling
    def switch_to_window(self, window_index: int = -1) -> None:
        """Switch to window by index (default: last window)"""
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[window_index])

    def close_current_window(self) -> None:
        """Close current window"""
        self.driver.close()

    # Shadow DOM
    def get_shadow_element(self, host_locator: tuple, shadow_css: str, timeout: Optional[int] = None) -> any:
        """Access element within shadow DOM"""
        host = self._wait_for_element(host_locator, timeout)
        shadow_root = self.driver.execute_script('return arguments[0].shadowRoot', host)
        return shadow_root.find_element(By.CSS_SELECTOR, shadow_css)

    # Element State Checks
    def is_visible(self, locator: tuple, timeout: Optional[int] = None) -> bool:
        """Check if element is visible"""
        try:
            self._wait_for_element(locator, timeout or 5)
            return True
        except TimeoutException:
            return False

    def is_enabled(self, locator: tuple, timeout: Optional[int] = None) -> bool:
        """Check if element is enabled"""
        element = self._wait_for_element(locator, timeout)
        return element.is_enabled()

    def is_selected(self, locator: tuple, timeout: Optional[int] = None) -> bool:
        """Check if element is selected"""
        element = self._wait_for_element(locator, timeout)
        return element.is_selected()

    # Element Properties
    def get_text(self, locator: tuple, timeout: Optional[int] = None) -> str:
        """Get element text"""
        element = self._wait_for_element(locator, timeout)
        return element.text

    def get_attribute(self, locator: tuple, attribute: str, timeout: Optional[int] = None) -> str:
        """Get element attribute"""
        element = self._wait_for_element(locator, timeout)
        return element.get_attribute(attribute)

    # Select Operations
    def select_by_text(self, locator: tuple, text: str, timeout: Optional[int] = None) -> None:
        """Select dropdown option by visible text"""
        from selenium.webdriver.support.ui import Select
        element = self._wait_for_element(locator, timeout)
        Select(element).select_by_visible_text(text)

    def select_by_value(self, locator: tuple, value: str, timeout: Optional[int] = None) -> None:
        """Select dropdown option by value"""
        from selenium.webdriver.support.ui import Select
        element = self._wait_for_element(locator, timeout)
        Select(element).select_by_value(value)

    # JavaScript Operations
    def execute_script(self, script: str, *args) -> any:
        """Execute JavaScript code"""
        return self.driver.execute_script(script, *args)

    def scroll_into_view(self, locator: tuple, timeout: Optional[int] = None) -> None:
        """Scroll element into view"""
        element = self._wait_for_element(locator, timeout)
        self.execute_script("arguments[0].scrollIntoView(true);", element)

    # Alert Handling
    def accept_alert(self, timeout: Optional[int] = None) -> None:
        """Accept alert"""
        WebDriverWait(self.driver, timeout or self.default_timeout).until(EC.alert_is_present())
        self.driver.switch_to.alert.accept()

    def dismiss_alert(self, timeout: Optional[int] = None) -> None:
        """Dismiss alert"""
        WebDriverWait(self.driver, timeout or self.default_timeout).until(EC.alert_is_present())
        self.driver.switch_to.alert.dismiss()

    def get_alert_text(self, timeout: Optional[int] = None) -> str:
        """Get alert text"""
        WebDriverWait(self.driver, timeout or self.default_timeout).until(EC.alert_is_present())
        return self.driver.switch_to.alert.text

    # Cookie Handling
    def add_cookie(self, cookie_dict: dict) -> None:
        """Add cookie to browser"""
        self.driver.add_cookie(cookie_dict)

    def delete_all_cookies(self) -> None:
        """Delete all cookies"""
        self.driver.delete_all_cookies()

    # Screenshot
    def take_screenshot(self, filename: str) -> None:
        """Take screenshot of current page"""
        self.driver.save_screenshot(filename)

    def take_element_screenshot(self, locator: tuple, filename: str, timeout: Optional[int] = None) -> None:
        """Take screenshot of specific element"""
        element = self._wait_for_element(locator, timeout)
        element.screenshot(filename)

    def quit_browser(self) -> None:
        """Quit browser"""
        self.driver.quit()