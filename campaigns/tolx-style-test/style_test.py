"""Style test: AI-generated 3D-render footage + TOLX motion-graphics overlay (two shots, ~10 s, 9:16).

Base layer: two Kling 3.0 clips (photoreal CGI shop shelves, no text/logos/people).
Overlay layer, drawn here: gold hand-drawn doodles that draw themselves on (scribble circle, spark
strokes), white rounded app tiles that pop in with a spring and soft shadow, and 2-4 word kinetic
keywords. Brand fonts/colours from ../tolx-kit. Frame n is shown at n/30 s.

Usage: python style_test.py --out test.mp4 [--vo vo.wav --music music.wav] [--frames 30,90]
       Doodle anchor points are set per shot in SHOTS (stage coordinates, 1080x1920).
"""
import argparse
import math
import os
import subprocess
import sys
from functools import lru_cache

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "tolx-kit"))
import tolx_kit as K  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--out")
ap.add_argument("--vo")
ap.add_argument("--music")
ap.add_argument("--sfx")
ap.add_argument("--frames")
ARGS = ap.parse_args()

W, H, FPS = 1080, 1920, 30
K.H, K.OY = H, 0                     # draw straight on the full 9:16 canvas
DOODLE = (255, 206, 72)              # warm highlighter gold, a touch brighter than brand gold for doodles
GOLD, TEXT, BG = K.GOLD, K.TEXT, K.BG
ease, lin, back = K.ease, K.lin, K.back

# ---------------------------------------------------------------- footage
def load_clip(path):
    """Decode a clip to a list of 1080x1920 RGB frames (cover-fit), lightly graded darker/warmer."""
    probe = subprocess.run([K.FFMPEG, "-i", path], capture_output=True, text=True).stderr
    vf = ("scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,"
          "eq=brightness=-0.03:saturation=0.95,colorbalance=rs=0.04:gs=0.01:bs=-0.04")
    raw = subprocess.run([K.FFMPEG, "-loglevel", "error", "-i", path, "-vf", vf, "-f", "rawvideo",
                          "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    n = len(raw) // (W * H * 3)
    return [Image.frombuffer("RGB", (W, H), raw[i * W * H * 3:(i + 1) * W * H * 3]) for i in range(n)]


# ---------------------------------------------------------------- doodles
def wobble_path(points, seed, amp=5.0):
    rng = np.random.default_rng(seed)
    return [(x + rng.normal(0, amp), y + rng.normal(0, amp)) for x, y in points]


def scribble_circle(cx, cy, rx, ry, seed=1, turns=1.18):
    """A hand-drawn loop that overshoots its start (like a marker circle)."""
    pts = []
    n = 90
    for i in range(n + 1):
        t = turns * 2 * math.pi * i / n - math.pi * 0.62
        wob = 1 + 0.06 * math.sin(3 * t + seed) + 0.03 * math.sin(7 * t)
        pts.append((cx + rx * wob * math.cos(t), cy + ry * wob * math.sin(t) + 6 * (i / n)))
    return wobble_path(pts, seed, 1.6)


def spark_strokes(cx, cy, r0, r1, angles):
    return [[(cx + r0 * math.cos(a), cy + r0 * math.sin(a)), (cx + r1 * math.cos(a), cy + r1 * math.sin(a))]
            for a in angles]


def draw_polyline(frame, pts, prog, width=11, color=DOODLE, glow=True):
    """Draw the first `prog` (0..1) of a polyline with round caps, plus a soft glow."""
    if prog <= 0:
        return
    k = max(2, int(len(pts) * prog))
    seg = pts[:k]
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.line(seg, fill=color + (255,), width=width, joint="curve")
    r = width / 2
    for x, y in (seg[0], seg[-1]):
        d.ellipse((x - r, y - r, x + r, y + r), fill=color + (255,))
    if glow:
        g = lay.filter(ImageFilter.GaussianBlur(14))
        frame.alpha_composite(g)
        frame.alpha_composite(g)
    frame.alpha_composite(lay)


# ---------------------------------------------------------------- app tiles
@lru_cache(None)
def tile(kind, size=220):
    """White rounded app tile with a soft shadow and a simple icon (gold + dark)."""
    pad = 40
    im = Image.new("RGBA", (size + 2 * pad, size + 2 * pad), (0, 0, 0, 0))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((pad + 6, pad + 14, pad + size + 6, pad + size + 14), 40, fill=(0, 0, 0, 150))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(16)))
    im.alpha_composite(K.rrect(size, size, 40, (250, 250, 248, 255)), (pad, pad))
    d = ImageDraw.Draw(im)
    x0, y0 = pad + size * 0.22, pad + size * 0.22
    s = size * 0.56
    dark = (34, 34, 40)
    if kind == "sheet":                      # spreadsheet grid
        d.rounded_rectangle((x0, y0, x0 + s, y0 + s), 12, outline=dark, width=10)
        d.rectangle((x0 + 5, y0 + 5, x0 + s - 5, y0 + s * 0.28), fill=GOLD)
        for i in (1, 2):
            d.line((x0, y0 + s * (0.28 + 0.24 * i), x0 + s, y0 + s * (0.28 + 0.24 * i)), fill=dark, width=8)
        d.line((x0 + s * 0.42, y0 + s * 0.28, x0 + s * 0.42, y0 + s), fill=dark, width=8)
    elif kind == "box":                      # stock box
        d.polygon([(x0, y0 + s * 0.3), (x0 + s / 2, y0 + s * 0.08), (x0 + s, y0 + s * 0.3), (x0 + s / 2, y0 + s * 0.52)],
                  fill=GOLD)
        d.polygon([(x0, y0 + s * 0.3), (x0 + s / 2, y0 + s * 0.52), (x0 + s / 2, y0 + s), (x0, y0 + s * 0.78)], fill=dark)
        d.polygon([(x0 + s, y0 + s * 0.3), (x0 + s / 2, y0 + s * 0.52), (x0 + s / 2, y0 + s), (x0 + s, y0 + s * 0.78)],
                  fill=(70, 70, 80))
    return im


