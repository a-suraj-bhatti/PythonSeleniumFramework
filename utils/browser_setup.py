from selenium import webdriver
import yaml
from selenium.webdriver.firefox.options import Options as FirefoxOptions


def get_driver(browser_override=None, config_dict=None):
    # Use the provided config dictionary if available; otherwise load from file.
    if config_dict is None:
        with open('config/config.yaml', 'r') as file:
            config = yaml.safe_load(file)
    else:
        config = config_dict
    
    # Use override if provided, else get from config (defaulting to chrome).
    browser = browser_override if browser_override else config.get('browser', 'chrome')

    # Check the execution mode from config ("local" or "cloud")
    execution = config.get("execution", "local")
    if execution == "cloud":
        # In cloud mode, use cloud_provider credentials.
        cloud = config.get('cloud_provider', {})
        if cloud.get("username") and cloud.get("access_key"):
            provider = cloud.get("name", "").lower()
            if provider == "browserstack":
                desired_cap = {
                    "browserName": browser,
                    "browserstack.user": cloud.get("username"),
                    "browserstack.key": cloud.get("access_key"),
                    "name": "Selenium Test"
                }
                remote_url = "https://hub-cloud.browserstack.com/wd/hub"
                return webdriver.Remote(command_executor=remote_url, desired_capabilities=desired_cap)
            elif provider == "saucelabs":
                desired_cap = {
                    "browserName": browser,
                    "username": cloud.get("username"),
                    "accessKey": cloud.get("access_key"),
                    "name": "Selenium Test"
                }
                remote_url = "https://ondemand.saucelabs.com/wd/hub"
                return webdriver.Remote(command_executor=remote_url, desired_capabilities=desired_cap)
            else:
                raise ValueError(f"Unsupported cloud provider: {provider}")
        else:
            raise ValueError("Cloud execution requires valid cloud_provider credentials.")
    else:
        # Local execution ignores cloud_provider settings.
        if browser == 'chrome':
            from selenium.webdriver.chrome.options import Options as ChromeOptions
            options = ChromeOptions()
            options.enable_bidi = True
            return webdriver.Chrome(options=options)
        elif browser == 'edge':
            from selenium.webdriver.edge.options import Options as EdgeOptions
            options = EdgeOptions()
            options.enable_bidi = True
            return webdriver.Edge(options=options)
        elif browser == 'firefox':
            options = FirefoxOptions()
            options.enable_bidi = True
            return webdriver.Firefox(options=options)
        else:
            raise ValueError(f"Unsupported browser: {browser}") 