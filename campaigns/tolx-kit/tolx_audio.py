"""TOLX video kit, audio side: original code-composed score, UI sound effects and voiceover placement.

No samples, loops or recordings are used for music/SFX, so no third-party licence applies.
Voiceover takes are synthetic speech (Higgsfield Text to Speech V2, ElevenLabs engine, preset
voice "Marcus"), one file per line; place_vo() trims them, shortens long pauses, speeds a line
up by at most 1.15x (pitch kept) only if it overruns its scene, and never overlaps two lines.
"""
import os
import subprocess

import imageio_ffmpeg
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt

SR = 48000
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
NOTE = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
rng = np.random.default_rng(42)


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
    return level * lp(s, bright) / (3 * len(freqs)) * np.minimum(1, t / 0.6) * np.minimum(1, (dur - t) / 0.6)


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
    return vel * np.sin(2 * np.pi * np.cumsum(48 + 80 * np.exp(-t * 32)) / SR) * np.exp(-t * 10)


def tick(vel):
    t = tt(0.05)
    return vel * hp(rng.standard_normal(len(t)), 5000) * np.exp(-t * 90)


def sub(freq, dur, vel):
    t = tt(dur)
    return vel * np.sin(2 * np.pi * freq * t) * np.minimum(1, t / 0.04) * np.minimum(1, (dur - t) / 0.2)


def pop(vel, pitch):
    t = tt(0.09)
    f = pitch * (1 + 0.6 * np.exp(-t * 60))
    return vel * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 45) * np.minimum(1, t / 0.002)


def swish(dur, level, lo=400, hi=5000, rise=True):
    t = tt(dur)
    env = (t / dur) ** 2 if rise else np.sin(np.pi * t / dur) ** 2
    return level * bp(rng.standard_normal(len(t)), lo, hi) * env


def alert(vel):
    """Two-tone attention chime (low-stock warning)."""
    out = np.zeros(int(SR * 0.6))
    add(out, bell(hz("A5"), vel, 0.5), 0.0)
    add(out, bell(hz("E5"), vel, 0.5), 0.14)
    return out


def build_music(dur, turn, work, end, bpm=112):
    """Problem section (Am / Fmaj7, ticking) until `turn`, lift to C - G - Am - F, full groove from `work`,
    C major chord rings out from `end` (all in seconds)."""
    beat = 60 / bpm
    bar = 4 * beat
    music = np.zeros(int(SR * dur))
    prob = [("A2", ["A3", "C4", "E4", "B4"]), ("F2", ["F3", "A3", "C4", "E4"])]
    t, k = 0.0, 0
    while t < turn:
        bass, voicing = prob[k % 2]
        add(music, pad([hz(n) for n in voicing], bar + 0.6, 0.11, 1400), max(0, t - 0.1))
        add(music, sub(hz(bass), bar, 0.16), t)
        t += bar
        k += 1
    for b in range(int(turn / (beat / 2))):
        add(music, tick(0.05 if b % 2 == 0 else 0.025), b * beat / 2)
        if b % 4 == 2:
            add(music, pluck(hz("E5"), 0.035, 12), b * beat / 2)
    add(music, swish(1.6, 0.06, 300, 6000), turn - 1.3)
    work_prog = [("C2", ["C4", "E4", "G4", "D5"]), ("G1", ["B3", "D4", "G4", "D5"]),
                 ("A1", ["A3", "C4", "E4", "B4"]), ("F1", ["A3", "C4", "F4", "E5"])]
    arp = [0, 2, 1, 3, 2, 1, 3, 2]
    t, k = turn, 0
    while t < end:
        bass, voicing = work_prog[k % 4]
        add(music, pad([hz(n) for n in voicing], bar + 0.6, 0.09 if t < work else 0.12, 2400), max(0, t - 0.1))
        add(music, sub(hz(bass) * 2, bar - 0.05, 0.20), t)
        for s in range(8):
            ts = t + s * beat / 2
            if ts >= end:
                break
            if ts >= work - 1e-6:
                add(music, pluck(hz(voicing[arp[s]]) * 2, 0.07), ts)
                if s % 4 == 0:
                    add(music, kick(0.30), ts)
                if s % 2 == 1:
                    add(music, tick(0.035), ts)
            elif s % 2 == 0:
                add(music, pluck(hz(voicing[arp[s]]) * 2, 0.045), ts)
        t += bar
        k += 1
    for i, n in enumerate(["C3", "G3", "C4", "E4", "G4", "D5"]):
        add(music, bell(hz(n), 0.05, 3.5), end + 0.04 * i)
    add(music, pad([hz(n) for n in ["C4", "E4", "G4", "B4"]], dur - end + 0.2, 0.11, 2200), end - 0.2)
    add(music, sub(hz("C2"), dur - end, 0.18), end)
    return hp(music, 28)


