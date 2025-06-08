"""
Tests for the OpenShift Lifecycle Visualizer main script.
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ocp_lifecycle_visualizer import main

class TestMain(unittest.TestCase):
    """Test cases for the main script."""

    @patch('modules.functions.setup_logging')
    @patch('modules.functions.get_logger')
    @patch('modules.functions.get_ebs_account')
    @patch('modules.functions.get_username')
    @patch('modules.functions.check_vpn_connection')
    @patch('modules.database.DatabaseManager')
    def test_main_successful_flow(self, mock_db_manager, mock_vpn_check, mock_get_username, 
                                mock_get_ebs, mock_get_logger, mock_setup_logging):
        """Test successful main function flow."""
        # Set up mocks
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        mock_get_ebs.return_value = '123456'
        mock_get_username.return_value = 'testuser'
        mock_vpn_check.return_value = True
        
        # Mock database connection and query
        mock_db_instance = MagicMock()
        mock_db_manager.return_value = mock_db_instance
        mock_db_instance.initialize.return_value = True
        
        mock_connection = MagicMock()
        mock_db_instance.get_connection.return_value.__enter__.return_value = mock_connection
        
        mock_result = MagicMock()
        mock_connection.execute.return_value = mock_result
        mock_result.__iter__.return_value = [MagicMock(account_name='Test Account')]

        # Call main with arguments
        main(debug=False, ebs_account='123456', username='testuser')

        # Verify function calls
        mock_setup_logging.assert_called_once_with(False)
        mock_get_logger.assert_called_once_with('MAIN')
        mock_get_ebs.assert_called_once_with('123456')
        mock_get_username.assert_called_once_with('testuser')
        mock_vpn_check.assert_called_once()
        mock_db_manager.assert_called_once()
        mock_db_instance.initialize.assert_called_once()
        mock_logger.info.assert_any_call('Starting OpenShift Lifecycle Visualizer')
        mock_logger.info.assert_any_call('EBS Account: 123456')
        mock_logger.info.assert_any_call('Database Username: testuser')
        mock_logger.info.assert_any_call('Account verified successfully')

    @patch('modules.functions.setup_logging')
    @patch('modules.functions.get_logger')
    @patch('modules.functions.get_ebs_account')
    @patch('modules.functions.get_username')
    @patch('modules.functions.check_vpn_connection')
    def test_main_vpn_check_failure(self, mock_vpn_check, mock_get_username, 
                                  mock_get_ebs, mock_get_logger, mock_setup_logging):
        """Test main function when VPN check fails."""
        # Set up mocks
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        mock_get_ebs.return_value = '123456'
        mock_get_username.return_value = 'testuser'
        mock_vpn_check.return_value = False

        # Call main with arguments
        main(debug=False, ebs_account='123456', username='testuser')

        # Verify function calls
        mock_setup_logging.assert_called_once_with(False)
        mock_get_logger.assert_called_once_with('MAIN')
        mock_get_ebs.assert_called_once_with('123456')
        mock_get_username.assert_called_once_with('testuser')
        mock_vpn_check.assert_called_once()
        mock_logger.error.assert_called_once_with("VPN connection check failed. Please connect to the VPN and try again.")

    @patch('modules.functions.setup_logging')
    @patch('modules.functions.get_logger')
    @patch('modules.functions.get_ebs_account')
    @patch('modules.functions.get_username')
    @patch('modules.functions.check_vpn_connection')
    @patch('modules.database.DatabaseManager')
    def test_main_no_account_found(self, mock_db_manager, mock_vpn_check, mock_get_username,
                                 mock_get_ebs, mock_get_logger, mock_setup_logging):
        """Test main function when no account is found."""
        # Set up mocks
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        mock_get_ebs.return_value = '123456'
        mock_get_username.return_value = 'testuser'
        mock_vpn_check.return_value = True
        
        # Mock database connection and query
        mock_db_instance = MagicMock()
        mock_db_manager.return_value = mock_db_instance
        mock_db_instance.initialize.return_value = True
        
        mock_connection = MagicMock()
        mock_db_instance.get_connection.return_value.__enter__.return_value = mock_connection
        
        mock_result = MagicMock()
        mock_connection.execute.return_value = mock_result
        mock_result.__iter__.return_value = []  # Empty result

        # Call main with arguments
        main(debug=False, ebs_account='123456', username='testuser')

        # Verify function calls
        mock_logger.error.assert_called_once_with("No account found for EBS account number: 123456")

if __name__ == '__main__':
    unittest.main() 