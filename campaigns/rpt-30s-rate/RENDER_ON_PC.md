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

# 5. Composite text, logo, subtitles, music and SFX into the MP4
cd ..
python compose_film.py --frames .work\final --out review\RPT_30s_REVIEW_full.mp4 `
  --music audio\music.wav --sfx audio\sfx.wav --srt subtitles.srt --review
```

When the voiceover WAV is available, add `--vo path\to\voiceover.wav` (the subtitles in
`compose_film.py` must then be re-timed to the recording). Remove `--review` only after the
financing provider's approved wording and legal notes have been added to the panel.

## Notes

- If step 3 prints "No supported GPU found", enable the GPU in Blender:
  Edit > Preferences > System > Cycles Render Devices (OptiX/CUDA for NVIDIA, HIP for AMD),
  save preferences, and run step 3 again.
- `film.blend` is already built. To rebuild it from the library after editing the scripts:
  `& $BL -b --python build_stage.py` then `& $BL -b --python build_film.py`.
- Frame n is shown at (n-1)/30 s; frames 781-900 are the 2D end card made by the compositor.
- Output folders under `.work\` are not committed (see `.gitignore`).
