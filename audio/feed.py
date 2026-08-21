#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PULSE — il feed podcast privato (Addendum §11).

Un episodio per briefing: titolo = data + verdetto in una riga, note = testo del
briefing con i collegamenti, durata dichiarata vera. Nessun jingle, nessuna
musica, copertina statica sobria. L'infrastruttura d'ascolto è quella delle app
podcast: qui si genera solo l'XML.

feedXML(episodi, base) è PURA (dati → xml) così i collaudi la verificano con
episodi sintetici. Il deposito reale è audio/episodi.json, scritto dal workflow
del mattino insieme all'MP3.

Limite dichiarato, non nascosto: il repository è pubblico, quindi l'URL del feed
è offuscato (nome non indovinabile) ma non segreto in senso forte. Il feed porta
solo ciò che è già pubblico nell'app; nessun dato di paziente, mai.
"""
import json, os, re, sys
from datetime import datetime, timezone
from xml.sax.saxutils import escape

QUI = os.path.dirname(os.path.abspath(__file__))
BASE = 'https://dariogiunchi-cmd.github.io/pulse-knee'
DEPOSITO = os.path.join(QUI, 'episodi.json')
# Il nome del file di uscita è la parte «non indovinabile» dell'URL.
USCITA = os.path.join(QUI, 'pulse-x7k2m9qw4r.xml')


def rfc2822(iso):
    d = datetime.strptime(iso, '%Y-%m-%d').replace(hour=5, minute=30, tzinfo=timezone.utc)
    return d.strftime('%a, %d %b %Y %H:%M:%S %z')


def durata_hms(sec):
    sec = int(sec)
    return f"{sec//3600:02d}:{sec%3600//60:02d}:{sec%60:02d}"


def feedXML(episodi, base=BASE):
    """episodi: [{data:'YYYY-MM-DD', titolo, descrizione, file, bytes, secondi}] — i più recenti primi."""
    voci = []
    for e in sorted(episodi, key=lambda x: x['data'], reverse=True):
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', e.get('data', '')):
            raise SystemExit(f"❌ episodio con data non valida: {e.get('data')}")
        url = f"{base}/audio/{e['file']}"
        voci.append(
            '<item>'
            f"<title>{escape(e['titolo'])}</title>"
            f"<description>{escape(e.get('descrizione',''))}</description>"
            f"<pubDate>{rfc2822(e['data'])}</pubDate>"
            f"<guid isPermaLink=\"false\">pulse-{e['data']}</guid>"
            f"<enclosure url=\"{escape(url)}\" length=\"{int(e['bytes'])}\" type=\"audio/mpeg\"/>"
            f"<itunes:duration>{durata_hms(e['secondi'])}</itunes:duration>"
            '</item>')
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">\n'
            '<channel>'
            '<title>PULSE · knee</title>'
            f'<link>{base}/</link>'
            '<language>it</language>'
            '<description>Il briefing quotidiano sulla letteratura del ginocchio del Dr. Dario Giunchi. '
            'Voce sintetica dichiarata; ogni affermazione è tracciabile a una fonte verificata.</description>'
            '<itunes:block>Yes</itunes:block>'
            f'<itunes:image href="{base}/audio/copertina.png"/>'
            + ''.join(voci) +
            '</channel>\n</rss>\n')


if __name__ == '__main__':
    eps = json.load(open(DEPOSITO, encoding='utf-8')) if os.path.exists(DEPOSITO) else []
    open(USCITA, 'w', encoding='utf-8').write(feedXML(eps))
    print(f"📻 feed: {len(eps)} episodi → {os.path.basename(USCITA)}")
