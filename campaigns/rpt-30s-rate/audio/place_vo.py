"""Place the voiceover takes on the film timeline, one phrase per shot.

Sources (Higgsfield Text to Speech V2, ElevenLabs engine, preset voice "Gia"; converted
from MP3 to 48 kHz WAV):
  vo_raw.wav      the full script in one take (S1-S4 phrases are cut from it)
  vo_raw_url.wav  the closing line re-read as "Visita ristrutturare per te, punto it.
                  E raccontaci il tuo progetto." so the URL is spoken as separate words
Phrase boundaries are the measured pauses in each take (energy below 0.03 of peak).

Writes vo.wav (48 kHz stereo, 30.0 s) and prints the speech span of every phrase on
the film timeline, which is what SUBTITLES in compose_film.py is timed to.
Usage: python place_vo.py [audio_dir]
"""
import os
import sys

import numpy as np
from scipy.io import wavfile

HERE = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
SR, DUR = 48000, 30.0

# (source file, source in s, source out s, film start s, phrase)
PLACEMENTS = [
    ("vo_raw.wav", 0.00, 3.75, 0.40, "Il bagno che desideri parte da un progetto pensato per te."),    # S1
    ("vo_raw.wav", 4.50, 9.85, 4.25, "Spazi più pratici, materiali scelti con cura e dettagli..."),    # S2
    ("vo_raw.wav", 10.55, 14.30, 10.00, "Con Ristrutturare per Te puoi rinnovare il tuo bagno,"),      # S3
    ("vo_raw.wav", 14.50, 17.55, 16.45, "con pagamenti facili e flessibili, anche a rate."),           # S4, after the whip
    ("vo_raw.wav", 18.25, 20.20, 20.25, "Lavoriamo a Padova e provincia."),                            # S4
    ("vo_raw_url.wav", 0.00, 2.60, 23.00, "Visita ristrutturare per te,"),                             # S5
    ("vo_raw_url.wav", 2.80, 4.10, 25.75, "punto it."),                                                # end card, URL
    ("vo_raw_url.wav", 4.40, 6.24, 27.20, "E raccontaci il tuo progetto."),                            # end card
]


def load(name):
    sr, raw = wavfile.read(os.path.join(HERE, name))
    assert sr == SR, (name, sr)
    raw = raw.astype(np.float64) / 32768.0
    return np.stack([raw, raw], axis=1) if raw.ndim == 1 else raw


SOURCES = {name: load(name) for name in {p[0] for p in PLACEMENTS}}
out = np.zeros((int(SR * DUR), 2))
fade = int(SR * 0.015)
for name, a, b, start, text in PLACEMENTS:
    raw = SOURCES[name]
    mono = raw.mean(1)
    peak = np.abs(mono).max()
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
