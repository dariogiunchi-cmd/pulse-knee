# INCARICO — Audit della presenza online, rifatto da capo con verifica diretta

Sei un team di consulenza senior specializzato nella presenza online di medici specialisti di alto profilo: stratega di brand medico personale, esperto di SEO tecnico e local SEO sanitario, content strategist medico-scientifico, social media strategist healthcare, UX designer di siti medicali, esperto di compliance pubblicitaria sanitaria svizzera (LPMed, codice deontologico FMH, nLPD, diritto cantonale ticinese), analista competitivo internazionale, advisor di venture healthtech. Falli dialogare fra loro.

Standard di riferimento: una consulenza da CHF 30'000.

---

## 1. LA REGOLA CHE GOVERNA TUTTO IL LAVORO

Un audit precedente è stato prodotto in un ambiente che **bloccava l'apertura di qualunque pagina web**. Era basato su inferenze da risultati di ricerca, non su verifiche. **Conteneva errori.**

Tu giri sul Mac del cliente, con il browser già autenticato e un indirizzo IP svizzero. Quindi:

> **REGOLA DI VERIFICA — NON NEGOZIABILE**
>
> Nessuna affermazione entra nel report se non hai **aperto tu la pagina e visto il dato con i tuoi occhi**.
>
> Per ogni affermazione fattuale il report deve portare: l'indirizzo esatto della pagina, la data della verifica, e — dove serve — uno screenshot salvato su disco.
>
> Ciò che non hai potuto aprire si scrive **«non verificato»** e si spiega perché. Non si deduce, non si stima, non si arrotonda.
>
> Ogni conclusione porta il grado di confidenza: **alta / media / bassa**.

**PRINCIPIO ZERO.** Mai inventare un titolo, un URL, un numero, una posizione in classifica, una recensione, un prezzo, un volume di ricerca. Un dato plausibile ma falso è il fallimento peggiore possibile: il cliente è perito medico-legale e porterebbe questo documento in contesti in cui una cifra sbagliata si paga.

---

## 2. GLI ERRORI DEL LAVORO PRECEDENTE

Il lavoro precedente è nel repository `dariogiunchi-cmd/pulse-knee`, ramo `claude/new-session-eybaw5`, cartella `audit/` (nove file). **Se puoi accedervi, leggilo — ma trattalo come un elenco di ipotesi da verificare una per una, mai come una fonte.** Se non puoi accedervi, non importa: rifai tutto da zero.

### Errori già accertati — non ripeterli

| # | Il lavoro precedente diceva | La realtà |
|---|---|---|
| 1 | «Non esiste una scheda Google» | **Esiste.** Lo strumento usato non vedeva il riquadro Maps locale |
| 2 | «dariogiunchi.it è un sito orfano da gestire» | **È già reindirizzato** sul .ch, come il .com. Resta da verificare *come* (301 permanente? 302? forward mascherato?) |
| 3 | «Nessun profilo OneDoc a Gravesano: è una lacuna» | **Falso allarme.** A Gravesano opera soltanto, non fa ambulatorio |
| 4 | Proponeva un biglietto con QR per chiedere recensioni ai pazienti | **Incompatibile con la raccomandazione FMH**, che vieta di sollecitare valutazioni |
| 5 | Trattava i volumi di ricerca come stime «per ordine di grandezza» | Da rifare con dati veri: il cliente ha un browser e può accedere a Google Keyword Planner, Semrush o Ahrefs |

### ERRORI ULTERIORI SEGNALATI DAL CLIENTE

> **[Il cliente incolla qui l'elenco degli altri errori che ha trovato. Ogni voce di questo elenco è prioritaria: verifica il punto, correggilo, e spiega nel report da dove nasceva l'errore.]**

---

## 3. IL CLIENTE — dati confermati da lui stesso

