"""
10_advanced_visualizations.py
Uzlabota vizualizācijas sistēma — 5 profesionālas diagrammas ar latviskām nosaukumiem.
Lasa: aggregated_results.json, plan_results.json
Saglabā: advanced_report.html
"""

import os
import sys
import json
import base64
import io
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

script_dir = os.path.dirname(os.path.abspath(__file__))

# ── Datu ielāde ───────────────────────────────────────────────────────────────
with open(os.path.join(script_dir, "aggregated_results.json"), "r", encoding="utf-8") as f:
    agg = json.load(f)

with open(os.path.join(script_dir, "plan_results.json"), "r", encoding="utf-8") as f:
    plan = json.load(f)

# ── Krāsu palete (tumšais dizains) ───────────────────────────────────────────
BG      = '#0f0f1a'
CARD    = '#1e1e2e'
SURFACE = '#313244'
ACCENT  = '#7c9ef5'
TEXT    = '#cdd6f4'
MUTED   = '#a6adc8'
GREEN   = '#a6e3a1'
YELLOW  = '#f9e2af'
RED     = '#f38ba8'
MAUVE   = '#cba6f7'
TEAL    = '#89dceb'
PEACH   = '#fab387'

PALETTE = [ACCENT, GREEN, YELLOW, RED, MAUVE, TEAL, PEACH]

VERT_LV = {
    "digital_services_media_telecoms":          "Digitālie pakalpojumi & Telekomunikācijas",
    "professional_and_financial_services":      "Profesionālie & Finanšu pakalpojumi",
    "sports_fitness":                           "Sports & Fiziskā sagatavotība",
    "property":                                 "Īpašums",
    "tradesmen_and_non_professionals_services": "Amatnieki & Neprofesionālie pakalpojumi",
    "healthcare":                               "Veselības aprūpe",
    "societies_and_clubs":                      "Biedrības & Klubi",
}

VERT_SHORT = {
    "digital_services_media_telecoms":          "Digitālie\npak.",
    "professional_and_financial_services":      "Prof. &\nFinanšu",
    "sports_fitness":                           "Sports\n& Fitness",
    "property":                                 "Īpašums",
    "tradesmen_and_non_professionals_services": "Amatnieki\n& Nep.",
    "healthcare":                               "Veselības\naprūpe",
    "societies_and_clubs":                      "Biedrības\n& Klubi",
}

LV_MON = ['Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jūn',
           'Jūl', 'Aug', 'Sep', 'Okt', 'Nov', 'Dec']


def fig_to_b64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=150, bbox_inches='tight',
                facecolor=BG, edgecolor='none')
    buf.seek(0)
    return base64.b64encode(buf.read()).decode()


def style_ax(ax):
    ax.set_facecolor(CARD)
    ax.tick_params(colors=MUTED, labelsize=9)
    for spine in ax.spines.values():
        spine.set_color(SURFACE)
        spine.set_linewidth(0.5)
    ax.xaxis.label.set_color(MUTED)
    ax.yaxis.label.set_color(MUTED)
    ax.title.set_color(TEXT)


charts_b64 = {}
print("⏳ Ģenerē vizualizācijas...\n")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 1. Nozaru kopējie maksājumu apjomi  (horizontālie joslas, sakārtotas)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
d1      = plan[0]["data"]
raw1    = [r["parent_vertical"] for r in d1]
vals1   = [r["total"] for r in d1]
labs1   = [VERT_LV.get(v, v) for v in raw1]
total1  = sum(vals1)

order1       = list(np.argsort(vals1))
vals1_s      = [vals1[i] for i in order1]
labs1_s      = [labs1[i] for i in order1]
colors1      = [PALETTE[i % len(PALETTE)] for i in range(len(vals1_s))]

fig1, ax1 = plt.subplots(figsize=(13, 6))
fig1.patch.set_facecolor(BG)
style_ax(ax1)

bars1 = ax1.barh(range(len(labs1_s)), vals1_s, color=colors1,
                 height=0.65, edgecolor='none')
