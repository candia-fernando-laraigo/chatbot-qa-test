"""
Configuration settings for the chatbot QA tests.
"""

import os

# Browser configuration
BROWSER_TYPE: str = "chrome"  # Options: chrome, firefox, edge
HEADLESS: bool = True  # Set to False for debugging visual issues

LARAIGO_CHATBOT_PROD: str = "https://demos.laraigo.com/QAOmar/Automatizacion.html"
LARAIGO_CHATBOT_TEST: str = "https://demos.laraigo.com/QAOmar/AutomatizacionTST.html"

PAGE_URL: str = LARAIGO_CHATBOT_TEST
PAGE_TIMEOUT: int = 300

PYTEST_WORKERS: int = 5
TEST_DATA_DIR: str = os.path.join(os.path.dirname(__file__), "../test_data")
SCREENSHOT_DIR: str = os.path.join(os.path.dirname(__file__), "../screenshots")
TAKE_SCREENSHOT_ON_FAILURE: bool = True
