#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PULSE — la consegna quotidiana (Addendum 4 §7): il testo dell'email/issue.

Stessa struttura della schermata «Oggi», stesso ordine di domini, stessa
grammatica a una riga. Niente emoji, niente riquadri: composizione tipografica
sobria. L'intestazione dichiara la copertura, non la selezione. Leggibile per
intero senza aprire nulla; un solo collegamento per voce. Le prime tre righe
(anteprima iPhone) dicono già cosa c'è.

costruisci_email(dati_js) è PURA (testo di dati/giorno.js → titolo, corpo):
test/consegna.py la collauda nel cancello.
"""
import json, re

DOMINI = [('menisco', 'MENISCO'), ('cartilagine', 'CARTILAGINE'), ('legamenti', 'LEGAMENTI'),
          ('artroscopia', 'ALTRA ARTROSCOPIA E PROCEDURE AFFINI'), ('osteotomie', 'OSTEOTOMIE'),
          ('protesi', 'PROTESI'), ('trauma', 'TRAUMATOLOGIA DEL GINOCCHIO'),
          ('riab', 'RIABILITAZIONE E RETURN TO SPORT'), ('lineeguida', 'LINEE GUIDA E CONSENSUS')]
MESI = ['gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno', 'luglio',
        'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre']


def _campo(voce, nome):
    m = re.search(nome + r''':\s*(?:"((?:[^"\\]|\\.)*)"|'((?:[^'\\]|\\.)*)')''', voce)
    if not m:
        return ''
    return (m.group(1) if m.group(1) is not None else m.group(2)).replace('\\"', '"').replace("\\'", "'")


def _voci_blocco(blocco):
    """Spezza un array JS di oggetti nelle sue voci (al primo livello)."""
    return re.findall(r'\{[^{}]*\}', blocco)


def _solid(meta):
    return ' · '.join(p.strip() for p in meta.split('·') if p.strip() and not p.strip().startswith('['))[:80]


def costruisci_email(dati):
    build = re.search(r"var BUILD_DATE='(\d{4}-\d{2}-\d{2})'", dati).group(1)
    a, me, g = build.split('-')
    data_it = f"{int(g)} {MESI[int(me)-1]}"

    m_art = re.search(r'var ARTICLES=(\[.*?\]);\n', dati, re.S)
    m_ex = re.search(r'var EXTRA=(\[.*?\]);', dati, re.S)
    m_sc = re.search(r'var SCOPERTE=(\[.*?\]);', dati, re.S)
    m_pk = re.search(r'var PICK=(\d+);', dati)
    m_au = re.search(r'visti:(\d+)', dati)
    pick = int(m_pk.group(1)) if m_pk else None

    voci = []
    for v in _voci_blocco(m_art.group(1)) if m_art else []:
        n = re.search(r'\{n:(\d+),', v)
        if not n:
            continue
        voci.append({'n': int(n.group(1)), 'dom': _campo(v, 'dom'),
                     'riga': _campo(v, 'riga') or _campo(v, 'h'),
                     'solid': _solid(_campo(v, 'meta')), 'j': _campo(v, 'j'),
                     'pmid': _campo(v, 'pmid')})
    for v in (_voci_blocco(m_ex.group(1)) if m_ex else []):
        voci.append({'n': None, 'dom': _campo(v, 'dom'), 'riga': _campo(v, 'h'),
                     'solid': '', 'j': _campo(v, 'j'), 'pmid': _campo(v, 'pmid')})
    for v in (_voci_blocco(m_sc.group(1)) if m_sc else []):
        voci.append({'n': None, 'dom': _campo(v, 'dom'), 'riga': _campo(v, 't'),
                     'solid': '', 'j': '', 'pmid': _campo(v, 'pmid')})

    evid = next((v for v in voci if v['n'] == pick), None)
    visti = m_au.group(1) if m_au else ''
    misura = (f"{visti} lavori esaminati · " if visti else '') + f"{len(voci)} rilevanti"

    def rl(v):
        fonte = ' · '.join(x for x in (v['solid'], v['j']) if x)
        link = f" — [PubMed](https://pubmed.ncbi.nlm.nih.gov/{v['pmid']}/)" if v['pmid'] else ''
        return f"- {v['riga']}" + (f" ({fonte})" if fonte else '') + link

    corpo = [misura, '']
    if evid:
        corpo += [f"IN EVIDENZA: {evid['riga']}" + (f" ({evid['solid']} · {evid['j']})" if evid['j'] else ''),
                  f"[PubMed](https://pubmed.ncbi.nlm.nih.gov/{evid['pmid']}/)", '']
    righe = [v for v in voci if v is not evid]
    for dom, nome in DOMINI:
        mie = [v for v in righe if v['dom'] == dom]
        if not mie:
            continue
        corpo.append(nome)
        corpo += [rl(v) for v in mie]
        corpo.append('')
    orfane = [v for v in righe if v['dom'] not in {d for d, _ in DOMINI}]
    if orfane:
        corpo.append('ALTRO')
        corpo += [rl(v) for v in orfane]
        corpo.append('')

    m_cg = re.search(r'var CONGRESSI=(\[.*?\]);', dati, re.S)
    congressi = []
    for v in (_voci_blocco(m_cg.group(1)) if m_cg else []):
        sig = _campo(v, 'sig')
        if not sig:
            continue
        pezzi = [sig] + [x for x in (_campo(v, 'citta'), _campo(v, 'date')) if x]
        for etich, ch in (('scadenza abstract', 'abstract'), ('early bird', 'early')):
            val = _campo(v, ch)
            if val:
                pezzi.append(f"{etich}: {val}")
        congressi.append('- ' + ' · '.join(pezzi))
    if congressi:
        corpo += ['CONGRESSI'] + congressi + ['']

    m_in = re.search(r'var INDUSTRIA=(\[.*?\]);', dati, re.S)
    notizie, richiami = [], []
    for v in (_voci_blocco(m_in.group(1)) if m_in else []):
        riga = _campo(v, 'riga')
        if not riga:
            continue
        fonte = _campo(v, 'fonte')
        url = _campo(v, 'url')
        r = '- ' + riga + (f" ({fonte})" if fonte else '') + (f" — [fonte]({url})" if url else '')
        (richiami if _campo(v, 'tipo') == 'richiamo' else notizie).append(r)
    if notizie or richiami:
        corpo += ['INDUSTRIA E MERCATO'] + notizie + richiami + ['']

    base = 'https://dariogiunchi-cmd.github.io/pulse-knee'
    corpo += ['---',
              f"Ascolta l'episodio: {base}/audio/{build}.mp3",
              f"Apri PULSE: {base}/",
              'Rispondi a questa email per orientare i prossimi numeri.']

    titolo = f"PULSE {data_it} — " + (evid['riga'] if evid else misura)
    return titolo[:250], '\n'.join(corpo)


if __name__ == '__main__':
    t, c = costruisci_email(open('dati/giorno.js', encoding='utf-8').read())
    print(t)
    print()
    print(c)
