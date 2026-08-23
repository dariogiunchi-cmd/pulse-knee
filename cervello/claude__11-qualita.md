# PULSE — regole di qualità (vincolanti)

*Introdotte il 2 agosto 2026 dopo un audit che ha trovato difetti reali.*

Queste regole valgono ogni mattina. Non sono consigli: se una non è rispettata,
il briefing non è pronto.

---

## 1. RUBRICA DELL'EVIDENZA (livello `CONF`)

| Livello | Disegni |
|---|---|
| **alta** | Meta-analisi di RCT · RCT ampio a basso rischio di bias · registro nazionale con esiti duri |
| **media** | SR di studi osservazionali · coorte prospettica · registro medio · comparativo con controllo |
| **bassa** | Revisione narrativa · cadavere · serie di casi · retrospettivo senza confronto · editoriale · preprint |

Si assegna per **disegno dello studio**, non a sensazione.

## 2. NUMERI E INCERTEZZA — obbligatori

Ogni campo *Risultati*: almeno un risultato quantificato con la sua incertezza
(p, IC, OR/HR/MD, DS) **oppure** la formula esatta:
> «Dimensioni dell'effetto e intervalli di confidenza non riportati nell'abstract.»

## 3. STUDI MUTI — obbligatorio dichiararli

**Uno studio che non può escludere l'effetto non è negativo, è muto.** Popola `MUTE`.
Casi tipici: gruppi <20-30 per braccio con esiti rari · retrospettivi senza confronto ·
narrative senza esiti clinici · cadavere/banco · «nessuna differenza» su campioni piccoli
(**non è prova di equivalenza**).

*Dalla sera del 17 agosto il silenzio si misura*: per i confronti binari,
`python3 test/potenza.py <eventi1> <n1> <eventi2> <n2>` stampa l'IC 95% del rischio
relativo e la frase da usare — che cosa lo studio **non può escludere**. Il MUTE con
il numero («non può escludere un RR fino a 10,4») vale più del MUTE ad aggettivi.

## 4. TENSIONI — sezione «Dove le prove non ti coprono»

Dalle questioni aperte di `03-memoria.md`. Quattro campi obbligatori:

| Campo | Contenuto |
|---|---|
| `fai` | Che cosa fa lui, concretamente |
| `prove` | Su che cosa sono invece gli studi, con i numeri |
| `fare` | **Che cosa può farci oggi**, scritto come azione |
| `chiude` | Quale studio lo chiuderebbe e quando |

Senza il campo `fare` la tensione è accademica e inutile.

## 5. AUDIO DERIVATO DALLE SCHEDE
`BRIEF_TEXT` va costruito dalle schede del giorno, non scritto a parte.

## 6. LINGUA
Contenuti, verdetti e audio in **italiano**. Titoli originali nella lingua di pubblicazione.

## 7. ACCESSIBILITÀ
Ogni pulsante con sola icona deve avere `aria-label` in italiano.

## 8. NIENTE SEGNAPOSTO
Nessun pulsante deve dire «nel deploy funzionerà». O funziona, o non c'è.

## 9. CONTENUTI SOCIAL — tre toni, tre lunghezze, hashtag

**I formati parlati si misurano in secondi.** Per `video` e `reel` l'app non mostra
«corto/medio/lungo» ma **30, 60 e 90 secondi**, e accanto scrive la durata **calcolata
sul testo reale** a 2,5 parole al secondo (150 parole al minuto, la velocità di lettura
ad alta voce comunemente usata). Se il copione non arriva ai secondi chiesti, l'app lo
dichiara invece di far finta.

Conseguenza vincolante sulla scrittura dei copioni `video`: i tre blocchi vanno
dimensionati perché **cumulativamente** diano circa **75 · 150 · 225 parole**, cioè
30 · 60 · 90 secondi. Un copione che si ferma a 170 parole rende inutile la scelta dei
90 secondi. Vale per tutti e tre i toni.

`SOCV[n][formato][tono] = [b1,b2,b3]` — **tre blocchi**: la lunghezza si ottiene
prendendo i primi 1, 2 o 3 (Corto / Medio / Lungo). Ogni blocco regge anche da solo.

