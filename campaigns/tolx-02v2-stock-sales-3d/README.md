# TOLX video 02 v2: "Stock & sales" in the 3D-scene style (31.6 s, 9:16)

The first full video in the new visual style the client asked for (reference: Odoo's own marketing, with 3D-rendered
real-world scenes, white app tiles and hand-drawn highlight doodles on top). It replaces the text-heavy cards of v1
with **moving scenes, one idea per shot and 2–3 words on screen**. Topic, fonts, Gia's voice, the calm music,
the "Tol-x" brand line and the end card are unchanged.

## Deliverable
`deliverables/TOLX_02v2_stock-sales-3d_9x16.mp4`: 1080×1920, 30 fps, 948 frames, 31.6 s, H.264 + AAC, about -14.3 LUFS. Instagram Reels / Stories and
LinkedIn vertical. A 4:5 feed version would need the graphics re-laid out for the crop, so it isn't made yet.

## Shots

| # | Time | 3D scene (AI-generated) | Graphics on top | Gia |
|---|---|---|---|---|
| 1 | 0–3.6 s | Camera glides past dark shelves of boxes | Sheet tile, **Excel says 12** | Your spreadsheet says twelve in stock… |
| 2 | 3.6–6.6 s | Push-in on three boxes under a spotlight | Gold sparks, box tile with red **3**, **Shelf: 3** | But the shelf? Only three! |
| 3 | 6.6–10.6 s | Night desk: laptop, scattered papers, lamp | Five file tiles pop in with 12 / 9 / 7 / 10 / 3, jiggling, **Which file?** | Five files, five numbers. Which one is right? |
| 4 | 10.6–14.4 s | Box on a counter by card terminals, orbit | Sale tile, then gold arrow, then stock tile 6 → 4, **Stock updated** | With one system, every sale updates your stock. |
| 5 | 14.4–19.2 s | Warehouse aisle, dolly forward | Shop, warehouse and phone tiles all at **4**, gold link line, **Same number** | Shop, warehouse, your phone. Same number, everywhere! |
| 6 | 19.2–22.8 s | Tilt up to the lone box on the top shelf | Bell alert tile, gold arrow to the box, **Reorder in time** | Running low? You're alerted before you run out. |
| 7 | 22.8–27 s | Tidy shop at closing, pull-back | **Odoo logo** tile (official Odoo Ready Partner artwork) and Custom tile glide together, **Built around you** | Odoo, or software built around your business. |
| 8 | 27–31.6 s | Blurred, darkened last scene | Standard end card: discovery call, tolx.ae/contact, WhatsApp, Odoo Ready Partner badge | Book your discovery call with Tol-x today! |

## How it's built
- **Footage:** 7 × 5 s Kling 3.0 clips (pro, silent), photoreal CGI prompts with *no text, logos or people*. Clips 1–2 come
  from the approved style test. Prompts are in the git log and in the Higgsfield history. Cost: 7.5 credits per clip.
- **Overlay:** `../tolx-kit/tolx_overlay.py` provides grading, vignette, zoom-blur cuts, drawn-on doodles (sparks, curved
  arrows; the scribble circle was removed at client request), springy app tiles with gold/dark icons, and baseline-aligned kinetic keywords. `compose.py` holds the
  per-shot overlays. `timeline.py` holds the shot lengths, set from the measured voice takes.
- **Audio:** `audio/compose_audio.py` builds the smooth bed, a soft whoosh into every cut, small chimes for the tiles,
  and Gia's lines (`vo_lines/g0–g7`, 1.06× energetic read). The brand is spoken "Tol-x" (prompt "Tolex").

```bash
python audio/compose_audio.py
python compose.py --out deliverables/TOLX_02v2_stock-sales-3d_9x16.mp4 --vo audio/vo_gia.wav --music audio/music.wav --sfx audio/sfx.wav
python compose.py --frames 83,185,305      # stills to .work/ for checking overlay positions
```

## Guardrails
- **No on-screen AI footnote** (client decision, 4 Oct 2026). The footage is still AI-generated: Instagram/Meta and other
  platforms may apply their own "AI info" label, and the post caption can disclose it. Products, numbers and the shop
  are invented. No client, no prices, no savings. The features shown (stock updated by sales, one shared figure, low-stock
  alerts) are generic inventory functions in Odoo and similar systems.
- **Where Odoo is named, its logo is shown** (client decision). The official Odoo Ready Partner artwork from the TOLX theme
  (`assets/odoo_ready_partners_rgb.png`) appears unchanged, apart from proportional resizing, on a white tile in shot 7 and on the
  end card. The other icons are TOLX-drawn.
- The voice is synthetic (Higgsfield TTS, ElevenLabs preset Gia), so don't present it as a human recording.

## Post copy
Use the same as v1 (`../tolx-02-stock-sales/README.md`), with the UTM `utm_content=video02v2`.

## Checks performed
- Rendered end to end. Decoding confirmed 948 frames, 31.6 s, 1080×1920, with an AAC track. About -14.3 LUFS.
- Before the final render I inspected stills from every shot. That led to three fixes: a keyword too wide for the screen,
  overlapping tiles, and the reorder arrow re-aimed at the lone box.
- Frames decoded at each cut confirm the zoom-blur crossfades and that the graphics clear before each cut.
- VO placement: all 8 lines at 1.06×, no overlaps.
- **Not done:** human playback and listening review, and test uploads.

## v3 changes (client feedback)
- Removed the yellow scribble circle in shot 1.
- Removed the on-screen "AI-generated visuals" footnote.
- Shot 7 now shows the Odoo logo (official partner artwork) on the Odoo tile instead of a generic glyph.
