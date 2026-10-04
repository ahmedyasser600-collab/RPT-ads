"""Original music bed + UI sound effects for the TOLX "WhatsApp orders" video.

Composed in code (no samples, loops or recordings), so no third-party licence applies.
Event times come from ../timeline.py, so every chat pop, step tick and board move is
frame-locked to the picture.

  0-9 s    problem: A minor pad, muted ticking pulse, a soft pop per chat message
           (the burying cascade gets quieter and denser)
  9 s      turn: swell + swish, the harmony lifts to C major
  11.5-26  workflow: C - G - Am - F, plucked eighths, soft kick; a chime on each step
  26-30 s  end card: C major chord rings out

Writes music.wav and sfx.wav (48 kHz stereo).
Usage: python compose_audio.py [out_dir]
"""
import os
import sys

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import timeline as TL  # noqa: E402

SR = 48000
DUR = TL.TOTAL / TL.FPS
N = int(SR * DUR)
T = np.arange(N) / SR
BPM = 112
BEAT = 60 / BPM
BAR = 4 * BEAT
rng = np.random.default_rng(42)
NOTE = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}


def sec(frame):
    return frame / TL.FPS


def hz(n):
    return 440.0 * 2 ** ((NOTE[n[:-1]] + 12 * (int(n[-1]) + 1) - 69) / 12)


def lp(x, f):
    return sosfilt(butter(2, f, "low", fs=SR, output="sos"), x)


def hp(x, f):
    return sosfilt(butter(2, f, "high", fs=SR, output="sos"), x)


def bp(x, lo, hi):
    return sosfilt(butter(2, [lo, hi], "band", fs=SR, output="sos"), x)


def add(buf, sig, start):
    i = int(round(start * SR))
    j = min(len(buf), i + len(sig))
    if 0 <= i < j:
        buf[i:j] += sig[: j - i]


def tt(dur):
    return np.arange(int(SR * dur)) / SR


def pad(freqs, dur, level, bright=1800):
    t = tt(dur)
    s = sum(np.sin(2 * np.pi * (f + d) * t + rng.uniform(0, 6.28)) +
            0.3 * np.sin(4 * np.pi * (f + d) * t) for f in freqs for d in (-0.5, 0, 0.5))
    s = lp(s, bright)
    return level * s / (3 * len(freqs)) * np.minimum(1, t / 0.6) * np.minimum(1, (dur - t) / 0.6)


def pluck(freq, vel, decay=8):
    t = tt(0.6)
    s = np.sin(2 * np.pi * freq * t) + 0.4 * np.sin(4 * np.pi * freq * t) + 0.15 * np.sin(6 * np.pi * freq * t)
    return vel * lp(s, 4200) * np.exp(-t * decay) * np.minimum(1, t / 0.002)


def bell(freq, vel, dur=1.6):
    t = tt(dur)
    s = sum(a * np.sin(2 * np.pi * freq * r * t) * np.exp(-t * d)
            for r, a, d in ((1, 1, 2.5), (2.76, 0.35, 5), (5.4, 0.15, 8), (2.0, 0.25, 3)))
    return vel * s * np.minimum(1, t / 0.003)


def kick(vel):
    t = tt(0.32)
    f = 48 + 80 * np.exp(-t * 32)
    return vel * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 10)


def tick(vel):
    t = tt(0.05)
    return vel * hp(rng.standard_normal(len(t)), 5000) * np.exp(-t * 90)


def sub(freq, dur, vel):
    t = tt(dur)
    return vel * np.sin(2 * np.pi * freq * t) * np.minimum(1, t / 0.04) * np.minimum(1, (dur - t) / 0.2)


def pop(vel, pitch):
    """Short rounded 'message' blip: a fast downward sine chirp."""
    t = tt(0.09)
    f = pitch * (1 + 0.6 * np.exp(-t * 60))
    return vel * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 45) * np.minimum(1, t / 0.002)


def swish(dur, level, lo=400, hi=5000, rise=True):
    t = tt(dur)
    env = (t / dur) ** 2 if rise else np.sin(np.pi * t / dur) ** 2
    return level * bp(rng.standard_normal(len(t)), lo, hi) * env


# ---------------------------------------------------------------- music
music = np.zeros(N)
t_turn, t_work, t_end = sec(TL.TURN), sec(TL.STEP_LOG), sec(TL.END_CARD)

# problem section: Am(add9) - Fmaj7 pads, a ticking clock-like pulse, low sub
prob = [("A2", ["A3", "C4", "E4", "B4"]), ("F2", ["F3", "A3", "C4", "E4"])]
t = 0.0
k = 0
while t < t_turn:
    bass, voicing = prob[k % 2]
    add(music, pad([hz(n) for n in voicing], BAR + 0.6, 0.11, 1400), max(0, t - 0.1))
    add(music, sub(hz(bass), BAR, 0.16), t)
    t += BAR
    k += 1
