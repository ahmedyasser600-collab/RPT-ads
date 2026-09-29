"""Compose the 40s background score directly on the Reel's scene timeline.

Soft piano + warm pad, synthesized. Every scene cut gets its chord change, so music,
voice-over and picture move together:
  0.0  cold, sparse (the old bathroom)      8.8  the filter opens (turn of the story)
 12.6  warm and full, chimes on the words   22.0  gentle pulse builds through the works
 28.4  full resolution on the before/after  33.6  calm cadence under the CTA, fade to 40.0
Light SFX: tape-measure unroll at 12.6, soft whoosh on the wipe at 28.4.

Usage: python3 compose_music.py <out.wav>
"""
import sys

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, fftconvolve, sosfilt

SR, DUR = 48000, 40.0
N = int(SR * DUR)
rng = np.random.default_rng(7)


def hz(note):
    names = {"C": 0, "C#": 1, "D": 2, "Eb": 3, "E": 4, "F": 5, "F#": 6, "G": 7, "Ab": 8, "A": 9, "Bb": 10, "B": 11}
    name, octave = note[:-1], int(note[-1])
    return 440.0 * 2 ** ((names[name] + 12 * (octave + 1) - 69) / 12)


def piano(freq, dur, vel=0.5):
    """Soft felt-piano tone: a few slightly inharmonic partials with exponential decay."""
    t = np.arange(int(SR * dur)) / SR
    out = np.zeros_like(t)
    for k, amp in enumerate([1.0, 0.45, 0.22, 0.12, 0.06], start=1):
        f = freq * k * (1 + 0.0004 * k * k)
        out += amp * np.sin(2 * np.pi * f * t) * np.exp(-t * (1.6 + 0.9 * k))
    attack = np.minimum(1, t / 0.006)
    release = np.minimum(1, (dur - t) / 0.25)
    return vel * out * attack * release


def pad(freqs, dur, level=0.12):
    """Warm pad: detuned sines with slow swell in and out."""
    t = np.arange(int(SR * dur)) / SR
    out = np.zeros_like(t)
    for f in freqs:
        for det in (-0.35, 0.0, 0.35):
            out += np.sin(2 * np.pi * (f + det) * t + rng.uniform(0, 6.28))
    env = np.minimum(1, t / 1.2) * np.minimum(1, (dur - t) / 1.0)
    return level * out / (3 * len(freqs)) * env


def add(buf, sig, start):
    i = int(start * SR)
    j = min(len(buf), i + len(sig))
    buf[i:j] += sig[: j - i]


def lowpass(sig, cutoff):
    return sosfilt(butter(2, cutoff, "low", fs=SR, output="sos"), sig)


# (start, end, bass, pad notes, arpeggio notes, arpeggio step seconds)
SECTIONS = [
    (0.0, 4.6, "A2", ["A3", "C4", "E4"], ["A4", "E4", "C5", "E4"], 0.75),        # Am, sparse
    (4.6, 8.8, "F2", ["F3", "A3", "E4"], ["A4", "C5", "E4", "C5"], 0.75),        # Fmaj7
    (8.8, 12.6, "C3", ["C4", "E4", "G4"], ["G4", "C5", "E5", "C5"], 0.5),        # C, opens up
    (12.6, 17.4, "G2", ["G3", "B3", "D4"], ["D5", "B4", "G4", "B4"], 0.5),       # G, warm
    (17.4, 22.0, "F2", ["F3", "A3", "C4", "E4"], ["C5", "A4", "E5", "A4"], 0.5),  # Fmaj7
    (22.0, 23.4, "C3", ["C4", "E4", "G4"], ["E5", "G4", "C5", "G4"], 0.35),      # build: C
    (23.4, 25.0, "B2", ["G3", "B3", "D4"], ["D5", "G4", "B4", "G4"], 0.35),      # G/B
    (25.0, 28.4, "A2", ["A3", "C4", "E4"], ["E5", "A4", "C5", "A4"], 0.35),      # Am
    (28.4, 33.6, "C2", ["C4", "E4", "G4", "C5"], ["G5", "E5", "C5", "E5"], 0.5),  # C, resolution
    (33.6, 36.2, "F2", ["F3", "A3", "C4", "G4"], ["C5", "A4", "G4", "A4"], 0.65),  # Fadd9
    (36.2, 37.8, "G2", ["G3", "B3", "D4"], ["D5", "B4"], 0.8),                   # G
    (37.8, 40.0, "C2", ["C4", "E4", "G4"], [], 1.0),                             # C, final
]

