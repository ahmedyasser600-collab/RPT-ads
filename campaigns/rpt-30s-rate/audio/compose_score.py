"""Original score + SFX for the 30s RPT financing reel, composed on the film's own timeline.

Owned by the campaign (composed in code, no third-party samples or recordings), so no
external music licence applies. ~100 BPM feel (eighth-note arpeggio = 0.3 s), warm piano
+ soft pad, chord change exactly on every cut. SFX are placed on the animation keyframes
of blender/build_film.py (frame n -> (n-1)/30 s).

Writes sfx.wav (effects only), 48 kHz stereo. The score now comes from compose_music.py;
the piano score below is kept only because it draws from the same random stream as the
SFX, so removing it would change sfx.wav.
Usage: python3 compose_score.py <out_dir>
"""
import os
import sys

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, fftconvolve, sosfilt

SR, DUR = 48000, 30.0
N = int(SR * DUR)
rng = np.random.default_rng(11)


def t_of(frame):
    return (frame - 1) / 30.0


def hz(note):
    names = {"C": 0, "C#": 1, "D": 2, "Eb": 3, "E": 4, "F": 5, "F#": 6, "G": 7, "Ab": 8, "A": 9, "Bb": 10, "B": 11}
    return 440.0 * 2 ** ((names[note[:-1]] + 12 * (int(note[-1]) + 1) - 69) / 12)


def piano(freq, dur, vel):
    t = np.arange(int(SR * dur)) / SR
    out = sum(a * np.sin(2 * np.pi * freq * k * (1 + 0.0004 * k * k) * t) * np.exp(-t * (1.5 + 0.9 * k))
              for k, a in enumerate([1.0, 0.45, 0.22, 0.12, 0.06], start=1))
    return vel * out * np.minimum(1, t / 0.006) * np.minimum(1, (dur - t) / 0.25)


def pad(freqs, dur, level):
    t = np.arange(int(SR * dur)) / SR
    out = sum(np.sin(2 * np.pi * (f + d) * t + rng.uniform(0, 6.28)) for f in freqs for d in (-0.3, 0, 0.3))
    return level * out / (3 * len(freqs)) * np.minimum(1, t / 0.9) * np.minimum(1, (dur - t) / 0.8)


def add(buf, sig, start):
    i = int(start * SR)
    j = min(len(buf), i + len(sig))
    if j > i:
        buf[i:j] += sig[: j - i]


def band(sig, lo, hi):
    return sosfilt(butter(2, [lo, hi], "band", fs=SR, output="sos"), sig)


def lowpass(sig, cutoff):
    return sosfilt(butter(2, cutoff, "low", fs=SR, output="sos"), sig)


# (start s, end s, bass, pad, arpeggio, step s, velocity)
SECTIONS = [
    (0.0, 4.0, "F2", ["F3", "A3", "C4", "E4"], ["C5", "A4", "E5", "A4"], 0.6, 0.17),   # S1 doorway: gentle
    (4.0, 9.0, "D2", ["D3", "F3", "A3", "C4"], ["A4", "F4", "C5", "F4"], 0.6, 0.15),   # S2 cutaway: curious
    (9.0, 11.4, "C2", ["C3", "E3", "G3"], ["G4", "C5", "E5", "C5"], 0.3, 0.18),       # S3 assembly builds
    (11.4, 13.8, "B1", ["G3", "B3", "D4"], ["D5", "G4", "B4", "G4"], 0.3, 0.20),
    (13.8, 16.0, "A1", ["A3", "C4", "E4"], ["E5", "A4", "C5", "A4"], 0.3, 0.22),
    (16.0, 23.0, "F2", ["F3", "A3", "C4", "G4"], ["C5", "A4", "G5", "A4"], 0.3, 0.13),  # S4 financing: warm, keeps the pulse
    (23.0, 26.0, "G2", ["G3", "B3", "D4"], ["D5", "B4", "G4", "B4"], 0.6, 0.18),       # S5 hero
    (26.0, 30.0, "C2", ["C3", "G3", "E4", "G4"], ["G4", "C5", "E5"], 0.9, 0.15),        # end card: resolve
]