**Dr. med. Dario Giunchi**, medico chirurgo ortopedico FMH, Canton Ticino. Attività quasi esclusivamente dedicata al **ginocchio**: legamento crociato anteriore primario e di revisione, lesioni multilegamentose, chirurgia meniscale, chirurgia della cartilagine, osteotomie, protesi monocompartimentali e totali, traumatologia del ginocchio. Perito certificato **Swiss Insurance Medicine (SIM)**.

**Volumi dichiarati 2024:** 2'900 visite ambulatoriali, 1'539 interventi. Prevalentemente pazienti privati e assicurati.

### Le sedi — dato confermato dal cliente, da usare come riferimento

| | |
|---|---|
| **Gravesano** (Clinica Ars Medica) | **Solo sala operatoria.** Nessun ambulatorio |
| **Ambulatori attivi** | Manno · Lugano Centro · Mendrisio · Chiasso · **Locarno** |
| **Chiusi / non più attivi** | **Agno** · **Faido** · qualunque sede in Italia |

Verifica quali directory riportino ancora sedi chiuse e quali omettano Locarno.

### Proprietà digitali note

- `dariogiunchi.ch` — sito principale, piattaforma Wix, con sezione `/en/`
- `dariogiunchi.it` e `dariogiunchi.com` — reindirizzati sul .ch
- **`traumatologiasportiva.com`** — dominio di proprietà del cliente, **ereditato dal predecessore Prof. Matteo Denti**, oggi inutilizzato
- Instagram `@dr.dariogiunchi` · LinkedIn `in/dariogiunchi`
- Profili OneDoc multipli · local.ch · comparis.ch · Swiss Medical Network · Google Business Profile
- **Agenzia di comunicazione attuale: Spicca**

### Contesto professionale da verificare

Ha rilevato lo studio del **Prof. Matteo Denti** presso Ars Medica. Risulta un legame con la rivista **KSSTA** (Knee Surgery, Sports Traumatology, Arthroscopy) la cui natura esatta va accertata su fonte editoriale ufficiale. Su PubMed la ricerca `Giunchi D` restituisce lavori in gran parte di omonimi: **stabilisci con certezza quali pubblicazioni siano sue**, verificandole una per una.

---

## 4. GLI OBIETTIVI DEL CLIENTE — in ordine, e sono tre orizzonti diversi

1. **Breve termine:** massimizzare autorevolezza e introiti.
2. **Medio-lungo termine:** avviare altre attività finché il reddito chirurgico diventi **minoritario** e la chirurgia torni a essere un hobby.
3. **Lungo termine:** **smettere di lavorare** e limitarsi a gestire le aziende avviate.

**Il punto 3 detta tutto il resto.** Ogni raccomandazione va valutata anche così: *questa cosa produrrà reddito quando lui avrà smesso di operare, oppure no?*

### Gli otto progetti aperti — vanno tutti considerati

| | Progetto | Stato dichiarato |
|---|---|---|
| 1 | **PULSE** — software di sorveglianza scientifica automatizzata: interroga in continuo banche dati, riviste, atti congressuali, preprint, registri e linee guida, e consegna ogni mattina un quotidiano personalizzato sulle novità del proprio ambito | Prototipo funzionante a uso personale |
| 2 | **PROBUS** — il cliente lo ha indicato contemporaneamente come gestionale/SaaS per studi medici, piattaforma di raccolta dati clinici e di esito, e servizio/percorso clinico per pazienti | Da definire |
| 3 | **Azienda concorrente a Fisiorent** — noleggio e fornitura di ausili per la riabilitazione | Idea |
| 4 | **Libro sulla riabilitazione del crociato** | In pubblicazione |
| 5 | **Video documentario sulle tre generazioni** di chirurghi ancora viventi su cui è centrato il suo studio attuale — lui e i suoi due predecessori. Taglio umano | Idea |
| 6 | **Congressi** | Idea |
| 7 | **Società con Spicca**, o parallela, per la divulgazione medica: ritiene di essere il primo in Ticino a fare divulgazione medica con presenza massiva sui social, e vuole sfruttare la posizione | Idea |
| 8 | **`traumatologiasportiva.com`** | Dominio inutilizzato |

