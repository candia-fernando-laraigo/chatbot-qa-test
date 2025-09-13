"""
Configuration settings for the chatbot QA tests.
"""

import os

# Base URL configuration
# Can be either a web URL (https://) or a local file path (file://)
BASE_URL: str = (
    f"file://{os.path.abspath(os.path.join(os.path.dirname(__file__), '../simple-web/index.html'))}"
)

# Browser configuration
BROWSER_TYPE: str = "chrome"  # Options: chrome, firefox, edge
HEADLESS: bool = True  # Set to False for debugging visual issues

# Test execution configuration
PYTEST_WORKERS: int = 16  # Number of parallel test executions
PARALLEL_PROCESSES: int = 2  # Number of parallel processes of pytest-xdist
IMPLICIT_WAIT: int = 60  # Default wait time in seconds
EXPLICIT_WAIT: int = 60  # Default explicit wait time in seconds

# Test data
TEST_DATA_DIR: str = os.path.join(os.path.dirname(__file__), "../test_data")

# Screenshots
SCREENSHOT_DIR: str = os.path.join(os.path.dirname(__file__), "../screenshots")
TAKE_SCREENSHOT_ON_FAILURE: bool = True
