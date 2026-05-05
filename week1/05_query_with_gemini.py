"""
05_query_with_gemini.py
Izmanto Gemini API (REST) ar automātisku retry.
"""

import os
import json
import time
import requests
from dotenv import load_dotenv

script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
load_dotenv(os.path.join(project_dir, ".env"))

API_KEY = os.getenv("GEMINI_API_KEY")

with open(os.path.join(script_dir, "database_context.txt"), "r", encoding="utf-8") as f:
    db_context = f.read()

with open(os.path.join(script_dir, "sample_data.json"), "r", encoding="utf-8") as f:
    sample_data = f.read()

prompt = f"""Tu esi SQL eksperts. Tev ir MySQL datubāze:

{db_context}

Datu paraugi:
{sample_data}

Uzraksti SQL vaicājumus:
1. Kopējais maksājumu apjoms pa organizācijām
2. Cik mandātu katrai organizācijai
3. Vidējais maksājuma apjoms pa gadiem

Katram TIKAI SQL, formāts:
-- Jautājums 1
SELECT ...
-- Jautājums 2
SELECT ...
-- Jautājums 3
SELECT ...
"""

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}"
data = {"contents": [{"parts": [{"text": prompt}]}]}

for attempt in range(5):
    print(f"🤖 Mēģinājums {attempt + 1}...")
    response = requests.post(url, json=data)
    result = response.json()

    if "candidates" in result:
        sql_text = result["candidates"][0]["content"]["parts"][0]["text"]
        print("\n📝 Ģenerētie SQL vaicājumi:\n")
        print(sql_text)
        with open(os.path.join(script_dir, "generated_queries.sql"), "w", encoding="utf-8") as f:
            f.write(sql_text)
        print("\n✅ Saglabāts: week1/generated_queries.sql")
        break
    else:
        wait = 40
        print(f"⏳ API kvota — gaidu {wait} sekundes...")
        time.sleep(wait)
else:
    print("❌ API neizdevās pēc 5 mēģinājumiem.")
