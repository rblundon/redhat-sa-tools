from sqlalchemy import create_engine
from trino.auth import OAuth2Authentication
from sqlalchemy.schema import Table, MetaData
from sqlalchemy.sql.expression import select, text

ebs_account = '677861'
date = '2025-04-30'

try:
    engine = create_engine(
    "trino://rblundon@prod.sep.starburst.redhat.com:443/s3_datahub_ccx",
        connect_args={
            "auth": OAuth2Authentication(),
            "http_scheme": "https",
        }
    )

    with engine.connect() as connection:
        print("Successfully connected to Trino!")

        # Define your SQL query using named placeholders (e.g., :segment)
        # These act as secure templates for your variables.
        query = text("""
        SELECT
            cluster_id,
            date
        FROM
            ccx_sensitive.cluster_accounts
        WHERE
            ebs_account = :account_id 
            AND date = :date
        """)

        params = {
            "account_id": ebs_account,
            "date": date
        }
    
        result = connection.execute(query, params)

        for row in result:
            print(f"{row.cluster_id:<30} | {row.date:<20}")

except Exception as e:
    print(f"Error: {e}")

finally:
    if 'connection' in locals():
        connection.close()
        print("Connection closed.")