for bar, val in zip(bars1, vals1_s):
    pct = val / total1 * 100
    ax1.text(bar.get_width() + total1 * 0.007,
             bar.get_y() + bar.get_height() / 2,
             f'€{val:,.0f}  ({pct:.1f}%)',
             va='center', color=TEXT, fontsize=8.5, fontweight='bold')

ax1.set_yticks(range(len(labs1_s)))
ax1.set_yticklabels(labs1_s, fontsize=9)
ax1.set_xlabel('Kopējie maksājumi (EUR)', fontsize=10)
ax1.set_title('Nozaru kopējie maksājumu apjomi', fontsize=14, fontweight='bold', pad=16)
ax1.set_xlim(0, max(vals1_s) * 1.45)
ax1.grid(axis='x', color=SURFACE, linewidth=0.5, linestyle='--', alpha=0.7)
ax1.set_axisbelow(True)
ax1.text(0.99, 0.02, f'Kopā: €{total1:,.0f}',
         transform=ax1.transAxes, ha='right', va='bottom',
         color=MUTED, fontsize=9,
         bbox=dict(boxstyle='round,pad=0.3', facecolor=SURFACE, edgecolor='none', alpha=0.8))
fig1.tight_layout(pad=1.5)
charts_b64['v1'] = fig_to_b64(fig1)
plt.close(fig1)
print("  ✓ 1/5 — Nozaru kopējie maksājumu apjomi")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2. Maksājumu laika dinamika pa mēnešiem  (platības + līnija)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
d2      = plan[1]["data"]
months  = [r["month"] for r in d2]
counts  = [r["payment_count"] for r in d2]
xlabs2  = [f"{LV_MON[int(m.split('-')[1])-1]}\n{m.split('-')[0]}" for m in months]
x2      = np.arange(len(months))
maxc    = max(counts)

fig2, ax2 = plt.subplots(figsize=(14, 6))
fig2.patch.set_facecolor(BG)
style_ax(ax2)

ax2.fill_between(x2, counts, alpha=0.18, color=ACCENT)
ax2.plot(x2, counts, color=ACCENT, linewidth=2.5, marker='o',
         markersize=6, markerfacecolor=CARD, markeredgecolor=ACCENT,
         markeredgewidth=2, zorder=5)

# Maksimuma anotācija
mi = int(np.argmax(counts))
ax2.annotate(f'Maksimums\n{counts[mi]:,.0f}',
             xy=(x2[mi], counts[mi]),
             xytext=(x2[mi] - min(2, mi), counts[mi] * 0.82),
             color=YELLOW, fontsize=8.5, fontweight='bold',
             arrowprops=dict(arrowstyle='->', color=YELLOW, lw=1.5),
             bbox=dict(boxstyle='round,pad=0.3', facecolor=SURFACE,
                       edgecolor='none', alpha=0.85))

# Gadu robeža
yr_idx = next((i for i, m in enumerate(months) if m.startswith('2019')), None)
if yr_idx:
    ax2.axvline(x=yr_idx - 0.5, color=MUTED, linewidth=1.2,
                linestyle='--', alpha=0.5)
    ax2.text(yr_idx - 0.35, maxc * 0.97, '2019 →',
             color=MUTED, fontsize=8.5, va='top')

ax2.set_xticks(x2)
ax2.set_xticklabels(xlabs2, fontsize=8)
ax2.set_ylabel('Maksājumu skaits', fontsize=10)
ax2.set_title('Maksājumu laika dinamika pa mēnešiem', fontsize=14, fontweight='bold', pad=16)
ax2.grid(axis='y', color=SURFACE, linewidth=0.5, linestyle='--', alpha=0.7)
ax2.set_axisbelow(True)
ax2.set_xlim(-0.5, len(months) - 0.5)
ax2.set_ylim(0, maxc * 1.22)

if counts[0] > 0:
    growth = (counts[-1] - counts[0]) / counts[0] * 100
    ax2.text(0.99, 0.97, f'Izaugsme: +{growth:.0f}%',
             transform=ax2.transAxes, ha='right', va='top',
             color=GREEN, fontsize=9, fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.3', facecolor=SURFACE,
                       edgecolor='none', alpha=0.85))
