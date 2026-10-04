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
- **Voice:** Marcus (Higgsfield TTS V2, ElevenLabs engine). Synthetic, so it's never presented as a human recording.
  The narration doesn't say "TOLX" until the pronunciation is confirmed.
- Scenarios are illustrative and labelled on screen. No invented client results, prices, savings or integrations.
- To change the CTA (for example, if the call is free) edit `CTA_URL`, `PHONE`, `CALL_LENGTH` and `draw_end_card()` here,
  then re-render each video.