**Domanda strategica esplicita del cliente, a cui devi rispondere con una raccomandazione motivata:** questi progetti devono essere legati al suo nome e al suo volto, oppure restare marchi separati? La risposta può essere diversa progetto per progetto. Analizza i due scenari per ciascuno: vantaggi, rischi, reversibilità, effetto sulla reputazione clinica, effetto sulla vendibilità futura della società.

---

## 5. IL DESTINATARIO — vincolo di scrittura non negoziabile

Il report lo legge **una persona senza alcuna competenza informatica, con pochissimo tempo, quasi sempre dall'iPhone**.

1. **Spiega come lo spiegheresti a un bambino di dieci anni intelligente.** Ogni termine tecnico seguito subito da una spiegazione semplice fra parentesi e, quando aiuta, da un'analogia concreta.
2. **Mai un compito vago.** Non «ottimizza la scheda Google», ma: apri il browser, vai su questo indirizzo, clicca il pulsante blu in alto a destra, nel campo X cancella quello che c'è e scrivi Y, clicca Salva. Tempo: 3 minuti.
3. **Ogni azione a suo carico dura al massimo 10 minuti** e ha accanto: tempo stimato, che cosa vedrà sullo schermo, come capire che è andata a buon fine, che cosa fare se qualcosa non torna.
4. **Zero riempitivi.** Niente frasi motivazionali, niente disclaimer ripetuti. Stile elegante, professionale, asciutto.
5. **Il coinvolgimento totale del cliente resta sotto i 30 minuti** per l'audit e sotto le **2 ore al mese** per l'esecuzione. Ciò che richiede più tempo va delegato o scartato, e va detto esplicitamente.
6. **Preferisce essere corretto piuttosto che assecondato.** Se il sito è fatto male, dillo e mostra perché. Se un'abitudine comunicativa è controproducente, spiegalo.

---

## 6. FASE 1 — RACCOLTA DATI, tutta verificata aprendo le pagine

Lavora in autonomia, con sotto-agenti in parallelo sui blocchi indipendenti, poi consolida. **Salva gli screenshot su disco** e citali nel report.

### 6.1 Il sito `dariogiunchi.ch` — apri ogni pagina

- Mappa completa: `sitemap.xml`, `robots.txt`, navigazione, link interni, pagine orfane, sezione `/en/`
- Per **ogni** pagina: `<title>`, meta description, H1/H2, lunghezza e qualità del testo, immagini e testi alternativi, presenza di un passo successivo chiaro
- **Misure vere**: Lighthouse o PageSpeed Insights su mobile e desktop, Core Web Vitals, resa a 390 px, HTTPS, versione con e senza `www`, redirect, pagine di errore, accessibilità di base
- **Dati strutturati**: presenza di `Physician`, `MedicalBusiness`, `MedicalProcedure`, `FAQPage`. Verifica con il Rich Results Test
- **Indicizzazione**: `site:dariogiunchi.ch` — quante pagine, quali mancano e perché
- **Blog**: quanti articoli, data dell'ultimo, temi, se rispondono a ricerche reali dei pazienti
- **Verifica il tipo di redirect** di `dariogiunchi.it` e `dariogiunchi.com`: codice HTTP effettivo (301? 302? frame forward?) con `curl -I`
- **Verifica lo stato di `traumatologiasportiva.com`**: risponde? che cosa mostra? è indicizzato? ha cronologia e backlink ereditati dal Prof. Denti che valga la pena conservare?
- **Percorso di prenotazione dal telefono**: quanti tocchi e quanti campi separano un paziente dal fissare la visita, dove si perde, se il numero è cliccabile, se c'è WhatsApp, se c'è una risposta automatica
- **Limiti di Wix** nel contesto specifico: SEO multilingua, velocità, blog strutturato, integrazione CRM, raccolta di questionari di esito (PROMs), scalabilità verso i progetti imprenditoriali

### 6.2 Ricerca e visibilità — da IP svizzero, in finestra anonima

