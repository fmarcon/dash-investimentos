import os
import time

import psycopg2
from psycopg2 import OperationalError

DB_HOST = os.environ.get("POSTGRES_HOST", "db")
DB_PORT = int(os.environ.get("POSTGRES_PORT", 5432))
DB_NAME = os.environ.get("POSTGRES_DB", "invest")
DB_USER = os.environ.get("POSTGRES_USER", "invest")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "investpass")

print("Waiting for PostgreSQL to become available...")
while True:
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            connect_timeout=3,
        )
        conn.close()
        print("PostgreSQL is available.")
        break
    except OperationalError:
        print("PostgreSQL not ready yet, retrying in 1s...")
        time.sleep(1)
