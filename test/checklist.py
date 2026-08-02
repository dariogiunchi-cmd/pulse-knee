#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PULSE — controllo strutturale prima della pubblicazione.
Verifica che nessuna funzione sia stata persa nella ricostruzione quotidiana,
che il JavaScript sia sintatticamente valido e che nulla di segreto finisca
in un repository pubblico.

Uso:  PULSE_HTML=/percorso/index.html python3 checklist.py
Esce con codice 1 se anche un solo controllo fallisce.
"""
import os, re, sys, subprocess, json, tempfile

H = os.environ.get('PULSE_HTML') or os.path.abspath('index.html')
D = os.path.dirname(H) or '.'
h = open(H, encoding='utf-8').read()

ko = []
def chk(nome, cond, extra=""):
    print(("✅ " if cond else "❌ ") + nome + ("" if cond or not extra else "  →  " + str(extra)[:200]))
    if not cond:
        ko.append(nome)

# ---------------------------------------------------------------- file richiesti
RICHIESTI = ['index.html', 'manifest.json', 'sw.js', '.nojekyll',
             'apple-touch-icon.png', 'icon-192.png', 'icon-512.png',
             'icon-maskable-512.png']
# pulse_brief.mp3 è stato tolto il 2 agosto 2026: 673 KB mai richiesti da nessuna
# pagina (la voce è quella del dispositivo, via speechSynthesis). Se un giorno
# torna un file audio davvero collegato, va rimesso in questo elenco.
mancanti = [f for f in RICHIESTI if not os.path.exists(os.path.join(D, f))]
chk("tutti i file del sito sono presenti", not mancanti, mancanti)

# ---------------------------------------------------------------- funzioni vive
MARCATORI = [
 ("Mancato aggiornamento",        ["function renderFresh", "BUILD_DATE="]),
 ("Allerta ritrattazioni",        ["function renderRetr", "RETRACTED"]),
 ("Tensioni «Cosa non torna»",    ["var TENSIONS=", "function renderTens"]),
 ("Studi muti (sottopotenza)",    ["var MUTE=", "function muteHTML"]),
 ("Collegamenti nel tempo",       ["function linksHTML"]),
 ("Ricerca nell'archivio",        ["function searchHist"]),
 ("Vista duello",                 ["function openDuel", "DUELS"]),
 ("Tempo di lettura",             ["function readMin"]),
 ("Autocritica settimanale",      ["function renderAudit"]),
 ("Barre di confidenza",          ["function confHTML", "confHTML(a.n)"]),
 ("Verdetto del giorno",          ["function renderVerdict", 'class="vitem"']),
 ("Filtri rapidi",                ["function setFilter"]),
 ("Scorri per salvare",           ["_sItem"]),
 ("Ricerca nei salvati",          ["function renderSaved"]),
 ("Condividi",                    ["function shareArt"]),
 ("Lettura vocale",               ["function speakBrief", "function speakCard"]),
 ("Contenuti social",             ["function openSocial", "SOCV", "TAGS"]),
 ("Adatta funzionante",           ["function toggleEdit", "edits:{}"]),
 ("Email della newsletter",       ["var NLB=", "function nlText"]),
 ("Post per il blog Wix",         ["function blogText", "function slugify"]),
 ("Post per Google Business",     ["function gbpText", "GBP_MAX"]),
 ("Scelta della destinazione",    ["function setDest", "function outText"]),
 ("Memoria dei lavori scelti",    ["function wIdx", "function wArt", "weekly:["]),
 ("Salvati che sopravvivono",     ["function savedList", "function isSaved", "savedItems:[]"]),
 ("Duelli non fantasma",          ["function duelliVivi"]),
 ("Versione mista dei testi",     ["setNlVer('mix'", "function wBlurb"]),
 ("Durata video in secondi",      ["function setSec", "function durataNota", "PAROLE_AL_SECONDO"]),
 ("Pulsante Video sulle schede",  ["ib vid"]),
 ("Memoria dell'utente",          ["localStorage.getItem('pulse4')"]),
 ("App installabile",             ['rel="manifest"', "apple-touch-icon", "serviceWorker"]),
]
for nome, ms in MARCATORI:
    persi = [m for m in ms if m not in h]
    chk(nome, not persi, "marcatori persi: " + ", ".join(persi) if persi else "")

# ---------------------------------------------------------------- sintassi
m = re.search(r'<script>([\s\S]*)</script>', h)
chk("il blocco <script> esiste", m is not None)
if m:
    with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False, encoding='utf-8') as f:
        f.write(m.group(1)); tmp = f.name
    r = subprocess.run(['node', '--check', tmp], capture_output=True, text=True)
    chk("il JavaScript non ha errori di sintassi", r.returncode == 0, r.stderr.strip()[:200])
    os.unlink(tmp)

# ---------------------------------------------------------------- trappole note
resid = re.findall(r'\\U0001[0-9a-fA-F]{4}', h)
chk("nessun escape \\U rimasto letterale", not resid, resid[:4])

chk("nessun segnaposto «nel deploy funzionerà»", "nel deploy funzioner" not in h)

chk("etichette di accessibilità (≥6)", h.count('aria-label') >= 6, h.count('aria-label'))

chk("la chiave della memoria è ancora 'pulse4'", "localStorage.getItem('pulse4')" in h)

# ---------------------------------------------------------------- nessun segreto
SEGRETI = [r'ghp_[A-Za-z0-9]{20,}', r'github_pat_[A-Za-z0-9_]{20,}',
           r'gho_[A-Za-z0-9]{20,}', r'xoxb-[A-Za-z0-9-]{20,}',
           r'sk-[A-Za-z0-9]{32,}', r'AIza[A-Za-z0-9_-]{30,}']
trovati = []
for f in os.listdir(D):
    p = os.path.join(D, f)
    if not os.path.isfile(p) or f.endswith(('.png', '.mp3', '.jpg')):
        continue
    try:
        t = open(p, encoding='utf-8', errors='ignore').read()
    except Exception:
        continue
    for pat in SEGRETI:
        if re.search(pat, t):
            trovati.append(f)
            break
sub = os.path.join(D, 'cervello')
if os.path.isdir(sub):
    for f in os.listdir(sub):
        t = open(os.path.join(sub, f), encoding='utf-8', errors='ignore').read()
        if any(re.search(pat, t) for pat in SEGRETI):
            trovati.append('cervello/' + f)
chk("NESSUNA CREDENZIALE nei file da pubblicare", not trovati, trovati)

# ---------------------------------------------------------------- peso
kb = len(h.encode()) / 1024
import gzip
gz = len(gzip.compress(h.encode(), 9)) / 1024
chk("l'app resta sotto i 120 KB compressi", gz < 120, f"{gz:.0f} KB compressi")
print(f"   ℹ️  index.html: {kb:.0f} KB grezzi · {gz:.0f} KB come lo scarica l'iPhone")

print()
if ko:
    print(f"❌ CONTROLLO STRUTTURALE FALLITO — {len(ko)} problemi: {ko}")
    sys.exit(1)
print("✅ CONTROLLO STRUTTURALE SUPERATO")
