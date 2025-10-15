"""
Pytest configuration and fixtures.
"""

import os
import pytest
import json
import base64
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from pytest_html import extras

from utils.logger import TestLogger
from config.config import (
    BROWSER_TYPE,
    HEADLESS,
    SCREENSHOT_DIR,
    TAKE_SCREENSHOT_ON_FAILURE,
)


def pytest_configure(config):
    """Configure pytest."""
    # Create screenshots directory if it doesn't exist
    if not os.path.exists(SCREENSHOT_DIR):
        os.makedirs(SCREENSHOT_DIR)

    config.addinivalue_line("markers", "examples: mark a test as an example test")
    config.addinivalue_line(
        "markers", "laraigo: mark a test as a Laraigo-specific test"
    )
    config.addinivalue_line(
        "markers", "laraigo_ui: mark a test as a Laraigo-UI debug test"
    )

    # Add custom CSS via environment variable which pytest-html will pick up
    css = """
    .test-data { margin: 15px 0; border: 1px solid #ddd; padding: 10px; border-radius: 5px; background-color: #f8f8f8; }
    .test-data pre { white-space: pre-wrap; max-height: 300px; overflow: auto; margin-top: 10px; }
    .test-data h3 { margin-top: 0; color: #333; }
    """
    if hasattr(config, "_metadata"):
        config._metadata["Test Data CSS"] = css


@pytest.fixture(scope="function")
def driver(request):
    """Fixture for WebDriver."""
    driver = _setup_driver()
    yield driver
    driver.quit()


TEST_DATA = {}
test_logger = TestLogger()


