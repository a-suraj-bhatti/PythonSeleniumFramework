# Selenium & API Automation Testing Framework

This framework is designed to help you perform robust end-to-end testing for web applications and APIs. It supports advanced features like parallel test execution, configurable environments (local or cloud), cross-browser testing, and uses the Page Object Model (POM) for maintainable UI tests. Additionally, it offers simple and reusable utilities for both UI actions and API interactions.

## Features

- **Cross-Browser Testing (Local & Cloud):**
  - Local execution supports multiple browsers (Chrome, Firefox, Edge).
  - Cloud integration with BrowserStack or Sauce Labs is available via configuration.
  - Command-line options override config file values for quick switching.
  
- **Parallel Test Execution:**
  - Use [pytest-xdist](https://pypi.org/project/pytest-xdist/) to run tests concurrently on multiple browsers.

- **Page Object Model (POM):**
  - Centralized page objects to encapsulate UI interactions.
  - Example page (`pages/example_page.py`) demonstrates a basic use case.

- **Separation of Concerns:**
  - **UI Tests:** Use Selenium WebDriver wrapped inside common actions (`utils/ui_actions.py`).
  - **API Tests:** Utilize a common API actions utility based on `requests` (`utils/api_actions.py`).

- **Flexible Configuration:**
  - All key settings (execution mode, browser list, URLs, cloud credentials) are maintained in a YAML file (`config/config.yaml`).
  - Command-line arguments (e.g., `--execution`, `--browsers`) take precedence over configuration file values.

- **Test Organization:**
  - Tests for UI and API are separated into different directories (`tests/test_ui.py` and `tests/test_api.py`).
  - Auto-attaching of the UI fixtures to test classes (only for tests marked with `@pytest.mark.ui`) so that API tests aren’t affected.

## Directory Structure

```
automation_framework/
├── config/
│   └── config.yaml            # Main configuration file
├── pages/
│   ├── base_page.py           # Base class for all page objects
│   └── example_page.py        # Example page using the POM
├── tests/
│   ├── test_ui.py             # UI tests using Selenium
│   └── test_api.py            # API tests using requests
├── utils/
│   ├── browser_setup.py       # Logic to instantiate WebDriver (local/cloud)
│   ├── ui_actions.py          # Common UI actions (open URL, quit browser)
│   └── api_actions.py         # Common API actions (GET, POST, etc.)
├── conftest.py                # Pytest fixtures and test parameterization
├── pytest.ini                 # Pytest configuration file (markers, etc.)
└── requirements.txt           # Python dependencies
```

## Setup & Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/a-suraj-bhatti/PythonSeleniumFramework.git
   cd automation_framework
   ```

2. **Create a Python Virtual Environment:**

   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment:**

   - On **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - On **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Edit the `config/config.yaml` file to set your environment:

```yaml
execution: local               # Options: "local" or "cloud"
browsers:
  - chrome
  - firefox
base_url: "https://www.saucedemo.com/"
api_base_url: "http://api.example.com"
cloud_provider:
  name: "browserstack"         # Options: "browserstack" or "saucelabs"
  username: "your_username"
  access_key: "your_access_key"
```

- **Local Execution:** The tests will run on your specified browsers.
- **Cloud Execution:** Change `execution` to `cloud` for remote runs (make sure your `cloud_provider` section is properly populated).

You can override any of these using command-line options when running tests (e.g., `pytest --execution=cloud --browsers="chrome,firefox"`).

## How to Run the Tests

### Running UI Tests

UI tests are written under `tests/test_ui.py` and are marked with `@pytest.mark.ui`. They run on multiple browsers as defined in the configuration or by CLI overrides.

Run UI tests with:

```bash
pytest -m ui
```

For parallel execution (if you have pytest-xdist installed):

```bash
pytest -m ui -n 4
```

### Running API Tests

API tests are written under `tests/test_api.py` and use the `api_setup` fixture.

Run API tests with:

```bash
pytest -m api
```

**Note:** These tests are not influenced by the UI-specific fixtures, so no browsers will be launched for API tests.

## Advanced Usage

- **Command-Line Overrides:**
  - Override the execution type: `pytest --execution=cloud`
  - Provide a custom list of browsers: `pytest --browsers="chrome,firefox,edge"`
  - Override URLs: `pytest --base_url="https://new-url.com" --api_base_url="http://new-api.com"`

- **Parallel Execution:**
  With `pytest-xdist`, you can run tests in parallel across multiple processes:
  ```bash
  pytest -m ui -n 4
  ```

- **Cloud Testing:**
  Ensure your cloud environment credentials are correctly set in `config/config.yaml` if running in cloud mode.

## Contributing

Contributions are welcome! Feel free to fork the repository and submit pull requests for improvements, additional features, or bug fixes. Please ensure that your code follows the existing style and includes tests where appropriate.



---

Happy Testing!
