# File 7 — Nota strategica: PULSE e PROBUS
### Documento riservato · Redatto per essere mostrato a un potenziale socio, consulente o investitore
**19 agosto 2026**

---

## Avvertenza metodologica

Questa nota è basata su ricerca documentale condotta il 19 agosto 2026. **Nessuna pagina web è stata aperta direttamente** a causa di una restrizione di rete dell'ambiente di analisi: i dati provengono da estratti restituiti dai motori di ricerca. I prezzi sono classificati per affidabilità della fonte, e i punti che richiedono un parere legale sono elencati in chiusura. **Nessun dato è stato inferito o costruito**: dove manca, è scritto che manca.

---

# 1. PULSE

## 1.1 Che cos'è, oggi

Software di sorveglianza scientifica automatizzata. Interroga in continuo banche dati bibliografiche, riviste, atti congressuali, preprint, registri e linee guida, e consegna ogni mattina alle 5:00 UTC — in formato di quotidiano personalizzato — le novità rilevanti sul perimetro clinico scelto, filtrate secondo le preferenze dell'utente.

È in uso quotidiano reale da parte di un chirurgo ortopedico del ginocchio in Svizzera. Non è una presentazione: è un prodotto che gira.

## 1.2 Il mercato, senza sconti

Sono stati censiti **oltre venti prodotti** che occupano parti dello stesso spazio. Il quadro è il seguente.

### I concorrenti diretti sono gratuiti

| Prodotto | Che cosa fa | Prezzo | Proprietà |
|---|---|---|---|
| **Read by QxMD** | Feed personalizzato di letteratura biomedica, mobile-first, recupero del full text via credenziali istituzionali | **Gratuito** | **WebMD** (acquisita 2019). Monetizza con pubblicità farmaceutica |
| **Scholar Inbox** | Digest quotidiano personalizzato, ricerca semantica, pianificatore di congressi | **Gratuito** | Accademico. Copre preprint, non MEDLINE |
| **Semantic Scholar Feeds** | Raccomandazioni personalizzate + digest, alert su citazioni e autori | **Gratuito**, API gratuita | Allen Institute |
| **PubMed / My NCBI** | Alert su query salvate, giornalieri o settimanali | **Gratuito**, max 100 query | NIH |
| **OpenEvidence** | Motore di risposta clinica su corpus licenziato (NEJM, JAMA, Wiley, Cochrane) | **Gratuito**, pubblicità farmaceutica | $12 mld di valutazione (gen. 2026) |
| **Vera Health** | Risposta clinica su 60M+ paper, 900+ calcolatori | **Gratuito** per clinici verificati | Si posiziona come alternativa europea a OpenEvidence |
| **Medscape AI** | Insight per specialità | **Gratuito** per 13 mln di membri | WebMD |

### I prodotti a pagamento non fanno consegna quotidiana

| Prodotto | Prezzo (fonte) | Limite rispetto a Pulse |
|---|---|---|
| **Consensus** | Pro $20/mese o $144/anno *(ufficiale)* | È **pull**: nessun monitoraggio continuo |
| **Scite** | $20/mese, Pro $50/mese *(ufficiale)* | Alert di citazione, non un briefing |
| **Elicit** | ~$10–49/mese *(solo aggregatori, contraddittori)* | Strumento da progetto, non da abitudine |
| **Undermind** | ~$16/mese *(aggregatore)* | Nessun push |
| **NEJM Journal Watch** | $129/anno *(listino ufficiale)* | Cura umana, periodico, non personalizzato |
| **DynaMed** | $399/anno, $475 con AI *(ufficiale)* | Supporto decisionale, altra categoria |
| **UpToDate** | ~$579/anno *(fonte terziaria, da riverificare)* | Idem |
| **OrthoEvidence** | prezzo individuale non rilevato | **Gratuito come beneficio associativo** per i soci di BASEM e Canadian Orthopaedic Association |

