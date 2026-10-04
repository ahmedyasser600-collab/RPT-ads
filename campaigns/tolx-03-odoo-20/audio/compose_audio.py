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


# energetic from the first frame: full 124 BPM groove throughout, C major ring-out under the end card
music = A.build_music(DUR, 0.0, 0.3, s(TL.END_CARD), bpm=124)
SLAMS = [3, 13, 26]                         # compose_03.py SLAM_ODOO / SLAM_20 / SLAM_HERE

sfx = np.zeros(int(A.SR * DUR))
for f, v in zip(SLAMS, (0.45, 0.7, 0.4)):                            # title hits: whoosh in, then a hit
    A.add(sfx, A.swish(0.35, 0.05 * v / 0.45, 300, 7000), s(f) - 0.3)
    A.add(sfx, A.kick(v), s(f + 5))
    A.add(sfx, A.sub(A.hz("C2"), 0.5, 0.25 * v), s(f + 5))
A.add(sfx, A.bell(A.hz("C6"), 0.06, 1.6), s(SLAMS[1] + 5))
A.add(sfx, A.pop(0.08, 900), s(41))                                   # release chip
for f in (TL.PAIN + 6, TL.PAIN + 16):
    A.add(sfx, A.pop(0.09, 640), s(f + 1))
A.add(sfx, A.swish(0.35, 0.05, 1500, 7000, rise=False), s(TL.AGENT - 26))  # strike-through
for f in (TL.AGENT, TL.ACCOUNT, TL.OFFLINE):
    A.add(sfx, A.bell(A.hz("G5"), 0.045, 1.2), s(f + 2))
for k in range(int(len("Alert me when phone cases drop below 5.") / 1.3 / 3)):
    A.add(sfx, A.tick(0.018), s(TL.PROMPT_TYPE + 3 * k))
A.add(sfx, A.pop(0.08, 1100), s(TL.PLAN_IN + 1))
for f in TL.PLAN_STEPS:
    A.add(sfx, A.pop(0.06, 980), s(f + 1))
A.add(sfx, A.tick(0.08), s(TL.APPROVE))
A.add(sfx, A.bell(A.hz("E6"), 0.05, 1.2), s(TL.APPROVE + 3))
for k in range(int(len("How much do customers owe me?") / 1.3 / 3)):
    A.add(sfx, A.tick(0.018), s(TL.Q_TYPE + 3 * k))
A.add(sfx, A.pop(0.08, 1100), s(TL.ANSWER_IN + 1))
for f in TL.ANSWER_ROWS:
    A.add(sfx, A.pop(0.06, 940), s(f + 1))
A.add(sfx, A.alert(0.05), s(TL.GO_OFFLINE))
for f in TL.POS_ORDERS:
    A.add(sfx, A.bell(A.hz("A5"), 0.035, 0.6), s(f + 1))              # till "ding" while offline
A.add(sfx, A.bell(A.hz("C6"), 0.05, 1.0), s(TL.BACK_ONLINE))
A.add(sfx, A.bell(A.hz("G6"), 0.04, 1.0), s(TL.BACK_ONLINE + 4))
for f in TL.TILES_IN:
    A.add(sfx, A.swish(0.4, 0.03, 800, 6000, rise=False), s(f))
A.add(sfx, A.kick(0.3), s(TL.MERGE + 16))
A.add(sfx, A.bell(A.hz("E6"), 0.05, 1.4), s(TL.MERGE + 18))
for f in TL.OFFER_BEATS[:2]:
    A.add(sfx, A.pop(0.07, 880), s(f + 2))
A.add(sfx, A.swish(0.9, 0.04, 300, 5000), s(TL.END_CARD) - 0.8)
A.add(sfx, A.pop(0.07, 760), s(TL.END_CARD + 51))                     # partner badge

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
    ("Ready to move to Odoo 20? Book your discovery call today!", s(TL.OFFER) + 0.1, DUR - 0.8),
]
A.place_vo(LINES, os.path.join(HERE, "vo_lines"), "g", os.path.join(HERE, "vo_gia.wav"), DUR,
           base_tempo=1.06, fx=A.ENERGY_FX)
