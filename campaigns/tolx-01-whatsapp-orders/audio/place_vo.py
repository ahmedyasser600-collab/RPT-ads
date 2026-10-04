"""Place the voiceover lines on the video timeline -> vo_<voice>.wav (48 kHz mono, 30 s).

Each line is a separate synthetic-speech take (Higgsfield Text to Speech V2, ElevenLabs
engine, preset voice) in vo_lines/<prefix><n>.mp3. This script trims each take, shortens
long internal pauses, speeds it up gently (max 1.15x, pitch kept) only if it still
overruns its scene window, and places it at the window start. Windows follow ../timeline.py.

Also writes <out>.srt with the spoken lines at their placed times (for caption uploads).
Usage: python place_vo.py <prefix> <out.wav>     e.g.  python place_vo.py f vo_gia.wav
"""
import os
import subprocess
import sys

import imageio_ffmpeg
import numpy as np
from scipy.io import wavfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import timeline as TL  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
SR = 48000
MAX_PAUSE = 0.22          # internal pauses longer than this are shortened to it
MAX_TEMPO = 1.15


def s(f):
    return f / TL.FPS


# (line, window start s, window end s). The text is the generation prompt, kept for reference.
LINES = [
    ("Taking orders on WhatsApp?", 0.35, s(TL.KEY_IN) - 0.15),
    ("Here's the order. Now... find it.", s(TL.KEY_IN) + 0.05, s(TL.QUESTIONS) - 0.05),
    ("Who's handling it? Did anyone follow up?", s(TL.QUESTIONS) + 0.1, s(TL.TURN) + 0.3),
    ("Give every order a place to live.", s(TL.TURN) + 0.35, s(TL.STEP_LOG) - 0.05),
    ("One: log it in one system.", s(TL.STEP_LOG) + 0.1, s(TL.STEP_ASSIGN) - 0.05),
    ("Two: assign it to one person.", s(TL.STEP_ASSIGN) + 0.1, s(TL.STEP_TRACK) - 0.05),
    ("Three: track the status, so nobody has to ask.", s(TL.STEP_TRACK) + 0.1, s(TL.STEP_FOLLOW) - 0.05),
    ("Four: follow up, with a name and a date.", s(TL.STEP_FOLLOW) + 0.1, s(TL.STATEMENT) + 0.08),
    ("Move beyond WhatsApp, with Odoo, or software built around your business.", s(TL.STATEMENT) + 0.18,
     s(TL.END_CARD) + 0.2),
    ("Book your discovery call today.", s(TL.END_CARD) + 1.0, s(TL.TOTAL) - 0.6),
]


def load(path, tempo=1.0):
    af = ["aresample=48000"] + ([f"atempo={tempo:.4f}"] if tempo != 1.0 else [])
    raw = subprocess.run([FFMPEG, "-nostdin", "-loglevel", "error", "-i", path, "-af", ",".join(af),
                          "-ac", "1", "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).astype(np.float64)


def tighten(x):
    """Trim leading/trailing silence and shorten long internal pauses (10 ms frames, -40 dBFS gate)."""
    hop = SR // 100
    frames = len(x) // hop
    rms = np.array([np.sqrt(np.mean(x[i * hop:(i + 1) * hop] ** 2) + 1e-12) for i in range(frames)])
    voiced = rms > 10 ** (-40 / 20)
    idx = np.flatnonzero(voiced)
    if not len(idx):
        return x
    a, b = max(0, idx[0] - 2), min(frames, idx[-1] + 6)
    out, run = [], 0
    keep = int(MAX_PAUSE * 100)
    for i in range(a, b):
        run = 0 if voiced[i] else run + 1
        if run <= keep:
            out.append(x[i * hop:(i + 1) * hop])
    y = np.concatenate(out)
    fade = int(0.008 * SR)
    y[:fade] *= np.linspace(0, 1, fade)
    y[-fade:] *= np.linspace(1, 0, fade)
    return y


def main():
    prefix, out = sys.argv[1], sys.argv[2]
    track = np.zeros(int(SR * TL.TOTAL / TL.FPS))
    prev_end = 0.0
    cues = []
    for k, (text, t0, t1) in enumerate(LINES):
        t0 = max(t0, prev_end + 0.12)                       # never overlap the previous line
        path = os.path.join(HERE, "vo_lines", f"{prefix}{k}.mp3")
        y = tighten(load(path))
        win = t1 - t0
        tempo = 1.0
        if len(y) / SR > win:
            tempo = min(MAX_TEMPO, len(y) / SR / win)
            y = tighten(load(path, tempo))
        dur = len(y) / SR
        flag = "  OVERRUN" if dur > win + 0.02 else ""
        print(f"{k}: {t0:5.2f}-{t0 + dur:5.2f}s (window {win:.2f}s, tempo {tempo:.2f}){flag}  {text}")
        prev_end = t0 + dur
        cues.append((t0, t0 + dur, text.replace("...", "")))
        i = int(t0 * SR)
        j = min(len(track), i + len(y))
        track[i:j] += y[: j - i]
    track *= 0.89 / np.max(np.abs(track))
    wavfile.write(os.path.join(HERE, out), SR, (track * 32767).astype(np.int16))
    def ts(x):
        ms = int(round(x * 1000))
        return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"
    with open(os.path.join(HERE, os.path.splitext(out)[0] + ".srt"), "w", encoding="utf-8") as fh:
        for i, (a, b, text) in enumerate(cues, 1):
            fh.write(f"{i}\n{ts(a)} --> {ts(b + 0.3)}\n{' '.join(text.split())}\n\n")
    print("wrote", out)


if __name__ == "__main__":
    main()
