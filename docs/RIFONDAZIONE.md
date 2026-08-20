# RIFONDAZIONE — diagnosi con evidenze e schermata unica

20 agosto 2026 · ramo `rifondazione/v3` · risponde all'Addendum unificato, sezione 17,
punti 1–4. Le misure sono prese sull'app appena pubblicata (main `fde5750`), con
Playwright sul contenuto reale del 20 agosto.

---

## 1. Le tre cause di difficoltà, verificate nel codice

### 1.1 Il prodotto è «pull» — CONFERMATO, senza eccezioni

Non esiste **alcun canale che porti il contenuto all'utente**:

- I cinque workflow (`.github/workflows/`) sono: `cancello` (CI), `raccolta`
  (deposito json), `ripristino` (collaudo mensile), `chiedi-deploy` (in attesa di
  chiavi) e `battito` — che invia un'email **solo quando il briefing NON arriva**
  (rilevatore di guasto, non consegna di contenuto).
- Nell'app, l'unico accenno a una notifica è `askNotif()` (`modello.html:1026`):
  chiede il permesso per gli **avvisi del browser**, che su iPhone funzionano solo
  con la PWA in Home Screen, e comunque sarebbero un *promemoria di aprire*, non il
  contenuto.
- Il contenuto vive esclusivamente dentro `index.html` servito da GitHub Pages:
  per sapere cosa è successo, bisogna ricordarsi di andare a prenderlo.

### 1.2 Il costo è nelle decisioni — CONFERMATO, misurato

Elementi interattivi **visibili** per vista (Playwright, `button/[role=button]/
[onclick]/input/a` visibili, 390 px, 20 agosto):

| Vista | Elementi interattivi |
|---|---|
| Oggi | 29 (più 5 azioni per ognuna delle 9 schede quando aperta) |
| Newsletter | 17 |
| Impostazioni | **85** |
| Archivio | 2 · Salvati 1 · Rassegna 0 (fetch) |

Decisioni distinte che la giornata tipo propone (con la funzione che le genera):

1. Quale filtro-pallino usare — 4 chip (`fchip`).
2. Per **ognuna** delle 9 schede: aprire? salvare (`toggleSave`)? utile/non utile
   (`vote`)? generare social (`openSocial`, `modello.html:943`)? sceglierla per il
   video (`pickWeek`)? — 5 azioni × 9 schede = 45 scelte possibili sul percorso.
3. Il foglio social: 3 toni × 3 lunghezze × 4 formati = **36 combinazioni**
   (`setTone` :602, `curTone/curLen/curFmt` :562) più «Adatta».
4. Newsletter: scegliere fino a 4 lavori fra 9, poi 3 versioni del testo.
5. «Sorprendimi» e la seconda pagina (10 brevi in più oggi): leggere o no.
6. I suggerimenti del focus (`acceptSugg` :741): accettare o respingere.
7. Le 5 tensioni aperte: sempre lì, ogni giorno, da riconsiderare.

Il redesign ha ridotto i **tap** (3 per il testo social) ma nessuna di queste
**decisioni** è stata tolta. È la conferma della diagnosi: il costo percepito non
stava nei pixel.

### 1.3 Personalizzazione = configurazione — CONFERMATO, con l'aggravante del giro manuale

- Le liste curate in Impostazioni contengono oggi **55 voci** (10 riviste, 23
  opinion leader, 14 società, 8 aziende), tutte gestite a mano con `addItem`
  (`modello.html:717`) — aggiungi/rimuovi, campo per campo.
- Il giudizio dell'utente (`S.votes`) **non modifica da solo la selezione**: viene
  tradotto in testo da `segnaliTesto()` che l'utente deve **copiare e incollare
  nella chat con Claude** perché il mattino successivo ne tenga conto
  (`cervello/claude__07-preferenze.md`). Il ciclo di apprendimento esiste, ma ha
  dentro un lavoro manuale dell'utente: è personalizzazione trasformata in
  commissione.

### 1.4 Consumo e produzione mescolati — CONFERMATO

`itemHTML` (`modello.html:645`) inietta su **ogni** scheda di lettura i controlli
di produzione «✎ Social» e «Video». La Newsletter è una delle 6 voci della barra
principale. Il momento del consumo (aggiornarsi, ogni mattina) e il momento della
produzione (contenuti, settimanale) condividono schermata, gerarchia e attenzione.

---

## 2. Verifica empirica delle voci del browser (Addendum §9)

- **Chromium del sandbox (Linux, headless)**: `speechSynthesis.getVoices()` →
  **lista vuota** `[]`. Nessun motore di sintesi installato: qui la lettura ad
  alta voce non esiste proprio.
- **iPhone (Safari)**: non posso eseguire codice sul dispositivo da questa
  sessione. Ma il dato empirico c'è già, ed è stato pagato: il 19–20 agosto
  l'utente ha **installato Emma Premium a livello di sistema** e il browser ha
  continuato a riprodurre Alice; l'app ha dovuto introdurre una classifica delle
  voci (`_ordinaVoci`) e un selettore manuale. Il selettore voce in Impostazioni
  elenca esattamente ciò che Safari espone: è la prova visibile sul dispositivo,
  senza console.
- Conclusione di piattaforma (coerente con la documentazione Apple): le voci
  Premium/Enhanced sono destinate ad accessibilità e Siri; l'API web ne espone un
  sottoinsieme e tipicamente serve la variante **compatta** anche a nome uguale.
  **Nessun codice nel browser può accedere a Emma Premium.** La sezione 10
  dell'Addendum (audio pre-generato) è l'unica strada, e risolve per costruzione
  anche l'interruzione sui testi lunghi e la resa incoerente fra dispositivi.

