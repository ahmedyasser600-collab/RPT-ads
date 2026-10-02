"""Original instrumental bed + transition swishes for the 30s "Dal bagno all'intero edificio" reel.

Composed in code (no samples or recordings), so no third-party licence applies.
100 BPM (beat 0.6 s, bar 2.4 s): warm piano, plucked eighth-note texture, soft kick/shaker,
sustained sub bass. F - C/E - Dm - Bb, resolving to F under the end card.
  0-3 s    piano and pad only (hook)
  3-24 s   pluck, soft percussion and bass
  24-27 s  percussion out under the question
  27-30 s  final F chord rings out

Writes music.wav and sfx.wav (48 kHz stereo). The narration ducks the music in the mix.
Usage: python compose_audio.py [out_dir]
"""
import os
import sys

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt

SR, DUR, BEAT = 48000, 30.0, 0.6
BAR = 4 * BEAT
N = int(SR * DUR)
T = np.arange(N) / SR
rng = np.random.default_rng(23)

NOTE = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11, "Bb": 10}


def hz(n):
    return 440.0 * 2 ** ((NOTE[n[:-1]] + 12 * (int(n[-1]) + 1) - 69) / 12)


CHORDS = {  # bass, voicing
    "F": ("F2", ["F3", "A3", "C4", "E4"]),
    "C/E": ("E2", ["E3", "G3", "C4", "D4"]),
    "Dm": ("D2", ["D3", "F3", "A3", "C4"]),
    "Bb": ("Bb1", ["Bb3", "D4", "F4", "A4"]),
}
PROG = ["F", "C/E", "Dm", "Bb"]


def chord_at(t):
    if t >= 27.0:
        return CHORDS["F"]
    return CHORDS[PROG[int(t // BAR) % len(PROG)]]


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


def piano(freq, dur, vel):
    t = tt(dur)
    out = sum(a * np.sin(2 * np.pi * freq * k * (1 + 0.0004 * k * k) * t) * np.exp(-t * (1.2 + 0.8 * k))
              for k, a in enumerate([1.0, 0.45, 0.22, 0.12, 0.06], start=1))
    return vel * out * np.minimum(1, t / 0.006) * np.minimum(1, (dur - t) / 0.3)


def pluck(freq, vel):
    t = tt(0.5)
    s = np.sin(2 * np.pi * freq * t) + 0.35 * np.sin(4 * np.pi * freq * t) + 0.12 * np.sin(6 * np.pi * freq * t)
    return vel * lp(s, 3500) * np.exp(-t * 9) * np.minimum(1, t / 0.002)


def kick(vel):
    t = tt(0.3)
    f = 50 + 70 * np.exp(-t * 30)
    return vel * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 11)


def shaker(vel):
    t = tt(0.08)
    return vel * hp(rng.standard_normal(len(t)), 6000) * np.sin(np.pi * t / 0.08) ** 2


def sub(freq, dur, vel):
    t = tt(dur)
    return vel * np.sin(2 * np.pi * freq * t) * np.minimum(1, t / 0.05) * np.minimum(1, (dur - t) / 0.2)


def pad(freqs, dur, level):
    t = tt(dur)
    s = sum(np.sin(2 * np.pi * (f + d) * t + rng.uniform(0, 6.28)) for f in freqs for d in (-0.4, 0, 0.4))
    return level * s / (3 * len(freqs)) * np.minimum(1, t / 0.8) * np.minimum(1, (dur - t) / 0.8)


music = np.zeros(N)
n_bars = int(np.ceil(27.0 / BAR))
for b in range(n_bars):
    t0 = b * BAR
    bass, voicing = chord_at(t0)
    add(music, pad([hz(n) for n in voicing], BAR + 0.8, 0.10), max(0.0, t0 - 0.2))
    for k, n in enumerate(voicing[:3]):                     # soft rolled piano chord each bar
        add(music, piano(hz(n), 2.6, 0.13), t0 + 0.03 * k)
    if t0 >= 3.0 - 1e-6 and t0 < 24.0:
        add(music, sub(hz(bass), BAR - 0.05, 0.22), t0)
# final chord under the end card
for k, n in enumerate(["F2", "C3", "F3", "A3", "C4", "E4"]):
    add(music, piano(hz(n), 3.0, 0.12), 27.0 + 0.05 * k)
add(music, pad([hz(n) for n in ["F3", "A3", "C4", "E4"]], 3.0, 0.10), 26.8)

# eighth-note pluck texture and soft percussion
for s in range(int(27.0 / (BEAT / 2))):
    t = s * BEAT / 2
    voicing = chord_at(t)[1]
    if t >= 3.0:
        note = voicing[[0, 2, 1, 3, 2, 1, 3, 2][s % 8]]
        add(music, pluck(hz(note) * 2, 0.09 if t < 24.0 else 0.06), t)
    if 3.0 <= t < 24.0:
        beat = s // 2
        if s % 2 == 0 and beat % 2 == 0:
            add(music, kick(0.35), t)
        if s % 2 == 1:
            add(music, shaker(0.05), t)
music = hp(music, 30)

sfx = np.zeros(N)


def swish(dur, level, lo=500, hi=4000):
    t = tt(dur)
    return level * bp(rng.standard_normal(len(t)), lo, hi) * np.sin(np.pi * t / dur) ** 2


for t_cut, dur, level in ((3.0, 0.5, 0.05), (10.0, 0.6, 0.025), (18.0, 0.5, 0.05), (24.0, 0.5, 0.04), (27.0, 0.6, 0.035)):
    add(sfx, swish(dur, level), t_cut - dur / 2)


def finish(sig, peak, width_ms=(11, 17)):
    left = sig + 0.15 * np.roll(lp(sig, 4000), int(SR * width_ms[0] / 1000))
    right = sig + 0.15 * np.roll(lp(sig, 4000), int(SR * width_ms[1] / 1000))
    st = np.stack([left, right], axis=1)
    st *= (np.minimum(1, T / 0.05) * np.clip((DUR - T) / 2.0, 0, 1))[:, None]
    return st * (peak / np.max(np.abs(st)))


out = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
os.makedirs(out, exist_ok=True)
wavfile.write(os.path.join(out, "music.wav"), SR, (finish(music, 0.5) * 32767).astype(np.int16))
wavfile.write(os.path.join(out, "sfx.wav"), SR, (finish(sfx, 0.3) * 32767).astype(np.int16))
print("wrote music.wav and sfx.wav")
