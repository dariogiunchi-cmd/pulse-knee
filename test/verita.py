#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PULSE — controlli di VERITÀ, non di struttura.

Le altre suite verificano che l'app funzioni. Questa verifica che non affermi
cose false. È la difesa meccanica del PRINCIPIO ZERO: una citazione plausibile
ma inventata è il fallimento peggiore possibile del sistema, perché il Dr.
Giunchi la porterebbe in una perizia.

Nessuno di questi controlli può dimostrare che una citazione sia VERA — per
quello serve riaprire PubMed, e lo fa la sessione del mattino. Questi controlli
trovano le impronte tipiche dell'invenzione e le affermazioni che l'app fa su
sé stessa e che non corrispondono ai suoi stessi dati.
"""
import os, re, sys, json
from datetime import date

H = os.environ.get('PULSE_HTML') or os.path.abspath('index.html')
h = open(H, encoding='utf-8').read()
ko = []
def chk(nome, cond, extra=""):
    print(("✅ " if cond else "❌ ") + nome + ("" if cond or not extra else "  →  " + str(extra)[:200]))
    if not cond: ko.append(nome)

def var(nome, default=None):
    # Fermarsi al primo «;» della STESSA riga: con `.+?` e re.S la lettura scavalcava
    # il commento in coda e restituiva spazzatura, facendo saltare il controllo
    # successivo senza che nulla segnalasse il problema. Un controllo che si
    # disattiva da solo è peggio di un controllo assente.
    m = re.search(r"var %s\s*=\s*([^;\n]+);" % nome, h)
    return m.group(1).strip() if m else default

# ------------------------------------------------------------ i dati del giorno
pmid  = re.findall(r"pmid:'(\d+)'", h)
doi   = re.findall(r"doi:'([^']+)'", h)
narts = len(re.findall(r"\{n:\d+,mono:", h))

chk("ci sono schede", narts > 0, narts)
chk("ogni scheda ha un PMID", len(pmid) == narts, (len(pmid), narts))
chk("ogni scheda ha un DOI", len(doi) == narts, (len(doi), narts))

# ------------------------------------------------------------ PMID plausibili
chk("nessun PMID ripetuto", len(pmid) == len(set(pmid)), [x for x in pmid if pmid.count(x) > 1][:4])
mal = [x for x in pmid if not (7 <= len(x) <= 9)]
chk("i PMID hanno una lunghezza plausibile (7-9 cifre)", not mal, mal)
tondi = [x for x in pmid if x.endswith('0000') or x in ('12345678', '11111111')]
chk("nessun PMID sospettosamente tondo", not tondi, tondi)

# Impronta tipica dell'invenzione: PMID in progressione aritmetica esatta.
# I PMID reali della stessa settimana sono vicini ma MAI in sequenza regolare.
nums = sorted(int(x) for x in pmid)
seq = []
if len(nums) >= 3:
    for i in range(len(nums) - 2):
        d1, d2 = nums[i+1] - nums[i], nums[i+2] - nums[i+1]
        if d1 == d2 and d1 <= 2:
            seq.append((nums[i], nums[i+1], nums[i+2]))
chk("nessuna progressione regolare fra i PMID (impronta dell'invenzione)", not seq, seq[:2])

# ------------------------------------------------------------ DOI plausibili
chk("nessun DOI ripetuto", len(doi) == len(set(doi)), [x for x in doi if doi.count(x) > 1][:4])
maldoi = [x for x in doi if not re.match(r'^10\.\d{4,9}/\S+$', x)]
chk("i DOI hanno la forma corretta (10.xxxx/…)", not maldoi, maldoi[:4])

# ------------------------------------------------------------ ciò che l'app afferma di sé
build = (var('BUILD_DATE') or '').strip("'\"")
chk("BUILD_DATE è una data valida", re.match(r'^\d{4}-\d{2}-\d{2}$', build) is not None, build)

citv = var('CIT_VERIFICATE')
chk("il conteggio delle citazioni verificate esiste", citv is not None)
chk("il conteggio delle citazioni è un numero leggibile",
    citv is not None and citv.isdigit(), citv)
if citv is not None and citv.isdigit():
    chk("non dichiara più citazioni verificate delle schede esistenti",
        int(citv) <= narts, f"dice {citv} verificate su {narts} schede")

# L'intestazione conteneva «15» lavori mentre erano 11 — residuo di un errore corretto
# nello storico ma mai nell'app, rimasto visibile all'utente per venti pubblicazioni.
_visibile = re.sub(r'<script>[\s\S]*?</script>', '', h)
chk("l'intestazione non contiene numeri scritti a mano",
    not re.search(r'class="kpi[^"]*"><b>\d+</b>', _visibile) and 'id="kpis"' in h,
    "i conteggi in cima vanno contati, non scritti")
chk("la data non è scritta a mano",
    not re.search(r'class="date"[^>]*>\s*\w+\s+\d+\s+\w+\s+\d{4}', _visibile),
    "la data va derivata da BUILD_DATE")

chk("il piè di pagina non contiene conteggi scritti a mano",
    not re.search(r'verificate\s+\d+\s*/\s*\d+', re.sub(r'<script>[\s\S]*?</script>', '', h)),
    "il totale va contato, non scritto")

# Il controllo delle ritrattazioni deve essere RIFATTO ogni giorno: se la data
# resta indietro, l'app rassicura l'utente con un controllo che non ha fatto.
lrc = (var('LAST_RETRACTION_CHECK') or '').strip("'\"")
MESI = ['gennaio','febbraio','marzo','aprile','maggio','giugno','luglio',
        'agosto','settembre','ottobre','novembre','dicembre']
atteso = ''
if re.match(r'^\d{4}-\d{2}-\d{2}$', build):
    a, m, g = build.split('-')
    atteso = f"{int(g)} {MESI[int(m)-1]} {a}"
chk("il controllo delle ritrattazioni è di oggi, non di ieri",
    lrc == atteso, f"dice «{lrc}», dovrebbe dire «{atteso}»")

# ------------------------------------------------------------ coerenza interna
for nome, chiave in [('CONF', 'livello di evidenza'), ('MUTE', 'studi muti'),
                     ('NLB', 'testi per la distribuzione'), ('SOCV', 'contenuti social')]:
    m = re.search(r"var %s\s*=\s*(\{[\s\S]*?\});\s*\n" % nome, h)
    if not m: continue
    try:
        chiavi = re.findall(r'[\{,]\s*"?(\d+)"?\s*:', m.group(1))
    except Exception:
        continue
    numeri = set(re.findall(r"\{n:(\d+),mono:", h))
    orfani = sorted(set(chiavi) - numeri)
    chk(f"«{chiave}» non punta a schede inesistenti", not orfani, orfani[:5])

for nome in ['LINKS', 'DUELS']:
    m = re.search(r"var %s\s*=\s*([\[{][\s\S]*?)\;\s*\n" % nome, h)
    if not m: continue
    rif = set(re.findall(r'[ab]:(\d+)|\{n:(\d+),rel', m.group(1)))
    rif = {x or y for x, y in rif} if rif and isinstance(next(iter(rif)), tuple) else rif
    numeri = set(re.findall(r"\{n:(\d+),mono:", h))
    orf = sorted({r for r in rif if r} - numeri)
    chk(f"«{nome}» non punta a schede inesistenti", not orf, orf[:5])

print()
if ko:
    print(f"❌ CONTROLLI DI VERITÀ FALLITI — {len(ko)}: {ko}")
    sys.exit(1)
print(f"✅ CONTROLLI DI VERITÀ SUPERATI — {narts} schede, {len(set(pmid))} PMID distinti")
