"""Place the narration take on the film timeline, one sentence per beat.

Source: vo_raw.wav, one continuous take of the brief's script, generated with Higgsfield
Text to Speech V2 (ElevenLabs engine, preset voice "Gia"), converted from MP3 to 48 kHz WAV.
This is synthetic speech, not a human recording.
Sentence boundaries are the measured pauses in the take (energy below 0.03 of peak).

Writes vo.wav (48 kHz stereo, 30.0 s) and prints the speech span of every sentence on the
film timeline; SUBTITLES in compose_cantiere.py is timed to it.
Usage: python place_vo.py [audio_dir]
"""
import os
import sys

import numpy as np
from scipy.io import wavfile

HERE = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
SR, DUR = 48000, 30.0

# (source in s, source out s, film start s, sentence)
PLACEMENTS = [
    (0.00, 3.80, 0.30, "Dal bagno di casa agli interventi su un intero edificio."),
    (4.30, 9.50, 4.10, "Ogni progetto parte da uno spazio da trasformare e da un'idea da costruire."),
    (10.00, 16.10, 9.40, "Con Ristrutturare per Te, guardiamo oltre il cantiere e immaginiamo nuove possibilità."),
    (16.60, 23.40, 15.70, "Qui ti mostriamo lavori in corso e possibili finiture: dal singolo ambiente ai progetti più grandi."),
    (23.90, 25.90, 24.00, "Hai uno spazio da rinnovare?"),
    (26.10, 27.28, 27.20, "Parliamone insieme."),
]

sr, raw = wavfile.read(os.path.join(HERE, "vo_raw.wav"))
assert sr == SR, sr
raw = raw.astype(np.float64) / 32768.0
if raw.ndim == 1:
    raw = np.stack([raw, raw], axis=1)
mono = raw.mean(1)
peak = np.abs(mono).max()

out = np.zeros((int(SR * DUR), 2))
fade = int(SR * 0.015)
for a, b, start, text in PLACEMENTS:
    clip = raw[int(a * SR):int(b * SR)].copy()
    ramp = np.linspace(0, 1, fade)[:, None]
    clip[:fade] *= ramp
    clip[-fade:] *= ramp[::-1]
    i = int(start * SR)
    out[i:i + len(clip)] += clip
    seg = np.abs(mono[int(a * SR):int(b * SR)])
    win = int(SR * 0.02)
    voiced = [k for k in range(0, len(seg) - win, win) if seg[k:k + win].max() > 0.03 * peak]
    s0, s1 = start + voiced[0] / SR, start + (voiced[-1] + win) / SR
    print(f"{s0:6.2f} - {s1:6.2f}  {text}")

wavfile.write(os.path.join(HERE, "vo.wav"), SR, (np.clip(out, -1, 1) * 32767).astype(np.int16))
print("wrote vo.wav")
