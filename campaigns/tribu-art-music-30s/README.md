# Tribu del Alma — Art & Music Retreat · 30 s vertical reel

The hook is "That creative project you keep postponing." The reel shows the real finca, real people
painting outdoors and real music on the terrace, then ends with a clear invitation to ask about joining.
It is 1080 × 1920, 30 fps, 30.0 s, H.264 High, yuv420p, AAC 48 kHz, and is built for Instagram Reels.

## Deliverables (`out/`)

| File | What it is |
|---|---|
| `tribu-art-music-30s.mp4` | **Main video.** Sparse designed text, narration and music |
| `tribu-art-music-30s-captioned.mp4` | Same video with burned-in narration captions |
| `tribu-art-music-30s-music-only.mp4` | Designed text and music, no narration. Use it as the base if a host records the voiceover |
| `tribu-art-music-30s.srt` | Narration captions. Upload them to Instagram with the main video, or keep them for accessibility |
| `contact-sheet.png` | Six frames, one per storyboard beat |

## ⚠️ Facts and items needing owner confirmation

1. **Dates.** On screen and in the narration it reads "19–25 October" / "nineteenth to twenty-fifth October".
   Year 2026 is the working campaign year. These dates come from the campaign brief and the Week 1 & 2 sprint
   document; the owner has not confirmed them. To change them, edit `event` in `config.json` and re-render.
   If the spoken date changes, re-run `audio/make_vo.py`.
2. **Photos are stand-ins cut from your website screenshot, not the original files.** The render environment's
   network policy blocked `tribudelalma.com` (HTTP 403 at the proxy), so none of the seven asset URLs could be
   downloaded. The three real Tribu photographs visible in the supplied screenshot PDF were cut out pixel for
   pixel instead (`tools/extract_standins.py`). No upscaling, retouching or generation was done when cutting them:
   - finca and landscape (`vinca-pura-vida-2.jpg`): two clean crops, avoiding the demo page's rounded corner and caption
   - people painting outdoors (`IMG_8033.jpg`)
   - music on the terrace (`Ray-Miek-Live-tribudelalma.jpg`), slightly cropped by the page layout
3. **Two of the seven requested assets are not in the video: the bedroom and "artists in residence" photos.**
   The screenshot does not contain them and they could not be downloaded. The 18–24 s "experience" beat therefore
   uses the full outdoor-studio photo and the finca garden, and there is no bedroom shot.
4. **Logo is a stand-in.** The original transparent logo PNG could not be downloaded. The end card uses the
   round emblem from the screenshot header (about 118 px, shown at 176 px on a cream seal, so it is slightly soft).
   It also has a typeset label "TRIBU DEL ALMA" in Asul. The label is not a reconstruction of the logo, and it
   disappears automatically when the original logo is supplied.
5. **The voice is synthetic.** See *Voiceover* below. Please listen before publishing. I could not audition
   the audio myself: the render environment has no playback, so audio was checked by measurement only.
6. **People.** Nobody is named or labelled. The terrace music photo is **not** presented as Danielle and Ray.
7. Not included, as instructed: prices, remaining places, discounts, testimonials, booking deadlines and any claims
   about healing or transformation.

### Swapping in the original files (recommended before publishing)

Download these into `assets/originals/` with the exact file names below, then re-render:
`IMG_8033.jpg`, `vinca-pura-vida-2.jpg`, `Ray-Miek-Live-tribudelalma.jpg`,
`tribu-del-alma-logo.final_.png` (optional for now: `artists-in-residence.jpg`, `Retreat-venue-Spain.jpg`).
The renderer uses an original file whenever it exists and falls back to the stand-in otherwise.
Originals have different dimensions and framing from the screenshot cut-outs, so check `contact-sheet.png`
afterwards and adjust the `focus` and `zoom` values in `config.json` where needed. To let a cloud session
download them itself, add `tribudelalma.com` and `www.tribudelalma.com` to the environment's allowed domains.

## Storyboard as built

| Time | Beat | Picture | On-screen text | Narration |
|---|---|---|---|---|
| 0–4 s | Recognition | Close crop of the painting table, slow pull-back | **That project you / keep postponing?** (readable on frame 0; a gold rule draws in) | "That creative project you keep postponing." |
| 4–8 s | Possibility | The finca opens from the centre outward like doors, then a slow push | GAUCÍN · ANDALUSIA / **Make room for it.** | "What if you gave it a week?" |
| 8–13 s | Creative freedom | Outdoor painting photo in two crops (table and painting, then easel) | **Paint.  Write.** / **Make music.**, word by word, each word on its spoken cue | "The painting, … the story, … the song." |
| 13–18 s | Connection | Terrace music photo, slow pan from the guitarist to the singer | **Your own rhythm.** / **Shared moments.** | "At Tribu del Alma, there's space to follow your own rhythm, create alongside others," |
| 18–24 s | The experience | Whole outdoor studio, then the finca garden | **Space to create.** → **Time to simply be.** | "…and enjoy the quieter moments in between." |
| 24–30 s | Invitation | The garden photo grows into the end-card band, then emblem, title, dates, place, CTA, website | Art & Music Retreat · 19–25 October · Gaucín, Andalusia · **Ask us about joining** · tribudelalma.com | "Join our Art and Music Retreat in Andalusia, nineteenth to twenty-fifth October. Ask us about joining." |

