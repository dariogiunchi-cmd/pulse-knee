#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PULSE — backup del cervello.

I documenti del Progetto vengono scritti in una cartella; questo script li
ripulisce da ogni credenziale e genera l'indice con le impronte.

Il repository è PUBBLICO: la ripulitura non è un accessorio, è la condizione
per poter mettere lì dentro il cervello.

Uso:  python3 cervello.py <cartella_cervello>
Esce con 1 se una credenziale sopravvive alla ripulitura.
"""
import os, re, sys, hashlib
from datetime import date

DEST = sys.argv[1] if len(sys.argv) > 1 else 'cervello'
if not os.path.isdir(DEST):
    print("❌ cartella inesistente:", DEST); sys.exit(2)

# Elenco volutamente largo: meglio oscurare qualcosa di innocuo che pubblicare una chiave.
SEGRETI = [
    (r'ghp_[A-Za-z0-9]{16,}',         'ghp_***TOKEN-RIMOSSO***'),
    (r'github_pat_[A-Za-z0-9_]{16,}', 'github_pat_***TOKEN-RIMOSSO***'),
    (r'gho_[A-Za-z0-9]{16,}',         'gho_***TOKEN-RIMOSSO***'),
    (r'xox[baprs]-[A-Za-z0-9-]{16,}', 'xox-***TOKEN-RIMOSSO***'),
    (r'sk-[A-Za-z0-9]{24,}',          'sk-***CHIAVE-RIMOSSA***'),
    (r'AIza[A-Za-z0-9_\-]{28,}',      'AIza***CHIAVE-RIMOSSA***'),
    (r'xkeysib-[A-Za-z0-9]{16,}',     'xkeysib-***CHIAVE-RIMOSSA***'),
]

OGGI = date.today().isoformat()
schede, oscurati = [], 0

for nome in sorted(os.listdir(DEST)):
    if not nome.endswith('.md') or nome == 'LEGGIMI.md':
        continue
    p = os.path.join(DEST, nome)
    t = open(p, encoding='utf-8').read()
    n = 0
    for pat, sost in SEGRETI:
        t, k = re.subn(pat, sost, t); n += k
    if n:
        open(p, 'w', encoding='utf-8').write(t)
        oscurati += n
    schede.append((nome, len(t.encode()), hashlib.sha256(t.encode()).hexdigest()[:12], n))

# --- controllo finale: nessuna credenziale può essere sopravvissuta -------------
rimaste = []
for nome, *_ in schede:
    t = open(os.path.join(DEST, nome), encoding='utf-8').read()
    if any(re.search(pat, t) for pat, _ in SEGRETI):
        rimaste.append(nome)
if rimaste:
    print("❌ CREDENZIALE SOPRAVVISSUTA in:", rimaste); sys.exit(1)

# --- indice --------------------------------------------------------------------
righe = "\n".join(
    f"| `{n}` | {b/1024:.1f} KB | `{h}` |" + ("" if not k else f" ⟵ {k} oscurate")
    for n, b, h, k in schede)
tot = sum(b for _, b, _, _ in schede)

open(os.path.join(DEST, 'LEGGIMI.md'), 'w', encoding='utf-8').write(f"""# PULSE — il cervello

*Indice rigenerato il {OGGI}.*

Questi file sono la **memoria** del sistema: chi è il Dr. Giunchi, che cosa opera, quali
lavori sono già stati visti, quali tensioni restano aperte, come si scrivono le schede e
i contenuti, quali regole di qualità sono vincolanti, come si pubblica e come si distribuisce.

**Dal 17 agosto 2026 l'ORIGINALE è questa cartella.** Deciso dal Dr. Giunchi quando il
lavoro si è spostato su Claude Code: qui ogni modifica ha una storia, un diff e un autore;
nel Progetto claude.ai non ha niente di tutto questo. Il Progetto ne conserva una copia
per le conversazioni; se le due versioni divergono, **vince il repository**. Prima era il
contrario — i documenti fino al 12 agosto vanno letti sapendolo.

## Le credenziali non sono qui

Il repository è pubblico. Prima di ogni scrittura, token e chiavi vengono sostituiti con
`***TOKEN-RIMOSSO***`, e la pubblicazione si ferma se una credenziale sopravvive al
controllo. In questo aggiornamento: **{oscurati} sostituzioni**.
La pubblicazione ordinaria non richiede più alcun token: la sessione Claude Code spinge
dal proprio accesso autorizzato. Il token GitHub resta nel Progetto come via di riserva.

## Documenti ({len(schede)}, {tot/1024:.0f} KB in tutto)

| File | Peso | Impronta |
|---|---|---|
{righe}

L'impronta è il SHA-256 abbreviato: due copie con la stessa impronta sono identiche
carattere per carattere. I nomi con `claude__` corrispondono a `claude/` nel Progetto.

## Come si ricostruisce tutto, se un giorno servisse

1. Il repository È la ricostruzione: clonarlo basta. `CLAUDE.md` orienta la sessione,
   questa cartella contiene la memoria, `test/` il cancello.
2. Per rifare anche il Progetto claude.ai: incollare `00-istruzioni-del-progetto.md`
   come istruzioni permanenti e caricare gli altri file, riportando `claude__` a `claude/`.
3. L'attività quotidiana delle 5.00 UTC si ricrea con il testo in `claude__13-attivita.md`.
4. `bash test/verifica.sh` deve dare verde **prima** di qualunque pubblicazione.

## Che cosa non è ricostruibile da qui

Le scelte fatte dentro l'app — articoli salvati, voti, lavori scelti per la
distribuzione, testi social adattati — vivono nel browser del suo iPhone, sotto la chiave
`pulse4`. Non sono su nessun server: se cancella i dati del sito, quelle si perdono.
Tutto il resto è qui.
""")

print(f"🧠 cervello: {len(schede)} documenti, {tot/1024:.0f} KB · {oscurati} credenziali oscurate")
for n, b, h, k in schede:
    print(f"   {n:44} {b/1024:6.1f} KB  {h}" + ("  🔒" if k else ""))
