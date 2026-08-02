# -*- coding: utf-8 -*-
import sys,json
from playwright.sync_api import sync_playwright
fails=[]
def chk(n,c,e=""):
    print(("PASS " if c else "FAIL ")+n+(" :: "+str(e)[:200] if not c and e else ""))
    if not c: fails.append(n)
import os
_H=os.environ.get('PULSE_HTML') or os.path.abspath('index.html')
U='file://'+_H
with sync_playwright() as p:
    b=p.chromium.launch()
    # --- A. utente nuovo
    ctx=b.new_context(viewport={"width":390,"height":900}); pg=ctx.new_page()
    errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    pg.goto(U); pg.wait_for_timeout(400)
    st=pg.evaluate("({j:S.journals,k:S.kols,s:S.societies,c:S.companies,v:S.prefv})")
    chk("nuovo: 10 riviste", len(st["j"])==10, st["j"])
    chk("nuovo: 21 opinion leader", len(st["k"])==21, len(st["k"]))
    chk("nuovo: 14 società", len(st["s"])==14, len(st["s"]))
    chk("nuovo: 8 aziende", len(st["c"])==8, st["c"])
    chk("nessun doppione nelle liste iniziali",
        all(len(x)==len(set(x)) for x in [st["j"],st["k"],st["s"],st["c"]]))
    for nome in ["ESSKA","SFA","SOFCOT","AGA","BASK","SIAGASCOT","swiss orthopaedics","FMH","AOSSM","AAOS","APKASS (Asia)"]:
        chk("società "+nome, nome in st["s"])
    for nome in ["Marcheggiani Muccioli","Grassi","Bonanzinga","Kon","Marcacci","Bait","Andriolo","Petersen","Zantop","Andy Williams (Fortius)","Helito","Franciozi","Musahl (Pittsburgh)","LaPrade","Rodeo","Mayo Clinic","Della Villa (Isokinetic)","D'Ambrosi"]:
        chk("kol "+nome, nome in st["k"])
    for nome in ["KSSTA","JEO","AJSM","Arthroscopy","OJSM","JBJS","The Knee","BJSM"]:
        chk("rivista "+nome, nome in st["j"])
    for nome in ["DePuy Synthes","Zimmer Biomet","Smith & Nephew","Arthrex","Stryker","Medacta","Lima","aziende innovative e asiatiche"]:
        chk("azienda "+nome, nome in st["c"])
    pg.click("button:has-text('Impostazioni')"); pg.wait_for_timeout(250)
    chk("sezione Aziende visibile", pg.locator("#setAz .tag").count()==8, pg.locator("#setAz .tag").count())
    chk("link alle versioni", pg.locator("a[href='versioni/']").count()==1)
    chk("aziende nel riquadro In focus", "Medacta" in pg.inner_text("#focusMore"))
    ctx.close()

    # --- B. utente che ha GIÀ uno stato salvato (il caso vero: il suo iPhone)
    ctx2=b.new_context(viewport={"width":390,"height":900}); pg2=ctx2.new_page()
    errs2=[]; pg2.on("pageerror",lambda e:errs2.append(str(e)))
    pg2.goto(U); pg2.wait_for_timeout(300)
    PRIMO = pg2.evaluate("ARTICLES[0].n")   # i numeri cambiano ogni mattina
    vecchio={"saved":[2,4],"votes":{"1":1},"seen":[1,2],
             "journals":["AJSM","KSSTA","Rivista sua"],
             "kols":["D'Ambrosi","Un suo nome"],
             "societies":["ESSKA","Una sua società"],
             "weekly":[{"n":PRIMO,"d":"2026-08-02","v":"https://youtu.be/x","a":{"h":"T","j":"J","date":"d","pmid":"1","v":"v"},"b":{"prof":["a","b","c"],"paz":["a","b","c"]}}],
             "winLit":45,"suggIdx":3}
    pg2.evaluate("v => localStorage.setItem('pulse4', JSON.stringify(v))", vecchio)
    pg2.reload(); pg2.wait_for_timeout(500)
    s2=pg2.evaluate("({j:S.journals,k:S.kols,s:S.societies,c:S.companies,v:S.prefv,sv:S.saved,vo:S.votes,w:S.weekly,wl:S.winLit,si:S.suggIdx})")
    chk("migrazione: salvataggi intatti", s2["sv"]==[2,4], s2["sv"])
    chk("migrazione: voti intatti", s2["vo"]=={"1":1}, s2["vo"])
    chk("migrazione: newsletter intatta", len(s2["w"])==1 and s2["w"][0]["v"]=="https://youtu.be/x")
    chk("migrazione: finestra 45 gg conservata", s2["wl"]==45)
    chk("migrazione: indice proposte conservato", s2["si"]==3)
    chk("migrazione: le sue voci restano", "Rivista sua" in s2["j"] and "Un suo nome" in s2["k"] and "Una sua società" in s2["s"])
    chk("migrazione: le nuove sono state unite", "SOFCOT" in s2["s"] and "Helito" in s2["k"] and "JEO" in s2["j"])
    chk("migrazione: nessun doppione", len(s2["j"])==len(set(s2["j"])) and len(s2["k"])==len(set(s2["k"])) and len(s2["s"])==len(set(s2["s"])))
    chk("migrazione: aziende create", len(s2["c"])==8)
    chk("migrazione: marcatore alzato", s2["v"]==2)
    # C. ciò che toglie deve restare tolto
    pg2.evaluate("rm('societies','SOFCOT')"); pg2.wait_for_timeout(200)
    pg2.reload(); pg2.wait_for_timeout(500)
    s3=pg2.evaluate("S.societies")
    chk("ciò che toglie resta tolto dopo il riavvio", "SOFCOT" not in s3, [x for x in s3 if 'SOF' in x])
    chk("nessun errore JS", len(errs)==0 and len(errs2)==0, (errs[:2],errs2[:2]))
    ctx2.close(); b.close()
print("\n"+("TUTTO OK" if not fails else f"{len(fails)} FALLITI: {fails}"))
sys.exit(1 if fails else 0)
