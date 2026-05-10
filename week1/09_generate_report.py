"""
09_generate_report.py
Rīks 3: Apvieno visus rezultātus vienā HTML lapā.
"""

import os
import json
import base64

script_dir = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(script_dir, "analysis_plan.json"), "r", encoding="utf-8") as f:
    plan = json.load(f)["plan"]

with open(os.path.join(script_dir, "plan_results.json"), "r", encoding="utf-8") as f:
    results = json.load(f)

def img_to_base64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return None

html = """<!DOCTYPE html>
<html lang="lv">
<head>
<meta charset="UTF-8">
<title>Direct Payments — Datu Analīze</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { background: #0f0f1a; color: #cdd6f4; font-family: 'Segoe UI', sans-serif; }
  header { background: linear-gradient(135deg, #1e1e2e, #313244);
           padding: 40px; text-align: center; border-bottom: 2px solid #7c9ef5; }
  header h1 { font-size: 2.2em; color: #7c9ef5; margin-bottom: 8px; }
  header p { color: #a6adc8; font-size: 1.1em; }
  .summary { display: flex; justify-content: center; gap: 30px;
             padding: 30px; background: #1e1e2e; }
  .stat { text-align: center; background: #313244;
          padding: 20px 35px; border-radius: 12px; border-top: 3px solid #7c9ef5; }
  .stat .num { font-size: 2em; color: #7c9ef5; font-weight: bold; }
  .stat .lbl { color: #a6adc8; margin-top: 5px; }
  .section { max-width: 1100px; margin: 40px auto; padding: 0 20px; }
  .card { background: #1e1e2e; border-radius: 16px; margin-bottom: 50px;
          border: 1px solid #313244; overflow: hidden; }
  .card-header { background: #313244; padding: 20px 30px;
                 border-left: 4px solid #7c9ef5; }
  .card-header h2 { color: #cdd6f4; font-size: 1.4em; }
  .card-header .meta { color: #a6adc8; font-size: 0.9em; margin-top: 5px; }
  .card-body { padding: 25px 30px; }
  .card-body img { width: 100%; border-radius: 10px; margin-bottom: 20px; }
  .description { color: #a6adc8; margin-bottom: 15px; font-style: italic; }
  .insight { background: #313244; border-left: 3px solid #a6e3a1;
             padding: 15px 20px; border-radius: 8px; color: #cdd6f4; line-height: 1.7; }
  .separator { text-align: center; color: #444; font-size: 1.5em;
               margin: 10px 0 30px; letter-spacing: 8px; }
  .badge { display: inline-block; background: #7c9ef5; color: #1e1e2e;
           padding: 3px 10px; border-radius: 20px; font-size: 0.8em;
           font-weight: bold; margin-left: 10px; }
  footer { text-align: center; padding: 30px; color: #585b70;
           border-top: 1px solid #313244; margin-top: 40px; }
</style>
</head>
<body>
<header>
  <h1>🔍 Direct Payments — Datu Analīze</h1>
  <p>LLM-ģenerēts vizualizāciju plāns un ieskati | Mara Medne | FITA ML kurss</p>
</header>
"""

total_rows = sum(r.get("row_count", 0) for r in results)
html += f"""
<div class="summary">
  <div class="stat"><div class="num">{len(results)}</div><div class="lbl">Vizualizācijas</div></div>
  <div class="stat"><div class="num">{total_rows:,}</div><div class="lbl">Datu rindas</div></div>
  <div class="stat"><div class="num">3</div><div class="lbl">Datubāzes tabulas</div></div>
  <div class="stat"><div class="num">LLM</div><div class="lbl">Ģenerēts plāns</div></div>
</div>
<div class="section">
"""

for i, r in enumerate(results):
    plan_item = next((p for p in plan if p["id"] == r["id"]), {})
    description = plan_item.get("description", "")
    viz = r.get("viz_type", "").upper()

    img_tag = ""
    if r.get("chart"):
        chart_path = os.path.join(script_dir, r["chart"])
        b64 = img_to_base64(chart_path)
        if b64:
            img_tag = f'<img src="data:image/png;base64,{b64}" alt="{r["title"]}">'

    if i > 0:
        html += '<div class="separator">— — —</div>'

    html += f"""
  <div class="card">
    <div class="card-header">
      <h2>{r['id']}. {r['title']} <span class="badge">{viz}</span></h2>
      <div class="meta">📊 {r.get('row_count', 0)} datu rindas</div>
    </div>
    <div class="card-body">
      {img_tag}
      <p class="description">{description}</p>
      <div class="insight">💡 <strong>Ieskats:</strong> {r.get('insight', 'Nav pieejams')}</div>
    </div>
  </div>
"""

html += """
</div>
<footer>Ģenerēts ar Python + OpenRouter LLM | FITA ML kurss 2026 | Mara Medne</footer>
</body></html>"""

output_path = os.path.join(script_dir, "final_report.html")
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"✅ HTML atskaite gatava!")
print(f"📁 Atver: week1/final_report.html")