**Formati:** `video` (30-90s) · `linkedin` · `instagram` · `reel`
**Toni:** `chir` (ortopedici: termini tecnici, livelli di evidenza, p e intervalli) ·
`misto` (specialista + curante + fisioterapista) · `pazienti` (nessuna sigla non spiegata).

**Hashtag** in `TAGS[n]`: `linkedin` (**esattamente 3**), `instagram` (9-12),
`kw` (**parole chiave per Google**, separate dagli hashtag).
Distinzione da tenere visibile: gli hashtag servono su Instagram e LinkedIn; su Google
contano le parole chiave dentro al testo.

Restano valide le regole di `06-social.md`. I testi modificati con «Adatta» restano
salvati per combinazione formato+tono+lunghezza e hanno la precedenza.

## 10. DISTRIBUZIONE MENSILE — `NLB` e fotografia dei lavori scelti

Disegno completo, parte legale e opzioni di automazione: `claude/12-distribuzione.md`.

**Obbligo quotidiano: `NLB`, in TRE registri.** Per **ogni** lavoro del giorno:

```
NLB = { numero: { prof: [titolo, corpo, nota critica],
                  mix:  [titolo, corpo, nota sul limite],
                  paz:  [titolo, corpo, nota rassicurante],
                  kw:   "3-4 parole chiave, come le cerca un paziente su Google" } }
```

Il registro **misto** è stato chiesto esplicitamente il 2 agosto 2026 ed è il più
difficile dei tre: deve essere capito da chiunque — medico curante, fisioterapista e
paziente — senza che il primo lo trovi banale né l'ultimo incomprensibile. Regola
pratica: nessuna sigla non sciolta, ma i numeri restano, e il limite dello studio si
scrive per esteso invece che con l'etichetta metodologica. È il registro che l'app usa
di default per Google Business Profile.

Frasi intere, **mai elenchi puntati**. `prof` = numeri e limite dichiarato, tono da
collega. `paz` = italiano semplice, nessuna promessa di risultato.
Il **primo blocco è il titolo**: regge da solo come sottotitolo nel blog e come riga di
elenco su Google. Massimo ~95 caratteri, senza punto finale.
I blurb si generano per **tutti** i lavori, non solo per il PICK: lui sceglie quando vuole.

**Fotografia dei lavori scelti — non toccare.**
```
S.weekly = [{ n, d, v, a:{h,j,journal,date,pmid,v}, b:{prof,paz,kw} }, …]   // 'pulse4'
```
I numeri di scheda cambiano ogni mattina: il riconoscimento «già scelto» avviene per
**PMID** (`wIdx`). Senza questo, dopo una notte le scelte sparirebbero.

**Funzioni intatte:** `pickWeek`, `wIdx`, `wArt`, `wBlurb`, `nlPicks`, `renderNl`,
`renderNlOut`, `nlText`, `blogText`, `gbpText`, `outText`, `nlKw`, `slugify`, `noDot`,
`setDest`, `setBlogUrl`, `setVid`, `setNlVer`, `copyOut`, `copyBody`, `copyPart` ·
`S.blogUrl` · pulsante `ib vid` · tab `📤 Newsletter` · `weekly` in `DEF`.

**Nessun linguaggio pubblicitario — è un vincolo legale.** LPMed art. 40 lett. d e Legge
sanitaria ticinese art. 70. Vietati inviti all'azione, sconti, gratuità, promesse di
risultato, «senza rischi», superlativi comparativi. La nota critica di ogni blurb è ciò
che rende il testo credibile invece che promozionale. `distribuzione.py` lo verifica.

**Mai:** chiedergli se ha girato il video, sollecitare l'invio, proporgli un calendario
editoriale.

---

## Difetti trovati e corretti (audit 2 agosto 2026)