> ⚠️ **Attenzione su un dato che circola.** Alcuni aggregatori attribuiscono a «Consensus» prezzi di $600–1'250 al mese: appartengono a **un'altra azienda omonima** (goconsensus.com, automazione di demo commerciali). Un business case costruito su quei numeri sbaglia bersaglio.

### E il concorrente che non fattura contro di lei

Un abbonamento **ChatGPT Plus** da ~$20/mese, con un *Scheduled Task* ricorrente, produce già oggi un briefing quotidiano su un argomento clinico. Lo fa male — non ha PMID come chiave stabile, non controlla le ritrattazioni, allucina citazioni, non ha memoria del perimetro — **ma è a un prompt di distanza dal 70% della funzione, e costa zero marginale a chi quell'abbonamento ha già.**

## 1.3 Che cosa fa PULSE che gli altri non fanno

Onestamente: **nessuna singola funzione di Pulse è nuova.** Ogni componente esiste altrove, spesso gratis. Ciò che nessuno dei venti prodotti censiti ha è la **combinazione**, e in particolare due elementi che non nascono da un'intuizione di prodotto ma da una necessità professionale.

**1. Il cancello di verità meccanizzato.** Nessun concorrente ha un controllo che **blocca la pubblicazione** se una citazione non è verificata, se un numero è privo della sua incertezza, se un riferimento punta a una scheda inesistente. Gli altri mitigano l'allucinazione con citazioni cliccabili; nessuno la tratta come **condizione di rilascio**. Il risultato è un artefatto raro in questo settore: un prodotto AI il cui output è **riproducibile, versionato, con istantanee datate e prova verificabile di ciò che era pubblicato in una certa data**.

**2. Il registro di conformità pubblicitaria.** Un controllo che blocca sulla base della LPMed art. 40 lett. d e della Legge sanitaria ticinese non è una funzione che un fondatore americano penserebbe di costruire. Per un mercato europeo di professionisti sanitari regolamentati è esattamente ciò che manca a tutti gli altri.

**3. Una finestra circostanziale, che non è un vantaggio competitivo.** Il **27 aprile 2026 OpenEvidence si è ritirata da Unione europea e Regno Unito**, motivando con l'incertezza regolatoria legata all'AI Act; a luglio 2026 non era ancora rientrata, e la vicenda è oggetto di commento sul *Lancet Regional Health – Europe*. È una finestra reale — **ma Vera Health la sta già occupando, gratuitamente e a livello mondiale.**

## 1.4 Quanto dura il vantaggio: **12-24 mesi. Meno se qualcuno con distribuzione decide di farlo.**

Il ragionamento, senza indulgenza:

- **La raccolta dati è merce comune.** E-utilities gratuite, Crossref in pubblico dominio, Europe PMC gratuita, Unpaywall 100'000 chiamate al giorno, Retraction Watch aperta. Chiunque replica l'ingestione in poche settimane.
- **Il modello linguistico è merce comune e deflaziona.** La distanza fra la sintesi di Pulse e quella di un modello di frontiera con un buon prompt si assottiglia a ogni rilascio. Il cancello di verifica compensa oggi; fra due generazioni compenserà meno.
- **Il push programmato è già un pulsante** negli assistenti generalisti, e le tre grandi non venderanno «sorveglianza ortopedica»: la regaleranno come effetto collaterale.
- **La verticalità non protegge da sola.** Qualunque concorrente può assumere un ortopedico consulente per un fine settimana.
- **Il muro vero è il full text, e sta dalla parte sbagliata.** Wiley ha dichiarato **$49 milioni di ricavi da licenze AI** nell'esercizio chiuso il 30 aprile 2026, citando fra i clienti OpenEvidence. Il contenuto clinico che rende credibile un concorrente si compra a milioni di dollari l'anno. **In una gara di contenuti Pulse perde per definizione.**
- **La domanda solvibile individuale è debole.** Il concorrente diretto è gratis. Il concorrente clinico serio è gratis, perché la pubblicità farmaceutica paga più di quanto pagherebbe il medico.
- **E il mercato verticale è minuscolo.** La FMH conta oltre 46'000 medici in tutta la Svizzera; gli ortopedici sono dell'ordine delle migliaia, i chirurghi del ginocchio delle centinaia. **Anche con conversione del 100% e €500 l'anno, la Svizzera ortopedica non è un'azienda.**

