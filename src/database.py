import sqlite3
db_path="data/sales.db"

def get_connection():
    connection=sqlite3.connect(db_path)
    return connection


def query_database(query):
    """
    Execute a read-only SQL query against the sales database.
    """
    if not query.strip().lower().startswith("select"):
        raise ValueError("Only SELECT queries are allowed.")
    connection=get_connection()
    try:
        cursor = connection.cursor()

        cursor.execute(query)

        results = cursor.fetchall()


        return results
    finally:
        connection.close()    