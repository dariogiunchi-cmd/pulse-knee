#!/usr/bin/env bash
# PULSE — pubblicazione. L'unica strada consentita per mandare l'app online.
#
#   PULSE_TOKEN=ghp_... bash test/pubblica.sh "2026-08-02" "descrizione del commit"
#
# Fa, in quest'ordine:
#   1. verifica completa      → se fallisce, NON pubblica e non tocca nulla
#   2. clona il repository    → così istantanee e cervello NON vengono cancellati
#   3. copia i file del sito e i test
#   4. salva l'istantanea datata e applica la ritenzione
#   5. commit e push (non forzato: la storia resta)
#   6. riscarica dallo SHA e riverifica il file davvero online
#
# NON scrive mai il token a schermo.

set -uo pipefail
QUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP="$(cd "$QUI/.." && pwd)"
DATA="${1:-$(date +%F)}"
MSG="${2:-PULSE $DATA}"
REPO_URL_PUB="https://github.com/dariogiunchi-cmd/pulse-knee.git"
RAW="https://raw.githubusercontent.com/dariogiunchi-cmd/pulse-knee"

if [ -z "${PULSE_TOKEN:-}" ]; then
  echo "❌ Manca PULSE_TOKEN. Il token sta in claude/10-deploy.md, non in questo file."
  exit 2
fi
AUTH="https://dariogiunchi-cmd:${PULSE_TOKEN}@github.com/dariogiunchi-cmd/pulse-knee.git"
mask() { sed -e "s/${PULSE_TOKEN}/***/g"; }

# ---------------------------------------------------------------- 1. verifica
echo "▶ 1/6  verifica"
if ! bash "$QUI/verifica.sh" "$APP/index.html"; then
  echo
  echo "⛔ PUBBLICAZIONE ANNULLATA. Il sito online resta quello di ieri, intatto."
  exit 1
fi

# ---------------------------------------------------------------- 2. clone
echo
echo "▶ 2/6  clono il repository (per non perdere istantanee e cervello)"
LAVORO="$(mktemp -d)"
trap 'rm -rf "$LAVORO"' EXIT
if ! GIT_TERMINAL_PROMPT=0 git clone -q "$AUTH" "$LAVORO/repo" 2>&1 | mask; then
  echo "❌ clone fallito"; exit 3
fi
cd "$LAVORO/repo"
git config user.email "noreply@anthropic.com"
git config user.name "Claude"
PRIMA="$(git rev-parse HEAD)"
echo "   versione online prima di ora: ${PRIMA:0:7}"

# ------------------------------------------------- 2b. il fermo contro la sovrascrittura
# Difetto pagato la sera del 4 agosto 2026, e va capito bene perché è subdolo.
# Alle 18:51 sono state pubblicate quattro correzioni. Alle 18:53 è partito il briefing,
# che ha clonato il repository un istante PRIMA che quella pubblicazione fosse visibile.
# Alle 19:10 il briefing ha pubblicato: il clone di partenza era fresco, il push non è
# stato forzato, la storia è rimasta lineare — e le quattro correzioni sono sparite lo
# stesso, perché il passo 3 copia index.html sopra il clone senza chiedersi da quale
# versione quel file discenda.
# Nessun allarme è suonato: 464 controlli verdi su un file che aveva appena cancellato
# il lavoro di mezz'ora prima. Le suite collaudano il contenuto, non la discendenza.
# Da qui in avanti la discendenza si verifica: se la copia di lavoro nasce da una
# versione più vecchia di quella online, non si pubblica.
BASE="$(git -C "$APP" rev-parse HEAD 2>/dev/null || true)"
if [ -z "$BASE" ]; then
  echo "   ⚠️  la copia di lavoro non è un repository git: impossibile verificare da quale"
  echo "       versione discende. Procedo, ma questa è la condizione in cui si sovrascrive."