music = np.zeros(N)
for start, end, bass, pads, arp, step, vel in SECTIONS:
    soft = 0.55 if start in (16.0, 26.0) else 1.0        # financing panel + end card land gently, not as a stab
    add(music, piano(hz(bass), min(end - start + 0.5, 3.5), 0.5 * soft), start)
    for k, n in enumerate(pads[:3]):
        add(music, piano(hz(n), min(end - start + 0.5, 3.5), 0.18 * soft), start + 0.02 + (0.06 * k if soft < 1 else 0))
    add(music, pad([hz(n) for n in pads], end - start + 0.7, 0.11), max(0.0, start - 0.25))
    t, i = start + step, 0
    while t < end - 0.08:
        add(music, piano(hz(arp[i % len(arp)]), 1.4, vel), t)
        t, i = t + step, i + 1
for k, n in enumerate(["C4", "E4", "G4", "C5"]):        # final chord under the CTA, rolled and quiet
    add(music, piano(hz(n), 2.6, 0.07), 27.0 + 0.09 * k)

# Low pulse under the assembly (S3), one per beat; it carries on, softer, under S4.
for t0 in np.arange(9.0, 23.0, 0.6):
    tt = np.arange(int(SR * 0.22)) / SR
    add(music, np.sin(2 * np.pi * 58 * tt) * np.exp(-tt * 18) * (0.14 if t0 < 16.0 else 0.07), t0)

# ------------------------------------------------------------- SFX on animation keyframes
sfx = np.zeros(N)


def click(level=0.05, bright=4500):
    tt = np.arange(int(SR * 0.05)) / SR
    return level * band(rng.standard_normal(len(tt)), 1500, bright) * np.exp(-tt * 90)


def thump(level=0.18, f=70):
    tt = np.arange(int(SR * 0.3)) / SR
    return level * np.sin(2 * np.pi * f * tt) * np.exp(-tt * 14)


def swish(dur, level, lo=400, hi=3500):
    tt = np.arange(int(SR * dur)) / SR
    return level * band(rng.standard_normal(len(tt)), lo, hi) * np.sin(np.pi * tt / dur) ** 2


add(sfx, swish(0.9, 0.04, 2000, 9000), t_of(20))                 # mirror LED on (soft shimmer)
for i, f in enumerate((150, 156, 162, 168)):                     # floor layers lift
    add(sfx, swish(0.35, 0.025, 600, 2500), t_of(f) - 0.25)
for i, f in enumerate((250, 254, 258, 262)):                     # layers settle
    add(sfx, click(0.05, 3000) + 0, t_of(f) + 0.0)
for i in range(0, 42, 3):                                         # tiles settle (every third tile)
    add(sfx, click(0.035), t_of(271 + i * 2 + 14))
add(sfx, thump(0.16, 62), t_of(352))                             # shower tray in place
add(sfx, swish(1.0, 0.05, 1500, 7000), t_of(360))                # glass slides
add(sfx, click(0.06, 6000), t_of(390))                           # glass seats
add(sfx, thump(0.12, 80), t_of(404))                             # vanity mounts
add(sfx, click(0.05, 3500), t_of(416))                           # basin
add(sfx, click(0.04, 5000), t_of(422))                           # tap
add(sfx, click(0.04, 4000), t_of(432))                           # mirror
add(sfx, swish(0.4, 0.035, 300, 1800), t_of(440))                # drawer opens
add(sfx, thump(0.06, 110), t_of(452))
add(sfx, swish(0.4, 0.035, 300, 1800), t_of(466))                # drawer closes
add(sfx, thump(0.08, 100), t_of(478))
add(sfx, swish(0.7, 0.03, 500, 3000), 15.7)                      # transition to S4
add(sfx, swish(0.7, 0.03, 500, 3000), 25.8)                      # transition to end card


def finish(sig, peak, reverb_mix):
    tt = np.arange(N) / SR
    ir_t = np.arange(int(SR * 2.0)) / SR
    chans = []
    for ch in range(2):
        ir = lowpass(rng.standard_normal(len(ir_t)) * np.exp(-ir_t * 3.4), 5000)
        ir /= np.sqrt(np.sum(ir ** 2))
        chans.append(sig + reverb_mix * fftconvolve(sig, ir)[:N])
    st = np.stack(chans, axis=1)
    st *= (np.minimum(1, tt / 0.3) * np.clip((DUR - tt) / 1.5, 0, 1))[:, None]
    return st * (peak / np.max(np.abs(st)))


out = sys.argv[1]
os.makedirs(out, exist_ok=True)
finish(music, 0.5, 0.5)  # not written any more; keeps the random stream (SFX reverb) unchanged
wavfile.write(os.path.join(out, "sfx.wav"), SR, (finish(sfx, 0.35, 0.25) * 32767).astype(np.int16))
print("wrote sfx.wav")
