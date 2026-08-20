# PULSE — Benchmark (Fase 2, 20 agosto 2026)

Obiettivo: estrarre **meccanismi trasferibili** che riducano il time-to-insight o
aumentino la fiducia nel dato. Perimetro: solo clinico-chirurgico (Addendum 1 —
nessun pattern medico-legale valutato). Fonti: prodotti visitati/analizzati in
sessione (QxMD Read, NEJM Clinician, OpenEvidence, UpToDate — 19 agosto) e
letteratura di prodotto/design citata in coda.

---

## 1. Tabella comparativa (pattern → problema → applicabilità a PULSE)

| Prodotto | Pattern osservato | Problema che risolve | Applicabilità |
|---|---|---|---|
| Scite | Badge citazionale Supporting/Contrasting sull'articolo | «questo lavoro ha retto?» senza aprire nulla | **Alta** — il raccoglitore `destino` ha già i citanti; manca solo la classificazione visiva sul PICK passato |
| Consensus / Elicit | Filtro per **disegno di studio** (RCT, coorte, revisione) e quartile | triage per solidità, non per argomento | **Alta** — `design` è già in ogni scheda, oggi sepolto nel dettaglio |
| Semantic Scholar | TLDR di una riga sopra l'abstract | capire «di cosa parla» in 2 secondi | **Alta** — la riga `v` esiste già: va promossa tipograficamente, non creata |
| PubMed (limiti noti) | Lista di soli titoli, zero segnali di qualità | — (è il controesempio) | Nulla — è ciò da cui PULSE scappa |
| QxMD Read | Alert per keyword/collezioni | sorveglianza passiva | Già superato: lo screening del mattino è più selettivo |
| NEJM Clinician | Tipi editoriali dichiarati (Journal Watch / Guideline Watch) | sapere il *genere* prima del contenuto | **Media** — i «meta» delle schede già lo fanno; renderlo un'etichetta di prima classe |
| UpToDate / OpenEvidence | Grado dell'evidenza esplicito accanto alla raccomandazione | fiducia calibrata | **Media** — PULSE ha CONF+MUTE; unificarli in un unico segnale visivo coerente |
| Linear | Riga-lista densa a colonne stabili su griglia 4 px; azioni fuori dalla riga | scansione veloce di molte voci senza rumore | **Alta** — la scheda in lista oggi ha 6 azioni sempre visibili |
| Linear / Raycast | Command palette ⌘K | qualunque cosa in ≤2 gesti da tastiera | **Alta (desktop)** — su mobile l'equivalente esiste già: è il 🎙 |
| Superhuman | Split della lista per rilevanza (non filtri manuali) | prima ciò che ti riguarda | **Alta** — 🟠/🟢 sopra, ⚪ sotto, senza chiedere nulla |
| Superhuman | j/k da tastiera, velocità come feature | triage al ritmo del pensiero | **Media (desktop)** |
| Stripe | `tabular-nums`, numeri a destra, righe mute | leggere i numeri senza rileggerli | **Alta** — kpi, conteggi, barre |
| Stripe / FT | Gerarchia con tipografia e spazio, MAI col colore | il colore resta al significato | **Alta** — principio guida del sistema token |
| Bloomberg | Densità estrema ma **una** gerarchia dominante per riquadro | tanta informazione, un solo punto d'ingresso per blocco | **Media** — guida per la modalità compatta desktop |
| Things 3 | «Oggi» come concetto centrale; il giorno vuoto è uno stato di quiete, non di errore | il no-news con dignità | **Alta** — PULSE lo ha già nei testi; manca la dignità *visiva* |
| Readwise Reader / Reeder | Coda di lettura con posizione ricordata | riprendere dove si era | **Media** — la playlist auto già lo fa per l'audio; estendere alla lettura |
| GOV.UK | Il testo È l'interfaccia: verbi coerenti, un nome per azione | zero ambiguità | **Alta** — incoerenze rilevate in audit (Salva/★, Copia/Copiato) |
| Apple HIG | Azioni primarie nel terzo inferiore, target ≥44 pt | uso a una mano | **Alta** — tab oggi a metà pagina, sotto l'audiobar |
| Mercury/Monzo | Un numero-eroe per schermata, il resto in sordina | risposta prima dei dettagli | **Alta** — il verdetto del giorno come eroe |

## 2. I 15 pattern che rubiamo (ordinati per impatto sul time-to-insight)