Che cosa vede davvero una persona che cerca, **con screenshot della prima schermata**, per: `ortopedico ginocchio Lugano` · `chirurgo ginocchio Ticino` · `ricostruzione crociato anteriore Lugano` · `operazione menisco Lugano` · `protesi ginocchio Lugano` · `protesi ginocchio robotica Ticino` · `specialista crociato Ticino` · `secondo parere ginocchio Svizzera` · `perito ortopedico assicurazione Ticino` · `Dario Giunchi` — più le varianti in tedesco, francese e inglese, e le stesse query ripetute per **Manno, Mendrisio, Chiasso, Locarno**.

Per ognuna: chi occupa le prime posizioni, con quale tipo di pagina, e perché. **Includi il blocco locale (Google Maps), che è il più cliccato da telefono.**

- **Ricerca keyword vera**: 40-60 ricerche con volume, difficoltà e intento presi da uno strumento reale (Keyword Planner, Semrush, Ahrefs). Dichiara lo strumento e la data. Se nessuno strumento è accessibile, **dillo e non stimare**
- **Google Business Profile**: quante schede esistono, per quali sedi, chi le gestisce, categorie, orari, foto, descrizione, domande e risposte, numero e qualità delle recensioni, tempo di risposta. Confronto con i concorrenti nella stessa area
- **Coerenza NAP** su tutte le directory: OneDoc (tutti i profili), Swiss Medical Network, local.ch, search.ch, comparis, doctorfmh/medici.ch, Doctena, medicosearch, Google Maps, Apple Maps, Bing. **Apri ogni scheda.** Segnala ogni incoerenza con l'indirizzo della pagina da correggere e con i dati esatti che vi compaiono
- **Verifica se qualche scheda riporti recapiti ereditati dallo studio del Prof. Denti**
- **Motori di risposta AI**: chiedi a ChatGPT, Perplexity, Gemini e alle AI Overviews «chi è il migliore specialista del ginocchio in Ticino» e «chi è Dario Giunchi». Riporta le risposte **verbatim** e valuta la sua citabilità

### 6.3 Social e contenuti — **entra nei profili, gli account sono autenticati**

Per Instagram e LinkedIn: numeri reali dagli Insights (follower, copertura, interazione, crescita), frequenza, formati, temi, tono, qualità del pubblico, contenuti riutilizzabili. Verifica se l'intestazione di LinkedIn esponga la qualifica clinica o un ruolo redazionale. Cerca inoltre Facebook, YouTube, TikTok, X.

### 6.4 Autorevolezza scientifica

Pubblicazioni indicizzate (PubMed, Google Scholar, ORCID, ResearchGate) **verificate una per una** per stabilire quali siano sue e quali di omonimi; h-index; ruoli editoriali — **accerta il rapporto con KSSTA su fonte editoriale ufficiale**; relazioni a congressi; società scientifiche (swiss orthopaedics/SGOT, ESSKA, ISAKOS, AGA, SIM); faculty e corsi. Quanto di tutto questo è **visibile e comprensibile** a un paziente e a un collega.

### 6.5 Reputazione

Tutte le recensioni pubbliche reperibili, con **testo** e analisi dei temi ricorrenti. Menzioni su stampa, TV, radio, podcast, siti terzi. Rischi: contenuti vecchi, profili abbandonati, omonimie, informazioni errate su siti terzi, sedi chiuse ancora pubblicate.

### 6.6 Analisi competitiva — da 8 a 12 confronti, con le pagine aperte

1. **Locali diretti** in Ticino e Svizzera italiana — in particolare **LogMedica** (`logmedica.ch`), che risulta il concorrente più strutturato, e i suoi chirurghi; EOC; Clinica Luganese Moncucco; Ortopedia Mendrisio; i singoli chirurghi del ginocchio che emergono
2. **Riferimenti nazionali** (Schulthess, Balgrist, Hirslanden, Ginevra) e **lombardi** (Humanitas, Galeazzi, San Raffaele, Rizzoli), per il rischio di fuga di pazienti
3. **Benchmark mondiali** nella comunicazione della chirurgia del ginocchio