1. Le tensioni non erano nell'app: zero occorrenze. Erano il cuore del progetto.
2. Su 11 schede solo 6 avevano un numero, una sola una misura di incertezza.
3. La sottopotenza non era mai calcolata, nonostante fosse un principio dichiarato.
4. Modalità scura difettosa: titoli su fondo chiaro, illeggibili.
5. Zero etichette di accessibilità.
6. Pulsante «Adatta» finto.
7. Livello di evidenza assegnato senza rubrica.
8. Lingua incoerente fra impostazioni e contenuti.
9. Le tensioni erano astratte: mancava «che cosa puoi farci».
10. I contenuti social avevano un solo tono e una sola lunghezza, senza hashtag.
11. La newsletter salvava solo il **numero** del lavoro scelto: dopo il ricambio notturno
    le quattro scelte sarebbero sparite. Corretto con la fotografia e il PMID.
    *Trovato in fase di test, mai arrivato all'utente.*
12. In modalità scura `.ib{background:… !important}` annullava lo stato acceso di ★, 👍,
    👎. Corretto con override dedicati.
13. Con cinque tab, a 375 px l'ultima usciva dallo schermo. Ora vanno a capo.
14. Nel blog la fonte usava la **sigla** della rivista (`Fonte: A —`). Corretto: nome per
    esteso, con fallback alla sigla per le scelte già in memoria.
15. Gli escape `\U0001f4f9` erano finiti **letterali** nel JavaScript. Trovato dai test,
    mai pubblicato. Ora `checklist.py` li cerca a ogni pubblicazione.
16. Le suite di test vivevano in `/tmp`: sarebbero sparite alla fine della sessione, e la
    checklist si eseguiva a mano. Ora vivono nel repository e `verifica.sh` è il solo
    modo per pubblicare.
17. La pubblicazione faceva `git init` + `push -f`: avrebbe cancellato istantanee e
    cervello a ogni giro. Ora si clona.

18. **Il difetto più grave della giornata, e riguardava il cancello stesso.** Le prime
    suite davano per scontati i lavori di oggi: «gli articoli 2, 1, 4 e 5», «esattamente
    48 testi social», «quattro lavori con le varianti». Simulando il briefing di domani —
    schede nuove, numeri diversi, tre lavori invece di quattro — **tutte e otto le suite
    fallivano**. Il cancello avrebbe bloccato una pubblicazione perfettamente valida,
    lasciando online l'app del giorno prima senza che nessuno se ne accorgesse: un
    fallimento silenzioso travestito da sicurezza. Riscritte tutte: **si collauda la
    macchina, non il carico del giorno** (vedi `test/comune.py`).
19. **Un articolo salvato oggi avrebbe mandato in errore l'app domani.** `S.saved`
    conteneva solo numeri di scheda; il mattino dopo quei numeri appartengono ad altri
    lavori o non esistono, e la scheda «Salvati» andava in eccezione. Corretto con la
    stessa fotografia usata per la newsletter (`savedItems`, riconoscimento per PMID),
    con migrazione dal vecchio formato. Trovato simulando il giorno dopo, mai arrivato
    all'utente.
20. Un `DUELS` che puntava a schede non più presenti mostrava una barra «VS» che non
    apriva nulla. Ora i duelli si filtrano su ciò che esiste davvero (`duelliVivi`).
21. Il verdetto diceva sempre «sono i **due** più importanti di oggi», anche con tre o
    quattro lavori in discussione. Ora la frase segue il numero reale.
22. La scheda sull'angolo postero-laterale riportava «da 2,5° a 7,6°» senza le deviazioni
    standard, che pure erano nella fonte e nei blurb. Trovato dal controllo «ogni scheda
    ha un numero con la sua incertezza». Ripristinato: 2,5°±0,9° → 7,6°±4,4°.

23. **Segnaposto sopravvissuti al controllo che doveva trovarli.** Il piè di pagina diceva
    ancora «Prototipo app PULSE» e «nel deploy: su ogni articolo», e un messaggio a
    comparsa diceva «Contenuti generati nel deploy». Il controllo cercava una sola frase
    esatta. Ora cerca una famiglia di segnaposto, come parole intere, **sia nel testo
    visibile sia dentro i messaggi generati dal JavaScript** — dove si nascondeva quello
    peggiore.
