"""
Utility functions for the OpenShift Lifecycle Visualizer.
"""

import click
import logging
import socket
from datetime import datetime

def setup_logging(debug=False):
    """Set up logging configuration."""
    log_format = '%(asctime)s - %(levelname)s - [%(category)s] - %(message)s'
    log_level = logging.DEBUG if debug else logging.INFO
    
    # Create a custom filter to add category
    class CategoryFilter(logging.Filter):
        def filter(self, record):
            if not hasattr(record, 'category'):
                record.category = 'GENERAL'
            return True

    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=[
            logging.StreamHandler(),  # Console handler
            logging.FileHandler(f'lifecycle_visualizer_{datetime.now().strftime("%Y%m%d")}.log')
            if debug else logging.NullHandler()  # File handler for debug
        ]
    )
    
    # Add category filter
    for handler in logging.getLogger().handlers:
        handler.addFilter(CategoryFilter())

def get_logger(category):
    """Get a logger with the specified category."""
    logger = logging.getLogger(category)
    logger.category = category
    return logger

def get_ebs_account(ebs_account=None):
    """Get EBS account number from argument or prompt."""
    if not ebs_account:
        ebs_account = click.prompt('Please enter the EBS account number', type=str)
    return ebs_account

def get_username(username=None):
    """Get username for database authentication from argument or prompt."""
    if not username:
        username = click.prompt('Please enter your database username', type=str)
    return username

def check_vpn_connection():
    """
    Check if the user is connected to the Red Hat VPN by attempting to resolve
    the database hostname.
    
    Returns:
        bool: True if VPN appears to be connected, False otherwise
    """
    try:
        socket.gethostbyname('prod.sep.starburst.redhat.com')
        return True
    except socket.gaierror:
        return False 