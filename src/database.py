import sqlite3
db_path="data/sales.db"

def get_connection():
    connection=sqlite3.connect(db_path)
    return connection


def query_database(query):
    connection=get_connection()
    cursor = connection.cursor()

    cursor.execute(query)

    results = cursor.fetchall()

    connection.close()

    return results