# PULSE — Audit UX/UI (Fase 1, 20 agosto 2026)

Baseline pre-redesign. Nessuna modifica al codice in questa fase.
Screenshot dello stato attuale: `docs/before/` (29 immagini: 6 schede × mobile/desktop × chiaro/scuro + benvenuto, scheda aperta, pannello social, modalità auto, guida).

---

## 3.1 Ricognizione tecnica

| Aspetto | Stato |
|---|---|
| Stack | HTML + CSS + JavaScript **vanilla**, nessun framework, nessun build tool |
| Architettura | `index.html` = PRODOTTO di `modello.html` (codice) + `dati/giorno.js` (contenuti del giorno), ricomposto da `test/costruisci.py`. Un file servito, autosufficiente |
| Stato | `localStorage` chiave `pulse4`, migrazioni versionate (`PREFV`), fusione non distruttiva fra dispositivi |
| Routing | Nessuno: 6 viste commutate via `tab()` (display on/off), stato non riflesso nell'URL |
| Hosting | GitHub Pages, ramo `main`, root. PWA: `sw.js` network-first, `manifest.json` |
| Dipendenze runtime | **0** (nessun CDN, nessun pacchetto). Unico servizio esterno facoltativo: il Worker `chiedi/` |
| Peso | `index.html` 246 KB grezzi → **74 KB gzip** trasferiti. Nessuna immagine nel critico |
| File monolitici | `modello.html` **1.813 righe** (CSS+HTML+JS in un file — scelta architetturale del progetto, non incidente); `index.html` 2.053 (generato). Nessun altro file >430 righe |
| Duplicazioni | pattern `fermaVoce`-prima-di-agire ormai centralizzato; residui: 3 varianti di lista-articolo (`itemHTML`, `spBreveHTML`, righe rassegna) con markup simile non condiviso |
| Vulnerabilità | n/a (zero dipendenze). Superficie: `esc()` applicato sistematicamente sull'output dinamico |

## 3.2 Inventario funzionale (verificato, non dichiarato)

Ogni voce è coperta dal cancello (`test/verifica.sh`, **605 controlli**, verde stanotte sul push del briefing) e dal viaggio-utente Playwright (45 passi). «Tap» = tocchi dopo l'apertura dell'app.

| Funzione | Dove (modello.html) | Tap oggi | Verificata da |
|---|---|---|---|
| Stato del giorno (banner freschezza + verdetto) | `renderFresh`, `renderVerdict` | **0** | qualita, checklist |
| Lettura scheda (apri/chiudi) | `toggle`, `itemHTML` | 1 | qualita, logica |
| Scheda estesa (risultati, muto, confidenza, link) | `itemHTML` | 2 | qualita |
| Salva scheda (tap o swipe destro) | `toggleSave`, gesto touch | 1–2 | logica, salvati, memoria |
| Voto 👍/👎 | `vote` | 2 | logica, memoria |
| Podcast/lettura vocale (2 voci se dialogo) | `speakBrief`, `parla`, `_natQueue` | 1 | qualita |
| Modalità auto (playlist, PTT, velocità) | `apriAuto`, `autoVai`, `autoMic` | 1 | qualita + viaggio |
| Comandi vocali (vocabolario) / Chiedi a PULSE | `interpretaComando`, `chiediPulse` | 1 + voce | qualita (17 frasi) |
| Rassegna 9 fonti (sommario + soffietti) | `rassHTML`, `apriRassegna` | 1 | rassegna (21) |
| Seconda pagina + Sorprendimi | `renderSeconda`, `sorprendimi` | 1–2 | qualita, memoria |
| Tensioni «dove le prove non ti coprono» | `renderTens` | 0 (visibili) +1 dettaglio | qualita |
| Social 3 toni × 3 lunghezze × 4 formati + Adatta | `openSocial`, `socText` | 3 alla copia | social (20) |
| Newsletter (scelta 📹, 3 versioni, copia) | `pickWeek`, `renderNlOut` | 3–6 | newsletter (73) |
| Archivio + ricerca storica | `searchHist` | 1 + digitazione | checklist |
| Salvati + ricerca | `renderSaved` | 1 | salvati |
| Trasferimento fra dispositivi / backup file | `linkTrasferimento`, `esportaBackup` | 2–3 | trasferimento (25) |
| Segnali a PULSE 📡 | `segnaliTesto` | 2 | qualita |
| Benvenuto/novità + guida ❓ | `benvenutoHTML`, `guidaHTML` | 0 / 1 | qualita + viaggio |
| Preferenze (riviste, KOL, temi) + proposte | `suggAperte` ecc. | 1–2 | preferenze (65) |
| Dimensione testo / voce / velocità | `setTesto`, `popolaVoci`, `setRate` | 2 | qualita |

**Tutte funzionano.** Nessuna funzione morta trovata; nessun percorso che accetti dati di pazienti (vincolo §2.6: verificato — gli unici input liberi sono ricerche locali, «Adatta» sui testi social e la configurazione del cervello).

## 3.3 Inventario interfaccia e stati

Viste: Oggi · Rassegna · Archivio · Salvati · Newsletter · Impostazioni. Overlay: Social, Guida, Auto. Primo avvio: Benvenuto.

