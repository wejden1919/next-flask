import psycopg2
import os


def connect_to_database():
    try:
        conn = psycopg2.connect(
            dbname="testdb",
            user="postgres",
            password="wejden26162609",
            host=os.environ.get("DATABASE_URL"), 
            port="5432"
        )
        return conn
    except psycopg2.Error as e:
        print("Error connecting to database:", e)
        return None

def execute_query(query, values=None):
    conn = connect_to_database()
    cursor = conn.cursor()
    try:
        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)
        return cursor, conn
    except psycopg2.Error as e:
        conn.rollback()  # Rollback changes if query fails
        print("Error executing SQL query:", e)
        return None, None


