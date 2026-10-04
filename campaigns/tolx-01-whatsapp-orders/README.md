# TOLX video 01: "WhatsApp orders without losing track" (30 s)

The first video in the TOLX content series. It goes with the first guide the website
update plans: **"How to manage WhatsApp orders without losing track."** It follows one
order from a busy team group chat into a simple four-step workflow (log, assign, track,
follow up), then points to the guide.

Audience: UAE shop, kiosk, service and trading-company owners whose orders live in
WhatsApp groups, Excel and staff memory. Most of them have never searched for "ERP".

## Deliverables (`deliverables/`)

| File | Use |
|---|---|
| `TOLX_01_whatsapp-orders_reel_9x16_vo-gia.mp4` / `_vo-marcus.mp4` | **With voiceover** (female Gia / male Marcus). Instagram Reels / Stories, LinkedIn vertical. 1080×1920 |
| `TOLX_01_whatsapp-orders_feed_4x5_vo-gia.mp4` / `_vo-marcus.mp4` | **With voiceover.** LinkedIn feed, Instagram feed. 1080×1350 |
| `TOLX_01_whatsapp-orders_reel_9x16.mp4`, `..._feed_4x5.mp4` | Music-only versions (no narration) |
| `captions_vo-gia.srt`, `captions_vo-marcus.srt` | Spoken-line captions matching each voiceover version |
| `cover_reel.png`, `cover_feed.png` | Cover / thumbnail ("Buried in the group chat.") |
| `captions.srt` | On-screen copy as a caption file, for the music-only versions |
| `storyboard_*.png` | Contact sheets showing 10 key frames |

Both files: H.264 + AAC, 30 fps, 900 frames, 30.0 s, about -14 LUFS integrated.

## Storyboard

| Time | Scene | On screen |
|---|---|---|
| 0–3.8 s | Hook | "Taking orders on WhatsApp?" A "Shop Team" group chat fills up |
| 3.8–6.7 s | The order | "Here's the order. Now find it." The order message is highlighted, then buried by 18 more messages |
| 6.7–9 s | Pain | "Buried in the group chat." *Who's handling it? Was it confirmed? Did anyone follow up?* |
| 9–11.5 s | Turn | "Give every order a place to live." The chat scrolls back and the order lifts out as a card |
| 11.5–14.3 s | 1 Log it | The order card fills in: customer, items, delivery |
| 14.3–17 s | 2 Assign it | Owner: Sara. Status: NEW. Next step: confirm stock and time |
| 17–20.5 s | 3 Track it | The card moves across a board: New → Confirmed → Delivered |
| 20.5–23 s | 4 Follow up | Reminder: "Sat 10:00 · Sara: call Khalid, happy with the order? Ask about a reorder." |
| 23–26 s | Statement | "Every order gets an owner, a status and a next step." Not every shop needs a full ERP |
| 26–30 s | End card | TOLX helm + wordmark, "Free guide: How to manage WhatsApp orders without losing track", `tolx.ae/blog` |

### Honesty guardrails built into the video
- An "ILLUSTRATIVE WORKFLOW" chip and the footnote "Illustrative scenario. Not a client project." stay on screen.
- Names, orders and the shop are invented. No client logos, results, savings or testimonials appear.
- The order is *recorded* in a shared list ("Log it"). Nothing claims an automatic or native WhatsApp integration.
  The chat UI is generic, with no WhatsApp logo, colours or trade dress. "WhatsApp" appears only as a descriptive word.
- No product is named. The video says the right tool depends on workflow and budget.

## Before you post: check these
1. **CTA URL.** The end card says `tolx.ae/blog` because the guide isn't published yet. Once it's live,
   set `CTA_URL` in `compose_tolx.py` to the article URL (keep it short) and re-render.
   Until then, post the article link in the first comment / bio link.
