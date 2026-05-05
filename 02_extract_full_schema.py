import mysql.connector
import json

DB_CONFIG = {
    "host": "87.110.123.151",
    "user": "fita",
    "password": "2026-04-28",
    "database": "direct_payments",
    "connection_timeout": 10,
}


def extract_schema():
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor(dictionary=True)

    # Visas tabulas
    cursor.execute("""
        SELECT TABLE_NAME, TABLE_COMMENT
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_SCHEMA = 'direct_payments'
    """)
    tables = cursor.fetchall()

    schema = {"database": "direct_payments", "tables": []}

    for table in tables:
        table_name = table["TABLE_NAME"]
        print(f"📋 Apstrādā: {table_name}")

        # Kolonnas
        cursor.execute(f"""
            SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_KEY,
                   COLUMN_DEFAULT, COLUMN_COMMENT, CHARACTER_MAXIMUM_LENGTH
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = 'direct_payments' AND TABLE_NAME = '{table_name}'
            ORDER BY ORDINAL_POSITION
        """)
        columns = cursor.fetchall()

        # Foreign keys
        cursor.execute(f"""
            SELECT COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE TABLE_SCHEMA = 'direct_payments'
              AND TABLE_NAME = '{table_name}'
              AND REFERENCED_TABLE_NAME IS NOT NULL
        """)
        foreign_keys = cursor.fetchall()

        # Rindu skaits
        cursor.execute(f"SELECT COUNT(*) AS cnt FROM `{table_name}`")
        row_count = cursor.fetchone()["cnt"]

        schema["tables"].append({
            "name": table_name,
            "comment": table["TABLE_COMMENT"],
            "row_count": row_count,
            "columns": columns,
            "foreign_keys": foreign_keys,
        })

    cursor.close()
    connection.close()

    # Saglabā JSON
    with open("week1/database_schema.json", "w", encoding="utf-8") as f:
        json.dump(schema, f, indent=2, ensure_ascii=False, default=str)

    print(f"\n✅ Saglabāts: week1/database_schema.json")
    print(f"   Tabulu skaits: {len(schema['tables'])}")


if __name__ == "__main__":
    extract_schema()