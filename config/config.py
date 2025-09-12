"""
Configuration settings for the chatbot QA tests.
"""

import os

# Base URL configuration
# Can be either a web URL (https://) or a local file path (file://)
BASE_URL = f"file://{os.path.abspath(os.path.join(os.path.dirname(__file__), '../simple-web/index.html'))}"

# Browser configuration
BROWSER_TYPE = 'chrome'  # Options: chrome, firefox, edge
HEADLESS = True  # Set to False for debugging visual issues

# Test execution configuration
PARALLEL_EXECUTION = 10  # Number of parallel test executions
IMPLICIT_WAIT = 60  # Default wait time in seconds
EXPLICIT_WAIT = 60  # Default explicit wait time in seconds

# Test data
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), '../test_data')

# Screenshots
SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), '../screenshots')
TAKE_SCREENSHOT_ON_FAILURE = True