# PULSE — strumenti di terze parti e costi (tetto: 10 CHF/EUR/USD al mese, complessivi)

Aggiornato: 20 agosto 2026.

| Strumento | Funzione | Costo/mese | Stato | Credenziali | Disattivazione |
|---|---|---|---|---|---|
| GitHub (Pages+Actions) | hosting, CI, raccoglitore notturno | 0 | attivo | — | — |
| Cloudflare Workers | cervello «Chiedi a PULSE» | 0 (piano free) | pronto, in attesa delle chiavi | secret del Worker, mai nel repo | `wrangler delete` |
| Claude API (Anthropic) | conversazione del cervello | ~1–2 stimati | in attesa delle chiavi | secret Worker | rimuovere secret |
| OpenAI TTS | voce naturale | ~4–6 stimati | in attesa delle chiavi (facoltativo) | secret Worker | rimuovere secret; l'app torna alla voce di sistema |
| **Totale impegnato** | | **~5–8 stimati** | | | |

## Redesign UX v2 — decisione di spesa: **0**

- **Tipografia**: valutata una licenza professionale (il candidato naturale
  indicato). Scartata a favore del **system stack** (SF Pro su iPhone): 0 KB,
  resa nativa perfetta sull'uso prevalente, nessun FOUT sulla pagina critica.
  Alternativa gratuita di riserva già individuata (Inter, self-hosted, ~90 KB)
  se in futuro si vorrà un'identità distinta su desktop: reversibile in un
  commit. Nessuna spesa giustificabile finché il gratuito è questo.
- **Icone**: SVG inline disegnate nei token (poche, sobrie): 0.
- **Test/audit**: Playwright + Lighthouse già nel cancello: 0.

Regole rispettate: nessuna chiave nel repository (verificato dal cancello,
controllo credenziali di checklist.py); nessun lock-in — la scomparsa di
qualunque servizio a pagamento degrada con eleganza dichiarata (voce di sistema,
vocabolario locale), mai rompe l'app; nessun tracciamento dell'utente introdotto.

## Motore vocale (20 agosto 2026, prova d'ascolto alla cieca)

Scelto **Kokoro** (open-source, 82M, voce it `if_sara`) — il file «B» della prova
a tre: contro Azure neurale (anteprima edge-tts) e Piper. Costo: **0**. Nessun
account, nessuna chiave, nessun servizio: il modello gira nel runner GitHub del
workflow `mattino.yml`. Disattivazione: cancellare il workflow. Se il progetto
Kokoro sparisse, il modello resta scaricabile/cache-abile: nessun lock-in.
Volume reale misurato: ~2.500 caratteri/briefing ≈ 76.000/mese (un terzo della
stima dell'Addendum) — anche i motori a pagamento sarebbero rientrati nei loro
livelli gratuiti; a maggior ragione non si paga nulla. Budget totale usato: 0/25.
