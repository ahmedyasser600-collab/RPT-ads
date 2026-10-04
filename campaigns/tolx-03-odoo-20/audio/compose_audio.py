"""Score, SFX and voiceover placement for TOLX video 03 (frame-locked to ../timeline.py).

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


# the "problem" colour only covers the pain recap; the hook already lifts
music = A.build_music(DUR, s(TL.AGENT), s(TL.AGENT + 30), s(TL.END_CARD))

sfx = np.zeros(int(A.SR * DUR))
A.add(sfx, A.swish(0.8, 0.05, 300, 6000), s(4) - 0.5)               # title in
A.add(sfx, A.kick(0.4), s(10))
A.add(sfx, A.bell(A.hz("C6"), 0.05, 1.6), s(12))
A.add(sfx, A.pop(0.08, 900), s(31))                                   # release chip
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

LINES = [  # (text = generation prompt, window start s, window end s). Takes: vo_lines/m<n>.mp3 (Marcus).
    ("Odoo 20 just landed. Here's why it's time to move.", 0.3, s(TL.PAIN)),
    ("Still running on chats and spreadsheets?", s(TL.PAIN) + 0.1, s(TL.AGENT)),
    ("Tell the AI agent what you need, in plain words. It shows you the plan before it runs.",
     s(TL.AGENT) + 0.15, s(TL.ACCOUNT)),
    ("Ask your accounting assistant what you're owed. The answer comes from your own reports.",
     s(TL.ACCOUNT) + 0.1, s(TL.OFFLINE)),
    ("Internet down at the kiosk? Your point of sale keeps selling offline.", s(TL.OFFLINE) + 0.1, s(TL.ONE)),
    ("One system for your whole business, with AI built in.", s(TL.ONE) + 0.1, s(TL.OFFER)),
    ("Move to Odoo 20 with us. Book your discovery call today.", s(TL.OFFER) + 0.1, DUR - 0.8),
]
A.place_vo(LINES, os.path.join(HERE, "vo_lines"), "m", os.path.join(HERE, "vo_marcus.wav"), DUR)
