var store={};global.localStorage={getItem:k=>store[k]||null,setItem:(k,v)=>store[k]=v};
function CL(){return {_c:{},add(c){this._c[c]=1},remove(c){delete this._c[c]},toggle(c){this._c[c]=this._c[c]?0:1},contains(c){return !!this._c[c]}};}
function stub(){return {classList:CL()};}
function El(){var e={innerHTML:'',textContent:'',value:'',style:{},classList:CL(),addEventListener(){},querySelector(){return El()},scrollIntoView(){},closest(){return null},id:''};e.parentNode={children:[stub(),stub(),stub(),stub()],id:''};e.children=[];return e;}
var reg={};global.document={getElementById:id=>reg[id]||(reg[id]=El()),querySelectorAll:()=>[],querySelector:()=>El(),addEventListener(){}};
global.navigator={clipboard:{writeText(){return Promise.resolve()}},share:null};global.location={href:'https://esempio/pulse/',hash:'',split(){return['']}};global.history={replaceState(){}};global.btoa=s=>Buffer.from(s,'binary').toString('base64');global.atob=s=>Buffer.from(s,'base64').toString('binary');global.window={addEventListener(){}};global.confirm=()=>true;global.event=null;
var _f=process.env.PULSE_HTML||'index.html';
var _h=require('fs').readFileSync(_f,'utf8');
eval(_h.match(/<script>([\s\S]*)<\/script>/)[1]);
// I numeri di scheda cambiano ogni mattina: si scoprono, non si scrivono a mano.
var NN=ARTICLES.map(function(a){return a.n});
var P1=NN[0], P2=(NN[1]!==undefined?NN[1]:NN[0]), P3=(NN[2]!==undefined?NN[2]:NN[0]);
var PSOC=NN.filter(function(n){return typeof SOC!=='undefined'&&SOC[n]})[0];
if(PSOC===undefined)PSOC=NN.filter(function(n){return typeof SOCV!=='undefined'&&SOCV[n]})[0];

var pass=0,fail=0;
function ok(c,m){console.log((c?'✅':'❌')+' '+m);c?pass++:fail++;}

console.log('\n--- 0. LAVORO DEL GIORNO E COLONNA DESTRA ---');
// L'INDICE del giorno: copertura completa, una riga per voce, conteggi derivati.
renderGiorno();
var _voci=vociIndice();
ok(_voci.length===ARTICLES.length+EXTRA.length+SCOPERTE.length,
   'ogni cosa rilevante del giorno è nell\'indice: '+_voci.length+' voci, nessun tetto');
var _gi=document.getElementById('gindice').innerHTML;
ok((_gi.match(/class="irow"/g)||[]).length>=_voci.length-1,
   'una riga per ogni voce (l\'evidenza conta come riga del suo dominio)');
ok(document.getElementById('gmisura').textContent.indexOf(String(_voci.length)+' rilevanti')>=0,
   'l\'intestazione dichiara la misura, contata e mai scritta a mano');
ok(_gi.indexOf('— nulla oggi')>=0 || DOMINI.every(function(d){return _voci.some(function(v){return v.dom===d[0]})}),
   'un dominio senza voci si contrae in una riga sola');
ok(document.getElementById('gevid').innerHTML.indexOf((A[PICK].riga||A[PICK].h).slice(0,40))>=0,
   'l\'evidenza del giorno è il lavoro indicato da PICK, dai dati');
var _oldPick=PICK;PICK=99999;renderGiorno();
ok(document.getElementById('gindice').innerHTML.length>200,'PICK rotto → l\'indice resta in piedi');
PICK=_oldPick;renderGiorno();
// la riga: fatto (riga o h), mai il vuoto; senza dominio si finisce in «Altro», non nel nulla
var _domV=ARTICLES[1].dom;ARTICLES[1].dom='';renderGiorno();
ok(document.getElementById('gindice').innerHTML.indexOf('Altro')>=0,
   'una voce senza dominio finisce in «Altro», non sparisce');
ARTICLES[1].dom=_domV;renderGiorno();
// il giudizio unico: per PMID, pesi da soli, «utile» archivia, annullo simmetrico
var _pm=ARTICLES[0].pmid;var _aG=_artPm(_pm);
giudica(_pm,1);
ok(S.giudizi[_pm]===1,'✓ utile registrato per PMID, non per posizione');
ok(S.savedItems.some(function(x){return x.a&&x.a.pmid===_pm}),'«utile» archivia la scheda da sola');
ok((S.pesi.riviste||{})[_aG.j]===1,'il giudizio aggiorna i pesi della rivista da solo');
giudica(_pm,1);
ok(!S.giudizi[_pm]&&!(S.pesi.riviste||{})[_aG.j]&&!S.savedItems.some(function(x){return x.a&&x.a.pmid===_pm}),
   'toccare di nuovo annulla giudizio, peso e archiviazione');
