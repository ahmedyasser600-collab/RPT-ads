"""TOLX video 01 v2 "WhatsApp orders" in the 3D-scene + 2D-overlay style (~26.5 s, 9:16).

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

K.END_CARD, K.TOTAL = END_CARD, TOTAL          # the kit's end card and fades key off these

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
BURST = [(250, 560, -8), (820, 500, 7), (180, 880, 5), (880, 860, -6), (420, 420, 4), (680, 980, -4)]


def ov_phone(fr, i, out):
    for k, (x, y, rot) in enumerate(BURST):                         # chat bubbles burst in around the phone
        O.put_tile(fr, x, y, i, 4 + 5 * k, "chat", rot=rot, size=150, out=out)
    O.put_tile(fr, 540, 600, i, 36, "chat", badge="99+", size=230, rot=0, out=out)
    O.keyword(fr, i, 40, (("On ", TEXT), ("WhatsApp?", DOODLE)), 1400, out=out)


def ov_buried(fr, i, out):
    """New bubbles keep arriving at the top and push the gold ORDER bubble down and away."""
    step, x = 120, 555
    arrivals = [6, 14 + 12, 30 + 12, 46 + 12, 62 + 12]               # frame each new bubble lands
    order_at = 6
    for k, f in enumerate(arrivals):
        if i < f:
            continue
        pushed = sum(ease(lin(i, g, g + 8)) for g in arrivals[k + 1:])
        y = 790 + step * pushed
        if k == 0:                                                  # the order
            O.put_tile(fr, x, y, i, f, "receipt", badge="!", badge_col=GOLD, label="NEW ORDER", rot=-3,
                       out=out * (1 - ease(lin(y, 1150, 1260))))
        else:
            O.put_tile(fr, x + (-30 if k % 2 else 30), y, i, f, "chat", size=150, rot=(-5, 5)[k % 2], out=out * (1 - ease(lin(y, 1150, 1260))))
    O.keyword(fr, i, 70, (("Order ", TEXT), ("buried", DOODLE)), 1400, out=out)


def ov_parcel(fr, i, out):
    O.draw_polyline(fr, ARROW_PARCEL, ease(lin(i, 28, 46)) * out)
    for hd in ARROW_PARCEL_HEAD:
        O.draw_polyline(fr, hd, ease(lin(i, 46, 52)) * out)
    O.put_tile(fr, 540, 540, i, 6, "person", badge="?", badge_col=(130, 130, 140), out=out)
    O.keyword(fr, i, 16, (("Who's ", TEXT), ("on it?", DOODLE)), 820, out=out)


def ov_status(fr, i, out):
    steps = (("receipt", 230, "NEW"), ("box", 540, "CONFIRMED"), ("check", 850, "DELIVERED"))
    for k, (kind, x, lab) in enumerate(steps):
        O.put_tile(fr, x, 560, i, 10 + 16 * k, kind, size=190, label=lab, rot=(-4, 0, 4)[k], out=out)
    O.put_tile(fr, 540, 900, i, 60, "person", label="OWNER", size=170, out=out)
    O.draw_polyline(fr, STATUS_LINE, ease(lin(i, 16, 52)) * out, width=8)
    O.keyword(fr, i, 64, (("Every order ", TEXT), ("tracked", DOODLE)), 1400, size=80, out=out)


def ov_reminder(fr, i, out):
    O.put_tile(fr, 560, 760, i, 8, "bell", label="CALL BACK  SAT 10:00", size=230, rot=-4, out=out)
    for k, st in enumerate(REMIND_SPARKS):
        O.draw_polyline(fr, st, ease(lin(i, 18 + 2 * k, 26 + 2 * k)) * out, width=12)
    O.keyword(fr, i, 26, (("No missed ", TEXT), ("follow-ups", DOODLE)), 1400, size=80, out=out)


def ov_offer(fr, i, out):
    """The pitch is simply 'shift to Odoo now': the Odoo logo tile, centred, with gold sparks."""
    if i >= 6:
        tt = lin(i, 6, 22)
        sp = odoo_tile().rotate(-4 * (1 - ease(tt)), resample=Image.BICUBIC, expand=True)
        K.put(fr, sp, 540, 800 + 6 * math.sin((i - 6) / 11), "cc", a=ease(tt * 2) * out,
              s=max(0.01, 1.25 * O.spring(tt)))
    for k, st in enumerate(OFFER_SPARKS):
        O.draw_polyline(fr, st, ease(lin(i, 18 + 2 * k, 26 + 2 * k)) * out, width=12)
    O.keyword(fr, i, 26, (("Shift to ", TEXT), ("Odoo", DOODLE)), 1400, out=out)


OVERLAYS = {"phone": ov_phone, "buried": ov_buried, "parcel": ov_parcel, "status": ov_status,
            "reminder": ov_reminder, "offer": ov_offer}


# ---------------------------------------------------------------- end card
@lru_cache(None)
def partner_badge():
    art = Image.open(os.path.join(HERE, "assets", "odoo_ready_partners_rgb.png")).convert("RGBA")
    art = art.crop(art.getbbox())
    art = art.resize((250, int(art.height * 250 / art.width)), Image.LANCZOS)
    card = K.rrect(306, art.height + 40, 20, (255, 255, 255, 255)).copy()
    card.alpha_composite(art, (28, 20))
    return card


@lru_cache(None)
def odoo_tile():
    """White rounded tile carrying the official Odoo Ready Partner artwork (unchanged, proportional resize),
    same shadow treatment as the other app tiles."""
    from PIL import ImageDraw
    art = Image.open(os.path.join(HERE, "assets", "odoo_ready_partners_rgb.png")).convert("RGBA")
    art = art.crop(art.getbbox())
    tw, th, pad = 330, 220, 40
    art = art.resize((270, int(art.height * 270 / art.width)), Image.LANCZOS)
    im = Image.new("RGBA", (tw + 2 * pad, th + 2 * pad), (0, 0, 0, 0))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((pad + 6, pad + 14, pad + tw + 6, pad + th + 14), 40, fill=(0, 0, 0, 150))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(16)))
    im.alpha_composite(K.rrect(tw, th, 40, (250, 250, 248, 255)), (pad, pad))
    im.alpha_composite(art, (pad + (tw - art.width) // 2, pad + (th - art.height) // 2))
    return im


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
    return fr.convert("RGB")


def setup():
    global VIGNETTE, ARROW_PARCEL, ARROW_PARCEL_HEAD, STATUS_LINE, REMIND_SPARKS, OFFER_SPARKS
    for s in SHOTS:
        if s["clip"] not in CLIPS:
            CLIPS[s["clip"]] = O.load_clip(os.path.join(HERE, s["clip"]))
    VIGNETTE = O.make_vignette()
    ARROW_PARCEL = O.arrow_path(600, 930, 560, 1220, bend=0.25, seed=4)
    ARROW_PARCEL_HEAD = O.arrow_head(ARROW_PARCEL)
    STATUS_LINE = O.arrow_path(250, 700, 850, 700, bend=0.1, seed=5)
    REMIND_SPARKS = O.spark_strokes(560, 760, 220, 290, (-150, -120, -60, -30))
    OFFER_SPARKS = O.spark_strokes(540, 800, 290, 360, (-155, -125, -55, -25, 25, 55, 125, 155))


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
