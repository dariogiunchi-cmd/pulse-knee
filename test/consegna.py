# -*- coding: utf-8 -*-
"""
PULSE — collaudo della consegna quotidiana (audio/consegna.py, Addendum 4 §7).
Macchina pura sul dato reale del giorno + regole ferree: niente emoji, stessa
struttura dell'app, un collegamento per voce, anteprima che dice già cosa c'è.
"""
import os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'audio'))
from consegna import costruisci_email

ok = 0; bad = 0
def chk(c, m):
    global ok, bad
    print(('✅ ' if c else '❌ ') + m)
    if c: ok += 1
    else: bad += 1

H = os.environ.get('PULSE_HTML') or os.path.abspath('index.html')
dati = open(H, encoding='utf-8').read()
titolo, corpo = costruisci_email(dati)

chk(titolo.startswith('PULSE ') and len(titolo) <= 250, 'il titolo apre con PULSE e la data')
chk('rilevanti' in corpo.splitlines()[0], "la prima riga dichiara la copertura, non la selezione")
prime3 = '\n'.join(corpo.splitlines()[:3])
chk('rilevanti' in prime3 and ('IN EVIDENZA' in prime3 or len(prime3) > 40),
    "l'anteprima (prime tre righe) dice già cosa c'è oggi")

# niente emoji, da nessuna parte (§7)
emoji = re.findall(r'[\U0001F000-\U0001FAFF☀-➿⬀-⯿]', titolo + corpo)
chk(not emoji, 'nessuna emoji nella consegna' + (f' — trovate: {emoji[:3]}' if emoji else ''))

# stessa struttura dell'app: i domini presenti nel dato compaiono, nell'ordine
if "dom:'" in dati:
    ordine = [s for s in ['MENISCO', 'CARTILAGINE', 'LEGAMENTI', 'PROTESI'] if s + '\n' in corpo + '\n' or ('\n' + s) in corpo]
    posizioni = [corpo.index(s) for s in ordine]
    chk(posizioni == sorted(posizioni), 'i domini compaiono nell\'ordine dichiarato')
    chk(len(ordine) >= 2, f'i domini del giorno sono sezioni della consegna ({ordine})')

# un solo collegamento per voce
for r in corpo.splitlines():
    if r.startswith('- ') and r.count('](') > 1:
        chk(False, f'più di un collegamento su una voce: {r[:60]}')
        break
else:
    chk(True, 'un solo collegamento per voce')

# nessuna parola di sistema (§8.5 vale anche in posta)
banditi = [w for w in ['raccoglitore', 'feed', 'json', 'UTC', 'interrogat', 'verificato dal']
           if w.lower() in corpo.lower()]
chk(not banditi, 'nessuna parola di sistema nella consegna' + (f' — {banditi}' if banditi else ''))

# nessun paragrafo: solo righe (prosa zero, §8.3)
lunghe = [r[:60] for r in corpo.splitlines() if len(r) > 220]
chk(not lunghe, 'nessun paragrafo nella consegna: solo righe' + (f' — {lunghe[:1]}' if lunghe else ''))

# l'episodio e l'app sono raggiungibili, una volta sola
chk(corpo.count('/audio/') == 1 and 'Apri PULSE' in corpo, "l'episodio e l'app chiudono la consegna")

# sintetico: i richiami stanno DOPO le notizie in INDUSTRIA
SINT = """var BUILD_DATE='2026-08-21';
var PICK=1;
var ARTICLES=[
 {n:1,dom:'menisco',riga:"La sutura di prova regge",mono:'x',j:'KSSTA',dot:'green',sec:'res',h:"t",v:"v",meta:"RCT · 100 · [I]",pmid:'41111111',doi:'10.1/a'}];
var EXTRA=[];var SCOPERTE=[];
var CONGRESSI=[{sig:'ESSKA',citta:'Prova',date:'1-2 mag',abstract:'2026-09-30'}];
var INDUSTRIA=[{tipo:'richiamo',fonte:'openFDA',riga:"Richiamo di prova"},{fonte:'MassDevice',riga:"Lancio di prova"}];
"""
t2, c2 = costruisci_email(SINT)
chk(c2.index('Lancio di prova') < c2.index('Richiamo di prova'), 'in INDUSTRIA le notizie prima, i richiami in coda')
chk('ESSKA' in c2 and 'scadenza abstract: 2026-09-30' in c2, 'i congressi sono dati strutturati, non prosa')
chk('La sutura di prova regge' in t2, "il titolo porta l'evidenza del giorno")

print(f"\n===== CONSEGNA: {ok} verificati · {bad} errori =====")
sys.exit(1 if bad else 0)
