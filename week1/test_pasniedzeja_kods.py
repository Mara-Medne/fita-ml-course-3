import mysql.connector
from mysql.connector import Error


def execute_query(host_name, user_name, user_password, query, db_name=None):
    connection = None
    try:
        conn_args = {
            "host": host_name,
            "user": user_name,
            "password": user_password
        }
        if db_name:
            conn_args["database"] = db_name
        connection = mysql.connector.connect(**conn_args)
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query)

        if cursor.with_rows:
            return cursor.fetchall()
        else:
            connection.commit()
            return f"Query executed successfully. Rows affected: {cursor.rowcount}"
    except Error as e:
        return f"Error: '{e}'"
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()


if __name__ == "__main__":
    # Tās pašas vērtības, ko pasniedzējs liktu secrets.yaml
    DB_HOST = "87.110.123.151"
    DB_USER = "fita"
    DB_PASSWORD = "2026-04-28"
    SCRIPT = "SHOW DATABASES;"
    DB_NAME = None

    print("Mēģinu izpildīt pasniedzēja kodu...")
    output = execute_query(DB_HOST, DB_USER, DB_PASSWORD, SCRIPT, DB_NAME)

    print("\n--- Output ---")
    print(output)