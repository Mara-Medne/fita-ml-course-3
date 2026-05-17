"""
12_fetch_scheme_data.py
Vaicā datubāzi — maksājumu shēmas pa nozarēm un mēnešiem.
Saglabā: week1/scheme_by_vertical.json
"""
import os, json, mysql.connector

script_dir = os.path.dirname(os.path.abspath(__file__))

DB_CONFIG = {
    "host": "87.110.123.151", "user": "fita",
    "password": "2026-04-28",  "database": "direct_payments",
    "connection_timeout": 10,
}

SQL = """
SELECT
    o.parent_vertical   AS vertical,
    DATE_FORMAT(p.charge_date, '%Y-%m') AS month,
    m.scheme,
    COUNT(*)            AS payment_count
FROM payments p
JOIN mandates m ON p.mandate_id = m.id
JOIN organisations o ON m.organisation_id = o.id
GROUP BY o.parent_vertical, month, m.scheme
ORDER BY month, o.parent_vertical, m.scheme
"""

conn   = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor(dictionary=True)
cursor.execute(SQL)
rows   = cursor.fetchall()
cursor.close(); conn.close()

out = os.path.join(script_dir, "scheme_by_vertical.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(rows, f, indent=2, ensure_ascii=False, default=str)

print(f"Saglabats: {len(rows)} rindas -> week1/scheme_by_vertical.json")
schemes  = sorted(set(r["scheme"] for r in rows))
print(f"Shemas: {schemes}")
for s in schemes:
    t = sum(r["payment_count"] for r in rows if r["scheme"] == s)
    print(f"  {s}: {t} maksajumi")
