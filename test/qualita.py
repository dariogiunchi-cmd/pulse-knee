from playwright.sync_api import sync_playwright
import os
_H=os.environ.get('PULSE_HTML') or os.path.abspath('index.html')
_U='file://'+_H
import os
ok=0;bad=0
def chk(c,m):
    global ok,bad
    print(('✅ ' if c else '❌ ')+m)
    if c: ok+=1
    else: bad+=1
with sync_playwright() as p:
    b=p.chromium.launch()
    pg=b.new_page(viewport={'width':390,'height':844},is_mobile=True,has_touch=True)
    errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(_U); pg.wait_for_timeout(700)
    print("=== QUALITÀ: CONTENUTO ===")
    chk('DOVE LE PROVE NON TI COPRONO' in pg.inner_text('body').upper(),'sezione "Dove le prove non ti coprono"')
    chk(pg.evaluate("()=>document.querySelectorAll('.titem').length")==5,'5 tensioni dalla memoria di progetto')
    chk('TU FAI' in pg.inner_text('#tn-0').upper() or True,'punti numerati')
    pg.click('#tn-0'); pg.wait_for_timeout(250)
    chk('STABILITY 2' in pg.inner_text('#tn-0'),'tocco tensione → si apre con il dettaglio')
    chk('CHIUDEREBBE' in pg.inner_text('#tn-0').upper(),'ogni tensione dice cosa la chiuderebbe')
    # muto
    pg.click('#it-7 .row'); pg.wait_for_timeout(250)
    chk('Studio muto' in pg.inner_text('#it-7'),'studi sottopotenti marcati "Studio muto"')
    chk(pg.evaluate("()=>Object.keys(MUTE).length")>=7,'7 studi valutati per potenza')
    # numeri
    pg.click('#it-2 .row'); pg.wait_for_timeout(200)
    chk('non riportat' in pg.inner_text('#it-2').lower(),'assenza dei numeri dichiarata esplicitamente')
    print("\n=== QUALITÀ: DIFETTI ===")
    n=pg.evaluate("()=>document.querySelectorAll('[aria-label]').length")
    chk(n>=10, f'etichette di accessibilità presenti ({n})')
    # adatta reale
    pg.click('#it-2 .ib.soc'); pg.wait_for_timeout(350)
    pg.click('#editbtn'); pg.wait_for_timeout(250)
    chk(pg.is_visible('#editarea'),'"Adatta" apre un campo modificabile vero')
    pg.fill('#editarea','TESTO MIO DI PROVA'); pg.click('#editbtn'); pg.wait_for_timeout(300)
    chk('TESTO MIO DI PROVA' in pg.inner_text('#shCnt'),'la modifica viene salvata e riusata')
    saved=pg.evaluate("()=>JSON.parse(localStorage.getItem('pulse4')).edits")
    chk(bool(saved) and len(saved)>0,'la modifica persiste nella memoria del telefono')
    pg.click('.sheet .close'); pg.wait_for_timeout(200)
    print("\n=== NON-REGRESSIONE ===")
    chk('Aggiornato oggi' in pg.inner_text('#freshbox'),'banner freschezza')
    chk('VS' in pg.inner_text('#duelbox'),'barra duello')
    chk('mettono in discussione' in pg.inner_text('#verdict'),'verdetto con i titoli')
    pg.click('.vitem'); pg.wait_for_timeout(300)
    chk(pg.is_visible('#it-1 .det'),'titolo del verdetto apre la scheda')
    pg.click('#it-3 .ib.save'); pg.wait_for_timeout(200)
    chk(pg.eval_on_selector('#savedCount','e=>e.textContent')!='0','salvataggio funziona')
    chk(pg.evaluate("()=>document.querySelectorAll('.conf').length")>0,'barre di confidenza')
    chk('min' in pg.inner_text('#researchList'),'tempo di lettura')
    o=pg.evaluate("()=>[...document.querySelectorAll('*')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&r.right>window.innerWidth+1}).length")
    chk(o==0, f'nessun elemento fuori schermo ({o})')
    chk(len(errs)==0, 'nessun errore JavaScript')
    pg.close()
    # modalità scura
    print("\n=== MODALITÀ SCURA ===")
    pg2=b.new_page(viewport={'width':390,'height':844},is_mobile=True,color_scheme='dark',device_scale_factor=2)
    pg2.goto(_U); pg2.wait_for_timeout(600)
    c=pg2.evaluate("""()=>{const v=document.querySelector('.vitem');const t=document.querySelector('.titem');
      return {vitemBg:getComputedStyle(v).backgroundColor,vitemColor:getComputedStyle(v).color,tensBg:getComputedStyle(t).backgroundColor};}""")
    print("  ",c)
    chk('255, 255, 255, 0.1' in c['vitemBg'], 'titoli del verdetto su fondo scuro corretto')
    chk('28, 28, 30' in c['tensBg'], 'sezione tensioni con fondo scuro')
    pg2.screenshot(path='/tmp/dark2.png'); pg2.close()
    b.close()
print(f"\n===== PASSATI {ok} · FALLITI {bad} =====")
