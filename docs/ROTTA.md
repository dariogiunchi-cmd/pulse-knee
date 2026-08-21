# CORREZIONE DI ROTTA — Addendum 4, punti 1–3

21 agosto 2026 · risponde all'Addendum 4 (§9, punti 1–3). Si ferma al punto 4 in
attesa di approvazione.

---

## 1. Come sono classificate e ordinate le notizie OGGI, nel codice

**L'ordinamento** delle schede è deciso dal mandato del mattino con una regola
scritta: «le schede, in ordine: rossi, arancioni, verdi, bianchi»
(`cervello/05-formato.md:64`). È un ordinamento **per impatto sulla pratica**,
non per dominio clinico: la conferma della diagnosi dell'Addendum.

**Gli assi di classificazione** esistenti, tutti e tre, sono praticocentrici o
non clinici:

1. **`dot`** per scheda (`dati/giorno.js`, campo `dot:'green'|'orange'|'red'|'gray'`)
   con legenda: 🔴 richiamo/ritiro · 🟠 «**contraddice o mette in discussione una
   tua tecnica**» · 🟢 riguarda una tua tecnica · ⚪ contesto
   (`cervello/05-formato.md:42`, `modello.html:834`). La cornice nasce nel
   cervello: `cervello/02-cosa-opera.md:116` la codifica come categoria n. 2 dei
   criteri di selezione.
2. **`sec`** (`res`/`disc`): ricerca vs «oltre il consueto». Binario, non un dominio.
3. **`TAGS`**: solo hashtag social e keyword SEO — non è una tassonomia.

**Dove è codificata la cornice «mette in discussione la tua pratica»:**

- **Nell'app online** (`main`, `modello.html:1363-1366`, `renderVerdict`): il
  titolo dominante della schermata è «N lavori mettono in discussione quello che
  fai» / «Oggi niente mette in discussione quello che fai». La lente È l'indice —
  il difetto principale, testuale.
