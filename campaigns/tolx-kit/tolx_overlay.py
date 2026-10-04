"""TOLX "3D scene + 2D overlay" style (approved from the 4 Oct 2026 style test).

Base layer: AI-generated photoreal CGI clips (no text/logos/people in the footage).
Overlay layer, drawn here on a full 1080x1920 canvas: gold hand-drawn doodles that draw themselves on,
white rounded app tiles that pop in with a spring and soft shadow (gold/dark icons), baseline-aligned
kinetic keywords (2-4 words), a vignette, a zoom-blur crossfade between shots.
"""
import math
import subprocess
from functools import lru_cache

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import tolx_kit as K

W, H, FPS = 1080, 1920, 30
DOODLE = (255, 206, 72)            # warm highlighter gold for doodles
RED = (226, 72, 60)
DARK = (34, 34, 40)
ease, lin, back = K.ease, K.lin, K.back


def use_full_canvas():
    """Overlay drawing uses canvas pixels directly (no stage offset)."""
    K.H, K.OY = H, 0


# ---------------------------------------------------------------- footage
def load_clip(path):
    """Decode to 30 fps 1080x1920 RGB frames (cover-fit), lightly graded darker and warmer."""
    vf = ("scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,"
          "eq=brightness=-0.03:saturation=0.95,colorbalance=rs=0.04:gs=0.01:bs=-0.04")
    raw = subprocess.run([K.FFMPEG, "-loglevel", "error", "-i", path, "-vf", vf, "-f", "rawvideo",
                          "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    n = len(raw) // (W * H * 3)
    return [Image.frombuffer("RGB", (W, H), raw[i * W * H * 3:(i + 1) * W * H * 3]) for i in range(n)]


def zoom_blur_mix(a_img, b_img, t):
    """Crossfade with a brief push-in and blur peak in the middle (t 0..1)."""
    z = 1 + 0.08 * math.sin(math.pi * t)
    m = Image.blend(a_img, b_img, ease(t)).resize((int(W * z), int(H * z)), Image.BILINEAR)
    x0, y0 = (m.width - W) // 2, (m.height - H) // 2
    return m.crop((x0, y0, x0 + W, y0 + H)).filter(ImageFilter.GaussianBlur(4 * math.sin(math.pi * t)))


def make_vignette():
    y, x = np.mgrid[0:H, 0:W]
    d = np.sqrt(((x - W / 2) / (W * 0.75)) ** 2 + ((y - H / 2) / (H * 0.62)) ** 2)
    a = np.clip((d - 0.55) * 1.4, 0, 1) * 200
    top = np.clip((420 - y) / 420, 0, 1) * 120
    alpha = np.clip(a + top, 0, 235).astype(np.uint8)
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    im.putalpha(Image.fromarray(alpha))
    return im


# ---------------------------------------------------------------- doodles
def _wobble(points, seed, amp):
    rng = np.random.default_rng(seed)
    return [(x + rng.normal(0, amp), y + rng.normal(0, amp)) for x, y in points]


def scribble_circle(cx, cy, rx, ry, seed=1, turns=1.18):
    pts = []
    n = 90
    for i in range(n + 1):
        t = turns * 2 * math.pi * i / n - math.pi * 0.62
        wob = 1 + 0.06 * math.sin(3 * t + seed) + 0.03 * math.sin(7 * t)
        pts.append((cx + rx * wob * math.cos(t), cy + ry * wob * math.sin(t) + 6 * (i / n)))
    return _wobble(pts, seed, 1.6)


def spark_strokes(cx, cy, r0, r1, angles_deg):
    out = []
    for a in angles_deg:
        a = math.radians(a)
        out.append([(cx + r0 * math.cos(a), cy + r0 * math.sin(a)), (cx + r1 * math.cos(a), cy + r1 * math.sin(a))])
    return out


def arrow_path(x0, y0, x1, y1, bend=0.25, seed=2):
    """A hand-drawn curved arrow body (head drawn separately by arrow_head)."""
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    nx, ny = -(y1 - y0), (x1 - x0)
    cx, cy = mx + nx * bend, my + ny * bend
    pts = [((1 - t) ** 2 * x0 + 2 * (1 - t) * t * cx + t ** 2 * x1,
            (1 - t) ** 2 * y0 + 2 * (1 - t) * t * cy + t ** 2 * y1) for t in np.linspace(0, 1, 40)]
    return _wobble(pts, seed, 1.2)


def arrow_head(path, size=40):
    (x0, y0), (x1, y1) = path[-4], path[-1]
    a = math.atan2(y1 - y0, x1 - x0)
    return [[(x1 - size * math.cos(a + s * 0.55), y1 - size * math.sin(a + s * 0.55)), (x1, y1)] for s in (-1, 1)]


def draw_polyline(frame, pts, prog, width=11, color=DOODLE, glow=True):
    if prog <= 0:
        return
    seg = pts[:max(2, int(round(len(pts) * min(1, prog))))]
    if prog < 1 and len(pts) == 2:
        (xa, ya), (xb, yb) = pts
        seg = [(xa, ya), (xa + (xb - xa) * prog, ya + (yb - ya) * prog)]
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
def _icon(d, kind, x0, y0, s):
    G = K.GOLD
    if kind == "sheet":
        d.rounded_rectangle((x0, y0, x0 + s, y0 + s), 12, outline=DARK, width=10)
        d.rectangle((x0 + 5, y0 + 5, x0 + s - 5, y0 + s * 0.28), fill=G)
        for i in (1, 2):
            d.line((x0, y0 + s * (0.28 + 0.24 * i), x0 + s, y0 + s * (0.28 + 0.24 * i)), fill=DARK, width=8)
        d.line((x0 + s * 0.42, y0 + s * 0.28, x0 + s * 0.42, y0 + s), fill=DARK, width=8)
    elif kind == "box":
        d.polygon([(x0, y0 + s * .3), (x0 + s / 2, y0 + s * .08), (x0 + s, y0 + s * .3), (x0 + s / 2, y0 + s * .52)], fill=G)
        d.polygon([(x0, y0 + s * .3), (x0 + s / 2, y0 + s * .52), (x0 + s / 2, y0 + s), (x0, y0 + s * .78)], fill=DARK)
        d.polygon([(x0 + s, y0 + s * .3), (x0 + s / 2, y0 + s * .52), (x0 + s / 2, y0 + s), (x0 + s, y0 + s * .78)],
                  fill=(70, 70, 80))
    elif kind == "receipt":
        d.polygon([(x0 + s * .15, y0), (x0 + s * .85, y0), (x0 + s * .85, y0 + s), (x0 + s * .72, y0 + s * .9),
                   (x0 + s * .58, y0 + s), (x0 + s * .44, y0 + s * .9), (x0 + s * .3, y0 + s), (x0 + s * .15, y0 + s * .9)],
                  fill=DARK)
        for i, w in enumerate((0.5, 0.4, 0.5)):
            d.line((x0 + s * .27, y0 + s * (0.22 + 0.18 * i), x0 + s * (0.27 + w), y0 + s * (0.22 + 0.18 * i)),
                   fill=(250, 250, 248), width=7)
        d.ellipse((x0 + s * .55, y0 + s * .62, x0 + s * .75, y0 + s * .82), fill=G)
    elif kind == "store":
        d.rectangle((x0 + s * .1, y0 + s * .42, x0 + s * .9, y0 + s), fill=DARK)
        d.polygon([(x0, y0 + s * .42), (x0 + s * .12, y0 + s * .08), (x0 + s * .88, y0 + s * .08), (x0 + s, y0 + s * .42)],
                  fill=G)
        d.rectangle((x0 + s * .4, y0 + s * .62, x0 + s * .6, y0 + s), fill=(250, 250, 248))
    elif kind == "warehouse":
        d.polygon([(x0, y0 + s * .38), (x0 + s / 2, y0 + s * .05), (x0 + s, y0 + s * .38)], fill=G)
        d.rectangle((x0 + s * .06, y0 + s * .38, x0 + s * .94, y0 + s), fill=DARK)
        for i in range(3):
            d.line((x0 + s * .24, y0 + s * (0.55 + 0.14 * i), x0 + s * .76, y0 + s * (0.55 + 0.14 * i)),
                   fill=(250, 250, 248), width=7)
    elif kind == "phone":
        d.rounded_rectangle((x0 + s * .24, y0, x0 + s * .76, y0 + s), 18, fill=DARK)
        d.rounded_rectangle((x0 + s * .3, y0 + s * .1, x0 + s * .7, y0 + s * .8), 6, fill=G)
        d.ellipse((x0 + s * .45, y0 + s * .85, x0 + s * .55, y0 + s * .95), fill=(250, 250, 248))
    elif kind == "bell":
        d.pieslice((x0 + s * .14, y0 + s * .05, x0 + s * .86, y0 + s * .8), 180, 360, fill=G)
        d.rectangle((x0 + s * .14, y0 + s * .42, x0 + s * .86, y0 + s * .72), fill=G)
        d.rounded_rectangle((x0 + s * .02, y0 + s * .7, x0 + s * .98, y0 + s * .8), 6, fill=DARK)
        d.ellipse((x0 + s * .4, y0 + s * .82, x0 + s * .6, y0 + s * 1.0), fill=DARK)
    elif kind == "chat":                          # speech bubble with text lines
        d.rounded_rectangle((x0, y0 + s * .05, x0 + s, y0 + s * .75), 22, fill=K.GOLD)
        d.polygon([(x0 + s * .18, y0 + s * .7), (x0 + s * .1, y0 + s * .98), (x0 + s * .42, y0 + s * .74)], fill=K.GOLD)
        for i, w in enumerate((0.7, 0.5)):
            d.line((x0 + s * .16, y0 + s * (0.3 + 0.2 * i), x0 + s * (0.16 + w), y0 + s * (0.3 + 0.2 * i)),
                   fill=DARK, width=9)
    elif kind == "check":                         # gold tick in a circle
        d.ellipse((x0, y0, x0 + s, y0 + s), fill=(80, 200, 120))
        d.line((x0 + s * .26, y0 + s * .52, x0 + s * .44, y0 + s * .7), fill=(250, 250, 248), width=14)
        d.line((x0 + s * .43, y0 + s * .7, x0 + s * .76, y0 + s * .32), fill=(250, 250, 248), width=14)
    elif kind == "person":                        # owner avatar
        d.ellipse((x0 + s * .3, y0, x0 + s * .7, y0 + s * .4), fill=DARK)
        d.pieslice((x0 + s * .1, y0 + s * .45, x0 + s * .9, y0 + s * 1.25), 180, 360, fill=K.GOLD)
    elif kind == "odoo":                          # TOLX-style "apps" glyph (not Odoo's logo)
        for i in range(2):
            for j in range(2):
                c = G if (i + j) % 2 == 0 else DARK
                d.rounded_rectangle((x0 + s * (0.04 + 0.5 * i), y0 + s * (0.04 + 0.5 * j),
                                     x0 + s * (0.46 + 0.5 * i), y0 + s * (0.46 + 0.5 * j)), 12, fill=c)
    elif kind == "custom":                        # code brackets
        for sgn, xa in ((-1, x0 + s * .32), (1, x0 + s * .68)):
            d.line((xa, y0 + s * .15, xa + sgn * s * .26, y0 + s * .5), fill=DARK, width=14)
            d.line((xa + sgn * s * .26, y0 + s * .5, xa, y0 + s * .85), fill=DARK, width=14)
        d.line((x0 + s * .56, y0 + s * .1, x0 + s * .44, y0 + s * .9), fill=K.GOLD, width=12)


@lru_cache(None)
def tile(kind, size=220, badge=None, badge_col=RED, label=None):
    pad = 40
    im = Image.new("RGBA", (size + 2 * pad, size + 2 * pad + (54 if label else 0)), (0, 0, 0, 0))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((pad + 6, pad + 14, pad + size + 6, pad + size + 14), 40, fill=(0, 0, 0, 150))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(16)))
    im.alpha_composite(K.rrect(size, size, 40, (250, 250, 248, 255)), (pad, pad))
    d = ImageDraw.Draw(im)
    _icon(d, kind, pad + size * 0.22, pad + size * 0.22, size * 0.56)
    if badge:
        b = K.circle(96, badge_col + (255,)).copy()
        ts = K.tight(badge, "P9", 52 if len(badge) < 3 else 40, (255, 255, 255))
        b.alpha_composite(ts, ((96 - ts.width) // 2, (96 - ts.height) // 2))
        im.alpha_composite(b, (im.width - 120, 8))
    if label:
        ts = K.text_sprite(label, "M", 26, (240, 240, 240), 2)
        im.alpha_composite(ts, ((im.width - ts.width) // 2, pad + size + 16))
    return im


def spring(t, overshoot=1.9):
    t = K.clamp(t)
    return 1 - math.exp(-6 * t) * math.cos(overshoot * math.pi * t * 1.6) if t < 1 else 1.0


def put_tile(frame, x, y, n, f, kind, rot=-6.0, out=1.0, **kw):
    if n < f:
        return
    t = lin(n, f, f + 16)
    sp = tile(kind, **kw).rotate(rot * (1 - 0.4 * ease(t)), resample=Image.BICUBIC, expand=True)
    K.put(frame, sp, x, y + 6 * math.sin((n - f) / 11), "cc", a=ease(t * 2) * out, s=max(0.01, spring(t)))


# ---------------------------------------------------------------- kinetic keywords
@lru_cache(None)
def baseline_word(text, size, col, depth=6):
    top = K.text_sprite(text, "P9I", size, col)
    side = K.text_sprite(text, "P9I", size, K.DEEP_GOLD)
    im = Image.new("RGBA", (top.width + depth, top.height + depth), (0, 0, 0, 0))
    for k in range(depth, 0, -1):
        im.alpha_composite(side, (k, k))
    im.alpha_composite(top, (0, 0))
    return im


def keyword(frame, n, f, segs, y, size=104, out=1.0):
    """Words rise in one by one on a soft dark band. segs: ((text, colour), ...)."""
    if n < f:
        return
    words = [(w, col) for text, col in segs for w in text.split(" ") if w]
    sprites = [baseline_word(w, size, col) for w, col in words]
    gap = int(size * 0.28)
    total = sum(s.width for s in sprites) + gap * (len(sprites) - 1)
    g, pad = K.glow(total + 60, size + 30, (0, 0, 0), 30, 150)
    K.put(frame, g, W / 2 - (total + 60) / 2 - pad, y - (size + 30) / 2 - pad, "tl", a=ease(lin(n, f, f + 10)) * 0.9 * out)
    x = W / 2 - total / 2
    for i, sp in enumerate(sprites):
        dy, a, sc = K.reveal(n, f + 4 * i, 12, 40)
        K.put(frame, sp, x + sp.width / 2, y + dy, "cc", a=a * out, s=sc, text=True)
        x += sp.width + gap


@lru_cache(None)
def notification_card(title, sub, kind="bell", width=760):
    """Phone-style notification: white rounded card, icon tile on the left, bold dark title and a grey line.
    Readable on any footage (replaces thin mono labels)."""
    pad, h = 40, 200
    im = Image.new("RGBA", (width + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((pad + 6, pad + 14, pad + width + 6, pad + h + 14), 44, fill=(0, 0, 0, 160))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18)))
    im.alpha_composite(K.rrect(width, h, 44, (250, 250, 248, 255)), (pad, pad))
    d = ImageDraw.Draw(im)
    s = 120
    d.rounded_rectangle((pad + 40, pad + (h - s) // 2, pad + 40 + s, pad + (h + s) // 2), 30, fill=(240, 236, 226))
    _icon(d, kind, pad + 40 + s * 0.2, pad + (h - s) // 2 + s * 0.2, s * 0.6)
    tx = pad + 40 + s + 36
    d.text((tx, pad + 38), title, font=K.F("C7", 54), fill=DARK)
    d.text((tx, pad + 112), sub, font=K.F("C5", 38), fill=(110, 110, 118))
    return im


def put_card(frame, sprite, x, y, n, f, out=1.0):
    if n < f:
        return
    t = lin(n, f, f + 16)
    K.put(frame, sprite, x, y + 30 * (1 - ease(t)) + 5 * math.sin((n - f) / 12), "cc", a=ease(t * 2) * out,
          s=max(0.01, 0.85 + 0.15 * spring(t)))
