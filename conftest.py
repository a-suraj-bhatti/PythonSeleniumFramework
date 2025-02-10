import pytest
import yaml
from utils.browser_setup import get_driver
from utils.ui_actions import UIActions
from utils.api_actions import APIActions
from py.xml import html
import os

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
            metafunc.parametrize("browser_name", browsers, indirect=True)
        else:
            metafunc.parametrize("browser_name", ["cloud"], indirect=True)

# Fixture to load configuration and override with command-line arguments (if provided)
@pytest.fixture(scope="session")
def config_data(request):
    config_path = os.path.join(os.path.dirname(__file__), "config", "config.yaml")
    with open(config_path, "r") as file:
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

# Define the browser_name fixture. It now safely returns the parameter using getattr.
@pytest.fixture
def browser_name(request):
    param = getattr(request, "param", None)
    if param is not None:
        return param
    return "chrome"  # default fallback

# Fixture for UI tests; driver is created based on the environment & browser_name, using config overrides.
@pytest.fixture(scope="function")
def ui_setup(request, browser_name, config_data):
    # Record the browser name on the test node for reporting purposes.
    request.node.browser = browser_name
    if config_data.get("execution", "local") == "cloud":
        driver = get_driver(config_dict=config_data)
    else:
        driver = get_driver(browser_override=browser_name, config_dict=config_data)
    ui_actions = UIActions(driver)
    yield driver, ui_actions
    ui_actions.quit_browser()

# Autouse fixture to attach ui_setup for UI tests only.
# It attaches *only* for tests marked with @pytest.mark.ui and defined in a class.
@pytest.fixture(autouse=True)
def attach_ui_setup(request, browser_name):
    if request.cls is not None and request.node.get_closest_marker("ui"):
        ui_setup_instance = request.getfixturevalue("ui_setup")
        request.cls.driver, request.cls.ui_actions = ui_setup_instance

# Fixture for API tests uses the overridden API base URL.
@pytest.fixture(scope="function")
def api_setup(config_data):
    return APIActions(config_data["api_base_url"])

def pytest_configure(config):
    # Set default HTML report output if not specified.
    if not config.option.htmlpath:
        config.option.htmlpath = 'report.html'
    # Ensure that a metadata dictionary exists.
    if not hasattr(config, 'metadata'):
        config.metadata = {}
    config.metadata['Project Name'] = 'Selenium & API Automation Testing Framework'

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # This hook is called when each test's report is being generated.
    outcome = yield
    rep = outcome.get_result()
    # Attach the browser information (if set) from the test node to the report.
    rep.browser = getattr(item, "browser", "N/A")

def pytest_html_results_table_header(cells):
    # Insert the header for a new column "Browser" into the HTML report.
    cells.insert(2, html.th('Browser'))

def pytest_html_results_table_row(report, cells):
    # Safely insert the browser value into the HTML report row.
    browser = getattr(report, "browser", "N/A")
    cells.insert(2, html.td(browser))    