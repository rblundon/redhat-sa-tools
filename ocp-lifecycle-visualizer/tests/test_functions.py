"""
Tests for the OpenShift Lifecycle Visualizer functions.
"""

import unittest
from unittest.mock import patch, MagicMock
import logging
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.functions import setup_logging, get_logger, get_ebs_account, get_username, check_vpn_connection

class TestFunctions(unittest.TestCase):
    """Test cases for the functions module."""

    def setUp(self):
        """Set up test environment."""
        # Reset logging configuration before each test
        for handler in logging.getLogger().handlers[:]:
            logging.getLogger().removeHandler(handler)
        logging.getLogger().setLevel(logging.NOTSET)

    def test_setup_logging_debug(self):
        """Test logging setup in debug mode."""
        setup_logging(debug=True)
        logger = logging.getLogger()
        
        # Check if debug level is set
        self.assertEqual(logger.level, logging.DEBUG)
        
        # Check if both console and file handlers are present
        handlers = logger.handlers
        self.assertEqual(len(handlers), 2)
        self.assertTrue(any(isinstance(h, logging.StreamHandler) for h in handlers))
        self.assertTrue(any(isinstance(h, logging.FileHandler) for h in handlers))

    def test_setup_logging_normal(self):
        """Test logging setup in normal mode."""
        setup_logging(debug=False)
        logger = logging.getLogger()
        
        # Check if info level is set
        self.assertEqual(logger.level, logging.INFO)
        
        # Check if only console handler is present
        handlers = logger.handlers
        self.assertEqual(len(handlers), 1)
        self.assertTrue(isinstance(handlers[0], logging.StreamHandler))

    def test_get_logger(self):
        """Test logger creation with category."""
        logger = get_logger('TEST')
        
        # Check if logger has the correct category
        self.assertEqual(logger.category, 'TEST')
        
        # Check if logger is properly configured
        self.assertIsInstance(logger, logging.Logger)

    @patch('click.prompt')
    def test_get_ebs_account_with_input(self, mock_prompt):
        """Test EBS account retrieval with user input."""
        mock_prompt.return_value = '123456'
        result = get_ebs_account()
        self.assertEqual(result, '123456')
        mock_prompt.assert_called_once_with('Please enter the EBS Account Number')

    def test_get_ebs_account_with_argument(self):
        """Test EBS account retrieval with provided argument."""
        result = get_ebs_account('123456')
        self.assertEqual(result, '123456')

    @patch('click.prompt')
    def test_get_username_with_input(self, mock_prompt):
        """Test username retrieval with user input."""
        mock_prompt.return_value = 'testuser'
        result = get_username()
        self.assertEqual(result, 'testuser')
        mock_prompt.assert_called_once_with('Please enter your username')

    def test_get_username_with_argument(self):
        """Test username retrieval with provided argument."""
        result = get_username('testuser')
        self.assertEqual(result, 'testuser')

    @patch('subprocess.run')
    def test_check_vpn_connection_success(self, mock_run):
        """Test VPN connection check when connected."""
        mock_run.return_value = MagicMock(returncode=0)
        self.assertTrue(check_vpn_connection())

    @patch('subprocess.run')
    def test_check_vpn_connection_failure(self, mock_run):
        """Test VPN connection check when not connected."""
        mock_run.return_value = MagicMock(returncode=1)
        self.assertFalse(check_vpn_connection())

if __name__ == '__main__':
    unittest.main() 