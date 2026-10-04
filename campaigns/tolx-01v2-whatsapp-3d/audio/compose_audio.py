"""Audio for TOLX video 01 v2: smooth bed, Gia (energetic), a few soft accents per shot."""
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
for k in range(6):                                                      # bubbles bursting in
    A.add(sfx, A.soft_keys(A.hz(["E5", "G5", "A5", "C6", "D6", "E6"][k]), 0.02, 0.5), s(st[0] + 4 + 5 * k) + 0.1)
A.add(sfx, A.chime(0.035), s(st[0] + 36) + 0.15)                        # 99+
for f in (6, 26, 42, 58, 74):                                           # bubbles arriving, order pushed down
    A.add(sfx, A.soft_keys(A.hz("G5"), 0.02, 0.5), s(st[1] + f) + 0.1)
A.add(sfx, A.chime(0.03), s(st[2] + 14) + 0.1)                          # who's on it
for k in range(3):                                                      # status steps
    A.add(sfx, A.soft_keys(A.hz(["C5", "E5", "G5"][k]), 0.03, 0.8), s(st[3] + 10 + 16 * k) + 0.1)
A.add(sfx, A.chime(0.035), s(st[3] + 60) + 0.1)                         # owner
A.add(sfx, A.chime(0.035), s(st[4] + 8) + 0.15)                         # reminder
A.add(sfx, A.chime(0.035), s(st[5] + 18))                               # Odoo
A.write_stereo(os.path.join(HERE, "music.wav"), music, 0.55, DUR)
A.write_stereo(os.path.join(HERE, "sfx.wav"), sfx, 0.45, DUR)
print("wrote music.wav and sfx.wav")

LINES = [  # (Gia prompt, window start s, window end s); takes vo_lines/g<n>.mp3 (g5, g6 reused from video 02 v2)
    ("Taking orders on WhatsApp?", s(st[0]) + 0.4, s(st[1])),
    ("Then somewhere in that chat, an order is getting buried.", s(st[1]) + 0.25, s(st[2])),
    ("Who's handling it? Did anyone follow up?", s(st[2]) + 0.25, s(st[3])),
    ("In one system, every order gets an owner and a status.", s(st[3]) + 0.25, s(st[4])),
    ("And every follow-up comes with a reminder.", s(st[4]) + 0.25, s(st[5])),
    ("It's time to shift to Oh-doo!", s(st[5]) + 0.25, s(TL.END_CARD)),
    ("Book your discovery call with Tolex today!", s(TL.END_CARD) + 0.9, DUR - 0.5),
]
A.place_vo(LINES, os.path.join(HERE, "vo_lines"), "g", os.path.join(HERE, "vo_gia.wav"), DUR,
           base_tempo=1.06, fx=A.ENERGY_FX)
