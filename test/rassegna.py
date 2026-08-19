# -*- coding: utf-8 -*-
"""
PULSE — collaudo della Rassegna (richiami, trial, video dal raccoglitore notturno).

Si collauda la MACCHINA con dati sintetici, mai il carico del giorno: il file
fonti/raccolta.json cambia ogni notte e può legittimamente essere vuoto o avere
fonti mute — ciò che non può succedere è che una fonte muta venga TACIUTA, o che
un DOI citato colpito da ritrattazione non diventi rosso.
"""
from playwright.sync_api import sync_playwright
import os, sys
_H = os.environ.get('PULSE_HTML') or os.path.abspath('index.html')
_U = 'file://' + _H
ok = 0; bad = 0
def chk(c, m):
    global ok, bad
    print(('✅ ' if c else '❌ ') + m)
    if c: ok += 1
    else: bad += 1

with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 390, 'height': 844})
    errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto(_U); pg.wait_for_timeout(600)

    chk(pg.evaluate("typeof rassHTML==='function' && typeof apriRassegna==='function'"),
        "la macchina della rassegna esiste")
    chk(pg.locator('#rassegna').count() == 1 and pg.locator('.tabs button', has_text='Rassegna').count() == 1,
        "la scheda Rassegna è raggiungibile con un tocco")

    # tutte le fonti a posto → tutte le sezioni, col rosso sulle aziende sorvegliate
    h = pg.evaluate("""rassHTML({generato:'2026-01-01T04:15:00Z',fonti:{
      openfda:{esito:'ok',dati:{richiami:[{recalling_firm:'Ditta Sorvegliata',product_description:'knee implant',sorvegliata:true},
                                          {recalling_firm:'Altra Ditta',product_description:'knee brace',sorvegliata:false}],enforcement:[]}},
      swissmedic:{esito:'ok',dati:{voci:[{titolo:'Avviso',link:'https://example.org',data:'2026-01-01'}]}},
      trials:{esito:'ok',dati:[{sorveglianza:'Sorveglianza di prova',studi:[{nct:'NCT99999999',titolo:'t',stato:'RECRUITING',aggiornato:'2026-01-01',n:10}]}]},
      ritrattazioni:{esito:'ok',dati:{doi_citati_controllati:5,colpiti:[],nel_perimetro:[]}},
      destino:{esito:'ok',dati:[{pmid:'11111111',titolo:'PICK di prova',citanti:['22222222','33333333'],nuovi:['33333333']},
                                {pmid:'44444444',titolo:'PICK recente',citanti:[],nuovi:[]}]},
      youtube:{esito:'ok',dati:{video:[{canale:'Canale',titolo:'video',link:'https://example.org',data:'2026-01-01'}]}}}})""")
    chk('🔴' in h and 'Ditta Sorvegliata' in h, "un richiamo su azienda sorvegliata è rosso")
    chk('⚪' in h, "un richiamo su altra ditta resta bianco")
    chk('NCT99999999' in h and 'Sorveglianza di prova' in h, "i trial delle tensioni compaiono con NCT e stato")
    chk('5' in h and 'ritirato' in h, "il conteggio dei DOI controllati è dichiarato")
    chk('PICK di prova' in h and 'pubmed.ncbi.nlm.nih.gov/33333333' in h,
        "il destino dei verdetti: un citante nuovo compare col suo link PubMed")
    chk('nessun citante ancora' in h, "un PICK senza citanti lo dichiara, non lo nasconde")
    chk('1 con citanti nuovi' in h, "il titolo della sezione conta i PICK con citanti nuovi")

    # ogni fonte muta si dichiara, una per una
    ko = pg.evaluate("""rassHTML({generato:'x',fonti:{openfda:{esito:'non risposto: t'},swissmedic:{esito:'non risposto: t'},
      trials:{esito:'non risposto: t'},ritrattazioni:{esito:'non risposto: t'},destino:{esito:'non risposto: t'},
      youtube:{esito:'non risposto: t'}}})""")
    chk(ko.count('non verificata stanotte') == 6, "sei fonti mute → sei dichiarazioni, nessuna taciuta")

    # un DOI citato colpito da ritrattazione deve urlare
    hot = pg.evaluate("""rassHTML({generato:'x',fonti:{ritrattazioni:{esito:'ok',
      dati:{doi_citati_controllati:5,colpiti:[{tipo:'retraction',doi_citato:['10.1000/prova']}],nel_perimetro:[]}}}})""")
    chk('🔴' in hot and '10.1000/prova' in hot and 'colpito' in hot,
        "una ritrattazione su un DOI citato diventa rossa e nominata")

    # niente dati → niente finzioni
    chk('non ha ancora depositato' in pg.evaluate("rassHTML(null)"),
        "senza raccolta l'app lo dice, non finge")

    # l'apertura vera: su file:// il fetch fallisce e il fallimento è dichiarato
    pg.click(".tabs button:has-text('Rassegna')"); pg.wait_for_timeout(500)
    t = pg.inner_text('#rassbox')
    chk('non raggiungibile' in t or 'Carico' in t or 'raccoglitore' in t,
        "il caricamento fallito si dichiara invece di lasciare il vuoto")

    chk(len(errs) == 0, "nessun errore JavaScript")
    b.close()

print(f"\n===== RASSEGNA: {ok} verificati · {bad} errori =====")
sys.exit(1 if bad else 0)
