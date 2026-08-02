# -*- coding: utf-8 -*-
"""Trasferimento fra dispositivi: deve FONDERE, mai far perdere qualcosa."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
from comune import U, numeri, con_nlb
f=[]
def chk(n,c,e=""):
    print(("PASS " if c else "FAIL ")+n+(" :: "+str(e)[:180] if not c and e else ""))
    if not c: f.append(n)

with sync_playwright() as p:
    b=p.chromium.launch()
    # --- DISPOSITIVO A (telefono)
    ca=b.new_context(viewport={"width":390,"height":844}); A=ca.new_page()
    errsA=[]; A.on("pageerror", lambda e: errsA.append(str(e)))
    A.goto(U); A.wait_for_timeout(500)
    N=numeri(A); NL=con_nlb(A,4)
    A.evaluate("ns => ns.forEach(function(n){toggleSave(null,n)})", N[:3])
    A.evaluate("ns => ns.forEach(function(n){pickWeek(null,n)})", NL[:2])
    A.evaluate("acceptSugg()"); A.evaluate("dismissSugg()")
    A.evaluate("addItem2 = null; S.kols.push('Nome solo sul telefono'); S.votes[%d]=1; save();" % N[0])
    A.wait_for_timeout(200)
    link = A.evaluate("linkTrasferimento()")
    chk("il link si genera", link.startswith("file://") and "#stato=" in link, link[:60])
    chk("il link è sotto i 25 KB", len(link) < 25000, f"{len(link)//1024} KB")
    statoA = A.evaluate("({sv:savedList().length,w:(S.weekly||[]).length,k:S.kols.length,sd:Object.keys(S.suggDone).length})")

    # --- DISPOSITIVO B (computer): stato DIVERSO, non vuoto
    cb=b.new_context(viewport={"width":430,"height":900}); B=cb.new_page()
    errsB=[]; B.on("pageerror", lambda e: errsB.append(str(e)))
    B.goto(U); B.wait_for_timeout(500)
    B.evaluate("ns => ns.forEach(function(n){toggleSave(null,n)})", N[3:5])
    B.evaluate("S.kols.push('Nome solo sul computer'); S.societies.push('Società solo sul computer'); save(); render();")
    B.wait_for_timeout(200)
    primaB = B.evaluate("({sv:savedList().length,k:S.kols.length,soc:S.societies.length})")
    chk("i due dispositivi partono diversi", primaB["sv"] != statoA["sv"], (primaB, statoA))

    # --- apre il link sul dispositivo B
    B.goto(link); B.wait_for_timeout(700)
    dopoB = B.evaluate("({sv:savedList().length,w:(S.weekly||[]).length,k:S.kols,soc:S.societies,sd:Object.keys(S.suggDone).length,vo:S.votes})")
    chk("i salvati si sommano, non si sostituiscono", dopoB["sv"] == 5, (dopoB["sv"], statoA["sv"], primaB["sv"]))
    chk("i lavori scelti arrivano dal telefono", dopoB["w"] == 2, dopoB["w"])
    chk("quello che c'era solo sul computer resta", "Nome solo sul computer" in dopoB["k"] and "Società solo sul computer" in dopoB["soc"])
    chk("quello che c'era solo sul telefono arriva", "Nome solo sul telefono" in dopoB["k"])
    chk("le proposte già risposte non tornano", dopoB["sd"] == 2, dopoB["sd"])
    chk("i voti arrivano", str(N[0]) in dopoB["vo"] or N[0] in dopoB["vo"])
    chk("il link sparisce dalla barra", "#stato=" not in B.evaluate("location.href"))
    chk("nessun doppione fra le preferenze", len(dopoB["k"]) == len(set(dopoB["k"])))

    # --- riapre lo stesso link: idempotente
    B.goto(link); B.wait_for_timeout(700)
    di_nuovo = B.evaluate("savedList().length")
    chk("riaprire lo stesso link non duplica nulla", di_nuovo == 5, di_nuovo)

    # --- persistenza
    B.goto(U); B.wait_for_timeout(600)
    chk("la fusione resta dopo la chiusura", B.evaluate("savedList().length") == 5)

    # --- link rovinato: non deve azzerare nulla
    B.goto(U.split('#')[0] + "#stato=xxxNONVALIDOxxx"); B.wait_for_timeout(600)
    chk("un link rovinato non cancella i dati", B.evaluate("savedList().length") == 5)
    chk("nessun errore JavaScript", len(errsA)==0 and len(errsB)==0, (errsA[:2], errsB[:2]))

    # --- la sezione è visibile e spiega che non c'è sincronizzazione automatica
    B.goto(U); B.wait_for_timeout(500)
    B.click("button:has-text('Impostazioni')"); B.wait_for_timeout(300)
    t = B.inner_text("#settings")
    chk("l'app dichiara che non c'è un server", "non ha un server" in t)
    chk("l'app dice che le copie si fondono", "fondono" in t)
    chk("c'è il pulsante per copiare il link", B.locator("#syncbox button").count() >= 1)
    b.close()
print("\n" + ("TUTTO OK" if not f else f"{len(f)} FALLITI: {f}"))
sys.exit(1 if f else 0)
