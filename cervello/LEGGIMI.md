# PULSE — il cervello

*Copia di sicurezza dei documenti del Progetto, aggiornata il 2026-08-02.*

Questi file sono la **memoria** del sistema: chi è il Dr. Giunchi, che cosa opera, quali
lavori sono già stati visti, quali tensioni restano aperte, come si scrivono le schede e
i contenuti, quali regole di qualità sono vincolanti, come si pubblica e come si distribuisce.

**L'originale vive nel Progetto claude.ai.** Questa è la copia: se il Progetto va perso, da
qui il sistema si ricostruisce per intero. Se le due versioni divergono, **vince il
Progetto** — questa cartella è di sola lettura.

## Le credenziali non sono qui

Il repository è pubblico. Prima di ogni scrittura, token e chiavi vengono sostituiti con
`***TOKEN-RIMOSSO***`, e la pubblicazione si ferma se una credenziale sopravvive al
controllo. In questo aggiornamento: **0 sostituzioni**.
Il token GitHub vero vive solo nel Progetto, dentro `claude/10-deploy.md`.

## Documenti (14, 88 KB in tutto)

| File | Peso | Impronta |
|---|---|---|
| `00-istruzioni-del-progetto.md` | 3.4 KB | `78dba04be726` |
| `01-profilo.md` | 6.3 KB | `a39ce39af586` |
| `02-cosa-opera.md` | 6.4 KB | `5eab1d69d4be` |
| `03-memoria.md` | 12.1 KB | `d65df47bcd49` |
| `04-fonti.md` | 7.9 KB | `7aeb81624749` |
| `05-formato.md` | 4.9 KB | `3cfd7dd432fa` |
| `06-social.md` | 3.2 KB | `e798b888fbdf` |
| `claude__07-preferenze.md` | 7.2 KB | `dbff92d13672` |
| `claude__08-archivio.md` | 0.4 KB | `aba6dc9d105b` |
| `claude__09-storico.md` | 3.4 KB | `81aae08ac418` |
| `claude__10-deploy.md` | 7.3 KB | `5945a85b0e7a` |
| `claude__11-qualita.md` | 13.0 KB | `ddda92c195d0` |
| `claude__12-distribuzione.md` | 5.1 KB | `53733f2ec633` |
| `claude__13-attivita.md` | 7.3 KB | `05cdb40550e6` |

L'impronta è il SHA-256 abbreviato: due copie con la stessa impronta sono identiche
carattere per carattere. I nomi con `claude__` corrispondono a `claude/` nel Progetto.

## Come si ricostruisce tutto, se un giorno servisse

1. Creare un Progetto su claude.ai e incollare `00-istruzioni-del-progetto.md` come
   istruzioni permanenti.
2. Caricare gli altri file con gli stessi nomi, riportando `claude__` a `claude/`.
3. Rigenerare un token GitHub (scope `repo`) e scriverlo in `claude/10-deploy.md`.
4. Ricreare l'attività quotidiana delle 5 del mattino con il testo conservato in
   `claude/10-deploy.md`.
5. `bash test/verifica.sh` deve dare verde **prima** di qualunque pubblicazione.

## Che cosa non è ricostruibile da qui

Le scelte fatte dentro l'app — articoli salvati, voti, lavori scelti per la
distribuzione, testi social adattati — vivono nel browser del suo iPhone, sotto la chiave
`pulse4`. Non sono su nessun server: se cancella i dati del sito, quelle si perdono.
Tutto il resto è qui.