vote(null,ARTICLES[1].n,-1);
ok(S.giudizi[ARTICLES[1].pmid]===-1,'i pollici delle schede parlano la stessa lingua: giudizio per PMID');
giudica(ARTICLES[1].pmid,-1);
S.pesi={};save();

// scadenze: si costruiscono date relative a oggi, mai letterali
function _fra(g){var d=new Date(Date.now()+g*86400000);
 return d.getFullYear()+'-'+('0'+(d.getMonth()+1)).slice(-2)+'-'+('0'+d.getDate()).slice(-2);}
ok(giorniA(_fra(5))===5 && giorniA(_fra(0))===0 && giorniA(_fra(-3))===-3,'i giorni a una scadenza si contano giusti');
ok(scadenzaTesto(_fra(5)).indexOf('5 giorni')>=0,'fra cinque giorni → «5 giorni»');
ok(scadenzaTesto(_fra(1)).indexOf('domani')>=0,'fra un giorno → «domani», non «1 giorni»');
ok(scadenzaTesto(_fra(0)).indexOf('scade oggi')>=0,'oggi → «scade oggi»');
ok(scadenzaTesto(_fra(-2)).indexOf('scaduta')>=0,'passata → dichiarata scaduta, mai un numero positivo');
var _oc=CONGRESSI;
CONGRESSI=[{sig:'BBB',citta:'Prova',date:'1-2 dic',abstract:_fra(40)},{sig:'AAA',citta:'X',date:'giu',abstract:_fra(20)},{sig:'VECCHIO',abstract:_fra(-40)}];
renderGiorno();
var _gc=document.getElementById('gindice').innerHTML;
ok(_gc.indexOf('AAA')>=0&&_gc.indexOf('BBB')>=0,'i congressi sono righe strutturate: sigla, città, date, scadenze');
ok(_gc.indexOf('AAA')<_gc.indexOf('BBB'),'ordinati per scadenza più vicina, non per data del congresso');
ok(_gc.indexOf('VECCHIO')<0,'un congresso con le scadenze passate sparisce da solo');
ok(_gc.indexOf('iscad')>=0&&_gc.indexOf('iscad forte')<0,'scadenza entro 30 giorni evidenziata, senza gridare');
CONGRESSI=[{sig:'SETTE',abstract:_fra(3)}];renderGiorno();
ok(document.getElementById('gindice').innerHTML.indexOf('iscad forte')>=0,'entro 7 giorni l\'evidenza si rafforza');
CONGRESSI=[];renderGiorno();
ok(document.getElementById('gindice').innerHTML.indexOf('Congressi — nulla oggi')>=0,
   'senza congressi: una riga dal punto di vista dell\'utente, niente scuse di sistema');
CONGRESSI=_oc;renderGiorno();
// industria: righe, coi richiami in coda
var _oi=INDUSTRIA;
INDUSTRIA=[{tipo:'richiamo',fonte:'openFDA',riga:'Richiamo di prova'},{fonte:'MassDevice',riga:'Lancio di prova di un sistema'}];
renderGiorno();
var _gind=document.getElementById('gindice').innerHTML;
ok(_gind.indexOf('Lancio di prova')<_gind.indexOf('Richiamo di prova'),
   'in Industria le notizie vengono prima, i richiami in coda');
INDUSTRIA=_oi;renderGiorno();

console.log('\n--- 1. FALLIMENTO SILENZIOSO ---');
// Il banner si collauda contro la verità del giorno, non contro l'ipotesi che il file
// sia stato costruito oggi: quando si pubblica una correzione senza briefing nuovo,
// BUILD_DATE resta indietro ed è giusto che il banner lo dichiari (regola 11).
var _bdReale=BUILD_DATE;
var _n=new Date(), _oggiIso=_n.getFullYear()+'-'+('0'+(_n.getMonth()+1)).slice(-2)+'-'+('0'+_n.getDate()).slice(-2);
BUILD_DATE=_oggiIso; renderFresh();
ok(document.getElementById('gfresh').innerHTML==='','briefing di oggi → nessun banner: il successo è il silenzio, lo dice il verdetto');
BUILD_DATE=_bdReale; renderFresh();
ok(_bdReale===_oggiIso ? document.getElementById('gfresh').innerHTML===''
   : document.getElementById('gfresh').innerHTML.length>0,
   'file di oggi → silenzio; file vecchio → dichiarato');
