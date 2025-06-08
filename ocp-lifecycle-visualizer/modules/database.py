"""
Database connection management module.
Handles database connections and queries.
"""

import logging
from contextlib import contextmanager
from sqlalchemy import create_engine, text
from trino.auth import OAuth2Authentication
from modules.functions import check_vpn_connection

class DatabaseManager:
    """Manages database connections and queries."""
    
    def __init__(self, connection_string, username):
        """
        Initialize the database manager.
        
        Args:
            connection_string (str): Database connection string
            username (str): Username for OAuth2 authentication
        """
        self.logger = logging.getLogger('DATABASE')
        self.connection_string = connection_string
        self.username = username
        self._engine = None
        
    def initialize(self):
        """Initialize the database engine."""
        try:
            # Check VPN connection first
            if not check_vpn_connection():
                self.logger.error("""
Database connection failed. Please ensure you are connected to the Red Hat VPN.
You can connect to the VPN using:
    - GlobalProtect VPN client
    - Or visit: https://vpn.redhat.com

After connecting to the VPN, please try running the program again.
""")
                return False

            # Update connection string with username
            connection_string = self.connection_string.replace('{username}', self.username)
            
            self._engine = create_engine(
                connection_string,
                connect_args={
                    "auth": OAuth2Authentication(),
                    "http_scheme": "https",
                }
            )
            
            # Test the connection
            with self._engine.connect() as connection:
                self.logger.info("Successfully connected to Trino!")
            
            return True
            
        except Exception as e:
            self.logger.error(f"""
Database connection failed. Please ensure you are connected to the Red Hat VPN.
You can connect to the VPN using:
    - GlobalProtect VPN client
    - Or visit: https://vpn.redhat.com

After connecting to the VPN, please try running the program again.

Error details: {e}
""")
            return False
    
    @contextmanager
    def get_connection(self):
        """
        Get a database connection.
        
        Yields:
            Connection: A database connection
            
        Example:
            with db_manager.get_connection() as connection:
                result = connection.execute(query)
        """
        if not self._engine:
            raise RuntimeError("Database manager not initialized. Call initialize() first.")
            
        connection = self._engine.connect()
        try:
            yield connection
        finally:
            connection.close()
            self.logger.debug("Connection closed")
    
    def cleanup(self):
        """Clean up database resources."""
        if self._engine:
            self._engine.dispose()
            self.logger.info("Database resources cleaned up") 