# -*- coding: utf-8 -*-
"""
PULSE — collaudo del feed podcast (audio/feed.py). Macchina pura, episodi sintetici.
Le regole di verità valgono anche qui: durata dichiarata vera, niente episodi con
date malformate, voce dichiaratamente sintetica nella descrizione del canale.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'audio'))
from feed import feedXML, durata_hms

ok = 0; bad = 0
def chk(c, m):
    global ok, bad
    print(('✅ ' if c else '❌ ') + m)
    if c: ok += 1
    else: bad += 1

EP = [{'data': '2026-08-20', 'titolo': '20 agosto — Due richiami, e una coppia sullo slope',
       'descrizione': 'Testo del briefing.', 'file': '2026-08-20.mp3', 'bytes': 1234567, 'secondi': 154},
      {'data': '2026-08-19', 'titolo': '19 agosto — prova',
       'descrizione': 'x', 'file': '2026-08-19.mp3', 'bytes': 99, 'secondi': 3661}]
x = feedXML(EP, base='https://esempio.test/pulse')

chk('<rss' in x and '</rss>' in x and 'itunes' in x, 'il feed è un RSS podcast ben formato')
chk('Due richiami' in x, 'il titolo porta data e verdetto in una riga')
chk('url="https://esempio.test/pulse/audio/2026-08-20.mp3"' in x, "l'enclosure punta all'MP3 giusto")
chk('length="1234567"' in x, 'il peso dichiarato è quello vero')
chk('<itunes:duration>00:02:34</itunes:duration>' in x, 'la durata dichiarata è quella vera (2:34)')
chk('<itunes:duration>01:01:01</itunes:duration>' in x, 'la durata regge anche sopra l\'ora')
chk(x.index('2026-08-20.mp3') < x.index('2026-08-19.mp3'), 'gli episodi sono in ordine: il più recente primo')
chk('<itunes:block>Yes</itunes:block>' in x, 'il feed chiede di NON essere indicizzato nelle directory')
chk('sintetica' in x, 'la voce si dichiara sintetica nel canale')
chk(durata_hms(0) == '00:00:00' and durata_hms(59) == '00:00:59', 'la durata non inventa mai secondi')

# una data malformata deve FERMARE la generazione, non produrre un feed sbagliato
try:
    feedXML([{'data': 'ieri', 'titolo': 't', 'file': 'x.mp3', 'bytes': 1, 'secondi': 1}])
    chk(False, 'una data malformata ferma la generazione')
except SystemExit:
    chk(True, 'una data malformata ferma la generazione')

print(f"\n===== PODCAST: {ok} verificati · {bad} errori =====")
sys.exit(1 if bad else 0)
