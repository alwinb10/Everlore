#Everlore
import mysql.connector
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "idko",   # change this
    "database": "everlore"
}

def get_connection():
    """
    Creates and returns a new MySQL connection.
    """
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print("❌ Database Connection Failed:", err)
        return None

def execute_query(query, values=None):
    """
    Used for INSERT, UPDATE, DELETE
    """
    conn = get_connection()
    if conn is None:
        return False

    cursor = conn.cursor()

    try:
        cursor.execute(query, values or ())
        conn.commit()
        return True

    except mysql.connector.Error as err:
        print("❌ Query Execution Error:", err)
        return False

    finally:
        cursor.close()
        conn.close()
def fetch_all(query, values=None):
    """
    Used for SELECT queries
    """
    conn = get_connection()
    if conn is None:
        return []

    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(query, values or ())
        result = cursor.fetchall()
        return result

    except mysql.connector.Error as err:
        print("❌ Fetch Error:", err)
        return []

    finally:
        cursor.close()
        conn.close()
def fetch_one(query, values=None):
    """
    Used for SELECT queries that return only one row
    """
    conn = get_connection()
    if conn is None:
        return None

    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(query, values or ())
        return cursor.fetchone()

    except mysql.connector.Error as err:
        print("❌ Fetch Error:", err)
        return None

    finally:
        cursor.close()
        conn.close()


def fetch_value(query, values=None):
    """
    Used for SELECT COUNT(*) or other queries that return a single value.
    """
    conn = get_connection()
    if conn is None:
        return 0

    cursor = conn.cursor()

    try:
        cursor.execute(query, values or ())
        result = cursor.fetchone()
        return result[0] if result else 0

    except mysql.connector.Error as err:
        print("❌ Fetch Error:", err)
        return 0

    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    conn = get_connection()

    if conn:
        print("✅ Connected to EVERLORE successfully!")
        conn.close()
