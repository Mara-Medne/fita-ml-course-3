"""
08_execute_plan.py
Rīks 2: Katram plāna punktam ģenerē SQL, izpilda, vizualizē un raksta ieskatus.
"""

import os
import json
import requests
import mysql.connector
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from dotenv import load_dotenv

script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
load_dotenv(os.path.join(project_dir, ".env"))

API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "nvidia/nemotron-3-super-120b-a12b:free"

DB_CONFIG = {
    "host": "87.110.123.151",
    "user": "fita",
    "password": "2026-04-28",
    "database": "direct_payments",
    "connection_timeout": 10,
}

with open(os.path.join(script_dir, "analysis_plan.json"), "r", encoding="utf-8") as f:
    plan = json.load(f)["plan"]

with open(os.path.join(script_dir, "database_context.txt"), "r", encoding="utf-8") as f:
    db_context = f.read()

charts_dir = os.path.join(script_dir, "charts")
os.makedirs(charts_dir, exist_ok=True)

def ask_llm(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    data = {"model": MODEL, "messages": [{"role": "user", "content": prompt}]}
    r = requests.post(url, headers=headers, json=data)
    result = r.json()
    if "choices" in result:
        return result["choices"][0]["message"]["content"].strip()
    return None

def clean_sql(text):
    if "```" in text:
        text = text.split("```")[1]
        if text.startswith("sql"):
            text = text[3:]
    return text.strip().rstrip(";")

def make_chart(item, rows):
    viz = item["viz_type"]
    title = item["title"]
    chart_path = os.path.join(charts_dir, f"chart_{item['id']}.png")

    if not rows or len(rows[0]) < 2:
        return None

    keys = list(rows[0].keys())
    labels = [str(r[keys[0]])[:20] for r in rows[:15]]
    values = []
    for r in rows[:15]:
        try:
            values.append(float(r[keys[1]]))
        except:
            values.append(0)

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('#1e1e2e')
    ax.set_facecolor('#1e1e2e')
    ax.tick_params(colors='white')
    ax.title.set_color('white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    for spine in ax.spines.values():
        spine.set_edgecolor('#444')

    colors = ['#7c9ef5', '#f5a97f', '#a6e3a1', '#f38ba8', '#cba6f7']

    if viz == "pie":
        ax.pie(values, labels=labels, autopct='%1.1f%%',
               colors=colors, textprops={'color': 'white'})
    elif viz == "horizontal_bar":
        ax.barh(labels, values, color=colors[0])
        ax.invert_yaxis()
    elif viz == "line":
        ax.plot(labels, values, marker='o', color=colors[0], linewidth=2)
        plt.xticks(rotation=45, ha='right')
    else:
        ax.bar(labels, values, color=colors[0])
        plt.xticks(rotation=45, ha='right')

    ax.set_title(title, fontsize=14, pad=15)
    plt.tight_layout()
    plt.savefig(chart_path, dpi=150, bbox_inches='tight',
                facecolor=fig.get_facecolor())
    plt.close()
    return chart_path

results = []
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor(dictionary=True)

for item in plan:
    print(f"\n{'='*50}")
    print(f"📊 {item['id']}. {item['title']}")

    # a) SQL ģenerēšana
    sql_prompt = f"""Tev ir MySQL datubāze:
{db_context}

Uzraksti TIKAI vienu SQL vaicājumu priekš: {item['title']}
Hints: {item['sql_hint']}
Atbildi TIKAI ar SQL, bez komentāriem, bez ```atzīmēm."""

    sql_raw = ask_llm(sql_prompt)
    if not sql_raw:
        print("  ❌ SQL ģenerēšana neizdevās")
        continue

    sql = clean_sql(sql_raw)
    print(f"  SQL: {sql[:80]}...")

    # SQL izpilde
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        rows = [{k: (float(v) if hasattr(v, '__float__') else v)
                 for k, v in r.items()} for r in rows]
        print(f"  ✅ {len(rows)} rindas")
    except Exception as e:
        print(f"  ❌ SQL kļūda: {e}")
        continue

    # b) Grafiks
    chart_path = make_chart(item, rows)
    if chart_path:
        print(f"  📈 Grafiks: {os.path.basename(chart_path)}")

    # c) Ieskati
    insight_prompt = f"""Datu analītiķis raksta īsu aprakstu latviešu valodā (3-4 teikumi).
Grafika nosaukums: {item['title']}
Dati (pirmās 5 rindas): {json.dumps(rows[:5], ensure_ascii=False, default=str)}
Uzraksti konkrētus, noderīgus ieskatus par šiem datiem."""

    insight = ask_llm(insight_prompt)
    print(f"  💡 Ieskats: {insight[:100] if insight else 'Nav'}...")

    results.append({
        "id": item["id"],
        "title": item["title"],
        "viz_type": item["viz_type"],
        "sql": sql,
        "row_count": len(rows),
        "chart": f"charts/chart_{item['id']}.png" if chart_path else None,
        "insight": insight,
        "data": rows[:10]
    })

cursor.close()
conn.close()

with open(os.path.join(script_dir, "plan_results.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False, default=str)

print(f"\n✅ Gatavs! {len(results)}/5 punkti izpildīti")
print(f"📁 Saglabāts: week1/plan_results.json")
print(f"📁 Grafiki: week1/charts/")