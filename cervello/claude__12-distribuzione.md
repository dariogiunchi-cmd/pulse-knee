# PULSE — distribuzione: una scelta, tre destinazioni

*Costruita il 2 agosto 2026. Primo ciclo previsto: video da settembre, primo invio e prima
pubblicazione a fine settembre 2026.*

## Il principio

Lui sceglie **un lavoro a settimana** toccando `📹 Video` su una scheda. Nient'altro.
A fine mese quei quattro lavori diventano **tre testi già scritti**:

| Destinazione | Dove | Che cosa fa lui |
|---|---|---|
| **✉️ Email** | Brevo → medici curanti, fisioterapisti, pazienti | copia, incolla, programma |
| **🌐 Blog** | Wix, www.dariogiunchi.ch/blog | copia titolo+descrizione in SEO, corpo nel post |
| **📍 Google** | Google Business Profile, «Aggiungi aggiornamento» | copia, incolla |

Stesso contenuto, tre forme. Il lavoro intellettuale è già fatto ogni mattina dentro `NLB`.

## Perché tre forme e non un solo testo

- **Email**: relazione. Chi la riceve lo conosce già. Regge il tono da collega, i numeri,
  il limite dichiarato. Due versioni (professionisti / pazienti).
- **Blog**: ricerca. È l'unico dei tre che genera visibilità duratura su Google. Serve
  titolo ≤65 caratteri, meta description ≤170, sottotitoli `##`, parole chiave **dentro
  al testo** (non hashtag), fonti esplicite. È anche l'unico che vive per anni.
- **Google Business Profile**: prossimità. Massimo 1500 caratteri, ma su telefono si
  leggono le **prime ~100 lettere** prima di «Altro»: il senso deve stare già lì.
  Serve a portare al blog e a rinnovare il profilo (segnale di attività locale).

## Il vincolo che decide il tono — non è stile, è legge

Base legale: **LPMed art. 40 lett. d** (RS 811.11) e **Legge sanitaria ticinese art. 70**.
L'informazione al pubblico deve essere **oggettiva**, corrispondere a un **interesse
pubblico** e **non essere ingannevole né invasiva**.

Vietato in tutti e tre i testi: inviti all'azione («prenota», «chiama ora»), sconti,
prestazioni gratuite, promesse di risultato, «senza rischi», superlativi comparativi,
specializzazioni non riconosciute MEBEKO, pazienti riconoscibili.

**Conseguenza pratica, ed è la parte che conta.** L'autorevolezza non si ottiene
nonostante questi limiti: si ottiene **grazie** a essi. Un testo che scrive «questo studio
è troppo piccolo per dimostrarlo» è più credibile di uno che promette. Per questo la nota
critica dei blurb non è un obbligo formale — è ciò che distingue il testo da una
pubblicità. `test/distribuzione.py` cerca dodici parole vietate in tutti e tre i testi a
ogni pubblicazione, e la blocca se ne trova una.

## Automazione: che cosa è realmente possibile

Verificato il 2 agosto 2026, non ipotizzato.

**Wix.** Esiste `POST https://www.wixapis.com/blog/v3/draft-posts` per creare un post in
bozza. Richiede però **l'installazione di una app OAuth Wix** con permesso *Manage Blog*:
una chiave API non basta.

**Google Business Profile.** L'API esiste (`accounts.locations.localPosts`) ma è dietro un
**cancello di approvazione**: profilo verificato e attivo da oltre 60 giorni, sito web,
progetto Google Cloud e una domanda formale («Application for Basic API Access»). Finché
la quota resta a 0 QPM non è approvata; i tempi non sono dichiarati e il rifiuto è
frequente per chi non è agenzia.

**Giudizio onesto: non conviene.** Il copia-incolla mensile costa circa tre minuti in
tutto. Un'integrazione OAuth su due piattaforme costa una configurazione, si rompe quando
scadono i token, e va rifatta. Tre minuti al mese non giustificano un sistema che può
fallire in silenzio — e il fallimento silenzioso è esattamente il difetto che PULSE esiste
per non avere.

**L'alternativa che vale, se un giorno i tre minuti diventassero troppi:** con l'app
desktop di Claude aperta, la sessione può guidare il suo browser già autenticato e
incollare al posto suo, mentre lui guarda. Nessuna chiave, nessuna app OAuth, nessun token
che scade. Da valutare dopo il primo ciclo reale, non prima.

## Struttura dei testi generati

**Blog** — `blogText()`
```
TITOLO DELLA PAGINA           ≤65 caratteri
DESCRIZIONE PER GOOGLE        ≤170 caratteri
INDIRIZZO DELLA PAGINA        slug generato da slugify()
PAROLE CHIAVE                 da NLB[n].kw, max 10, senza hashtag
——— DA QUI IN GIÙ: INCOLLA NEL BLOG ———
apertura · 4 sezioni ## con corpo, nota, Fonte (rivista per esteso + PubMed),
link al video se presente · ## In breve · disclaimer · firma FMH
```

**Google** — `gbpText()`
```
riga d'apertura (il senso sta nei primi 100 caratteri)
che cosa è questa rubrica, in due righe
• quattro titoli in parole semplici
link al post del blog (campo S.blogUrl, modificabile nell'app)
firma
```
Contatore caratteri sempre visibile. Oltre 1500 il testo si accorcia da solo, mai a metà
parola, e il link resta.

## Che cosa deve fare il briefing quotidiano

Generare `NLB` per **ogni** lavoro del giorno. Regole complete in
`claude/11-qualita.md` §10.

## Da chiedergli, una volta sola

- La newsletter parte da una lista che oggi non esiste: chi ci va dentro, e come raccoglie
  il consenso (nLPD). Serve prima del primo invio, non prima di settembre.
- Google Business Profile: il profilo è già verificato e attivo?
