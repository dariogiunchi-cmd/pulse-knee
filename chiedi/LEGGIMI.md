# «Chiedi a PULSE» — il cervello esterno

L'app è una pagina statica: non può custodire chiavi API. Questo Worker
(Cloudflare, piano gratuito) le custodisce per lei e offre due porte:

- **/chiedi** — conversazione libera con Claude, con il giornale del giorno
  come contesto (lo legge dal repository pubblico, cache 30 minuti).
- **/voce** — voce naturale (OpenAI `gpt-4o-mini-tts`, due voci per il podcast).

Ogni richiesta è protetta da una parola d'ordine (`PAROLA`), scelta dall'utente
e scritta una sola volta nell'app: vive nel suo telefono, mai nel repository.

## Attivazione (le uniche azioni che spettano al Dr. Giunchi)

1. **console.anthropic.com** → API keys → crea una chiave, carica 5 CHF.
2. **platform.openai.com** → API keys → crea una chiave, carica 5 CHF
   (facoltativa: serve solo per la voce naturale).
3. **dash.cloudflare.com** → crea l'account gratuito → My Profile → API Tokens
   → Create Token → modello «Edit Cloudflare Workers».
4. Su GitHub: `pulse-knee → Settings → Secrets and variables → Actions` →
   aggiungi quattro secret: `CLOUDFLARE_API_TOKEN`, `ANTHROPIC_API_KEY`,
   `OPENAI_API_KEY`, `PULSE_PAROLA` (una parola a scelta, es. tre parole unite).

Poi si scrive in chat a Claude «attiva il cervello»: il workflow
`chiedi-deploy` fa il resto e restituisce l'indirizzo. Nell'app:
Impostazioni → **Il cervello di PULSE** → si incollano indirizzo e parola. Fine.

## Costi realistici (uso personale quotidiano)

| Voce | Costo |
|---|---|
| Cloudflare Workers | 0 (piano gratuito, 100k richieste/giorno) |
| Claude (claude-haiku-4-5, domande brevi) | ~1–2 CHF/mese |
| Voce naturale (podcast + risposte, ~10 min/giorno) | ~4–6 CHF/mese |
| **Totale** | **~5–8 CHF/mese** |

Senza la chiave OpenAI tutto funziona lo stesso: le risposte arrivano scritte
e lette dalla voce di sistema del telefono.

## Che cosa NON fa

- Non memorizza nulla: niente database, niente log applicativi.
- Non inventa: il sistema impone il PRINCIPIO ZERO (citazioni mai inventate,
  dati assenti dichiarati) e risposte brevi, da ascoltare.
- Non fa pubblicità: vincolo legale svizzero, scritto nelle istruzioni.
