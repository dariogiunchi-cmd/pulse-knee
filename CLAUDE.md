# PULSE — istruzioni per Claude Code

Questo file viene letto automaticamente da Claude Code a ogni sessione aperta in questa
cartella. Non è documentazione per l'utente: è la memoria di lavoro dell'agente.

**Dal 17 agosto 2026 l'originale del cervello è `cervello/` in questo repository** —
deciso dal Dr. Giunchi quando il lavoro si è spostato su Claude Code. Il Progetto
claude.ai «PULSE — Direzione Scientifica Ginocchio» ne conserva una copia per le
conversazioni; in caso di divergenza **vince il repository**. Fino al 12 agosto era il
contrario: i documenti scritti prima vanno letti sapendolo. Dopo ogni modifica a
`cervello/` si rilancia `python3 test/cervello.py cervello` (ripulisce le credenziali e
rigenera l'indice).

---

## Che cos'è

Applicazione a pagina singola per il **Dr. Dario Giunchi**, chirurgo ortopedico FMH
dedicato al ginocchio, Ticino. Ogni mattina alle 5.00 UTC una sessione automatica cerca
la letteratura nuova sul ginocchio, scrive le schede del giorno e ripubblica l'app.

Online: <https://dariogiunchi-cmd.github.io/pulse-knee/> (GitHub Pages, ramo `main`, root).

Non è un sito informativo: è uno strumento di lavoro che lui apre dall'iPhone. Tutto ciò
che l'app afferma su sé stessa deve essere vero.

**Mobile prima di tutto — sua indicazione esplicita (19 agosto): l'app si usa quasi
sempre dal telefono, raramente dal desktop.** Ogni funzione nuova si progetta a
390 px e si collauda lì per prima; i bersagli di tocco stanno a ≥44 px (minimo
Apple); il desktop è un adattamento, mai il punto di partenza.

---

## Le tre regole che non si negoziano

**1. PRINCIPIO ZERO.** Mai inventare titoli, autori, riviste, DOI, PMID, numeri,
popolazioni, follow-up, risultati. Dato assente si scrive «non riportato». Fonte non
aperta si dichiara non verificata. *Una citazione falsa ma plausibile è il fallimento
peggiore possibile: lui la porterebbe in tribunale.*

**2. NIENTE LINGUAGGIO PUBBLICITARIO.** Non è stile, è legge: LPMed art. 40 lett. d
(RS 811.11) e Legge sanitaria ticinese art. 70. Vietati inviti all'azione, sconti,
gratuità, promesse di risultato, «senza rischi», superlativi comparativi.
`test/distribuzione.py` lo verifica a ogni pubblicazione e blocca.

**3. NULLA VIENE PUBBLICATO O INVIATO SENZA SUA CONFERMA ESPLICITA.** Vale per i social,
le email, il blog. La pubblicazione dell'**app** è invece automatica di sua volontà.

---

## Il cancello — l'unica strada per andare online

```bash
bash test/verifica.sh                  # 499 controlli su index.html
bash test/verifica.sh /altro/file.html # verifica un file specifico
```

Esce 0 solo se tutto passa. **Qualsiasi altro codice = non pubblicare.**

```bash
bash test/pubblica.sh "2026-08-17" "PULSE 17 agosto 2026"
```

Fa tutto in sei passi: verifica → clone → copia → istantanea datata → commit firmato e
push → riscarica dallo SHA e riverifica ciò che è davvero online. **Non serve alcun
token**: da una sessione autorizzata il push passa dal remoto della sessione (verificato
prima di iniziare). `PULSE_TOKEN=<token>` davanti al comando resta come via di riserva
da ambienti non autorizzati.

### Quando una suite fallisce, il difetto è quasi sempre nei contenuti del giorno

Le suite **collaudano la macchina, non il carico del giorno** (`test/comune.py`). Se una
si accende, cerca in quest'ordine: un numero senza la sua incertezza, un `DUELS` o un
`LINKS` che punta a una scheda inesistente, una parola pubblicitaria, `CIT_VERIFICATE` o
`LAST_RETRACTION_CHECK` non aggiornati.

**Mai disattivare un controllo per far passare una pubblicazione.** Se hai cambiato di
proposito qualcosa che un test sorveglia, aggiorna il test *insieme* al codice, e
collaudalo rompendo davvero ciò che deve proteggere — un controllo che non suona è peggio
di un controllo assente (difetto 32).

**Mai reintrodurre nei test conteggi assoluti o numeri di scheda scritti a mano.** È
l'errore più costoso della storia del progetto (difetti 18 e 34): il cancello si sarebbe
chiuso su un briefing valido, lasciando online quello del giorno prima senza che nessuno
se ne accorgesse.

**Se il messaggio dice che mancano degli strumenti, non è l'app a essere rotta.**
Installali e rilancia; non toccare `index.html`.

---

## L'ambiente — trappole già pagate

| Trappola | Regola |
|---|---|
| **Playwright** | Serve **`playwright==1.56.0`**: è la versione che corrisponde al Chromium **1194** dell'immagine. La 1.62 ne pretende una 1234 che non c'è, e fa fallire nove suite su dodici. Ci pensa `.claude/hooks/session-start.sh`. |
| **`github.io` dal sandbox** | `curl` risponde `000`. **Non è un guasto del sito.** Verifica con l'URL raw sullo SHA. |
| **Cache di `raw.githubusercontent.com`** | L'URL sul *ramo* resta in cache alcuni minuti e restituisce versioni vecchie. Per scaricare o verificare usa sempre l'URL con lo **SHA del commit**. Il 2 agosto questa trappola ha fatto sparire le barre di confidenza. |
| **Firma dei commit** | Configurata a livello globale, GitHub la verifica. **Non disattivarla mai** con `-c commit.gpgsign=false`: rende ogni pubblicazione «Unverified». |
| **Escape unicode** | Le patch Python in raw string lasciano `\U0001f4f9` letterale nel JavaScript e JS non riconosce `\U` maiuscolo. `checklist.py` lo cerca. |
| **Servizi irraggiungibili** | `wixapis.com`, `mybusiness.googleapis.com`, `oauth2.googleapis.com`, `wix.com`, `api.brevo.com`. Nessuna pubblicazione automatica verso quei servizi è possibile da qui. |

---

## Le variabili che il briefing riscrive ogni mattina

**Dalla sera del 17 agosto vivono in `dati/giorno.js`** — l'unico file che il briefing tocca.
`index.html` è il prodotto di `modello.html` (il codice, da non toccare mai) più i
dati: si rigenera con `python3 test/costruisci.py`, e il cancello blocca un
`index.html` modificato a mano (`costruisci.py --verifica`). Dopo il ripristino di
un'istantanea: `costruisci.py --estrai` riallinea modello e dati all'index ripristinato.

Tutte come `var` a livello superiore:

`SELEZIONE` (la schermata unica: verdetto + ≤3 schede {pmid,dice,cambia,perche};
facoltativa per le istantanee vecchie, il cancello ne fa rispettare il tetto) ·
`BUILD_DATE` · `ARTICLES` · `CIT_VERIFICATE` · `CONF` · `MUTE` · `TENSIONS` · `LINKS` ·
`DUELS` · `HISTORY` · `AUDIT` · `RETRACTED` · `LAST_RETRACTION_CHECK` · `BRIEF_TEXT` · `BRIEF_DIALOGO` (facoltativa:
il podcast a due voci; se manca, ▶ legge `BRIEF_TEXT`) ·
`NLB` · `SOCV` · `TAGS` · `SOC` · `SUGGQ` · `VERDICT` · `PICK` · `INDUSTRIA` ·
`CONGRESSI` · `SOCIETA` · `NONVERIF` · `EXTRA` · `SCOPERTE` (la «seconda pagina»:
brevi verificati senza numeri + proposte fuori dal solito — regole in claude__13)

### Da non toccare mai

- la chiave `localStorage` **`pulse4`** — cambiarla cancella tutto lo stato dell'utente;
- `S.weekly` (lavori scelti per la distribuzione) e `S.savedItems` (articoli salvati);
- `PREFV` / `PREF_*` — se aggiungi voci alle sue liste, **alza `PREFV` di 1**.

### L'errore commesso tre volte in un giorno solo

`S.saved`, `S.weekly` e `suggIdx` identificavano le cose per **posizione nell'elenco**.
I numeri di scheda cambiano ogni mattina: dopo una notte le scelte sparivano, o
ricomparivano proposte già respinte. Corretto identificando **per contenuto** — PMID per
gli articoli, nome per le proposte.

> **Regola generale che ne discende: se una cosa deve sopravvivere alla notte, non la si
> identifica per posizione.** Vale per qualunque funzione nuova.

---

## Discendenza — la regola 13

**Una pubblicazione deve discendere da ciò che è online.** `pubblica.sh` confronta lo
`HEAD` della copia di lavoro con `origin/main` al momento del clone; se la copia è un
antenato si ferma con codice **4**, elenca i commit finiti nel mezzo e dice come
riallinearsi. `PULSE_SOVRASCRIVI=1` è l'unica scappatoia, e si dichiara a video.

Nasce da un difetto reale: la sera del 4 agosto il briefing ha clonato il repository un
istante prima che una pubblicazione fosse visibile, e mezz'ora di correzioni è sparita
con **464 controlli verdi**. Le suite guardavano *che cosa* viene pubblicato e mai *sopra
che cosa*.

> **Questa è la regola che rende possibile lavorare in due sulla stessa app** — una
> sessione Cowork e una Claude Code, o due Claude Code. Prima di ogni pubblicazione:
> `git fetch origin main && git log --oneline HEAD..origin/main`.

---

## Struttura

```
index.html          l'app servita: PRODOTTO di modello + dati. Non si modifica a mano
modello.html        il codice dell'app (HTML, CSS, JS). Si tocca solo per cambiare l'app
dati/giorno.js      i contenuti del giorno: l'unico file che il briefing riscrive
manifest.json sw.js PWA — funziona offline; le istantanee non si tengono in cache
cervello/           l'ORIGINALE del cervello (14-standard-di-cura.md: registro peritale)
audio/              orecchio.py (testo per l'orecchio) · feed.py (podcast) · gli MP3
                    del giorno e il feed, generati dal workflow mattino.yml su main
config/             pronuncia.json — il dizionario di pronuncia per l'audio
test/               le suite, costruisci.py, potenza.py, verifica.sh, pubblica.sh
versioni/           istantanee datate, per tornare indietro in un minuto
fonti/              fonti.json (configurazione) · raccolta.json (deposito notturno del
                    raccoglitore: richiami, trial, ritrattazioni, video — il sandbox
                    non esce su internet, i runner di GitHub sì)
.github/workflows/  cancello.yml (verifica su ogni PR) · battito.yml (07:15 UTC: se il
                    briefing non è arrivato, email da GitHub e issue — non consuma
                    crediti Claude: è il rilevatore indipendente della regola 36) ·
                    raccolta.yml (04:15 UTC, scrive fonti/raccolta.json) ·
                    ripristino.yml (mensile: l'ultima istantanea deve passare il cancello) ·
                    mattino.yml (quando dati/giorno.js arriva su main: genera l'MP3
                    con Kokoro, aggiorna il feed podcast, apre l'issue-email col
                    briefing completo — la consegna push; le risposte dell'utente
                    all'email sono giudizi che la sessione delle 5 legge)
```

### Le suite

| Suite | Copre |
|---|---|
| `checklist.py` | struttura, sintassi JS, credenziali, segnaposto, peso |
| `verita.py` | **PRINCIPIO ZERO meccanizzato**: PMID unici e non in progressione aritmetica, conteggi non gonfiati, riferimenti a schede esistenti |
| `logica.js` | salvataggi, voti, confidenza, voce, persistenza |
| `mobile.py` | 375/390/430 px, chiaro e scuro |
| `qualita.py` | numeri con incertezza, studi muti, tensioni, accessibilità |
| `social.py` | 3 toni × 3 lunghezze × 4 formati, hashtag |
| `newsletter.py` | email: struttura, PMID, versioni, persistenza |
| `memoria.py` | sopravvivenza delle scelte al ricambio quotidiano |
| `distribuzione.py` | blog e Google: SEO, limite 1500, **niente pubblicità** |
| `preferenze.py` `salvati.py` `trasferimento.py` | migrazioni e stato fra dispositivi |
| `orecchio.py` `podcast.py` | audio: pronuncia e feed — durate e pesi dichiarati veri |

Tutte accettano `PULSE_HTML=<percorso>`; `verifica.sh` lo imposta da solo.

---

## Come lavora, e come vuole essere trattato

Livello atteso: **consulente senior**. Preferisce una risposta lunga e completa a una
breve e incompleta, e **preferisce essere corretto piuttosto che assecondato**. Se un
ragionamento è debole, va detto. Quando l'evidenza è debole, va dichiarata debole.

Non gradisce: frasi motivazionali, riempitivi, ripetizioni, disclaimer eccessivi,
semplificazioni non necessarie, affermazioni senza spiegazione.

**Non vuole pubblicare articoli.** Non proporgli mai di sottomettere un abstract, non
chiedergli i suoi dati di esito, non trasformare una scadenza congressuale in un
progetto.

**Non sollecitare** la newsletter, il consenso nLPD, né chiedergli se ha girato il video.

**Se incolla un messaggio che inizia con «SEGNALI PULSE»** (il tasto 📡 dell'app):
sono i suoi voti, salvati e proposte. Aggiorna `cervello/claude__07-preferenze.md`
di conseguenza e conferma in una riga. I segnali orientano la selezione dei giorni
successivi, mai le regole di verità.

Il perimetro clinico, l'ordine delle schede, la rete di riviste e opinion leader, le
tensioni aperte e il formato esatto delle schede stanno in `cervello/`. **Leggi
`cervello/00-istruzioni-del-progetto.md` prima di toccare i contenuti**, non solo il
codice.

---

## Una testa sola — il repository

Dal 17 agosto 2026 **tutto vive qui**: il cervello (`cervello/`, l'originale), il codice,
il cancello, e il mandato del mattino (`cervello/claude__13-attivita.md`). Il briefing
quotidiano gira come **Routine alle 5.00 UTC** che apre una sessione Claude Code nuova su
questo repository, con il connettore PubMed; pubblica con `bash test/pubblica.sh` senza
token, dall'accesso autorizzato della sessione. Il Progetto claude.ai resta per le
conversazioni e come custode del token di riserva.

**Il coinvolgimento dell'utente va ridotto al minimo — sua richiesta esplicita.** Non ha
competenze informatiche né tempo: consegnargli risultati finiti, mai procedure da
eseguire. Se serve un'azione che solo lui può fare, una riga sola, e solo quando è
davvero indispensabile.

**Regola imparata il 2 agosto, e vale ancora:** ogni volta che aggiungi una condizione al
cancello, aggiungila **anche** al mandato del mattino
(`cervello/claude__13-attivita.md`). Un controllo nuovo che la sessione delle 5 non
conosce le blocca la pubblicazione il giorno dopo. Aggiornare quel file basta: la
Routine lo legge dal repository a ogni esecuzione.
