"""
11_fetch_monthly_data.py
Vaicā datubāzi — iegūst mēnešu maksājumu un mandātu datus pa nozarēm.
Saglabā: week1/monthly_by_vertical.json
"""

import os
import json
import mysql.connector

script_dir = os.path.dirname(os.path.abspath(__file__))

DB_CONFIG = {
    "host": "87.110.123.151",
    "user": "fita",
    "password": "2026-04-28",
    "database": "direct_payments",
    "connection_timeout": 10,
}

SQL_PAYMENTS = """
SELECT
    o.parent_vertical AS vertical,
    DATE_FORMAT(p.charge_date, '%Y-%m') AS month,
    COUNT(*) AS payment_count,
    ROUND(SUM(p.amount), 2) AS total_amount
FROM payments p
JOIN mandates m ON p.mandate_id = m.id
JOIN organisations o ON m.organisation_id = o.id
GROUP BY o.parent_vertical, month
ORDER BY month, o.parent_vertical
"""

SQL_MANDATES = """
SELECT
    o.parent_vertical AS vertical,
    DATE_FORMAT(m.created_at, '%Y-%m') AS month,
    COUNT(*) AS mandate_count
FROM mandates m
JOIN organisations o ON m.organisation_id = o.id
GROUP BY o.parent_vertical, month
ORDER BY month, o.parent_vertical
"""

print("Savienojas ar datubazi...")
conn   = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor(dictionary=True)

print("Vaica maksajumu datus pa nozarem un menesiem...")
cursor.execute(SQL_PAYMENTS)
payments_rows = cursor.fetchall()
print(f"  {len(payments_rows)} rindas")

print("Vaica mandatu datus pa nozarem un menesiem...")
cursor.execute(SQL_MANDATES)
mandates_rows = cursor.fetchall()
print(f"  {len(mandates_rows)} rindas")

cursor.close()
conn.close()

# Konvertē decimal uz float
def clean(rows):
    return [{k: (float(v) if hasattr(v, '__float__') and not isinstance(v, (int, float)) else v)
             for k, v in r.items()} for r in rows]

result = {
    "payments_by_vertical_month": clean(payments_rows),
    "mandates_by_vertical_month": clean(mandates_rows),
}

out = os.path.join(script_dir, "monthly_by_vertical.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False, default=str)

print(f"\nSaglabats: week1/monthly_by_vertical.json")

# Atra parskats
months_p = sorted(set(r["month"] for r in payments_rows))
verts    = sorted(set(r["vertical"] for r in payments_rows))
print(f"Menesi: {months_p[0]} - {months_p[-1]} ({len(months_p)} menesi)")
print(f"Nozares: {len(verts)}")
for v in verts:
    total = sum(r["payment_count"] for r in payments_rows if r["vertical"] == v)
    print(f"  {v}: {total} maksajumi")
