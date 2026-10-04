"""TOLX video 02 v2 "Stock & sales" in the 3D-scene + 2D-overlay style (~31.6 s, 9:16).

Base: Kling 3.0 photoreal CGI clips (AI-generated; no text, logos or people in the footage).
Overlay (../tolx-kit/tolx_overlay.py): drawn-on gold doodles, springy app tiles, 2-4 word keywords.
Voice: Gia (energetic read), calm smooth music bed, soft accents. Ends on the standard discovery-call
end card with the Odoo Ready Partner badge. Frame n is shown at n/30 s.

Usage: python compose.py --out deliverables/X.mp4 --vo audio/vo_gia.wav --music audio/music.wav --sfx audio/sfx.wav
       python compose.py --frames 40,150,...      (writes .work/fNNN.png)
"""
import argparse
import math
import os
import subprocess
import sys
from functools import lru_cache

from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "tolx-kit"))
import tolx_kit as K  # noqa: E402
import tolx_overlay as O  # noqa: E402
from timeline import SHOTS, END_CARD, TOTAL, shot_at  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--out")
ap.add_argument("--vo")
ap.add_argument("--music")
ap.add_argument("--sfx")
ap.add_argument("--frames")
ARGS = ap.parse_args()

W, H = O.W, O.H
ease, lin = K.ease, K.lin
TEXT, GOLD, DOODLE, RED = K.TEXT, K.GOLD, O.DOODLE, (240, 96, 80)
GREEN = (80, 200, 120)
XFADE = 8
CLIPS = {}


# ---------------------------------------------------------------- per-shot overlays (i = frame within shot)
def ov_shelves(fr, i, out):
    O.draw_polyline(fr, CIRCLE, ease(lin(i, 10, 30)))
    O.put_tile(fr, 820, 520, i, 16, "sheet", out=out)
    O.keyword(fr, i, 26, (("Excel says ", TEXT), ("12", DOODLE)), 1380, out=out)


def ov_three(fr, i, out):
    for k, st in enumerate(SPARKS):
        O.draw_polyline(fr, st, ease(lin(i, 6 + 3 * k, 14 + 3 * k)), width=12)
    O.put_tile(fr, 800, 560, i, 12, "box", badge="3", out=out)
    O.keyword(fr, i, 16, (("Shelf: ", TEXT), ("3", RED)), 1400, out=out)


FILES = [("12", 260, 560, -8), ("9", 800, 520, 7), ("7", 210, 900, 6), ("10", 860, 880, -6), ("3", 530, 420, -3)]


def ov_files(fr, i, out):
    for k, (num, x, y, rot) in enumerate(FILES):
        jig = 4 * math.sin(i / 2.3 + k) if i > 40 else 0            # nervous jiggle once all are in
        O.put_tile(fr, x + jig, y, i, 8 + 7 * k, "sheet", rot=rot, badge=num, size=180, out=out)
    O.keyword(fr, i, 46, (("Which ", TEXT), ("file?", DOODLE)), 1400, out=out)


def ov_sale(fr, i, out):
    O.put_tile(fr, 290, 600, i, 8, "receipt", label="SALE  2 PCS", out=out)
    O.draw_polyline(fr, ARROW_SALE, ease(lin(i, 26, 44)))
    for hd in ARROW_SALE_HEAD:
        O.draw_polyline(fr, hd, ease(lin(i, 44, 50)))
    O.put_tile(fr, 800, 600, i, 40, "box", badge="6" if i < 58 else "4", label="IN STOCK", rot=5, out=out)
    O.keyword(fr, i, 54, (("Stock ", TEXT), ("updated", DOODLE)), 1400, out=out)


def ov_sync(fr, i, out):
    for k, (kind, x, y, lab) in enumerate(((("store", 230, 600, "SHOP")), ("warehouse", 540, 470, "WAREHOUSE"),
                                           ("phone", 850, 600, "YOUR PHONE"))):
        O.put_tile(fr, x, y, i, 10 + 10 * k, kind, rot=(-5, 0, 5)[k], badge="4", badge_col=(60, 150, 90),
                   size=190, label=lab, out=out)
    O.draw_polyline(fr, LINK, ease(lin(i, 44, 66)), width=8)
    O.keyword(fr, i, 70, (("Same ", TEXT), ("number", DOODLE)), 1400, out=out)


def ov_alert(fr, i, out):
    O.put_tile(fr, 280, 1020, i, 30, "bell", badge="!", out=out)
    O.draw_polyline(fr, ARROW_ALERT, ease(lin(i, 46, 64)))
    for hd in ARROW_ALERT_HEAD:
        O.draw_polyline(fr, hd, ease(lin(i, 64, 70)))
    O.keyword(fr, i, 40, (("Reorder ", TEXT), ("in time", DOODLE)), 1400, out=out)


def ov_offer(fr, i, out):
    t = ease(K.clamp((i - 40) / 18))                                 # tiles glide together
    O.put_tile(fr, 320 + 50 * t, 820, i, 8, "odoo", label="ODOO", out=out)
    O.put_tile(fr, 760 - 50 * t, 820, i, 18, "custom", label="CUSTOM", rot=6, out=out)
    if i > 30:
        K.put_text(fr, "or", "P7", 46, DOODLE, 540, 820, "cc", a=(1 - t) * out)
    O.keyword(fr, i, 44, (("Built ", TEXT), ("around you", DOODLE)), 1400, out=out)


