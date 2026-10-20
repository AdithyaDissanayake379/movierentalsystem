
# ============================================================
# MOVIE RENTAL MANAGEMENT SYSTEM
# Employee Authentication Module
# ============================================================

import bcrypt

from database.connection import (
    fetch_all,
    execute_query
)


# ------------------------------------------------------------
# Function 1: Register a new employee
# ------------------------------------------------------------

def register_employee(username, password, full_name):
    """
    Register a new employee with a securely hashed password.
    """

    # Remove unnecessary spaces
    username = username.strip()
    full_name = full_name.strip()

    # Validate username and full name
    if not username:
        raise ValueError("Username cannot be empty")

    if not full_name:
        raise ValueError("Employee name cannot be empty")

    if len(username) > 60:
        raise ValueError("Username is too long")

    if len(full_name) > 120:
        raise ValueError("Employee name is too long")

    # Validate password
    if len(password) < 10:
        raise ValueError(
            "Password must contain at least 10 characters"
        )

    if len(password.encode("utf-8")) > 72:
        raise ValueError(
            "Password must not exceed 72 UTF-8 bytes"
        )

    # Check if the username already exists
    sql_check = """
        SELECT employee_id
        FROM employees
        WHERE username = %s
    """

    existing_user = fetch_all(
        sql_check,
        (username,)
    )

    if existing_user:
        raise ValueError(
            "This username is already registered"
        )

    # Convert password to bytes and hash it
    password_bytes = password.encode("utf-8")

    hashed_password = bcrypt.hashpw(
        password_bytes,
        bcrypt.gensalt()
    )

    password_hash = hashed_password.decode("utf-8")

    # Insert employee into the database
    sql_insert = """
        INSERT INTO employees
        (username, password_hash, full_name)
        VALUES (%s, %s, %s)
    """

    employee_id = execute_query(
        sql_insert,
        (username, password_hash, full_name)
    )

    return employee_id


# ------------------------------------------------------------
# Function 2: Authenticate employee login
# ------------------------------------------------------------

def authenticate_employee(username, password):
    """
    Validate employee credentials.

    Returns employee information if login is successful.
    Returns None if login fails.
    """

    username = username.strip()

    sql = """
        SELECT employee_id,
               username,
               password_hash,
               full_name
        FROM employees
        WHERE username = %s
    """

    employees = fetch_all(
        sql,
        (username,)
    )

    # Reject login if employee does not exist
    if not employees:
        return None

    employee = employees[0]

    # Convert stored hash to bytes
    stored_hash = employee[
        "password_hash"
    ].encode("utf-8")

    password_bytes = password.encode("utf-8")

    # bcrypt passwords have a 72-byte limit
    if len(password_bytes) > 72:
        return None

    # Verify the password against the hash
    password_correct = bcrypt.checkpw(
        password_bytes,
        stored_hash
    )

    if not password_correct:
        return None

    # Return only non-sensitive employee details
    return {
        "employee_id": employee["employee_id"],
        "username": employee["username"],
        "full_name": employee["full_name"]
    }