24. **L'app prometteva una sincronizzazione che non esiste.** In Impostazioni si leggeva:
    «Nel prototipo tutto resta su questo iPhone. Nel deploy vive nel tuo Google e si
    sincronizza.» Non c'è alcun Google, e non c'è alcuna sincronizzazione: tutto vive nel
    localStorage di quel browser. Sostituito con come stanno davvero le cose, compreso
    l'avvertimento che cancellare i dati del sito cancella salvataggi e scelte.
    *Era la cosa meno vera presente nell'app.*

25. **La copia di lavoro restava indietro rispetto a ciò che era online.** `pubblica.sh`
    pubblica da un clone temporaneo — scelta giusta, perché protegge istantanee e
    cervello — ma non riallineava `/home/claude/deploy`. Risultato: dopo ogni
    pubblicazione la copia locale sembrava «modificata e non pubblicata», e una sessione
    successiva avrebbe potuto ripartire da uno stato ingannevole o, peggio, ripubblicare
    all'indietro. Corretto: la pubblicazione ora riallinea la copia di lavoro all'ultimo
    SHA e lo dichiara. Tolti anche `__pycache__` dai file pubblicabili (`.gitignore`) e
    la credenziale dall'indirizzo del remoto nella configurazione locale di git.

26. **Le proposte da seguire venivano tracciate per POSIZIONE nell'elenco** (`suggIdx`),
    e l'elenco viene rigenerato ogni mattina. Due conseguenze, entrambe verificate: le
    proposte nuove finite in cima venivano **saltate senza che lui le vedesse**, e quelle
    a cui aveva gia' risposto potevano **ricomparire**. E' il terzo caso dello stesso
    errore in una giornata — identita' per posizione invece che per contenuto, dopo i
    lavori salvati e quelli scelti per i video. Corretto: `suggDone` per nome, con
    migrazione dal vecchio indice.
    **E' il difetto che l'utente ha notato per primo**, segnalando che l'app gli
    richiedeva conferme gia' date.
27. La migrazione appena scritta leggeva `SUGGQ` **dentro `load()`**, dove la variabile
    non e' ancora definita: l'app si fermava con un errore prima di partire. Spostata
    dove il dato esiste. *Trovata dai test, non pubblicata.*
28. `history.replaceState` chiamato **prima** della fusione annullava in silenzio l'intero
    trasferimento fra dispositivi. La pulizia dell'indirizzo non deve mai precedere il
    lavoro utile.
29. Con PULSE **gia' aperto**, il link di trasferimento cambiava solo il frammento e il
    browser non ricaricava la pagina: non succedeva assolutamente nulla. Aggiunto
    l'ascolto di `hashchange`. Trovato provando due dispositivi veri invece di uno.

30. **Tutte le pubblicazioni della giornata erano «Unverified» su GitHub.** La procedura
    ereditata disattivava esplicitamente la firma dei commit (`-c commit.gpgsign=false`),
    mentre l'ambiente ha una firma SSH configurata e GitHub la verifica. Riattivata, e
    l'intera storia rifirmata dopo aver verificato che l'albero dei file fosse **identico
    byte per byte** prima e dopo la riscrittura. `pubblica.sh` ora avvisa se un commit
    esce senza firma, invece di lasciar passare la cosa in silenzio.

31. **La copia di lavoro credeva di avere quindici commit non ancora spinti**, pur essendo
    allineata a GitHub carattere per carattere. `pubblica.sh` spinge da un **clone
    temporaneo**, quindi il riferimento locale `origin/main` non veniva mai aggiornato e
    `git status` confrontava contro una versione vecchia. Difetto solo di contabilita',
    non di contenuto — ma esattamente il tipo che porta a fidarsi di un segnale sbagliato,
    o a "risolverlo" con una spinta forzata che invece cancellerebbe del lavoro.
    Ora la procedura aggiorna anche il riferimento.

---

## Prove di funzionamento globale (2 agosto 2026, sera)

Fino a questo punto erano stati collaudati i *pezzi*. Queste sono le prove del sistema
**intero**, e vanno rifatte quando si cambia qualcosa di strutturale.

