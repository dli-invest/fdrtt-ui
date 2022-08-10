import mysql.connector
import os

def connect_to_db():
    # read database credentials from environment variables
    db_host = os.environ.get("DB_HOST")
    db_user = os.environ.get("DB_USER")
    db_pass = os.environ.get("DB_PASSWORD")
    db_name = os.environ.get("DB_NAME")
    return mysql.connector.connect(
        user=db_user, password=db_pass, host=db_host, database=db_name
    )