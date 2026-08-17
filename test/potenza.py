#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PULSE — il MUTO si calcola, non si dichiara a sensazione.

«Uno studio che non può escludere l'effetto non è negativo, è muto» è un principio
del sistema fin dal 2 agosto — ma finora il giudizio era a occhio. Questo strumento
dà al briefing il numero: dato un confronto con esito binario, calcola l'intervallo
di confidenza al 95% del rischio relativo (metodo di Katz) e della differenza di
rischio, e li traduce nella frase onesta: che cosa lo studio NON può escludere.

Uso (dal mandato del mattino, quando si scrive un MUTE):
  python3 test/potenza.py <eventi1> <n1> <eventi2> <n2>
  python3 test/potenza.py 6 46 3 63        # es.: 13,0% vs 4,8%
  python3 test/potenza.py --collaudo       # verifica se stesso su casi noti

Con zero eventi in un braccio usa la regola del tre (limite superiore ≈ 3/n).
"""
import math, sys


def katz_rr(e1, n1, e2, n2):
    """RR (gruppo1 vs gruppo2) con IC 95% log-normale di Katz.
    Correzione di continuità +0,5 ovunque se un braccio ha zero eventi."""
    if e1 == 0 or e2 == 0:
        e1, e2, n1, n2 = e1 + .5, e2 + .5, n1 + 1, n2 + 1
    rr = (e1 / n1) / (e2 / n2)
    se = math.sqrt(1 / e1 - 1 / n1 + 1 / e2 - 1 / n2)
    return rr, rr * math.exp(-1.96 * se), rr * math.exp(1.96 * se)


def wald_rd(e1, n1, e2, n2):
    """Differenza di rischio con IC 95% di Wald."""
    p1, p2 = e1 / n1, e2 / n2
    se = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    d = p1 - p2
    return d, d - 1.96 * se, d + 1.96 * se


def riassunto(e1, n1, e2, n2):
    p1, p2 = 100 * e1 / n1, 100 * e2 / n2
    righe = [f"gruppo 1: {e1}/{n1} ({p1:.1f}%) · gruppo 2: {e2}/{n2} ({p2:.1f}%)"]
    if e1 == 0 and e2 == 0:
        righe.append(f"zero eventi in entrambi i bracci: regola del tre — il tasso reale può "
                     f"arrivare a {300/n1:.1f}% e {300/n2:.1f}%. Nessun confronto possibile.")
        return "\n".join(righe)
    rr, lo, hi = katz_rr(e1, n1, e2, n2)
    d, dlo, dhi = wald_rd(e1, n1, e2, n2)
    righe.append(f"rischio relativo {rr:.2f} (IC 95% {lo:.2f}–{hi:.2f})")
    righe.append(f"differenza di rischio {100*d:+.1f} punti (IC 95% {100*dlo:+.1f} / {100*dhi:+.1f})")
    if lo <= 1 <= hi:
        righe.append(f"→ non significativo, ma l'intervallo NON esclude né un rischio "
                     f"{'ridotto fino a RR '+format(lo,'.2f') if lo<1 else ''}"
                     f"{' né ' if lo<1 and hi>1 else ''}"
                     f"{'aumentato fino a RR '+format(hi,'.2f') if hi>1 else ''}: "
                     f"questo è il perimetro del silenzio, da scrivere nel MUTE.")
    else:
        righe.append("→ differenza statisticamente significativa: non è uno studio muto "
                     "(almeno su questo endpoint).")
    return "\n".join(righe)


def collaudo():
    # Caso reale del briefing del 12 agosto (scheda 9): 13,0% vs 4,8%, dichiarato muto.
    rr, lo, hi = katz_rr(6, 46, 3, 63)
    assert lo < 1 < hi, "il caso noto come muto deve avere IC che attraversa 1"
    assert hi > 5, f"con questi numeri il RR non escludibile supera 5 (trovato {hi:.2f})"
    # Caso chiaramente significativo: 30/100 vs 10/100.
    rr2, lo2, hi2 = katz_rr(30, 100, 10, 100)
    assert lo2 > 1, "un effetto netto deve avere il limite inferiore sopra 1"
    # Zero eventi: la continuità non deve dividere per zero.
    katz_rr(0, 75, 4, 75)
    print("✅ collaudo superato: muto riconosciuto muto, significativo riconosciuto tale, zero eventi gestito")
    return 0


if __name__ == '__main__':
    a = sys.argv[1:]
    if a == ['--collaudo']:
        sys.exit(collaudo())
    if len(a) != 4:
        print(__doc__); sys.exit(2)
    e1, n1, e2, n2 = (int(x) for x in a)
    if not (0 <= e1 <= n1 and 0 <= e2 <= n2 and n1 > 0 and n2 > 0):
        print("❌ eventi e numerosità incoerenti"); sys.exit(2)
    print(riassunto(e1, n1, e2, n2))
