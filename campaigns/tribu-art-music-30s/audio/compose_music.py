"""Original acoustic instrumental bed for the 30 s Tribu del Alma Art & Music reel.

Composed and synthesised entirely in this script: no samples, loops or recordings, so no
third-party licence applies. The guitar is a Karplus-Strong plucked-string model with a
soft nylon-like excitation and a small body resonance; bass, shaker and frame drum are
simple synthesised voices; a short synthetic room reverb glues them together.

60 BPM, 4/4 (one bar = 4 s), D major, fingerpicked eighth notes.
  bar 0  0-4 s    D(add9)   guitar alone, treble only: the hook
  bar 1  4-8 s    Gmaj7     thumb bass + soft bass enter: "make room"
  bar 2  8-12 s   Bm7       shaker enters: paint / write / make music
  bar 3  12-16 s  A(sus4)   soft frame drum on 1 and 3: shared moments
  bar 4  16-20 s  D
  bar 5  20-24 s  Gmaj7     drum and shaker thin out
  bar 6  24-28 s  Em7 | A   end card: gentle strums
  bar 7  28-30 s  D         final chord rings out, fade

No impacts, risers, whooshes or 'spiritual' effects. Writes music.wav (48 kHz stereo).
Usage: python compose_music.py [out.wav]
"""
import os
import sys

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, lfilter, resample_poly, sosfilt

SR, DUR = 48000, 30.0
OS = 2                      # guitar is synthesised at 96 kHz for finer string tuning
N = int(SR * DUR)
rng = np.random.default_rng(1911)
NOTES = {"C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5, "F#": 6, "G": 7, "G#": 8, "A": 9, "A#": 10, "B": 11}


def hz(name):
    return 440.0 * 2 ** ((NOTES[name[:-1]] + 12 * (int(name[-1]) + 1) - 69) / 12)


def sos(kind, f, order=2, sr=SR):
    return butter(order, f, kind, fs=sr, output="sos")


def add(buf, sig, t, gain=1.0):
    i = int(round(t * SR))
    if i < 0:                                      # humanised timing may land just before 0
        sig, i = sig[-i:], 0
    j = min(len(buf), i + len(sig))
    if 0 <= i < j:
        buf[i:j] += gain * sig[: j - i]


# ------------------------------------------------------------------ instruments
def string(freq, vel, t60=3.2, length=3.5, bright=0.5):
    """Karplus-Strong plucked string at 96 kHz, returned at 48 kHz."""
    sr = SR * OS
    period = sr / freq - 0.5                       # the 2-tap average adds half a sample
    d = int(round(period))
    g = 0.001 ** (1.0 / (freq * t60))
    burst = rng.uniform(-1, 1, d)
    burst = sosfilt(sos("low", 1200 + 5000 * bright, 1, sr), burst)
    pos = max(1, int(d * 0.18))                    # plucked ~1/5 from the bridge
    burst = burst - np.concatenate([np.zeros(pos), burst[:-pos]])
    x = np.zeros(int(sr * length))
    x[:d] = burst
    a = np.zeros(d + 2)
    a[0], a[d], a[d + 1] = 1.0, -g / 2, -g / 2
    y = lfilter([1.0], a, x)
    y = resample_poly(y, 1, OS)
    y *= np.minimum(1, (len(y) - np.arange(len(y))) / (0.05 * SR))
    return vel * y / (np.abs(y).max() + 1e-9)


def body(sig):
    """A few soft body resonances for warmth."""
    out = sig.copy()
    for f, q in ((105, 0.10), (210, 0.07), (420, 0.04)):
        out += q * sosfilt(sos("band", [f * 0.85, f * 1.15]), sig) * 6
    return sosfilt(sos("low", 7000), out)


def bass(freq, dur, vel):
    t = np.arange(int(SR * dur)) / SR
    s = np.sin(2 * np.pi * freq * t) + 0.3 * np.sin(4 * np.pi * freq * t) + 0.1 * np.sin(6 * np.pi * freq * t)
    env = np.minimum(1, t / 0.012) * np.exp(-t * 1.1) * np.minimum(1, (dur - t) / 0.15)
    return vel * sosfilt(sos("low", 600), s * env)


def frame_drum(vel):
    t = np.arange(int(SR * 0.6)) / SR
    f = 58 + 40 * np.exp(-t * 25)
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7)
    skin = sosfilt(sos("band", [180, 900]), rng.standard_normal(len(t))) * np.exp(-t * 40) * 0.25
    return vel * (tone + skin) * np.minimum(1, t / 0.003)


def shaker(vel):
    t = np.arange(int(SR * 0.09)) / SR
    return vel * sosfilt(sos("band", [4000, 9500]), rng.standard_normal(len(t))) * np.sin(np.pi * t / 0.09) ** 3


