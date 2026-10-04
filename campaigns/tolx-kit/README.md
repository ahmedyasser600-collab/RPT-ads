# TOLX video kit

Shared code for the TOLX LinkedIn / Instagram series (videos 02 onward; video 01 keeps its own copy
of the same code). It keeps every video on one brand, one layout and one lead CTA.

- `tolx_kit.py`: brand tokens and fonts, the helm logo (redrawn from the theme's `partials/helm.php`),
  sprites and motion helpers, the 1080×1350 stage (feed 4:5, or placed at y=250 in a 9:16 reel), headlines and the
  4-step progress rail. It also holds the **"Ready to move beyond …?" Odoo / Custom software statement**, the
  **discovery-call end card**, layout safety checks, SRT writing, storyboard sheets and the voice-ducked audio mix.
- `tolx_audio.py`: code-composed score (problem → lift → workflow groove → end chord), UI sound effects,
  and `place_vo()` for per-line voiceover takes (trim, tighten pauses, ≤1.15× speed-up, no overlaps, SRT).
- `fonts/`: Poppins, Chakra Petch, Share Tech Mono (SIL OFL, licences included).

Series rules baked in:
- **The goal is leads.** Every video ends with "Move beyond X, with Odoo or software built around your business",
  then "Book a 30-minute discovery call · tolx.ae/contact · WhatsApp +971 50 986 0063".
- **Series style (v2, from 4 Oct 2026 feedback):**
  - **Title:** heavy Poppins Black italic with a subtle gold extrusion, entering with a *smooth* staggered reveal
    (`reveal()` + `underline()`). **No slam, screen-shake or flash** (judged cringe).
  - **Music:** the calm, premium `build_music_smooth()` bed (breathing pads, soft sub, soft kick on 1 and 3, sparse keys).
    **No plucky 124 BPM groove.** Effects stay sparse and soft (`chime`, gentle `swish`), with no pop or tick clutter.
  - **Voice:** **Gia** (Higgsfield TTS V2, ElevenLabs preset), short punchy lines, `place_vo(..., base_tempo=1.06, fx=ENERGY_FX)`.
    Synthetic, so it's never presented as a human recording.
  - **Brand in the CTA (required):** the last line says "**Book your discovery call with TOLX today!**".
  - **Pronunciation: TOLX is said "Tol-x"**, chosen by the client from samples (`pronunciation/B_Tolex.mp3`). In TTS prompts always write `Tolex`
    (`tolx_audio.BRAND_SPOKEN`). On screen and in captions it stays "TOLX", and `place_vo` converts the SRT text automatically.
  - The older `extruded/slam/shake/flash` and `build_music()` helpers remain for reference only.
  - Videos 01–02 still use the earlier Marcus / calm treatment and don't say the brand yet.
- Scenarios are illustrative and labelled on screen. No invented client results, prices, savings or integrations.
- To change the CTA (for example, if the call is free) edit `CTA_URL`, `PHONE`, `CALL_LENGTH` and `draw_end_card()` here,
  then re-render each video.
