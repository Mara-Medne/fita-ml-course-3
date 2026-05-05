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

## Autore
Mara Medne