# ------------------------------------------------------------------ score
# Each chord: thumb bass strings and four treble strings for the picking pattern.
CHORDS = {
    "Dadd9": (["D3", "A2"], ["A3", "D4", "E4", "F#4"]),
    "Gmaj7": (["G2", "D3"], ["B3", "D4", "F#4", "G4"]),
    "Bm7":   (["B2", "F#3"], ["A3", "D4", "F#4", "B4"]),
    "Asus4": (["A2", "E3"], ["A3", "D4", "E4", "A4"]),
    "A":     (["A2", "E3"], ["A3", "C#4", "E4", "A4"]),
    "D":     (["D3", "A2"], ["A3", "D4", "F#4", "A4"]),
    "Em7":   (["E2", "B2"], ["G3", "D4", "E4", "B4"]),
}
BASS_ROOT = {"Dadd9": "D2", "Gmaj7": "G2", "Bm7": "B1", "Asus4": "A1", "A": "A1", "D": "D2", "Em7": "E2"}
# (bar start s, chord for beats 1-2, chord for beats 3-4)
BARS = [(0, "Dadd9", "Dadd9"), (4, "Gmaj7", "Gmaj7"), (8, "Bm7", "Bm7"), (12, "Asus4", "A"),
        (16, "D", "D"), (20, "Gmaj7", "Gmaj7")]
PATTERN = [("T", 0), ("H", 2), ("H", 1), ("H", 3), ("T", 1), ("H", 2), ("H", 0), ("H", 3)]  # per eighth

gtr = np.zeros(N)
bas = np.zeros(N)
drm = np.zeros(N)
shk = np.zeros(N)

for bar_t, c1, c2 in BARS:
    for k, (kind, idx) in enumerate(PATTERN):
        t = bar_t + 0.5 * k
        chord = c1 if k < 4 else c2
        thumbs, trebles = CHORDS[chord]
        human = rng.normal(0, 0.008)
        if kind == "T":
            if bar_t == 0:                                 # hook: treble only, soft
                add(gtr, string(hz(trebles[1]), 0.3, t60=3.0, bright=0.45), t + human)
                continue
            add(gtr, string(hz(thumbs[idx % 2]), 0.55, t60=3.6, bright=0.35), t + human)
        else:
            vel = (0.42 if bar_t == 0 else 0.36) * (1.1 if k in (1, 5) else 1.0)
            add(gtr, string(hz(trebles[idx]), vel, t60=2.8, bright=0.55), t + human)
    if bar_t >= 4:
        add(bas, bass(hz(BASS_ROOT[c1]), 1.9, 0.5), bar_t)
        add(bas, bass(hz(BASS_ROOT[c2]), 1.9, 0.38), bar_t + 2)
    if 8 <= bar_t < 24:
        for e in range(8):
            add(shk, shaker(0.05 if e % 2 else 0.028), bar_t + 0.5 * e + 0.004)
    if 12 <= bar_t < 24:
        lvl = 0.30 if bar_t < 20 else 0.2
        add(drm, frame_drum(lvl), bar_t)
        add(drm, frame_drum(lvl * 0.7), bar_t + 2)
        add(drm, frame_drum(lvl * 0.35), bar_t + 3.5)

# End card: soft rolled strums (Em7, A, then D ringing out) plus a high melody note.
def strum(chord, t, vel, spread=0.035, t60=4.5):
    thumbs, trebles = CHORDS[chord]
    for i, n in enumerate([thumbs[0]] + trebles):
        add(gtr, string(hz(n), vel * (1.0 if i else 1.1), t60=t60, length=4.5, bright=0.4), t + i * spread)


strum("Em7", 24.0, 0.32)
add(bas, bass(hz("E2"), 1.9, 0.4), 24.0)
for k in (1, 2, 3):
    add(gtr, string(hz(CHORDS["Em7"][1][[2, 1, 3][k - 1]]), 0.3, t60=2.6), 24.0 + 0.5 * k)
strum("A", 26.0, 0.30)
add(bas, bass(hz("A1"), 1.9, 0.36), 26.0)
for k in (1, 2, 3):
    add(gtr, string(hz(CHORDS["A"][1][[2, 1, 3][k - 1]]), 0.28, t60=2.6), 26.0 + 0.5 * k)
strum("D", 28.0, 0.30, spread=0.05, t60=5.0)
add(bas, bass(hz("D2"), 2.0, 0.34), 28.0)
add(gtr, string(hz("F#5"), 0.18, t60=4.0, length=2.0), 28.55)

gtr = body(gtr)


def fft_convolve(a, b):
    n = 1 << int(np.ceil(np.log2(len(a) + len(b))))
    return np.fft.irfft(np.fft.rfft(a, n) * np.fft.rfft(b, n), n)[: len(a)]


def reverb(sig, seed, length=1.1, mix=0.18):
    r = np.random.default_rng(seed)
    t = np.arange(int(SR * length)) / SR
    ir = sosfilt(sos("low", 5000), r.standard_normal(len(t)) * np.exp(-t * 6.0))
    ir /= np.sqrt((ir ** 2).sum())
    return sig + mix * fft_convolve(sig, ir)


dry_l = 1.00 * gtr + 0.30 * bas + 0.45 * drm + 0.8 * shk
dry_r = 0.92 * gtr + 0.30 * bas + 0.45 * drm + 1.0 * shk
left = reverb(sosfilt(sos("high", 45), dry_l), 11)
right = reverb(sosfilt(sos("high", 45), dry_r), 12)
st = np.stack([left, right], axis=1)
t = np.arange(N) / SR
st *= (np.minimum(1, t / 0.03) * np.clip((DUR - t) / 1.6, 0, 1))[:, None]   # gentle fade to silence by 30 s
st *= 0.5 / np.abs(st).max()

out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "music.wav")
wavfile.write(out, SR, (st * 32767).astype(np.int16))
print("wrote", out)
