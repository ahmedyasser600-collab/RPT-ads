"""Score, SFX and voiceover placement for TOLX video 04 (frame-locked to ../timeline.py).

Series style (from video 03): 124 BPM groove from frame 0, slam hits on the title, Gia energetic read.
Writes music.wav, sfx.wav, vo_gia.wav (+ .srt) next to this script.
Usage: python compose_audio.py
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tolx-kit"))
import timeline as TL  # noqa: E402
import tolx_audio as A  # noqa: E402

DUR = TL.TOTAL / TL.FPS


def s(f):
    return f / TL.FPS


music = A.build_music(DUR, 0.0, 0.3, s(TL.END_CARD), bpm=124)

sfx = np.zeros(int(A.SR * DUR))
for f, v in zip(TL.SLAMS, (0.4, 0.45, 0.7, 0.35)):
    A.add(sfx, A.swish(0.35, 0.05 * v / 0.45, 300, 7000), s(f) - 0.3)
    A.add(sfx, A.kick(v), s(f + 5))
    A.add(sfx, A.sub(A.hz("C2"), 0.5, 0.25 * v), s(f + 5))
A.add(sfx, A.bell(A.hz("C6"), 0.06, 1.6), s(TL.SLAMS[2] + 5))
for f in TL.MILESTONES_IN:
    A.add(sfx, A.pop(0.07, 900), s(f + 1))
for f in (TL.HL_JULY, TL.HL_MARCH):
    A.add(sfx, A.alert(0.05), s(f))
A.add(sfx, A.pop(0.08, 760), s(TL.PDF_IN + 1))
A.add(sfx, A.swish(0.3, 0.05, 1500, 7000, rise=False), s(TL.PDF_X))
A.add(sfx, A.swish(0.5, 0.04, 500, 5000, rise=False), s(TL.MORPH))
for f in TL.DATA_ROWS:
    A.add(sfx, A.tick(0.05), s(f))
A.add(sfx, A.pop(0.08, 1000), s(TL.ASP_IN + 2))
A.add(sfx, A.pop(0.07, 1200), s(TL.SPLIT_IN + 2))
A.add(sfx, A.bell(A.hz("E6"), 0.04, 1.0), s(TL.PACKET + 24))
for f in TL.DOCS_IN:
    A.add(sfx, A.pop(0.08, 700), s(f + 1))
A.add(sfx, A.kick(0.55), s(TL.STAMP + 5))
A.add(sfx, A.alert(0.06), s(TL.STAMP + 5))
for f in TL.CHECKS:
    A.add(sfx, A.bell(A.hz("G5"), 0.05, 0.9), s(f + 1))
for f in TL.OFFER_BEATS[:2]:
    A.add(sfx, A.pop(0.07, 880), s(f + 2))
A.add(sfx, A.swish(0.9, 0.04, 300, 5000), s(TL.END_CARD) - 0.8)
A.add(sfx, A.pop(0.07, 760), s(TL.END_CARD + 51))

A.write_stereo(os.path.join(HERE, "music.wav"), music, 0.55, DUR)
A.write_stereo(os.path.join(HERE, "sfx.wav"), sfx, 0.45, DUR)
print("wrote music.wav and sfx.wav")

LINES = [  # (text = generation prompt, window start s, window end s). Takes: vo_lines/g<n>.mp3 (Gia).
    ("UAE e-invoicing is coming! Is your business ready?", 0.45, s(TL.DEADLINES)),
    ("Selling to other businesses? Your deadline is July 2027!", s(TL.DEADLINES) + 0.1, s(TL.HL_MARCH) - 0.1),
    ("And you must appoint an accredited provider by the end of March!", s(TL.HL_MARCH), s(TL.FORMAT)),
    ("No more PDF invoices. Every invoice goes out as structured data, through your provider.",
     s(TL.FORMAT) + 0.1, s(TL.EXCEL)),
    ("Still invoicing from Excel or Word? That won't cut it!", s(TL.EXCEL) + 0.1, s(TL.READY)),
    ("Get your sales, VAT and invoices into one system now, and be ready early!", s(TL.READY) + 0.1, s(TL.OFFER)),
    ("With Odoo, or software built around your business. Book your discovery call today!", s(TL.OFFER) + 0.1,
     DUR - 0.8),
]
A.place_vo(LINES, os.path.join(HERE, "vo_lines"), "g", os.path.join(HERE, "vo_gia.wav"), DUR,
           base_tempo=1.06, fx=A.ENERGY_FX)
