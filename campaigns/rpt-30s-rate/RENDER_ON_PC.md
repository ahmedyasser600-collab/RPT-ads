# Render the 30s reel on a Windows PC (GPU)

Everything needed is in this repository: the read-only 3D library (repo root), the campaign
Blender files and scripts (`blender/`), the compositor, fonts, logo, music, SFX and subtitles.

## Requirements (one time)

- Git for Windows, Python 3.10+ (`python --version`), Blender 4.5 LTS.
- Python packages: `python -m pip install pillow imageio-ffmpeg numpy scipy`

## Steps (PowerShell)

```powershell
# 1. Get the project
git clone https://github.com/ahmedyasser600-collab/RPT-ads.git
cd RPT-ads
git checkout claude/rpt-instagram-reel-concept-ulolnv
cd campaigns\rpt-30s-rate\blender

# 2. Point to Blender (adjust if installed elsewhere)
$BL = "C:\Program Files\Blender Foundation\Blender 4.5\blender.exe"

# 3. One-frame GPU test (frame 400 = assembly shot). Look for "GPU rendering with ..."
& $BL -b --python render_frames.py -- 400 400 ..\.work\final 100 128 gpu

# 4. Full render: frames 1-780 at 1080x1920, 128 samples, GPU. Resumable: run again if stopped.
& $BL -b --python render_frames.py -- 1 780 ..\.work\final 100 128 gpu

# 5. Composite text, logo, subtitles, voiceover, music and SFX into the MP4
cd ..
python compose_film.py --frames .work\final --out review\RPT_30s_REVIEW_full.mp4 `
  --vo audio\vo.wav --music audio\music.wav --sfx audio\sfx.wav --srt subtitles.srt
```

Audio is made in code from files in `audio\` (no step needed unless you change them):
`python audio\compose_music.py` (score), `python audio\place_vo.py` (places the Higgsfield
voiceover takes `vo_raw*.wav` on the shots; `SUBTITLES` in `compose_film.py` is timed to it).
`--review` adds a "REVIEW" tag and a legal-note placeholder; the client approved the panel
wording "Più modi per pagare, anche a rate." without extra details, so it is no longer used.
On this PC (Intel Arc iGPU, not detected by Cycles) the reel was rendered on the CPU at
32 samples into `.work\final32` (~35-45 s per frame).

## Notes

- If step 3 prints "No supported GPU found", enable the GPU in Blender:
  Edit > Preferences > System > Cycles Render Devices (OptiX/CUDA for NVIDIA, HIP for AMD),
  save preferences, and run step 3 again.
- `film.blend` is already built. To rebuild it from the library after editing the scripts:
  `& $BL -b --python build_stage.py` then `& $BL -b --python build_film.py`.
- Frame n is shown at (n-1)/30 s; frames 781-900 are the 2D end card made by the compositor.
- Output folders under `.work\` are not committed (see `.gitignore`).
