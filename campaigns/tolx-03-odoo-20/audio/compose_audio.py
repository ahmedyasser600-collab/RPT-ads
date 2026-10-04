"""Score, SFX and voiceover placement for TOLX video 03 (frame-locked to ../timeline.py).

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
REVEALS = [2, 14, 28]                       # compose_03.py SLAM_ODOO / SLAM_20 / SLAM_HERE (smooth reveals)

# few, soft accents (no pops / ticks / hits)
sfx = np.zeros(int(A.SR * DUR))
A.add(sfx, A.swish(1.2, 0.025, 300, 3000), s(REVEALS[1]) - 0.6)
A.add(sfx, A.chime(0.04), s(REVEALS[1] + 6))
for f in (TL.PAIN, TL.AGENT, TL.ACCOUNT, TL.OFFLINE, TL.ONE):
    A.add(sfx, A.swish(0.8, 0.02, 300, 3000, rise=False), s(f) - 0.2)
A.add(sfx, A.chime(0.03), s(TL.APPROVE + 3))
A.add(sfx, A.chime(0.03), s(TL.ANSWER_IN + 2))
A.add(sfx, A.soft_kick(0.25), s(TL.GO_OFFLINE))
A.add(sfx, A.chime(0.035), s(TL.BACK_ONLINE))
A.add(sfx, A.chime(0.03), s(TL.MERGE + 18))
A.add(sfx, A.swish(1.2, 0.025, 300, 3500), s(TL.END_CARD) - 0.9)

A.write_stereo(os.path.join(HERE, "music.wav"), music, 0.55, DUR)
A.write_stereo(os.path.join(HERE, "sfx.wav"), sfx, 0.45, DUR)
print("wrote music.wav and sfx.wav")

LINES = [  # (text = generation prompt, window start s, window end s). Takes: vo_lines/g<n>.mp3 (Gia, energetic read).
    ("Odoo 20 is HERE! And it's time to make the move!", 0.45, s(TL.PAIN)),
    ("Still stuck on chats and spreadsheets?!", s(TL.PAIN) + 0.1, s(TL.AGENT)),
    ("Meet your AI agent! Just tell it what you need, and it shows you the plan before it runs.",
     s(TL.AGENT) + 0.15, s(TL.ACCOUNT)),
    ("Need numbers? Ask your accounting assistant what you're owed. Answers straight from your own reports!",
     s(TL.ACCOUNT) + 0.1, s(TL.OFFLINE)),
    ("Internet down at the kiosk? No problem! Your point of sale keeps selling.", s(TL.OFFLINE) + 0.1, s(TL.ONE)),
    ("One system for your whole business. With AI built in!", s(TL.ONE) + 0.1, s(TL.OFFER)),
    ("Ready to move to Odoo 20? Book your discovery call with Tolx today!", s(TL.OFFER) + 0.1, DUR - 0.8),
]
A.place_vo(LINES, os.path.join(HERE, "vo_lines"), "g", os.path.join(HERE, "vo_gia.wav"), DUR,
           base_tempo=1.06, fx=A.ENERGY_FX)
