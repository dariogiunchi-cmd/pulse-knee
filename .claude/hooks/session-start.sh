#!/bin/bash
# PULSE — preparazione dell'ambiente all'avvio di una sessione Claude Code sul web.
#
# PERCHÉ ESISTE. Il 17 agosto 2026 `test/verifica.sh` si è fermata al cancello zero:
# Playwright non era installato. Installandolo senza vincolo di versione arriva la
# 1.62, che pretende Chromium build 1234, mentre l'immagine di sistema ne contiene
# una sola, la 1194. Risultato: nove suite su dodici fallite con
# «Executable doesn't exist», e una sessione distratta avrebbe potuto concludere che
# fosse l'app a essere rotta — esattamente ciò che il cancello zero vuole impedire.
#
# La 1.56.0 è la versione che corrisponde al Chromium 1194 già presente. Non
# aggiornarla senza aver prima verificato quale build si trova in /opt/pw-browsers.
set -euo pipefail

# Sul Mac del Dr. Giunchi Playwright si porta dietro il proprio Chromium: nessun
# vincolo di versione da rispettare, e nessun motivo di installare niente.
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

ATTESA="1.56.0"
ORA="$(python3 -c "import importlib.metadata as m; print(m.version('playwright'))" 2>/dev/null || echo "")"

if [ "$ORA" != "$ATTESA" ]; then
  echo "PULSE · installo playwright==$ATTESA (trovato: ${ORA:-nessuno})"
  pip install -q "playwright==$ATTESA" --break-system-packages
else
  echo "PULSE · playwright $ATTESA già presente"
fi

# Prova vera: il browser si apre davvero? Un import riuscito non lo garantisce —
# è proprio la differenza fra i due che ha prodotto le nove suite rosse.
if python3 -c "
from playwright.sync_api import sync_playwright
with sync_playwright() as p: p.chromium.launch().close()
" 2>/dev/null; then
  echo "PULSE · Chromium si apre — test/verifica.sh è eseguibile"
else
  echo "PULSE · ATTENZIONE: Chromium non si apre. Le suite nel browser falliranno."
  echo "PULSE · Non è l'app a essere rotta: NON modificare index.html per far passare i test."
  echo "PULSE · Controlla quale build c'è in /opt/pw-browsers e allinea la versione qui sopra."
fi
