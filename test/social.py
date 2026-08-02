from playwright.sync_api import sync_playwright
import os
_H=os.environ.get('PULSE_HTML') or os.path.abspath('index.html')
_U='file://'+_H
import os,sys
ok=0;bad=0
def chk(c,m):
    global ok,bad
    print(('✅ ' if c else '❌ ')+m)
    if c: ok+=1
    else: bad+=1
path=_H
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844},is_mobile=True)
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(_U); pg.wait_for_timeout(700)
    pg.click('#it-2 .ib.soc'); pg.wait_for_timeout(400)
    chk(pg.is_visible('#shCtrl'),'controlli tono e lunghezza')
    c=pg.inner_text('#shCtrl').upper()
    chk('CHIRURGHI' in c and 'PAZIENTI' in c,'tre toni')
    chk('CORTO' in c and 'LUNGO' in c,'tre lunghezze')
    med=pg.inner_text('#shCnt')
    pg.click('.sseg button >> nth=3'); pg.wait_for_timeout(250); short=pg.inner_text('#shCnt')
    pg.click('.sseg button >> nth=5'); pg.wait_for_timeout(250); lng=pg.inner_text('#shCnt')
    chk(len(short)<len(med)<len(lng),'la lunghezza cambia il testo')
    pg.click('.sseg button >> nth=0'); pg.wait_for_timeout(250); chir=pg.inner_text('#shCnt')
    pg.click('.sseg button >> nth=2'); pg.wait_for_timeout(250); paz=pg.inner_text('#shCnt')
    chk(chir!=paz,'il tono cambia il testo')
    m=pg.inner_text('#shMeta')
    chk('#ginocchio' in m and 'GOOGLE' in m.upper(),'hashtag + parole chiave Google')
    pg.click('#shTabs button >> nth=1'); pg.wait_for_timeout(300)
    chk(pg.inner_text('#shMeta').count('#')==3,'LinkedIn: 3 hashtag')
    pg.click('#shTabs button >> nth=2'); pg.wait_for_timeout(250)
    chk(pg.inner_text('#shMeta').count('#')>=9,'Instagram: set esteso')
    # tutti e 4 gli articoli hanno le varianti
    n=pg.evaluate("()=>Object.keys(SOCV).length")
    chk(n==4,f'{n} lavori con varianti complete')
    tot=pg.evaluate("()=>{let c=0;for(const a in SOCV)for(const f in SOCV[a])c+=Object.keys(SOCV[a][f]).length;return c;}")
    chk(tot==48,f'{tot} testi generati (4 lavori x 4 formati x 3 toni)')
    chk(len(errs)==0,'nessun errore JavaScript')
    chk(pg.evaluate("()=>[...document.querySelectorAll('*')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&r.right>window.innerWidth+1}).length")==0,'niente fuori schermo')
    b.close()
print(f"== SOCIAL: {ok} verificati · {bad} errori ==")
sys.exit(1 if bad else 0)
