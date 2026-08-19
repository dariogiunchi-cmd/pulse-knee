#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PULSE — il raccoglitore notturno delle fonti esterne.

PERCHÉ ESISTE. Il sandbox delle sessioni Claude ha la rete chiusa: openFDA,
Swissmedic, ClinicalTrials.gov e Crossref non rispondono da lì (verificato il
17-18 agosto 2026). I runner di GitHub Actions invece escono su internet: questo
script gira lì alle 4.15 UTC (.github/workflows/raccolta.yml), interroga SOLO
API ufficiali e feed pubblici, e deposita `fonti/raccolta.json` nel repository.
La sessione del briefing delle 5.00 lo trova come file locale.

PRINCIPI, gli stessi di tutto il sistema:
- una fonte che non risponde si DICHIARA (`esito` per fonte), mai si tace;
- niente scraping di piattaforme che lo vietano: API e feed, punto;
- lo script non decide che cosa è importante — raccoglie; giudica il briefing.

Uso:  python3 test/raccolta.py            scrive fonti/raccolta.json
      python3 test/raccolta.py --scopri   in più, risolve feed Swissmedic e
                                          canali YouTube candidati (si usa a mano
                                          finché la configurazione non è stabile)
"""
import json, os, re, sys, time
import urllib.parse
import urllib.request, urllib.error
from datetime import datetime, timedelta, timezone
from xml.etree import ElementTree

QUI = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(QUI)
CFG = json.load(open(os.path.join(APP, 'fonti', 'fonti.json'), encoding='utf-8'))
UA = {'User-Agent': 'PULSE-raccolta/1.0 (https://github.com/dariogiunchi-cmd/pulse-knee; mailto:dariogiunchi@gmail.com)'}
OGGI = datetime.now(timezone.utc)


def prendi(url, timeout=25):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode('utf-8', 'replace')


def fonte(fn):
    """Esegue una fonte e ne cattura l'esito invece di far morire il raccoglitore."""
    try:
        dati = fn()
        return {'esito': 'ok', 'dati': dati}
    except Exception as e:
        return {'esito': f'non risposto: {type(e).__name__} {str(e)[:120]}', 'dati': None}


# ---------------------------------------------------------------- openFDA
def openfda():
    out = {}
    for nome, url in (('richiami', CFG['openfda']['url_prodotto']),
                      ('enforcement', CFG['openfda']['url_enforcement'])):
        try:
            j = json.loads(prendi(url))
            voci = []
            for r in j.get('results', []):
                voci.append({k: r.get(k) for k in
                             ('recall_number', 'recalling_firm', 'product_description',
                              'reason_for_recall', 'root_cause_description',
                              'event_date_initiated', 'report_date', 'recall_status',
                              'classification') if r.get(k)})
            out[nome] = voci
        except urllib.error.HTTPError as e:
            if e.code == 404:      # openFDA risponde 404 quando la ricerca non trova nulla
                out[nome] = []
            else:
                raise
    sorv = [a.lower() for a in CFG['aziende_sorvegliate']]
    for gruppo in out.values():
        for v in gruppo:
            # il nome sorvegliato può stare nella ditta che richiama OPPURE nel
            # prodotto: il richiamo dei kit Medline contenenti materiale Zimmer
            # Biomet (visto al primo giro reale) sfuggiva al solo campo ditta.
            testo = ((v.get('recalling_firm') or '') + ' ' + (v.get('product_description') or '')).lower()
            v['sorvegliata'] = any(a in testo for a in sorv)
    return out


