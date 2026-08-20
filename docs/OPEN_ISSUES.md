# PULSE — questioni aperte

## Dimensione medico-legale disattivata (Addendum 1, 20 agosto 2026)

Per decisione dell'utente, la dimensione medico-legale/peritale/assicurativa esce
da PULSE: nessun criterio di selezione, nessun elemento d'interfaccia, nessun
riferimento nei testi delle schede.

**Che cosa è stato disattivato (isolato, non cancellato — reversibile in un commit):**

1. `cervello/claude__13-attivita.md` — il paragrafo «STANDARD DI CURA» che ogni
   mattina aggiungeva una riga al registro `cervello/14-standard-di-cura.md`.
   Ora è racchiuso in un commento HTML con data e motivo. Il registro resta nel
   repository con le sue righe storiche, intatte: NON viene toccato lo schema dei
   dati già archiviati, solo fermata l'aggiunta di righe nuove. Riattivazione:
   togliere il commento.
2. `cervello/00-istruzioni-del-progetto.md` — la riga «È perito SIM: …» nei
   criteri di peso, sostituita dalla motivazione puramente clinica (i consensus
   contano perché ridefiniscono la pratica, non per il loro peso peritale).

**Interfaccia e codice dell'app:** l'audit (docs/AUDIT.md §3.2) non ha trovato
alcuna categoria, filtro, parola chiave di ricerca o criterio di punteggio
medico-legale nell'app: nulla da rimuovere lato codice.

**Contenuto del giorno:** la scheda 1 del 20 agosto contiene la frase «peso
peritale alto» nella riga di rilevanza — è contenuto quotidiano scritto dal
briefing prima dell'Addendum, ruota via col ricambio di domani; il mandato
aggiornato vieta la formula da domani in poi. Non modificata a mano (i dati del
giorno non si ritoccano fuori dal briefing).