> ### Verdetto
> **La difendibilità di PULSE come abbonamento venduto a singoli specialisti è debole. Non marginale: debole.** Chi presentasse questo progetto come «uno spazio vuoto» sarebbe smentito in venti minuti di ricerca.

## 1.5 Dove si sposta il valore — tre porte

**Porta 1 · Il corpus, non il codice.** Il perimetro clinico, l'ordine delle schede, la rete di riviste e opinion leader, le tensioni aperte, il registro peritale, le preferenze accumulate: è **giudizio editoriale codificato**, e cresce con l'uso. Il codice si riscrive in un mese; quel corpus no. Pulse ha valore se diventa **la piattaforma su cui un esperto codifica il proprio perimetro** — non un feed sul ginocchio, ma lo strumento con cui un secondo, un terzo, un decimo esperto costruisce il proprio.

**Porta 2 · Il compratore è la società scientifica, non il chirurgo.** È il modello che l'ortopedia ha **già validato**: OrthoEvidence è gratuito per i soci di BASEM e della Canadian Orthopaedic Association, e lo paga la società. Una società scientifica ha budget, deve dimostrare valore ai soci, non vuole costruire, e ha lo stesso problema di conformità pubblicitaria che Pulse ha già risolto. **È il canale più realistico — e richiede un venditore, non un ingegnere.**

**Porta 3 · La sorveglianza regolatoria per l'industria medtech — dove il cancello diventa il prodotto.** L'MDR impone a ogni fabbricante una revisione sistematica e ricorrente della letteratura per tutta la vita del dispositivo (PMS, PMCF, CER, PSUR). DistillerSR e CiteMed vendono esattamente questo. In quel mercato: la sorveglianza continua è un **obbligo di legge**; **la tracciabilità è il valore** — istantanee datate, commit firmati, riverifica di ciò che è online, controlli che bloccano; il compratore è un ufficio regolatorio con budget ricorrente. E un'azienda medtech del ginocchio vive nello stesso perimetro clinico del corpus già costruito.

> ⚠️ **Con un conflitto da governare per iscritto.** Vendere sorveglianza della letteratura a un fabbricante i cui dispositivi *sono giudicati* in quella letteratura è un problema di indipendenza. Va risolto nel contratto, non con la buona fede.

**Le tre porte si escludono in parte.** Il prodotto per il chirurgo vuole brevità e mobile; quello per la società scientifica vuole marchio e distribuzione; quello per l'industria vuole tracciabilità ed esaustività. **Non si percorrono insieme.**

## 1.6 Vincoli da verificare prima di trasformarlo in prodotto

### Diritto d'autore — il rischio numero uno

| Risorsa | Metadati | Abstract | Full text |
|---|---|---|---|
| **PubMed / NCBI** | Liberi, **con disclaimer NCBI obbligatoriamente visibile in app** | **Copyright di terzi — uso commerciale a rischio** | Non fornito |
| **Europe PMC** | Liberi via API | Come sopra | Solo Open Access con licenza ridistribuibile |
| **Crossref** | **Pubblico dominio (CC0)** | **Esclusi dal CC0** | Non fornito |
| **Unpaywall** | Liberi, 100'000 chiamate/giorno | — | Solo link a copie OA legali |
| **Retraction Watch** (via Crossref dal 2023) | **Completamente aperti** | — | — |

