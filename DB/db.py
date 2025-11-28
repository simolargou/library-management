import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

load_dotenv()

def create_server_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            port=os.getenv("MYSQL_PORT")
        )
        return conn
    except Error as e:
        print("MySQL Connection Error:", e)
        return None


def create_database_if_missing():
    db_name = os.getenv("MYSQL_DATABASE")
    server_conn = create_server_connection()
    cursor = server_conn.cursor()

    cursor.execute("SHOW DATABASES;")
    existing = [db[0] for db in cursor.fetchall()]

    if db_name not in existing:
        cursor.execute(f"CREATE DATABASE {db_name};")
        print(f" Database created: {db_name}")
    else:
        print(f" Database exists: {db_name}")

    cursor.close()
    server_conn.close()


def create_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE"),
            port=os.getenv("MYSQL_PORT")
        )
        return conn
    except Error as e:
        print("DB Connection Error:", e)
        return None