fig2.tight_layout(pad=1.5)
charts_b64['v2'] = fig_to_b64(fig2)
plt.close(fig2)
print("  ✓ 2/5 — Maksājumu laika dinamika")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3. Mandātu skaits vs Kopējie maksājumi  (izkliedes grafiks pa nozarēm)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
q1m = {r["organisation_id"]: r for r in agg[0]["data"]}
q2m = {r["organisation_id"]: r for r in agg[1]["data"]}
common_ids = set(q1m) & set(q2m)

pts3 = [(q1m[oid]["total_payments"],
         q2m[oid]["mandate_count"],
         q1m[oid]["parent_vertical"])
        for oid in common_ids]

verts3     = sorted(set(p[2] for p in pts3))
vcol3      = {v: PALETTE[i % len(PALETTE)] for i, v in enumerate(verts3)}

fig3, ax3 = plt.subplots(figsize=(12, 7))
fig3.patch.set_facecolor(BG)
style_ax(ax3)

for v in verts3:
    sub = [(p[0], p[1]) for p in pts3 if p[2] == v]
    if sub:
        xs, ys = zip(*sub)
        ax3.scatter(xs, ys, c=vcol3[v], s=140, alpha=0.85,
                    edgecolors=CARD, linewidth=1.5, zorder=4,
                    label=VERT_LV.get(v, v))

allx3 = [p[0] for p in pts3]
ally3 = [p[1] for p in pts3]
if len(allx3) > 2:
    z3 = np.polyfit(allx3, ally3, 1)
    xl = np.linspace(min(allx3), max(allx3), 200)
    ax3.plot(xl, np.poly1d(z3)(xl), '--', color=MUTED,
             linewidth=1.5, alpha=0.5, label='Tendences līnija', zorder=3)

ax3.set_xlabel('Kopējie maksājumi (EUR)', fontsize=10)
ax3.set_ylabel('Mandātu skaits', fontsize=10)
ax3.set_title('Mandātu skaita un Maksājumu apjoma saistība pa nozarēm',
              fontsize=14, fontweight='bold', pad=16)
ax3.grid(color=SURFACE, linewidth=0.5, linestyle='--', alpha=0.5)
ax3.set_axisbelow(True)
ax3.legend(loc='upper left', facecolor=SURFACE, edgecolor='none',
           labelcolor=TEXT, fontsize=8, framealpha=0.9, borderpad=0.7)
fig3.tight_layout(pad=1.5)
charts_b64['v3'] = fig_to_b64(fig3)
plt.close(fig3)
print("  ✓ 3/5 — Mandātu un Maksājumu korelācija")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 4. Maksājumu shēmu sadalījums  (rinka diagramma + statistikas panelis)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
d4     = plan[2]["data"]
slbls  = [r["scheme"].upper() for r in d4]
svals  = [r["cnt"] for r in d4]
scols  = [ACCENT, GREEN]
stotal = sum(svals)
sdescs = ['Lielbritānijas tiešo debetu sistēma', 'Eiropas vienotās maksājumu zonas shēma']

fig4, (ax4l, ax4r) = plt.subplots(1, 2, figsize=(13, 6),
                                   gridspec_kw={'width_ratios': [1.1, 0.9]})
fig4.patch.set_facecolor(BG)
ax4l.set_facecolor(BG)

wedges, _, autotexts = ax4l.pie(
    svals, colors=scols, autopct='%1.1f%%',
    startangle=90, pctdistance=0.72,
    wedgeprops=dict(width=0.52, edgecolor=BG, linewidth=4))
for at in autotexts:
    at.set_color(CARD)
    at.set_fontsize(13)
    at.set_fontweight('bold')

ax4l.text(0, 0.08, f'{stotal:,.0f}', ha='center', va='center',
          color=TEXT, fontsize=16, fontweight='bold')
ax4l.text(0, -0.16, 'kopā\nmaksājumi', ha='center', va='center',
          color=MUTED, fontsize=9)
ax4l.set_title('Maksājumu shēmu sadalījums', color=TEXT,
               fontsize=13, fontweight='bold', pad=14)