piano_bus = np.zeros(N)
pad_bus = np.zeros(N)
sfx_bus = np.zeros(N)

for start, end, bass, pads, arp, step in SECTIONS:
    length = end - start
    # Chord change lands exactly on the scene cut.
    add(piano_bus, piano(hz(bass), min(length + 0.6, 4.0), 0.55), start)
    for n in pads[:3]:
        add(piano_bus, piano(hz(n), min(length + 0.6, 4.0), 0.22), start + 0.02)
    add(pad_bus, pad([hz(n) for n in pads], length + 0.8), start - 0.3 if start > 0 else 0)
    t, i = start + step, 0
    while arp and t < end - 0.1:
        vel = 0.16 if start < 8.8 else 0.22
        if 22.0 <= start < 28.4:
            vel = 0.2 + 0.08 * (t - 22.0) / 6.4  # build through the works
        add(piano_bus, piano(hz(arp[i % len(arp)]), 1.6, vel), t)
        t += step
        i += 1

# Final chord on "Padova e provincia", ringing out.
for n in ["C3", "G3", "C4", "E4", "G4", "C5"]:
    add(piano_bus, piano(hz(n), 2.8, 0.25), 39.2 - 1.4)

# Soft chimes on "Esigenze", "Budget", "Tempi".
for t0, n in [(13.9, "G5"), (14.9, "B5"), (16.2, "D6")]:
    add(piano_bus, piano(hz(n), 1.4, 0.14), t0)

# Pulse under the works (soft low thump on each photo cut and every 0.7s).
for t0 in np.arange(22.0, 28.4, 0.7):
    tt = np.arange(int(SR * 0.25)) / SR
    thump = np.sin(2 * np.pi * 60 * tt) * np.exp(-tt * 18) * 0.18
    add(sfx_bus, thump, t0)

# Tape measure unrolling at 12.6: bright noise with fast ticks.
tt = np.arange(int(SR * 0.8)) / SR
ticks = (np.sin(2 * np.pi * 38 * tt) > 0.9).astype(float)
unroll = sosfilt(butter(2, [2500, 7000], "band", fs=SR, output="sos"), rng.standard_normal(len(tt)))
add(sfx_bus, 0.05 * unroll * (0.4 + ticks) * np.minimum(1, (0.8 - tt) / 0.2), 12.6)

# Whoosh on the before/after wipe at 28.4.
tt = np.arange(int(SR * 0.9)) / SR
noise = rng.standard_normal(len(tt))
sweep = sosfilt(butter(2, [300, 3000], "band", fs=SR, output="sos"), noise)
add(sfx_bus, 0.07 * sweep * np.sin(np.pi * tt / 0.9) ** 2, 28.3)

# Cold, closed sound in the 'before' scenes; the filter opens on the turn at 8.8s.
t_all = np.arange(N) / SR
closed = lowpass(piano_bus + pad_bus, 900)
openmix = piano_bus + pad_bus
blend = np.clip((t_all - 8.4) / 0.8, 0, 1)
music = closed * (1 - blend) + openmix * blend + sfx_bus

# Room reverb: exponentially decaying stereo noise impulse.
ir_len = int(SR * 2.2)
ir_t = np.arange(ir_len) / SR
left, right = [], []
for ch in range(2):
    ir = rng.standard_normal(ir_len) * np.exp(-ir_t * 3.2)
    ir = lowpass(ir, 5000)
    ir /= np.sqrt(np.sum(ir ** 2))
    wet = fftconvolve(music, ir)[:N]
    (left if ch == 0 else right).append(0.75 * music + 0.45 * wet)
stereo = np.stack([left[0], right[0]], axis=1)

# Fade in/out and normalize to a modest level (voice sits on top in the mix).
fade = np.minimum(1, t_all / 0.4) * np.clip((DUR - t_all) / 1.2, 0, 1)
stereo *= fade[:, None]
stereo *= 0.5 / np.max(np.abs(stereo))
wavfile.write(sys.argv[1], SR, (stereo * 32767).astype(np.int16))