OVERLAYS = {"shelves": ov_shelves, "three": ov_three, "files": ov_files, "sale": ov_sale,
            "sync": ov_sync, "alert": ov_alert, "offer": ov_offer}


# ---------------------------------------------------------------- end card
@lru_cache(None)
def partner_badge():
    art = Image.open(os.path.join(HERE, "assets", "odoo_ready_partners_rgb.png")).convert("RGBA")
    art = art.crop(art.getbbox())
    art = art.resize((250, int(art.height * 250 / art.width)), Image.LANCZOS)
    card = K.rrect(306, art.height + 40, 20, (255, 255, 255, 255)).copy()
    card.alpha_composite(art, (28, 20))
    return card


def end_card(fr, n):
    """Standard kit end card (stage coords, placed at y=250 on the 9:16 canvas) + partner badge."""
    K.OY = 250
    K.draw_end_card(fr, n)
    t = lin(n, END_CARD + 50, END_CARD + 62)
    if t > 0:
        K.put(fr, partner_badge(), W / 2, 1150, "cc", a=ease(t * 1.4), s=0.9 + 0.1 * K.back(t, 1.8))
    K.OY = 0


# ---------------------------------------------------------------- frames
def clip_frame(shot, i):
    frames = CLIPS[shot["clip"]]
    return frames[min(max(i + shot.get("offset", 0), 0), len(frames) - 1)]


def render(n):
    O.use_full_canvas()
    k, shot = shot_at(n)
    if shot is None:                                                  # end card over the darkened last shot
        last = SHOTS[-1]
        base = clip_frame(last, n - last["start"]).filter(ImageFilter.GaussianBlur(14))
        dim = 0.35 + 0.5 * ease(lin(n, END_CARD, END_CARD + 12))
        base = Image.blend(base, Image.new("RGB", (W, H), K.BG), dim)
        fr = base.convert("RGBA")
        if n < END_CARD + XFADE:                                      # crossfade from the sharp shot
            sharp = clip_frame(last, n - last["start"])
            fr = Image.blend(sharp, base, ease(lin(n, END_CARD, END_CARD + XFADE))).convert("RGBA")
        end_card(fr, n)
        return fr.convert("RGB")
    i = n - shot["start"]
    base = clip_frame(shot, i)
    nxt = SHOTS[k + 1] if k + 1 < len(SHOTS) else None
    if nxt and n >= nxt["start"] - XFADE // 2:
        base = O.zoom_blur_mix(base, clip_frame(nxt, n - nxt["start"]), lin(n, nxt["start"] - XFADE // 2,
                                                                              nxt["start"] + XFADE // 2))
    if k > 0 and i < XFADE // 2:
        prev = SHOTS[k - 1]
        base = O.zoom_blur_mix(clip_frame(prev, n - prev["start"]), base, lin(n, shot["start"] - XFADE // 2,
                                                                              shot["start"] + XFADE // 2))
    fr = base.convert("RGBA")
    fr.alpha_composite(VIGNETTE)
    end = shot["start"] + shot["len"]
    out = 1 - ease(lin(n, end - 7, end))                              # overlays clear just before the cut
    OVERLAYS[shot["overlay"]](fr, i, out)
    K.brand_lockup(fr, 90, 300, 44, 34, 1.0)
    K.put_text(fr, "AI-generated visuals. Illustrative.", "M", 22, (200, 200, 205), W / 2, 1560, "tc", a=0.8, track=1)
    return fr.convert("RGB")


def setup():
    global VIGNETTE, CIRCLE, SPARKS, ARROW_SALE, ARROW_SALE_HEAD, LINK, ARROW_ALERT, ARROW_ALERT_HEAD
    for s in SHOTS:
        if s["clip"] not in CLIPS:
            CLIPS[s["clip"]] = O.load_clip(os.path.join(HERE, s["clip"]))
    VIGNETTE = O.make_vignette()
    CIRCLE = O.scribble_circle(540, 900, 230, 120, seed=3)
    SPARKS = O.spark_strokes(560, 900, 200, 285, (-150, -118, -90, -62, -30))
    ARROW_SALE = O.arrow_path(420, 520, 670, 520, bend=0.35)
    ARROW_SALE_HEAD = O.arrow_head(ARROW_SALE)
    LINK = O.arrow_path(250, 760, 850, 760, bend=0.12, seed=5)
    ARROW_ALERT = O.arrow_path(360, 900, 590, 450, bend=-0.25, seed=7)
    ARROW_ALERT_HEAD = O.arrow_head(ARROW_ALERT)


def main():
    setup()
    if ARGS.frames:
        for n in map(int, ARGS.frames.split(",")):
            render(n).save(os.path.join(HERE, ".work", f"f{n:03d}.png"))
        return
    video = os.path.join(HERE, ".work", "silent.mp4")
    proc = subprocess.Popen([K.FFMPEG, "-nostdin", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                             "-s", f"{W}x{H}", "-r", "30", "-i", "-", "-c:v", "libx264", "-preset", "medium",
                             "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart", video], stdin=subprocess.PIPE)
    for n in range(TOTAL):
        proc.stdin.write(render(n).tobytes())
    proc.stdin.close()
    if proc.wait():
        raise SystemExit("ffmpeg failed")
    K.TOTAL = TOTAL
    ARGS.video_in = None
    K.mux_audio(ARGS, video, ARGS.out)


if __name__ == "__main__":
    main()