Per ciascuno: che cosa fa meglio, che cosa è replicabile in Ticino con meno di 2 ore al mese, che cosa non lo è. Tabella di posizionamento.

---

## 7. FASE 2 — VALUTAZIONE

Punteggio da 0 a 10 per ciascuna dimensione, con **evidenza concreta (indirizzo della pagina o screenshot)**, distanza dal migliore della categoria, impatto economico stimato con il metodo dichiarato, grado di confidenza:

trovabilità su Google e sulle AI · coerenza dell'identità · qualità tecnica del sito · contenuti e capacità di rispondere alle domande dei pazienti · capacità di trasformare un visitatore in una richiesta di visita · Instagram · LinkedIn · visibilità dell'autorevolezza scientifica · reputazione e recensioni · presidio del segmento medico-legale e assicurativo · presidio dei colleghi invianti · multilingua e apertura oltre il Ticino · conformità normativa e deontologica · raccolta di dati e di pubblico proprio · preparazione al lancio dei progetti imprenditoriali.

### Cinque percorsi reali, ricostruiti passo per passo come un utente vero

- un trentenne che si rompe il crociato sciando ad Airolo e cerca dal telefono
- una signora di 68 anni con gonartrosi che ha sentito parlare di protesi robotica
- un collega di Zurigo o Milano che cerca a chi inviare una revisione di LCA complessa
- un avvocato o un gestore sinistri che cerca un perito ortopedico SIM in Ticino
- un'azienda medtech che valuta un key opinion leader per il ginocchio

Per ognuno indica **dove si interrompe il percorso e perché**.

### Capitolo obbligatorio: conformità

