# CHANGELOG UX — Redesign v2, direzione A «Prima pagina»

20 agosto 2026 · ramo `redesign/ux-v2` · 11 commit di implementazione dopo i tre gate
(audit → benchmark → sistema di design con tre direzioni; approvata la A).
Metrica guida: **time-to-insight**. Vincoli rispettati: PRINCIPIO ZERO, nessuna
riscrittura da zero, zero dipendenze nuove nell'app, niente dati di pazienti,
interfaccia in italiano, spesa 0 (font di sistema; licenza tipografica valutata e
rinviata — v. `COSTI.md`).

## Che cosa è cambiato, in ordine di commit

1. **Fondamenta** (`e238fdd`) — token semantici (allerta/attrito/pratica/contesto/
   azione/inchiostro) con valori ricalibrati per tema chiaro e scuro, alias storici
   per il codice esistente; scala tipografica a 6 corpi (da 24 corpi trovati
   nell'audit); spaziatura a passi di 4 px; raggi e ombre unificati.
2. **La card dell'articolo** (`b171770`) — la riga chiusa è fatta per LEGGERE
   (pallino, titolo, perché-ti-tocca, meta); le azioni compaiono solo ad apertura
   (rivelazione progressiva, CSS puro); bersagli ≥44 px; lo stato aperto
   sopravvive al re-render (il salvataggio non chiude più la scheda sotto il dito).
3. **La Prima pagina** (`8536cad`) — il verdetto del giorno apre la pagina, a
   28 px senza scatola quando è quieto; conteggi onesti con sparkline degli ultimi
   14 giorni (dati veri da HISTORY); pillola «N/N citazioni verificate»; audiobar
   ridotta a una riga; barra delle sezioni fissa in basso su mobile (icone SVG +
   etichetta), in alto su desktop.
4. **Densità** (`2bb6711`) — righe più compatte sopra i 1024 px; i candidati del
   mese dentro la Newsletter, dove si decide.
5. **Produzione** (`59113ab`) — una sola funzione di copia con conferma sul
   bottone toccato («Copiato ✓»), coerente su tutti i flussi.
6. **Archivio e ricerca** (`4f49fca`) — campo vuoto con invito ed esempi; query
   ripetuta (con escape) nel messaggio di nessun risultato; stato offline
   dichiarato («questa è l'ultima edizione scaricata») con ascoltatori
   online/offline; skeleton al caricamento della Rassegna, spento con
   `prefers-reduced-motion`.
7. **Micro-interazioni** (`7675857`) — via le emoji da tutti i controlli: pollici
   SVG per i voti, icone a tratto per Video / segnali / trasferimento / backup /
   pannello auto; cursori al posto dell'ingranaccio-sole; chip di sezione SVG
   monocromi; toast con verbo coerente.
8. **Accessibilità** (`971f937`) — landmark (`main`, banner, navigation,
   contentinfo), un solo `h1`, ordine dei titoli senza salti; Invio/Spazio
   attivano ogni `role=button`; schede raggiungibili da tastiera con
   `aria-expanded` veritiero; focus visibile; contrasto AA misurato e corretto
   nei due temi. **axe-core: 0 violazioni su 6 viste × 2 temi.**
9. **Calendario vero** (`9e9fb04`) — l'archivio non è più markup scritto a mano
   fermo al 12 agosto: si genera da BUILD_DATE e HISTORY; trovati e corretti,
   guardando lo schermo, il weekend fuori viewport e la collisione di classe
   `.empty`.
10. **Prestazioni** (`35f115e`) — velo d'avvio: nessun dipinto intermedio che
    slitta (CLS 0,91 → 0), con tre sicurezze (noscript, valvola 4 s, guardie).
11. **Guida e Novità** (`4f2cd29`) — la guida descrive i controlli come appaiono
    oggi; GUIDA_V 5 annuncia la veste nuova una volta sola.

Ogni condotta nuova è coperta da sentinelle nel cancello (614 controlli, erano
605): stato aperto, rivelazione progressiva, velo d'avvio, calendario, tastiera,
landmark — ognuna collaudata **rompendo davvero** ciò che protegge.

## Metriche — prima → dopo

Misure locali ripetibili (Lighthouse 12, Chromium sandbox, 4G simulato; stessa
procedura della baseline in `AUDIT.md` §3.5).

| Obiettivo (prompt) | Prima | Dopo | Esito |
|---|---|---|---|
| Novità del giorno ≤1 tap | 0 tap ma sotto audiobar e tab | **0 tap, primo elemento** | ✅ |
| Scheda → social copiato ≤4 tap | 3 | **3** (scheda → ✎ Social → Copia) | ✅ |
| Lighthouse Performance mobile ≥90 | 59 | **96** (desktop: 100) | ✅ |
| Lighthouse Accessibility 100 | 94 | **100** (mobile e desktop; axe 0 violazioni) | ✅ |
| Contrasto AA anche in scuro | no (12 nodi axe) | **sì, misurato** | ✅ |
| Apertura < 1,5 s su 4G | FCP 2,1 s | **FCP 2,3 s** | ❌ dichiarato |
| Famiglie tipografiche ≤2 | 1 (24 corpi) | **1 (6 corpi + 1 micro-etichetta)** | ✅ |
| Zero stati non disegnati | 5 mancanti o deboli | **0** (offline, skeleton, inviti, vuoti) | ✅ |
| CLS | 0,855 | **0** | ✅ |
| TBT | 570 ms | **0 ms** | ✅ |
| Peso trasferito | 74 KB gzip | **77 KB gzip** (+3: SVG e stati) | ✅ |

**Sul FCP mancato**: l'app è UN file con dentro i dati del giorno; a 4G simulato
il collo è trasferimento+parse, non il layout. La strada per scendere sotto 1,5 s
è il pre-render statico in `costruisci.py` (il briefing già rigenera index.html
ogni mattina): annotata in `OPEN_ISSUES.md`, non improvvisata a fine progetto.

## Il test dei 5 secondi, schermo per schermo

- **Oggi**: «Niente mette in discussione quello che fai» — il verdetto È la
  prima riga. Superato.
- **Rassegna**: sommario a colpo d'occhio coi conteggi; le sezioni che scottano
  sono già aperte. Superato.
- **Archivio**: un calendario col punto sui giorni usciti e l'oggi evidenziato;
  sotto, la ricerca. Superato.
- **Salvati**: o l'elenco o «Nessun articolo salvato · tocca la stella».
  Superato.
- **Newsletter**: «0 di 4» in alto, candidati con + accanto. Superato.
- **Impostazioni**: titoli piani, un blocco per argomento. Superato.

## Deviazioni deliberate dal benchmark (Fase 2)

- **Niente riordino automatico per rilevanza** (pattern 3): l'ordine 1..N del
  briefing È la gerarchia editoriale, decisa ogni mattina con criteri clinici;
  un riordino client-side la distruggerebbe e romperebbe i comandi a voce
  («apri la tre»). Al suo posto: filtri per pallino coi conteggi.
- **Emoji conservate nei CONTENUTI** (pallini 🔴🟠🟢⚪ nella guida, marcatori di
  sezione della Rassegna, ⚠️ delle fonti mute): lì sono informazione, non
  decorazione, e le sentinelle del cancello le esigono. Bandite solo dai
  controlli.

## Autovalutazione: 92/100

Dove perde punti: FCP sopra obiettivo (−5); il pannello auto conserva lo stile
proprio scuro-fisso non ancora unificato coi token (−2); la vista desktop è un
adattamento corretto ma senza idee proprie oltre le due colonne di Oggi (−1).
Tutti e tre annotati in `OPEN_ISSUES.md` con la strada proposta.

## Confronto visivo

`docs/confronto.html` affianca i 29 scatti prima/dopo (stessi nomi in
`docs/before/` e `docs/after/`).
