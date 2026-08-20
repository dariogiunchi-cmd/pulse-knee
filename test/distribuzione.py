# -*- coding: utf-8 -*-
import sys,re
from playwright.sync_api import sync_playwright
import os
_H=os.environ.get('PULSE_HTML') or os.path.abspath('index.html')
_U='file://'+_H
import sys as _sy; _sy.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from comune import con_nlb, numeri, salta
PATH=_U
fails=[]
def chk(n,c,e=""):
    print(("PASS " if c else "FAIL ")+n+(" :: "+str(e)[:220] if not c and e else ""))
    if not c: fails.append(n)
with sync_playwright() as p:
    b=p.chromium.launch()
    for theme in ["light","dark"]:
      for w in [375,390,430]:
        ctx=b.new_context(viewport={"width":w,"height":900},color_scheme=theme)
        pg=ctx.new_page(); errs=[]
        pg.on("pageerror",lambda e:errs.append(str(e)))
        pg.on("console",lambda m:errs.append(m.text) if m.type=="error" else None)
        pg.goto(PATH); pg.wait_for_timeout(400)
        tag=f"[{theme}/{w}] "
        SCELTI=con_nlb(pg,4)
        if not SCELTI:
            salta("blog e Google","nessun lavoro con i testi pronti oggi")
            chk(tag+"la macchina c'è comunque", pg.evaluate("typeof blogText==='function' && typeof gbpText==='function'"))
            ctx.close(); continue
        for n in SCELTI: pg.evaluate(f"pickWeek(null,{n})")
        pg.wait_for_timeout(200)
        pg.evaluate("tab('news')")
        pg.wait_for_timeout(250)

        if theme=="light" and w==390:
            chk(tag+"3 destinazioni", pg.locator("#nldest button").count()==3)
            # EMAIL
            t=pg.inner_text("#nlout")
            chk(tag+"email: OGGETTO", t.startswith("OGGETTO: "))
            chk(tag+"email: versione visibile", pg.locator("#nlver").is_visible())
            chk(tag+"email: campo url nascosto", not pg.locator("#gbpurlbox").is_visible())
            # BLOG
            # TRE registri, non due
            chk(tag+"tre versioni disponibili", pg.locator("#nlver button").count()==3, pg.locator("#nlver button").count())
            pg.click("#nlver button:has-text('Misto')"); pg.wait_for_timeout(250)
            mx=pg.inner_text("#nlout")
            chk(tag+"email: versione mista distinta", mx.startswith("OGGETTO: ") and "in chiaro" in mx, mx[:70])
            chk(tag+"misto: né gergo da collega né tono da paziente", "Gentili colleghe" not in mx and "spiegate semplice" not in mx)
            chk(tag+"misto: il limite resta dichiarato", any(k in mx.lower() for k in ["limite","osservazional","campione","non dimostra","sottopotent","piccol"]), mx[:200])
            pg.click("#nlver button:has-text('Professionisti')"); pg.wait_for_timeout(200)
            pg.click("#nldest button:has-text('Blog')"); pg.wait_for_timeout(250)
            bl=pg.inner_text("#nlout")
            for k in ["TITOLO DELLA PAGINA","DESCRIZIONE PER GOOGLE","INDIRIZZO DELLA PAGINA","PAROLE CHIAVE","INCOLLA NEL BLOG","## In breve"]:
                chk(tag+"blog: "+k, k in bl)
            chk(tag+"blog: un sottotitolo per lavoro + «In breve»", bl.count("\n## ")>=len(SCELTI)+1, bl.count("\n## "))
            chk(tag+f"blog: {len(SCELTI)} fonti PubMed", len(re.findall(r"pubmed\.ncbi\.nlm\.nih\.gov/\d+/",bl))==len(SCELTI))
            chk(tag+"blog: slug pulito", re.search(r"\n([a-z0-9-]+)\n\nPAROLE",bl) is not None, bl[:400])
            slug=re.search(r"\n([a-z0-9-]+)\n\nPAROLE",bl).group(1)
            chk(tag+"blog: slug senza accenti/spazi", re.fullmatch(r"[a-z0-9-]+",slug) is not None, slug)
            chk(tag+"blog: parole chiave presenti", len(bl.split("PAROLE CHIAVE")[1].split("\n")[1].strip())>10)
            chk(tag+"blog: disclaimer", "non sostituisce una valutazione clinica" in bl)
            chk(tag+"blog: firma FMH", "specialista FMH" in bl)
            chk(tag+"blog: niente **", "**" not in bl)
            chk(tag+"blog: niente undefined", "undefined" not in bl)
            desc=bl.split("\n")[4]
            chk(tag+"blog: meta description <=170", len(desc)<=170, len(desc))
            tit=bl.split("\n")[1]
            chk(tag+"blog: titolo <=65", len(tit)<=65, (len(tit),tit))
            # blog cambia con la versione
            pg.click("#nlver button:has-text('Pazienti')"); pg.wait_for_timeout(250)
            blp=pg.inner_text("#nlout")
            chk(tag+"blog: versione pazienti diversa", blp!=bl)
            chk(tag+"blog: pazienti senza gergo 'sottopotente'", "sottopotente" not in blp)
            pg.click("#nlver button:has-text('Professionisti')"); pg.wait_for_timeout(200)
            # GOOGLE
            pg.click("#nldest button:has-text('Google')"); pg.wait_for_timeout(250)
            g=pg.inner_text("#nlout")
            chk(tag+"google: versione nascosta", not pg.locator("#nlver").is_visible())
            chk(tag+"google: campo url visibile", pg.locator("#gbpurlbox").is_visible())
            chk(tag+"google: <=1500 caratteri", len(g)<=1500, len(g))
            chk(tag+"google: contatore mostrato", "/ 1500 caratteri" in pg.inner_text("#nlmeta"), pg.inner_text("#nlmeta"))
            chk(tag+"google: contatore verde", pg.locator("#nlmeta .okc").count()==1)
            chk(tag+f"google: {len(SCELTI)} righe elenco", g.count("\n• ")==len(SCELTI), g.count("\n• "))
            chk(tag+"google: url del blog", "dariogiunchi.ch/blog" in g)
            chk(tag+"google: senso nei primi 100", "ginocchio" in g[:100], g[:100])
            chk(tag+"google: niente **", "**" not in g)
            # NIENTE PUBBLICITA' (LPMed art.40 / LSan art.70)
            vietate=["prenota","chiama ora","sconto","gratis","gratuito","offerta","il migliore","garantito","senza rischi","risultato garantito","promozione","approfitta"]
            for txt,lbl in [(g,"google"),(bl,"blog"),(pg.evaluate("(function(){var d=nlDest;nlDest='mail';var x=outText();nlDest=d;return x})()"),"email")]:
                low=txt.lower()
                bad=[v for v in vietate if v in low]
                chk(tag+lbl+": nessun linguaggio pubblicitario", not bad, bad)
            # url personalizzato
            pg.fill("#gbpurl","https://www.dariogiunchi.ch/post/ginocchio-agosto")
            pg.wait_for_timeout(250)
            chk(tag+"google: url personalizzato usato", "post/ginocchio-agosto" in pg.inner_text("#nlout"))
            pg.reload(); pg.wait_for_timeout(400)
            pg.evaluate("tab('news')"); pg.wait_for_timeout(200)
            pg.click("#nldest button:has-text('Google')"); pg.wait_for_timeout(250)
            chk(tag+"google: url ricordato dopo ricarica", "post/ginocchio-agosto" in pg.inner_text("#nlout"))
            chk(tag+"google: campo ripopolato", pg.input_value("#gbpurl").endswith("ginocchio-agosto"))
            # limite duro: testi lunghissimi
            over=pg.evaluate("""() => {
              (S.weekly||[]).forEach(function(w){ w.b={prof:['P'.repeat(400),'x','y'],paz:['Z'.repeat(400),'x','y']} });
              nlDest='gbp'; var t=gbpText(); return {len:t.length, tail:t.slice(-200)};
            }""")
            chk(tag+"google: taglia se supera 1500", over["len"]<=1500, over["len"])
            chk(tag+"google: url resta anche dopo il taglio", "dariogiunchi.ch" in over["tail"], over["tail"])
            pg.reload(); pg.wait_for_timeout(400)
            pg.evaluate("tab('news')"); pg.wait_for_timeout(200)

        # layout su tutte le destinazioni
        for dest,label in [("mail","Email"),("blog","Blog"),("gbp","Google")]:
            pg.click(f"#nldest button:has-text('{label}')"); pg.wait_for_timeout(250)
            ow=pg.evaluate("""() => { var bad=[],vw=document.documentElement.clientWidth;
              document.querySelectorAll('#news *').forEach(function(e){var r=e.getBoundingClientRect();
              if(r.width>0&&(r.right>vw+1||r.left<-1))bad.push(e.className+'|'+Math.round(r.right));});
              return {vw:vw,sw:document.documentElement.scrollWidth,bad:bad.slice(0,4)};}""")
            chk(tag+label+": niente fuori schermo", len(ow["bad"])==0 and ow["sw"]<=ow["vw"]+1, ow)
            c=pg.evaluate("""() => {var o=document.getElementById('nlout');var s=getComputedStyle(o);return [s.color,s.backgroundColor]}""")
            def lum(r):
                v=[int(x)/255 for x in re.findall(r"\d+",r)[:3]]
                v=[x/12.92 if x<=.03928 else ((x+.055)/1.055)**2.4 for x in v]
                return .2126*v[0]+.7152*v[1]+.0722*v[2]
            l1,l2=lum(c[0]),lum(c[1]); ratio=(max(l1,l2)+.05)/(min(l1,l2)+.05)
            chk(tag+label+": contrasto >=4.5", ratio>=4.5, f"{ratio:.2f} {c}")
            chk(tag+label+": testo non vuoto", len(pg.inner_text("#nlout"))>150)
        tt=pg.evaluate("""() => {var bad=[];document.querySelectorAll('#news button,#news .nlrm').forEach(function(e){
          var r=e.getBoundingClientRect(); if(r.width>0&&r.height<28)bad.push(e.textContent.trim()+':'+Math.round(r.height));});return bad}""")
        chk(tag+"bersagli tattili >=28px", len(tt)==0, tt)
        chk(tag+"nessun errore JS", len(errs)==0, errs[:3])
        ctx.close()
    b.close()
print("\n"+("TUTTO OK" if not fails else f"{len(fails)} FALLITI: {fails}"))
sys.exit(1 if fails else 0)
