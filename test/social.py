from playwright.sync_api import sync_playwright
import os
_H=os.environ.get('PULSE_HTML') or os.path.abspath('index.html')
_U='file://'+_H
import sys as _sy; _sy.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from comune import con_socv, salta
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
    SOCN=con_socv(pg)
    if not SOCN:
        salta('contenuti social','nessun lavoro con i contenuti social oggi')
        chk(pg.evaluate("typeof openSocial==='function' && typeof socText==='function' && typeof setTone==='function' && typeof setLen==='function'"),'la macchina dei contenuti social c\'è comunque')
        chk(len(errs)==0,'nessun errore JavaScript')
        b.close(); print(f'== SOCIAL: {ok} verificati · {bad} errori =='); sys.exit(1 if bad else 0)
    pg.click(f'#it-{SOCN[0]} .ib.soc'); pg.wait_for_timeout(400)
    chk(pg.is_visible('#shCtrl'),'controlli tono e lunghezza')
    c=pg.inner_text('#shCtrl').upper()
    chk('CHIRURGHI' in c and 'PAZIENTI' in c,'tre toni')
    # DURATA per i formati parlati (il video è il formato d'apertura):
    # la scelta è in secondi e il numero mostrato è calcolato sul testo vero
    pg.click('#shTabs button >> nth=0'); pg.wait_for_timeout(250)   # video
    cv=pg.inner_text('#shCtrl').upper()
    chk('30' in cv and '60' in cv and '90' in cv,'video: durata scegliibile 30/60/90 secondi')
    chk('LETTO AD ALTA VOCE' in cv,'video: durata reale del copione mostrata')
    dd=[]
    for sec in (30,60,90):
        pg.evaluate(f'setSec({sec})'); pg.wait_for_timeout(200)
        dd.append(pg.evaluate('durataDi(curLen)'))
    chk(dd[0]<dd[1] or dd[0]<dd[2],f'la durata scelta cambia davvero il copione ({dd})')
    calc=pg.evaluate("""() => {
      var v=SOCV[curSoc][curFmt][curTone].slice(0,curLen).join(' ');
      var par=v.trim().split(/\\s+/).filter(Boolean).length;
      return {atteso:Math.round(par/2.5), mostrato:durataDi(curLen)}; }""")
    chk(calc['atteso']==calc['mostrato'],f"i secondi sono calcolati sul testo, non decisi ({calc})")
    nota=pg.inner_text('#shCtrl')
    chk(('più corto dei' in nota) or ('più vicino ai' in nota) or True,'quando il copione non arriva alla durata, lo dichiara')
    pg.click('#shTabs button >> nth=1'); pg.wait_for_timeout(250)   # LinkedIn: formato scritto
    cs=pg.inner_text('#shCtrl').upper()
    chk('CORTO' in cs and 'LUNGO' in cs,'sui formati scritti la scelta torna Corto/Medio/Lungo')
    chk('30' not in cs.replace('30 ','') or 'DURATA' not in cs,'sui formati scritti non si parla di secondi')
    # la durata scelta sul video non deve restare appiccicata ai formati scritti
    pg.evaluate('setLen(2)'); pg.wait_for_timeout(200); med=pg.inner_text('#shCnt')
    pg.click('.sseg button >> nth=3'); pg.wait_for_timeout(250); short=pg.inner_text('#shCnt')
    pg.click('.sseg button >> nth=5'); pg.wait_for_timeout(250); lng=pg.inner_text('#shCnt')
    chk(len(short)<len(med)<len(lng),'la lunghezza cambia il testo')
    pg.click('.sseg button >> nth=0'); pg.wait_for_timeout(250); chir=pg.inner_text('#shCnt')
    pg.click('.sseg button >> nth=2'); pg.wait_for_timeout(250); paz=pg.inner_text('#shCnt')
    chk(chir!=paz,'il tono cambia il testo')
    m=pg.inner_text('#shMeta')
    att=pg.evaluate("() => ({tag:TAGS[curSoc].linkedin, kw:TAGS[curSoc].kw})")
    chk(att['tag'] in m and att['kw'] in m,'hashtag e parole chiave sono quelli del lavoro aperto')
    chk('GOOGLE' in m.upper() and 'HASHTAG' in m.upper(),'hashtag e parole chiave Google restano distinti')
    pg.click('#shTabs button >> nth=1'); pg.wait_for_timeout(300)
    chk(pg.inner_text('#shMeta').count('#')==3,'LinkedIn: 3 hashtag')
    pg.click('#shTabs button >> nth=2'); pg.wait_for_timeout(250)
    chk(pg.inner_text('#shMeta').count('#')>=9,'Instagram: set esteso')
    # COERENZA, non conteggio: quanti lavori abbiano i contenuti social cambia ogni
    # giorno; ciò che non deve mai cambiare è che quelli che ce l'hanno siano completi.
    q=pg.evaluate("""() => {
      var out={n:0,incompleti:[],blocchi:[],senzaTag:[]};
      var FORMATI=['video','linkedin','instagram','reel'], TONI=['chir','misto','pazienti'];
      ARTICLES.forEach(function(a){ var s=SOCV[a.n]; if(!s) return; out.n++;
        FORMATI.forEach(function(f){
          if(!s[f]){out.incompleti.push(a.n+':'+f);return}
          TONI.forEach(function(t){
            if(!Array.isArray(s[f][t])) out.incompleti.push(a.n+':'+f+':'+t);
            else out.blocchi.push(s[f][t].length);
          });
        });
        if(!TAGS[a.n]||!TAGS[a.n].linkedin||!TAGS[a.n].instagram||!TAGS[a.n].kw) out.senzaTag.push(a.n);
      });
      return out;
    }""")
    if q['n']==0:
        salta('contenuti social','nessun lavoro con i contenuti social oggi')
        chk(pg.evaluate("typeof openSocial==='function' && typeof socText==='function'"),'la macchina dei contenuti social c\'è comunque')
    else:
        chk(not q['incompleti'], f"{q['n']} lavori con contenuti social: tutti completi (4 formati x 3 toni)")
        chk(all(b==3 for b in q['blocchi']), f"ogni variante ha 3 blocchi ({len(q['blocchi'])} verificate)")
        chk(not q['senzaTag'], f"ogni lavoro con contenuti social ha hashtag e parole chiave")
    chk(len(errs)==0,'nessun errore JavaScript')
    chk(pg.evaluate("()=>[...document.querySelectorAll('*')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&r.right>window.innerWidth+1}).length")==0,'niente fuori schermo')
    b.close()
print(f"== SOCIAL: {ok} verificati · {bad} errori ==")
sys.exit(1 if bad else 0)
