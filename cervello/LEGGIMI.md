# PULSE — il cervello

*Indice rigenerato il 2026-08-20.*

Questi file sono la **memoria** del sistema: chi è il Dr. Giunchi, che cosa opera, quali
lavori sono già stati visti, quali tensioni restano aperte, come si scrivono le schede e
i contenuti, quali regole di qualità sono vincolanti, come si pubblica e come si distribuisce.

**Dal 17 agosto 2026 l'ORIGINALE è questa cartella.** Deciso dal Dr. Giunchi quando il
lavoro si è spostato su Claude Code: qui ogni modifica ha una storia, un diff e un autore;
nel Progetto claude.ai non ha niente di tutto questo. Il Progetto ne conserva una copia
per le conversazioni; se le due versioni divergono, **vince il repository**. Prima era il
contrario — i documenti fino al 12 agosto vanno letti sapendolo.

## Le credenziali non sono qui

Il repository è pubblico. Prima di ogni scrittura, token e chiavi vengono sostituiti con
`***TOKEN-RIMOSSO***`, e la pubblicazione si ferma se una credenziale sopravvive al
controllo. In questo aggiornamento: **0 sostituzioni**.
La pubblicazione ordinaria non richiede più alcun token: la sessione Claude Code spinge
dal proprio accesso autorizzato. Il token GitHub resta nel Progetto come via di riserva.

## Documenti (16, 179 KB in tutto)

| File | Peso | Impronta |
|---|---|---|
| `00-istruzioni-del-progetto.md` | 3.8 KB | `5dea9e4bf858` |
| `01-profilo.md` | 6.3 KB | `a39ce39af586` |
| `02-cosa-opera.md` | 6.4 KB | `5eab1d69d4be` |
| `03-memoria.md` | 27.9 KB | `7128a16e9aa0` |
| `04-fonti.md` | 8.4 KB | `4e694c6f7ebf` |
| `05-formato.md` | 4.9 KB | `3cfd7dd432fa` |
| `06-social.md` | 3.2 KB | `e798b888fbdf` |
| `14-standard-di-cura.md` | 3.8 KB | `e9637a6a1363` |
| `claude__07-preferenze.md` | 9.3 KB | `764ff5730906` |
| `claude__08-archivio.md` | 0.4 KB | `aba6dc9d105b` |
| `claude__09-storico.md` | 49.5 KB | `39900a33711c` |
| `claude__10-deploy.md` | 8.5 KB | `96b10a23c26e` |
| `claude__11-qualita.md` | 23.9 KB | `4f5e2d22760c` |
| `claude__12-distribuzione.md` | 5.1 KB | `53733f2ec633` |
| `claude__13-attivita.md` | 14.1 KB | `ded60f1f8be5` |
| `claude__15-rassegna-social.md` | 3.3 KB | `249c2a54704b` |

L'impronta è il SHA-256 abbreviato: due copie con la stessa impronta sono identiche
carattere per carattere. I nomi con `claude__` corrispondono a `claude/` nel Progetto.

## Come si ricostruisce tutto, se un giorno servisse

1. Il repository È la ricostruzione: clonarlo basta. `CLAUDE.md` orienta la sessione,
   questa cartella contiene la memoria, `test/` il cancello.
2. Per rifare anche il Progetto claude.ai: incollare `00-istruzioni-del-progetto.md`
   come istruzioni permanenti e caricare gli altri file, riportando `claude__` a `claude/`.
3. L'attività quotidiana delle 5.00 UTC si ricrea con il testo in `claude__13-attivita.md`.
4. `bash test/verifica.sh` deve dare verde **prima** di qualunque pubblicazione.

## Che cosa non è ricostruibile da qui

Le scelte fatte dentro l'app — articoli salvati, voti, lavori scelti per la
distribuzione, testi social adattati — vivono nel browser del suo iPhone, sotto la chiave
`pulse4`. Non sono su nessun server: se cancella i dati del sito, quelle si perdono.
Tutto il resto è qui.
