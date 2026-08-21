# -*- coding: utf-8 -*-
"""
PULSE — collaudo del testo per l'orecchio (audio/orecchio.py + config/pronuncia.json).

Si collauda la MACCHINA con frasi sintetiche, mai il carico del giorno. Le regole
di verità valgono anche qui: la trasformazione deve cambiare la PRONUNCIA, mai il
CONTENUTO — l'ultimo blocco lo verifica sul briefing reale.
"""
import os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'audio'))
from orecchio import trasforma, carica_dizionario, _estrai_brief

ok = 0; bad = 0
def chk(c, m):
    global ok, bad
    print(('✅ ' if c else '❌ ') + m)
    if c: ok += 1
    else: bad += 1

D = carica_dizionario()

# --- sigle lettera per lettera, all'italiana --------------------------------
chk(trasforma('rottura del LCA', D) == 'rottura del elle ci a',
    'LCA → elle ci a')
chk('elle ci pi' in trasforma('LCP integro', D), 'LCP → elle ci pi')
chk(trasforma('va alla sala', D) == 'va alla sala',
    'ALL non tocca «alla»: solo a parola intera, maiuscole esatte')
chk(trasforma('una CALL con i colleghi', D) == 'una CALL con i colleghi',
    'ALL non tocca nemmeno CALL: il confine di parola vale anche in maiuscolo')
chk(trasforma('la RM di controllo', D) == 'la erre emme di controllo',
    'RM → erre emme')

# --- sigle inglesi che restano inglesi --------------------------------------
chk('ei si el' in trasforma('ACL reconstruction', D), 'ACL → ei si el')
chk('kuus' in trasforma('punteggio KOOS', D), 'KOOS → kuus (parola)')

# --- riviste sciolte per esteso ---------------------------------------------
chk('Knee Surgery, Sports Traumatology, Arthroscopy' in trasforma('su KSSTA quest\'anno', D),
    'KSSTA → titolo per esteso')
chk('American Journal of Sports Medicine' in trasforma('pubblicato su AJSM', D),
    'AJSM → titolo per esteso')

# --- valori statistici -------------------------------------------------------
chk('p minore di zero virgola zero cinque' in trasforma('significativo (p<0.05)', D),
    'p<0.05 → parlato')
chk('intervallo di confidenza al novantacinque per cento' in trasforma('IC 95% 1,2–3,4', D),
    'IC 95% → parlato')
chk('dodici' not in trasforma('slope di 12°', D) and '12 gradi' in trasforma('slope di 12°', D),
    '12° → 12 gradi')
chk('1406' in trasforma('coorte su 1.406 pazienti', D),
    '1.406 → 1406 (il punto delle migliaia non diventa «uno punto quattro»)')
chk('18 per cento' in trasforma('il 18% dei casi', D), '18% → 18 per cento')
chk('contro' in trasforma('80 vs 45', D), 'vs → contro')

# --- parentesi → incisi ------------------------------------------------------
t = trasforma('il prelievo (margine superiore) rischia', D)
chk('(' not in t and 'margine superiore' in t,
    'le parentesi diventano incisi, senza perdere il contenuto')

# --- PRINCIPIO ZERO: sul briefing REALE nessun numero cambia valore ----------
reale = _estrai_brief()
voce = trasforma(reale, D)
def numeri(s):
    # i valori del testo: cifre normalizzate (1.406→1406 è la stessa quantità)
    return sorted(re.findall(r'\d+', s.replace('.', '').replace(',', '')))
chk(numeri(reale) == numeri(voce),
    'briefing reale: le quantità sono le stesse prima e dopo (solo pronuncia)')
chk(len(voce) > 100, f'briefing reale trasformato ({len(voce)} caratteri)')

print(f"\n===== ORECCHIO: {ok} verificati · {bad} errori =====")
sys.exit(1 if bad else 0)
