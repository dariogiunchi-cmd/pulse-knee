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

**Obbligo quotidiano: `NLB`.** Per **ogni** lavoro del giorno:

```
NLB = { numero: { prof: [titolo, corpo, nota critica],
                  paz:  [titolo, corpo, nota rassicurante],
                  kw:   "3-4 parole chiave, come le cerca un paziente su Google" } }
```

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
