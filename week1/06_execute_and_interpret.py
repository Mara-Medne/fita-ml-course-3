"""
06_execute_and_interpret.py
Izpilda SQL vaicājumus un saglabā rezultātus.
"""

import mysql.connector
import json
import os
import re

DB_CONFIG = {
    "host": "87.110.123.151",
    "user": "fita",
    "password": "2026-04-28",
    "database": "direct_payments",
    "connection_timeout": 10,
}

script_dir = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(script_dir, "generated_queries.sql"), "r", encoding="utf-8") as f:
    sql_content = f.read()

# Sadala SQL pa vaicājumiem
queries = []
current_comment = ""
for line in sql_content.strip().split("\n"):
    if line.startswith("--"):
        current_comment = line.replace("--", "").strip()
    elif line.strip().upper().startswith("SELECT"):
        # Savāc pilnu vaicājumu līdz ;
        queries.append({"name": current_comment, "sql": ""})
    if queries and not line.startswith("--"):
        queries[-1]["sql"] += line + "\n"

connection = mysql.connector.connect(**DB_CONFIG)
cursor = connection.cursor(dictionary=True)

results = []
for q in queries:
    sql = q["sql"].strip().rstrip(";")
    print(f"\n📊 {q['name']}")
    print(f"   SQL: {sql[:80]}...")
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        results.append({
            "question": q["name"],
            "sql": sql,
            "row_count": len(rows),
            "data": rows[:20],
        })
        print(f"   ✅ Rezultāti: {len(rows)} rindas")
    except Exception as e:
        print(f"   ❌ Kļūda: {e}")
        results.append({"question": q["name"], "sql": sql, "error": str(e)})

cursor.close()
connection.close()

with open(os.path.join(script_dir, "aggregated_results.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False, default=str)

print("\n✅ Saglabāts: week1/aggregated_results.json")

# Vienkāršs apraksts
report = "# Datubāzes analīzes rezultāti\n\n"
for r in results:
    report += f"## {r['question']}\n\n"
    if "error" in r:
        report += f"Kļūda: {r['error']}\n\n"
    else:
        report += f"Atrasti {r['row_count']} ieraksti.\n\n"
        if r["data"]:
            for row in r["data"][:5]:
                report += f"- {row}\n"
            report += "\n"

with open(os.path.join(script_dir, "final_report.md"), "w", encoding="utf-8") as f:
    f.write(report)

print("✅ Saglabāts: week1/final_report.md")
