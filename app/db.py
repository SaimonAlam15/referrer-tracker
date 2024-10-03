import os

import snowflake.connector

def get_snowflake_connection():
    conn = snowflake.connector.connect(
        user=os.getenv('USER'),
        password=os.getenv('PASSWORD'),
        account=os.getenv('ACCOUNT'),
        warehouse=os.getenv('WAREHOUSE'),
        database=os.getenv('DATABASE'),
        schema=os.getenv('SCHEMA')
    )
    return conn