# ---------------------------------------------------------------- Swissmedic
def swissmedic():
    feeds = CFG.get('swissmedic_feed') or []
    if not feeds:
        return {'nota': 'nessun feed configurato: usare --scopri per trovarli', 'voci': []}
    voci = []
    for u in feeds:
        xml = prendi(u)
        root = ElementTree.fromstring(xml.encode())
        for item in root.iter():
            if item.tag.endswith('item') or item.tag.endswith('entry'):
                t = {c.tag.split('}')[-1]: (c.text or '').strip() for c in item}
                voci.append({'feed': u, 'titolo': t.get('title'),
                             'link': t.get('link') or t.get('id'),
                             'data': t.get('pubDate') or t.get('updated')})
    return {'voci': voci[:40]}


def swissmedic_scopri():
    """Cerca i feed in due mosse: (1) qualunque href che contenga 'rss' nelle pagine
    di partenza; (2) prova a scaricare i candidati e tiene solo ciò che è XML vero.
    Nulla si inventa: si registra che cosa risponde e che cosa no."""
    candidati, trovati = [], []
    for pagina in CFG.get('swissmedic_scopri', []):
        try:
            html = prendi(pagina)
            for m in re.finditer(r'href="([^"]*rss[^"]*)"', html, re.I):
                u = m.group(1).replace('&amp;', '&')
                if u.startswith('/'):
                    u = 'https://www.swissmedic.ch' + u
                if u.startswith('http') and u not in candidati:
                    candidati.append(u)
        except Exception as e:
            trovati.append({'pagina': pagina, 'errore': f'{type(e).__name__} {str(e)[:80]}'})
    for u in candidati[:12]:
        try:
            corpo = prendi(u)
            if '<rss' in corpo[:400] or '<feed' in corpo[:400]:
                tit = re.search(r'<title>([^<]*)</title>', corpo)
                trovati.append({'feed': u, 'xml': True, 'titolo': tit.group(1) if tit else ''})
            else:
                trovati.append({'feed': u, 'xml': False, 'nota': 'risponde ma non è un feed'})
        except Exception as e:
            trovati.append({'feed': u, 'errore': f'{type(e).__name__} {str(e)[:80]}'})
        time.sleep(1)
    return trovati


# ---------------------------------------------------------------- ClinicalTrials.gov
def trials():
    out = []
    for q in CFG['trials_query']:
        url = ('https://clinicaltrials.gov/api/v2/studies?query.term=' +
               urllib.parse.quote(q['q']) +
               '&sort=LastUpdatePostDate:desc&pageSize=8'
               '&fields=NCTId,BriefTitle,OverallStatus,LastUpdatePostDate,Phase,EnrollmentCount,StudyType')
        j = json.loads(prendi(url))
        studi = []
        for s in j.get('studies', []):
            p = s.get('protocolSection', {})
            idm = p.get('identificationModule', {})
            st = p.get('statusModule', {})
            de = p.get('designModule', {})
            studi.append({'nct': idm.get('nctId'), 'titolo': idm.get('briefTitle'),
                          'stato': st.get('overallStatus'),
                          'aggiornato': (st.get('lastUpdatePostDateStruct') or {}).get('date'),
                          'fase': (de.get('phases') or None),
                          'n': (de.get('enrollmentInfo') or {}).get('count'),
                          'tipo': de.get('studyType')})
        out.append({'sorveglianza': q['nome'], 'studi': studi})
        time.sleep(1)
    return out


# ---------------------------------------------------------------- Crossref (ritrattazioni)
def citati_nel_repo():
    """I DOI citati da PULSE, letti dallo storico e dalla memoria del repository."""
    dois = set()
    for f in ('cervello/claude__09-storico.md', 'cervello/03-memoria.md'):
        p = os.path.join(APP, f)
        if os.path.exists(p):
            dois.update(re.findall(r'\b(10\.\d{4,9}/[^\s|\]]+)', open(p, encoding='utf-8').read()))
    return {d.rstrip('.,;') for d in dois}