def spring(t, overshoot=1.9):
    """0 -> 1 with a springy overshoot."""
    t = K.clamp(t)
    return 1 - math.exp(-6 * t) * math.cos(overshoot * math.pi * t * 1.6) if t < 1 else 1.0


def put_tile(frame, kind, x, y, n, f, rot=-6.0, badge=None):
    if n < f:
        return
    t = lin(n, f, f + 16)
    sc = spring(t)
    sp = tile(kind)
    if badge:
        sp = sp.copy()
        b = K.circle(96, (226, 72, 60, 255)).copy()
        ts = K.tight(badge, "P9", 56, (255, 255, 255))
        b.alpha_composite(ts, ((96 - ts.width) // 2, (96 - ts.height) // 2))
        sp.alpha_composite(b, (sp.width - 120, 8))
    sp = sp.rotate(rot * (1 - 0.4 * ease(t)), resample=Image.BICUBIC, expand=True)
    bob = 6 * math.sin((n - f) / 11)
    K.put(frame, sp, x, y + bob, "cc", a=ease(t * 2), s=max(0.01, sc))


# ---------------------------------------------------------------- kinetic keywords
@lru_cache(None)
def baseline_word(text, size, col, depth=6):
    """Extruded word on the font's full line box (not cropped), so mixed words share one baseline."""
    top = K.text_sprite(text, "P9I", size, col)
    side = K.text_sprite(text, "P9I", size, K.DEEP_GOLD)
    im = Image.new("RGBA", (top.width + depth, top.height + depth), (0, 0, 0, 0))
    for k in range(depth, 0, -1):
        im.alpha_composite(side, (k, k))
    im.alpha_composite(top, (0, 0))
    return im

def keyword(frame, n, f, segs, y, size=104):
    """2-4 words that rise in word by word (smooth), on a soft dark band for legibility."""
    if n < f:
        return
    words = []
    for text, col in segs:
        for w in text.split(" "):
            if w:
                words.append((w, col))
    sprites = [baseline_word(w, size, col) for w, col in words]
    gap = int(size * 0.28)
    total = sum(s.width for s in sprites) + gap * (len(sprites) - 1)
    band = K.glow(total + 60, size + 30, (0, 0, 0), 30, 150)
    g, pad = band
    K.put(frame, g, W / 2 - (total + 60) / 2 - pad, y - (size + 30) / 2 - pad, "tl", a=ease(lin(n, f, f + 10)) * 0.9)
    x = W / 2 - total / 2
    for i, sp in enumerate(sprites):
        dy, a, sc = K.reveal(n, f + 4 * i, 12, 40)
        K.put(frame, sp, x + sp.width / 2, y + dy, "cc", a=a, s=sc, text=True)
        x += sp.width + gap


# ---------------------------------------------------------------- shots
# Doodle anchors are in canvas pixels; tuned to the generated clips after viewing them.
SHOTS = [
    {"clip": "clips/shot1.mp4", "start": 0, "len": 150,
     "circle": (540, 900, 230, 120), "tile": ("sheet", 820, 520), "kw_f": 34,
     "kw": (("Excel says ", TEXT), ("12", DOODLE)), "kw_y": 1380},
    {"clip": "clips/shot2.mp4", "start": 150, "len": 150,
     "spark": (560, 900), "tile": ("box", 800, 560), "kw_f": 20,
     "kw": (("Shelf: ", TEXT), ("3", (240, 96, 80))), "kw_y": 1400},
]
TOTAL = 300
CLIPS = {}


def render(n):
    shot = SHOTS[0] if n < SHOTS[1]["start"] else SHOTS[1]
    i = n - shot["start"]
    frames = CLIPS[shot["clip"]]
    base = frames[min(i, len(frames) - 1)].convert("RGBA")
    # transition: quick zoom-blur crossfade into shot 2
    if SHOTS[1]["start"] - 6 <= n < SHOTS[1]["start"] + 6:
        t = lin(n, SHOTS[1]["start"] - 6, SHOTS[1]["start"] + 6)
        a_img = CLIPS[SHOTS[0]["clip"]][min(n, len(CLIPS[SHOTS[0]["clip"]]) - 1)]
        b_img = CLIPS[SHOTS[1]["clip"]][max(0, n - SHOTS[1]["start"])]
        z = 1 + 0.08 * math.sin(math.pi * t)
        mixed = Image.blend(a_img, b_img, ease(t)).resize((int(W * z), int(H * z)), Image.BILINEAR)
        mixed = mixed.crop(((mixed.width - W) // 2, (mixed.height - H) // 2, (mixed.width - W) // 2 + W,
                            (mixed.height - H) // 2 + H)).filter(ImageFilter.GaussianBlur(4 * math.sin(math.pi * t)))
        base = mixed.convert("RGBA")
    frame = base
    # vignette for depth and legibility
    frame.alpha_composite(VIGNETTE)
    if "circle" in shot:
        cx, cy, rx, ry = shot["circle"]
        draw_polyline(frame, CIRCLE_PTS, ease(lin(i, 12, 34)))
    if "spark" in shot:
        cx, cy = shot["spark"]
        for k, stroke in enumerate(SPARKS):
            p = ease(lin(i, 10 + 3 * k, 18 + 3 * k))
            draw_polyline(frame, [stroke[0], (stroke[0][0] + (stroke[1][0] - stroke[0][0]) * p,
                                              stroke[0][1] + (stroke[1][1] - stroke[0][1]) * p)], 1 if p > 0 else 0,
                          width=12)
    kind, tx, ty = shot["tile"]
    put_tile(frame, kind, tx, ty, i, 18, badge="3" if kind == "box" else None)
    keyword(frame, i, shot["kw_f"], shot["kw"], shot["kw_y"])
    # brand mark + honesty footnote
    K.brand_lockup(frame, 90, 300, 44, 34, 1.0)
    K.put_text(frame, "AI-generated visuals. Illustrative.", "M", 22, (200, 200, 205), W / 2, 1560, "tc", a=0.8,
               track=1)
    return frame.convert("RGB")


def make_vignette():
    y, x = np.mgrid[0:H, 0:W]
    d = np.sqrt(((x - W / 2) / (W * 0.75)) ** 2 + ((y - H / 2) / (H * 0.62)) ** 2)
    a = np.clip((d - 0.55) * 1.4, 0, 1) * 200
    top = np.clip((420 - y) / 420, 0, 1) * 120            # keep the brand mark readable
    alpha = np.clip(a + top, 0, 235).astype(np.uint8)
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    im.putalpha(Image.fromarray(alpha))
    return im


def main():
    global VIGNETTE, CIRCLE_PTS, SPARKS
    for s in SHOTS:
        CLIPS[s["clip"]] = load_clip(os.path.join(HERE, s["clip"]))
    VIGNETTE = make_vignette()
    CIRCLE_PTS = scribble_circle(*SHOTS[0]["circle"], seed=3)
    cx, cy = SHOTS[1]["spark"]
    SPARKS = spark_strokes(cx, cy, 200, 285, [math.radians(a) for a in (-150, -118, -90, -62, -30)])
    if ARGS.frames:
        for n in map(int, ARGS.frames.split(",")):
            render(n).save(os.path.join(HERE, ".work", f"f{n:03d}.png"))
        return
    video = os.path.join(HERE, ".work", "silent.mp4")
    proc = subprocess.Popen([K.FFMPEG, "-nostdin", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                             "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium",
                             "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart", video], stdin=subprocess.PIPE)
    for n in range(TOTAL):
        proc.stdin.write(render(n).tobytes())
    proc.stdin.close()
    proc.wait()
    K.TOTAL = TOTAL
    K.mux_audio(ARGS, video, ARGS.out)


if __name__ == "__main__":
    main()
