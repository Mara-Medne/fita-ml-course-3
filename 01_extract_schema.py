"""
01_extract_schema.py
====================
Mērķis (1. solis): Pārbaudīt, vai varam pieslēgties MySQL serverim.

Pasniedzēja dotie dati:
- serveris: 87.110.123.151
- ports: 3306 (MySQL noklusējamais)
- lietotājs: fita
- parole: 2026-04-28
"""

import mysql.connector
from mysql.connector import Error

# Servera pieslēguma parametri
DB_CONFIG = {
    "host": "87.110.123.151",
    "user": "fita",
    "password": "2026-04-28",
    "connection_timeout": 10,
}


def test_connection():
    """Mēģina pieslēgties serverim un noskaidrot tā versiju."""
    try:
        # Veidojam savienojumu
        connection = mysql.connector.connect(**DB_CONFIG)

        if connection.is_connected():
            # Iegūstam servera versiju kā pārbaudi
            db_info = connection.get_server_info()
            print("✅ Veiksmīgi pieslēgts MySQL serverim!")
            print(f"   Servera versija: {db_info}")

            # Pārbaudām, kādas datubāzes ir pieejamas
            cursor = connection.cursor()
            cursor.execute("SHOW DATABASES;")
            databases = cursor.fetchall()

            print(f"\n📁 Pieejamās datubāzes ({len(databases)} kopā):")
            for db in databases:
                print(f"   - {db[0]}")

            cursor.close()

    except Error as e:
        print(f"❌ Kļūda pieslēdzoties: {e}")

    finally:
        # Vienmēr aizveram savienojumu
        if "connection" in locals() and connection.is_connected():
            connection.close()
            print("\n🔌 Savienojums aizvērts.")


if __name__ == "__main__":
    test_connection()