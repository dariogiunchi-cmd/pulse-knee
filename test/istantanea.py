#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PULSE — istantanee datate.

Ogni pubblicazione lascia una copia dell'app con la data del giorno, così è
sempre possibile riaprire un PULSE del passato o tornarci in un comando.

Ritenzione: tutti i giorni degli ultimi 30, più il primo di ogni mese per
sempre. Il resto viene tolto perché il repository non cresca senza limite.

Uso:  python3 istantanea.py <cartella_repo> <file_index.html> <data AAAA-MM-GG>
"""
import os, sys, json, shutil, html
from datetime import date, timedelta

if len(sys.argv) < 4:
    print("uso: istantanea.py <repo> <index.html> <AAAA-MM-GG>"); sys.exit(2)
REPO, SRC, OGGI = sys.argv[1], sys.argv[2], sys.argv[3]
try:
    d_oggi = date.fromisoformat(OGGI)
except ValueError:
    print("❌ data non valida:", OGGI); sys.exit(2)

VER = os.path.join(REPO, 'versioni')
os.makedirs(VER, exist_ok=True)

# --- 1. salva la copia del giorno -------------------------------------------
dest = os.path.join(VER, OGGI + '.html')
shutil.copy2(SRC, dest)
print(f"📸 istantanea salvata: versioni/{OGGI}.html ({os.path.getsize(dest)//1024} KB)")

# --- 2. ritenzione ----------------------------------------------------------
tenute, tolte = [], []
for f in sorted(os.listdir(VER)):
    if not f.endswith('.html') or f == 'index.html':
        continue
    try:
        d = date.fromisoformat(f[:-5])
    except ValueError:
        continue
    recente = (d_oggi - d) <= timedelta(days=30)
    primo_del_mese = (d.day == 1)
    if recente or primo_del_mese or d == d_oggi:
        tenute.append(d)
    else:
        os.remove(os.path.join(VER, f))
        tolte.append(f)
tenute.sort(reverse=True)
if tolte:
    print(f"🧹 tolte {len(tolte)} istantanee oltre i 30 giorni (i primi del mese restano): {', '.join(tolte[:5])}")

# --- 3. elenco leggibile dalla macchina -------------------------------------
elenco = [{"data": d.isoformat(),
           "file": f"versioni/{d.isoformat()}.html",
           "byte": os.path.getsize(os.path.join(VER, d.isoformat() + '.html'))}
          for d in tenute]
with open(os.path.join(VER, 'elenco.json'), 'w', encoding='utf-8') as f:
    json.dump({"aggiornato": OGGI, "versioni": elenco}, f, ensure_ascii=False, indent=1)

# --- 4. pagina sfogliabile dal telefono -------------------------------------
MESI = ['gennaio','febbraio','marzo','aprile','maggio','giugno','luglio',
        'agosto','settembre','ottobre','novembre','dicembre']
righe = []
for d in tenute:
    et = f"{d.day} {MESI[d.month-1]} {d.year}"
    tag = ' <span class="t">oggi</span>' if d == d_oggi else (
          ' <span class="t m">primo del mese</span>' if d.day == 1 and (d_oggi-d) > timedelta(days=30) else '')
    kb = os.path.getsize(os.path.join(VER, d.isoformat()+'.html')) // 1024
    righe.append(f'<a href="./{d.isoformat()}.html"><b>{html.escape(et)}</b>{tag}<span class="k">{kb} KB</span></a>')

pagina = """<!doctype html><html lang="it"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="robots" content="noindex">
<title>PULSE — versioni precedenti</title><style>
*{box-sizing:border-box}
body{margin:0;padding:22px 16px calc(30px + env(safe-area-inset-bottom));font:15px/1.5 -apple-system,BlinkMacSystemFont,"SF Pro Text",system-ui,sans-serif;background:#f5f5f7;color:#1d1d1f;-webkit-text-size-adjust:100%}
.w{max-width:520px;margin:0 auto}
h1{font-size:22px;letter-spacing:-.02em;margin:0 0 4px}
p{color:#6e6e73;font-size:13px;margin:0 0 18px;line-height:1.5}
a{display:flex;align-items:center;gap:9px;text-decoration:none;color:inherit;background:#fff;border-radius:12px;padding:14px 15px;margin-bottom:8px;box-shadow:0 1px 2px rgba(0,0,0,.05),0 4px 14px rgba(0,0,0,.04);min-height:44px}
a b{font-weight:600;font-size:14.5px}
.k{margin-left:auto;color:#8e8e93;font-size:11.5px}
.t{background:#34c759;color:#fff;font-size:10px;font-weight:700;padding:2px 7px;border-radius:20px;text-transform:uppercase;letter-spacing:.03em}
.t.m{background:#8e8e93}
.b{display:inline-block;margin-bottom:16px;color:#0071e3;font-weight:600;font-size:13.5px;text-decoration:none;background:none;box-shadow:none;padding:0;min-height:0}
@media(prefers-color-scheme:dark){body{background:#000;color:#f5f5f7}a{background:#1c1c1e;box-shadow:0 1px 2px rgba(0,0,0,.4)}p{color:#a1a1a6}}
</style></head><body><div class="w">
<a class="b" href="../">‹ torna al PULSE di oggi</a>
<h1>Versioni precedenti</h1>
<p>Ogni giorno il PULSE viene salvato così com&rsquo;era. Restano tutti i giorni degli ultimi trenta e il primo di ogni mese, per sempre. Toccane una per riaprirla.</p>
__RIGHE__
</div></body></html>"""
pagina = pagina.replace('__RIGHE__', '\n'.join(righe) if righe else '<p>Nessuna istantanea ancora.</p>')
with open(os.path.join(VER, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(pagina)

print(f"📚 {len(tenute)} versioni disponibili · elenco: versioni/index.html")
