# RPT — "Dal bagno all'intero edificio" (30 s, 9:16)

Photo-based reel, no 3D. Real construction photos are labelled **"Prima"**; the AI-generated
design concepts are labelled **"Dopo"** (client's choice). Because the "Dopo" images are
illustrative concepts, not finished RPT work, the footnote **"Immagini “dopo” a scopo
illustrativo"** is on screen whenever one is visible. No copy is baked into the images.

## Assets

| # | Original (`photos/originals/`) | Concept (`photos/concepts/`, AI-generated, hypothetical) |
|---|---|---|
| 01 | `01_original_demolition.jpg` | `01_concept_bathroom.webp` |
| 02 | `02_original_room.jpg` | `02_concept_study.webp` |
| 03 | `03_original_staircase_portal.jpg` | `03_concept_staircase_portal.webp` |
| 04 | `04_original_staircase_wide.jpg` (shown cropped so the worker at the right edge is out of frame) | `04_concept_staircase_wide.webp` |

03 and 04 are the same site. The concepts are creative interpretations, not measured
proposals or completed RPT work, so they are revealed with wipes/dissolves, never morphs.

- Logo: `reels/assets/logo.webp` (repo), unchanged raster, proportional resize only.
- Fonts: Plus Jakarta Sans (`fonts/`, OFL).
- Narration: `audio/vo_raw.wav`, synthetic speech (Higgsfield Text to Speech V2, ElevenLabs
  engine, preset voice "Gia"), the brief's script; placed per sentence by `audio/place_vo.py`
  into `audio/vo.wav`.
- Music and swishes: `audio/compose_audio.py` -> `audio/music.wav`, `audio/sfx.wav`
  (original, composed in code, 100 BPM; no third-party licence needed).
- Captions: `captions.srt` (written by the compositor).

## Render (PowerShell, from this folder)

```powershell
python -m pip install pillow imageio-ffmpeg numpy scipy
python audio\compose_audio.py audio          # only if the score is changed
python audio\place_vo.py audio               # only if the narration placement is changed
# 540x960 review
python compose_cantiere.py --out .work\review_540.mp4 --size 540 --vo audio\vo.wav `
  --music audio\music.wav --sfx audio\sfx.wav --srt captions.srt --storyboard .work\storyboard.png
# 1080x1920 final
python compose_cantiere.py --out .work\RPT_30s_cantiere_1080.mp4 --vo audio\vo.wav `
  --music audio\music.wav --sfx audio\sfx.wav --srt captions.srt
```

Renders go to `.work\` and are not committed. Frame n (zero-based) is shown at n/30 s; 900 frames.
Important text stays inside x 100-900, y 240-1530 (`check_layout()` fails the build otherwise).
