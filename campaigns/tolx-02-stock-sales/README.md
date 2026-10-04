# TOLX video 02: "When Excel stops working" (stock & sales, 34 s)

Goal: **generate leads.** The video names a familiar problem (the stock spreadsheet doesn't match the
shelf, and nobody knows which file is right). It then shows the alternative, one system with one stock number,
and ends on a direct offer: Odoo, or custom software built around the business, plus a discovery-call CTA.

## Deliverables (`deliverables/`)

| File | Use |
|---|---|
| `TOLX_02_stock-sales_reel_9x16.mp4` | Instagram Reels / Stories, LinkedIn vertical. 1080×1920, Marcus voiceover |
| `TOLX_02_stock-sales_feed_4x5.mp4` | LinkedIn feed, Instagram feed. 1080×1350, Marcus voiceover |
| `cover_reel.png`, `cover_feed.png` | Cover ("The shelf says 3.") |
| `captions.srt` | Spoken-line captions (upload on LinkedIn) |
| `captions_onscreen.srt` | On-screen copy as captions |
| `storyboard_*.png` | 11-frame contact sheets |

Both files: H.264 + AAC, 30 fps, 1030 frames, 34.3 s, about -14.6 LUFS.

## Storyboard and voiceover (Marcus)

| Time | On screen | Voiceover |
|---|---|---|
| 0–3.3 s | "Your spreadsheet says 12." Stock sheet, the 12 is highlighted | Your spreadsheet says twelve in stock. |
| 3.3–5 s | "The shelf says 3." Shelf with 3 boxes, the cell turns red | The shelf says three. |
| 5–6.7 s | "Which file is right?" Five file versions, five different numbers | Which file is right? |
| 6.7–9.5 s | "Five files. Five numbers." *Who updated it last? What sold today? When do we reorder?* | Who sold what? When do we reorder? |
| 9.5–12.2 s | "One system. One number." Files collapse into one product record | Move to one system, with one number. |
| 12.2–15.5 s | **1 Sell.** Sale #2201 drops in, on hand 6 → 4 | Make a sale, and stock updates once. |
| 15.5–19.8 s | **2 Same number.** Shop, warehouse and owner's phone all show 4 | The shop, the warehouse and your phone all see the same number. |
| 19.8–23.2 s | **3 Reorder in time.** Low-stock alert, then draft purchase order #0318 | Running low? It tells you before you run out. |
| 23.2–26 s | **4 See the day.** Sales today, low-stock items, top seller, sales by hour | And you see the whole day at a glance. |
| 26–30.3 s | "Ready to move beyond Excel?" **Odoo** or **Custom software**, sized to your workflow and budget | Move beyond Excel, with Odoo, or software built around your business. |
| 30.3–34.3 s | End card: TOLX, "Book a 30-minute discovery call", `tolx.ae/contact`, WhatsApp +971 50 986 0063 | Book your discovery call today. |

### Guardrails
- An "ILLUSTRATIVE WORKFLOW" chip and the footnote "Illustrative scenario. Not a client project." stay on screen.
  Products, quantities and order numbers are invented. There are no prices, savings or client names.
- The features shown are generic inventory functions found in Odoo and similar systems: stock updated at sale,
  one shared stock record, a minimum-stock flag with a *draft* purchase order, and a daily summary. The video does not claim POS hardware,
  integrations or a specific delivered project.
- The voice is synthetic (Higgsfield TTS V2, ElevenLabs engine, preset voice "Marcus"), so don't present it as a human recording.
- "30-minute discovery call" follows the site's own wording ("usually 30 minutes for an initial call").
  The video doesn't say "free". If the call is free, change `CALL_LENGTH`/end-card copy in `../tolx-kit/tolx_kit.py`.

## Post copy (lead-focused)

Use UTM-tagged links so enquiries can be attributed:
`https://tolx.ae/contact/?utm_source=linkedin&utm_medium=social&utm_campaign=stock-sales&utm_content=video02`
(swap `linkedin` → `instagram` for Instagram).

**LinkedIn**
> If your stock lives in "Stock_FINAL_v7.xlsx", you already know the problem: the file says 12, the shelf says 3, and nobody is sure which version is right.
>
> One system fixes that:
> • a sale updates stock once, at the moment it happens
> • the shop, warehouse and owner see the same number
> • low stock is flagged before you run out
> • you can see the day at a glance
>
> At TOLX we set up Odoo, or build custom software around exactly how your business works, sized to your workflow and budget.
>
> Book a 30-minute discovery call → [UTM link]  ·  or WhatsApp +971 50 986 0063
>
> (Illustrative workflow in the video, not a client project.)
>
> #SmallBusinessUAE #InventoryManagement #Odoo #DubaiBusiness #Retail #SME

**Instagram**
> Your spreadsheet says 12. The shelf says 3. 😬
>
> Move to one system with one number:
> ✅ sales update stock instantly
> ✅ shop, warehouse and owner see the same figure
> ✅ low-stock alerts before you run out
>
> Odoo or custom software, built around your business.
> 📞 Book a 30-min discovery call: link in bio, or WhatsApp +971 50 986 0063
> Illustrative workflow, not a client project.
>
> #DubaiSmallBusiness #UAEbusiness #ShopOwner #InventoryManagement #Odoo #TOLX

## Render

```bash
python -m pip install pillow imageio-ffmpeg numpy scipy
python audio/compose_audio.py                       # music.wav, sfx.wav, vo_marcus.wav (+ .srt)
python compose_02.py --format reel --out .work/silent_reel.mp4 --storyboard deliverables/storyboard_reel.png \
  --cover deliverables/cover_reel.png --srt deliverables/captions_onscreen.srt
python compose_02.py --format reel --video-in .work/silent_reel.mp4 --vo audio/vo_marcus.wav \
  --music audio/music.wav --sfx audio/sfx.wav --out deliverables/TOLX_02_stock-sales_reel_9x16.mp4
# same two steps with --format feed -> ..._feed_4x5.mp4
```
Shared brand, layout, end card and mix settings live in `../tolx-kit/` (see its README).

## Checks performed
- Both formats rendered end to end. Decoding confirmed 1030 frames, 34.3 s, 1080×1920 and 1080×1350, with an AAC track.
- Loudness measured with ffmpeg ebur128 at about -14.6 LUFS integrated.
- Inspected frames decoded from the MP4 (hook, step 1, step 3, end card) and an in-between strip of the sale-ticket transition.
  That inspection led to two fixes: an overflowing label and a ticket overlapping text.
- `check_layout()` passes for every 5th frame in both formats.
- VO placement log shows no overlaps. The largest speed-up is 1.03×.
- **Not done:** human listening review, test uploads to LinkedIn/Instagram, and cover-crop checks in each app.
