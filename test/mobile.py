from playwright.sync_api import sync_playwright
import os
_H=os.environ.get('PULSE_HTML') or os.path.abspath('index.html')
_U='file://'+_H
import os
path=_U
import sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from comune import numeri, con_socv, con_nlb, salta
# I numeri di scheda cambiano ogni mattina: si scoprono a runtime, mai scritti a mano.
# Vedi comune.py per il perché (difetto del 2 agosto 2026).

ok=0;bad=0
def chk(c,m):
    global ok,bad
    print(('✅ ' if c else '❌ ')+m); 
    if c: ok+=1
    else: bad+=1
with sync_playwright() as p:
    b=p.chromium.launch()
    for name,w,hh in [('iPhone SE',375,667),('iPhone 14',390,844),('iPhone 14 Pro Max',430,932)]:
        pg=b.new_page(viewport={'width':w,'height':hh},is_mobile=True,has_touch=True)
        errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.goto(path); pg.wait_for_timeout(600)
        print(f"\n=== {name} ({w}px) ===")
        r=pg.evaluate("""()=>{const de=document.documentElement;
          const over=[...document.querySelectorAll('*')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&r.right>window.innerWidth+1}).length;
          return {h:de.scrollWidth>window.innerWidth+1, over};}""")
        chk(not r['h'], 'nessuno scorrimento orizzontale')
        chk(r['over']==0, f"nessun elemento tagliato fuori schermo (trovati {r['over']})")
        chk(len(errs)==0, 'nessun errore JavaScript al caricamento')
        pg.close()
    # interazioni su iPhone 14
    pg=b.new_page(viewport={'width':390,'height':844},is_mobile=True,has_touch=True)
    errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(path); pg.wait_for_timeout(600)
    print("\n=== INTERAZIONI (iPhone 14) ===")
    # Il banner va confrontato con la VERITÀ del giorno, non con l'ipotesi che il file
    # sia stato costruito oggi: quando si pubblica una correzione senza un briefing
    # nuovo, BUILD_DATE resta indietro ed è giusto che il banner lo dica (regola 11).
    _bd = pg.evaluate('BUILD_DATE')
    _oggi = pg.evaluate("new Date().toLocaleDateString('sv')")   # sv → AAAA-MM-GG
    _testo = pg.inner_text('#freshbox')
    if _bd == _oggi:
        chk('Aggiornato oggi' in _testo, 'briefing di oggi → banner «Aggiornato oggi»')
    else:
        atteso = ('in preparazione' in _testo) or ('non è arrivato' in _testo) \
                 or ('arriva verso le' in _testo) or ('giorni fa' in _testo)
        chk(atteso, f'briefing del {_bd}, oggi è {_oggi} → il banner lo dichiara')
        chk('Aggiornato oggi' not in _testo, 'non dice «aggiornato oggi» quando non lo è')
    haD=pg.evaluate('typeof duelliVivi==="function" && duelliVivi().length>0')
    if haD: chk('VS' in pg.inner_text('#duelbox'),'barra duello visibile')
    else: chk(pg.evaluate('typeof openDuel==="function"'),'duello: nessuno oggi, la funzione c\'è')
    chk('min' in pg.inner_text('#researchList'),'tempo di lettura mostrato sulle schede')
    # apri dettagli prima scheda
    N=numeri(pg); PRIMO=N[0]
    pg.click(f'#it-{PRIMO} .row'); pg.wait_for_timeout(250)
    chk(pg.is_visible(f'#it-{PRIMO} .det'),'tocco sulla scheda → dettagli si aprono')
    # «Collegati nel tempo» esiste solo se quel giorno c'è davvero un collegamento:
    # si verifica la macchina, e il contenuto solo quando c'è.
    haL=pg.evaluate('n => !!(typeof LINKS!=="undefined" && LINKS[n] && LINKS[n].length)', PRIMO)
    if haL: chk('COLLEGATI' in pg.inner_text(f'#it-{PRIMO}').upper(),'campo "Collegati nel tempo" presente')
    else: chk(pg.evaluate('typeof linksHTML==="function"'),'collegamenti nel tempo: nessuno oggi, la funzione c\'è')
    # salva
    pg.click(f'#it-{PRIMO} .ib.save'); pg.wait_for_timeout(200)
    chk(pg.eval_on_selector('#savedCount','e=>e.textContent')=='1','tocco su ★ → contatore Salvati = 1')
    # filtro
    pg.click('.filters .fchip >> nth=1'); pg.wait_for_timeout(250)
    att=pg.eval_on_selector_all('#researchList .item','e=>e.length')
    tot=pg.evaluate('ARTICLES.length')
    chk(att <= tot, f'filtro "La mia pratica" → {att} lavori su {tot}')
    pg.click('.filters .fchip >> nth=0'); pg.wait_for_timeout(200)
    # duello
    if haD:
        pg.click('#duelbox .duelbar'); pg.wait_for_timeout(350)
        chk(pg.is_visible('#ov'),'tocco su VS → si apre il confronto')
        chk('duelgrid' in pg.inner_html('#shCnt'),'confronto in due colonne')
        pg.click('#ov .close'); pg.wait_for_timeout(200)
    # tab archivio + autocritica + ricerca — per NOME, mai per posizione:
    # l'aggiunta della Rassegna ha spostato gli indici e nth=1 apriva un'altra tab.
    pg.click(".tabs button:has-text('Archivio')"); pg.wait_for_timeout(300)
    chk('AUTOCRITICA' in pg.inner_text('#auditbox').upper(),'Archivio → autocritica settimanale')
    pg.fill('#histq','menisco'); pg.wait_for_timeout(350)
    chk(pg.evaluate('typeof searchHist==="function"') and pg.locator('#histres').count()==1,'ricerca nell\'archivio attiva')
    # salvati + ritrattazioni
    pg.click(".tabs button:has-text('Salvati')"); pg.wait_for_timeout(300)
    chk('Nessun articolo salvato è stato ritirato' in pg.inner_text('#retrbox'),'Salvati → conferma controllo ritrattazioni')
    # impostazioni
    pg.click(".tabs button:has-text('Impostazioni')"); pg.wait_for_timeout(300)
    chk('PROMEMORIA' in pg.inner_text('#settings').upper(),'Impostazioni si apre')
    # zoom test: focus su input non deve ingrandire (font >=16px)
    fs=pg.eval_on_selector('#jinput','e=>getComputedStyle(e).fontSize')
    chk(float(fs.replace('px',''))>=16, f'campi di testo a {fs} → iPhone non ingrandisce la pagina')
    # --- le due righe di pulsanti non devono andare a capo ---------------------
    # Il 5 agosto 2026 «Dettagli» finiva da solo su una seconda riga, e «★ Salva»
    # faceva lo stesso nel lavoro del giorno. Nessuna suite se ne accorgeva: si
    # collaudava che i pulsanti CI FOSSERO, mai come stessero. Qui si misura, a più
    # larghezze e con il testo ingrandito come nelle impostazioni di iOS.
    def righe_di(sel):
        return pg.evaluate("""s=>{const a=document.querySelector(s);if(!a)return -1;
          const k=[...a.children].filter(c=>c.offsetParent!==null);
          if(!k.length)return 0;
          return new Set(k.map(c=>Math.round(c.getBoundingClientRect().top))).size;}""", sel)
    def tronchi_di(sel):
        return pg.evaluate("""s=>{const a=document.querySelector(s);if(!a)return 0;
          return [...a.children].filter(c=>c.scrollWidth>c.clientWidth+1).length;}""", sel)
    for larg in (320, 375, 393):
        pg.set_viewport_size({'width':larg,'height':900})
        pg.click(".tabs button:has-text('Oggi')"); pg.wait_for_timeout(300)
        for sel, nome in (('.acts','pulsanti della scheda'), ('.pick .act','pulsanti del lavoro del giorno')):
            r = righe_di(sel)
            chk(r == 1, f'{nome} su una riga sola a {larg} px' + ('' if r==1 else f' (ne servono {r})'))
            chk(tronchi_di(sel) == 0, f'{nome}: nessuna etichetta tagliata a {larg} px')
    # con il testo ingrandito del 35%
    pg.set_viewport_size({'width':393,'height':900}); pg.wait_for_timeout(200)
    pg.evaluate("""()=>{document.querySelectorAll('.ib .t').forEach(e=>e.style.fontSize='15.5px');
      document.querySelectorAll('.pick .act .btn').forEach(e=>e.style.fontSize='17px');}""")
    pg.wait_for_timeout(200)
    chk(righe_di('.acts')==1,'pulsanti della scheda su una riga anche con il testo ingrandito del 35%')
    chk(righe_di('.pick .act')==1,'pulsanti del lavoro del giorno idem')

    chk(len(errs)==0,'nessun errore JavaScript durante l\'uso')
    pg.screenshot(path='/tmp/shot.png',full_page=False)
    pg.close(); b.close()
print(f"\n===== PASSATI {ok} · FALLITI {bad} =====")
