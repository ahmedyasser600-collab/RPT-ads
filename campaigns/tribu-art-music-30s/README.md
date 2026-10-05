# Tribu del Alma — Art & Music Retreat · 30 s vertical reel

The reel follows the hook "That creative project you keep postponing." It turns that recognition into an
invitation to ask about joining. It is 1080 × 1920, 30 fps, 30.0 s, H.264 High, yuv420p, AAC 48 kHz, and is built
for Instagram Reels.

**This version uses no photographs.** At the client's request the stand-in photos were removed until good
photography is supplied. Each beat is a brand-colour field with a simple line drawing that draws itself.
The section *Photos wanted* below lists the shots that would replace or join these drawings.

## Deliverables (`out/`)

| File | What it is |
|---|---|
| `tribu-art-music-30s.mp4` | **Main video.** Designed text, narration and music |
| `tribu-art-music-30s-captioned.mp4` | Same video with burned-in narration captions |
| `tribu-art-music-30s-music-only.mp4` | Designed text and music, no narration. Use it as the base if a host records the voiceover |
| `tribu-art-music-30s.srt` | Narration captions. Upload them with the main video, or keep them for accessibility |
| `contact-sheet.png` | Six frames, one per storyboard beat |

## Storyboard as built

| Time | Beat | Picture | On-screen text | Narration |
|---|---|---|---|---|
| 0–4 s | Recognition | Cream. A rust dry-brush stroke moves across, then stops unfinished | **That project you / keep postponing?** (readable on frame 0; a gold rule draws in) | "That creative project you keep postponing." |
| 4–8 s | Possibility | Deep green opens from the centre like doors. Gold hill lines draw in, and the land fills in softly | GAUCÍN · ANDALUSIA / **Make room for it.** | "What if you gave it a week?" |
| 8–13 s | Creative freedom | Cream. A paint stroke, then a looping hand, then a sound wave, each on its word | **Paint.  Write.** / **Make music.** (word by word, on the spoken cues) | "The painting, … the story, … the song." |
| 13–18 s | Connection | Sage. A cream wave keeps its own rhythm; a green wave arrives out of step, then falls into step with it | **Your own rhythm.** / **Shared moments.** | "At Tribu del Alma, there's space to follow your own rhythm, create alongside others," |
| 18–24 s | The experience | Cream. An open arch fills with a warm wash. A horizon line, then a low sun rising | **Space to create.** → **Time to simply be.** | "…and enjoy the quieter moments in between." |
| 24–30 s | Invitation | End card: emblem, title, dates, place, CTA, website, a small gold hill line | Art & Music Retreat · 19–25 October · Gaucín, Andalusia · **Ask us about joining** · tribudelalma.com | "Join our Art and Music Retreat in Andalusia, nineteenth to twenty-fifth October. Ask us about joining." |

Scene changes are a soft colour wipe rising from the bottom, except the "doors" opening at 4 s. The CTA is on
screen from 25.8 s to 30 s (4.2 s).

Essential text stays inside x 100–900 and y 250–1500. `render.py` runs `check_layout()` and fails the build if:
- text leaves that area
- a block has more than two lines
- a caption overlaps designed text
- the CTA is shown for less than 4 s

Centred elements are centred on the safe area (x = 500), not on the frame, so they clear Instagram's
right-hand buttons.

## ⚠️ Items needing owner confirmation

1. **Dates.** On screen it reads "19–25 October"; the narration says "nineteenth to twenty-fifth October".
   Year 2026 is the working campaign year. The dates come from the campaign brief and the sprint document;
   the owner has not confirmed them. Edit `event` in `config.json` and re-render. If the spoken date changes,
   re-run `audio/make_vo.py`.
2. **The logo is a stand-in.** `tribudelalma.com` was blocked in the render environment, so the original
   transparent logo PNG could not be downloaded. The end card uses the round emblem cut pixel for pixel from the
   supplied website screenshot. It is about 118 px, shown at 196 px, so it is slightly soft. It also has a typeset
   "TRIBU DEL ALMA" label in Asul; this is a label, not a reconstruction of the logo. Put the original at
   `assets/originals/tribu-del-alma-logo.final_.png` and the renderer uses it, scaled proportionally only,
   and drops the label.
3. **The voice is synthetic.** See *Voiceover*. Please listen before publishing. I could not audition audio in
   the render environment, so the mix was checked by measurement.
4. **Music licence.** See *Music*. The credit lines must go in the post caption.
5. Not included, as instructed: prices, remaining places, discounts, testimonials, booking deadlines and any
   claims about healing or transformation.

## Music

**"The Hero's Journey" by Audio Library Beats Group**, supplied by the client
(`assets/music/the-heros-journey-audio-library.mp3`). The edit uses the track's opening, 0:00–0:30, unchanged
except for a 2 s fade-out at the end. Its quiet intro sits under the hook. The orchestral swell grows from about
20 s and peaks under the invitation. The music stays under the narration and ducks 5 dB while she speaks.

Put this credit in the Instagram caption (it is also stored in `config.json → audio.music_credit`):

```
Music: The Hero's Journey by Audio Library Beats Group
Free Download / Stream: https://links.al/qTd
Music promoted by Audio Library: https://links.al/youtube
```

