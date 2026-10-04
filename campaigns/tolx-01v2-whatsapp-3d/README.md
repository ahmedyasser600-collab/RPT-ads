# TOLX video 01 v2: "WhatsApp orders" in the 3D-scene style (26.5 s, 9:16)

Second video in the client-approved "3D scene + 2D overlay" style (see `../tolx-02v2-stock-sales-3d/README.md`
and `CLAUDE.md`). One idea per shot, 2–3 words on screen, Gia voice, calm music, a direct **"Shift to Odoo now"**
pitch with the Odoo logo, and the standard discovery-call end card.

## Deliverable
`deliverables/TOLX_01v2_whatsapp-orders-3d_9x16.mp4`: 1080×1920, 30 fps, 796 frames, 26.5 s. Reels / Stories / LinkedIn vertical.

## Shots

| # | Time | 3D scene (AI-generated) | Graphics on top | Gia |
|---|---|---|---|---|
| 1 | 0–3.2 s | Phone glowing on a dark shop counter, push-in | Six gold chat tiles burst in around it, then a big chat tile **99+**, **On WhatsApp?** | Taking orders on WhatsApp? |
| 2 | 3.2–7.4 s | Phone on a stand on a cluttered packing table, orbit | Chat tiles stack on the phone screen and push the **NEW ORDER** tile down until it disappears, **Order buried** | Then somewhere in that chat, an order is getting buried. |
| 3 | 7.4–10.7 s | Back-room table of parcels, one lone parcel in a spotlight | Owner tile with grey **?**, **Who's on it?**, gold arrow down to the lone parcel | Who's handling it? Did anyone follow up? |
| 4 | 10.7–15.1 s | Open rear doors of a white van full of parcels, push-in | Status tiles NEW → CONFIRMED → DELIVERED with a gold line, OWNER tile, **Every order tracked** | In one system, every order gets an owner and a status. |
| 5 | 15.1–18.5 s | Tablet on a night desk with a warm lamp | Bell tile **CALL BACK · SAT 10:00** with gold sparks, **No missed follow-ups** | And every follow-up comes with a reminder. |
| 6 | 18.5–21.9 s | Organised dispatch room, parcels lined up, pull-back | **Odoo logo** tile (official partner artwork) with gold sparks, **Shift to Odoo** | It's time. Shift to Odoo now! |
| 7 | 21.9–26.5 s | Blurred, darkened last scene | End card: discovery call, tolx.ae/contact, WhatsApp, Odoo Ready Partner badge | Book your discovery call with Tol-x today! |

## Notes
- **Clips:** 6 × Kling 3.0 pro, silent, 9:16, plus one regeneration (the first van clip had an invented shop sign and a car-maker
  emblem, which broke the no-text/no-logos rule, so it was replaced by the rear-doors close-up). 52.5 credits in total.
- **Voice:** Gia lines `g0`–`g4` are new. `g5` ("It's time. Shift to Odoo now!") and `g6` (Tol-x CTA) are reused from video 02 v2.
- **Brand safety:** chat bubbles are TOLX gold (not WhatsApp green), with no WhatsApp logo. "WhatsApp" is only used as a word.
  The tablet's bit of garbled AI lettering is covered by the reminder tile.
- No on-screen AI footnote (client decision). Platforms may add their own AI label.
- Fixed in the kit usage: the compositor now passes this video's END_CARD/TOTAL to the shared end card. Before the fix
  the end card stayed blank because it was keyed to video 02's timing.

```bash
python audio/compose_audio.py
python compose.py --out deliverables/TOLX_01v2_whatsapp-orders-3d_9x16.mp4 --vo audio/vo_gia.wav --music audio/music.wav --sfx audio/sfx.wav
```
