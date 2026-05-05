"""
04_extract_samples.py
Izvelk 3-5 rindas no katras tabulas.
"""

import mysql.connector
import json
import os

DB_CONFIG = {
    "host": "87.110.123.151",
    "user": "fita",
    "password": "2026-04-28",
    "database": "direct_payments",
    "connection_timeout": 10,
}

connection = mysql.connector.connect(**DB_CONFIG)
cursor = connection.cursor(dictionary=True)

cursor.execute("""
    SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES
    WHERE TABLE_SCHEMA = 'direct_payments'
""")
tables = [row["TABLE_NAME"] for row in cursor.fetchall()]

samples = {}
for table in tables:
    print(f"📋 {table}")
    cursor.execute(f"SELECT * FROM `{table}` LIMIT 5")
    samples[table] = cursor.fetchall()

cursor.close()
connection.close()

script_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(script_dir, "sample_data.json"), "w", encoding="utf-8") as f:
    json.dump(samples, f, indent=2, ensure_ascii=False, default=str)

print("\n✅ Saglabāts: week1/sample_data.json")
