/* PULSE — «Chiedi a PULSE»: il cervello esterno.
 *
 * PERCHÉ ESISTE. L'app è una pagina statica su GitHub Pages: non può custodire
 * una chiave API (chiunque la leggerebbe nel sorgente). Questo Worker gira su
 * Cloudflare (piano gratuito), custodisce le chiavi come secret, e offre due
 * porte all'app:
 *   POST /chiedi  { parola, domanda, storia? }  → { risposta }
 *       Conversazione libera con Claude, col giornale del giorno come contesto.
 *   POST /voce    { parola, testo, voce: "A"|"B" } → audio/mpeg
 *       Voce naturale (OpenAI TTS). "A" e "B" sono le due voci del podcast.
 *
 * SICUREZZA. Ogni richiesta porta la `parola` (secret PAROLA): senza, 401.
 * La parola la sceglie il Dr. Giunchi e la scrive UNA volta nell'app
 * (Impostazioni → Il cervello di PULSE); vive solo nel suo telefono.
 *
 * PRINCIPIO ZERO anche qui: il sistema di istruzioni impone di NON inventare
 * citazioni né numeri, di dichiarare ciò che non è nei dati del giorno, e di
 * rispondere in breve (si ascolta in auto). Niente linguaggio pubblicitario.
 *
 * Secret richiesti (wrangler secret put …):
 *   PAROLA               la parola d'ordine condivisa con l'app
 *   ANTHROPIC_API_KEY    console.anthropic.com
 *   OPENAI_API_KEY       platform.openai.com (solo per /voce; senza, /voce dice 503)
 * Variabili opzionali: MODELLO (default claude-haiku-4-5), VOCE_A, VOCE_B.
 */

const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

const DATI_URL = 'https://raw.githubusercontent.com/dariogiunchi-cmd/pulse-knee/main/dati/giorno.js';

function json(corpo, stato) {
  return new Response(JSON.stringify(corpo), {
    status: stato || 200,
    headers: { 'Content-Type': 'application/json; charset=utf-8', ...CORS },
  });
}

/* Il contesto: i dati del giorno, presi dal repository pubblico (cache 30 min).
   Si mandano quasi interi: è il giornale che l'utente ha davanti, e Claude deve
   rispondere SU QUELLO prima che sul sapere generale. */
async function contesto() {
  const r = await fetch(DATI_URL, { cf: { cacheTtl: 1800, cacheEverything: true } });
  if (!r.ok) return '';
  const t = await r.text();
  return t.slice(0, 120000);
}

const SISTEMA = `Sei PULSE, l'assistente scientifico personale del Dr. Dario Giunchi,
chirurgo ortopedico FMH dedicato al ginocchio (Ticino). Ti parla a voce, spesso in auto.

REGOLE NON NEGOZIABILI:
1. MAI inventare titoli, autori, riviste, DOI, PMID, numeri o risultati. Se un dato
   non è nel giornale del giorno (qui sotto) e non sei certo del sapere generale,
   dillo: «questo non è nei dati di oggi e non posso verificarlo ora».
2. Rispondi in ITALIANO, in forma PARLATA e BREVE: di norma sotto le 100 parole,
   frasi semplici, niente elenchi puntati, niente simboli — verrà letto a voce.
   Se serve più dettaglio, chiudi offrendo: «vuoi che approfondisca?».
3. Niente linguaggio promozionale o promesse di risultato (vincolo legale svizzero).
4. Se la domanda riguarda un paziente specifico, ricordagli in una riga che la
   decisione clinica resta sua: tu porti la letteratura, non la visita.
5. Livello: consulente senior che parla a un pari. Se un suo ragionamento è debole,
   diglielo.

IL GIORNALE DI OGGI (variabili JavaScript, sono i dati verificati del mattino):
`;

async function chiedi(b, env) {
  const dati = await contesto();
  const storia = Array.isArray(b.storia) ? b.storia.slice(-8) : [];
  const messaggi = storia
    .filter(m => m && (m.ruolo === 'utente' || m.ruolo === 'pulse') && m.t)
    .map(m => ({ role: m.ruolo === 'utente' ? 'user' : 'assistant', content: String(m.t).slice(0, 2000) }));
  messaggi.push({ role: 'user', content: String(b.domanda || '').slice(0, 2000) });
  const r = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: {
      'x-api-key': env.ANTHROPIC_API_KEY,
      'anthropic-version': '2023-06-01',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      model: env.MODELLO || 'claude-haiku-4-5',
      max_tokens: 700,
      system: SISTEMA + dati,
      messages: messaggi,
    }),
  });
  if (!r.ok) {
    const err = await r.text();
    return json({ errore: 'il modello non ha risposto', dettaglio: err.slice(0, 200) }, 502);
  }
  const j = await r.json();
  const testo = (j.content || []).filter(c => c.type === 'text').map(c => c.text).join(' ').trim();
  return json({ risposta: testo || 'Non ho una risposta.' });
}

async function voce(b, env) {
  if (!env.OPENAI_API_KEY) return json({ errore: 'voce naturale non configurata' }, 503);
  const quale = b.voce === 'B' ? (env.VOCE_B || 'onyx') : (env.VOCE_A || 'nova');
  const r = await fetch('https://api.openai.com/v1/audio/speech', {
    method: 'POST',
    headers: {
      Authorization: 'Bearer ' + env.OPENAI_API_KEY,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      model: 'gpt-4o-mini-tts',
      voice: quale,
      input: String(b.testo || '').slice(0, 3500),
      instructions: 'Parla in italiano naturale, tono da podcast professionale, ritmo tranquillo.',
      response_format: 'mp3',
    }),
  });
  if (!r.ok) {
    const err = await r.text();
    return json({ errore: 'sintesi vocale non riuscita', dettaglio: err.slice(0, 200) }, 502);
  }
  return new Response(r.body, { headers: { 'Content-Type': 'audio/mpeg', ...CORS } });
}

export default {
  async fetch(req, env) {
    if (req.method === 'OPTIONS') return new Response(null, { headers: CORS });
    if (req.method !== 'POST') return json({ errore: 'solo POST' }, 405);
    let b;
    try { b = await req.json(); } catch (e) { return json({ errore: 'corpo non valido' }, 400); }
    if (!env.PAROLA || b.parola !== env.PAROLA) return json({ errore: 'parola d’ordine mancante o errata' }, 401);
    const percorso = new URL(req.url).pathname;
    try {
      if (percorso === '/chiedi') return await chiedi(b, env);
      if (percorso === '/voce') return await voce(b, env);
    } catch (e) {
      return json({ errore: 'errore interno', dettaglio: String(e).slice(0, 200) }, 500);
    }
    return json({ errore: 'percorso sconosciuto' }, 404);
  },
};