- **Nel ramo `rifondazione/v3`** (completo, MAI fuso, in attesa di un «vai» che
  l'Addendum 4 rende superato): la cornice migrava in `SELEZIONE.testo` con il
  tetto di tre schede — selezione al posto della lente, ma sempre giudizio al
  posto dell'indice. **Anche questo è revocato**: il ramo non va fuso com'è.
- **Nessuna classificazione per dominio clinico esiste da nessuna parte**:
  «menisco», «cartilagine», «legamenti» non sono un campo dei dati, di nessuna
  variabile, di nessun test.

**Le altre due sezioni revocate, come stanno oggi:**

- `CONGRESSI=[]` (`dati/giorno.js:210`): vuoto, e l'app riempie il vuoto con la
  prosa di scuse «Nessuna scadenza verificata oggi: il raccoglitore notturno non
  copre ancora questa fonte» — telemetria come contenuto (conferma §6).
- `INDUSTRIA` contiene **solo i richiami openFDA** — la sorveglianza normativa al
  posto di prodotti e mercato (conferma §5). La duplicazione osservata nasce dal
  fatto che lo stesso richiamo compare in INDUSTRIA, nel briefing e nella
  Rassegna senza dedup fra superfici.

**Cosa del ramo `rifondazione/v3` sopravvive alla revoca** (validato, riusabile):
il giudizio unico ✓/✗ per PMID coi pesi emergenti · la consegna push via issue
GitHub · l'audio pre-generato Kokoro + feed podcast + dizionario di pronuncia ·
la sottrazione di benvenuto/tutorial/contatori · il lettore semplice.
**Cosa si butta**: SELEZIONE ≤3, il verdetto-selezione, la schermata a tre schede.

**Un dato utile già disponibile**: l'intestazione fattuale del §3.1 è derivabile
senza infrastruttura nuova — `AUDIT.visti` conta già i lavori esaminati (oggi:
29 esaminati, 9 schede + 10 brevi + 2 scoperte = 21 rilevanti mostrati).

---

## 2. La tassonomia dei domini, mappata sulle fonti attuali

| # | Dominio | Fonte oggi | Adeguata? |
|---|---|---|---|
| 1 | Menisco | Screening PubMed del mandato (ricerche per tecnica + termine-nucleo) | **Sì** come copertura; **manca solo il campo**: nessuna scheda porta il dominio. Serve `dom:` per scheda/breve, assegnato dal mandato, valori chiusi verificati dal cancello |
| 2 | Cartilagine | idem | idem |
| 3 | Legamenti (LCA, LCP, periferia, multileg.) | idem | idem |
| 4 | Altra artroscopia e procedure affini | idem | idem |
| 5 | Osteotomie | idem | idem |
| 6 | Protesi (mono/totale, robotica) | idem | idem |
| 7 | Traumatologia del ginocchio | idem — oggi sotto-cercata (la rete di ricerca è centrata su artroscopia) | **Parziale**: aggiungere un ramo di ricerca dedicato allo screening |
| 8 | Riabilitazione e return to sport | idem — presente ma non sistematica | **Parziale**: idem |
| 9 | Linee guida e consensus | raccolta `linee_guida` (PubMed, tipi consensus/guideline, 60 gg) | **Sì** — ha già intercettato il consensus tedesco del 20 agosto |
| 10 | Congressi | **NESSUNA fonte automatica** (CONGRESSI scritto a mano, di fatto vuoto) | **NO**. Proposta sotto |
| 11 | Industria e mercato | Solo openFDA richiami + Swissmedic | **NO** per il nuovo scopo. Proposta sotto |

**Congressi — proposta.** Le date e scadenze congressuali non hanno un'API: la
soluzione onesta è un deposito curato `fonti/congressi.json` (i 13 richiesti:
ESSKA, ISAKOS, ICRS, AAOS, AOSSM, EFORT, SIAGASCOT, SIOT, Swiss Orthopaedics,
AGA, SFA, APKASS + corsi europei di ginocchio), con sigla · città · date ·
scadenza abstract · early bird · url, compilato una volta con verifica fonte per
fonte e **riverificato mensilmente dal mandato** (le scadenze cambiano poco).
Il raccoglitore lo legge e calcola le evidenze (≤30 gg, ≤7 gg); l'app ordina per
scadenza. La riga di copertura dichiara «Fonti congressuali coperte: N su 13».

**Industria e mercato — proposta.** Nuovo modulo `industria` del raccoglitore
notturno (i runner GitHub escono su internet):

- **Stampa di settore via RSS** (feed pubblici): MassDevice, Medical Design &
  Outsourcing, Fierce Medtech, Orthopedics This Week/OrthoSpineNews dove il feed
  esiste — filtro per ginocchio e per le ~20 aziende sorvegliate (lista §5
  dell'Addendum, che estende le 8 attuali di `PREF_AZ`).
- **openFDA 510(k)/De Novo** (API già in uso per i richiami): le AUTORIZZAZIONI
  di dispositivi ginocchio — il segnale che precede il lancio.
- **Comunicati/IR aziendali via RSS** dove pubblicati.
- **EUDAMED**: nessuna API stabile — copertura dichiarata assente, non finta.
- **Dedup a monte** per titolo normalizzato + azienda; i richiami scivolano in
  coda e compaiono SOLO quando nuovi (memoria degli già-visti nel deposito).
- Il mandato riscrive le voci in righe (grammatica §3.3) e le verifica come ogni
  altra affermazione: PRINCIPIO ZERO invariato.

Una notizia come «J&J mette in vendita DePuy Synthes» arriva da stampa di settore
e IR: con queste fonti sarebbe intercettata (prova di copertura richiesta al §8.1
da eseguire in implementazione, prima dell'interfaccia).

Polso social, preprint, destino dei verdetti, video: restano in Rassegna/archivio
— non sono domini dell'indice quotidiano.

---

## 3. Wireframe ASCII — la schermata «Oggi» nuova (390 px)

### Caso A — giornata leggera (5 voci)

```
┌─────────────────────────────────────────────┐
│ PULSE · knee                             ↻  │
│                                             │
│ Giovedì 21 agosto                           │
│ 29 lavori esaminati · 5 rilevanti           │  ← misura, non giudizio
│                                             │
│ ┌─────────────────────────────────────────┐ │
│ │ IN EVIDENZA                             │ │  ← uno solo, due righe
│ │ La Kniegesellschaft raccomanda la       │ │
│ │ correzione individualizzata dello slope │ │
│ │ consensus 14 esperti · KSSTA            │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│ LEGAMENTI 2                                 │
│ · Sopra i 10° di slope la ri-rottura del    │
│   crociato quasi raddoppia                  │
│     coorte 1406 · J Exp Orthop          ●   │  ← ● = tocca la tua pratica
│ · Il nervo cutaneo femorale rischia al      │
│   margine superiore del prelievo QT         │
│     cadavere 29 · Surg Radiol Anat          │
│                                             │
│ MENISCO — nulla oggi                        │  ← dominio vuoto: una riga
│ CARTILAGINE — nulla oggi                    │
│ PROTESI 1                                   │
│ · La bi-mono compartimentale recupera più   │
│   in fretta della totale nei primi 2 anni   │
│     coorte IPTW 80 · Orthop Surg            │
│ RIABILITAZIONE 1                            │
│ · Sigarette elettroniche: più complicanze   │
│   dopo artroscopia di menisco               │
│     coorte appaiata · Orthopedics           │
│ LINEE GUIDA — nulla oggi                    │
│ CONGRESSI 2  (scadenza più vicina: 12 set)  │
│ INDUSTRIA E MERCATO 1                       │
│                                             │
│ ▶ Briefing · 3 min                          │
│ Copertura: 9 fonti su 10 · dettaglio        │  ← l'UNICA riga di sistema
│ Archivio · Produzione · Profilo             │
└─────────────────────────────────────────────┘
```

### Caso B — giornata piena (25 voci): stessa struttura, tempo costante

```
┌─────────────────────────────────────────────┐
│ Giovedì 21 agosto                           │
│ 63 lavori esaminati · 25 rilevanti          │
│                                             │
│ ┌ IN EVIDENZA ────────────────── 2 righe ┐  │
│                                             │
│ MENISCO 4                              [–]  │  ← richiudibile
│ · riga · riga · riga · riga                 │
│ CARTILAGINE 2                          [–]  │
│ · riga · riga                               │
│ LEGAMENTI 6                            [–]  │
│ · riga ● · riga · riga · riga · riga · riga │
│ ALTRA ARTROSCOPIA 3                    [–]  │
│ OSTEOTOMIE 1                                │
│ PROTESI 4                              [–]  │
│ TRAUMATOLOGIA — nulla oggi                  │
│ RIABILITAZIONE 2                            │
│ LINEE GUIDA 1                               │
│ · L'ESSKA pubblica il consensus sulle       │
│   suture meniscali in lesione radiale       │
│     consensus formale · KSSTA           ●   │
│ CONGRESSI 3   scadenza vicina: ISAKOS 7 gg  │  ← evidenza forte ≤7 gg
│ · ISAKOS · Monaco · 6-9 giu · abstract:     │
│   28 ago · early bird: 15 ott               │
│ INDUSTRIA E MERCATO 2                       │
│ · J&J esplora la cessione di DePuy Synthes  │
│     Reuters/IR · mercato                    │
│ · Smith+Nephew ottiene il 510(k) per il     │
│   sistema meniscale X                       │
│     FDA 510(k) · prodotto                   │
│                                             │
│ ▶ Briefing · 6 min                          │
│ Copertura: 9 fonti su 10 · dettaglio        │
│ Archivio · Produzione · Profilo             │
└─────────────────────────────────────────────┘
```

Regole comuni (dal §2-3 dell'Addendum):

- Riga = fatto col verbo, ≤ ~90 caratteri · fonte · marcatore disegno+numerosità.
  La grammatica diventa una **sentinella del cancello** (lunghezza, niente
  paragrafi, niente parole di sistema — prove §8.3 e §8.5 meccanizzate).
- ● discreto = «tocca la tua pratica»: etichetta filtrabile in archivio, mai
  cornice. Legenda in un tap sul primo uso del segno.
- 1 tap sulla riga → la scheda (profondità 2); dalla scheda → fonte originale
  (profondità 3). Il giudizio ✓/✗ (che resta, per PMID, coi pesi) vive nella
  scheda, non sulla riga: l'indice si scorre, non si comanda.
- Dominio vuoto = una riga contratta. Nessun conteggio di arretrati, nulla scade
  in debito.
- I contenuti esistenti (EXTRA brevi compresi) confluiscono nell'indice del loro
  dominio: la distinzione scheda/breve resta solo nella profondità (breve = riga
  con scheda ridotta), mai nell'indice.

### Nota di conflitto, dichiarata (Addendum §10)

Piccola tensione fra §3.1 e §6: il §3.1 mette «9 fonti su 10 raggiunte»
**nell'intestazione**, il §6 ordina di consolidare la copertura delle fonti in
**una riga in fondo**. Propongo la lettura coerente adottata nei wireframe:
l'intestazione dichiara la misura del **contenuto** (esaminati · rilevanti), la
riga di fondo la misura del **sistema** (fonti raggiunte · dettaglio). Se
preferisci le fonti in testa, è uno spostamento di una riga.

Nessun'altra istruzione dell'Addendum 4 mi risulta in conflitto con l'obiettivo
della sezione 1. Il vincolo dei 60 secondi cambia natura ma resta meccanizzabile:
non più budget di parole della selezione, ma budget di **righe per voce** (1) e
grammatica verificata dal cancello — il tempo di scorrimento resta costante
perché cresce solo la lunghezza della pagina, non il costo di orientamento.
