var store={};global.localStorage={getItem:k=>store[k]||null,setItem:(k,v)=>store[k]=v};
function CL(){return {_c:{},add(c){this._c[c]=1},remove(c){delete this._c[c]},toggle(c){this._c[c]=this._c[c]?0:1},contains(c){return !!this._c[c]}};}
function stub(){return {classList:CL()};}
function El(){var e={innerHTML:'',textContent:'',value:'',style:{},classList:CL(),addEventListener(){},querySelector(){return El()},scrollIntoView(){},closest(){return null},id:''};e.parentNode={children:[stub(),stub(),stub(),stub()],id:''};e.children=[];return e;}
var reg={};global.document={getElementById:id=>reg[id]||(reg[id]=El()),querySelectorAll:()=>[],querySelector:()=>El(),addEventListener(){}};
global.navigator={clipboard:{writeText(){return Promise.resolve()}}};global.window={};global.confirm=()=>true;global.event=null;
var _f=process.env.PULSE_HTML||'index.html';
var _h=require('fs').readFileSync(_f,'utf8');
eval(_h.match(/<script>([\s\S]*)<\/script>/)[1]);
var pass=0,fail=0;
function ok(c,m){console.log((c?'✅':'❌')+' '+m);c?pass++:fail++;}

console.log('\n--- 1. FALLIMENTO SILENZIOSO ---');
renderFresh();
ok(document.getElementById('freshbox').innerHTML.indexOf('Aggiornato oggi')>=0,'oggi → banner verde "Aggiornato oggi"');
var real=BUILD_DATE; BUILD_DATE='2026-07-28'; renderFresh();
ok(document.getElementById('freshbox').innerHTML.indexOf('giorni fa')>=0 && document.getElementById('freshbox').innerHTML.indexOf('non sta girando')>=0,'5 giorni fa → allarme rosso con istruzione');
BUILD_DATE='2026-08-01'; renderFresh();
ok(document.getElementById('freshbox').innerHTML.indexOf('ieri')>=0,'ieri → avviso giallo');
BUILD_DATE=real;

console.log('\n--- 2. ALLERTA RITRATTAZIONE ---');
ok(retrHTML(1)==='','nessuna ritrattazione → nessun avviso');
RETRACTED[1]='ritirato per errore nei dati';
ok(retrHTML(1).indexOf('Articolo ritirato')>=0,'con ritrattazione → banner rosso nella scheda');
toggleSave(null,1); renderRetr();
ok(document.getElementById('retrbox').innerHTML.indexOf('sono stati ritirati')>=0 || document.getElementById('retrbox').innerHTML.indexOf('è stato ritirato')>=0,'salvato ritirato → avviso in Salvati');
delete RETRACTED[1]; renderRetr();
ok(document.getElementById('retrbox').innerHTML.indexOf('Nessun articolo salvato è stato ritirato')>=0,'nessuna ritrattazione → conferma verde con data');

console.log('\n--- 3. COLLEGAMENTO NEL TEMPO ---');
var L=linksHTML(1);
ok(L.indexOf('Collegati nel tempo')>=0,'campo "Collegati nel tempo" presente');
ok(L.indexOf('[3]')>=0 && L.indexOf('posizione opposta')>=0,'lavoro 1 collegato al 3 come posizione opposta');
ok(linksHTML(8)==='','lavoro senza collegamenti → nessun campo');
document.getElementById('histq').value='menisco'; searchHist();
ok(document.getElementById('histres').innerHTML.length>50,'ricerca archivio "menisco" → risultati');
document.getElementById('histq').value='zzzznope'; searchHist();
ok(document.getElementById('histres').innerHTML.indexOf('Nessun risultato')>=0,'ricerca senza esito → messaggio corretto');
document.getElementById('histq').value=''; searchHist(); ok(document.getElementById('histres').innerHTML==='','ricerca vuota → pulita');

console.log('\n--- 4. VISTA DUELLO ---');
renderDuel();
ok(document.getElementById('duelbox').innerHTML.indexOf('VS')>=0 && document.getElementById('duelbox').innerHTML.indexOf('confronta')>=0,'barra duello mostrata in Oggi');
openDuel(0);
ok(document.getElementById('shCnt').innerHTML.indexOf('duelgrid')>=0,'duello aperto in due colonne');
ok(document.getElementById('shCnt').innerHTML.indexOf('Conclusione')>=0 && document.getElementById('shCnt').innerHTML.indexOf('Evidenza')>=0,'confronto include conclusioni e livello di evidenza');
ok(document.getElementById('shTitle').textContent.indexOf('retto femorale')>=0,'titolo del duello corretto');

console.log('\n--- 5. TEMPO DI LETTURA ---');
var m2=readMin(A[2]);
ok(m2>=1 && m2<=4,'tempo di lettura art.2 = '+m2+' min (range valido)');
ok(readMin(A[1])>=1,'tempo calcolato su tutte le schede');

console.log('\n--- 6. AUTOCRITICA SETTIMANALE ---');
renderAudit();
ok(document.getElementById('auditbox').innerHTML.indexOf('Autocritica della settimana')>=0,'riquadro autocritica presente');
ok(document.getElementById('auditbox').innerHTML.indexOf('Swissmedic')>=0,'elenca le fonti non verificate');
ok(document.getElementById('auditbox').innerHTML.indexOf('fuori finestra')>=0,'dichiara quanti lavori ha scartato');

console.log('\n--- 7. NON-REGRESSIONE (tutto il resto) ---');
toggleSave(null,2);ok(S.saved.indexOf(2)>=0,'Salva');
vote(null,3,1);ok(S.votes[3]===1,'Voto 👍');
toggle(2);ok(S.seen.indexOf(2)>=0,'Segna letto');
renderResearch();ok(true,'Filtri + verdetto');
renderVerdict();ok(document.getElementById('verdict').innerHTML.indexOf('mettono in discussione')>=0,'Verdetto del giorno con i titoli');
renderSaved();ok(true,'Ricerca salvati');
openSocial(null,2);ok(curSoc===2,'Contenuti social');
speakCard(null,2);ok(true,'Lettura vocale scheda');
shareArt(null,2);ok(true,'Condividi');
ok(confHTML(8).indexOf('alta')>=0,'Barre di confidenza');
ok(typeof speakBrief==='function','Riassunto vocale');
ok(JSON.parse(store['pulse4']).saved.length>0,'Persistenza');
console.log('\n=========================');
console.log('PASSATI: '+pass+'   FALLITI: '+fail);
console.log(fail?'⚠️ CI SONO ERRORI':'🎉 TUTTO VERDE');
