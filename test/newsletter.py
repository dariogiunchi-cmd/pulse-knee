import sys, re
from playwright.sync_api import sync_playwright
import os
_H=os.environ.get('PULSE_HTML') or os.path.abspath('index.html')
_U='file://'+_H
import sys as _sy; _sy.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from comune import con_nlb, numeri, salta

PATH = _U
fails = []
def chk(name, cond, extra=""):
    print(("PASS " if cond else "FAIL ") + name + (" :: "+str(extra) if not cond and extra else ""))
    if not cond: fails.append(name)

with sync_playwright() as p:
    b = p.chromium.launch()
    for theme in ["light", "dark"]:
        for w in [375, 390, 430]:
            ctx = b.new_context(viewport={"width": w, "height": 800},
                                color_scheme=theme, device_scale_factor=2)
            pg = ctx.new_page()
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
            pg.goto(PATH)
            pg.wait_for_timeout(400)

            tag = f"[{theme}/{w}] "
            SCELTI = con_nlb(pg, 4)
            TUTTI = numeri(pg)
            ALTRO = next((x for x in TUTTI if x not in SCELTI), None)
            if not SCELTI:
                salta("newsletter", "nessun lavoro con i testi pronti oggi")
                chk(tag+"la macchina della newsletter c'è comunque",
                    pg.evaluate("typeof nlText==='function' && typeof pickWeek==='function'"))
                ctx.close(); continue

            if theme == "light" and w == 390:
                # --- 1. Video button exists on every card
                nvid = pg.locator('.ib.vid').count()
                chk(tag+"pulsanti Video sulle schede", nvid >= 6, nvid)

                # --- 2. Newsletter tab exists
                chk(tag+"tab Newsletter", pg.locator("button:has-text('Newsletter')").count() == 1)

                # --- 3. empty state
                pg.click("button:has-text('Newsletter')")
                pg.wait_for_timeout(200)
                intro = pg.inner_text("#nlintro")
                chk(tag+"stato vuoto spiegato", "Come funziona" in intro, intro[:60])
                chk(tag+"4 slot vuoti", pg.locator("#nlslots .nlslot").count() == 4)
                out0 = pg.inner_text("#nlout")
                chk(tag+"testo vuoto istruttivo", "«Video»" in out0 and "blog" in out0, out0[:80])
                chk(tag+"contatore 0 di 4", pg.inner_text("#nlcount") == "0 di 4", pg.inner_text("#nlcount"))

                # --- 4. sceglie i lavori del giorno che hanno i testi (i numeri cambiano ogni mattina)
                pg.click("button:has-text('Oggi')")
                pg.wait_for_timeout(150)
                for n in SCELTI:
                    pg.evaluate(f"pickWeek(null,{n})")
                pg.wait_for_timeout(200)
                w4 = pg.evaluate("(S.weekly||[]).map(function(x){return x.n})")
                chk(tag+f"{len(SCELTI)} lavori scelti", w4 == SCELTI, (w4, SCELTI))

                # --- 5. oltre il quarto viene rifiutato (solo se oggi ce n'è un quinto)
                if len(SCELTI) == 4 and ALTRO is not None:
                    pg.evaluate(f"pickWeek(null,{ALTRO})")
                    cnt5 = pg.evaluate("(S.weekly||[]).length")
                    chk(tag+"il quinto viene rifiutato", cnt5 == 4, cnt5)
                else:
                    salta("limite di quattro", "oggi non ci sono abbastanza lavori per provarlo")

                # --- 6. video buttons turn on
                on = pg.locator('.ib.vid.on').count()
                chk(tag+f"{len(SCELTI)} pulsanti Video accesi", on == len(SCELTI), on)

                # --- 7. newsletter view filled
                pg.click("button:has-text('Newsletter')")
                pg.wait_for_timeout(200)
                chk(tag+f"{len(SCELTI)} slot pieni", pg.locator("#nlslots .nlnum.full").count() == len(SCELTI))
                chk(tag+f"contatore {len(SCELTI)} di 4", pg.inner_text("#nlcount") == f"{len(SCELTI)} di 4")
                chk(tag+"un campo link video per slot", pg.locator("#nlslots .nlvid").count() == len(SCELTI))

                # --- 8. output structure
                t = pg.inner_text("#nlout")
                chk(tag+"OGGETTO presente", t.startswith("OGGETTO: "), t[:40])
                chk(tag+"ANTEPRIMA presente", "ANTEPRIMA: " in t)
                chk(tag+f"{len(SCELTI)} punti numerati", all((f"\n{i}. " in t or t.startswith(f"{i}. ")) for i in range(1, len(SCELTI)+1)))
                pmids = re.findall(r"pubmed\.ncbi\.nlm\.nih\.gov/(\d+)/", t)
                chk(tag+f"{len(SCELTI)} link PubMed", len(pmids) == len(SCELTI), pmids)
                real = pg.evaluate("(S.weekly||[]).map(function(x){return A[x.n].pmid})")
                chk(tag+"PMID corrispondono agli articoli", pmids == real, (pmids, real))
                chk(tag+"nessun ** markdown", "**" not in t)
                chk(tag+"firma presente", "Dario Giunchi" in t)
                chk(tag+"nessun undefined/null", "undefined" not in t and "null" not in t)

                # --- 9. toggle version
                prof = t
                pg.click("#nlver button:has-text('Pazienti')")
                pg.wait_for_timeout(200)
                paz = pg.inner_text("#nlout")
                chk(tag+"versione pazienti diversa", paz != prof and len(paz) > 200)
                chk(tag+"oggetto pazienti dedicato", "spiegate semplice" in paz, paz[:70])
                chk(tag+"tono paziente (no 'colleghe')", "Gentili colleghe" not in paz)
                pg.click("#nlver button:has-text('Professionisti')")
                pg.wait_for_timeout(150)
                chk(tag+"ritorno a professionisti", pg.inner_text("#nlout") == prof)

                # --- 10. video link flows into text
                pg.locator("#nlslots .nlvid").first.fill("https://youtu.be/TEST123")
                pg.wait_for_timeout(250)
                t2 = pg.inner_text("#nlout")
                chk(tag+"link video nel testo", "https://youtu.be/TEST123" in t2)
                chk(tag+"etichetta commento video", "Il mio commento in video" in t2)

                # --- 11. persistence across reload
                pg.reload(); pg.wait_for_timeout(400)
                pg.click("button:has-text('Newsletter')"); pg.wait_for_timeout(200)
                chk(tag+"stato salvato dopo ricarica", pg.locator("#nlslots .nlnum.full").count() == len(SCELTI))
                chk(tag+"link video salvato", "TEST123" in pg.inner_text("#nlout"))

                # --- 12. remove one
                pg.locator("#nlslots .nlrm").first.click()
                pg.wait_for_timeout(250)
                resta = len(SCELTI) - 1
                chk(tag+"rimozione funziona", pg.evaluate("(S.weekly||[]).length") == resta)
                chk(tag+f"contatore aggiornato a {resta}", pg.inner_text("#nlcount") == f"{resta} di 4")
                if resta:
                    chk(tag+f"testo aggiornato a {resta}", f"{resta} novità" in pg.inner_text("#nlout"))
                pg.evaluate(f"pickWeek(null,{SCELTI[0]})")
                pg.wait_for_timeout(150)
            else:
                # seed state for layout checks
                pg.evaluate("ns => { S.weekly=[]; ns.forEach(function(n){ pickWeek(null,n) }); if(S.weekly[0]) S.weekly[0].v='https://youtu.be/abc'; save(); render(); }", SCELTI)
                pg.wait_for_timeout(200)

            # --- layout: nothing overflows on the newsletter view
            pg.click("button:has-text('Newsletter')")
            pg.wait_for_timeout(250)
            ow = pg.evaluate("""() => {
              var bad=[]; var vw=document.documentElement.clientWidth;
              document.querySelectorAll('#news *').forEach(function(e){
                var r=e.getBoundingClientRect();
                if(r.width>0 && (r.right>vw+1||r.left<-1)) bad.push(e.className+'|'+Math.round(r.left)+'-'+Math.round(r.right));
              });
              return {vw:vw, sw:document.documentElement.scrollWidth, bad:bad.slice(0,5)};
            }""")
            chk(tag+"niente esce dallo schermo", len(ow["bad"]) == 0, ow)
            chk(tag+"nessuno scroll orizzontale", ow["sw"] <= ow["vw"] + 1, ow)

            # --- contrast: nlout text vs background
            col = pg.evaluate("""() => {
              var o=document.getElementById('nlout'); var cs=getComputedStyle(o);
              return {c:cs.color, b:cs.backgroundColor};
            }""")
            def lum(rgb):
                v = [int(x)/255 for x in re.findall(r"\d+", rgb)[:3]]
                v = [c/12.92 if c <= .03928 else ((c+.055)/1.055)**2.4 for c in v]
                return .2126*v[0]+.7152*v[1]+.0722*v[2]
            l1, l2 = lum(col["c"]), lum(col["b"])
            ratio = (max(l1,l2)+.05)/(min(l1,l2)+.05)
            chk(tag+"contrasto testo newsletter >=4.5", ratio >= 4.5, f"{ratio:.2f} {col}")

            # --- video input readable / no iOS zoom
            fs = pg.evaluate("""() => { var i=document.querySelector('.nlvid'); return i?parseFloat(getComputedStyle(i).fontSize):0 }""")
            chk(tag+"input video >=16px (no zoom iOS)", fs >= 16, fs)

            # --- tabs wrap, all 5 reachable
            tb = pg.evaluate("""() => {
              var vw=document.documentElement.clientWidth; var bad=[];
              document.querySelectorAll('.tabs button').forEach(function(b){
                var r=b.getBoundingClientRect(); if(r.right>vw+1||r.left<-1) bad.push(b.textContent.trim());
              });
              return {n:document.querySelectorAll('.tabs button').length, bad:bad};
            }""")
            chk(tag+"tutte le tab visibili", tb["n"] >= 5 and len(tb["bad"]) == 0, tb)

            # --- tap target size
            tt = pg.evaluate("""() => {
              var bad=[];
              document.querySelectorAll('#news button, #news .nlrm, .ib.vid').forEach(function(e){
                var r=e.getBoundingClientRect(); if(r.width>0&&r.height<28) bad.push(e.textContent.trim()+':'+Math.round(r.height));
              });
              return bad;
            }""")
            chk(tag+"bersagli tattili >=28px", len(tt) == 0, tt)

            chk(tag+"nessun errore JS", len(errs) == 0, errs[:3])
            ctx.close()
    b.close()

print("\n" + ("TUTTO OK" if not fails else f"{len(fails)} FALLITI: {fails}"))
sys.exit(1 if fails else 0)
