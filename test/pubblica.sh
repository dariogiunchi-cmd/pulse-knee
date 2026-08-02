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

# ---------------------------------------------------------------- 3. file
echo
echo "▶ 3/6  copio i file del sito"
for f in index.html manifest.json sw.js .nojekyll apple-touch-icon.png \
         icon-192.png icon-512.png icon-maskable-512.png; do
  if [ -f "$APP/$f" ]; then cp "$APP/$f" "./$f"; else echo "   ⚠️  assente in locale, tengo quello online: $f"; fi
done
mkdir -p test && cp "$QUI"/*.py "$QUI"/*.js "$QUI"/*.sh test/ 2>/dev/null
[ -d "$APP/cervello" ] && { mkdir -p cervello && cp "$APP/cervello/"* cervello/ 2>/dev/null; }

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
git -c commit.gpgsign=false commit -q -m "$MSG"
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

echo
echo "═══════════════════════════════════════════════════════════"
echo "  ✅ ONLINE E VERIFICATO — $DATA"
echo "     https://dariogiunchi-cmd.github.io/pulse-knee/"
echo "     versione ${SHA:0:7} · precedente ${PRIMA:0:7}"
echo "     istantanee: /pulse-knee/versioni/"
echo "═══════════════════════════════════════════════════════════"
