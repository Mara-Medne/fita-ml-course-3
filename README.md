## Apraksts

Python rīku komplekts, kas izvelk MySQL datubāzes shēmu, izmanto LLM (OpenRouter) SQL vaicājumu un vizualizāciju ģenerēšanai, izpilda vaicājumus un apkopo rezultātus divās HTML atskaitēs — pamata un uzlabotajā.

## Interaktīvā atskaite

**[Skatīt interaktīvo atskaiti (GitHub Pages)](https://mara-medne.github.io/fita-ml-course-3/week1/interactive_report.html)**

Interaktīva HTML atskaite ar Chart.js — datumu filtri, nozaru atlase, dinamiskas diagrammas.

## Datubāze

- **direct_payments** (MySQL 8.0.44)
- 3 tabulas: `mandates` (9 381 ieraksti), `organisations` (431), `payments` (33 461)
- Datu periods: 2018–2019

## Failu struktūra

### 1. posms — Datu ieguve un sagatavošana
- `01_extract_schema.py` — MySQL savienojuma tests
- `02_extract_full_schema.py` — shēmas izvilkšana → `database_schema.json`
- `03_generate_context.py` — LLM konteksta ģenerēšana → `database_context.txt`
- `04_extract_samples.py` — datu paraugu izvilkšana → `sample_data.json`

### 2. posms — SQL ģenerēšana un izpilde (Gemini)
- `05_query_with_gemini.py` — Gemini API SQL ģenerēšana → `generated_queries.sql`
- `06_execute_and_interpret.py` — SQL izpilde → `aggregated_results.json`, `final_report.md`

### 3. posms — LLM vizualizāciju plāns (OpenRouter)
- `07_generate_plan.py` — OpenRouter ģenerē 5 vizualizāciju plānu → `analysis_plan.json`
- `08_execute_plan.py` — SQL izpilde, grafiku ģenerēšana, LLM ieskati → `plan_results.json`, `charts/`
- `09_generate_report.py` — pamata HTML atskaite → `final_report.html`

### 4. posms — Uzlabotās vizualizācijas
- `10_advanced_visualizations.py` — 5 profesionālas diagrammas → `advanced_report.html`
- `11_fetch_monthly_data.py` — mēnešu maksājumu dati pa nozarēm → `monthly_by_vertical.json`
- `12_fetch_scheme_data.py` — maksājumu shēmu dati → `scheme_by_vertical.json`

## Kā palaist

```bash
python -m venv venv
.\venv\Scripts\activate        # Linux/Mac: source venv/bin/activate
pip install -r requirements.txt

# 1. posms — datu ieguve
python week1/01_extract_schema.py
python week1/02_extract_full_schema.py
python week1/03_generate_context.py

python week1/04_extract_samples.py

# 2. posms — SQL ar Gemini
python week1/05_query_with_gemini.py
python week1/06_execute_and_interpret.py

# 3. posms — LLM plāns ar OpenRouter
python week1/07_generate_plan.py
python week1/08_execute_plan.py
python week1/09_generate_report.py

# 4. posms — uzlabotās vizualizācijas
python week1/11_fetch_monthly_data.py
python week1/12_fetch_scheme_data.py
python week1/10_advanced_visualizations.py
```

## Vides mainīgie (`.env`)

```
GEMINI_API_KEY=...
OPENROUTER_API_KEY=...
```

## Autore

Mara Medne — FITA ML kurss 2026