elif [ "$BASE" != "$PRIMA" ]; then
  if git cat-file -e "$BASE^{commit}" 2>/dev/null && git merge-base --is-ancestor "$BASE" "$PRIMA"; then
    echo
    echo "⛔ PUBBLICAZIONE ANNULLATA — la tua copia di lavoro è indietro."
    echo
    echo "   tu parti da:  ${BASE:0:7}"
    echo "   online c'è:   ${PRIMA:0:7}"
    echo
    echo "   Nel frattempo qualcun altro ha pubblicato:"
    git log --pretty='     · %h %ad %s' --date=format:'%d/%m %H:%M' "$BASE..$PRIMA" | head -10
    echo
    echo "   File toccati da quelle pubblicazioni:"
    git diff --name-only "$BASE" "$PRIMA" | sed 's/^/     · /' | head -15
    echo
    echo "   Pubblicare ora cancellerebbe quel lavoro senza che nessun test se ne accorga."
    echo "   Fai così, nell'ordine:"
    echo "     1)  cd $APP && git fetch origin main && git log --oneline HEAD..origin/main"
    echo "     2)  metti da parte le tue modifiche (git diff > /tmp/mie.patch)"
    echo "     3)  git reset --hard origin/main"
    echo "     4)  riapplica le tue modifiche sopra il nuovo stato e rilancia la verifica"
    echo
    echo "   Se — e solo se — sei certo che nulla vada perso: PULSE_SOVRASCRIVI=1 davanti al comando."
    [ "${PULSE_SOVRASCRIVI:-}" = "1" ] || exit 4
    echo "   ⚠️  PULSE_SOVRASCRIVI=1: proseguo sovrascrivendo. Scelta tua, dichiarata."
  else
    echo "   ℹ️  la copia di lavoro ha una storia divergente da quella online (${BASE:0:7} non"
    echo "       discende da ${PRIMA:0:7}). Non è il caso della sovrascrittura silenziosa; proseguo."
  fi
else
  echo "   ✓ la copia di lavoro discende esattamente da ciò che è online"
fi

# ---------------------------------------------------------------- 3. file
echo
echo "▶ 3/6  copio i file del sito"
for f in index.html manifest.json sw.js .nojekyll apple-touch-icon.png \
         icon-192.png icon-512.png icon-maskable-512.png; do
  if [ -f "$APP/$f" ]; then cp "$APP/$f" "./$f"; else echo "   ⚠️  assente in locale, tengo quello online: $f"; fi