ax4r.set_facecolor(BG)
ax4r.axis('off')
yb = [0.68, 0.28]
for i, (lbl, val, col, desc, y) in enumerate(
        zip(slbls, svals, scols, sdescs, yb)):
    rect = mpatches.FancyBboxPatch(
        (0.04, y - 0.06), 0.92, 0.30,
        boxstyle='round,pad=0.03',
        facecolor=SURFACE, edgecolor=col, linewidth=2,
        transform=ax4r.transAxes)
    ax4r.add_patch(rect)
    ax4r.text(0.13, y + 0.17, lbl,
              transform=ax4r.transAxes, color=col,
              fontsize=13, fontweight='bold', va='center')
    ax4r.text(0.13, y + 0.06, f'{val:,.0f} maksājumi',
              transform=ax4r.transAxes, color=TEXT, fontsize=10, va='center')
    ax4r.text(0.13, y - 0.01, f'{val/stotal*100:.1f}% no kopējā skaita',
              transform=ax4r.transAxes, color=MUTED, fontsize=9, va='center')
    ax4r.text(0.13, y - 0.09, desc,
              transform=ax4r.transAxes, color=MUTED, fontsize=8,
              va='center', style='italic')

fig4.tight_layout(pad=1.5)
charts_b64['v4'] = fig_to_b64(fig4)
plt.close(fig4)
print("  ✓ 4/5 — Maksājumu shēmu sadalījums")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 5. Top 10 organizāciju maksājumu apjomi pēc nozarēm  (joslu grafiks)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
d5      = plan[3]["data"]
q1lkp   = {r["organisation_id"]: r["parent_vertical"] for r in agg[0]["data"]}
olbls5  = [f'#{i+1}' for i in range(len(d5))]
ovals5  = [r["total"] for r in d5]
overts5 = [q1lkp.get(r["org_id"], "nezināms") for r in d5]
max5    = max(ovals5)

all_v5  = sorted(set(overts5))
vcol5   = {v: PALETTE[i % len(PALETTE)] for i, v in enumerate(all_v5)}
bcols5  = [vcol5[v] for v in overts5]

fig5, ax5 = plt.subplots(figsize=(13, 6))
fig5.patch.set_facecolor(BG)
style_ax(ax5)

x5    = np.arange(len(olbls5))
bars5 = ax5.bar(x5, ovals5, color=bcols5, width=0.65, edgecolor='none', zorder=4)

for bar, val in zip(bars5, ovals5):
    ax5.text(bar.get_x() + bar.get_width() / 2,
             bar.get_height() + max5 * 0.012,
             f'€{val/1000:.0f}k',
             ha='center', va='bottom', color=TEXT, fontsize=8.5, fontweight='bold')

for bar, vert in zip(bars5, overts5):
    ax5.text(bar.get_x() + bar.get_width() / 2,
             -max5 * 0.055,
             VERT_SHORT.get(vert, vert),
             ha='center', va='top', color=MUTED, fontsize=7)

ax5.set_xticks(x5)
ax5.set_xticklabels(olbls5, fontsize=9)
ax5.set_ylabel('Kopējie maksājumi (EUR)', fontsize=10)
ax5.set_title('Top 10 organizāciju maksājumu apjomi pēc nozarēm',
              fontsize=14, fontweight='bold', pad=16)
ax5.grid(axis='y', color=SURFACE, linewidth=0.5, linestyle='--', alpha=0.7)
ax5.set_axisbelow(True)
ax5.set_ylim(-max5 * 0.14, max5 * 1.15)

handles5 = [mpatches.Patch(color=vcol5[v], label=VERT_LV.get(v, v)) for v in all_v5]
ax5.legend(handles=handles5, loc='upper right', facecolor=SURFACE,
           edgecolor='none', labelcolor=TEXT, fontsize=8, framealpha=0.9)
