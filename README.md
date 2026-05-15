# FITA 3. kurss — 1. nedēļas B uzdevums

## Apraksts
Python rīks, kas izvelk MySQL datubāzes shēmu, ģenerē kontekstu LLM,
izmanto Gemini API SQL vaicājumu ģenerēšanai, izpilda tos un apkopo rezultātus.

## Datubāze
- direct_payments (MySQL 8.0.44)
- 3 tabulas: mandates (9381), organisations (431), payments (33461)

## Failu struktūra
- 01_extract_schema.py — MySQL savienojuma tests
- 02_extract_full_schema.py — shēmas izvilkšana
- 03_generate_context.py — konteksta ģenerēšana
- 04_extract_samples.py — datu paraugu izvilkšana
- 05_query_with_gemini.py — Gemini API SQL ģenerēšana
- 06_execute_and_interpret.py — SQL izpilde un rezultātu apkopojums

## Kā palaist
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python week1/01_extract_schema.py
python week1/02_extract_full_schema.py
python week1/03_generate_context.py
python week1/04_extract_samples.py
python week1/05_query_with_gemini.py
python week1/06_execute_and_interpret.py

## Izmantotie modeļi un versijas

| Pakotne / Modelis | Versija / ID |
|---|---|
| Python | 3.11 |
| mysql-connector-python | 9.6.0 |
| python-dotenv | jaunākā |
| requests | jaunākā |
| matplotlib | jaunākā |
| Gemini API modelis | gemini-pro |
| OpenRouter modelis | nvidia/nemotron-3-super-120b-a12b:free |
| MySQL datubāze | 8.0.44 |

## Docker Compose

### Sagatavošana

```bash
# 1. Kopē .env šablonu un aizpildi API atslēgas
cp .env.example .env
```

`.env` failā ieraksti:
```
GEMINI_API_KEY=tava_gemini_atslega
OPENROUTER_API_KEY=tava_openrouter_atslega
```

### Palaišana

```bash
# Uzbūvē Docker image
docker compose build

# Palaid 1. skriptu (noklusējums)
docker compose run --rm week1

# Palaid konkrētu skriptu
SCRIPT=02_extract_full_schema.py docker compose run --rm week1
SCRIPT=03_generate_context.py docker compose run --rm week1
SCRIPT=04_extract_samples.py docker compose run --rm week1
SCRIPT=05_query_with_gemini.py docker compose run --rm week1
SCRIPT=06_execute_and_interpret.py docker compose run --rm week1
SCRIPT=07_generate_plan.py docker compose run --rm week1
SCRIPT=08_execute_plan.py docker compose run --rm week1
SCRIPT=09_generate_report.py docker compose run --rm week1
```

### Logi

```bash
# Reāllaika logi
docker compose logs -f week1

# Pēdējās 50 rindas
docker compose logs --tail=50 week1
```

Logi tiek saglabāti JSON formātā ar automātisku rotāciju (10 MB × 5 faili).

## Autore
Mara Medne
