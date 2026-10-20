
# ==========================================================
# MOVIE RENTAL MANAGEMENT SYSTEM
# Database Connection Module
# ==========================================================

import os
from contextlib import contextmanager

import mysql.connector
from dotenv import load_dotenv


# Load configuration values from the .env file
load_dotenv(override=True)


# ----------------------------------------------------------
# Function 1: Create a database connection
# ----------------------------------------------------------

@contextmanager
def get_connection():
    """
    Establish a connection to the MySQL database.

    The connection is automatically closed after use.
    """

    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "movie_rental")
    )

    try:
        yield connection

    finally:
        connection.close()


# ----------------------------------------------------------
# Function 2: Retrieve records from the database
# ----------------------------------------------------------

def fetch_all(sql, params=()):
    """
    Execute a SELECT query and return all matching records.

    Example:
        fetch_all("SELECT * FROM movies")
    """

    with get_connection() as connection:

        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute(sql, params)
            records = cursor.fetchall()

            return records

        finally:
            cursor.close()


# ----------------------------------------------------------
# Function 3: Insert, update or delete records
# ----------------------------------------------------------

def execute_query(sql, params=()):
    """
    Execute INSERT, UPDATE or DELETE statements.

    Save the transaction when successful.
    Roll back the transaction if an error occurs.
    """

    with get_connection() as connection:

        cursor = connection.cursor()

        try:
            cursor.execute(sql, params)

            connection.commit()

            return cursor.lastrowid

        except Exception:
            connection.rollback()
            raise

        finally:
            cursor.close()
