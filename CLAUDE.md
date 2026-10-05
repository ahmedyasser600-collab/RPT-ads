# Repository notes

This repo holds two separate video projects: **RPT** (Italian bathroom-renovation reels: `reels/`, `campaigns/rpt-*`,
`assets/`) and **TOLX** (UAE business-systems social videos: `campaigns/tolx-*`). Keep them separate.

## TOLX website theme
- Source in `campaigns/tolx-site-theme/tolx/` (WordPress), packaged zips in `dist/`. Keep the brand (black + gold, Chakra Petch /
  Share Tech Mono). Site positioning: **Odoo partner, diplomatic**: lead with Odoo implemented around
  the client's business. Never headline "not Odoo-only" or push alternatives; at most a soft line that advice starts from the client's needs.

## TOLX videos (LinkedIn / Instagram)
- Shared code and the series rules live in `campaigns/tolx-kit/` (read its README before making a new video).
- **Brand pronunciation: TOLX is pronounced "Tol-x".** In any voiceover / TTS prompt write `Tolex`
  (client-approved sample: `campaigns/tolx-kit/pronunciation/B_Tolex.mp3`)
  (`tolx_audio.BRAND_SPOKEN`). On screen and in captions keep "TOLX".
- **Odoo pronunciation: "oh-DOO"** (Odoo's own team, Odoo forum). In TTS prompts write `Oh-doo` (`tolx_audio.ODOO_SPOKEN`);
  on screen and in captions keep "Odoo".
- Goal is leads: every video ends with a direct **"It's time to shift to Odoo"** pitch (client decision, 4 Oct 2026: don't
  offer "or software built around your business" for now), then "Book your discovery call with Tolex today!"
  and the end card (tolx.ae/contact, WhatsApp +971 50 986 0063).
- Current style: female voice Gia (Higgsfield TTS V2, ElevenLabs preset, energetic read), smooth title reveals
  (no slam/shake/flash), the calm `build_music_smooth()` bed, few soft sound effects.
- No invented client results, prices, savings or unverified integrations. Check dated facts (e.g. Odoo releases,
  UAE regulations) before each video.
- **Newest style (client-approved, video 02 v2): "3D scene + 2D overlay".** AI-generated photoreal CGI clips (Higgsfield
  Kling 3.0 pro, silent, 9:16, prompts with no text/logos/people) with `campaigns/tolx-kit/tolx_overlay.py` graphics:
  springy white app tiles, gold doodles (sparks, arrows), 2-3 word keywords, one idea per shot, ~3.5-4.5 s shots.
  - **No on-screen "AI-generated" footnote** (client decision). **No scribble circles** (client found them unclear).
  - **When Odoo is mentioned, show Odoo's logo**: use the official partner artwork from the TOLX theme
    (`odoo_ready_partners_rgb.png`), unchanged, on a white tile.