The file's metadata says "all-rights-reserved", and Audio Library's free licence is written mainly with YouTube
in mind. Before running this as a paid ad, confirm that their terms cover promotional use on Instagram.

## Voiceover

- **Engine:** Kokoro-82M v1.0 (Apache-2.0) via `kokoro-onnx` (MIT), preset voice `af_heart`, speed 0.94.
  It runs locally on CPU with no account, API or paid service. It is a stock synthetic voice. It does not clone or
  imitate any real person, and it must not be described as a host recording.
- "Tribu del Alma" is forced to Spanish pronunciation ("TREE-boo del AHL-ma") through a phoneme override.
- **Script change:** the brief's sentences 2 and 3 are swapped so the narration matches the storyboard. Every word
  is kept, and nothing is sped up: there is 20.1 s of speech in the 30 s film.
- Mix, measured on the final MP4:
  - narrated passages are about −13 LUFS
  - music in the pauses is about −25 LUFS, rising to about −20 LUFS as the swell arrives
  - integrated −13.8 LUFS; true peak −1.4 dBFS, so nothing clips

### Timed narration script (for a host recording)

Record it as one relaxed take; the edit will be re-timed to it. To replace the voice, swap `audio/vo/*.wav`.
Clip names and start times are in `config.json → voiceover.clips`.

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

## Photos wanted

Real photos of the place and the people will make this far stronger than drawings or generated images. Ideal
specs: vertical 9:16 (or a frame that crops cleanly to it), at least 1080 × 1920 (2160 × 3840 is better), natural
light, warm and unposed, no heavy filters. Leave room near the bottom third for text.

| Beat | Shot |
|---|---|
| 0–4 s Hook | Close-up of an **unfinished** piece: a half-painted canvas on an easel, an open notebook with a pen resting on it, or a guitar leaning on a chair. No face needed |
| 4–8 s Possibility | **Finca Pura Vida and the Gaucín hills**, wide, early morning or golden hour. Ideally a slow 4–5 s handheld or tripod clip |
| 8–13 s Paint | Hands painting at an outdoor table: brush, palette, colour on paper |
| 8–13 s Write | Someone writing in a notebook in the shade, on the terrace or under a tree |
| 8–13 s Make music | Hands on a guitar or another instrument, close |
| 13–18 s Connection | The group on the terrace: music, laughter, a shared moment. Several people, natural and candid |
| 18–24 s Space to create | The creative space or studio corner, uncluttered, with materials laid out |
| 18–24 s Time to simply be | A quiet moment: a bedroom with morning light, a hammock, a view from the terrace, or tea at a table |
| 24–30 s End card | A calm landscape or a detail of the finca to sit behind or above the logo |

Also needed: the original **transparent logo PNG**, and permission from everyone who is recognisable.

**About generating these with AI:** the safe use is for close, non-identifying details, such as hands with a
brush, a notebook, a guitar neck or a palette. Do not generate the finca, the landscape or "participants", and do
not present generated images as the real venue or real guests. People booking a retreat will reasonably take
those images as what they are buying. If any generated image is used, keep it to details, and consider a small
"illustrative image" note.

## Render

You need Python 3.10+ and the packages below. ffmpeg comes with `imageio-ffmpeg`.

```sh
pip install pillow numpy scipy imageio-ffmpeg soundfile pyloudnorm
python render.py                      # all deliverables into out/ (~2–3 min on CPU)
python render.py --frames 0,450,840   # QA: single frames (plain + captioned) as PNG
python render.py --sheet-only         # contact sheet + SRT only
```

Optional:

```sh
pip install kokoro-onnx                            # narration: download the two model files listed in
python audio/make_vo.py <dir-with-model-files>     #   audio/make_vo.py, then regenerate audio/vo/*.wav
python tools/extract_standins.py <screenshot.pdf>  # recreate the stand-in emblem (needs poppler)
```

Frame n is shown at n/30 s and is computed from that time alone, so renders are deterministic.

## Project layout

```
config.json            copy, dates, colours, fonts, logo, scenes, text cues, narration, captions, music
render.py              backgrounds and line drawings, text, end card, layout check, audio mix, encoding
audio/make_vo.py       local TTS narration → audio/vo/*.wav
assets/music/          the supplied track
assets/standin/        emblem cut from the supplied screenshot
assets/originals/      put the original logo here (empty)
assets/fonts/          Goudy Bookletter 1911, ABeeZee, Asul (SIL OFL 1.1, licences alongside)
tools/extract_standins.py
out/                   rendered deliverables
```

## Attribution

- Music: "The Hero's Journey" by Audio Library Beats Group (credit lines above).
- Logo emblem: © Tribu del Alma, from the brand's website as captured in the supplied screenshot.
- Fonts: Goudy Bookletter 1911 (Barry Schwartz), ABeeZee (The ABeeZee Project Authors) and Asul (Mariela Monsalve),
  all under the SIL Open Font License 1.1 and obtained from the @fontsource npm packages.
- Narration: Kokoro-82M (hexgrad, Apache-2.0) via kokoro-onnx (MIT).
- Line drawings: created in code for this project.
- Brand colours as supplied in the brief: cream #F0EEE2, sage #5A8073, muted gold #B3AE86, rust #9B4B01 and
  deep green #243F36.
