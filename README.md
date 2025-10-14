# Chatbot QA Test Automation

A test automation framework for validating web-based chatbot interfaces using pytest and Selenium WebDriver.

## Documentation

This project includes comprehensive documentation to help you get started:

- [User Manual](docs/USER_MANUAL.md) - Step-by-step instructions for using the framework
- [Complete Documentation](docs/DOCUMENTATION.md) - Detailed technical documentation
- [Quick Reference](docs/QUICK_REFERENCE.md) - Handy commands and patterns
- [Execution Flowchart](docs/FLOWCHART.md) - Visual representation of the test execution flow
- [Test Cases - Laraigo](docs/TEST_CASES_LARAIGO.md) - Specific test cases for Laraigo chatbot
- [Test Cases - Examples](docs/TEST_CASES_EXAMPLE.md) - Sample test cases

## Key Features

- **Page Object Model** pattern for maintainable test code
- **Parallel test execution** for faster results
- **Screenshot capture** on test failures
- **Detailed HTML reports** with response time metrics
- **Configurable** browser, headless mode, and wait times
- **Modular architecture** for easy expansion

## Prerequisites

- Python 3.7 or higher
- Chrome browser (Firefox and Edge also supported)
- Make (optional, for Makefile commands)

## Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/candia-fernando-laraigo/chatbot-qa-test
   cd chatbot-qa-test
   ```

2. Set up the environment:
   ```bash
   make setup
   ```

3. Run the tests:
   ```bash
   make test
   ```

## Available Commands

```bash
make setup          # Set up the environment
make test           # Run all Laraigo tests
make test-examples  # Run example tests only
make report         # Open the latest HTML report
make clean          # Clean up temporary files
```

Or use the test runner directly:

```bash
python main.py              # Run all tests
python main.py --suite examples  # Run only example tests
python main.py --parallel 4      # Run with 4 parallel workers
python main.py -v                # Run with verbose output
```

## Configuration

You can customize test execution by modifying `config/config.py`:

- Browser type and headless mode
- Base URL for testing
- Wait times and timeouts
- Screenshot settings
- Parallel execution settings

See the [Complete Documentation](docs/DOCUMENTATION.md) for more details on configuration options.