fig5.tight_layout(pad=2)
charts_b64['v5'] = fig_to_b64(fig5)
plt.close(fig5)
print("  ✓ 5/5 — Top 10 organizāciju salīdzinājums")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# HTML atskaites ģenerēšana
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
viz_meta = [
    {
        "key":   "v1",
        "title": "Nozaru kopējie maksājumu apjomi",
        "badge": "HORIZONTĀLIE JOSLAS",
        "desc":  ("Salīdzinājums starp 7 nozarēm pēc kopējiem maksājumu apjomiem EUR. "
                  "Joslas sakārtotas augošā secībā — no mazākās līdz lielākajai nozarei."),
        "insight": plan[0].get("insight") or
                   ("Digitālie pakalpojumi & Telekomunikācijas dominē ar €1.19M — aptuveni "
                    "1.5× vairāk nekā nākamā nozare. Biedrības & Klubi uzrāda vismazāko apjomu."),
        "rows":  plan[0].get("row_count", 7),
        "sql":   plan[0].get("sql", ""),
    },
    {
        "key":   "v2",
        "title": "Maksājumu laika dinamika pa mēnešiem",
        "badge": "LAIKA RINDA",
        "desc":  ("Maksājumu skaita izmaiņas no 2018. gada aprīļa. "
                  "Redzama strauja eksponenciāla izaugsme platformas agrīnajā periodā."),
        "insight": plan[1].get("insight") or
                   ("No 54 maksājumiem aprīlī 2018 līdz >6000 janvārī 2019 — "
                    "vairāk nekā 100× izaugsme. Straujākais kāpums: +645% maijā."),
        "rows":  plan[1].get("row_count", len(d2)),
        "sql":   plan[1].get("sql", ""),
    },
    {
        "key":   "v3",
        "title": "Mandātu skaita un Maksājumu apjoma saistība pa nozarēm",
        "badge": "IZKLIEDES GRAFIKS",
        "desc":  ("Katrs punkts — viena organizācija. X ass: kopējie maksājumi, "
                  f"Y ass: mandātu skaits. Krāsas atbilst nozarēm. "
                  f"Analizētas {len(common_ids)} organizācijas."),
        "insight": ("Lielākā daļa organizāciju ar augstu mandātu skaitu (>400) pieder "
                    "sports & fitness nozarei. Veselības aprūpe un profesionālie pakalpojumi "
                    "uzrāda augstākus maksājumus ar mazāku mandātu skaitu — augstāka "
                    "vidējā maksājuma vērtība."),
        "rows":  len(common_ids),
        "sql":   "Savienoti: aggregated_results.json — Jautājums 1 (maksājumi) + Jautājums 2 (mandāti)",
    },
    {
        "key":   "v4",
        "title": "Maksājumu shēmu sadalījums",
        "badge": "RINKA DIAGRAMMA",
        "desc":  ("BACS (Lielbritānija) un SEPA Core (Eiropa) maksājumu shēmu "
                  f"sadalījums — kopā {stotal:,.0f} maksājumi."),
        "insight": (f"BACS dominē ar {svals[0]:,.0f} maksājumiem ({svals[0]/stotal*100:.1f}%), "
                    f"SEPA Core — {svals[1]:,.0f} ({svals[1]/stotal*100:.1f}%). "
                    "Proporcionāli liecina, ka lielākā daļa klientu darbojas Lielbritānijā."),
        "rows":  plan[2].get("row_count", 2),
        "sql":   plan[2].get("sql", ""),
    },
    {
        "key":   "v5",
        "title": "Top 10 organizāciju maksājumu apjomi pēc nozarēm",
        "badge": "JOSLU GRAFIKS",
        "desc":  ("Desmit labākās organizācijas pēc kopējiem maksājumu apjomiem. "
                  "Krāsas un apzīmējumi norāda piederību nozarei."),
        "insight": plan[3].get("insight") or
                   ("Lielākā organizācija sasniedz €305k. Top 3 kopā — vairāk nekā €800k, "
                    "kas veido ~20% no visu organizāciju kopējā apjoma."),
        "rows":  plan[3].get("row_count", 10),
        "sql":   plan[3].get("sql", ""),
    },
]

gen_date  = datetime.now().strftime("%d.%m.%Y %H:%M")
total_rows = sum(m["rows"] for m in viz_meta)