def write_stereo(path, sig, peak, dur):
    t = np.arange(len(sig)) / SR
    left = sig + 0.15 * np.roll(lp(sig, 4000), int(SR * 0.009))
    right = sig + 0.15 * np.roll(lp(sig, 4000), int(SR * 0.015))
    st = np.stack([left, right], axis=1)
    st *= (np.minimum(1, t / 0.03) * np.clip((dur - t) / 1.5, 0, 1))[:, None]
    st *= peak / np.max(np.abs(st))
    wavfile.write(path, SR, (st * 32767).astype(np.int16))


# ---------------------------------------------------------------- voiceover placement
MAX_PAUSE = 0.22
MAX_TEMPO = 1.15


def _load(path, tempo=1.0):
    af = ["aresample=48000"] + ([f"atempo={tempo:.4f}"] if tempo != 1.0 else [])
    raw = subprocess.run([FFMPEG, "-nostdin", "-loglevel", "error", "-i", path, "-af", ",".join(af),
                          "-ac", "1", "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).astype(np.float64)


def _tighten(x):
    hop = SR // 100
    frames = len(x) // hop
    rms = np.array([np.sqrt(np.mean(x[i * hop:(i + 1) * hop] ** 2) + 1e-12) for i in range(frames)])
    voiced = rms > 10 ** (-40 / 20)
    idx = np.flatnonzero(voiced)
    if not len(idx):
        return x
    out, run = [], 0
    for i in range(max(0, idx[0] - 2), min(frames, idx[-1] + 6)):
        run = 0 if voiced[i] else run + 1
        if run <= int(MAX_PAUSE * 100):
            out.append(x[i * hop:(i + 1) * hop])
    y = np.concatenate(out)
    fade = int(0.008 * SR)
    y[:fade] *= np.linspace(0, 1, fade)
    y[-fade:] *= np.linspace(1, 0, fade)
    return y


def tight_duration(path):
    return len(_tighten(_load(path))) / SR


def place_vo(lines, vo_dir, prefix, out_wav, dur):
    """lines: (text, window_start_s, window_end_s). Takes are <vo_dir>/<prefix><index>.mp3.
    Writes out_wav and a matching .srt; returns the placed (start, end, text) cues."""
    track = np.zeros(int(SR * dur))
    prev_end, cues = 0.0, []
    for k, (text, t0, t1) in enumerate(lines):
        path = os.path.join(vo_dir, f"{prefix}{k}.mp3")
        t0 = max(t0, prev_end + 0.12)
        y = _tighten(_load(path))
        win, tempo = t1 - t0, 1.0
        if len(y) / SR > win:
            tempo = min(MAX_TEMPO, len(y) / SR / win)
            y = _tighten(_load(path, tempo))
        d = len(y) / SR
        print(f"{k}: {t0:5.2f}-{t0 + d:5.2f}s (window {win:.2f}s, tempo {tempo:.2f})"
              f"{'  OVERRUN' if d > win + 0.02 else ''}  {text}")
        prev_end = t0 + d
        cues.append((t0, t0 + d, " ".join(text.replace("...", "").split())))
        i = int(t0 * SR)
        j = min(len(track), i + len(y))
        track[i:j] += y[: j - i]
    track *= 0.89 / np.max(np.abs(track))
    wavfile.write(out_wav, SR, (track * 32767).astype(np.int16))

    def ts(x):
        ms = int(round(x * 1000))
        return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"
    with open(os.path.splitext(out_wav)[0] + ".srt", "w", encoding="utf-8") as fh:
        for i, (a, b, text) in enumerate(cues, 1):
            fh.write(f"{i}\n{ts(a)} --> {ts(b + 0.3)}\n{text}\n\n")
    return cues
