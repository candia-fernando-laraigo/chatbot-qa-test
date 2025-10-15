#!/usr/bin/env python3
"""
Simplified test runner for chatbot QA tests using pytest.
"""
import os
import sys
import argparse
import logging
import subprocess

from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config.config import PYTEST_WORKERS, SCREENSHOT_DIR


def main():
    """Run chatbot QA tests with pytest."""
    # Parse arguments
    parser = argparse.ArgumentParser(description="Run Chatbot QA Tests")
    parser.add_argument(
        "--suite",
        default="all",
        help="Test suite to run",
    )
    parser.add_argument(
        "--parallel",
        type=int,
        default=PYTEST_WORKERS,
        help="Number of parallel executions",
    )
    parser.add_argument(
        "--verbose", "-v", action="count", default=0, help="Verbosity level"
    )
    parser.add_argument(
        "--count",
        type=int,
        default=1,
        help="Number of times to repeat the test run (default: 1)",
    )
    args = parser.parse_args()

    # Setup basic directories
    for directory in ["logs", "reports", SCREENSHOT_DIR]:
        if not os.path.exists(directory):
            os.makedirs(directory)

    # Setup logging
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"logs/test_run_{timestamp}.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
    )
    logger = logging.getLogger(__name__)
    logger.info("Starting test execution")

    # Build pytest arguments
    pytest_args = []

    # Set verbosity
    if args.verbose:
        pytest_args.extend(["-" + "v" * args.verbose])

    # Set parallel execution
    if args.parallel > 1:
        pytest_args.extend(["-n", str(args.parallel)])

    # Set test suite
    if args.suite == "all":
        pytest_args.append("tests/")
    else:
        pytest_args.extend(["-m", args.suite])

    report_file = f"reports/{timestamp}_report.html"
    cmd_args = (
        [sys.executable, "-m", "pytest"]
        + pytest_args
        + ["--count", str(args.count)]
        + ["--html=" + report_file, "--self-contained-html", "--capture=tee-sys"]
    )

    logger.info(f"Running command: {' '.join(cmd_args)}")
    process = subprocess.run(cmd_args, capture_output=False)
    exit_code = process.returncode
    if exit_code == 0:
        logger.info("Test run completed successfully")
    else:
        logger.error(f"Test run failed with exit code {exit_code}")


if __name__ == "__main__":
    main()