**1. Ripristino da un'istantanea.** La rete di sicurezza non era mai stata tirata:
scaricata `versioni/2026-08-02.html` e passata al cancello — 440 controlli verdi. Il
ritorno indietro funziona davvero, non solo sulla carta.

**2. Presenza degli strumenti.** `node`, `python3`, `git`, Playwright e Chromium sono
nell'immagine di sistema (`/usr/local/lib/python3.11/dist-packages`), quindi ci saranno
anche in un contenitore nuovo. Aggiunto comunque un **cancello zero** in `verifica.sh`:
se manca uno strumento lo dice in chiaro, con il comando per rimediare, e soprattutto
scrive *«non e' l'app a essere rotta — NON modificare index.html per far passare i
test»*. Senza quell'avviso, una sessione futura potrebbe mettersi a "correggere" codice
sano. Collaudato nascondendo `python3`: il messaggio giusto compare.

**3. Ciclo quotidiano completo.** Simulato esattamente cio' che fara' la sessione delle
5: clone del repository → lettura del cervello → riscrittura di ARTICLES, SOCV, TAGS,
NLB, SOC, DUELS, LINKS, MUTE, CONF, SUGGQ e BUILD_DATE → 440 controlli → istantanea con
ritenzione → commit **firmato**. Tutto superato.

**4. Il passaggio di giorno visto dall'utente.** Le due versioni servite sullo *stesso
indirizzo*, come sul suo telefono: stato creato con l'app del 2 agosto (3 salvati,
3 lavori scelti, un link video, un testo adattato, due proposte risposte, due voti, un
nome aggiunto), poi sostituzione dell'app con quella del 3 agosto e riapertura.
**Diciotto controlli, tutti superati**: nulla perso, proposte gia' risposte non
riproposte, proposte nuove mostrate, newsletter e blog ancora generati, zero errori.

**5. Un mese intero.** Quattro ricostruzioni settimanali con numeri di scheda tutti
diversi (100, 200, 300, 400) e una scelta per settimana. A fine mese la newsletter
contiene i quattro PMID giusti nell'ordine giusto, i quattro titoli distinti, i quattro
link video, e le date di scelta. E' il percorso che paga solo dopo trenta giorni ed era
l'ultimo mai provato.

**Cosa resta non dimostrabile qui:** il briefing vero delle 5 del mattino — ricerca su
PubMed, verifica delle citazioni, scrittura dei contenuti — perche' richiede la rete e
un contenitore nuovo. La meccanica attorno e' provata; il contenuto lo si giudica domani.

---

## 12. I CONTROLLI DI VERITÀ — `test/verita.py`

*Aggiunti la sera del 2 agosto, prima della prima esecuzione non sorvegliata.*

Le altre suite verificano che l'app **funzioni**. Questa verifica che non **affermi cose
false**. È la difesa meccanica del PRINCIPIO ZERO, e serve perché da domani il contenuto
viene generato senza che nessuno lo guardi.

Nessuno di questi controlli può dimostrare che una citazione sia vera — per quello serve
riaprire PubMed, e lo fa la sessione del mattino. Trovano le **impronte tipiche
dell'invenzione** e le affermazioni che l'app fa su sé stessa senza che i suoi dati le
sostengano:

- PMID e DOI **unici**, di lunghezza e forma plausibili, non tondi;
- **nessuna progressione aritmetica fra i PMID** — i PMID reali della stessa settimana
  sono vicini ma mai in sequenza regolare: una sequenza è l'impronta classica
  dell'invenzione;
- il conteggio delle citazioni verificate **non può superare** il numero di schede;
- `LAST_RETRACTION_CHECK` **deve coincidere con `BUILD_DATE`**: se resta indietro, l'app
  rassicura l'utente con un controllo che quel giorno non ha fatto;
- `CONF`, `MUTE`, `NLB`, `SOCV`, `LINKS`, `DUELS` **non possono puntare a schede
  inesistenti**.