done
mkdir -p test && cp "$QUI"/*.py "$QUI"/*.js "$QUI"/*.sh test/ 2>/dev/null
rm -rf test/__pycache__ cervello/__pycache__
[ -f "$APP/.gitignore" ] && cp "$APP/.gitignore" ./.gitignore
[ -d "$APP/cervello" ] && { mkdir -p cervello && cp "$APP/cervello/"* cervello/ 2>/dev/null; }

# File non più serviti da nessuna pagina. Il clone non cancella nulla da solo:
# vanno tolti qui, esplicitamente, e restano recuperabili dalla storia di git.
for f in pulse_brief.mp3; do
  if [ -f "./$f" ] && [ ! -f "$APP/$f" ]; then
    git rm -q --cached "$f" 2>/dev/null; rm -f "./$f"
    echo "   🧹 tolto dal repository (mai richiesto da nessuna pagina): $f"
  fi
done

# ---------------------------------------------------------------- 4. istantanea
echo
echo "▶ 4/6  istantanea del $DATA"
python3 "$QUI/istantanea.py" "$(pwd)" "./index.html" "$DATA" || { echo "❌ istantanea fallita"; exit 4; }

# controllo finale: nessuna credenziale in ciò che sto per rendere pubblico
if grep -rEl 'ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}' . \
     --exclude-dir=.git --exclude=*.png --exclude=*.mp3 2>/dev/null | grep -q .; then
  echo "❌ TROVATA UNA CREDENZIALE nei file da pubblicare. Fermo tutto."
  grep -rEl 'ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}' . --exclude-dir=.git 2>/dev/null
  exit 5
fi

# ---------------------------------------------------------------- 5. push
echo
echo "▶ 5/6  pubblico"
git add -A
if git diff --cached --quiet; then
  echo "   niente da pubblicare: identico a quanto è già online."
  exit 0
fi
# La firma dei commit e' configurata a livello globale in questo ambiente e GitHub
# la verifica: disattivarla — come faceva la vecchia procedura con
# `-c commit.gpgsign=false` — rendeva ogni pubblicazione "Unverified".
git commit -q -m "$MSG"
if ! git cat-file commit HEAD | grep -q "^gpgsig"; then
  echo "   ⚠️  commit non firmato: GitHub lo mostrera' come Unverified"
fi
if ! GIT_TERMINAL_PROMPT=0 git push -q "$AUTH" HEAD:main 2>&1 | mask; then
  echo "❌ push fallito. Online resta ${PRIMA:0:7}."; exit 6
fi
SHA="$(git rev-parse HEAD)"
echo "   pubblicato: ${SHA:0:7}   (per tornare indietro: ${PRIMA:0:7})"

# ---------------------------------------------------------------- 6. riverifica
echo
echo "▶ 6/6  riscarico dal repository e riverifico ciò che è davvero online"
sleep 20
CTRL="$LAVORO/online"; mkdir -p "$CTRL"
for f in index.html manifest.json sw.js apple-touch-icon.png icon-192.png icon-512.png icon-maskable-512.png; do
  curl -s "$RAW/$SHA/$f" -o "$CTRL/$f"
done
touch "$CTRL/.nojekyll"
if ! diff -q "$CTRL/index.html" "$APP/index.html" >/dev/null; then
  echo "❌ il file online NON corrisponde a quello locale."
  echo "   torna indietro:  curl -s $RAW/$PRIMA/index.html -o index.html  e ripubblica"
  exit 7
fi
echo "   il file online è identico a quello verificato ✅"
# Il file è già risultato IDENTICO byte per byte a quello verificato: rieseguire le
# suite nel browser darebbe per costruzione lo stesso esito e raddoppierebbe i tempi.
# Qui serve solo controllare che anche gli ALTRI file siano arrivati interi.
if ! PULSE_HTML="$CTRL/index.html" python3 "$QUI/checklist.py" >/dev/null 2>&1; then
  echo "❌ i file online non superano il controllo strutturale. Torna a ${PRIMA:0:7}."
  PULSE_HTML="$CTRL/index.html" python3 "$QUI/checklist.py" | grep '^❌'
  exit 8
fi

# La pubblicazione avviene da un clone temporaneo: senza questo passo la copia di
# lavoro in $APP resta indietro rispetto a ciò che è online, e ogni sessione
# successiva riparte da uno stato che sembra "modificato ma non pubblicato".
echo
echo "▶ allineo la copia di lavoro con ciò che è online"
if [ -d "$APP/.git" ]; then
  # Oltre a riportare i file, va aggiornato anche il riferimento locale a origin/main:
  # la pubblicazione avviene da un clone temporaneo, quindi la copia di lavoro non se ne
  # accorge da sola e continua a credere di avere commit non ancora spinti.
  ( cd "$APP" \
    && GIT_TERMINAL_PROMPT=0 git fetch -q "$AUTH" main 2>&1 | mask \
    && git reset -q --hard FETCH_HEAD \
    && git update-ref refs/remotes/origin/main "$SHA" \
    && rm -rf test/__pycache__ ) \
    && echo "   copia di lavoro allineata a ${SHA:0:7} (file e riferimento a GitHub)" \
    || echo "   ⚠️  allineamento non riuscito: la pubblicazione è comunque andata a buon fine"
fi

echo
echo "═══════════════════════════════════════════════════════════"
echo "  ✅ ONLINE E VERIFICATO — $DATA"
echo "     https://dariogiunchi-cmd.github.io/pulse-knee/"
echo "     versione ${SHA:0:7} · precedente ${PRIMA:0:7}"
echo "     istantanee: /pulse-knee/versioni/"
echo "═══════════════════════════════════════════════════════════"
