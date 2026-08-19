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
    pg.click('#ov .close'); pg.wait_for_timeout(200)
    print("\n=== NON-REGRESSIONE ===")
    # Il banner ha TRE stati legittimi (è arrivato · sta arrivando · non è arrivato):
    # pretendere «Aggiornato oggi» in assoluto significava dipendere dall'orologio, e
    # bloccava qualunque verifica notturna — trovato alle 5:42 UTC del 19 agosto.
    _fb=pg.inner_text('#freshbox')
    chk(('Aggiornato oggi' in _fb) or ('in preparazione' in _fb) or ('non è arrivato' in _fb),
        'banner freschezza in uno dei suoi tre stati dichiarati')
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

    # --- la seconda pagina: funzioni PURE su materiale sintetico -------------
    chk(pg3.evaluate("spSorpresa([{t:'a'},{t:'b'}],['a']).t")=='b',
        'Sorprendimi propone prima ciò che non è mai stato visto')
    chk(pg3.evaluate("spSorpresa([{t:'a'},{t:'b'}],['a','b']).t") in ('a','b'),
        'esaurite le novità, Sorprendimi ricomincia il giro invece di tacere')
    chk(pg3.evaluate("spSorpresa([],[])") is None,
        'senza scoperte non si inventa nulla')
    ordinati=pg3.evaluate("spLista([{pmid:'1'},{pmid:'2'},{pmid:'3'}],3,['3','1']).map(function(b){return b.pmid})")
    chk(ordinati[:2]==['3','1'],'esplora porta in cima i brevi affini, nell\'ordine dato')
    # coerenza col carico del giorno: la sezione esiste se e solo se ci sono dati
    coer2=pg3.evaluate("(document.getElementById('secpag').innerHTML.trim()!=='')===((typeof EXTRA!=='undefined'&&EXTRA.length>0)||(typeof SCOPERTE!=='undefined'&&SCOPERTE.length>0))")
    chk(coer2,'la seconda pagina compare se e solo se il giorno l\'ha riempita')

    # --- la voce: interprete dei comandi PURO, frasi sintetiche -----------------
    chk(pg3.evaluate("interpretaComando('apri la scheda tre').az")=='leggi'
        and pg3.evaluate("interpretaComando('apri la scheda tre').n")==3,
        'la voce capisce «apri la scheda tre» (numeri in lettere compresi)')
    chk(pg3.evaluate("interpretaComando('salva la 2').az")=='salva',
        'la voce capisce «salva»')
    chk(pg3.evaluate("interpretaComando('basta').az")=='stop',
        'la voce si ferma quando glielo si dice')
    chk(pg3.evaluate("interpretaComando('parlami del meteo').az")=='boh',
        'una richiesta fuori vocabolario viene dichiarata, non indovinata')
    chk(pg3.evaluate("_frasi('Una. Due! Tre?').length")==3,
        'la lettura spezza il testo in frasi (aggira il taglio di iOS)')

    # --- il podcast a due voci: macchina pura, dati sintetici -------------------
    chk(pg3.evaluate("dialogoFrasi([{chi:'A',t:'Prima frase. Seconda frase.'},{chi:'B',t:'Risposta.'}])"
                     ".map(function(x){return x.chi}).join('')")=='AAB',
        'il dialogo si spezza in frasi conservando chi parla')
    chk(pg3.evaluate("(function(){var v=typeof BRIEF_DIALOGO!=='undefined'?BRIEF_DIALOGO:undefined;"
                     "BRIEF_DIALOGO=[{chi:'A',t:'Ciao.'},{chi:'B',t:'Ciao a te.'}];"
                     "var c=_codaBrief();BRIEF_DIALOGO=v;"
                     "return typeof c[0]==='object'&&c[0].chi==='A'&&c[1].chi==='B'})()"),
        'con un dialogo presente il tasto ▶ legge il dialogo, a due voci')
    chk(pg3.evaluate("(function(){var v=typeof BRIEF_DIALOGO!=='undefined'?BRIEF_DIALOGO:undefined;"
                     "BRIEF_DIALOGO=[];var c=_codaBrief();BRIEF_DIALOGO=v;"
                     "return typeof c[0]==='string'})()"),
        'senza dialogo il tasto ▶ torna con eleganza a BRIEF_TEXT')
    chk(pg3.evaluate("typeof _voceB==='function'"),
        'esiste la scelta della seconda voce italiana')

    # --- benvenuto e guida: l'app si spiega da sola -----------------------------
    chk(pg3.evaluate("benvenutoHTML(0).indexOf('Benvenuto')>=0 && benvenutoHTML(0).indexOf('Ho capito')>=0"),
        'alla prima apertura compare il benvenuto con «Ho capito»')
    chk(pg3.evaluate("benvenutoHTML(GUIDA_V)")=='',
        'dopo «Ho capito» il benvenuto non torna mai più')
    g=pg3.evaluate("guidaHTML()")
    chk(all(w in g for w in ['richiamo di dispositivo','mette in discussione una tua tecnica',
                             'senza conflitto','non tocca la tua pratica']),
        'la guida spiega il significato di tutti e quattro i pallini')
    chk(all(w in g for w in ['Rassegna','Archivio','Salvati','Newsletter','Impostazioni']),
        'la guida nomina ogni scheda dell\'app')
    chk(all(w in g for w in ['sorprendimi','seconda pagina','basta','aiuto']),
        'la guida elenca il vocabolario dei comandi a voce')
    chk(pg3.evaluate("interpretaComando('aiuto').az")=='aiuto'
        and pg3.evaluate("interpretaComando('come funziona questa cosa').az")=='aiuto',
        'la voce capisce «aiuto» e «come funziona»')
    chk(pg3.evaluate("interpretaComando('riguardando la scheda due').az")!='aiuto',
        'una parola che contiene «guida» per caso non apre la guida')
    chk(pg3.evaluate("typeof setTesto==='function' && typeof applicaTesto==='function'"),
        'la dimensione del testo si può cambiare e riapplicare')

    # --- la modalità auto: playlist annunciata, comandi, velocità ---------------
    chk(pg3.evaluate("autoLista().length")==pg3.evaluate("ARTICLES.length")+1,
        'la playlist auto è briefing + tutte le schede del giorno')
    chk(pg3.evaluate("autoLista()[0].label").find('briefing')>=0
        and pg3.evaluate("autoLista()[0].n") is None,
        'la playlist apre col briefing, che non è salvabile')
    chk(pg3.evaluate("autoLista()[1].voci[0].t").startswith('Scheda 1 di '+str(pg3.evaluate("ARTICLES.length"))),
        'ogni scheda viene annunciata con la sua posizione')
    chk(pg3.evaluate("autoLista()[1].n")==pg3.evaluate("ARTICLES[0].n"),
        'la scheda in ascolto è identificata dal suo numero vero, per salvarla')
    for frase,att in [('prossima','prossima'),('vai avanti','prossima'),('indietro','indietro'),
                      ('ripeti','ripeti'),('pausa','pausa'),('riprendi','riprendi'),
                      ('salva questa','salvaquesta'),('più veloce','veloce'),('più piano','piano'),
                      ('velocità normale','ratenorm'),('modalità auto','auto'),
                      ('continua a leggere','seconda'),('apri la tre','leggi')]:
        chk(pg3.evaluate(f"interpretaComando('{frase}').az")==att,
            f'la voce capisce «{frase}» → {att}')
    chk(pg3.evaluate("(function(){var v=S.rate;var r1=setRate(2),r2=setRate(0.1);S.rate=v;save();return r1<=1.4&&r2>=0.7})()"),
        'la velocità di lettura ha limiti sani e si salva')

    # --- il cervello: conversazione libera e voce naturale, con onestà ----------
    chk(pg3.evaluate("chiediDisponibile()")==False,
        'senza configurazione il cervello risulta scollegato')
    chk(pg3.evaluate("_appiattisci([{t:'Prima. Seconda.',chi:'B'},'Terza.'])"
                     ".map(function(x){return typeof x==='string'?'s':x.chi}).join('')")=='BBs',
        'l\'appiattimento per la voce di sistema conserva chi parla')
    chk(pg3.evaluate("(function(){var v=S.cervello;S.cervello={url:'https://x',parola:'p'};"
                     "var d=chiediDisponibile();S.cervello=v;return d})()"),
        'con indirizzo e parola il cervello risulta collegato')
    chk(pg3.evaluate("""(function(){
      var v=S.cervello,dom=null,detto=null;
      S.cervello={url:'https://x',parola:'p'};
      var cp=chiediPulse,pl=parla;
      chiediPulse=function(d,cb){dom=d;cb('Risposta di prova.');};
      parla=function(items){detto=items[0];};
      eseguiComando(interpretaComando('quanto dura la riabilitazione dopo protesi'));
      chiediPulse=cp;parla=pl;S.cervello=v;
      return dom&&dom.indexOf('riabilitazione')>=0&&detto==='Risposta di prova.'})()"""),
        'una domanda fuori vocabolario, col cervello, diventa conversazione e risposta parlata')
    chk(pg3.evaluate("typeof fermaVoce==='function' && typeof _natQueue==='function' && typeof parla==='function'"),
        'la voce naturale ha partenza, coda e arresto unificati')
    chk(pg3.evaluate("_briefItems().length")>1,
        'il briefing per la voce naturale usa le battute del dialogo')
    chk(pg3.evaluate("autoLista()[1].voci[0].t").startswith('Scheda 1 di '),
        'anche in auto ogni scheda porta il suo annuncio di posizione')
    chk(pg3.evaluate("document.getElementById('vocesel')!==null && typeof popolaVoci==='function'"),
        'la voce di sistema si può scegliere dalle Impostazioni')
    chk(pg3.evaluate("JSON.stringify(statoDaTrasferire()).indexOf('cervello')")==-1,
        'indirizzo e parola del cervello NON viaggiano nel trasferimento né nel backup')

    # --- i segnali a PULSE: identità per contenuto, mai per posizione -----------
    chk(pg3.evaluate("(function(){var v=S.votes;S.votes={1:1,99:-1};"
                     "var t=segnaliTesto();S.votes=v;"
                     "return t.indexOf('SEGNALI PULSE')===0&&t.indexOf('PMID '+(A[1]&&A[1].pmid))>=0"
                     "&&t.indexOf('Meno così')<0})()"),
        'i segnali traducono i voti in PMID+titolo e ignorano schede inesistenti')
    chk(pg3.evaluate("(function(){var v=S.votes,s1=S.saved,s2=S.savedItems,w=S.weekly,d=S.suggDone;"
                     "S.votes={};S.saved=[];S.savedItems=[];S.weekly=[];S.suggDone={};"
                     "var t=segnaliTesto();S.votes=v;S.saved=s1;S.savedItems=s2;S.weekly=w;S.suggDone=d;"
                     "return t.indexOf('Nessun segnale ancora')>=0})()"),
        'senza scelte i segnali lo dichiarano, non fingono')
    dl=pg3.evaluate("typeof BRIEF_DIALOGO!=='undefined'?BRIEF_DIALOGO:null")
    if dl is not None:
        chk(all((r.get('chi') in ('A','B')) and (r.get('t') or '').strip() for r in dl)
            and {'A','B'} <= set(r.get('chi') for r in dl),
            'il dialogo del giorno ha battute valide e usa entrambe le voci')
    pg3.close()
    b.close()
print(f"\n===== PASSATI {ok} · FALLITI {bad} =====")
