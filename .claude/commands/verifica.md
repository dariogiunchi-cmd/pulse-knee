---
description: Esegue il cancello completo (499 controlli) e spiega ogni suite fallita
---

Esegui `bash test/verifica.sh` e riferisci l'esito.

Se **tutto passa**: dillo in una riga con il numero di controlli. Nient'altro.

Se **qualcosa fallisce**, per ogni suite rossa:

1. Leggi il messaggio d'errore per intero, non solo la prima riga.
2. Stabilisci di quale dei due casi si tratta, e **dillo esplicitamente**:
   - **manca uno strumento** (Playwright, Chromium, node) → non è l'app a essere rotta.
     Installa e rilancia. Ricorda il vincolo: `playwright==1.56.0`, perché l'immagine
     ha Chromium 1194. **Non modificare `index.html` per far passare i test.**
   - **il difetto è nei contenuti del giorno** → è il caso di gran lunga più frequente.
     Cerca in quest'ordine: un campo `results` senza incertezza (p, IC, OR/HR/MD, DS),
     un `DUELS` o `LINKS` che punta a una scheda inesistente, una parola pubblicitaria,
     `CIT_VERIFICATE` maggiore del numero di schede, `LAST_RETRACTION_CHECK` diverso da
     `BUILD_DATE`.
3. Proponi la correzione **nei contenuti**, non nel test.

Se sei convinto che sia il *test* a sbagliare, non disattivarlo: dimostralo prima —
mostra il caso valido che il test rifiuta — e solo allora correggi il test, collaudandolo
rompendo davvero ciò che deve proteggere.

Non pubblicare nulla: questo comando verifica soltanto.
