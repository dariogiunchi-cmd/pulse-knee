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

## Dal redesign v2 (20 agosto 2026, fine Fase 5)

1. **FCP 2,3 s su 4G simulato (obiettivo: <1,5 s).** L'app è un file unico coi
   dati del giorno dentro; il collo è trasferimento+parse. Strada proposta:
   pre-render statico della vista Oggi in `costruisci.py` (il briefing rigenera
   già index.html ogni mattina, quindi il pre-render sarebbe sempre fresco) con
   idratazione al boot. Da fare con le sue sentinelle, non in fretta.
2. **Il pannello auto ha uno stile proprio scuro-fisso** (fondo nero, bottoni
   #1c1c1e/#0a84ff) non unificato coi token semantici. Deliberato — in auto il
   fondo scuro fisso massimizza il contrasto — ma i colori andrebbero comunque
   espressi coi token.
3. **Desktop senza idee proprie oltre le due colonne di Oggi.** L'uso reale è
   quasi solo iPhone (indicazione esplicita del 19 agosto), quindi il desktop è
   un adattamento corretto e basta. Se l'uso desktop crescesse: colonna destra
   anche per Rassegna, scorciatoie da tastiera documentate.
4. **Riordino automatico per rilevanza: deciso di NON farlo** (deviazione dal
   pattern 3 del benchmark, motivata in CHANGELOG_UX.md): l'ordine del briefing
   È la gerarchia editoriale. Se un giorno servisse, va fatto lato briefing (che
   decide l'ordine), mai lato client.
5. **Emoji nei contenuti della Rassegna** (marcatori di sezione 📜 📣 🧪 ⚖️ e
   avvisi ⚠️): conservate deliberatamente — lì sono informazione compatta e le
   sentinelle le esigono. Se si vorrà uniformare anche quelle, va aggiornata
   `rassHTML` insieme a `test/rassegna.py`.
