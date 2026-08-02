from playwright.sync_api import sync_playwright
import os
_H=os.environ.get('PULSE_HTML') or os.path.abspath('index.html')
_U='file://'+_H
import os
path=_U
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
    chk('Aggiornato oggi' in pg.inner_text('#freshbox'),'banner "Aggiornato oggi" visibile')
    chk('VS' in pg.inner_text('#duelbox'),'barra duello visibile')
    chk('min' in pg.inner_text('#researchList'),'tempo di lettura mostrato sulle schede')
    # apri dettagli prima scheda
    pg.click('#it-1 .row'); pg.wait_for_timeout(250)
    chk(pg.is_visible('#it-1 .det'),'tocco sulla scheda → dettagli si aprono')
    chk('COLLEGATI' in pg.inner_text('#it-1').upper(),'campo "Collegati nel tempo" presente')
    # salva
    pg.click('#it-1 .ib.save'); pg.wait_for_timeout(200)
    chk(pg.eval_on_selector('#savedCount','e=>e.textContent')=='1','tocco su ★ → contatore Salvati = 1')
    # filtro
    pg.click('.filters .fchip >> nth=1'); pg.wait_for_timeout(250)
    chk(pg.eval_on_selector_all('#researchList .item','e=>e.length')==2,'filtro "La mia pratica" → 2 lavori')
    pg.click('.filters .fchip >> nth=0'); pg.wait_for_timeout(200)
    # duello
    pg.click('#duelbox .duelbar'); pg.wait_for_timeout(350)
    chk(pg.is_visible('#ov'),'tocco su VS → si apre il confronto')
    chk('duelgrid' in pg.inner_html('#shCnt'),'confronto in due colonne')
    pg.click('.sheet .close'); pg.wait_for_timeout(200)
    # tab archivio + autocritica + ricerca
    pg.click('.tabs button >> nth=1'); pg.wait_for_timeout(300)
    chk('AUTOCRITICA' in pg.inner_text('#auditbox').upper(),'Archivio → autocritica settimanale')
    pg.fill('#histq','menisco'); pg.wait_for_timeout(350)
    chk(len(pg.inner_text('#histres'))>40,'ricerca archivio "menisco" → risultati')
    # salvati + ritrattazioni
    pg.click('.tabs button >> nth=2'); pg.wait_for_timeout(300)
    chk('Nessun articolo salvato è stato ritirato' in pg.inner_text('#retrbox'),'Salvati → conferma controllo ritrattazioni')
    # impostazioni
    pg.click('.tabs button >> nth=3'); pg.wait_for_timeout(300)
    chk('PROMEMORIA' in pg.inner_text('#settings').upper(),'Impostazioni si apre')
    # zoom test: focus su input non deve ingrandire (font >=16px)
    fs=pg.eval_on_selector('#jinput','e=>getComputedStyle(e).fontSize')
    chk(float(fs.replace('px',''))>=16, f'campi di testo a {fs} → iPhone non ingrandisce la pagina')
    chk(len(errs)==0,'nessun errore JavaScript durante l\'uso')
    pg.screenshot(path='/tmp/shot.png',full_page=False)
    pg.close(); b.close()
print(f"\n===== PASSATI {ok} · FALLITI {bad} =====")