# --- HTML veidne ---------------------------------------------------------------
html = f"""<!DOCTYPE html>
<html lang="lv">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Uzlabotā Analītikas Atskaite — Direct Payments</title>
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    background: #0f0f1a;
    color: #cdd6f4;
    font-family: 'Segoe UI', system-ui, sans-serif;
    line-height: 1.6;
  }}

  /* ── Galvene ── */
  header {{
    background: linear-gradient(135deg, #1e1e2e 0%, #252540 50%, #1e1e2e 100%);
    padding: 50px 40px 38px;
    text-align: center;
    border-bottom: 2px solid #7c9ef5;
    position: relative;
    overflow: hidden;
  }}
  header::before {{
    content: '';
    position: absolute; inset: 0;
    background: radial-gradient(ellipse at 50% 0%,
                rgba(124,158,245,.13) 0%, transparent 70%);
  }}
  .header-chip {{
    display: inline-block;
    background: rgba(124,158,245,.14);
    color: #7c9ef5;
    border: 1px solid rgba(124,158,245,.28);
    padding: 4px 16px;
    border-radius: 20px;
    font-size: .78em;
    letter-spacing: .1em;
    text-transform: uppercase;
    margin-bottom: 18px;
    position: relative;
  }}
  header h1 {{
    font-size: 2.35em;
    font-weight: 700;
    color: #cdd6f4;
    margin-bottom: 10px;
    position: relative;
  }}
  header h1 span {{ color: #7c9ef5; }}
  header p {{
    color: #a6adc8;
    font-size: 1em;
    position: relative;
  }}

  /* ── Kopsavilkuma rinda ── */
  .summary {{
    display: flex;
    justify-content: center;
    gap: 18px;
    flex-wrap: wrap;
    padding: 28px 20px;
    background: #1e1e2e;
    border-bottom: 1px solid #313244;
  }}
  .stat {{
    text-align: center;
    background: #313244;
    padding: 16px 28px;
    border-radius: 14px;
    min-width: 120px;
    border-top: 3px solid #7c9ef5;
  }}
  .stat:nth-child(2) {{ border-top-color: #a6e3a1; }}
  .stat:nth-child(3) {{ border-top-color: #f9e2af; }}
  .stat:nth-child(4) {{ border-top-color: #cba6f7; }}
  .stat .num {{ font-size: 1.85em; font-weight: 700; color: #7c9ef5; }}
  .stat:nth-child(2) .num {{ color: #a6e3a1; }}
  .stat:nth-child(3) .num {{ color: #f9e2af; }}
  .stat:nth-child(4) .num {{ color: #cba6f7; }}
  .stat .lbl {{ color: #a6adc8; font-size: .85em; margin-top: 4px; }}

  /* ── Saturs ── */
  .content {{ max-width: 1100px; margin: 0 auto; padding: 40px 20px 60px; }}

  /* ── Atdalītājs ── */
  .divider {{
    display: flex; align-items: center; gap: 14px;
    margin: 48px 0 38px;
  }}
  .divider::before, .divider::after {{
    content: ''; flex: 1; height: 1px; background: #313244;
  }}
  .divider span {{
    color: #45475a; font-size: .8em;
    letter-spacing: .15em; text-transform: uppercase;
  }}

  /* ── Vizualizācijas karte ── */
  .card {{
    background: #1e1e2e;
    border-radius: 18px;
    border: 1px solid #313244;
    overflow: hidden;
    box-shadow: 0 4px 28px rgba(0,0,0,.32);
    margin-bottom: 0;
  }}
  .card-head {{
    background: #252535;
    padding: 18px 26px;
    border-bottom: 1px solid #313244;
    display: flex;
    align-items: flex-start;
    gap: 14px;
  }}
  .num-badge {{
    flex-shrink: 0;
    width: 34px; height: 34px;
    background: #7c9ef5;
    color: #1e1e2e;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; font-size: .9em;
  }}
  .title-block {{ flex: 1; }}
  .card-title {{ color: #cdd6f4; font-size: 1.2em; font-weight: 600; }}
  .card-meta {{ color: #585b70; font-size: .83em; margin-top: 3px; }}
  .type-chip {{
    flex-shrink: 0;
    background: rgba(124,158,245,.13);
    color: #7c9ef5;
    border: 1px solid rgba(124,158,245,.22);
    padding: 4px 12px;
    border-radius: 20px;
    font-size: .72em;
    font-weight: 600;
    letter-spacing: .04em;
    white-space: nowrap;
    align-self: center;
  }}
  .card-body {{ padding: 22px 26px 26px; }}
  .viz-img {{
    width: 100%;
    border-radius: 10px;
    margin-bottom: 18px;
    display: block;
  }}
  .viz-desc {{
    color: #a6adc8;
    font-size: .9em;
    margin-bottom: 13px;
    font-style: italic;
  }}
  .insight {{
    background: #252535;
    border-left: 3px solid #a6e3a1;
    padding: 13px 17px;
    border-radius: 0 8px 8px 0;
    color: #cdd6f4;
    line-height: 1.72;
    font-size: .92em;
  }}
  .insight strong {{ color: #a6e3a1; }}

  /* ── SQL bloķis ── */
  .sql-wrap {{ margin-top: 13px; }}
  details summary {{
    color: #45475a; font-size: .8em; cursor: pointer;
    padding: 5px 0; letter-spacing: .05em; text-transform: uppercase;
    user-select: none;
  }}
  details summary:hover {{ color: #a6adc8; }}
  pre.sql {{
    margin-top: 7px;
    background: #0f0f1a;
    border: 1px solid #313244;
    border-radius: 8px;
    padding: 12px 15px;
    font-size: .78em;
    color: #7c9ef5;
    overflow-x: auto;
    white-space: pre-wrap;
    word-break: break-word;
  }}

  /* ── Apakškolontituls ── */
  footer {{
    text-align: center;
    padding: 28px 20px;
    color: #45475a;
    border-top: 1px solid #313244;
    font-size: .86em;
  }}
  footer strong {{ color: #585b70; }}
</style>
</head>
<body>

<header>
  <div class="header-chip">FITA ML kurss · 2026</div>
  <h1>Direct Payments — <span>Uzlabotā Atskaite</span></h1>
  <p>5 profesionālas vizualizācijas &nbsp;·&nbsp; Mara Medne &nbsp;·&nbsp; {gen_date}</p>
</header>

<div class="summary">
  <div class="stat"><div class="num">5</div><div class="lbl">Vizualizācijas</div></div>
  <div class="stat"><div class="num">{total_rows}</div><div class="lbl">Datu rindas</div></div>
  <div class="stat"><div class="num">3</div><div class="lbl">DB tabulas</div></div>
  <div class="stat"><div class="num">2018–19</div><div class="lbl">Datu periods</div></div>
</div>

<div class="content">
"""