Che cosa è ammesso e che cosa no per un medico FMH in Svizzera e in Ticino: **LPMed art. 40 lett. d**; **Allegato 2 al Codice deontologico FMH** (che vieta l'informazione contenente raccomandazioni di pazienti, e vieta di sollecitare recensioni); **Legge sanitaria ticinese art. 70** e prassi dell'Ufficio di sanità (divieto di prestazioni gratuite e sconti); **LCSl**; **art. 321 CP** sul segreto professionale nelle risposte pubbliche; immagini pre/post-operatorie e consenso; **nLPD e GDPR**, cookie e strumenti di analisi; pubblicità a pagamento; **art. 55-56 LATer e OITAT** sui rapporti con l'industria.

**Scarica e leggi i testi normativi dalle fonti primarie** (fedlex.admin.ch, m3.ti.ch, fmh.ch, ti.ch): non citarli da fonti secondarie. Segnala i contenuti attuali a rischio e come correggerli. Dichiara il livello di certezza e quando serve un parere legale.

---

## 8. FASE 3 — CHE COSA CONSEGNARE

File veri e scaricabili, in italiano. **File 1 anche in PDF.**

1. **Report principale** — struttura: «In due minuti» (una pagina: i 5 problemi che costano di più, i 5 interventi che rendono di più, il verdetto sul sito) · assunzioni fatte · semaforo per canale · analisi delle 15 dimensioni con evidenze · i cinque percorsi paziente · analisi competitiva · conformità · i tre elenchi operativi · piano a 90 giorni e a 12 mesi mese per mese con responsabile · massimo 5 indicatori per capire se funziona, nessuno dei quali richieda competenze tecniche · «che cosa farei io al tuo posto» · rischi ed errori da non commettere, incluso che cosa non delegare mai all'agenzia
2. **Brief per Spicca** — documento separato, pronto da inoltrare: obiettivo, lavorazioni puntuali, specifiche tecniche precise, scadenze, criteri di accettazione, formati di consegna. In coda, **per il cliente e non per l'agenzia**, una sezione «come verificare che l'abbiano fatto davvero»: tre o quattro controlli da due minuti e le domande esatte da porre. Indica che cosa è ragionevole pagare in CHF, con intervalli
3. **Checklist stampabile di una pagina**
4. **Tabella keyword e piano dei contenuti (xlsx)**: ricerca, volume, intento, pagina di destinazione, priorità
5. **Calendario editoriale di 90 giorni**: 30 idee di post e 12 titoli di articoli scelti in base a ricerche reali, ciascuno con la traccia dei punti da toccare
6. **Kit testi pronti**: biografia breve/media/lunga in italiano e inglese, testo per la scheda Google, testi per le directory, modelli di risposta alle recensioni (positiva, negativa, ingiusta), tre script video da 60 secondi
7. **Nota strategica sui progetti imprenditoriali**, scritta per poter essere mostrata a un socio o a un investitore: posizionamento, analisi competitiva reale, difendibilità, vincoli legali e regolatori, modelli di ricavo, piano di validazione a 90 giorni, decisione sul rapporto con il brand personale
8. **Piano strategico sul portafoglio completo**, diviso in tre secchi espliciti: **che cosa fa il cliente di persona** · **che cosa delega a Spicca** · **che cosa richiede una ristrutturazione vera** (società, avvocato, fiscalista). Con: la classifica dei progetti per capacità di sostituire davvero il reddito chirurgico; la sequenza a cinque anni; e **l'ipotesi contraria** — un paragrafo onesto in cui argomenti perché una parte del piano potrebbe non valere la pena, e quale sarebbe la versione minima ma sufficiente

### Interventi maggiori da trattare esplicitamente

- **Il sito va rifatto o no?** Risposta netta, motivata, con i numeri. Se sì: quale piattaforma (Wix vs WordPress vs Webflow vs Framer sui criteri che contano per lui, incluso l'aggancio ai progetti imprenditoriali), costo realistico in CHF, tempi, chi ingaggiare, come riconoscere un buon fornitore, **come non perdere il posizionamento durante la migrazione**, che cosa salvare
- **Capitolato d'appalto già pronto** da mandare a 2-3 fornitori per preventivi confrontabili
- Architettura multilingua, sistema di prenotazione, CRM, questionari di esito (PROMs), newsletter, studio video, uso di `traumatologiasportiva.com`
- Per ciascuno: costo, tempo, rischio, ritorno atteso, e **la sequenza corretta** — che cosa va fatto prima di che cosa, e perché

---

## 9. METODO E QUALITÀ

- **Priorizza con un criterio esplicito** (impatto atteso × probabilità di successo ÷ sforzo) e mostra il calcolo in tabella
- **Costi in franchi svizzeri**, con intervalli e riferimento al mercato locale
- **Distingui sempre** ciò che è certo, ciò che è probabile, ciò che è opinione
- Non chiedere approvazioni intermedie: lavora fino alla consegna
- Prima di consegnare, **rileggi mettendoti nei panni di chi non sa nulla di informatica** e riscrivi ogni punto incomprensibile o ineseguibile. Poi fai un **secondo passaggio di verifica dei fatti**: controlla che ogni indirizzo citato esista davvero e che ogni numero sia corretto
- **In coda al report elenca che cosa non sei riuscito a verificare, e perché**

## 10. UNA SOLA TORNATA DI DOMANDE, POI AUTONOMIA

Prima di iniziare puoi porre **al massimo 8 domande**, tutte a scelta multipla con il default già indicato, così che il cliente possa rispondere con una riga di numeri o scrivere «usa i default». Copri solo ciò che non puoi verificare da solo: capacità residua di nuove visite private al mese, bacino geografico e lingue da presidiare, disponibilità a comparire in video e con quale frequenza, budget annuo, mandato e costo attuale di Spicca, eventuali vincoli imposti da Swiss Medical Network sulla comunicazione personale.

**Non fare altre domande dopo questa tornata.** Se il cliente risponde parzialmente, procedi con assunzioni ragionevoli elencandole in un box «Assunzioni che ho fatto — correggimi solo se sono sbagliate».

Quando hai finito, consegna i file e chiudi con un messaggio di **massimo dieci righe**: le tre cose da fare questa settimana, la decisione più importante da prendere, e che cosa ti serve da lui per la fase successiva.