@pytest.fixture(scope="function")
def test_data(request):
    """Fixture to store test data for reporting."""

    def _save_data(sent_message=None, response_text=None, response_time=None):
        test_id = request.node.nodeid
        if test_id in TEST_DATA:
            if sent_message is not None:
                TEST_DATA[test_id]["sent_message"] = sent_message
            if response_text is not None:
                TEST_DATA[test_id]["response_text"] = response_text
            if response_time is not None:
                TEST_DATA[test_id]["response_time"] = response_time

    return _save_data


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_protocol(item, nextitem):
    """Capture start and end time of test."""
    test_id = item.nodeid
    TEST_DATA[test_id] = {
        "start_time": time.time(),
        "sent_message": None,
        "response_text": None,
        "error": None,
        "screenshot": None,
        "duration": None,
    }
    # Log test start
    test_logger.log_test_start(test_id)
    yield


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Take screenshot on test failure and collect test data."""
    outcome = yield
    report = outcome.get_result()
    test_id = item.nodeid

    # For parametrized tests, get the parameter value
    if hasattr(item, "callspec"):
        param_values = item.callspec.params.values()
        if param_values:
            param_str = next(iter(param_values))
            if isinstance(param_str, str):
                TEST_DATA[test_id]["sent_message"] = param_str

    # Store end time and calculate duration
    if test_id in TEST_DATA:
        if report.when == "call":
            duration = time.time() - TEST_DATA[test_id]["start_time"]
            TEST_DATA[test_id]["duration"] = duration

            # Include response_time in the HTML report if it exists
            if "response_time" in TEST_DATA[test_id]:
                TEST_DATA[test_id]["response_time_ms"] = round(
                    TEST_DATA[test_id]["response_time"] * 1000, 2
                )

            # Log test completion with duration and status
            status = "PASS" if report.passed else "FAIL"
            error_msg = None
            if not report.passed:
                error_msg = (
                    report.longrepr.reprcrash.message
                    if hasattr(report, "longrepr")
                    and hasattr(report.longrepr, "reprcrash")
                    else "Test failed without detailed error message"
                )
            test_logger.log_test_end(test_id, status, duration, error_msg)

            # If the test has a chatbot_page fixture and it was accessed, try to get messages
            if hasattr(item, "funcargs"):
                # Get messages from the chatbot page if available
                if "chatbot_page" in item.funcargs:
                    chatbot_page = item.funcargs["chatbot_page"]
                    if hasattr(chatbot_page, "get_all_bot_messages") and hasattr(
                        chatbot_page, "get_all_user_messages"
                    ):
                        try:
                            bot_messages = chatbot_page.get_all_bot_messages()
                            user_messages = chatbot_page.get_all_user_messages()
                            if bot_messages:
                                TEST_DATA[test_id]["response_text"] = bot_messages[-1]
                            if user_messages and not TEST_DATA[test_id]["sent_message"]:
                                TEST_DATA[test_id]["sent_message"] = user_messages[-1]
                        except Exception as e:
                            TEST_DATA[test_id][
                                "error"
                            ] = f"Error getting messages: {str(e)}"

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver", None)
        if driver and TAKE_SCREENSHOT_ON_FAILURE:
            screenshot_name = f"failure_{item.name}"
            screenshot_path = take_screenshot(driver, screenshot_name)
            if screenshot_path and test_id in TEST_DATA:
                TEST_DATA[test_id]["screenshot"] = screenshot_path
                TEST_DATA[test_id]["error"] = (
                    report.longrepr.reprcrash.message
                    if hasattr(report, "longrepr")
                    and hasattr(report.longrepr, "reprcrash")
                    else "Test failed"
                )

                # Add the screenshot to the HTML report
                try:
                    with open(screenshot_path, "rb") as img_file:
                        screenshot_base64 = base64.b64encode(img_file.read()).decode(
                            "utf-8"
                        )
                    report.extras = [
                        extras.html(
                            f'<div class="test-data"><h3>Test Data</h3><pre>{json.dumps(TEST_DATA[test_id], indent=2)}</pre></div>'
                        ),
                        extras.image(screenshot_base64, screenshot_name),
                    ]
                except Exception as e:
                    report.extras = [
                        extras.html(
                            f'<div class="test-data"><h3>Test Data</h3><pre>{json.dumps(TEST_DATA[test_id], indent=2)}</pre><p>Error loading screenshot: {str(e)}</p></div>'
                        )
                    ]

    # Add test data to the report for passed tests too
    if report.when == "call" and report.passed and test_id in TEST_DATA:
        # Create a more user-friendly HTML report
        test_data_html = '<div class="test-data"><h3>Test Data</h3><table style="width:100%; border-collapse: collapse;">'

        # Add message and response rows if they exist
        if TEST_DATA[test_id].get("sent_message"):
            test_data_html += f'<tr><td style="padding:8px; border:1px solid #ddd; font-weight:bold;">Sent Message:</td><td style="padding:8px; border:1px solid #ddd;">{TEST_DATA[test_id]["sent_message"]}</td></tr>'

        if TEST_DATA[test_id].get("response_text"):
            # Format the response text (could be a list or string)
            response = TEST_DATA[test_id]["response_text"]
            if isinstance(response, list):
                response_formatted = "<br>".join(response)
            else:
                response_formatted = str(response)
            test_data_html += f'<tr><td style="padding:8px; border:1px solid #ddd; font-weight:bold;">Bot Response:</td><td style="padding:8px; border:1px solid #ddd;">{response_formatted}</td></tr>'

        # Add response time if it exists
        if TEST_DATA[test_id].get("response_time"):
            response_time_ms = round(TEST_DATA[test_id]["response_time"] * 1000, 2)
            test_data_html += f'<tr><td style="padding:8px; border:1px solid #ddd; font-weight:bold;">Response Time:</td><td style="padding:8px; border:1px solid #ddd;">{response_time_ms} ms</td></tr>'

        # Add test duration
        if TEST_DATA[test_id].get("duration"):
            duration_sec = round(TEST_DATA[test_id]["duration"], 2)
            test_data_html += f'<tr><td style="padding:8px; border:1px solid #ddd; font-weight:bold;">Test Duration:</td><td style="padding:8px; border:1px solid #ddd;">{duration_sec} sec</td></tr>'

        test_data_html += "</table>"

        # Add raw data in a collapsible section
        test_data_html += f'<details><summary style="margin-top:10px; cursor:pointer;">Raw Test Data</summary><pre>{json.dumps(TEST_DATA[test_id], indent=2)}</pre></details></div>'

        report.extras = [extras.html(test_data_html)]


@pytest.hookimpl(hookwrapper=True)
def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Add test data summary to HTML report."""
    yield

    # Create a summary JSON file with all test data
    if config.getoption("htmlpath"):
        html_path = config.getoption("htmlpath")

        # Prepare a clean version of test data for JSON output
        summary_data = {}
        for test_id, data in TEST_DATA.items():
            test_name = test_id.split("::")[-1]
            clean_data = {
                "name": test_name,
                "sent_message": data.get("sent_message", None),
                "response_text": data.get("response_text", None),
                "duration": round(data.get("duration", 0), 2),
                "error": data.get("error", None),
                "screenshot": (
                    os.path.basename(data.get("screenshot", ""))
                    if data.get("screenshot")
                    else None
                ),
                "status": "failed" if data.get("error") else "passed",
            }
            summary_data[test_id] = clean_data

        try:
            # Add the summary to the HTML report
            if os.path.exists(html_path):
                with open(html_path, "r", encoding="utf-8") as f:
                    html_content = f.read()

                # Create a summary div at the end of the body
                summary_div = f"""
                <div id="test-data-summary" style="margin: 20px; padding: 15px; border: 1px solid #ddd; border-radius: 5px;">
                    <h2>Test Data Summary</h2>
                    <details>
                        <summary>Click to view JSON summary of all tests</summary>
                        <pre style="max-height: 500px; overflow: auto;">{json.dumps(summary_data, indent=2)}</pre>
                    </details>
                </div>
                """

                # Insert before the closing body tag
                html_content = html_content.replace(
                    "</body>", f"{summary_div}\n</body>"
                )

                with open(html_path, "w", encoding="utf-8") as f:
                    f.write(html_content)
        except Exception as e:
            print(f"Error creating test data summary: {e}")


def take_screenshot(driver, name):
    """Take a screenshot and save it to the screenshots directory."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{name}.png"
    filepath = os.path.join(SCREENSHOT_DIR, filename)

    try:
        driver.save_screenshot(filepath)
        print(f"Screenshot saved: {filepath}")
        return filepath
    except Exception as e:
        print(f"Failed to take screenshot: {e}")
        return None


def _setup_driver():
    """Set up the WebDriver based on configuration."""
    if BROWSER_TYPE.lower() == "chrome":
        options = webdriver.ChromeOptions()
        if HEADLESS:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        # Add additional options to improve headless stability
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-infobars")
        return webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )

    elif BROWSER_TYPE.lower() == "firefox":
        options = webdriver.FirefoxOptions()
        if HEADLESS:
            options.add_argument("--headless")
        return webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()), options=options
        )

    elif BROWSER_TYPE.lower() == "edge":
        options = webdriver.EdgeOptions()
        if HEADLESS:
            options.add_argument("--headless")
        return webdriver.Edge(
            service=EdgeService(EdgeChromiumDriverManager().install()), options=options
        )

    else:
        raise ValueError(f"Unsupported browser type: {BROWSER_TYPE}")
