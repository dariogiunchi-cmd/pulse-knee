#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PULSE — costruzione dell'app: modello + dati del giorno → index.html.

PERCHÉ ESISTE. Fino al 17 agosto 2026 il briefing del mattino riscriveva le sue
variabili DENTRO index.html: 180 KB in cui convivono codice e contenuti. Il cancello
vede i contenuti sbagliati, ma un errore di sostituzione che corrompe il CODICE può
sfuggirgli. Da oggi il codice vive in `modello.html` (che il briefing non tocca mai)
e i contenuti in `dati/giorno.js`; index.html è il prodotto della loro unione.

Uso:
  python3 test/costruisci.py               costruisce index.html da modello + dati
  python3 test/costruisci.py --verifica    controlla che index.html coincida col
                                           prodotto di modello + dati (esce 1 se no)
  python3 test/costruisci.py --estrai      il percorso inverso: da un index.html
                                           (es. un'istantanea ripristinata) rigenera
                                           dati/giorno.js, lasciando il modello com'è

Il segnaposto nel modello è la riga `/*__DATI_DEL_GIORNO__*/`.
"""
import os, re, sys, tempfile

QUI = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(QUI)
MODELLO = os.path.join(APP, 'modello.html')
DATI = os.path.join(APP, 'dati', 'giorno.js')
INDEX = os.path.join(APP, 'index.html')
MARCA = '/*__DATI_DEL_GIORNO__*/'

# Le variabili che il briefing riscrive ogni mattina, nell'ordine in cui stavano
# in index.html. Tutto il resto è codice, e sta nel modello.
QUOTIDIANE = ['SELEZIONE', 'EXTRA', 'SCOPERTE',
              'SOC', 'SOCV', 'TAGS', 'NLB', 'ARTICLES', 'SUGGQ', 'BRIEF_TEXT',
              'BRIEF_DIALOGO',
              'CONF', 'BUILD_DATE', 'PICK', 'INDUSTRIA', 'CONGRESSI', 'SOCIETA',
              'NONVERIF', 'CIT_VERIFICATE', 'LAST_RETRACTION_CHECK', 'RETRACTED',
              'LINKS', 'DUELS', 'HISTORY', 'AUDIT', 'TENSIONS', 'MUTE']

# Variabili che possono legittimamente MANCARE (l'app le tratta con typeof):
# un'istantanea più vecchia della variabile deve restare ripristinabile.
FACOLTATIVE = {'BRIEF_DIALOGO', 'SELEZIONE'}


def _decl(nome, testo):
    """La dichiarazione completa `var NOME=...;` con l'eventuale commento in coda.
    Il valore termina col primo `;` a FINE riga (i valori non hanno righe che
    finiscono in `;` al loro interno)."""
    pat = re.compile(r'var %s=(?s:.*?);(?:[ \t]*(?://[^\n]*|/\*[^\n]*\*/))?[ \t]*\n' % nome)
    m = pat.search(testo)
    if not m:
        raise SystemExit(f"❌ dichiarazione non trovata: var {nome}")
    return m


def costruisci(scrivi=True):
    modello = open(MODELLO, encoding='utf-8').read()
    dati = open(DATI, encoding='utf-8').read()
    if modello.count(MARCA) != 1:
        raise SystemExit(f"❌ il modello deve contenere il segnaposto {MARCA} una volta sola")
    # controllo di sanità sui dati: tutte le variabili quotidiane, una volta ciascuna
    for v in QUOTIDIANE:
        n = len(re.findall(r'\bvar %s=' % v, dati))
        if n != 1 and not (n == 0 and v in FACOLTATIVE):
            raise SystemExit(f"❌ dati/giorno.js: 'var {v}=' compare {n} volte (attesa: 1)")
    if MARCA in dati:
        raise SystemExit("❌ dati/giorno.js contiene il segnaposto: file scambiati?")
    esito = modello.replace(MARCA, dati.rstrip('\n'))
    if scrivi:
        open(INDEX, 'w', encoding='utf-8').write(esito)
    return esito


def verifica():
    atteso = costruisci(scrivi=False)
    reale = open(INDEX, encoding='utf-8').read()
    if atteso == reale:
        print("✅ index.html coincide byte per byte con modello.html + dati/giorno.js")
        return 0
    print("❌ index.html NON coincide con modello + dati.")
    print("   Se hai modificato dati/giorno.js:  python3 test/costruisci.py")
    print("   Se hai modificato index.html a mano (o ripristinato un'istantanea):")
    print("     python3 test/costruisci.py --estrai   (riallinea i dati all'index)")
    print("   Il briefing del mattino NON deve toccare index.html direttamente.")
    return 1


def estrai():
    """Da index.html ricava dati/giorno.js e il modello. È il percorso inverso,
    per il ripristino di un'istantanea o la prima migrazione."""
    testo = open(INDEX, encoding='utf-8').read()
    blocchi = []
    primo = True
    for v in QUOTIDIANE:
        if v in FACOLTATIVE and not re.search(r'\bvar %s=' % v, testo):
            print(f"⚠️ var {v} assente (istantanea precedente alla variabile): si salta")
            continue
        m = _decl(v, testo)
        blocchi.append(testo[m.start():m.end()])
        testo = testo[:m.start()] + ('\x00' if primo else '') + testo[m.end():]
        primo = False
    testo = testo.replace('\x00', MARCA + '\n')
    os.makedirs(os.path.dirname(DATI), exist_ok=True)
    intestazione = ("/* PULSE — dati del giorno. QUESTO è il file che il briefing riscrive\n"
                    "   ogni mattina; index.html si rigenera con `python3 test/costruisci.py`.\n"
                    "   Il codice dell'app sta in modello.html e non va toccato. */\n")
    open(DATI, 'w', encoding='utf-8').write(intestazione + ''.join(blocchi))
    open(MODELLO, 'w', encoding='utf-8').write(testo)
    print(f"🧩 estratti {len(QUOTIDIANE)} blocchi → dati/giorno.js ({os.path.getsize(DATI)//1024} KB)"
          f" · modello.html ({os.path.getsize(MODELLO)//1024} KB)")
    return 0


if __name__ == '__main__':
    modo = sys.argv[1] if len(sys.argv) > 1 else ''
    if modo == '--verifica':
        # Se la verifica gira su un file ESTERNO (istantanea scaricata, clone di
        # controllo), la coerenza modello↔dati del repository non c'entra: si salta.
        ph = os.environ.get('PULSE_HTML')
        if ph and os.path.abspath(ph) != INDEX:
            print("⏭️  coerenza modello-dati — saltata: si sta verificando un file esterno.")
            sys.exit(0)
        if not (os.path.exists(MODELLO) and os.path.exists(DATI)):
            print("⏭️  coerenza modello-dati — saltata: modello o dati assenti.")
            sys.exit(0)
        sys.exit(verifica())
    elif modo == '--estrai':
        sys.exit(estrai())
    else:
        costruisci()
        print("🛠  index.html rigenerato da modello.html + dati/giorno.js")