1. **La prima schermata È la risposta** (Things 3, Mercury). Verdetto del giorno come blocco-eroe in cima: stato + data + un'unica frase; audiobar e tab scendono sotto. In PULSE: fusione dei due banner verdi in un solo blocco dominante.
2. **Render statico al build** (Core Web Vitals; il vantaggio di avere `costruisci.py`). La prima vista viene emessa come HTML già composto dal build del mattino: CLS da 0,855 → ~0, TBT giù, l'app non «salta» più. Nessun competitor statico può farlo meglio: i dati sono già lì.
3. **Split per rilevanza** (Superhuman). La lista si divide da sola: «Ti riguarda» (🟠🟢) sopra, «Contesto» (⚪) sotto. Il filtro manuale resta, ma non serve più per il caso comune.
4. **Riga-lista densa, azioni a scomparsa** (Linear; NN/g progressive disclosure). In lista: pallino · titolo · TLDR · rivista · disegno+n · età. Le 6 azioni compaiono solo a scheda aperta: da 54 bersagli a 9.
5. **TLDR tipograficamente dominante** (Semantic Scholar). La riga `v` subito sotto il titolo, corpo pieno; il resto dei metadati in sordina.
6. **Etichetta del disegno di studio in lista** (Consensus/Elicit). «RCT · 120» / «coorte · 1.406» / «consensus» come chip neutro: solidità visibile prima del tap.
7. **Badge del destino** (Scite). Sul PICK passato: «confermato da N / contrastato da N» quando il mattino ha classificato i citanti — fiducia calibrata nel tempo, unica nella categoria.
8. **Il giorno quieto come schermata migliore del prodotto** (Things 3, GOV.UK). Stato «niente ti riguarda oggi» grande, calmo, con i conteggi onesti sotto («9 lavori letti, 0 che ti toccano»).
9. **Sparkline dei 14 giorni** (Stripe). Micro-istogramma di HISTORY nell'intestazione: il polso del periodo in un colpo d'occhio, al posto dei chip «9 · ✓9/9» senza etichetta.
10. **Numeri tabellari allineati** (Stripe/FT). `font-variant-numeric: tabular-nums`, cifre a destra nelle righe con numeri.
11. **Tab in basso, pollice-first** (Apple HIG). Navigazione nel terzo inferiore su mobile; target ≥44 pt ovunque (già iniziato il 19 agosto).
12. **⌘K su desktop** (Linear/Raycast). Palette che riusa `interpretaComando`: stesso vocabolario della voce, zero logica nuova.
13. **Modalità compatta desktop dichiarata** (Bloomberg/Linear). Densità da scansione per i job 2–3: righe strette, confronto affiancato dei candidati alla newsletter.
14. **Un nome per azione, ovunque** (GOV.UK). «Salva→Salvata», «Copia→Copiato», «Ascolta→In lettura»: vocabolario unico UI+voce+toast.
15. **Skeleton solo dove c'è attesa vera** (Rassegna): struttura grigia delle sezioni al posto di «Carico…»; il resto della pagina non ha attese e non deve fingerne.

## 3. Cosa fanno tutti e noi NON faremo

- **Punteggi numerici di qualità** (0–100, stelle): il formato PULSE è un pallino solo, per scelta documentata («nove dimensioni che nessuno legge producono un totale che nessuno può contestare»).
- **Feed infinito e "related articles" in coda**: la sorveglianza ha un fondo; il giornale finisce, ed è un pregio (la seconda pagina è già l'estensione controllata).
- **Gamification** (streak, badge, obiettivi di lettura): il lettore è un pari, non un utente da trattenere.
- **Notifiche push**: il patto è «alle 7 è pronto»; l'attenzione la decide lui.
- **Sintesi AI in card senza fonte**: ogni frase resta tracciabile a PMID/DOI (Principio Zero); niente «AI summary» staccato dalla citazione.
- **Onboarding a tappe / tooltip tour**: benvenuto singolo + guida on-demand, già così.
- **Account, social, condivisione pubblica in-app**: prodotto per una persona.

## 4. L'errore sistematico della categoria (il vantaggio di PULSE)

**Tutti ottimizzano la ricerca; nessuno ottimizza la sorveglianza.** PubMed,
Semantic Scholar, Elicit, Consensus, perfino QxMD presuppongono un utente che
arriva con una domanda e fruga. La domanda quotidiana reale del chirurgo è
inversa: *«c'è qualcosa che deve raggiungermi oggi?»* — e su questa i competitor
rispondono con una lista vuota, che percepitamente è un fallimento. PULSE ha già
il «no» verificato come risposta di prima classe (0 è un conteggio con audit
dietro, non una rassicurazione): il redesign deve farne **il momento di maggiore
qualità visiva del prodotto** (pattern 1+8). Corollario dello stesso errore:
i competitor mostrano provenienza e metriche, mai **«che cosa cambia per te»** —
la riga `perte` di ogni scheda non ha equivalenti nella categoria, e in gerarchia
deve pesare quanto costa produrla.

---

Fonti principali: [Linear — design refresh](https://linear.app/now/behind-the-latest-design-refresh) · [analisi del sistema Linear](https://identityforge.io/learn/linear-design-system) · [Superhuman split inbox](https://blog.superhuman.com/how-to-split-your-inbox-in-superhuman/) · [analisi Stripe Dashboard](https://www.925studios.co/blog/stripe-dashboard-design-breakdown) · [GOV.UK Design System](https://design-system.service.gov.uk/) e [Design Principles](https://www.gov.uk/guidance/government-design-principles) · [progressive disclosure](https://en.wikipedia.org/wiki/Progressive_disclosure) · [confronto Elicit/Scite/Consensus](https://www.iatrox.com/blog/best-ai-tools-medical-research-2026-elicit-consensus-semantic-scholar-perplexity) · [Read by QxMD](https://www.qxmd.com/read-by-qxmd) · [NEJM Clinician](https://www.jwatch.org/).
