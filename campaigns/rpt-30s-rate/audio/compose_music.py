"""Original upbeat score for the 30s RPT reel, composed in code (no samples, no licence needed).

120 BPM (beat 0.5 s, bar 2 s), so the cuts at 4, 9, 16, 23 and 26 s sit on beats.
  0-4 s   S1  pad + pluck intro
  4-9 s   S2  kick and off-beat hats come in
  9-15 s  S3  full groove: kick, clap, hats, pumping bass, pluck
  15-16 s     one-bar breath with a riser into the financing message
  16-26 s S4/S5 full groove again
  26-30 s end card: soft landing on C, drums out, pad and pluck ring out

Writes music.wav (48 kHz stereo). The voiceover ducks it in compose_film.py.
Usage: python compose_music.py [out_dir]
"""
import os
import sys

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt

SR, DUR, BEAT = 48000, 30.0, 0.5
N = int(SR * DUR)
T = np.arange(N) / SR
rng = np.random.default_rng(7)

NOTE = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}


def hz(n):
    return 440.0 * 2 ** ((NOTE[n[0]] + 12 * (int(n[-1]) + 1) - 69) / 12)


CHORDS = {  # root (bass octave), triad (mid octave)
    "Am": ("A1", ["A3", "C4", "E4"]), "F": ("F1", ["F3", "A3", "C4"]),
    "C": ("C2", ["C4", "E4", "G4"]), "G": ("G1", ["G3", "B3", "D4"]),
}
BARS = ["Am", "F", "C", "G", "Am", "F", "C", "G", "F", "G", "Am", "F", "G", "C", "C"]   # 15 bars of 2 s


def chord_at(t):
    return CHORDS[BARS[min(int(t // 2), len(BARS) - 1)]]


def lp(x, f):
    return sosfilt(butter(2, f, "low", fs=SR, output="sos"), x)


def hp(x, f):
    return sosfilt(butter(2, f, "high", fs=SR, output="sos"), x)


def bp(x, lo, hi):
    return sosfilt(butter(2, [lo, hi], "band", fs=SR, output="sos"), x)


def saw(f, t):
    return 2 * ((f * t) % 1.0) - 1


def add(buf, sig, start):
    i = int(round(start * SR))
    j = min(len(buf), i + len(sig))
    if 0 <= i < j:
        buf[i:j] += sig[: j - i]


def env_t(dur):
    return np.arange(int(SR * dur)) / SR


# ---------------------------------------------------------------- instruments
def kick():
    t = env_t(0.35)
    f = 48 + 110 * np.exp(-t * 28)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t * 9) + 0.3 * rng.standard_normal(len(t)) * np.exp(-t * 400)


def clap():
    t = env_t(0.25)
    n = rng.standard_normal(len(t))
    e = sum(np.exp(-np.clip(t - d, 0, None) * 60) * (t >= d) for d in (0, 0.012, 0.024)) / 3
    return bp(n, 900, 3200) * e * 1.4


def hat(level=1.0):
    t = env_t(0.06)
    return hp(rng.standard_normal(len(t)), 7500) * np.exp(-t * 70) * level


def pluck(f, dur=0.3):
    t = env_t(dur)
    s = 0.6 * saw(f, t) + 0.4 * saw(f * 1.005, t)
    return lp(s, 2600) * np.exp(-t * 11) * np.minimum(1, t / 0.003)


def bass(f, dur=0.22):
    t = env_t(dur)
    s = np.sin(2 * np.pi * f * t) + 0.35 * lp(saw(f, t), 500)
    return s * np.minimum(1, t / 0.004) * np.minimum(1, (dur - t) / 0.03)


def pad_layer():
    out = np.zeros(N)
    for bar, name in enumerate(BARS):
        t0, dur = bar * 2.0, 2.0 + 0.4 + (2.0 if bar == len(BARS) - 1 else 0)
        t = env_t(dur)
        s = sum(saw(hz(n) * d, t) for n in CHORDS[name][1] for d in (0.996, 1.0, 1.004))
        s = lp(s, 1400) * np.minimum(1, t / 0.25) * np.minimum(1, (dur - t) / 0.4)
        add(out, s / 9, t0)
    return out


def riser(t0, dur):
    t = env_t(dur)
    n = rng.standard_normal(len(t))
    return bp(n, 800, 6000) * (t / dur) ** 2.2 * 0.5


# ---------------------------------------------------------------- arrangement
drums, basses, plucks = np.zeros(N), np.zeros(N), np.zeros(N)
BREATH = (15.0, 16.0)
kicks = [b * BEAT for b in range(int(4.0 / BEAT), int(26.0 / BEAT) + 1)
         if not BREATH[0] <= b * BEAT < BREATH[1]]
for k in kicks:
    add(drums, kick() * 0.9, k)
for b in range(int(9.0 / BEAT), int(26.0 / BEAT)):
    t = b * BEAT
    if BREATH[0] <= t < BREATH[1]:
        continue
    if b % 2 == 1:
        add(drums, clap() * 0.35, t)
for b in range(int(4.0 / BEAT), int(26.0 / BEAT)):
    t = b * BEAT
    if BREATH[0] <= t < BREATH[1]:
        continue
    add(drums, hat(0.22), t + 0.25)                       # off-beat open-ish hat
    if t >= 9.0:
        add(drums, hat(0.08), t + 0.125)
        add(drums, hat(0.08), t + 0.375)
    if t >= 9.0:
        root = hz(chord_at(t)[0])
        add(basses, bass(root) * 0.55, t + 0.25)           # pumping off-beat bass
    elif t % 2.0 == 0:
        add(basses, bass(hz(chord_at(t)[0]), 1.6) * 0.35, t)   # S2: long sub notes

# pluck: eighth-note arpeggio over the chord, an octave up; sparse in the intro and the end
for s in range(int(30.0 / 0.25)):
    t = s * 0.25
    triad = chord_at(t)[1]
    if t < 4.0 and s % 2:
        continue
    if t >= 26.0 and s % 2:
        continue
    if BREATH[0] <= t < BREATH[1] and s % 2:
        continue
    note = triad[[0, 1, 2, 1][s % 4]]
    f = hz(note) * 2
    add(plucks, pluck(f) * (0.16 if t < 26.0 else 0.11), t)

pad = pad_layer()

# Sidechain pump on pad and bass from the kicks.
pump = np.ones(N)
for k in kicks:
    i = int(k * SR)
    t = env_t(0.4)
    seg = 1 - 0.55 * np.exp(-t / 0.09)
    j = min(N, i + len(t))
    pump[i:j] = np.minimum(pump[i:j], seg[: j - i])

music = drums + basses * pump + plucks + pad * 0.5 * pump
add(music, riser(14.4, 1.6), 14.4)                       # into the financing message
add(music, riser(24.6, 1.4) * 0.7, 24.6)                 # into the end card
add(music, kick() * 0.6, 26.0)                           # soft landing on the end card
music = hp(music, 30)


def finish(sig, peak):
    left = sig + 0.15 * np.roll(lp(sig, 4000), int(SR * 0.011))
    right = sig + 0.15 * np.roll(lp(sig, 4000), int(SR * 0.017))
    st = np.stack([left, right], axis=1)
    st *= (np.minimum(1, T / 0.05) * np.clip((DUR - T) / 2.5, 0, 1))[:, None]
    return st * (peak / np.max(np.abs(st)))


out = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
os.makedirs(out, exist_ok=True)
wavfile.write(os.path.join(out, "music.wav"), SR, (finish(music, 0.5) * 32767).astype(np.int16))
print("wrote music.wav")
