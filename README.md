# Chatbot QA Test Automation

A simple yet powerful test automation framework for testing web-based chatbot interfaces using pytest.

## Project Structure

```
chatbot-qa-test/
├── config/                 # Configuration files
│   └── config.py           # Main configuration settings
├── conftest.py             # Pytest configuration and fixtures
├── pages/                  # Page Object Models
│   └── chatbot_page.py     # Chatbot interface page object
├── tests/                  # Test suites organized by functionality
│   ├── ui/                 # UI component tests
│   ├── messages/           # Message sending/receiving tests
│   └── responses/          # Chatbot response validation tests
├── simple-web/             # Sample web application for testing
│   ├── index.html          # HTML for the chatbot interface
│   ├── script.js           # JavaScript for chatbot functionality
│   └── style.css           # CSS styles for the chatbot
├── main.py                 # Main test runner script
├── Makefile                # Build automation
├── README.md               # Project documentation
└── TEST_CASES.md           # Test case documentation
```

## Features

- **Pytest Framework** for powerful, flexible testing
- **Page Object Model (POM)** design pattern for better maintainability
- **Parallel test execution** with pytest-xdist
- **Modular test organization** with pytest markers
- **Configurable** browser, headless mode, and other settings
- **Screenshot capture** on test failures
- **Detailed HTML reports** using pytest-html
- **Fixtures** for efficient test setup and teardown

## Prerequisites

- Python 3.7 or higher
- Chrome browser (Firefox and Edge are also supported)
- Make (optional, for using Makefile commands)

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd chatbot-qa-test
   ```

2. Set up the environment:
   ```bash
   make setup
   ```
   
   Or without Make:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

## Running Tests

### Using Makefile

Run all tests:
```bash
make test
```

Run specific test suites:
```bash
make test-ui          # UI tests only
make test-responses   # Response tests only
```

Run tests in parallel:
```bash
make test-parallel
```

Run tests directly with pytest:
```bash
make pytest
```

View HTML report:
```bash
make report
```

Clean up:
```bash
make clean
```

### Without Makefile

Run all tests with the test runner:
```bash
python main.py
```

Run specific test suites with the test runner:
```bash
python main.py --suite ui
python main.py --suite messages
python main.py --suite responses
```

Run tests in parallel with the test runner:
```bash
python main.py --parallel 3
```

Run tests directly with pytest:
```bash
pytest                           # Run all tests
pytest -v                        # Verbose output
pytest -m ui                     # Run UI tests only
pytest -m messages               # Run message tests only
pytest -m responses              # Run response tests only
pytest -n 3                      # Run in parallel with 3 workers
pytest --html=report.html        # Generate HTML report
```

## Configuration

You can customize test execution by modifying the `config/config.py` file or by setting environment variables:

- `BASE_URL` - The URL of the application to test
- `BROWSER_TYPE` - Browser to use (chrome, firefox, edge)
- `HEADLESS` - Run browser in headless mode (True/False)
- `PARALLEL_EXECUTION` - Number of parallel test executions
- `IMPLICIT_WAIT` - Default implicit wait time in seconds
- `EXPLICIT_WAIT` - Default explicit wait time in seconds
- `TAKE_SCREENSHOT_ON_FAILURE` - Take screenshot on test failure (True/False)

## Adding New Tests

1. Create a new test file in the appropriate directory under `tests/`
2. Extend the `BaseTest` class from `utils/base_test.py`
3. Use the Page Object Model from `pages/chatbot_page.py`
4. Run your tests using the main test runner
