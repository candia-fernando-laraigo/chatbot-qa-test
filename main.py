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
    args = parser.parse_args()

    # Setup basic directories
    for directory in ["logs", SCREENSHOT_DIR]:
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

    for i in range(10):
        report_file = f"reports/{timestamp}_report.html"
        # Prepare command to run pytest directly instead of using pytest.main()
        cmd_args = (
            [sys.executable, "-m", "pytest"]
            + pytest_args
            + ["--html=" + report_file, "--self-contained-html", "--capture=tee-sys"]
        )

        # Log command
        logger.info(f"Running command: {' '.join(cmd_args)}")

        process = subprocess.run(cmd_args, capture_output=False)
        exit_code = process.returncode

        if exit_code == 0:
            logger.info(f"Test Batch {i} completed successfully")
        else:
            logger.error(f"Test Batch {i} failed with exit code {exit_code}")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")


if __name__ == "__main__":
    main()
