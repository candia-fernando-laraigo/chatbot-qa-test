"""
Custom logger module for chatbot QA testing.
Provides a simple way to log test execution details to a file.
"""

import os
import logging
from datetime import datetime
from enum import Enum


class LogLevel(Enum):
    """Log levels for the test logger."""
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    ERROR = logging.ERROR


class TestLogger:
    """
    Simple logger for test execution.
    Records test execution time, status, and error details.
    """

    def __init__(self, log_dir='logs', log_file=None):
        """
        Initialize the logger.
        
        Args:
            log_dir (str): Directory to store log files
            log_file (str, optional): Specific log file name. If None, a default name with timestamp will be used.
        """
        # Create logs directory if it doesn't exist
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        # Set up log file name
        if log_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = f"test_execution_{timestamp}.log"
        
        self.log_path = os.path.join(log_dir, log_file)
        
        # Configure logger
        self.logger = logging.getLogger(f'test_logger_{id(self)}')
        self.logger.setLevel(logging.DEBUG)
        
        # Prevent duplicate logs
        if not self.logger.handlers:
            # File handler
            file_handler = logging.FileHandler(self.log_path)
            file_handler.setLevel(logging.DEBUG)
            
            # Format
            formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(formatter)
            
            # Add handler to logger
            self.logger.addHandler(file_handler)
    
    def log(self, message, level=LogLevel.INFO):
        """
        Log a message with the specified level.
        
        Args:
            message (str): Message to log
            level (LogLevel): Level to log at (DEBUG, INFO, ERROR)
        """
        self.logger.log(level.value, message)
    
    def debug(self, message):
        """Log a debug message."""
        self.log(message, LogLevel.DEBUG)
    
    def info(self, message):
        """Log an info message."""
        self.log(message, LogLevel.INFO)
    
    def error(self, message):
        """Log an error message."""
        self.log(message, LogLevel.ERROR)
    
    def log_test_start(self, test_name):
        """
        Log the start of a test.
        
        Args:
            test_name (str): Name of the test being executed
        """
        self.info(f"TEST START: {test_name}")
    
    def log_test_end(self, test_name, status, duration, error=None):
        """
        Log the end of a test with result information.
        
        Args:
            test_name (str): Name of the test
            status (str): Test status (PASS/FAIL)
            duration (float): Test execution time in seconds
            error (str, optional): Error message if test failed
        """
        self.info(f"TEST END: {test_name} - Status: {status} - Duration: {duration:.2f} seconds")
        
        if error and status == "FAIL":
            self.error(f"TEST FAILURE: {test_name} - Error: {error}")
    
    def log_response_time(self, test_name, query, response_time):
        """
        Log the response time for a chatbot query.
        
        Args:
            test_name (str): Name of the test
            query (str): The query sent to the chatbot
            response_time (float): Time taken for the chatbot to respond in seconds
        """
        self.info(f"RESPONSE TIME: {test_name} - Query: '{query}' - Time: {response_time:.2f} seconds")