2. **Campaign tags.** Use UTM-tagged links in captions/bio so the website's attribution capture can credit the video:
   - LinkedIn: `https://tolx.ae/blog/?utm_source=linkedin&utm_medium=social&utm_campaign=whatsapp-orders&utm_content=video01`
   - Instagram: `https://tolx.ae/blog/?utm_source=instagram&utm_medium=social&utm_campaign=whatsapp-orders&utm_content=video01`
3. Upload the matching `captions_vo-*.srt` (or `captions.srt` for music-only) on LinkedIn. On Instagram, the copy is already on screen.
4. Watch it once with sound on a phone before posting. Nobody has done a human playback review yet.

## Post copy

**LinkedIn**
> Most small businesses in the UAE don't lose orders because they're careless. They lose them because the order is message #47 in a busy team group.
>
> A simple fix, with or without new software:
> 1. Log it: every order goes into one shared list, not only the chat
> 2. Assign it: one person owns it
> 3. Track it: everyone can see the status without asking
> 4. Follow up: the next step has a name and a date
>
> The right tool depends on your workflow and budget. Sometimes that's a well-built shared sheet, sometimes a proper system.
>
> We wrote a practical guide: How to manage WhatsApp orders without losing track → [link]
>
> (The video shows an illustrative workflow, not a client project.)
>
> #SmallBusinessUAE #DubaiBusiness #SME #Operations #CustomerService

**Instagram**
> Taking orders on WhatsApp? Here's how to stop them getting buried in the group chat 👇
>
> 1️⃣ Log every order in one shared list
> 2️⃣ Give it one owner
> 3️⃣ Track the status where everyone can see it
> 4️⃣ Set a follow-up with a name and a date
>
> Free guide → link in bio
> Illustrative workflow, not a client project.
>
> #DubaiSmallBusiness #UAEbusiness #SmallBusinessTips #ShopOwner #DubaiShops #BusinessSystems #TOLX

## Voiceover
Synthetic speech: Higgsfield Text to Speech V2 (ElevenLabs engine), preset voices **Gia** (female)
and **Marcus** (male). It is generated, not a human recording, so don't describe it as a voice actor.
Each line is a separate take in `audio/vo_lines/` (`f*` = Gia, `m*` = Marcus, numbered by line).
`audio/place_vo.py` trims each take and shortens long pauses. Where a line runs past its scene,
the script speeds it up by at most 1.15× (pitch kept). It then places the line on its scene and writes
`audio/vo_<voice>.wav` + `.srt`. In the mix, the voice is loudness-matched (-16 LUFS stem), and music and
SFX are lowered and side-chain ducked. Stem measurement put the voice about 10–20 dB above the music
on every line, for both voices.

| # | Time | Line |
|---|---|---|
| 1 | 0.4 s | Taking orders on WhatsApp? |
| 2 | 3.9 s | Here's the order. Now… find it. |
| 3 | 6.8 s | Who's handling it? Did anyone follow up? |
| 4 | 9.4 s | Give every order a place to live. |
| 5 | 11.6 s | One: log it in one shared list. |
| 6 | 14.4 s | Two: assign it to one person. |
| 7 | 17.1 s | Three: track the status, so nobody has to ask. |
| 8 | 20.6 s | Four: follow up, with a name and a date. |
| 9 | 23.3 s | Every order gets an owner, a status, and a next step. |
| 10 | 26.8 s | Read the free guide on our blog. |

The narration never says "TOLX" because the intended pronunciation isn't confirmed. The logo and URL are on screen.
To change a line: regenerate that take into `audio/vo_lines/`, run `place_vo.py`, then remux (no picture re-render):

```bash
python audio/place_vo.py f vo_gia.wav          # or: m vo_marcus.wav
python compose_tolx.py --format reel --out .work/silent_reel.mp4          # once per format (silent master)
python compose_tolx.py --format reel --video-in .work/silent_reel.mp4 --vo audio/vo_gia.wav \
  --music audio/music.wav --sfx audio/sfx.wav --out deliverables/TOLX_01_whatsapp-orders_reel_9x16_vo-gia.mp4
```

## Render

