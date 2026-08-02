#!/usr/bin/env bash
# PULSE — verifica completa. Nessuna pubblicazione senza che questo dia verde.
#
#   bash test/verifica.sh                      verifica /home/claude/deploy/index.html
#   bash test/verifica.sh /altro/index.html    verifica un altro file (es. quello scaricato dal repo)
#
# Esce con 0 solo se TUTTO passa. Qualsiasi altro codice = non pubblicare.

set -uo pipefail
QUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PULSE_HTML="${1:-$(cd "$QUI/.." && pwd)/index.html}"

if [ ! -f "$PULSE_HTML" ]; then
  echo "❌ File non trovato: $PULSE_HTML"; exit 2
fi

echo "═══════════════════════════════════════════════════════════"
echo "  PULSE — verifica prima della pubblicazione"
echo "  file: $PULSE_HTML"
echo "═══════════════════════════════════════════════════════════"
echo

FALLITE=()
VERDI=0

TIMEOUT="${PULSE_TIMEOUT:-180}"

esegui() {                      # esegui <etichetta> <comando...>
  local nome="$1"; shift
  local out; local rc
  out="$(timeout "$TIMEOUT" "$@" 2>&1)"; rc=$?
  if [ $rc -eq 124 ]; then
    printf "  ❌ %-34s BLOCCATA (oltre %ss)\n" "$nome" "$TIMEOUT"
    FALLITE+=("$nome (bloccata)")
    return
  fi
  local n; n=$(printf '%s\n' "$out" | grep -c '^✅\|^PASS' || true)
  if [ $rc -eq 0 ]; then
    printf "  ✅ %-34s %3s controlli\n" "$nome" "$n"
    VERDI=$((VERDI + n))
  else
    printf "  ❌ %-34s FALLITA\n" "$nome"
    printf '%s\n' "$out" | grep -E '^❌|^FAIL|Error|error:' | head -6 | sed 's/^/       /'
    FALLITE+=("$nome")
  fi
}

# --- primo cancello: struttura e sintassi. Se fallisce qui, inutile aprire un browser:
#     un errore di sintassi lascerebbe le suite in attesa di elementi che non arriveranno mai.
esegui "struttura e credenziali" python3 "$QUI/checklist.py"
if [ ${#FALLITE[@]} -gt 0 ]; then
  echo
  echo "═══════════════════════════════════════════════════════════"
  echo "  ❌ NON PUBBLICARE — il controllo strutturale è fallito."
  echo "     Le suite nel browser non vengono nemmeno avviate."
  echo "═══════════════════════════════════════════════════════════"
  exit 1
fi

esegui "logica"                  node    "$QUI/logica.js"
esegui "adattamento mobile"      python3 "$QUI/mobile.py"
esegui "qualità dei contenuti"   python3 "$QUI/qualita.py"
esegui "contenuti social"        python3 "$QUI/social.py"
esegui "newsletter (email)"      python3 "$QUI/newsletter.py"
esegui "memoria delle scelte"    python3 "$QUI/memoria.py"
esegui "blog e Google"           python3 "$QUI/distribuzione.py"
esegui "preferenze e migrazione" python3 "$QUI/preferenze.py"

echo
echo "═══════════════════════════════════════════════════════════"
if [ ${#FALLITE[@]} -gt 0 ]; then
  echo "  ❌ NON PUBBLICARE — suite fallite: ${FALLITE[*]}"
  echo "═══════════════════════════════════════════════════════════"
  exit 1
fi
echo "  ✅ $VERDI controlli superati — si può pubblicare"
echo "═══════════════════════════════════════════════════════════"
exit 0