for i, m in enumerate(viz_meta):
    b64  = charts_b64.get(m["key"], "")
    img  = f'<img class="viz-img" src="data:image/png;base64,{b64}" alt="{m["title"]}">' if b64 else ''
    sep  = f'<div class="divider"><span>vizualizācija {i + 1}</span></div>' if i > 0 else ''
    sql_block = ""
    if m.get("sql"):
        sql_block = f"""
        <div class="sql-wrap">
          <details>
            <summary>&#9654; Skatīt SQL vaicājumu</summary>
            <pre class="sql">{m['sql']}</pre>
          </details>
        </div>"""

    html += f"""
  {sep}
  <div class="card">
    <div class="card-head">
      <div class="num-badge">{i + 1}</div>
      <div class="title-block">
        <div class="card-title">{m['title']}</div>
        <div class="card-meta">&#128202; {m['rows']} datu rindas</div>
      </div>
      <span class="type-chip">{m['badge']}</span>
    </div>
    <div class="card-body">
      {img}
      <p class="viz-desc">{m['desc']}</p>
      <div class="insight"><strong>&#128161; Ieskats:</strong> {m['insight']}</div>
      {sql_block}
    </div>
  </div>
"""

html += f"""
</div>

<footer>
  Ģenerēts ar <strong>Python + Matplotlib</strong> &nbsp;|&nbsp;
  FITA ML kurss 2026 &nbsp;|&nbsp;
  <strong>Mara Medne</strong> &nbsp;|&nbsp;
  {gen_date}
</footer>

</body>
</html>"""

out = os.path.join(script_dir, "advanced_report.html")
with open(out, "w", encoding="utf-8") as f:
    f.write(html)

print(f"\n✅ Uzlabotā HTML atskaite gatava!")
print(f"📁 Atver: week1/advanced_report.html")
