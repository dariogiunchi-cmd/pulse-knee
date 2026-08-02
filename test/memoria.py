import sys
from playwright.sync_api import sync_playwright
import os
_H=os.environ.get('PULSE_HTML') or os.path.abspath('index.html')
_U='file://'+_H
fails=[]
def chk(n,c,e=""):
    print(("PASS " if c else "FAIL ")+n+(" :: "+str(e) if not c and e else ""))
    if not c: fails.append(n)
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={"width":390,"height":800}); pg=ctx.new_page()
    errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    pg.goto(_U); pg.wait_for_timeout(400)
    for n in [2,1,4,5]: pg.evaluate(f"pickWeek(null,{n})")
    pg.wait_for_timeout(150)
    pg.evaluate("setVid(0,'https://youtu.be/W1')")
    snap=pg.evaluate("JSON.parse(JSON.stringify(S.weekly))")
    chk("snapshot articolo salvato", all(w.get('a') and w['a'].get('pmid') for w in snap), snap[:1])
    chk("snapshot blurb salvato", all(w.get('b') and w['b'].get('prof') for w in snap))
    pmids=[w['a']['pmid'] for w in snap]

    # SIMULA IL GIORNO DOPO: articoli completamente diversi, ARTICLES svuotato
    pg.evaluate("""() => {
      ARTICLES.length=0; for(var k in A) delete A[k];
      for(var k in NLB) delete NLB[k];
      ARTICLES.push({n:77,mono:'m-x',j:'X',dot:'green',sec:'res',h:'Nuovo lavoro di domani',v:'x',ax:'Y',date:'ago 2026',meta:'x',pmid:'99999999',doi:'10/x',journal:'X',authors:'Y',design:'d',pop:'p',results:'r',concl:'c',limits:'l',perte:'p'});
      A[77]=ARTICLES[0];
      renderNl();
    }""")
    pg.wait_for_timeout(200)
    pg.click("button:has-text('✉️ Newsletter')"); pg.wait_for_timeout(250)
    chk("4 slot sopravvivono al ricambio quotidiano", pg.locator("#nlslots .nlnum.full").count()==4)
    t=pg.inner_text("#nlout")
    chk("testo ancora completo", t.startswith("OGGETTO: ") and "4 novità" in t, t[:60])
    for pm in pmids:
        chk("PMID "+pm+" ancora nel testo", pm in t)
    chk("blurb professionale conservato", "meta-analisi" in t.lower(), t[:200])
    chk("link video conservato", "https://youtu.be/W1" in t)
    chk("nessun undefined", "undefined" not in t)
    pg.click("#nlver button:has-text('Pazienti')"); pg.wait_for_timeout(200)
    tp=pg.inner_text("#nlout")
    chk("versione pazienti conservata", tp!=t and "spiegate semplice" in tp)
    # rimozione dopo il ricambio
    pg.locator("#nlslots .nlrm").first.click(); pg.wait_for_timeout(200)
    chk("si può ancora togliere", pg.evaluate("(S.weekly||[]).length")==3)
    chk("nessun errore JS", len(errs)==0, errs[:3])
    b.close()
print("\n"+("TUTTO OK" if not fails else f"{len(fails)} FALLITI: {fails}"))
sys.exit(1 if fails else 0)
