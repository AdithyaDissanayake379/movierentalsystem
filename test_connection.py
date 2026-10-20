
# Test the database connection

from database.connection import get_connection


def test_database_connection():

    try:
        with get_connection() as connection:

            if connection.is_connected():

                print("Database connection successful!")

                cursor = connection.cursor()

                cursor.execute("SELECT DATABASE()")

                database_name = cursor.fetchone()[0]

                print("Connected to:", database_name)

                cursor.close()

    except Exception as error:

        print("Database connection failed!")
        print("Error:", error)


if __name__ == "__main__":
    test_database_connection()
