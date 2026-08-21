# SOTTRAZIONE — inventario e destino di ogni elemento attuale

20 agosto 2026 · risponde all'Addendum §7. Inventario completo dell'interfaccia
pubblicata (main `fde5750`), elemento per elemento, con tre destini possibili:
**ELIMINATO** (non serve all'obiettivo) · **RETROCESSO** (utile, ma fuori dal
percorso quotidiano) · **FUSO** (fa la stessa cosa di un altro elemento).

Regola permanente da qui in poi: per ogni elemento aggiunto alla schermata
quotidiana, uno va rimosso.

## Vista Oggi (percorso quotidiano attuale)

| Elemento | Destino | Perché |
|---|---|---|
| Banner freschezza (`renderFresh`) | **FUSO** nel verdetto | «Aggiornato oggi» e il verdetto sono la stessa risposta detta due volte; resta una riga sola. Gli stati di guasto (briefing non arrivato) restano: sono verità dovute |
| Verdetto eroe | **RESTA** (unico sopravvissuto com'è) | È già la riga di verdetto dell'Addendum §4; va riscritto in linguaggio ancora più naturale dal mandato |
| Conteggi «9 letti · 0 che ti toccano» | **ELIMINATO** | Statistica sul percorso quotidiano (anti-pattern §8) |
| Sparkline 14 giorni | **ELIMINATO** | Grafico; nessuna decisione clinica ne dipende |
| Pillola «9/9 citazioni verificate» | **RETROCESSO** in archivio/colophon | La garanzia di verifica è sacra ma è una proprietà del sistema, non una notizia del giorno |
| Audiobar (▶ · microfono · auto) | **FUSO** in un solo ▶ | ▶ riproduce l'MP3 pre-generato (Parte II); microfono conversazione → Profilo/secondario; modalità auto → sostituita dal podcast su CarPlay |
| «Il lavoro del giorno» (pick) | **FUSO** nelle ≤3 schede | Doppia gerarchia: il pick È la prima delle schede selezionate |
| Lista «Ricerca scientifica» (9 schede) | **FUSO** nella selezione ≤3 + archivio | Ciò che non entra nei tre va in archivio del giorno, consultabile, mai proposto |
| Filtri-pallino (4 chip) | **ELIMINATO** | Filtri sulla schermata quotidiana (anti-pattern §8); con ≤3 schede non c'è nulla da filtrare |
| 5 azioni per scheda (★ · su · giù · ✎ Social · Video) | **FUSO** in ✓/✗ | Una sola azione binaria; «utile» archivia (assorbe ★); i pesi si aggiornano da soli (assorbe «Manda i segnali»); Social e Video escono dal consumo → Produzione |
| «Dove le prove non ti coprono» (5 tensioni) | **RETROCESSO** in archivio; emergono nella scheda | Cinque questioni permanenti mostrate ogni giorno = debito visivo; una tensione riappare solo quando un lavoro del giorno la tocca («perché lo vedo») |
| Duelli (`DUELS`) | **FUSO** nel racconto della scheda | Quando due lavori si contraddicono, lo dice la scheda in una riga; niente vista dedicata |
| Seconda pagina (`EXTRA`, 10 brevi) + «Continua a leggere» | **RETROCESSO** in archivio del giorno | Consultabile da «Altre N in archivio» nel verdetto; mai elencata nella schermata |
| «Sorprendimi» (`SCOPERTE`) | **FUSO** nella selezione del mattino | La serendipità diventa un criterio del selettore (ogni tanto una delle ≤3 è fuori perimetro, dichiarata nel «perché lo vedo»), non un bottone da premere |
| «Il tuo focus» (riviste/KOL/temi + suggerimenti `SUGGQ`) | **RETROCESSO** nel Profilo; suggerimenti **ELIMINATI** come proposte | La personalizzazione emerge dal gesto ✓/✗; le liste restano leggibili/correggibili nel Profilo, mai proposte |
| Industria & tecnologia · Congressi · Società | **RETROCESSO** (Rassegna/archivio) | Consultazione, non consumo quotidiano. Un richiamo che scotta entra nel verdetto |

## Le altre viste

| Elemento | Destino | Perché |
|---|---|---|
| Rassegna (9 fonti, sommario, sezioni) | **RETROCESSO** (raggiungibile da Archivio) | Sorveglianza consultabile; le sole cose urgenti (richiamo sorvegliato, ritrattazione su citato, consensus nuovo) **salgono nel verdetto** il giorno stesso |
| Archivio (calendario + ricerca + autocritica) | **RETROCESSO** (resta, com'è, dietro «Archivio») | È il magazzino: tutto ciò che scompare dal quotidiano finisce qui |
| Salvati | **FUSO** nell'archivio («i tuoi utili») | «Utile» archivia; una lista separata con badge di conteggio non serve più. Il controllo ritrattazioni sui salvati resta, e urla nel verdetto |
| Newsletter (slot, candidati, 3 versioni) | **RETROCESSO** in «Produzione» | Mestiere settimanale, momento suo; i candidati sono gli «utili» della settimana — la scelta del video si fa lì, mai sulle schede del mattino |
| Foglio social (36 combinazioni + Adatta) | **RETROCESSO** in «Produzione» | Idem; da valutare in seguito una potatura delle 36 combinazioni, fuori dallo scopo di questo documento |
| Impostazioni (85 elementi interattivi) | **FUSO** in una pagina Profilo unica, conversazionale | Frasi, non caselle: «Seguo queste riviste: … correggi». Dentro: liste, voce, testo grande, trasferimento/backup, cervello. Mai proposta, mai necessaria |
| «Manda i segnali a PULSE» | **ELIMINATO** (come gesto manuale) | Il giudizio ✓/✗ aggiorna i pesi da solo: il giro copia-incolla era il sintomo più chiaro del difetto 2.3 |
| Benvenuto + card Novità (`GUIDA_V`) | **ELIMINATO** | Anti-pattern §8: alla prima apertura si vede contenuto reale |
| Guida «?» | **ELIMINATO** come overlay; una pagina di note dentro il Profilo | Se serve spiegazione il design è sbagliato; le sole cose da dire (dove vivono i dati, il limite iOS) stanno nel Profilo |
| Badge contatore Salvati sulla barra | **ELIMINATO** | Anti-pattern §8: mai far sentire in debito |
| Barra 6 tab | **FUSO** in una riga di testo: Archivio · Produzione · Profilo | Tre destinazioni secondarie, non promosse |
| Lettura vocale `speechSynthesis` (schede, briefing, auto) | **ELIMINATO** | Sostituita dall'MP3 pre-generato + feed podcast (Parte II). Il lettore in app diventa: un pulsante, ±15 s, velocità, posizione ricordata |
| Comandi vocali / conversazione («apri la tre», cervello) | **RETROCESSO** (secondario, dal Profilo) | Non è sul percorso dei 60 secondi; il cervello resta un'estensione facoltativa |
| Promemoria/notifiche browser (`askNotif`) | **ELIMINATO** | Sostituito dalla consegna push vera (email col briefing completo + episodio podcast) |

## Ciò che NON si tocca

- La chiave `localStorage` **`pulse4`** e la memoria esistente (salvati, voti,
  testi adattati): migrano nel nuovo modello, non si azzerano. «Utile» eredita i
  salvati di oggi.
- Il cancello e il PRINCIPIO ZERO: ogni sottrazione va fatta **insieme** alle sue
  sentinelle, mai disattivandole per far passare una pubblicazione.
- L'archivio storico (`versioni/`), la raccolta notturna, il battito delle 7:15.

## I due mestieri, separati (verifica richiesta dal §7)

Confermato nel codice: oggi la produzione vive dentro il consumo
(`itemHTML` mette ✎ Social e Video su ogni scheda di lettura; la Newsletter è in
barra principale). Nel nuovo modello: **il mattino si consuma** (schermata unica,
✓/✗), **la settimana si produce** («Produzione»: i tuoi utili della settimana →
scelta video → tre testi). Nessun controllo di produzione compare mai nella
schermata quotidiana.