```bash
python -m pip install pillow imageio-ffmpeg numpy scipy
python audio/compose_audio.py audio          # music.wav + sfx.wav (only if timing/score changed)
python compose_tolx.py --format reel --out deliverables/TOLX_01_whatsapp-orders_reel_9x16.mp4 \
  --music audio/music.wav --sfx audio/sfx.wav --srt deliverables/captions.srt \
  --storyboard deliverables/storyboard_reel.png --cover deliverables/cover_reel.png
python compose_tolx.py --format feed --out deliverables/TOLX_01_whatsapp-orders_feed_4x5.mp4 \
  --music audio/music.wav --sfx audio/sfx.wav \
  --storyboard deliverables/storyboard_feed.png --cover deliverables/cover_feed.png
# quick look at single frames: --frames 60,320,600 --out .work/check  (add --size 540 for fast review encodes)
```

- `timeline.py` holds every scene and event frame. Picture and sound both import it, so retiming happens in one place.
- Layout is designed on a 1080×1350 stage. In the reel version the stage sits at y=250 so text clears the Instagram/LinkedIn UI.
  `check_layout()` fails the build if any text leaves the safe box.
- The brand follows the TOLX theme. The helm is redrawn from the SVG in `partials/helm.php`, gold `#D4A843` on `#09090B`.
  Fonts are Poppins (headlines, as on the social card), Chakra Petch (UI, the site font) and Share Tech Mono (labels).
  They are bundled in `fonts/` under the SIL OFL.
- Music and SFX are composed in code (`audio/compose_audio.py`), so no third-party licence applies.

## Matching article brief: "How to manage WhatsApp orders without losing track"

Publish it as a normal WordPress post. Don't put it in a theme template. This title has **no verified search volume**.
Check UAE keyword data before you put ad spend behind it.

- **Reader:** owner or manager of a UAE shop, kiosk, service or trading business that takes orders through WhatsApp chats and staff groups.
- **Promise:** a practical way to stop orders getting lost, which works with a shared sheet today and grows into proper software when needed.
- **Outline:**
  1. Why orders get lost in chat: buried messages, no owner, no status, follow-ups held in someone's memory.
  2. The minimum record for every order: customer, items, delivery/date, owner, status, next step.
  3. The four-step routine (log, assign, track, follow up), with an example day in a kiosk, a service company and a trading firm. Label every example as illustrative.
  4. Simple setups by size: a shared sheet with clear columns, then a simple order/CRM tool, then an integrated system with stock and invoicing. Say when each is enough.
  5. Signs you've outgrown the spreadsheet: stock disagreements, double bookings, nobody knowing which orders are open.
  6. What to check before you buy software: workflow fit, who will use it daily, budget, support, and what WhatsApp connection is actually available. Don't promise integrations.
  7. Downloadable/printable checklist (only if one is actually provided).
- **Internal links:** the order tracking & customer follow-up service page, the Operations Opportunity Finder, and the Odoo guide as one option.
- **CTA:** "Talk through your order workflow" (contact) or take the assessment.
- **Avoid:** invented statistics, savings figures, client results, and "#1 in Dubai" claims.
- **Video:** embed this video near the top and link the post back from the video captions.

## Checks performed
- Rendered both formats end to end. ffprobe/ffmpeg decoding confirmed 900 frames, 30.0 s, H.264 + AAC at 1080×1920 and 1080×1350.
- Loudness measured with ffmpeg ebur128: about -13.6 LUFS integrated, peak about -2 dBFS.
- Inspected frames decoded from the MP4s, not only source renders. Contact sheets of in-between frames covered the lift-out and board transitions.
- `check_layout()` checked every 5th frame for text inside the safe area. It passes for both formats.
- Voiceover: placement log checked (no overlapping lines, max speed-up 1.15×). Voice-to-music ratio measured on
  separately rendered stems through the same filter chain. Final mixes measured at -14.2 / -14.9 LUFS.
- **Not done:** human listening review of the synthetic voices (pronunciation, naturalness, which voice fits TOLX better), upload tests on LinkedIn/Instagram, and checking how each app crops the cover.