// L'attesa non è un guasto: alle 7:10, con il briefing in preparazione, l'app diceva
// «qualcosa non ha funzionato». Questi controlli fissano i tre stati distinti.
var _real=BUILD_DATE, _ieri=new Date(Date.now()-86400000);
BUILD_DATE=_ieri.getFullYear()+'-'+('0'+(_ieri.getMonth()+1)).slice(-2)+'-'+('0'+_ieri.getDate()).slice(-2);
renderFresh();
var _t=document.getElementById('gfresh').innerHTML, _h=new Date().getUTCHours();
var _hm=new Date().getUTCHours()+new Date().getUTCMinutes()/60;
if(_hm>=5&&_hm<6.5) ok(_t.indexOf('in preparazione')>=0,'ieri, nell\'ora del briefing → «in preparazione», non un allarme');
else if(_h<5)   ok(_t.indexOf('arriva verso le 7')>=0,'ieri, di notte → attesa dichiarata, nessun allarme');
else            ok(_t.indexOf('non è arrivato')>=0,'ieri, a giornata inoltrata → allarme');
ok(_t.indexOf('qualcosa non ha funzionato')<0 || _h>=7,'nessun allarme prima che la finestra sia chiusa');
BUILD_DATE=_real;
// Le date si calcolano dal giorno reale, non si scrivono a mano: una data fissa
// («2026-07-28», «2026-08-01») collauda il calendario di UN giorno, non la macchina,
// e il mattino dopo mente. Il caso «ieri» è già coperto, in modo dinamico, dai tre
// stati qui sopra (notte · in preparazione · non arrivato).
var real=BUILD_DATE; var _5g=new Date(Date.now()-5*86400000);
BUILD_DATE=_5g.getFullYear()+'-'+('0'+(_5g.getMonth()+1)).slice(-2)+'-'+('0'+_5g.getDate()).slice(-2); renderFresh();
ok(document.getElementById('gfresh').innerHTML.indexOf('giorni fa')>=0 && document.getElementById('gfresh').innerHTML.indexOf('non sta girando')>=0,'5 giorni fa → allarme rosso con istruzione');
BUILD_DATE=real;

console.log('\n--- 2. ALLERTA RITRATTAZIONE ---');
ok(retrHTML(1)==='','nessuna ritrattazione → nessun avviso');
RETRACTED[1]='ritirato per errore nei dati';
ok(retrHTML(1).indexOf('Articolo ritirato')>=0,'con ritrattazione → banner rosso nella scheda');
toggleSave(null,P1); renderRetr();
ok(document.getElementById('retrbox').innerHTML.indexOf('sono stati ritirati')>=0 || document.getElementById('retrbox').innerHTML.indexOf('è stato ritirato')>=0,'salvato ritirato → avviso in Salvati');
delete RETRACTED[1]; renderRetr();
ok(document.getElementById('retrbox').innerHTML.indexOf('Nessun articolo salvato è stato ritirato')>=0,'nessuna ritrattazione → conferma verde con data');

console.log('\n--- 3. COLLEGAMENTO NEL TEMPO ---');
// quali lavori siano collegati fra loro cambia ogni giorno: si scopre, non si presume
var NL=NN.filter(function(n){return typeof LINKS!=='undefined'&&LINKS[n]&&LINKS[n].length&&A[LINKS[n][0].n]});
if(NL.length){var L=linksHTML(NL[0]);
 ok(L.indexOf('Collegati nel tempo')>=0,'campo "Collegati nel tempo" presente');
 var rif=LINKS[NL[0]][0];
 ok(L.indexOf('['+rif.n+']')>=0 && L.indexOf(rif.rel)>=0,'lavoro '+NL[0]+' collegato al '+rif.n+': '+rif.rel);}
else{ok(typeof linksHTML==='function','collegamenti nel tempo: nessuno oggi, la funzione c\'è');
 ok(linksHTML(NN[0])==='','nessun collegamento inventato dove non ce ne sono');}
// quale scheda sia priva di collegamenti cambia ogni giorno: si scopre a runtime,
// non si scrive a mano il numero (regola 11). Era tornato «8» — e oggi la scheda 8
// i collegamenti ce li ha.
var _noL=NN.filter(function(n){return !(typeof LINKS!=='undefined'&&LINKS[n]&&LINKS[n].length);})[0];
if(_noL!==undefined) ok(linksHTML(_noL)==='','lavoro senza collegamenti ('+_noL+') → nessun campo');
else ok(true,'oggi ogni lavoro ha collegamenti: niente da verificare qui');
document.getElementById('histq').value='menisco'; searchHist();
ok(document.getElementById('histres').innerHTML.length>50,'ricerca archivio "menisco" → risultati');
document.getElementById('histq').value='zzzznope'; searchHist();
ok(document.getElementById('histres').innerHTML.indexOf('Nessun risultato')>=0,'ricerca senza esito → messaggio corretto');
document.getElementById('histq').value=''; searchHist(); ok(document.getElementById('histres').innerHTML.indexOf('Cerca per tecnica')>=0,'ricerca vuota → invito con esempi, non il vuoto');

