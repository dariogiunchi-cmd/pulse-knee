# -*- coding: utf-8 -*-
"""
PULSE — fondamenta comuni alle suite.

REGOLA CHE HA COSTATO CARO, IL 2 AGOSTO 2026.
Le prime versioni delle suite davano per scontati i lavori di quel giorno:
«gli articoli 2, 1, 4 e 5», «esattamente 48 testi social», «quattro lavori con
le varianti». Il mattino dopo il briefing porta altri articoli, con altri
numeri e in altra quantità: tutte e otto le suite sarebbero fallite e il
cancello avrebbe **bloccato una pubblicazione perfettamente valida**, lasciando
online l'app del giorno prima senza che nessuno se ne accorgesse.

Un cancello che si chiude sul contenuto invece che sui difetti è peggio di
nessun cancello: è un fallimento silenzioso travestito da sicurezza.

Da qui la regola: **si collauda la macchina, non il carico del giorno.**
I numeri degli articoli si scoprono a runtime; le quantità si verificano come
coerenze interne («ogni lavoro che ha i contenuti social ne ha tre toni e tre
blocchi»), mai come conteggi assoluti.
"""
import os

H = os.environ.get('PULSE_HTML') or os.path.abspath('index.html')
U = 'file://' + H


def numeri(pg):
    """Tutti i numeri di scheda del giorno, nell'ordine in cui compaiono."""
    return pg.evaluate("() => ARTICLES.map(function(a){return a.n})")


def con_nlb(pg, quanti=4):
    """I primi <quanti> lavori del giorno che hanno i testi per la distribuzione."""
    return pg.evaluate(
        "q => ARTICLES.map(function(a){return a.n}).filter(function(n){return NLB[n]}).slice(0,q)",
        quanti)


def con_socv(pg):
    """I lavori del giorno che hanno i contenuti social."""
    return pg.evaluate(
        "() => ARTICLES.map(function(a){return a.n}).filter(function(n){return SOCV[n]})")


def salta(nome, motivo):
    """Un giorno può non avere materiale per una funzione: si dichiara, non si finge."""
    print(f"⏭️  {nome} — non collaudabile oggi ({motivo}). La macchina è comunque verificata.")
