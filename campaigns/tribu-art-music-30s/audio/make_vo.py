"""Generate the narration clips listed in config.json with a local, open TTS model.

Engine: Kokoro-82M v1.0 (Apache-2.0) via the kokoro-onnx package, preset voice from
config (af_heart). Runs offline on CPU; no account, API or paid service. This is
synthetic speech, not a host recording, and does not imitate any real person's voice.
The brand name is given its Spanish pronunciation through a phoneme override.

Model files (download once):
  https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
  https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin

Writes audio/vo/<clip id>.wav (24 kHz mono, silence trimmed) and prints each duration.
The renderer places the clips at the 'at' times in config.json.
Usage: python audio/make_vo.py <dir with model files>
"""
import json
import os
import sys

import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = json.load(open(os.path.join(HERE, "..", "config.json"), encoding="utf-8"))
VO = CFG["voiceover"]
model_dir = sys.argv[1] if len(sys.argv) > 1 else "."
k = Kokoro(os.path.join(model_dir, "kokoro-v1.0.onnx"), os.path.join(model_dir, "voices-v1.0.bin"))
out_dir = os.path.join(HERE, "vo")
os.makedirs(out_dir, exist_ok=True)

for clip in VO["clips"]:
    text = clip["text"].format(**CFG["event"])
    ph = k.tokenizer.phonemize(text, "en-us")
    for a, b in VO["pronunciation_overrides"].items():
        ph = ph.replace(a, b)
    samples, sr = k.create(ph, voice=VO["voice"], speed=VO["speed"], is_phonemes=True)
    level = np.abs(samples)
    voiced = np.where(level > level.max() * 0.02)[0]
    samples = samples[max(0, voiced[0] - int(0.01 * sr)): voiced[-1] + int(0.1 * sr)]
    sf.write(os.path.join(out_dir, f"{clip['id']}.wav"), samples, sr)
    print(f"{clip['id']:5s} {len(samples) / sr:5.2f}s  at {clip['at']:5.2f} -> {clip['at'] + len(samples) / sr:5.2f}  {text}")
