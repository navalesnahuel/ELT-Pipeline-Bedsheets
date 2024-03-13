import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def postgres_conn():
    # Access environment variables
    db_name = os.getenv('DB_NAME')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_port = os.getenv('DB_PORT')
    db_host = os.getenv('DB_HOST')

    # Establish database connection
    try:
        conn = psycopg2.connect(
            host=db_host,
            dbname=db_name,
            user=db_user,
            password=db_password,
            port=db_port
        )
        cursor = conn.cursor()
        return conn, cursor
    except psycopg2.Error as e:
        print(f"Error: Unable to connect to the database. {e}")
        return None, None