def ritrattazioni():
    da = (OGGI - timedelta(days=120)).strftime('%Y-%m-%d')
    miei = citati_nel_repo()
    esiti = {'doi_citati_controllati': len(miei), 'colpiti': [], 'nel_perimetro': [], 'tipi_falliti': []}
    for tipo in ('retraction', 'expression_of_concern', 'withdrawal'):
        url = (f'https://api.crossref.org/works?filter=update-type:{tipo},from-update-date:{da}'
               f'&rows=200&select=DOI,title,update-to,issued')
        try:
            j = json.loads(prendi(url))
        except Exception as e:
            esiti['tipi_falliti'].append({'tipo': tipo, 'errore': f'{type(e).__name__} {str(e)[:80]}'})
            continue
        for w in j.get('message', {}).get('items', []):
            bersagli = [u.get('DOI', '').lower() for u in (w.get('update-to') or [])]
            titolo = ' '.join(w.get('title') or [])
            colpito = [d for d in miei if d.lower() in bersagli]
            if colpito:
                esiti['colpiti'].append({'tipo': tipo, 'doi_citato': colpito,
                                         'avviso': w.get('DOI'), 'titolo': titolo})
            elif any(p.lower() in titolo.lower() for p in CFG['crossref_parole']):
                esiti['nel_perimetro'].append({'tipo': tipo, 'avviso': w.get('DOI'),
                                               'bersaglio': bersagli[:1], 'titolo': titolo[:160]})
        time.sleep(1)
    esiti['nel_perimetro'] = esiti['nel_perimetro'][:25]
    return esiti


# ------------------------------------------- il destino dei verdetti (chi cita i PICK)
def _pick_passati():
    """I lavori del giorno (PICK) di tutti i briefing, letti dallo storico."""
    p = os.path.join(APP, 'cervello', 'claude__09-storico.md')
    picks = []
    if os.path.exists(p):
        for m in re.finditer(r'PICK: ([^·\n]+)·\s*PMID (\d{7,9})', open(p, encoding='utf-8').read()):
            picks.append({'titolo': m.group(1).strip(' —·'), 'pmid': m.group(2)})
    visti = set()
    return [x for x in picks if not (x['pmid'] in visti or visti.add(x['pmid']))]


def destino():
    """Un verdetto non è vero per sempre: conta come la letteratura successiva tratta
    il lavoro. Qui si chiede a PubMed (elink, cited-in) chi ha citato ogni PICK; i
    citanti NUOVI rispetto all'ultima raccolta finiscono in evidenza, e il mandato
    del mattino li legge e li classifica (conferma/contrasta) sugli abstract."""
    picks = _pick_passati()
    prima = {}
    vecchio = os.path.join(APP, 'fonti', 'raccolta.json')
    if os.path.exists(vecchio):
        try:
            v = json.load(open(vecchio, encoding='utf-8'))
            for d in ((v.get('fonti', {}).get('destino', {}) or {}).get('dati') or []):
                prima[d.get('pmid')] = set(d.get('citanti') or [])
        except Exception:
            pass
    out = []
    for pk in picks:
        url = ('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed'
               '&linkname=pubmed_pubmed_citedin&retmode=json&id=' + pk['pmid'])
        j = json.loads(prendi(url))
        citanti = []
        for ls in j.get('linksets', []):
            for db in ls.get('linksetdbs', []):
                if db.get('linkname') == 'pubmed_pubmed_citedin':
                    citanti = [str(x) for x in db.get('links', [])]
        nuovi = sorted(set(citanti) - prima.get(pk['pmid'], set()))
        out.append({'pmid': pk['pmid'], 'titolo': pk['titolo'][:110],
                    'citanti': sorted(citanti), 'nuovi': nuovi})
        time.sleep(1)
    return out


