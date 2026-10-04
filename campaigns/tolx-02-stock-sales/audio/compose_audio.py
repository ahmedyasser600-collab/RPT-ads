"""Score, SFX and voiceover placement for TOLX video 02 (frame-locked to ../timeline.py).

Writes music.wav, sfx.wav, vo_marcus.wav (+ .srt) next to this script.
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


music = A.build_music(DUR, s(TL.TURN), s(TL.STEP_SELL), s(TL.END_CARD))

sfx = np.zeros(int(A.SR * DUR))
A.add(sfx, A.pop(0.10, 900), s(4))                                   # sheet appears
A.add(sfx, A.bell(A.hz("E6"), 0.04, 0.8), s(22))                    # "12" highlighted
A.add(sfx, A.kick(0.35), s(TL.SHELF + 6))                           # shelf lands
A.add(sfx, A.alert(0.05), s(TL.SHELF + 8))                          # mismatch
for f in TL.FILE_FRAMES:
    A.add(sfx, A.pop(0.09, 760 + 60 * A.rng.standard_normal()), s(f + 1))
for f in TL.QUESTION_FRAMES:
    A.add(sfx, A.pop(0.10, 520), s(f + 2))
A.add(sfx, A.swish(0.7, 0.05, 500, 4500, rise=False), s(TL.TURN + 4))  # files collapse
for f in (TL.STEP_SELL, TL.STEP_SYNC, TL.STEP_REORDER, TL.STEP_SEE):
    A.add(sfx, A.bell(A.hz("G5"), 0.045, 1.2), s(f + 2))
A.add(sfx, A.swish(0.4, 0.035, 800, 6000, rise=False), s(TL.SALE_IN))
A.add(sfx, A.bell(A.hz("C6"), 0.05, 0.9), s(TL.COUNT_DOWN))           # sale lands, 6 -> 4
for k in range(2):
    A.add(sfx, A.tick(0.05), s(TL.COUNT_DOWN + 4 + 3 * k))
for f in TL.SYNC_PULSES:
    A.add(sfx, A.pop(0.07, 1040), s(f + 16))
A.add(sfx, A.alert(0.07), s(TL.ALERT_IN + 2))
A.add(sfx, A.tick(0.08), s(TL.PO_CLICK))
A.add(sfx, A.pop(0.09, 880), s(TL.PO_CLICK + 2))
for f in TL.TILES:
    A.add(sfx, A.pop(0.07, 940), s(f + 2))
for f in TL.STATEMENT_BEATS[:2]:
    A.add(sfx, A.pop(0.07, 880), s(f + 2))
A.add(sfx, A.swish(0.9, 0.04, 300, 5000), s(TL.END_CARD) - 0.8)

A.write_stereo(os.path.join(HERE, "music.wav"), music, 0.55, DUR)
A.write_stereo(os.path.join(HERE, "sfx.wav"), sfx, 0.45, DUR)
print("wrote music.wav and sfx.wav")

# (text = generation prompt, window start s, window end s). Takes: vo_lines/m<n>.mp3 (Marcus).
LINES = [
    ("Your spreadsheet says twelve in stock.", 0.3, s(TL.SHELF) + 0.0),
    ("The shelf says three.", s(TL.SHELF) + 0.1, s(TL.FILES)),
    ("Which file is right?", s(TL.FILES) + 0.1, s(TL.QUESTIONS)),
    ("Who sold what? When do we reorder?", s(TL.QUESTIONS) + 0.15, s(TL.TURN)),
    ("Move to one system, with one number.", s(TL.TURN) + 0.15, s(TL.STEP_SELL)),
    ("Make a sale, and stock updates once.", s(TL.STEP_SELL) + 0.15, s(TL.STEP_SYNC)),
    ("The shop, the warehouse and your phone all see the same number.", s(TL.STEP_SYNC) + 0.1, s(TL.STEP_REORDER)),
    ("Running low? It tells you before you run out.", s(TL.STEP_REORDER) + 0.1, s(TL.STEP_SEE)),
    ("And you see the whole day at a glance.", s(TL.STEP_SEE) + 0.1, s(TL.STATEMENT)),
    ("Move beyond Excel, with Odoo, or software built around your business.", s(TL.STATEMENT) + 0.15,
     s(TL.END_CARD) + 0.2),
    ("Book your discovery call today.", s(TL.END_CARD) + 1.0, DUR - 0.6),
]
A.place_vo(LINES, os.path.join(HERE, "vo_lines"), "m", os.path.join(HERE, "vo_marcus.wav"), DUR)
