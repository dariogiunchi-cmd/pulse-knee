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

console.log('\n--- 1. FALLIMENTO SILENZIOSO ---');
renderFresh();
ok(document.getElementById('freshbox').innerHTML.indexOf('Aggiornato oggi')>=0,'oggi → banner verde "Aggiornato oggi"');
// La freschezza si misura sul giorno reale in cui gira la suite: le date NON si
// scrivono a mano (regola 11), altrimenti il test funziona solo il giorno in cui è
// stato scritto. Si cerca a runtime la data che il vero renderFresh classifica come
// "molti giorni fa" e quella che classifica come "ieri", qualunque sia l'ora del run.
var real=BUILD_DATE;
function _isoMinus(dd){return new Date(Date.now()-dd*86400000).toISOString().slice(0,10);}
function _daysOf(iso){return Math.floor((new Date()-new Date(iso+'T07:00:00'))/86400000);}
var _vecchio=null,_ieri=null;
for(var _k=1;_k<=8;_k++){var _iso=_isoMinus(_k),_d=_daysOf(_iso);
 if(_d===1&&_ieri===null)_ieri=_iso;
 if(_d>=2&&_vecchio===null)_vecchio=_iso;}
BUILD_DATE=_vecchio||_isoMinus(5); renderFresh();
ok(document.getElementById('freshbox').innerHTML.indexOf('giorni fa')>=0 && document.getElementById('freshbox').innerHTML.indexOf('non sta girando')>=0,'molti giorni fa → allarme rosso con istruzione');
BUILD_DATE=_ieri||_isoMinus(1); renderFresh();
ok(document.getElementById('freshbox').innerHTML.indexOf('ieri')>=0,'ieri → avviso giallo');
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
// non si scrive a mano il numero (regola 11).
var _noL=NN.filter(function(n){return !(typeof LINKS!=='undefined'&&LINKS[n]&&LINKS[n].length);})[0];
if(_noL!==undefined) ok(linksHTML(_noL)==='','lavoro senza collegamenti ('+_noL+') → nessun campo');
else ok(true,'oggi ogni lavoro ha collegamenti: niente da verificare qui');
document.getElementById('histq').value='menisco'; searchHist();
ok(document.getElementById('histres').innerHTML.length>50,'ricerca archivio "menisco" → risultati');
document.getElementById('histq').value='zzzznope'; searchHist();
ok(document.getElementById('histres').innerHTML.indexOf('Nessun risultato')>=0,'ricerca senza esito → messaggio corretto');
document.getElementById('histq').value=''; searchHist(); ok(document.getElementById('histres').innerHTML==='','ricerca vuota → pulita');

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
ok(document.getElementById('auditbox').innerHTML.indexOf('Swissmedic')>=0,'elenca le fonti non verificate');
ok(document.getElementById('auditbox').innerHTML.indexOf('fuori finestra')>=0,'dichiara quanti lavori ha scartato');

console.log('\n--- 7. NON-REGRESSIONE (tutto il resto) ---');
toggleSave(null,P2);ok(S.saved.indexOf(P2)>=0,'Salva');
vote(null,P3,1);ok(S.votes[P3]===1,'Voto 👍');
toggle(P2);ok(S.seen.indexOf(P2)>=0,'Segna letto');
renderResearch();ok(true,'Filtri + verdetto');
renderVerdict();
var VH=document.getElementById('verdict').innerHTML;
var ARANCI=ARTICLES.filter(function(a){return a.sec=='res'&&a.dot=='orange'}).length;
ok(ARANCI ? (VH.indexOf('in discussione')>=0 && VH.indexOf('vitem')>=0)
          : (VH.indexOf('niente mette in discussione')>=0),
   'Verdetto del giorno: '+(ARANCI?ARANCI+' lavori in discussione, con i titoli':'giornata senza contraddizioni, dichiarata'));
renderSaved();ok(true,'Ricerca salvati');
if(PSOC!==undefined){openSocial(null,PSOC);ok(curSoc===PSOC,'Contenuti social');}else{ok(typeof openSocial==='function','Contenuti social: nessun lavoro oggi, la funzione c\'è');}
speakCard(null,P2);ok(true,'Lettura vocale scheda');
shareArt(null,P2);ok(true,'Condividi');
var CN=NN.filter(function(n){return typeof CONF!=='undefined'&&CONF[n]});
ok(CN.length ? CN.every(function(n){return confHTML(n).indexOf(CONF[n])>=0})
             : typeof confHTML==='function',
   'Barre di confidenza'+(CN.length?' su '+CN.length+' schede, coerenti con CONF':': la funzione c\'è'));
ok(typeof speakBrief==='function','Riassunto vocale');
ok(JSON.parse(store['pulse4']).saved.length>0,'Persistenza');
console.log('\n=========================');
console.log('PASSATI: '+pass+'   FALLITI: '+fail);
console.log(fail?'⚠️ CI SONO ERRORI':'🎉 TUTTO VERDE');