# ---------------------------------------------------------------- YouTube (feed ufficiali)
def youtube():
    voci = []
    limite = OGGI - timedelta(days=14)
    for c in CFG.get('youtube_canali', []):
        url = 'https://www.youtube.com/feeds/videos.xml?channel_id=' + c['id']
        xml = prendi(url)
        root = ElementTree.fromstring(xml.encode())
        ns = {'a': 'http://www.w3.org/2005/Atom'}
        for e in root.findall('a:entry', ns)[:10]:
            pub = (e.findtext('a:published', '', ns) or '')[:10]
            try:
                recente = datetime.fromisoformat(pub).replace(tzinfo=timezone.utc) >= limite
            except ValueError:
                recente = False
            if recente:
                link = e.find('a:link', ns)
                voci.append({'canale': c['nome'], 'titolo': e.findtext('a:title', '', ns),
                             'link': link.get('href') if link is not None else None, 'data': pub})
        time.sleep(1)
    return {'video': sorted(voci, key=lambda v: v['data'], reverse=True)}


def youtube_scopri():
    trovati = []
    for h in CFG.get('youtube_scopri', []):
        try:
            html = prendi('https://www.youtube.com/' + h)
            cid = (re.search(r'"channelId":"(UC[\w-]{20,})"', html)
                   or re.search(r'youtube\.com/channel/(UC[\w-]{20,})', html)
                   or re.search(r'"browseId":"(UC[\w-]{20,})"', html))
            tit = re.search(r'<title>([^<]*)</title>', html)
            trovati.append({'handle': h, 'id': cid.group(1) if cid else None,
                            'titolo': (tit.group(1).replace(' - YouTube', '') if tit else None)})
        except Exception as e:
            trovati.append({'handle': h, 'errore': f'{type(e).__name__} {str(e)[:80]}'})
        time.sleep(1)
    return trovati


# ---------------------------------------------------------------- linee guida
def linee_guida():
    """Consensus, linee guida e position statement sul ginocchio, da PubMed.
    Nasce da un caso reale (19 agosto): un consensus americano sul post-operatorio
    delle suture meniscali circolava sui social PRIMA che lui lo vedesse altrove.
    La rete cattura per TITOLO oltre che per publication type, perché i consensus
    escono spesso tipizzati come semplici articoli."""
    q = urllib.parse.quote(CFG['linee_guida_query'])
    gg = CFG.get('linee_guida_giorni', 60)
    j = json.loads(prendi('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
                          f'?db=pubmed&retmode=json&retmax=40&datetype=edat&reldate={gg}&term=' + q))
    ids = (j.get('esearchresult', {}) or {}).get('idlist', [])
    voci = []
    if ids:
        time.sleep(1)
        s = json.loads(prendi('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi'
                              '?db=pubmed&retmode=json&id=' + ','.join(ids)))
        r = s.get('result', {})
        for pid in ids:
            d = r.get(pid) or {}
            if not d or not d.get('title'):
                continue
            voci.append({'pmid': pid, 'titolo': d.get('title')[:180],
                         'rivista': d.get('fulljournalname') or d.get('source'),
                         'data': d.get('epubdate') or d.get('pubdate'),
                         'tipi': list(d.get('pubtype') or [])[:3]})
    return {'finestra_giorni': gg, 'voci': voci}


