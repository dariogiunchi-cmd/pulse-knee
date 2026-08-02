# PULSE — pubblicazione dell'app (deploy)

*Attivo dal 2 agosto 2026.*

> ⚠️ **Questa è la copia pubblica.** Il token GitHub è stato tolto: vive solo nel
> Progetto claude.ai, in `claude/10-deploy.md`. Tutto il resto è identico.

## Indirizzo pubblico
**https://dariogiunchi-cmd.github.io/pulse-knee/**
GitHub Pages: ramo `main`, cartella `/ (root)`. Repo pubblico `dariogiunchi-cmd/pulse-knee`.
Istantanee datate: **/pulse-knee/versioni/**

## File nel repo (NON cancellarne nessuno)
`index.html` · `manifest.json` · `sw.js` · `.nojekyll` · `apple-touch-icon.png` ·
`icon-192.png` · `icon-512.png` · `icon-maskable-512.png` ·
`test/` (le suite e gli script) · `versioni/` (istantanee) · `cervello/` (questa cartella)

## Credenziale
Token GitHub dell'utente (classic, scope `repo`, senza scadenza).
**Sta solo nel Progetto claude.ai.** Va passato agli script come variabile `PULSE_TOKEN`,
mai scritto dentro un file del repository.
Per revocarlo: github.com/settings/tokens → Delete (l'aggiornamento automatico si ferma).

## Procedura di pubblicazione — un solo comando
```bash
PULSE_TOKEN=<token> bash test/pubblica.sh "2026-08-02" "PULSE 2 agosto 2026"
```
Lo script fa, in quest'ordine: verifica completa → clone del repository (così istantanee e
cervello non vengono cancellati) → copia dei file → istantanea datata con ritenzione →
commit e push → riscarica dallo SHA e riverifica ciò che è davvero online.
**Se la verifica fallisce non pubblica**, e il sito resta quello del giorno prima.

## Perché si clona invece di ripartire da zero
La vecchia procedura faceva `git init` + `push -f`: cancellava tutto ciò che non veniva
ricopiato. Con le istantanee e il cervello nel repository, quel modo avrebbe distrutto la
storia a ogni pubblicazione. Ora si clona, si aggiorna, si spinge senza forzare.

## 🔄 TORNARE INDIETRO se una versione esce rotta
```bash
# opzione A — da un'istantanea datata (la strada normale)
curl -s https://raw.githubusercontent.com/dariogiunchi-cmd/pulse-knee/main/versioni/2026-08-01.html -o index.html
# opzione B — da uno SHA noto
curl -s https://raw.githubusercontent.com/dariogiunchi-cmd/pulse-knee/<SHA_BUONO>/index.html -o index.html
# poi ripubblicare con test/pubblica.sh
```
In un minuto il sito torna alla versione precedente. Avvisare sempre l'utente in chat.

## ⚠️ TRAPPOLA DELLA CACHE — errore già commesso, non ripeterlo
`raw.githubusercontent.com/.../main/index.html` resta in cache alcuni minuti e può
restituire una versione VECCHIA. Se si riparte da quella, **le funzioni aggiunte il
giorno prima spariscono** (successo il 2 agosto: perse le barre di confidenza).
**Regola:** per scaricare la base e per verificare usa l'URL con lo **SHA del commit**,
non del ramo.

## ⚠️ github.io NON è raggiungibile dal sandbox
`curl` su `dariogiunchi-cmd.github.io` restituisce `000`. **Non è un guasto del sito.**
Verifica corretta: URL raw con lo SHA, `diff -q` col file locale, poi rilanciare la
verifica **sul file scaricato** — è ciò che `pubblica.sh` fa da solo al passo 6.
Bloccati allo stesso modo (verificato il 2 agosto 2026): `wixapis.com`,
`mybusiness.googleapis.com`, `oauth2.googleapis.com`, `wix.com`, `api.brevo.com`.
Nessuna pubblicazione automatica verso quei servizi è possibile da qui.

## ⚠️ ESCAPE UNICODE NELLE PATCH
Le patch generate con Python in raw string (`r"""…"""`) lasciano `\U0001f4f9` **letterale**
nel JavaScript, e JS non riconosce `\U` maiuscolo: l'utente legge «U0001f4f9».
`checklist.py` lo verifica a ogni pubblicazione. (`·` minuscolo è valido, va lasciato.)

## ✅ La checklist non si esegue più a mano
Sta dentro `test/checklist.py`, che verifica i marcatori di **26 funzioni**, la sintassi
JavaScript, gli escape unicode, i segnaposto, l'accessibilità, la chiave `pulse4`,
l'assenza di credenziali e il peso compresso. `verifica.sh` la esegue per prima e, se
fallisce, **non apre nemmeno il browser**.

## Le suite di test
Vivono in `test/`, dentro il repository, così ogni sessione le eredita.

| Suite | Che cosa copre |
|---|---|
| `checklist.py` | struttura, sintassi, credenziali, peso |
| `logica.js` | salvataggi, voti, confidenza, voce, persistenza |
| `mobile.py` | adattamento 375/390/430, chiaro e scuro |
| `qualita.py` | numeri, studi muti, tensioni, accessibilità |
| `social.py` | 3 toni × 3 lunghezze × 4 formati, hashtag |
| `newsletter.py` | email: struttura, PMID, versioni, persistenza |
| `memoria.py` | sopravvivenza delle scelte al ricambio quotidiano |
| `distribuzione.py` | blog e Google: SEO, limite 1500, **niente pubblicità** |

Tutte accettano `PULSE_HTML=<percorso>`; `verifica.sh` lo imposta da solo.

## Adattamento mobile — regole da non rompere
- `.add input,.srch input,.nlvid{font-size:16px}` → sotto i 16px **iPhone ingrandisce la pagina**
- `html,body{overflow-x:hidden;max-width:100%}` e `-webkit-text-size-adjust:100%`
- `.grid,.grid>*{min-width:0}` → senza questo il contenuto viene tagliato
- `.filters{flex-wrap:wrap}` · `@media(max-width:430px)` per le schede
- `@media(max-width:400px){.tabs{flex-wrap:wrap}}` → con 5 tab, a 375 px senza questo
  l'ultima esce dallo schermo
- `.pick .prev.cover` (serve la doppia specificità)
- Modalità scura: `.vitem`, `.tens2`, `.titem`, `.mute`, `.editbox`, `.nlout`, `.nlvid`,
  `.nlwrap` hanno override dedicati
- Modalità scura: `.ib{…!important}` annulla gli stati accesi → servono override espliciti
  per `.ib.save.on`, `.ib.up.on`, `.ib.down.on`, `.ib.vid.on`
- Bersagli tattili ≥ 28 px di altezza

## Stato dell'utente
Salvataggi, voti, letti, preferenze, testi social adattati, lavori scelti per la
distribuzione e indirizzo del blog vivono nel browser dell'iPhone (chiave `pulse4`).
Mantenere quel nome: cambiarlo cancella tutto. Non azzerare mai `S.weekly`.

## Il testo dell'attività quotidiana
L'attività «PULSE — briefing quotidiano ginocchio» parte ogni giorno alle 5.00 UTC.
Il testo completo del suo prompt è conservato in `cervello/claude__13-attivita.md`.

## Peso — misurato il 2 agosto 2026
`index.html`: 133 KB grezzi, **38 KB come lo scarica l'iPhone**. Alla prima apertura la
pagina fa **una sola richiesta**. Tolto `pulse_brief.mp3` (673 KB, zero riferimenti in
tutto il repository, mai scaricato): il repository è passato da 1,2 MB a 524 KB.

## Le suite — 387 controlli
`checklist.py` 36 · `logica.js` 35 · `mobile.py` 24 · `qualita.py` 23 · `social.py` 12 ·
`newsletter.py` 73 · `memoria.py` 14 · `distribuzione.py` 106 · `preferenze.py` 64.
Il cancello è stato collaudato sabotando l'app di proposito quattro volte: funzione persa,
errore di sintassi, credenziale nei file, parola pubblicitaria. Tutte e quattro bloccate.