Collaudata sabotando l'app cinque volte — PMID in sequenza, PMID duplicato, conteggio
gonfiato, data delle ritrattazioni vecchia, duello fantasma: **cinque su cinque
intercettati**.

---

## Difetti trovati e corretti (segue)

31. **Il piè di pagina dichiarava «citazioni verificate 11/11» scritto a mano.** Domani,
    con un numero diverso di schede, l'app avrebbe affermato all'utente una verifica che
    non corrispondeva ai suoi stessi dati. Ora il totale viene **contato**, e se le
    citazioni verificate sono meno delle schede il piè di pagina lo dichiara con un
    avviso invece di tacere.
32. **Un controllo che si disattivava da solo.** In `verita.py` la lettura di una
    variabile inciampava nel commento in coda alla riga e restituiva spazzatura: il
    controllo successivo veniva **saltato in silenzio** e la suite dava verde. Trovato
    solo perché ho sabotato l'app di proposito per vedere se le sentinelle suonassero.
    *Un controllo che non suona è peggio di un controllo assente: dà la sicurezza senza
    darne la sostanza.* Regola che ne discende: ogni nuova sentinella va collaudata
    rompendo davvero ciò che deve proteggere.

33. **Avevo aggiunto una condizione al cancello senza dirlo alla sessione del mattino.**
    I nuovi controlli di verità pretendono `CIT_VERIFICATE` e `LAST_RETRACTION_CHECK`
    aggiornati, ma le istruzioni quotidiane non ne parlavano: domattina la pubblicazione
    sarebbe stata bloccata da una regola che nessuno aveva comunicato.
    **Regola che ne discende: ogni condizione aggiunta al cancello va aggiunta anche al
    prompt dell'attività quotidiana, nello stesso momento.**
34. **Sette conteggi scritti a mano erano rientrati nelle suite** — «5 tensioni»,
    «10 riviste», «14 società», «8 aziende», «3 salvati», «5 dopo la fusione», «2 proposte
    risposte». Le tensioni cambiano ogni giorno: quel controllo sarebbe saltato **di
    certo** il 3 agosto. Tutti derivati dai dati. La regola 11 esisteva già: il fatto che
    sia stata violata due volte nello stesso giorno dice che va **verificata**, non solo
    scritta — d'ora in poi, dopo ogni modifica alle suite, cercare i confronti con numeri
    letterali.

**Prova finale del 2 agosto, sul «domani difficile»:** 7 schede, contenuti social solo su
2 lavori, una sola proposta, due tensioni, nessun duello, nessuno studio muto, nessun
collegamento. **458 controlli verdi.** È lo scenario magro che avrebbe fatto inciampare
ognuno dei conteggi scritti a mano.

---

## 13. LA DISCENDENZA — regola nata dalla sera del 4 agosto 2026

**Una pubblicazione deve discendere da ciò che è online.** Non è una raccomandazione: è
un controllo, e sta in `test/pubblica.sh`.

Che cosa è successo. Alle 18:51 sono state pubblicate quattro correzioni. Alle 18:53 è
partito il briefing, che ha clonato il repository un istante prima che quella
pubblicazione fosse visibile. Alle 19:10 il briefing ha pubblicato: clone fresco, push
non forzato, storia lineare — e le quattro correzioni erano sparite. Il passo che copia
`index.html` sopra il clone non si chiedeva da quale versione quel file discendesse.

**Nessun allarme è suonato.** 464 controlli verdi su un file che aveva appena cancellato
il lavoro di diciannove minuti prima. Le suite collaudano il contenuto della giornata,
non la sua discendenza: è una dimensione che nessuna di esse guardava.

Il fermo confronta lo `HEAD` della copia di lavoro con `origin/main` al momento del
clone. Se la copia di lavoro è un antenato di ciò che è online, si ferma con codice 4,
elenca i commit e i file finiti nel mezzo, e dice come riallinearsi. `PULSE_SOVRASCRIVI=1`
è l'unica scappatoia, e stampa a video che la scelta è stata dichiarata.

