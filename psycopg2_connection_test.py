# Minimal psycopg2 Connection Test
# File: psycopg2_connection_test.py
# This script tests if psycopg2 can connect to your database using your .env config.
# It does NOT affect your main codebase. You can run it with: pipenv run python psycopg2_connection_test.py

import os
from dotenv import load_dotenv
import psycopg2

# Load environment variables from .env
load_dotenv()

host = os.getenv('POSTGRES_HOST')
port = os.getenv('POSTGRES_PORT')
db = os.getenv('POSTGRES_DB')
user = os.getenv('POSTGRES_USER')
password = os.getenv('POSTGRES_PASSWORD')

print(f"Testing connection to {host}:{port}, database={db}, user={user}")

try:
    conn = psycopg2.connect(
        host=host,
        port=port,
        dbname=db,
        user=user,
        password=password
    )
    print("psycopg2 connection successful!")
    cur = conn.cursor()
    cur.execute("SELECT 1;")
    print("Test query result:", cur.fetchone())
    cur.close()
    conn.close()
    print("Connection closed cleanly.")
except Exception as e:
    print("psycopg2 connection failed:")
    print(e)
    import traceback
    traceback.print_exc()
