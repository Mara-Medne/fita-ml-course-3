"""
03_generate_context.py
Pārveido JSON shēmu cilvēkam draudzīgā tekstā Gemini API.
"""

import json
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(script_dir, "database_schema.json"), "r", encoding="utf-8") as f:
    schema = json.load(f)

lines = [f"# Datubāze: {schema['database']}\n"]

for table in schema["tables"]:
    lines.append(f"\n## Tabula: {table['name']}")
    lines.append(f"Rindu skaits: {table['row_count']}")
    if table.get("comment"):
        lines.append(f"Apraksts: {table['comment']}")
    
    lines.append("\nKolonnas:")
    for col in table["columns"]:
        nullable = "NULL" if col["IS_NULLABLE"] == "YES" else "NOT NULL"
        key = f" [{col['COLUMN_KEY']}]" if col["COLUMN_KEY"] else ""
        comment = f" — {col['COLUMN_COMMENT']}" if col.get("COLUMN_COMMENT") else ""
        lines.append(f"  - {col['COLUMN_NAME']}: {col['DATA_TYPE']} {nullable}{key}{comment}")
    
    if table["foreign_keys"]:
        lines.append("\nForeign keys:")
        for fk in table["foreign_keys"]:
            lines.append(f"  - {fk['COLUMN_NAME']} → {fk['REFERENCED_TABLE_NAME']}.{fk['REFERENCED_COLUMN_NAME']}")

context = "\n".join(lines)

with open(os.path.join(script_dir, "database_context.txt"), "w", encoding="utf-8") as f:
    f.write(context)

print("✅ Saglabāts: week1/database_context.txt")
print(f"\nGarums: {len(context)} simboli")