Collaudato su tre rami, con un repository finto: copia indietro → si ferma prima di
toccare qualsiasi file · copia allineata → passa e lo dice · copia indietro con
forzatura → avverte per intero, poi prosegue dichiarandolo. E il controllo che protegge
il fermo (`checklist.py`) è stato collaudato togliendo il fermo: suona.

> **La lezione, più generale del difetto.** Le suite guardavano *che cosa* viene
> pubblicato e mai *sopra che cosa*. Ogni volta che due sessioni possono lavorare sullo
> stesso oggetto, esiste una dimensione che nessun test di contenuto vede.

## Difetti trovati e corretti (4 agosto 2026)

35. **Due giorni di silenzio totale.** Il 3 e il 4 agosto il compito quotidiano è partito
    e non ha lasciato nulla: nessun commit, nessuna istantanea, nessuna entrata nello
    storico, nessun messaggio. L'utente ha aperto l'app e ha trovato il giorno prima.
    Causa più probabile, indicata da lui: **esaurimento dei crediti**. Il silenzio totale
    è la firma di una sessione che non è mai partita davvero — un esaurimento *durante* il
    lavoro avrebbe lasciato tracce parziali.
    **Regola che ne discende:** un guasto silenzioso è peggio di un guasto rumoroso. Il
    sistema deve avere almeno un rilevatore che non dipenda dalle stesse risorse di ciò
    che sorveglia.
36. **Il rilevatore che dipende da ciò che sorveglia.** La sentinella creata lo stesso
    giorno (compito schedulato delle 9, `trig_01FXmhEtnk1CrCDAk2DFGU4y`) consuma crediti
    anch'essa: se finiscono, tace. Per questo è scritta come **battito**, non come
    allarme: manda una riga anche quando va tutto bene. L'assenza del messaggio è essa
    stessa il segnale. L'unico rilevatore davvero indipendente è il banner dentro l'app,
    che gira sull'iPhone e non consuma nulla.
37. **La sentinella usava `api.github.com`, che dal sandbox risponde 403.** Scoperto
    provando il comando prima di lasciarla in servizio, non dopo. Riscritta su
    `raw.githubusercontent.com` più una sonda sull'istantanea del giorno
    (`versioni/AAAA-MM-GG.html`): due segnali che dicono cose diverse — l'app è stata
    ripubblicata, e il briefing è stato aggiornato — e permettono di distinguere «non è
    successo niente» da «è successo qualcosa ma non il briefing».
38. **L'intestazione dell'app era di nuovo scritta a mano** — «15» lavori mentre erano 11,
    più il conteggio degli arancioni, «11/11» e la data del 2 agosto — perché la
    correzione delle 18:51 era stata cancellata dal difetto della discendenza. Ripristinata
    e derivata: `renderTop()`.
39. **`PREFV` era tornato a 2 e Filardo e de Caro erano spariti dalle liste**, stessa
    causa. Ripristinati. Nota: entrambi i nomi erano stati riaperti su PubMed prima di
    scriverli — «Filaro», come era stato dettato, è **Giuseppe Filardo**, EOC Lugano.

40. **Un conteggio assoluto scritto a mano era sopravvissuto dentro una suite, per
    settimane, perché ogni giorno aveva sempre avuto abbastanza schede da non farlo
    inciampare.** `test/newsletter.py` verificava `nvid >= 6` (almeno sei pulsanti
    «📹 Video»): la mattina del 23 agosto, con una giornata leggera di 5 schede, il
    cancello si è fermato su un briefing valido — esattamente il difetto 18/34, la
    stessa famiglia di errore, non ancora spenta del tutto. Corretto derivando il
    numero atteso da `ARTICLES` (`nvid == len(TUTTI)`), come impone `test/comune.py`
    fin dal 2 agosto. Collaudato rompendolo davvero: con il pulsante rimosso dal
    rendering, la sentinella corretta segnala `(0, 5)` invece di tacere.
    **Regola che se ne ricava:** una regola di collaudo scritta bene in un file
    (`comune.py`) non protegge le suite che non la usano — ogni conteggio in ogni
    suite va controllato, non solo quelli aggiunti dopo la regola.
