# -*- coding: utf-8 -*-
"""I salvati devono sopravvivere al ricambio quotidiano delle schede."""
import sys, os, json
sys.path.insert(0,'/home/claude/deploy/test')
from playwright.sync_api import sync_playwright
from comune import U, numeri
f=[]
def chk(n,c,e=""):
    print(("PASS " if c else "FAIL ")+n+(" :: "+str(e)[:150] if not c and e else ""))
    if not c: f.append(n)
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={"width":390,"height":900}); pg=ctx.new_page()
    errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    pg.goto(U); pg.wait_for_timeout(400)
    N=numeri(pg)
    QUANTI=min(3,len(N))
    for n in N[:QUANTI]: pg.evaluate(f"toggleSave(null,{n})")
    pg.wait_for_timeout(200)
    chk(f"{QUANTI} salvati oggi", pg.evaluate("savedList().length")==QUANTI)
    chk("fotografia conservata", pg.evaluate("(S.savedItems||[]).every(function(i){return i.a&&i.a.pmid&&i.a.h})"))
    pmids=pg.evaluate("(S.savedItems||[]).map(function(i){return i.a.pmid})")
    chk("stella accesa sulle schede", pg.locator(".ib.save.on").count()>=QUANTI, pg.locator(".ib.save.on").count())

    # DOMANI: le schede cambiano tutte
    pg.evaluate("""() => {
      ARTICLES.length=0; for(var k in A) delete A[k];
      for(var i=0;i<4;i++){var a={n:90+i,mono:'m-x',j:'X',dot:'green',sec:'res',h:'Lavoro di domani '+i,v:'v',ax:'Y',date:'ago 2026',meta:'m',pmid:'8800'+i,doi:'10/x',journal:'X',authors:'Y',design:'d',pop:'p',results:'MD 1,0 (p=0,04)',concl:'c',limits:'l',perte:'p'};ARTICLES.push(a);A[a.n]=a;}
      render();
    }""")
    pg.wait_for_timeout(300)
    chk("l'app non va in errore il giorno dopo", len(errs)==0, errs[:2])
    pg.click("button:has-text('Salvati')"); pg.wait_for_timeout(300)
    chk(f"{QUANTI} salvati ancora presenti domani", pg.evaluate("savedList().length")==QUANTI)
    chk("le schede salvate si vedono", pg.locator("#savedList .item").count()==QUANTI, pg.locator("#savedList .item").count())
    chk("contatore corretto", pg.inner_text("#savedCount")==str(QUANTI))
    txt=pg.inner_text("#savedList")
    chk("i titoli di ieri sono ancora leggibili", len(txt)>100 and "Lavoro di domani" not in txt, txt[:80])
    chk("controllo ritrattazioni ancora attivo", "ritirato" in pg.inner_text("#retrbox").lower())
    pg.fill("#savedq","zzzz"); pg.wait_for_timeout(250)
    chk("ricerca nei salvati funziona ancora", "Nessun salvato corrisponde" in pg.inner_text("#savedList"))
    pg.fill("#savedq",""); pg.wait_for_timeout(250)
    # togliere uno dei salvati di ieri
    pg.evaluate("() => { S.savedItems.splice(0,1); save(); render(); }")
    pg.wait_for_timeout(200)
    chk("si può togliere un salvato di ieri", pg.evaluate("savedList().length")==QUANTI-1)
    chk("nessun errore JavaScript in tutto il percorso", len(errs)==0, errs[:2])
    b.close()
print("\n"+("TUTTO OK" if not f else f"{len(f)} FALLITI: {f}"))
sys.exit(1 if f else 0)
