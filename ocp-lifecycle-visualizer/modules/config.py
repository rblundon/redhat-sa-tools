"""
Configuration settings for the OpenShift Lifecycle Visualizer.
"""

import os

# Database Configuration
DB_CONNECTION_STRING = "trino://{username}@prod.sep.starburst.redhat.com:443/s3_datahub_ccx"
DB_USERNAME = "rblundon"  # Username for OAuth2 authentication
DB_POOL_SIZE = 5
DB_MAX_OVERFLOW = 10
DB_POOL_TIMEOUT = 30

# Logging Configuration
LOG_FORMAT = '%(asctime)s - %(levelname)s - [%(category)s] - %(message)s'
LOG_LEVEL = 'INFO'
LOG_FILE = f'lifecycle_visualizer_{os.path.basename(os.getcwd())}.log'

# Application Configuration
APP_NAME = "OpenShift Lifecycle Visualizer"
APP_VERSION = "1.0.0" 