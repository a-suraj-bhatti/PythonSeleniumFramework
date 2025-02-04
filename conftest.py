import pytest
import yaml
from utils.browser_setup import get_driver
from utils.ui_actions import UIActions
from utils.api_actions import APIActions

def pytest_addoption(parser):
    parser.addoption(
        "--execution",
        action="store",
        default=None,
        help="Override execution mode (local or cloud) from config"
    )
    parser.addoption(
        "--browsers",
        action="store",
        default=None,
        help="Override comma-separated list of browsers for local execution. E.g., chrome,firefox"
    )
    parser.addoption(
        "--base_url",
        action="store",
        default=None,
        help="Override base_url from config"
    )
    parser.addoption(
        "--api_base_url",
        action="store",
        default=None,
        help="Override API base_url from config"
    )

def pytest_generate_tests(metafunc):
    if "browser_name" in metafunc.fixturenames:
        # Determine execution mode: command-line overrides if provided, else from config file.
        execution_cli = metafunc.config.getoption("--execution")
        if execution_cli:
            execution = execution_cli
        else:
            with open("config/config.yaml", "r") as file:
                conf = yaml.safe_load(file)
            execution = conf.get("execution", "local")

        if execution == "local":
            browsers_cli = metafunc.config.getoption("--browsers")
            if browsers_cli:
                browsers = [b.strip() for b in browsers_cli.split(",")]
            else:
                with open("config/config.yaml", "r") as file:
                    conf = yaml.safe_load(file)
                browsers = conf.get("browsers", ["chrome"])
            metafunc.parametrize("browser_name", browsers)
        else:
            metafunc.parametrize("browser_name", ["cloud"])

# Fixture to load configuration and override with command-line arguments (if provided)
@pytest.fixture(scope="session")
def config_data(request):
    with open("config/config.yaml", "r") as file:
        config = yaml.safe_load(file)
    
    # Override execution mode if provided via command-line
    execution_override = request.config.getoption("--execution")
    if execution_override:
        config["execution"] = execution_override

    # Override browsers if provided via command-line
    browsers_override = request.config.getoption("--browsers")
    if browsers_override:
        config["browsers"] = [b.strip() for b in browsers_override.split(",")]

    # Override base_url and api_base_url
    base_url_override = request.config.getoption("--base_url")
    if base_url_override:
        config["base_url"] = base_url_override

    api_base_url_override = request.config.getoption("--api_base_url")
    if api_base_url_override:
        config["api_base_url"] = api_base_url_override

    return config

# Fixture for UI tests; driver is created based on the environment & browser_name, using config overrides.
@pytest.fixture(scope="function")
def ui_setup(request, browser_name, config_data):
    if config_data.get("execution", "local") == "cloud":
        driver = get_driver(config_dict=config_data)
    else:
        driver = get_driver(browser_override=browser_name, config_dict=config_data)
    ui_actions = UIActions(driver)
    yield driver, ui_actions
    # Teardown: Quit the browser after the test
    ui_actions.quit_browser()

# Autouse fixture to attach ui_setup to test classes
@pytest.fixture(autouse=True)
def attach_ui_setup(request, ui_setup):
    # Only attach if the test is part of a class (i.e. there's a "self")
    if request.cls is not None:
        request.cls.driver, request.cls.ui_actions = ui_setup

# Fixture for API tests uses the overridden API base URL.
@pytest.fixture(scope="function")
def api_setup(config_data):
    return APIActions(config_data["api_base_url"])    