Stati **già progettati** (raro trovarli, qui ci sono): giorno senza allerte («Oggi niente mette in discussione quello che fai») · giornale non arrivato/in preparazione (3 stati del banner) · fonte esterna muta (dichiarata per nome) · nessun richiamo/trial/video («Nessun … oggi», mai finto) · archivio-che-cresce · salvati vuoti · cervello non collegato · voce non supportata · errore rete Rassegna.

Stati **mancanti o deboli**:
1. **Pre-render**: la pagina arriva vuota e si riempie via JS → **CLS 0,855** (misurato). È il difetto strutturale n.1.
2. Rassegna in caricamento: testo «Carico la rassegna…», nessuno skeleton.
3. Ricerca archivio/salvati senza risultati: lista vuota silenziosa, nessun «nessun risultato per “x”».
4. Stato offline esplicito: il SW serve la cache ma l'utente non sa che sta guardando ieri.
5. Copia riuscita: toast presente ma incoerente tra i flussi (a volte «Copiato», a volte nulla su desktop senza permessi clipboard).

## 3.4 Audit critico (per gravità; euristica violata tra parentesi)

**BLOCCANTI (esperienza)**
1. **CLS 0,855 e TBT 570 ms**: tutto il render è post-load in un colpo solo (Nielsen: visibilità dello stato; Core Web Vitals). L'app «salta» a ogni apertura — sul telefono, il momento più frequente.
2. **Gerarchia della vista Oggi invertita**: il primo blocco è l'audiobar (3 bottoni blu grandi), poi i tab, e SOLO POI la risposta alla domanda del giorno — due banner verdi separati che dicono quasi la stessa cosa (freschezza + verdetto). Il time-to-insight è a 0 tap ma sotto ~1,5 schermate di scroll mentale (Von Restorff: tutto pesa uguale, niente pesa).
3. **24 corpi tipografici distinti** (obiettivo ≤6) e **~30 esadecimali fuori dai token**: il sistema esiste (`:root` con variabili) ma è eroso; il colore non è più solo semantico (Refactoring UI; §5.1 del mandato).

**GRAVI**
4. Chip di testata «9 · ✓9/9 · ↻ · ❓»: due numeri senza etichetta a colpo d'occhio (match sistema-mondo reale; test dei 5 secondi fallito su questa riga).
5. Copertina del PICK con **gradiente decorativo verde a onda**: estetica vietata dal mandato e peso visivo che compete col titolo (contrasto informazione/decorazione).
6. **Emoji come sistema iconografico** (tab, tasti, sezioni): funzionano, ma su iOS/desktop rendono in modo incoerente e collidono con l'estetica Bloomberg/Linear richiesta. Nota: i pallini 🔴🟠🟢⚪ sono già CSS (`.dot`), NON emoji — il significato è salvo.
7. Desktop = colonna mobile allargata con sidebar: la densità «compatta da scansione» richiesta per i job 2–3 non esiste come modalità dichiarata (confronto affiancato dei candidati assente).
8. Contrasto AA non ovunque (Lighthouse `color-contrast`; i `--dim` su tinta chiara falliscono in alcuni punti) e `label-content-name-mismatch` su alcuni bottoni; manca il landmark `<main>`.

**MEDI**
9. Azioni per scheda (★ 👍 👎 Social Video Dettagli) sempre tutte visibili → 6 controlli × 9 schede = 54 bersagli nella lista (Hick). Nessuna progressive disclosure.
10. Testi di sistema in gran parte buoni (onesti, in italiano), ma incoerenze di nome: «Salva/Salvata/★», «Copia il link/Copiato».
11. URL senza stato: refresh o condivisione perdono la vista corrente (Jakob: convenzioni web).
12. Skeleton assenti dove c'è attesa reale (Rassegna).

## 3.5 Baseline misurata (Lighthouse 12.x su Chromium sandbox, throttling di default; 4G simulato via CDP)

| Metrica | Mobile | Desktop |
|---|---|---|
| Performance | **59** | 76 |
| Accessibility | **94** | 94 |
| Best practices | 100 | — |
| FCP / LCP | 2,1 s / 2,1 s | — |
| TBT | 570 ms | — |
| **CLS** | **0,855** | — |
| Primo contenuto (4G CDP) | FCP 384 ms · DCL 1,47 s | — |
| Trasferito | 74 KB gzip, 1 richiesta critica | idem |
| Famiglie tipografiche | 1 (system stack) ✅ | — |
| Corpi tipografici | **24** | — |

**Tap dei tre job (misurati):**
- JOB 1 «cosa c'è di nuovo oggi»: **0 tap** (banner + verdetto visibili all'apertura) — già ≤1, ma sepolto sotto audiobar e tab (v. difetto 2).
- JOB 2 apertura → testo social pronto e copiato: **3 tap** (scheda → ✎ Social → Copia).
- JOB 3 selezione settimanale → newsletter copiata: **3–6 tap** (📹 per scheda scelta → Newsletter → Copia).

**Vantaggio strutturale da non perdere nel redesign**: 0 dipendenze, 74 KB, un file, 605 controlli automatici che coprono ogni funzione, PRINCIPIO ZERO meccanizzato. Qualsiasi direzione di design deve passare da quel cancello, ed è una garanzia che nessun competitor ha.
