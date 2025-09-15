#!/usr/bin/python3
"""
OpenShift Lifecycle Visualizer
Author: Ryan Blundon
Date: 2024-03-19
Description: Visualizes OpenShift cluster lifecycle information from database records.
             Verifies EBS account numbers against the database and confirms account names.
             Requires VPN connection and OAuth2 authentication for database access.
"""

import os
import sys
import click
from sqlalchemy import text
from modules.functions import setup_logging, get_logger, get_ebs_account, get_username
from modules.database import DatabaseManager
from modules.config import DB_CONNECTION_STRING

# Get script directory for relative paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

@click.command()
@click.option('--debug', is_flag=True, help='Enable debug logging')
@click.option('--ebs-account', help='EBS Account number')
@click.option('--username', help='Username for database authentication')
def main(debug, ebs_account, username):
    """OpenShift Lifecycle Visualizer - Track and visualize cluster lifecycles.
    
    This script connects to the Trino database to verify EBS account numbers
    and their associated account names. It requires:
    - VPN connection to Red Hat network
    - Valid OAuth2 credentials
    - EBS account number (provided or prompted)
    - Database username (provided or prompted)
    
    The script will:
    1. Verify VPN connection
    2. Establish database connection
    3. Query account information
    4. Display and confirm account details
    5. Retrieve and display associated clusters
    """
    setup_logging(debug)
    logger = get_logger('MAIN')
    logger.info('Starting OpenShift Lifecycle Visualizer')

    # Get EBS account number
    ebs_account = get_ebs_account(ebs_account)
    logger.info(f'EBS Account: {ebs_account}')

    # Get username for database authentication
    username = get_username(username)
    logger.info(f'Database Username: {username}')

    # Initialize database connection
    db_manager = DatabaseManager(
        connection_string=DB_CONNECTION_STRING,
        username=username
    )

    if not db_manager.initialize():
        logger.error("Failed to initialize database connection")
        sys.exit(1)

    try:
        # Verify account name
        with db_manager.get_connection() as connection:
            # First, verify the account
            account_query = text("""
                SELECT distinct(account_name)
                FROM ccx_sensitive.cluster_accounts 
                WHERE ebs_account = :account_id
            """)
            result = connection.execute(account_query, {"account_id": ebs_account})
            
            # Get the account name, filtering out None values
            account_names = [row.account_name for row in result if row.account_name is not None]
            
            if not account_names:
                logger.error(f"No account found for EBS account number: {ebs_account}")
                sys.exit(1)
                
            # Print account name(s) and get confirmation
            account_list = ", ".join(account_names)
            if not click.confirm(f"\nEBS account {ebs_account} linked to {account_list}. Proceed?"):
                logger.info("User rejected account verification. Exiting.")
                sys.exit(0)
                
            logger.info("Account verified successfully")

            # Now get the list of clusters
            cluster_query = text("""
                SELECT distinct(cluster_id)
                FROM ccx_sensitive.cluster_accounts 
                WHERE ebs_account = :account_id
            """)
            cluster_result = connection.execute(cluster_query, {"account_id": ebs_account})
            
            # Get the cluster IDs
            cluster_ids = [row.cluster_id for row in cluster_result]
            
            if not cluster_ids:
                logger.warning(f"No clusters found for EBS account: {ebs_account}")
            else:
                print(f"\nFound {len(cluster_ids)} cluster(s):")
                for cluster_id in cluster_ids:
                    print(f"  - {cluster_id}")

    except Exception as e:
        logger.error(f"Error executing query: {e}")
        sys.exit(1)
    finally:
        db_manager.cleanup()

if __name__ == '__main__':
    main() 