"""
07_generate_plan.py
Rīks 1: Izmanto LLM (OpenRouter) lai izveidotu vizualizāciju plānu.
"""

import os
import json
import requests
from dotenv import load_dotenv

script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
load_dotenv(os.path.join(project_dir, ".env"))

API_KEY = os.getenv("OPENROUTER_API_KEY")

with open(os.path.join(script_dir, "database_context.txt"), "r", encoding="utf-8") as f:
    db_context = f.read()

with open(os.path.join(script_dir, "sample_data.json"), "r", encoding="utf-8") as f:
    sample_data = f.read()

prompt = f"""Tu esi datu analītiķis. Tev ir MySQL datubāze ar šādu struktūru:

{db_context}

Datu paraugi:
{sample_data}

Izveido vizualizāciju plānu ar TIEŠI 5 punktiem. Katram punktam norādi:
- id: skaitlis 1-5
- title: īss nosaukums latviski
- description: ko šis grafiks parādīs (1-2 teikumi latviski)
- viz_type: viens no: bar, line, pie, horizontal_bar, scatter
- sql_hint: īss norādījums kādas kolonnas/tabulas izmantot
- separator: "---"

Atbildi TIKAI ar derīgu JSON, bez papildu teksta, bez ```atzīmēm:
{{
  "plan": [
    {{
      "id": 1,
      "title": "...",
      "description": "...",
      "viz_type": "bar",
      "sql_hint": "...",
      "separator": "---"
    }}
  ]
}}"""

url = "https://openrouter.ai/api/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}
data = {
    "model": "nvidia/nemotron-3-super-120b-a12b:free",
    "messages": [{"role": "user", "content": prompt}]
}

print("🤖 LLM ģenerē vizualizāciju plānu...")
response = requests.post(url, headers=headers, json=data)
result = response.json()

if "choices" in result:
    raw_text = result["choices"][0]["message"]["content"].strip()
    if "```" in raw_text:
        raw_text = raw_text.split("```")[1]
        if raw_text.startswith("json"):
            raw_text = raw_text[4:]
    raw_text = raw_text.strip()
    try:
        plan = json.loads(raw_text)
        output_path = os.path.join(script_dir, "analysis_plan.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(plan, f, indent=2, ensure_ascii=False)
        print(f"\n✅ Plāns izveidots ar {len(plan['plan'])} punktiem:\n")
        for item in plan["plan"]:
            print(f"   {item['separator']}")
            print(f"   {item['id']}. {item['title']} [{item['viz_type']}]")
            print(f"      {item['description']}")
        print("   ---")
        print(f"\n📁 Saglabāts: week1/analysis_plan.json")
    except json.JSONDecodeError as e:
        print(f"❌ JSON kļūda: {e}")
        print(f"Raw: {raw_text[:300]}")
else:
    print(f"❌ Kļūda: {result}")