**Il punto duro:** NCBI dichiara espressamente che gli abstract PubMed possono incorporare materiale protetto, che chi ne fa **uso commerciale** deve rispettare i termini del titolare del copyright, e che **NCBI stessa non può concedere quell'autorizzazione**. Un prodotto a pagamento che riproduce integralmente abstract non è coperto da alcuna licenza.
**Il perimetro sicuro è: metadati bibliografici + collegamento + sintesi originale.** Un briefing che incolla abstract è un rischio, non una funzione.
**L'unica buona notizia:** il controllo delle ritrattazioni può poggiare su Retraction Watch, acquisita da Crossref nel 2023 e resa completamente aperta e aggiornata ogni giorno lavorativo. È l'unico ingrediente senza problemi di licenza.

### Qualificazione regolatoria — dove passa il confine

**MDR 2017/745, regola 11:** il software destinato a fornire informazioni **utilizzate per prendere decisioni a fini diagnostici o terapeutici** è dispositivo medico di classe IIa o superiore. La guida **MDCG 2019-11**, rivista il 17 giugno 2025, chiarisce che la **«ricerca semplice»** — recupero di record confrontando metadati con criteri di ricerca, funzioni di biblioteca — **non qualifica**.

| Funzione di Pulse | Posizione |
|---|---|
| Ricerca, recupero, elenco di articoli nuovi | Fuori qualifica |
| Riassunto neutro di ciò che uno studio riporta | Ragionevolmente fuori: informa, non decide |
| Ordinamento per rilevanza secondo preferenze | Zona grigia, probabilmente ancora fuori |
| **I campi di verdetto e di selezione** | **Zona di rischio.** Se formulati come indirizzo clinico, si scivola nella regola 11 |
| Accettare i dati di un singolo paziente | **Dispositivo medico, classe IIa o superiore** |

**Il fattore decisivo è la destinazione d'uso dichiarata dal fabbricante**, non l'architettura. **È una decisione di prodotto da scrivere prima, non una formalità da sistemare dopo.**

**AI Act, articolo 50 — obblighi di trasparenza, applicabili dal 2 agosto 2026**, cioè da questo mese: chi fornisce sistemi che generano testo sintetico deve marcare gli output come generati da AI in formato leggibile da macchina; per i sistemi già sul mercato la marcatura è dovuta entro il 2 dicembre 2026. **Pulse genera testo.** Se offerto nell'UE, l'articolo 50 lo riguarda direttamente — ed è la norma per cui un concorrente da 12 miliardi di dollari, con un ufficio legale, ha preferito uscire dal mercato europeo.

**Svizzera.** ODmed e ODIV sono allineate all'MDR (revisioni in vigore dal 1° novembre 2023 e dal 1° gennaio 2025); Swissmedic applica lo stesso criterio della destinazione d'uso. **Non esiste un AI Act svizzero:** il 12 febbraio 2025 il Consiglio federale ha scelto un approccio settoriale, con un avamprogetto atteso entro fine 2026.
> **Conseguenza: per i prossimi 12-24 mesi la Svizzera è un ambiente più permissivo dell'UE per un prodotto di questo tipo. È una finestra reale — ma è una finestra, e il mercato svizzero da solo è troppo piccolo per un SaaS.**

### Protezione dei dati

Trattando solo dati di utenti professionali (non di pazienti) il quadro è gestibile: sotto i 250 collaboratori il registro dei trattamenti è di norma esentato, la soglia svizzera di notifica delle violazioni è più alta di quella europea. **Ma vendere nell'UE fa scattare il GDPR** (art. 3 par. 2) e con esso l'obbligo di designare per iscritto **un rappresentante nell'Unione** (art. 27), il registro art. 30 — nella pratica di un SaaS l'esenzione è illusoria — e un contratto di responsabile del trattamento con **ogni sub-responsabile**, a partire dal fornitore del modello linguistico, verso cui ogni contenuto trasmesso è un trasferimento.

### Rischio di allucinazione

