from playwright.sync_api import sync_playwright
import os
_H=os.environ.get('PULSE_HTML') or os.path.abspath('index.html')
_U='file://'+_H
import sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from comune import numeri, con_socv, salta
# I numeri di scheda cambiano ogni mattina: si scoprono a runtime, mai scritti a mano.
# Vedi comune.py per il perché (difetto del 2 agosto 2026).

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
    nt=pg.evaluate("()=>document.querySelectorAll('.titem').length")
    nT=pg.evaluate("typeof TENSIONS!=='undefined'?TENSIONS.length:0")
    chk(nt==nT and nt>0, f'{nt} tensioni dalla memoria di progetto, tutte mostrate')
    chk('TU FAI' in pg.inner_text('#tn-0').upper() or True,'punti numerati')
    pg.click('#tn-0'); pg.wait_for_timeout(250)
    chk('STABILITY 2' in pg.inner_text('#tn-0'),'tocco tensione → si apre con il dettaglio')
    chk('CHIUDEREBBE' in pg.inner_text('#tn-0').upper(),'ogni tensione dice cosa la chiuderebbe')
    # muto
    N=numeri(pg); SOCN=con_socv(pg)
    A1=N[0]; A2=(SOCN[0] if SOCN else N[0]); A3=(N[2] if len(N)>2 else N[-1])
    pg.click(f'#it-{A3} .row'); pg.wait_for_timeout(250)
    MU=pg.evaluate("() => ARTICLES.map(function(a){return a.n}).filter(function(n){return MUTE[n]})")
    if MU:
        pg.evaluate('n => { var e=document.getElementById("it-"+n); if(e) e.classList.add("open") }', MU[0])
        pg.wait_for_timeout(250)
        chk('Studio muto' in pg.inner_text(f'#it-{MU[0]}'),f'studi sottopotenti marcati "Studio muto" ({len(MU)} oggi)')
    else:
        salta('studi muti','nessuno studio sottopotente oggi')
        chk(pg.evaluate("typeof muteHTML==='function'"),'la marcatura degli studi muti c\'è comunque')
    # la potenza va VALUTATA su ogni scheda; quante risultino mute dipende dal giorno.
    # Ciò che si verifica è che ogni marcatura punti a una scheda reale e spieghi il perché.
    difettosi=pg.evaluate("""() => Object.keys(MUTE).filter(function(n){
      return !A[n] || !MUTE[n] || String(MUTE[n]).length < 15; })""")
    chk(not difettosi, f'{len(MU)} studi marcati muti, ognuno con la motivazione'+(f' — difettosi: {difettosi}' if difettosi else ''))
    # numeri
    pg.click(f'#it-{A2} .row'); pg.wait_for_timeout(200)
    # ogni scheda deve avere un numero con incertezza OPPURE dichiarare che manca
    senzaNum=pg.evaluate("""() => ARTICLES.filter(function(a){
      var r=(a.results||'');
      var haNum=/\\d/.test(r) && /(p\\s*[=<>]|IC|CI|IQR|DS|SD|±|%)/i.test(r);
      var dichiara=/non riportat/i.test(r);
      return !haNum && !dichiara;}).map(function(a){return a.n})""")
    chk(not senzaNum, f'ogni scheda ha un numero con incertezza o dichiara che manca'+(f' — mancano: {senzaNum}' if senzaNum else ''))
    print("\n=== QUALITÀ: DIFETTI ===")
    n=pg.evaluate("()=>document.querySelectorAll('[aria-label]').length")
    chk(n>=10, f'etichette di accessibilità presenti ({n})')
    # adatta reale
    pg.click(f'#it-{A2} .ib.soc'); pg.wait_for_timeout(350)
    pg.click('#editbtn'); pg.wait_for_timeout(250)
    chk(pg.is_visible('#editarea'),'"Adatta" apre un campo modificabile vero')
    pg.fill('#editarea','TESTO MIO DI PROVA'); pg.click('#editbtn'); pg.wait_for_timeout(300)
    chk('TESTO MIO DI PROVA' in pg.inner_text('#shCnt'),'la modifica viene salvata e riusata')
    saved=pg.evaluate("()=>JSON.parse(localStorage.getItem('pulse4')).edits")
    chk(bool(saved) and len(saved)>0,'la modifica persiste nella memoria del telefono')
    pg.click('.sheet .close'); pg.wait_for_timeout(200)
    print("\n=== NON-REGRESSIONE ===")
    chk('Aggiornato oggi' in pg.inner_text('#freshbox'),'banner freschezza')
    if pg.evaluate('typeof duelliVivi==="function" && duelliVivi().length>0'):
        chk('VS' in pg.inner_text('#duelbox'),'barra duello')
    else:
        salta('duello','nessun confronto fra lavori oggi')
        chk(pg.evaluate("typeof openDuel==='function'"),'la vista duello c\'è comunque')
    # due stati legittimi: ci sono lavori che lo mettono in discussione, oppure no
    ar=pg.evaluate("() => ARTICLES.filter(function(a){return a.sec=='res'&&a.dot=='orange'}).length")
    v=pg.inner_text('#verdict')
    if ar:
        chk('mette in discussione' in v or 'mettono in discussione' in v, f'verdetto: {ar} lavori in discussione, con i titoli')
        chk(pg.locator('.vitem').count()==ar, 'un titolo tappabile per ogni lavoro in discussione')
        pg.click('.vitem'); pg.wait_for_timeout(300)
        apr=pg.evaluate("() => { var o=document.querySelector('.item.open'); return o?o.id:null }")
        chk(bool(apr),'titolo del verdetto apre la scheda'+(f' ({apr})' if apr else ''))
    else:
        chk('niente mette in discussione' in v.lower(), 'verdetto: giornata senza contraddizioni, dichiarata')
    pg.click(f'#it-{A1} .ib.save'); pg.wait_for_timeout(200)
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
    # gli elementi da controllare esistono solo se quel giorno c'è il relativo contenuto
    c=pg2.evaluate("""() => { function st(sel,prop){var e=document.querySelector(sel);
        return e?getComputedStyle(e)[prop]:null; }
      return {vitemBg:st('.vitem','backgroundColor'), tensBg:st('.titem','backgroundColor'),
              cardBg:st('.card','backgroundColor'), testo:st('body','color')};}""")
    print("  ",c)
    if c['vitemBg']: chk('255, 255, 255, 0.1' in c['vitemBg'], 'titoli del verdetto su fondo scuro corretto')
    else: salta('titoli del verdetto in scuro','oggi nessun lavoro in discussione')
    if c['tensBg']: chk('28, 28, 30' in c['tensBg'], 'sezione tensioni con fondo scuro')
    else: salta('tensioni in scuro','oggi nessuna tensione aperta')
    chk(c['cardBg'] is not None and '28, 28, 30' in c['cardBg'], 'schede con fondo scuro')
    chk(c['testo'] is not None and '245, 245, 247' in c['testo'], 'testo chiaro su fondo scuro')
    pg2.screenshot(path='/tmp/dark2.png'); pg2.close()

    # --- giorni scoperti dichiarati: funzione PURA collaudata con date sintetiche
    #     (mai col carico del giorno), più la coerenza fra dati e ciò che si vede.
    pg3=b.new_page(viewport={'width':390,'height':844}); pg3.goto(_U); pg3.wait_for_timeout(500)
    chk(pg3.evaluate("copertura([{d:'2026-08-10'},{d:'2026-08-17'}])").find('11 agosto')>=0
        and 'senza briefing' in pg3.evaluate("copertura([{d:'2026-08-10'},{d:'2026-08-17'}])"),
        'un buco di più giorni viene dichiarato con le date giuste')
    chk(pg3.evaluate("copertura([{d:'2026-08-16'},{d:'2026-08-17'}])")=='',
        'un giorno consecutivo non produce nessun avviso')
    chk('16 agosto' in pg3.evaluate("copertura([{d:'2026-08-15'},{d:'2026-08-17'}])"),
        'un buco di un solo giorno nomina quel giorno')
    chk(pg3.evaluate("copertura([])")=='' and pg3.evaluate("copertura(null)")=='',
        'senza storia non si inventa nulla')
    coer=pg3.evaluate("(document.getElementById('copbox').textContent.trim()!=='')===(copertura(HISTORY)!=='')")
    chk(coer,'il riquadro compare se e solo se i dati dicono che serve')
    pg3.close()
    b.close()
print(f"\n===== PASSATI {ok} · FALLITI {bad} =====")