# ---------------------------------------------------------------- polso social
def polso():
    """Di che cosa parla la comunità: Altmetric aggrega le menzioni PUBBLICHE dei
    lavori scientifici (X, notizie, blog) — è la via legale al segnale «i colleghi
    ne parlano sui social»: non si scrutano i profili, si guarda quali LAVORI
    stanno circolando. Instagram non è tracciabile da nessuna API pubblica: quel
    canale resta alla rassegna dal Mac (claude__15)."""
    conf = CFG.get('altmetric', {})
    parole = [p.lower() for p in CFG['crossref_parole']]
    voci = []
    for pag in range(1, conf.get('pagine', 3) + 1):
        try:
            j = json.loads(prendi('https://api.altmetric.com/v1/citations/'
                                  f"{conf.get('finestra', '1w')}?num_results={conf.get('per_pagina', 100)}&page={pag}"))
        except urllib.error.HTTPError:
            if pag == 1:
                raise
            break
        for r in j.get('results', []):
            t = (r.get('title') or '').lower()
            if any(p in t for p in parole):
                voci.append({'titolo': (r.get('title') or '')[:160],
                             'rivista': r.get('journal'),
                             'doi': r.get('doi'), 'pmid': r.get('pmid'),
                             'punteggio': round(r.get('score') or 0),
                             'post_x': r.get('cited_by_tweeters_count') or 0,
                             'notizie': r.get('cited_by_msm_count') or 0,
                             'url': ('https://doi.org/' + r['doi']) if r.get('doi') else None})
        time.sleep(1)
    visti = set()
    voci = [v for v in voci if not ((v['doi'] or v['titolo']) in visti or visti.add(v['doi'] or v['titolo']))]
    voci.sort(key=lambda v: -v['punteggio'])
    return {'finestra': conf.get('finestra', '1w'), 'voci': voci[:12]}


# ---------------------------------------------------------------- preprint
def preprint():
    """Preprint sul ginocchio da Europe PMC (medRxiv, bioRxiv, Research Square…):
    la letteratura PRIMA della revisione. Si segnalano, non diventano mai schede:
    un preprint non è una prova, e la Rassegna lo dice."""
    gg = CFG.get('europepmc_giorni', 30)
    da = (OGGI - timedelta(days=gg)).strftime('%Y-%m-%d')
    a = OGGI.strftime('%Y-%m-%d')
    termini = ' OR '.join(f'TITLE:"{p}"' for p in
                          ('knee', 'meniscus', 'meniscal', 'anterior cruciate', 'patellofemoral', 'knee arthroplasty'))
    q = urllib.parse.quote(f'SRC:PPR AND FIRST_PDATE:[{da} TO {a}] AND ({termini})')
    j = json.loads(prendi('https://www.ebi.ac.uk/europepmc/webservices/rest/search'
                          '?format=json&pageSize=25&sort=P_PDATE_D%20desc&query=' + q))
    voci = []
    for r in ((j.get('resultList') or {}).get('result') or []):
        voci.append({'titolo': (r.get('title') or '')[:160],
                     'dove': r.get('journalTitle') or r.get('publisher') or 'archivio preprint',
                     'data': r.get('firstPublicationDate'),
                     'doi': r.get('doi'),
                     'url': ('https://doi.org/' + r['doi']) if r.get('doi') else None})
    return {'finestra_giorni': gg, 'voci': voci,
            'nota': 'preprint NON sottoposti a revisione: si leggono con questo peso, mai citati come prove'}


# ---------------------------------------------------------------- esecuzione
if __name__ == '__main__':
    scopri = '--scopri' in sys.argv
    out = {'generato': OGGI.strftime('%Y-%m-%dT%H:%M:%SZ'),
           'nota': 'Raccolta automatica da API ufficiali e feed pubblici. Ogni fonte dichiara il suo esito: «non risposto» significa che stanotte quella fonte NON è stata verificata.',
           'fonti': {
               'openfda': fonte(openfda),
               'swissmedic': fonte(swissmedic),
               'trials': fonte(trials),
               'ritrattazioni': fonte(ritrattazioni),
               'youtube': fonte(youtube),
               'destino': fonte(destino),
               'linee_guida': fonte(linee_guida),
               'polso': fonte(polso),
               'preprint': fonte(preprint),
           }}
    if scopri:
        out['scoperta'] = {'swissmedic': fonte(swissmedic_scopri), 'youtube': fonte(youtube_scopri)}
    dest = os.path.join(APP, 'fonti', 'raccolta.json')
    json.dump(out, open(dest, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    ko = [k for k, v in out['fonti'].items() if v['esito'] != 'ok']
    print(f"🌙 raccolta scritta: {os.path.getsize(dest)//1024} KB · fonti non risposte: {ko or 'nessuna'}")