Un aggregatore scientifico che riassume male è un danno reputazionale diretto per chi lo firma — e per un chirurgo che è anche perito, un rischio professionale. I controlli già in essere (PMID unici e non in progressione aritmetica, conteggi non gonfiati, riferimenti a schede esistenti, cancello bloccante) sono **il vero prodotto**. Prima di renderlo pubblico servono anche: sorveglianza delle ritrattazioni **su ogni scheda già pubblicata**, non solo su quelle nuove; e un registro degli errori corretti, pubblico.

## 1.7 Modelli di ricavo a confronto

| Modello | Prezzo plausibile | Mercato ottenibile | Sforzo commerciale | Compatibile con agenda chirurgica piena? |
|---|---|---|---|---|
| **Strumento interno non commercializzato** | — | — | Nullo | ✅ |
| **Abbonamento a singoli specialisti** | €15–40/mese | Centinaia in CH, migliaia in EU | **Altissimo** | ❌ |
| **Licenza a cliniche e gruppi** | €3'000–15'000/anno | Decine | Alto, ciclo lungo | ⚠️ |
| **Licenza a società scientifiche** | €10'000–50'000/anno | **Poche unità, ma sufficienti** | Medio: pochi interlocutori | ✅ |
| **Servizio all'industria medtech (sorveglianza MDR)** | €20'000–80'000/anno | Decine in EU | Medio-alto | ⚠️ conflitto da governare |
| **Versione gratuita al servizio del marchio personale** | 0 | — | Nullo | ✅ |

> **Quale sceglierei: la licenza alle società scientifiche, con la sorveglianza regolatoria medtech come seconda opzione.** Sono gli unici due modelli con **pochi interlocutori e contratti grandi**, cioè gli unici compatibili con chi opera 1'539 volte l'anno. Vendere a singoli medici richiede una macchina commerciale che non esiste e che non può essere costruita nei ritagli.

## 1.8 Il percorso a costo minimo per validarlo — 90 giorni, zero righe di codice

**L'esperimento.** Pubblicare per dodici settimane la rassegna curata come **newsletter gratuita verticale sul ginocchio**, con commento clinico firmato. Distribuzione: LinkedIn, sito, coda del libro in uscita, firma email.

**Che cosa si misura, e le soglie decise prima:**

| Indicatore | «Vale la pena proseguire» | «Fermarsi» |
|---|---|---|
| Iscritti a 90 giorni | **> 300**, di cui almeno 80 medici | < 120 |
| Tasso di apertura | **> 45%** | < 25% |
| Richieste spontanee di accesso allo strumento | **≥ 5** | 0 |
| Contatti da società scientifiche o industria | **≥ 1** | 0 |
| Tempo effettivo del committente | **< 2 ore/mese** | > 5 ore/mese |

**Perché questo esperimento e non un altro:** costa quasi nulla, non richiede decisioni societarie né legali, e **ha la proprietà rara di essere utile comunque**. Anche se Pulse non diventasse mai un prodotto, la newsletter avrà costruito il pubblico proprio che oggi manca — e che serve identicamente al libro, ai congressi, a Probus e a qualunque altra attività futura.

**La soglia sul tempo è la più importante.** Se alimentare la newsletter costa più di due ore al mese, il modello non regge: significa che il commento non è delegabile abbastanza, e allora Pulse non è un prodotto ma un secondo lavoro.

## 1.9 Nome, dominio, marchio

Da verificare **prima** di investire nel nome: disponibilità nelle estensioni `.ch`, `.com`, `.io`; e — soprattutto — assenza di marchi anteriori in **classe 9** (software) e **classe 42/44** (servizi informatici e medici) su `swissreg.ch` (gratuito, due minuti) e sul registro europeo EUIPO. «Pulse» è una parola comune e molto usata nel software: **la probabilità di un conflitto in classe 9 è alta.**
Costo della registrazione preventiva: poche centinaia di franchi. Costo di scoprirlo dopo aver costruito il marchio: un cambio di nome, o una transazione.

---

# 2. PROBUS

## 2.1 Il problema di definizione

Il committente ha indicato **tre nature contemporaneamente**: gestionale/SaaS per studi medici; piattaforma di raccolta dati clinici e di esito; servizio o percorso clinico per pazienti.

