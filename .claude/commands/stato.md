---
description: Diagnosi rapida — l'app online è aggiornata? il briefing sta girando?
---

Il guasto tipico di PULSE è **silenzioso**: il briefing non parte, nessuno se ne accorge,
e l'utente apre l'app trovando il giorno prima. Questo comando serve a vederlo subito.

Raccogli i fatti, senza commentarli mentre li raccogli:

1. `BUILD_DATE`, `CIT_VERIFICATE` e `LAST_RETRACTION_CHECK` in `index.html`
   (`grep -n 'var BUILD_DATE\|var CIT_VERIFICATE\|var LAST_RETRACTION_CHECK' index.html`).
2. La data di oggi, e **quanti giorni** sono passati da `BUILD_DATE`.
3. `git log --oneline -5` e `git fetch origin main && git log --oneline HEAD..origin/main`
   — la copia di lavoro è indietro rispetto a ciò che è online?
4. L'ultima istantanea in `versioni/elenco.json`.
5. L'ultima entrata in `cervello/claude__09-storico.md`.

Poi riferisci in **cinque righe al massimo**:

- se `BUILD_DATE` è di oggi o ieri → il sistema gira;
- se è più vecchio di due giorni → **dillo come guasto, non come ritardo**, e indica
  quale delle due firme corrisponde: silenzio totale (nessun commit, nessuna istantanea,
  nessuna entrata nello storico = la sessione non è mai partita, tipicamente crediti
  esauriti o push bloccato) oppure tracce parziali (è partita ed è morta a metà);
- se la copia di lavoro è indietro rispetto a `origin/main`, avvisa **prima** di
  qualunque modifica: pubblicare da qui cancellerebbe lavoro altrui (regola 13).

Meglio corto e vero che lungo e rassicurante.