---

## 3. La schermata unica — wireframe ASCII (390 px)

### Caso A — giorno vuoto (stato di successo, chiuso in 10 secondi)

```
┌─────────────────────────────────────┐
│                                     │
│  Giovedì 20 agosto                  │
│                                     │
│  Oggi niente di rilevante.          │
│  Letteratura controllata alle 5:04. │
│                                     │
│                                     │
│                                     │
│                                     │
│                                     │
│                                     │
│                                     │
│                                     │
│  ▶ Briefing di 40 secondi           │
│                                     │
│  ┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄   │
│  Archivio · Produzione · Profilo    │  ← una riga di testo, in fondo,
└─────────────────────────────────────┘    discreta. Non una barra di tab.
```

### Caso B — un articolo

```
┌─────────────────────────────────────┐
│  Giovedì 20 agosto                  │
│                                     │
│  Un lavoro che ti riguarda:         │
│  lo slope tibiale nella             │
│  revisione dell'LCA.                │
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ COSA DICE                       │ │
│ │ Sopra i 12° di slope, il        │ │
│ │ fallimento della revisione      │ │
│ │ raddoppia (18% vs 9%).          │ │
│ │                                 │ │
│ │ ◐ coorte, 402 ginocchia · AJSM  │ │  ← un solo indicatore di solidità
│ │                                 │ │
│ │ COSA CAMBIA PER TE              │ │
│ │ Nelle revisioni con slope alto, │ │
│ │ misurarlo prima diventa         │ │
│ │ difficile da evitare.           │ │
│ │                                 │ │
│ │ Lo vedi perché operi revisioni  │ │  ← toccabile: corregge la selezione
│ │ LCA ›                           │ │
│ │                                 │ │
│ │   ✓ utile        ✗ non utile    │ │  ← l'unica azione. Punto.
│ └─────────────────────────────────┘ │
│                                     │
│  ▶ Briefing · 3 min                 │
│  ┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄   │
│  Archivio · Produzione · Profilo    │
└─────────────────────────────────────┘
```

### Caso C — tre articoli (il massimo, sempre)

```
┌─────────────────────────────────────┐
│  Giovedì 20 agosto                  │
│                                     │
│  Tre novità. Una conta davvero.     │
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ Sopra i 12° di slope il         │ │
│ │ fallimento della revisione      │ │
│ │ raddoppia (18% vs 9%).          │ │
│ │ ● coorte 402 · AJSM             │ │
│ │ Cambia la tua pianificazione ›  │ │
│ │   ✓ utile        ✗ non utile    │ │
│ └─────────────────────────────────┘ │
│ ┌─────────────────────────────────┐ │
│ │ Il nervo safeno si risparmia    │ │
│ │ spostando il prelievo 2 cm      │ │
│ │ prossimale (studio anatomico).  │ │
│ │ ◔ cadaverico 29 · SRA           │ │
│ │ Non cambia la tua tecnica ›     │ │
│ │   ✓ utile        ✗ non utile    │ │
│ └─────────────────────────────────┘ │
│ ┌─────────────────────────────────┐ │
│ │ (terza scheda, stessa forma)    │ │
│ └─────────────────────────────────┘ │
│                                     │
│  ▶ Briefing · 5 min                 │
│  ┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄   │
│  Archivio · Produzione · Profilo    │
└─────────────────────────────────────┘
```

Regole comuni ai tre casi:

- **Zero tap** per arrivarci: è la schermata d'ingresso.
- «✓ utile / ✗ non utile» è **l'unica azione primaria** (swipe equivalente su
  mobile); «utile» archivia anche la scheda, senza stella separata. Il giudizio
  aggiorna i pesi della selezione **da solo** — il giro «Manda i segnali» sparisce.
- La riga «Lo vedi perché … ›» è insieme trasparenza e comando: toccata, offre
  «meno lavori così» / «più lavori così» / «questo tema non mi interessa».
- ▶ riproduce l'**MP3 pre-generato** del giorno (un pulsante, ±15 s, velocità),
  lo stesso episodio del feed podcast.
- La riga in fondo (Archivio · Produzione · Profilo) è testo discreto: porta ai
  mestieri secondari senza promuoverli. Su desktop identica, centrata.
- Il verdetto può dichiarare, senza contatore persistente, «Altre sei in
  archivio, nessuna decisiva»: scade col giorno, non torna domani.
- Se un'allerta della Rassegna scotta (richiamo su azienda sorvegliata,
  ritrattazione su un lavoro citato), **entra nel verdetto** — non in una
  sezione parallela da ricordarsi di aprire.

---

## 4. Dove va decisa la selezione (nota strutturale)

Il tetto di tre non è una regola dell'interfaccia: è una regola **del mandato del
mattino** (`cervello/claude__13-attivita.md`). È la sessione delle 5 che deve
scegliere gli 0–3 lavori e scrivere il verdetto in linguaggio naturale; l'app
mostra ciò che riceve. La rifondazione tocca quindi tre luoghi, con lo stesso
peso: il mandato (selezione e voce del verdetto), i dati (`dati/giorno.js`:
schema nuovo, più piccolo), l'app (schermata unica). Il cancello va aggiornato di
conseguenza, sentinella per sentinella, insieme al codice.