**Sono tre aziende diverse.** Cliente diverso, modello di ricavo diverso, regime regolatorio diverso, competenze diverse:

| Se è… | Il cliente è | Il ricavo è | Il regime è | Il concorrente è |
|---|---|---|---|---|
| Gestionale per studi medici | Il medico titolare | Abbonamento per postazione | Protezione dati | Mercato maturo e affollato in CH |
| Piattaforma di dati di esito | Cliniche, registri, industria | Licenza o progetto | **Dati sanitari + possibile dispositivo medico** | Registri nazionali, software di ricerca clinica |
| Percorso clinico per pazienti | Il paziente o l'assicuratore | Prestazione o convenzione | **Sanitario a pieno titolo** | Cliniche, assicurazioni |

**Finché sono tre, non è un progetto: è un'area di interesse.** E un'area di interesse non si finanzia, non si costituisce e non si vende.

## 2.2 La raccomandazione: congelare dodici mesi, e lasciare che nasca da sé

Non è una rinuncia, è la sequenza corretta — per una ragione concreta.

**La piattaforma di dati di esito nasce da sola** se il committente avvia la raccolta sistematica dei PROMs sui propri pazienti (KOOS, IKDC, Oxford Knee Score, prima dell'intervento, a sei e a dodici mesi). Con 1'539 interventi l'anno, entro dodici mesi avrà **300-500 ginocchia seguite prospetticamente** e saprà, per esperienza diretta e non per ipotesi, che cosa quel software deve fare, dove si rompe il flusso, che tasso di risposta è realistico, che cosa i pazienti effettivamente compilano.

Oggi non lo sa. Nessuno può saperlo per lui. E un software costruito su un'ipotesi di flusso clinico è il modo più comune di spendere CHF 100'000 per un prodotto che nessuno usa.

**Il costo del congelamento è zero**, perché nel frattempo si costruisce il dato che lo definirà. **Il costo di non congelarlo** è avviare in parallelo una seconda impresa software mentre la prima non ha ancora validato il proprio mercato.

⚠️ **Un vincolo da mettere in conto fin d'ora:** i dati di esito sono **dati sanitari**. Servono informativa nLPD, consenso esplicito scritto, contratto con chi ospita i dati, e — con finalità di ricerca — l'approvazione del **Comitato etico cantonale**. Vanno previsti nel budget dei PROMs, non scoperti dopo.

---

# 3. La decisione sul marchio — Pulse e Probus separati dal nome personale

La domanda era se legare i due progetti al nome e al volto del fondatore o tenerli come marchi autonomi. **La risposta è diversa da quella che sarebbe stata se l'obiettivo fosse solo commerciale**, perché l'obiettivo dichiarato del committente è, a termine, **cessare l'attività chirurgica e vivere della gestione delle società avviate**.

> **Un marchio che porta il nome del fondatore non si vende, e non gira senza di lui.**

| | Scenario «sotto il nome personale» | Scenario «marchio separato» |
|---|---|---|
| **Velocità di lancio** | Alta: la credibilità è già costruita | Bassa: si parte da zero |
| **Credibilità iniziale** | Alta presso i colleghi | Da costruire |
| **Mercato raggiungibile** | **Limitato all'ortopedia e alla reputazione del fondatore** | Qualunque specialità |
| **Rischio reputazionale incrociato** | **Alto**: un difetto del software tocca il chirurgo, e viceversa | Basso |
| **Vendibilità futura** | **Prossima a zero** | Reale |
| **Reversibilità** | Bassa: staccare un nome dopo è costoso e sospetto | Alta: il fondatore si può aggiungere in qualunque momento |

**Raccomandazione, distinta per progetto:**

- **PULSE → marchio separato**, con il fondatore **pubblicamente riconoscibile come tale**. La credibilità della firma clinica è un vantaggio reale in fase di lancio e va usata — ma come *attributo* del prodotto, non come suo nome. Un prodotto che si chiama come un chirurgo del ginocchio non venderà mai a un cardiologo, e non si vende affatto.
- **PROBUS → marchio separato, senza eccezioni.** È software destinato a studi medici: nessun collega compra un gestionale che porta il nome di un concorrente. Qui il nome personale è un ostacolo, non un vantaggio.

**Che cosa costruire subito, perché serve identicamente in ogni scenario:** il **pubblico proprio via newsletter**. È l'unico bene che nessuna piattaforma può togliere, l'unico canale di lancio che non va comprato due volte, e l'unico elemento di questo documento che è utile sia che Pulse diventi un'azienda, sia che resti lo strumento personale del chirurgo più aggiornato del Ticino.

---

# 4. La sequenza fra i due progetti

Con un'agenda chirurgica piena non si lanciano due prodotti insieme.

| | Progetto | Decisione | Perché |
|---|---|---|---|
| **Primo** | **PULSE** | Validare con la newsletter, 90 giorni, zero codice | È già costruito, il costo di validazione è quasi nullo, e l'esperimento è utile comunque |
| **Congelato 12 mesi** | **PROBUS** | Nessun investimento. Avviare invece i PROMi | Non è definito, e i PROMs lo definiranno gratis |

---

# 5. Punti che richiedono un parere legale specialistico

1. **Riproduzione di abstract in un prodotto commerciale.** NCBI e Crossref escludono entrambi gli abstract dal materiale liberamente riutilizzabile. Domanda specifica: *la sintesi generata da un modello linguistico a partire da un abstract protetto, rivenduta in abbonamento, è opera derivata?* Nessuna delle fonti consultate risponde.
2. **Destinazione d'uso e qualificazione come dispositivo medico.** Da scrivere **con** un consulente regolatorio prima di qualsiasi commercializzazione. In particolare: i campi di verdetto e di selezione sopravvivono a un'analisi MDCG 2019-11?
3. **AI Act art. 50** — se Pulse, offerto a clinici UE, sia «fornitore» ai sensi della norma, e come implementare la marcatura leggibile da macchina.
4. **Contratto di responsabile del trattamento con il fornitore del modello linguistico**, valutazione del trasferimento verso gli Stati Uniti, verifica che i contenuti non siano usati per l'addestramento.
5. **Rappresentante UE ex art. 27 GDPR** e mandatario UE per dispositivi medici: due nomine distinte, entrambe con costi ricorrenti.
6. **Indipendenza in caso di clienti industriali** — da governare contrattualmente e da dichiarare.
7. **Marchi anteriori** per «Pulse» e «Probus» in classe 9 e 42/44.

---

# 6. In una pagina, per un interlocutore esterno

**Che cosa esiste:** un software di sorveglianza scientifica in uso quotidiano reale, con un'architettura di verifica — cancello bloccante, istantanee datate, riproducibilità — che nessuno dei venti concorrenti censiti possiede.

**Che cosa non esiste:** un mercato dimostrato. I concorrenti diretti sono gratuiti e in mano a operatori con distribuzione enorme; il muro del full text si supera solo con licenze da milioni; il mercato verticale svizzero è troppo piccolo per un abbonamento individuale.

**Dove sta il valore reale:** non nel codice — replicabile in un mese — ma nel **corpus di giudizio editoriale codificato**, e nella **tracciabilità verificabile**, che è esattamente ciò che l'MDR impone all'industria medtech di dimostrare.

**Che cosa si chiede di decidere adesso:** nulla. Novanta giorni di newsletter, cinque soglie numeriche fissate in anticipo, e una decisione presa sui dati invece che sull'entusiasmo.

**Il rischio principale non è che Pulse fallisca.** È che assorba il tempo e le decisioni di un chirurgo che ha, nello stesso portafoglio, un progetto con un potenziale di reddito ricorrente molto superiore e un percorso molto più breve — la società di servizi per la riabilitazione. Quel confronto è sviluppato nel File 8.