The CTA is on screen from 25.8 s to 30 s (4.2 s). Essential text stays inside x 100–900 and y 250–1500.
`render.py` runs `check_layout()` and fails the build if text leaves that area, if a block has more than two
lines, or if the CTA is on screen for less than 4 s. Centred elements are centred on the safe area (x = 500),
not on the frame, so they clear Instagram's right-hand buttons.

## Voiceover

- **Engine:** Kokoro-82M v1.0 (Apache-2.0) via `kokoro-onnx`, preset voice `af_heart`, speed 0.94. It ran locally
  on CPU with no account, API or paid service. It is a stock synthetic voice. It does not clone or imitate any
  real person, and it must not be described as a host recording.
- "Tribu del Alma" is forced to Spanish pronunciation ("TREE-boo del AHL-ma") through a phoneme override.
  The model's default was "TRIB-oo… OL-ma".
- **Script change:** the brief's sentences 2 and 3 are swapped so the narration lines up with the storyboard.
  The finca reveal now carries "What if you gave it a week?", and "Paint. Write. Make music." now carries "The
  painting, the story, the song." Every word of the brief's script is kept. Nothing is sped up: there is 20.1 s
  of speech in the 30 s film.
- Mix (measured on the final MP4): narrated sections are about −17 LUFS. Music sits about 8 LU under the
  narration level and ducks a further 5 dB while she speaks, so it is clearly beneath the voice but still present
  in the pauses (about −28 LUFS). Integrated loudness is −17.6 LUFS and true peak is −1.5 dBFS, so nothing clips.
  Instagram normalises playback loudness, so there is no need to push it louder.

### Timed narration script (for a host recording)

Record it as one relaxed take and the edit will be re-timed to it. If you replace `audio/vo/*.wav`, the clip
names and start times are in `config.json → voiceover.clips`.

```
00:00.45  That creative project you keep postponing.
00:04.55  What if you gave it a week?
00:08.35  The painting,
00:09.55  the story,
00:10.75  the song.
00:13.35  At Tribu del Alma, there's space to follow your own rhythm,
          create alongside others, and enjoy the quieter moments in between.
00:22.40  Join our Art and Music Retreat in Andalusia, nineteenth to twenty-fifth October.
00:27.95  Ask us about joining.        (ends by ~29.3 s)
```

## Music

`audio/music.wav` is an original instrumental composed and synthesised for this project in
`audio/compose_music.py`. It uses no samples, loops or recordings, so **no third-party licence applies**.
It is a fingerpicked nylon-string guitar (Karplus–Strong physical model) at 60 BPM in D major. Soft bass enters
at 4 s, a shaker at 8 s and a frame drum at 12 s. The parts thin out under the end card and the piece resolves on
D. There are no impacts, whooshes, risers or "spiritual" sound effects. Guitar tuning was checked numerically
(within ±3 cents).

## Render

Requirements are Python 3.10+ and the packages below. ffmpeg comes with `imageio-ffmpeg`.

```sh
pip install pillow numpy scipy imageio-ffmpeg soundfile pyloudnorm
python render.py                      # all deliverables into out/ (~15–20 min on CPU)
python render.py --frames 0,450,840   # QA: single frames (plain + captioned) as PNG
python render.py --sheet-only         # contact sheet + SRT only
```

Optional regeneration steps:

```sh
python audio/compose_music.py                      # rebuild the music bed
pip install kokoro-onnx                            # narration: download the two model files listed in
python audio/make_vo.py <dir-with-model-files>     #   audio/make_vo.py, then regenerate audio/vo/*.wav
python tools/extract_standins.py <screenshot.pdf>  # recreate stand-ins (needs poppler pdfimages)
```

Frame n is shown at n/30 s and is computed from that time alone, so renders are deterministic.

## Project layout

```
config.json            copy, dates, colours, fonts, assets, panels, shot timings, text cues, narration, captions
render.py              compositor, layout check, audio mix, encoding, SRT, contact sheet
audio/compose_music.py original music bed  → audio/music.wav
audio/make_vo.py       local TTS narration → audio/vo/*.wav
tools/extract_standins.py
assets/standin/        photos and emblem cut from the supplied screenshot
assets/originals/      put the original website files here (empty)
assets/fonts/          Goudy Bookletter 1911, ABeeZee, Asul (SIL OFL 1.1, licences alongside)
out/                   rendered deliverables
```

## Attribution

- Photographs and emblem: © Tribu del Alma, taken from the brand's own website as captured in the supplied
  screenshot. The original URLs are listed in `config.json → assets`. They are used for Tribu del Alma's own promotion.
- Fonts: Goudy Bookletter 1911 (Barry Schwartz), ABeeZee (The ABeeZee Project Authors) and Asul (Mariela Monsalve),
  all under the SIL Open Font License 1.1 and obtained from the @fontsource npm packages.
- Narration: Kokoro-82M (hexgrad, Apache-2.0) via kokoro-onnx (MIT).
- Music: original, created in this project.
- Brand colours as supplied in the brief: cream #F0EEE2, sage #5A8073, muted gold #B3AE86, rust #9B4B01 and
  deep green #243F36.
