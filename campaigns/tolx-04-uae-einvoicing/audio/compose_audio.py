"""Score, SFX and voiceover placement for TOLX video 04 (frame-locked to ../timeline.py).

Series style (v2): smooth premium bed (build_music_smooth), few soft accents, Gia energetic read, brand named in the CTA.
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


music = A.build_music_smooth(DUR, s(TL.END_CARD))

# few, soft accents (no pops / ticks / hits)
sfx = np.zeros(int(A.SR * DUR))
A.add(sfx, A.swish(1.2, 0.025, 300, 3000), s(TL.REVEALS[2]) - 0.6)
A.add(sfx, A.chime(0.04), s(TL.REVEALS[2] + 6))
for f in (TL.HL_JULY, TL.HL_MARCH):
    A.add(sfx, A.chime(0.03), s(f))
for f in (TL.FORMAT, TL.EXCEL, TL.READY):
    A.add(sfx, A.swish(0.8, 0.02, 300, 3000, rise=False), s(f) - 0.2)
A.add(sfx, A.chime(0.03), s(TL.ASP_IN + 4))
A.add(sfx, A.soft_kick(0.3), s(TL.STAMP + 4))
for f in TL.CHECKS:
    A.add(sfx, A.soft_keys(A.hz("G5"), 0.03, 0.9), s(f + 1))
A.add(sfx, A.swish(1.2, 0.025, 300, 3500), s(TL.END_CARD) - 0.9)

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
    ("With Odoo, or software built around your business. Book your discovery call with Tolx today!", s(TL.OFFER) + 0.1,
     DUR - 0.8),
]
A.place_vo(LINES, os.path.join(HERE, "vo_lines"), "g", os.path.join(HERE, "vo_gia.wav"), DUR,
           base_tempo=1.06, fx=A.ENERGY_FX)
