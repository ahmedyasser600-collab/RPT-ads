"""Audio for TOLX video 02 v2: smooth bed, Gia (energetic), a few soft accents per shot."""
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


st = [sh["start"] for sh in TL.SHOTS]
music = A.build_music_smooth(DUR, s(TL.END_CARD))
sfx = np.zeros(int(A.SR * DUR))
for f in st[1:] + [TL.END_CARD]:
    A.add(sfx, A.swish(0.8, 0.025, 300, 3800), s(f) - 0.5)              # soft whoosh into every cut
A.add(sfx, A.swish(0.7, 0.018, 400, 3500, rise=False), s(st[0] + 10))  # scribble
A.add(sfx, A.chime(0.03), s(st[0] + 16) + 0.15)                         # sheet tile
A.add(sfx, A.soft_keys(A.hz("E6"), 0.03, 0.9), s(st[1] + 6))            # sparks
A.add(sfx, A.chime(0.03), s(st[1] + 12) + 0.15)
for k in range(5):                                                      # file tiles
    A.add(sfx, A.soft_keys(A.hz(["C5", "D5", "E5", "G5", "A5"][k]), 0.022, 0.6), s(st[2] + 8 + 7 * k) + 0.1)
A.add(sfx, A.chime(0.03), s(st[3] + 8) + 0.15)                          # sale
A.add(sfx, A.soft_keys(A.hz("G5"), 0.03, 0.9), s(st[3] + 58))           # 6 -> 4
for k in range(3):
    A.add(sfx, A.soft_keys(A.hz(["E5", "G5", "C6"][k]), 0.025, 0.7), s(st[4] + 10 + 10 * k) + 0.1)
A.add(sfx, A.chime(0.035), s(st[5] + 22) + 0.1)                         # alert
A.add(sfx, A.chime(0.035), s(st[6] + 58))                               # tiles meet
A.write_stereo(os.path.join(HERE, "music.wav"), music, 0.55, DUR)
A.write_stereo(os.path.join(HERE, "sfx.wav"), sfx, 0.45, DUR)
print("wrote music.wav and sfx.wav")

LINES = [  # (Gia prompt, window start s, window end s); takes vo_lines/g<n>.mp3
    ("Your spreadsheet says twelve in stock...", s(st[0]) + 0.35, s(st[1])),
    ("But the shelf? Only three!", s(st[1]) + 0.25, s(st[2])),
    ("Five files, five numbers. Which one is right?", s(st[2]) + 0.25, s(st[3])),
    ("With one system, every sale updates your stock.", s(st[3]) + 0.25, s(st[4])),
    ("Shop, warehouse, your phone. Same number, everywhere!", s(st[4]) + 0.25, s(st[5])),
    ("Running low? You're alerted before you run out.", s(st[5]) + 0.25, s(st[6])),
    ("Odoo, or software built around your business.", s(st[6]) + 0.25, s(TL.END_CARD)),
    ("Book your discovery call with Tolex today!", s(TL.END_CARD) + 0.9, DUR - 0.5),
]
A.place_vo(LINES, os.path.join(HERE, "vo_lines"), "g", os.path.join(HERE, "vo_gia.wav"), DUR,
           base_tempo=1.06, fx=A.ENERGY_FX)
