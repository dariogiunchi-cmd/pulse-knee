#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PULSE — il testo per l'orecchio non è il testo per l'occhio.

Trasforma il briefing del giorno (BRIEF_TEXT in dati/giorno.js) nel testo che la
voce deve DIRE, applicando config/pronuncia.json:

  1. regole_regex   — valori statistici e notazioni (p<0,05 · IC 95% · 12° · 1.406)
  2. sigle          — lettera_per_lettera, inglesi, parole (a parola intera,
                      maiuscole esatte: ALL non tocca «alla», RM non tocca «Roma»)
  3. riviste        — sciolte per esteso
  4. pulizia        — parentesi in incisi fra virgole, spazi doppi

PRINCIPIO ZERO: la trasformazione è di sola pronuncia. Non aggiunge, non toglie e
non riformula alcuna affermazione: i collaudi (test/orecchio.py) verificano che il
contenuto informativo resti identico.

Uso:
  python3 audio/orecchio.py                # dati/giorno.js → audio/briefing-orecchio.txt
  python3 audio/orecchio.py --stdin        # trasforma il testo da stdin (per i collaudi)
"""
import json, os, re, sys

QUI = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(QUI)
DIZ = os.path.join(APP, 'config', 'pronuncia.json')
DATI = os.path.join(APP, 'dati', 'giorno.js')
USCITA = os.path.join(QUI, 'briefing-orecchio.txt')


def carica_dizionario(percorso=DIZ):
    d = json.load(open(percorso, encoding='utf-8'))
    for sez in d.values():
        if isinstance(sez, dict):
            sez.pop('_nota', None)
    return d


def _sigla_re(sigla):
    """A parola intera e con le maiuscole esatte: \bALL\b ma mai dentro «alla»."""
    return re.compile(r'(?<![\w&])' + re.escape(sigla) + r'(?![\w&])')


def trasforma(testo, diz=None):
    d = diz or carica_dizionario()
    t = testo

    # 1. valori statistici e notazioni, nell'ordine del file
    for pat, ripo in d.get('regole_regex', {}).items():
        if pat.startswith('_'):
            continue
        t = re.sub(pat, ripo, t)

    # 2. sigle: prima le più lunghe, così SIGASCOT non viene mangiata da TC
    sigle = {}
    for sez in ('lettera_per_lettera', 'inglesi', 'parole'):
        for k, v in d.get(sez, {}).items():
            if not k.startswith('_'):
                sigle[k] = v
    for k in sorted(sigle, key=len, reverse=True):
        t = _sigla_re(k).sub(sigle[k], t)

    # 3. riviste per esteso
    riv = {k: v for k, v in d.get('riviste', {}).items() if not k.startswith('_')}
    for k in sorted(riv, key=len, reverse=True):
        t = _sigla_re(k).sub(riv[k], t)

    # 4. parentesi → incisi fra virgole; niente doppie virgole né spazi doppi
    t = re.sub(r'\s*\(([^)]{1,120})\)', r', \1,', t)
    t = re.sub(r',\s*,', ',', t)
    t = re.sub(r',\s*([.;!?])', r'\1', t)
    t = re.sub(r'[ \t]{2,}', ' ', t)
    return t.strip()


def _estrai_brief(percorso=DATI):
    js = open(percorso, encoding='utf-8').read()
    m = re.search(r'var BRIEF_TEXT=("(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\');', js)
    if not m:
        raise SystemExit('❌ BRIEF_TEXT non trovato in dati/giorno.js')
    grezzo = m.group(1)[1:-1]
    grezzo = grezzo.replace('\\n', '\n').replace("\\'", "'").replace('\\"', '"')
    return re.sub(r'\\u([0-9a-fA-F]{4})', lambda x: chr(int(x.group(1), 16)), grezzo)


if __name__ == '__main__':
    if '--stdin' in sys.argv:
        print(trasforma(sys.stdin.read()))
    else:
        voce = trasforma(_estrai_brief())
        open(USCITA, 'w', encoding='utf-8').write(voce + '\n')
        print(f"🎧 {USCITA} — {len(voce)} caratteri per l'orecchio")
