# PULSE — Sistema di design (Fase 3, 20 agosto 2026)

Metro unico: **time-to-insight** e fiducia nel dato. Tutto ciò che non serve a uno
dei due è rumore.

---

## 1. Palette — il colore è informazione

Sei valori semantici. Se un colore non codifica un significato, non esiste.

| Token | Chiaro | Scuro | Significato (unico) |
|---|---|---|---|
| `--allerta` | `#C0362C` | `#FF6B5E` | richiamo dispositivo · ritrattazione · contrasta un verdetto |
| `--attrito` | `#B45309` | `#F5A524` | mette in discussione una tua tecnica |
| `--pratica` | `#1E7A3C` | `#4ADE80` | riguarda le tue tecniche, senza conflitto · giorno quieto · conferma |
| `--contesto`| `#8A8A8E` | `#98989D` | nel perimetro, non tocca la pratica |
| `--azione` | `#0A63C4` | `#4B9FFF` | UNICO colore interattivo: link, bottoni primari, focus |
| `--inchiostro` + neutri | `#1B1B1E` su `#FFFFFF`/`#F4F4F6` | `#F2F2F4` su `#000`/`#151517` | testo, superfici, linee (`--dim`, `--linea`, `--fondo`, `--carta`) |

Regole: il verde/arancio/rosso NON si usano mai per decorare; il blu NON si usa
mai per informare; la gerarchia si fa con peso e dimensione, mai col colore.
Dark mode: token ridefiniti (già così), con i semantici ricalibrati per contrasto
AA su fondo scuro — non un'inversione automatica. Contrasto: tutte le coppie
testo/fondo ≥4,5:1 (verificato in Fase 5 con l'audit automatico).

## 2. Tipografia — una famiglia, sei corpi

**Famiglia: system stack** (`-apple-system, "SF Pro Text", Segoe UI, Roboto,
sans-serif`). Decisione argomentata: sull'iPhone — l'uso prevalente — SF Pro È il
volto professionale nativo, pesa 0 KB, niente FOUT sulla pagina critica da 74 KB.
Alternativa valutata e scartata: Inter self-hosted (gratuita, +~90 KB, identità
propria su desktop) — riproponibile in un commit se si vorrà un volto distinto;
nessuna licenza a pagamento necessaria (v. docs/COSTI.md).

Scala dichiarata (da 24 corpi attuali a **6 token**):

| Token | px / lh | Uso |
|---|---|---|
| `--t-eroe` | 28 / 34 | verdetto del giorno, stato quieto |
| `--t-titolo` | 20 / 26 | titoli di sezione e di scheda aperta |
| `--t-testo` | 17 / 26 | titolo in lista, corpo di lettura |
| `--t-secondario`| 15 / 22 | TLDR (`v`), testi di interfaccia |
| `--t-meta` | 13 / 18 | metadati, chip, etichette |
| `--t-micro` | 11 / 14 | contatori, timestamp |

Pesi: 400 / 600 / 700. Numeri: `font-variant-numeric: tabular-nums`, allineati a
destra dove in colonna. Collaudo con casi estremi reali (titoli AJSM ≥140
caratteri pieni di sigle): il troncamento è a 2 righe con ellissi in lista, mai a
metà parola scientifica.

## 3. Spaziatura e raggi

Griglia **4 px**: `--s1..--s7` = 4·8·12·16·24·32·48. Raggi: `--r1` 8 (chip),
`--r2` 12 (card), `--r3` 16 (pannelli). Niente valori fuori scala.

## 4. Densità — due modalità dichiarate

- `comoda` (default mobile): righe lista 64–72 px, bersagli ≥44 pt, lettura.
- `compatta` (default ≥1024 px, attivabile): righe 40–44 px, colonne allineate,
  scansione — il tavolo del verdetto settimanale. Non è responsive implicito: è
  un attributo (`data-densita`) con token propri.

## 5. Componenti — la card dell'articolo prima di tutto

**Card in lista (chiusa)** — risponde alle 4 domande in un colpo d'occhio:

```
● Il ginocchio tedesco raccomanda un approccio        ← titolo, 17/600, max 2 righe
  individuale allo slope
  consensus della Deutsche Kniegesellschaft: non      ← TLDR (v), 15/400, --dim
  una soglia unica ma valutazione individuale
  KSSTA · consensus · 14 esperti · ago   ▂▂▄ media    ← meta 13: rivista·disegno+n·età·confidenza
```

- ● = pallino di rilevanza (unico colore informativo della riga; per il contesto
  ⚪ il pallino è vuoto, non grigio pieno: pesa meno).
- «di cosa parla» = titolo+TLDR · «quanto è solido» = chip disegno+n e barra
  confidenza · «quanto è nuovo» = età/`nuovo` · «cosa farci» = pallino, e il
  dettaglio `perte` alla riga d'apertura.
- **Nessuna azione visibile in lista** (progressive disclosure): tap = apre.
- **Card aperta**: perte in evidenza (bordo `--attrito`/`--pratica` a sinistra),
  poi risultati con incertezze, «cosa NON può dire», limiti, PMID/DOI linkati;
  barra azioni UNICA in fondo (Salva ★ · Voto · Social · Video · Ascolta) nel
  terzo inferiore, bersagli 44 pt.
- Varianti della stessa card: breve della seconda pagina (senza barra), riga
  rassegna (con fonte), riga candidato (compatta con checkbox 📹). Un solo
  markup, tre densità — la triplicazione attuale si chiude.

Altri componenti (set minimo): blocco-eroe del giorno · sparkline 14 giorni ·
chip (filtri, disegno di studio) · sezione a soffietto · barra tab inferiore ·
toast · skeleton (solo Rassegna) · campo di ricerca con stato «nessun risultato
per “x”».

## 6. Movimento

Solo funzionale: apertura card (altezza, 200 ms), conferma azione (toast 150 ms),
cambio vista (dissolvenza 120 ms). `transform`/`opacity` soltanto;
`prefers-reduced-motion: reduce` → tutto istantaneo. Nessuna animazione
decorativa; la copertina a onda del PICK viene sostituita da una testata
tipografica con bordo semantico.

## 7. Architettura dell'informazione

Navigazione per momenti, non per funzioni tecniche. **Barra inferiore** (mobile,
pollice-first):

`Oggi` · `Rassegna` · `Archivio` · `★` · `Menu` (Newsletter/produzione,
Impostazioni, Guida — su desktop tutte le voci sono esposte).

Percorsi obiettivo (baseline → obiettivo):
- Job 1 «cosa c'è di nuovo»: 0 tap → **0 tap e <5 s di lettura** (blocco-eroe).
- Job 2 social pronto: 3 tap → **≤3** (card → Social → Copia).
- Job 3 newsletter: 3–6 tap → **≤4** (Menu→Produzione: candidati 📹 già
  raccolti col confronto affiancato in `compatta`; scelta → Copia).

Stati progettati (tutti): quieto («niente ti riguarda oggi» come schermata di
prima classe) · vuoto · in preparazione/non arrivato · errore di rete · offline
(«stai guardando l'edizione di ieri») · parziale (fonte muta) · nessun risultato
di ricerca · contenuto lungo (2 righe + ellissi) · caricamento (skeleton, solo
Rassegna).

Desktop: **⌘K** apre la palette che riusa `interpretaComando` (stesso vocabolario
del 🎙; zero logica nuova) + `j/k` sulla lista. Mobile: gesture esistenti
(swipe destro = Salva) mantenute e documentate in guida.

Prima vista **statica al build**: `costruisci.py` emette il blocco-eroe e la
lista del giorno già composti nell'HTML; il JS idrata senza ridisegnare → CLS ~0.

## 8. Testi dell'interfaccia

Voce attiva, un nome per azione in tutto il flusso (Salva→Salvata,
Copia→Copiato, Ascolta→In lettura), errori = cosa è successo + cosa fare, stati
vuoti = inviti, niente esclamativi, niente emoji di sistema (le emoji restano
solo dove sono contenuto, es. il pallino è CSS). Termini scientifici in inglese,
tutto il resto in italiano.

---

## 9. Tre direzioni — e la scelta

### A · «Prima pagina» — *il quotidiano che si legge in un colpo d'occhio*
Tesi: PULSE è un giornale; la prima schermata è la prima pagina, e la prima
pagina è il verdetto.

```
┌──────────────────────────────┐
│ PULSE · knee     gio 20 ago  │  ← testata minima
│                              │
│  Oggi niente mette in        │  ← blocco-eroe 28px
│  discussione quello che fai. │
│  9 letti · 0 che ti toccano  │  ← conteggi onesti, 13px
│  ▁▂▁▁▃▁▂▁▁▁▂▁▁▂  14 giorni   │  ← sparkline
│  ▶ Ascolta 4 min      🚗     │  ← audio, sotto l'insight
├──────────────────────────────┤
│ TI RIGUARDA (3)              │
│ ● titolo…                    │
│   tldr…                      │
│   KSSTA · consensus · ago    │
│ ● titolo…                    │
├──────────────────────────────┤
│ CONTESTO (6)  ▸              │  ← chiuso di default
├──────────────────────────────┤
│ Oggi Rassegna Arch. ★ Menu   │  ← barra inferiore
└──────────────────────────────┘
```
Rischio principale: resta l'IA attuale — il job 2/3 migliora per densità e
riordino, non per ristrutturazione; se un domani le funzioni raddoppiano, il
«Menu» si affolla.

### B · «Terminale» — *Bloomberg per il ginocchio*
Tesi: una sola tabella densa, tutto il giorno in 20 righe, zero card.

```
┌──────────────────────────────┐
│ 20 AGO   9 letti · 0 allerte │
│──────────────────────────────│
│ ● cons KSSTA  slope indiv.   │
│ ● coor JEO    slope rischio  │
│ ● anat SRA    nervo prelievo │
│ ○ rev  JISAKOS LET anatomia  │
│ …16 righe a 40px…            │
│──────────────────────────────│
│ [dettaglio della riga attiva]│
└──────────────────────────────┘
```
Rischio principale: su iPhone la densità estrema penalizza proprio il momento 1
(leggibilità a colpo d'occhio in corsia); il carattere editoriale (TLDR, perte)
— ciò che nessun competitor ha — si comprime fino a sparire.

### C · «Tre stanze» — *navigazione per momenti d'uso*
Tesi: tre ambienti separati (Oggi / Settimana / Produzione), ognuno col proprio
layout; Rassegna e Archivio diventano sezioni interne di Oggi e Settimana.

```
┌──────────────────────────────┐
│        [stanza: OGGI]        │
│  eroe + lista essenziale     │
│                              │
│  Settimana: candidati, con-  │
│  fronto, salvati, archivio   │
│  Produzione: social, news-   │
│  letter, blog                │
├──────────────────────────────┤
│   Oggi | Settimana | Prod.   │
└──────────────────────────────┘
```
Rischio principale: rimappa una navigazione ormai imparata (6 schede) e la
memoria delle scelte utente legata alle viste; è la ristrutturazione più costosa
da collaudare (percorsi nuovi in tutte le 16 suite) per un utente che l'attuale
mappa la usa già ogni giorno.

### Raccomandazione: **A — «Prima pagina»**, con la densità `compatta` di B
adottata SOLO su desktop per candidati/archivio.

Perché: il 90% delle aperture è il momento 1 su iPhone, e A ottimizza
esattamente quello con il rischio di regressione più basso (refactor incrementale
sotto un cancello da 605 controlli); incorpora 13 dei 15 pattern del benchmark.
Cosa si perde scartando B: la vista-tabella unica come identità — recuperata in
parte nella modalità compatta desktop, ma il mobile resta editoriale, non da
terminale. Cosa si perde scartando C: la purezza concettuale dei tre momenti
come stanze — A li serve con la gerarchia dentro la mappa esistente, e la
ristrutturazione resta possibile in futuro senza buttare nulla di A.