for b in range(int(t_turn / (BEAT / 2))):
    tb = b * BEAT / 2
    add(music, tick(0.05 if b % 2 == 0 else 0.025), tb)
    if b % 4 == 2:
        add(music, pluck(hz("E5"), 0.035, 12), tb)

# turn: rising swell into the lift
add(music, swish(1.6, 0.06, 300, 6000), t_turn - 1.3)

# workflow section: C - G - Am - F
work = [("C2", ["C4", "E4", "G4", "D5"]), ("G1", ["B3", "D4", "G4", "D5"]),
        ("A1", ["A3", "C4", "E4", "B4"]), ("F1", ["A3", "C4", "F4", "E5"])]
arp = [0, 2, 1, 3, 2, 1, 3, 2]
t = t_turn
k = 0
while t < t_end:
    bass, voicing = work[k % 4]
    level = 0.09 if t < t_work else 0.12
    add(music, pad([hz(n) for n in voicing], BAR + 0.6, level, 2400), max(0, t - 0.1))
    add(music, sub(hz(bass) * 2, BAR - 0.05, 0.20), t)
    for s in range(8):
        ts = t + s * BEAT / 2
        if ts >= t_end:
            break
        if ts >= t_work - 1e-6:
            add(music, pluck(hz(voicing[arp[s]]) * 2, 0.07), ts)
            if s % 4 == 0:
                add(music, kick(0.30), ts)
            if s % 2 == 1:
                add(music, tick(0.035), ts)
        elif s % 2 == 0:
            add(music, pluck(hz(voicing[arp[s]]) * 2, 0.045), ts)
    t += BAR
    k += 1
# end card: C major rings out
for i, n in enumerate(["C3", "G3", "C4", "E4", "G4", "D5"]):
    add(music, bell(hz(n), 0.05, 3.5), t_end + 0.04 * i)
add(music, pad([hz(n) for n in ["C4", "E4", "G4", "B4"]], DUR - t_end + 0.2, 0.11, 2200), t_end - 0.2)
add(music, sub(hz("C2"), DUR - t_end, 0.18), t_end)
music = hp(music, 28)

# ---------------------------------------------------------------- sfx
sfx = np.zeros(N)
for i, (f, sender, _) in enumerate(TL.CHAT):
    burying = f >= TL.BURY
    vel = 0.10 if not burying else 0.05 * (1 - 0.5 * (f - TL.BURY) / 80)
    pitch = (1100 if sender == "You" else 820) * (1 + 0.04 * rng.standard_normal())
    if i == TL.KEY_INDEX:
        vel, pitch = 0.16, 1250
    add(sfx, pop(vel, pitch), sec(f + 1))
add(sfx, bell(hz("E6"), 0.05, 1.0), sec(TL.KEY_IN + 5))            # highlight on the order
for f in TL.QUESTION_FRAMES:
    add(sfx, pop(0.10, 520), sec(f + 2))
add(sfx, swish(0.7, 0.05, 500, 4500, rise=False), sec(TL.TURN + 30) - 0.2)  # lift out
for f in (TL.STEP_LOG, TL.STEP_ASSIGN, TL.STEP_TRACK, TL.STEP_FOLLOW):
    add(sfx, bell(hz("G5"), 0.045, 1.2), sec(f + 2))
for k in range(16):                                                  # soft keystrokes while the card fills
    add(sfx, tick(0.02), sec(TL.STEP_LOG + 12 + k * 4))
add(sfx, pop(0.09, 700), sec(TL.STEP_ASSIGN + 10))                   # owner avatar
for f in (TL.MOVE_CONFIRMED, TL.MOVE_DELIVERED):
    add(sfx, swish(0.45, 0.035, 800, 6000, rise=False), sec(f))
    add(sfx, pop(0.07, 960), sec(f + 15))
add(sfx, bell(hz("C6"), 0.06, 1.4), sec(TL.FOLLOW_CHIP + 2))
add(sfx, bell(hz("E6"), 0.04, 1.2), sec(TL.FOLLOW_CHIP + 6))
for f in TL.STATEMENT_PILLS:
    add(sfx, pop(0.07, 880), sec(f + 2))
add(sfx, swish(0.9, 0.04, 300, 5000), sec(TL.END_CARD) - 0.8)


def finish(sig, peak, width_ms=(9, 15)):
    left = sig + 0.15 * np.roll(lp(sig, 4000), int(SR * width_ms[0] / 1000))
    right = sig + 0.15 * np.roll(lp(sig, 4000), int(SR * width_ms[1] / 1000))
    st = np.stack([left, right], axis=1)
    st *= (np.minimum(1, T / 0.03) * np.clip((DUR - T) / 1.5, 0, 1))[:, None]
    return st * (peak / np.max(np.abs(st)))


out = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
os.makedirs(out, exist_ok=True)
wavfile.write(os.path.join(out, "music.wav"), SR, (finish(music, 0.55) * 32767).astype(np.int16))
wavfile.write(os.path.join(out, "sfx.wav"), SR, (finish(sfx, 0.45) * 32767).astype(np.int16))
print("wrote music.wav and sfx.wav")
