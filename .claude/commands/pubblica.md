---
description: Pubblica l'app online, con i controlli di discendenza e di sicurezza
---

Pubblicare significa cambiare ciò che il Dr. Giunchi vedrà sull'iPhone. Si fa in
quest'ordine, senza saltare passi.

**1. Discendenza (regola 13).**
```
git fetch origin main && git log --oneline HEAD..origin/main
```
Se compare qualcosa, **fermati e dillo all'utente**: la tua copia è indietro e pubblicare
cancellerebbe quel lavoro. Riallineati prima (`git diff > /tmp/mie.patch`,
`git reset --hard origin/main`, riapplica), poi ricomincia da qui.

**2. Il cancello.**
```
bash test/verifica.sh
```
Se fallisce non si pubblica, punto. Correggi e rilancia. Non aggirarlo mai con un push a
mano, e non disattivare un controllo per farlo tacere.

**3. La pubblicazione vera.**
```
bash test/pubblica.sh "AAAA-MM-GG" "PULSE <data>"
```
Senza token: da una sessione autorizzata il push passa dal remoto della sessione, e lo
script lo verifica prima di iniziare. Solo se lo script dice che nessuna via risponde,
serve `PULSE_TOKEN=<token>` davanti al comando — il token vive nel Progetto claude.ai
(`claude/10-deploy.md`) e non va mai scritto in un file, in un commit o in un messaggio.

Lo script rifà la verifica per conto suo, clona, salva l'istantanea datata, firma il
commit, spinge, e infine **riscarica dallo SHA per riverificare ciò che è davvero
online**. Non ripetere a mano quei passi.

**4. Riferisci** lo SHA pubblicato e quello precedente, così il ritorno indietro è a
portata di mano:
```
curl -s https://raw.githubusercontent.com/dariogiunchi-cmd/pulse-knee/<SHA_PRECEDENTE>/index.html -o index.html
```

Se hai toccato qualcosa che vive anche in `cervello/`, aggiorna la copia, lancia
`python3 test/cervello.py cervello`, e **ricorda all'utente** che il ricopiaggio nel
Progetto claude.ai può farlo solo lui.