console.log('\n--- 4. VISTA DUELLO ---');
renderDuel();
var VIVI=duelliVivi();
if(VIVI.length){
 ok(document.getElementById('duelbox').innerHTML.indexOf('VS')>=0 && document.getElementById('duelbox').innerHTML.indexOf('confronta')>=0,'barra duello mostrata in Oggi');
 openDuel(VIVI[0].i);
 ok(document.getElementById('shCnt').innerHTML.indexOf('duelgrid')>=0,'duello aperto in due colonne');}
else{ok(document.getElementById('duelbox').innerHTML==='','nessun duello oggi: nessuna barra mostrata');
 ok(typeof openDuel==='function','la vista duello c\'è comunque');}
if(VIVI.length){
 ok(document.getElementById('shCnt').innerHTML.indexOf('Conclusione')>=0 && document.getElementById('shCnt').innerHTML.indexOf('Evidenza')>=0,'confronto include conclusioni e livello di evidenza');
 ok(document.getElementById('shTitle').textContent===DUELS[VIVI[0].i].topic,'titolo del duello = argomento del confronto');}
else{ok(true,'confronto: nessuno oggi');ok(true,'titolo del duello: nessuno oggi');}

console.log('\n--- 5. TEMPO DI LETTURA ---');
var m2=readMin(A[P2]);
ok(m2>=1 && m2<=9,'tempo di lettura scheda '+P2+' = '+m2+' min (plausibile)');
ok(NN.every(function(n){return readMin(A[n])>=1}),'tempo calcolato su tutte le '+NN.length+' schede');

console.log('\n--- 6. AUTOCRITICA SETTIMANALE ---');
renderAudit();
ok(document.getElementById('auditbox').innerHTML.indexOf('Autocritica della settimana')>=0,'riquadro autocritica presente');
// DERIVATO dai dati del giorno, mai una fonte scritta a mano: il 20 agosto la
// parola fissa «Swissmedic» ha fatto rosso su un briefing VALIDO (quella fonte
// era verificata, quindi giustamente assente) — difetto della classe vietata.
ok(AUDIT.nonverificate.length>0 && AUDIT.nonverificate.every(function(n){
  return document.getElementById('auditbox').innerHTML.indexOf(n)>=0;
}),'elenca tutte le '+AUDIT.nonverificate.length+' fonti non verificate del giorno');
ok(document.getElementById('auditbox').innerHTML.indexOf('fuori finestra')>=0,'dichiara quanti lavori ha scartato');

console.log('\n--- 7. NON-REGRESSIONE (tutto il resto) ---');
toggleSave(null,P2);ok(S.saved.indexOf(P2)>=0,'Salva');
vote(null,P3,1);ok(S.giudizi[A[P3].pmid]===1,'Voto ✓ (per PMID)');giudica(A[P3].pmid,1);
toggle(P2);ok(S.seen.indexOf(P2)>=0,'Segna letto');
renderResearch();ok(true,'Filtri + verdetto');
renderSaved();ok(true,'Ricerca salvati');
if(PSOC!==undefined){openSocial(null,PSOC);ok(curSoc===PSOC,'Contenuti social');}else{ok(typeof openSocial==='function','Contenuti social: nessun lavoro oggi, la funzione c\'è');}
speakCard(null,P2);ok(true,'Lettura vocale scheda');
shareArt(null,P2);ok(true,'Condividi');
var CN=NN.filter(function(n){return typeof CONF!=='undefined'&&CONF[n]});
ok(CN.length ? CN.every(function(n){return confHTML(n).indexOf(CONF[n])>=0})
             : typeof confHTML==='function',
   'Barre di confidenza'+(CN.length?' su '+CN.length+' schede, coerenti con CONF':': la funzione c\'è'));
ok(typeof renderPlayer==='function'&&typeof audioPlayPausa==='function'&&typeof audioSalta==='function','il lettore MP3 esiste: play, salti, velocità');
ok(JSON.parse(store['pulse4']).saved.length>0,'Persistenza');
console.log('\n=========================');
console.log('PASSATI: '+pass+'   FALLITI: '+fail);
console.log(fail?'⚠️ CI SONO ERRORI':'🎉 TUTTO VERDE');
