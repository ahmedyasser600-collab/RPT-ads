"""Render the 30 s vertical reel for Tribu del Alma's Art & Music Retreat (photo-free version).

Everything (copy, dates, colours, fonts, scenes, narration placement, captions, music) comes
from config.json. Frame n (zero-based) shows time n / fps; every frame is computed from that
time alone, so any frame can be rendered on its own.

No photographs: each scene is a brand-colour field with a simple line drawing that draws
itself (an unfinished brushstroke, the hills on the horizon, a paint stroke / handwriting
loop / sound wave, two rhythms falling into step, an arch with a low sun). The logo is the
supplied artwork, resized proportionally only.

Outputs (one pass):
  <out>/tribu-art-music-30s.mp4             designed text, narration + music
  <out>/tribu-art-music-30s-captioned.mp4   same, with burned-in narration captions
  <out>/tribu-art-music-30s-music-only.mp4  designed text, music only (for a host recording later)
  <out>/tribu-art-music-30s.srt             narration captions
  <out>/contact-sheet.png                   six-frame contact sheet

Usage:
  python render.py [--out out] [--size 1080] [--frames 0,120,...] [--sheet-only]
"""
import argparse
import json
import math
import os
import subprocess
import tempfile

import imageio_ffmpeg
import numpy as np
import pyloudnorm
import soundfile as sf
from PIL import Image, ImageDraw, ImageFont
from scipy.ndimage import minimum_filter1d, uniform_filter1d
from scipy.signal import resample_poly

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = json.load(open(os.path.join(HERE, "config.json"), encoding="utf-8"))
EV = CFG["event"]
W, H, FPS, DUR = CFG["video"]["width"], CFG["video"]["height"], CFG["video"]["fps"], CFG["video"]["duration"]
TOTAL = int(round(DUR * FPS))
SAFE = CFG["safe_area"]
CX = (SAFE["x0"] + SAFE["x1"]) / 2           # centred elements centre on the safe area, not the frame
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
NAME = "tribu-art-music-30s"


def rgb(hexstr):
    return tuple(int(hexstr[i:i + 2], 16) for i in (1, 3, 5))


C = {k: rgb(v) for k, v in CFG["colors"].items()}


def path(rel):
    return os.path.join(HERE, rel)


def fmt(text):
    return text.format(**EV)


# ------------------------------------------------------------------ fonts
def font(kind, size):
    return ImageFont.truetype(path(CFG["fonts"][kind]), size)


_title_fonts = {}


def title_font(size):
    if size not in _title_fonts:
        _title_fonts[size] = font("title", size)
    return _title_fonts[size]


F_LABEL = font("label", 32)
F_CAPTION = font("body", 40)
F_END_TITLE = font("title", 92)
F_END_DATES = font("body", 56)
F_END_PLACE = font("body", 42)
F_END_CTA = font("body", 46)
F_END_URL = font("body", 42)
F_END_BRAND = font("label", 28)


# ------------------------------------------------------------------ logo
LOGO_CFG = CFG["assets"]["logo"]
LOGO_IS_ORIGINAL = os.path.exists(path(LOGO_CFG["original"]))
LOGO_PATH = LOGO_CFG["original"] if LOGO_IS_ORIGINAL else LOGO_CFG["standin"]


def load_logo():
    im = Image.open(path(LOGO_PATH)).convert("RGBA")
    if LOGO_IS_ORIGINAL:
        bw, bh = LOGO_CFG["original_box"]
        s = min(bw / im.width, bh / im.height)            # proportional only
        return im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    # Stand-in: the emblem cut from the screenshot sits on the page's cream (#F0EEE2,
    # identical to our background). A soft circular mask removes the square edge.
    d = LOGO_CFG["standin_display_px"]
    im = im.resize((d, d), Image.LANCZOS)
    m = Image.new("L", (d * 4, d * 4), 0)
    ImageDraw.Draw(m).ellipse((6, 6, d * 4 - 6, d * 4 - 6), fill=255)
    im.putalpha(m.resize((d, d), Image.LANCZOS))
    return im


LOGO = load_logo()


# ------------------------------------------------------------------ easing / timing
def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease(x):                      # ease-out cubic
    x = clamp(x)
    return 1 - (1 - x) ** 3


def ease_io(x):                   # ease-in-out sine
    x = clamp(x)
    return 0.5 - 0.5 * math.cos(math.pi * x)


def lerp(a, b, p):
    return a + (b - a) * p


# ------------------------------------------------------------------ scenes and background
SCENES = CFG["scenes"]
GRAIN = np.random.default_rng(7).normal(0, 1.6, (H, W, 1)).astype(np.float32)


def scene_index(t):
    idx = 0
    for i, s in enumerate(SCENES):
        if t >= s["start"]:
            idx = i
    return idx


def background(t):
    i = scene_index(t)
    s = SCENES[i]
    cur = np.array(C[s["bg"]], np.float32)
    if i == 0 or t >= s["start"] + s.get("fade", 0.5):
        base = np.broadcast_to(cur, (H, W, 3))
    else:
        prev = np.array(C[SCENES[i - 1]["bg"]], np.float32)
        p = ease_io((t - s["start"]) / s.get("fade", 0.5))
        if s.get("transition") == "doors":
            # The new colour opens from the centre outward, like doors onto the landscape.
            half = p * (W / 2 + 30)
            x = np.arange(W, dtype=np.float32)
            m = np.clip((half - np.abs(x - W / 2)) / 24 + 0.5, 0, 1)[None, :, None]
            base = np.broadcast_to(prev, (H, W, 3)) * (1 - m) + cur * m
        else:
            # The new colour rises from the bottom with a soft edge (no muddy mid-blend).
            edge = H + 80 - p * (H + 160)
            y = np.arange(H, dtype=np.float32)
            m = np.clip((y - edge) / 80 + 0.5, 0, 1)[:, None, None]
            base = np.broadcast_to(prev, (H, W, 3)) * (1 - m) + cur * m
    return Image.fromarray(np.clip(base + GRAIN, 0, 255).astype(np.uint8)).convert("RGBA")


def scene_colors(t):
    s = SCENES[scene_index(t)]
    return C[s["ink"]], C[s["accent"]], s["bg"]


# ------------------------------------------------------------------ line drawings
SS = 2                            # motifs are drawn at 2x and downsampled for smooth lines


class Pen:
    """Anti-aliased drawing on a 2x layer; coordinates are frame pixels."""

    def __init__(self):
        self.im = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.im)
        self.used = False

    def line(self, pts, width, color, alpha):
        if len(pts) < 2 or alpha <= 0:
            return
        self.used = True
        fill = color + (int(255 * clamp(alpha)),)
        p2 = [(x * SS, y * SS) for x, y in pts]
        self.d.line(p2, fill=fill, width=max(1, int(round(width * SS))), joint="curve")
        r = width * SS / 2
        for x, y in (p2[0], p2[-1]):
            self.d.ellipse((x - r, y - r, x + r, y + r), fill=fill)

    def disc(self, cx, cy, r, color, alpha):
        self.used = True
        self.d.ellipse(((cx - r) * SS, (cy - r) * SS, (cx + r) * SS, (cy + r) * SS),
                       fill=color + (int(255 * clamp(alpha)),))

    def layer(self):
        return self.im.resize((W, H), Image.LANCZOS)


def partial(pts, p):
    """The first fraction p (by arc length) of a polyline."""
    if p <= 0:
        return []
    pts = np.asarray(pts, np.float64)
    seg = np.hypot(*np.diff(pts, axis=0).T)
    cum = np.concatenate([[0], np.cumsum(seg)])
    target = cum[-1] * clamp(p)
    k = int(np.searchsorted(cum, target))
    if k == 0:
        return [tuple(pts[0])]
    k = min(k, len(pts) - 1)
    f = (target - cum[k - 1]) / max(seg[k - 1], 1e-9)
    end = pts[k - 1] + (pts[k] - pts[k - 1]) * f
    return [tuple(q) for q in pts[:k]] + [tuple(end)]


def curve(fx, fy, n=240):
    return [(fx(u), fy(u)) for u in np.linspace(0, 1, n)]


def brush(pen, pts, p, color, alpha, spread=22, seed=3, bristles=16, wmin=2.5, wmax=6.5):
    """A dry-brush stroke: parallel bristles with slightly different lengths and opacity."""
    rng = np.random.default_rng(seed)
    pts = np.asarray(pts, np.float64)
    tang = np.gradient(pts, axis=0)
    norm = np.stack([-tang[:, 1], tang[:, 0]], 1)
    norm /= np.linalg.norm(norm, axis=1, keepdims=True) + 1e-9
    for b in range(bristles):
        o = lerp(-spread, spread, b / (bristles - 1)) + rng.normal(0, 1.5)
        length = 1 - abs(o) / spread * 0.18 - rng.uniform(0, 0.08)
        width = rng.uniform(wmin, wmax)
        a = alpha * rng.uniform(0.45, 0.95)
        swell = 1 - (abs(o) / spread) ** 2 * 0.5
        pen.line(partial(pts + norm * o * swell, p * length), width, color, a)


def stroke_alpha(t, s, out=0.35):
    return 1 - ease_io((t - (s["end"] - out)) / out)


def motif_unfinished_stroke(pen, t, s):
    # Starts already part-way (readable cover frame), moves on, then stops unfinished.
    t0, t1 = s["draw"]
    p = 0.30 + 0.38 * ease((t - t0) / (t1 - t0))
    pts = curve(lambda u: lerp(130, 950, u), lambda u: 660 - 90 * math.sin(math.pi * (u * 0.9 + 0.05)) + 24 * u)
    brush(pen, pts, p, C["rust"], 0.92 * stroke_alpha(t, s), spread=58, seed=11, bristles=34, wmin=6, wmax=13)


def hills(u, base, k):
    return base - (46 * math.sin(2 * math.pi * (0.75 * u) + 0.6 + k) + 22 * math.sin(2 * math.pi * 2.1 * u + k)
                   + 8 * math.sin(2 * math.pi * 5.3 * u + 2 * k))


def motif_hills(pen, t, s):
    t0, t1 = s["draw"]
    a = stroke_alpha(t, s)
    back = curve(lambda u: lerp(60, 1020, u), lambda u: hills(u, 690, 1.7))
    front = curve(lambda u: lerp(60, 1020, u), lambda u: hills(u, 790, 0.0))
    fill = ease_io((t - t0 - 0.8) / 1.6)
    if fill > 0:                                   # the land below the front ridge, softly filled in
        poly = [(x * SS, y * SS) for x, y in front] + [(1020 * SS, 1000 * SS), (60 * SS, 1000 * SS)]
        layer = Image.new("RGBA", pen.im.size, (0, 0, 0, 0))
        ImageDraw.Draw(layer).polygon(poly, fill=C["sage"] + (int(110 * fill * a),))
        fade = Image.linear_gradient("L").resize((pen.im.width, 210 * SS))
        mask = Image.new("L", pen.im.size, 255)
        mask.paste(fade.transpose(Image.FLIP_TOP_BOTTOM), (0, 790 * SS))
        mask.paste(0, (0, 1000 * SS, pen.im.width, pen.im.height))
        layer.putalpha(Image.composite(layer.getchannel("A"), Image.new("L", pen.im.size, 0), mask))
        pen.im.alpha_composite(layer)
    pen.line(partial(back, ease_io((t - t0) / (t1 - t0))), 5, C["gold"], 0.55 * a)
    pen.line(partial(front, ease_io((t - t0 - 0.35) / (t1 - t0))), 9, C["gold"], 0.95 * a)


def motif_paint_write_music(pen, t, s):
    a = stroke_alpha(t, s)
    tp, tw, tm = s["draw"]
    # Paint: a short brushstroke.
    paint = curve(lambda u: lerp(110, 860, u), lambda u: 370 - 44 * math.sin(math.pi * u) + 14 * u)
    brush(pen, paint, ease((t - tp) / 0.9), C["rust"], 0.92 * a, spread=40, seed=5, bristles=26, wmin=5, wmax=11)

    # Write: a loose, looping hand (abstract loops, not letters).
    def wx(u):
        return 110 + 700 * u - 30 * math.sin(u * 2 * math.pi * 7)

    def wy(u):
        th = u * 2 * math.pi * 7
        return 585 - 44 * math.cos(th) * (0.75 + 0.25 * math.sin(3 * u)) + 12 * math.sin(2 * math.pi * u)

    pen.line(partial(curve(wx, wy, 700), ease_io((t - tw) / 1.0)), 7, C["deep_green"], 0.95 * a)

    # Make music: a sound wave that swells and settles.
    def my(u):
        env = math.sin(math.pi * u) ** 0.9 * (0.65 + 0.35 * math.sin(2 * math.pi * 1.5 * u))
        return 800 + 84 * env * math.sin(2 * math.pi * 9 * u + 2.5 * (t - tm))

    pen.line(partial(curve(lambda u: lerp(110, 900, u), my, 500), ease_io((t - tm) / 1.0)), 7, C["sage"], 0.95 * a)


def motif_two_rhythms(pen, t, s):
    a = stroke_alpha(t, s)
    ta, tb = s["draw"]
    # Line A keeps its own steady rhythm; line B arrives out of step and falls into step with it.
    fa, pa = 2.6, -1.4 * (t - ta)
    ya = curve(lambda u: lerp(60, 1020, u), lambda u: 520 + 85 * math.sin(2 * math.pi * fa * u + pa), 400)
    pen.line(partial(ya, ease_io((t - ta) / 1.0)), 9, C["cream"], 0.95 * a)
    k = ease_io((t - tb - 0.4) / 1.6)                  # 0 = own rhythm, 1 = in step
    fb = lerp(3.7, fa, k)
    pb = lerp(-2.3 * (t - tb) + 1.9, pa, k)
    yb = curve(lambda u: lerp(60, 1020, u), lambda u: 660 + lerp(60, 85, k) * math.sin(2 * math.pi * fb * u + pb), 400)
    pen.line(partial(yb, ease_io((t - tb) / 1.0)), 9, C["deep_green"], 0.9 * a)


def arch_path(cx=500, half=250, top=520, bottom=930):
    arc = [(cx - half * math.cos(th), top - half * math.sin(th)) for th in np.linspace(0, math.pi, 120)]
    return [(cx - half, bottom)] + arc + [(cx + half, bottom)]


def motif_arch_and_sun(pen, t, s):
    a = stroke_alpha(t, s)
    t_arch, t_sun = s["draw"]
    wash = ease_io((t - t_arch - 0.9) / 1.2)
    if wash > 0:                                   # a warm wash fills the open arch: space
        layer = Image.new("RGBA", pen.im.size, (0, 0, 0, 0))
        ImageDraw.Draw(layer).polygon([(x * SS, y * SS) for x, y in arch_path()], fill=C["gold"] + (int(70 * wash * a),))
        pen.im.alpha_composite(layer)
        pen.used = True
    pen.line(partial(arch_path(), ease_io((t - t_arch) / 1.4)), 8, C["deep_green"], 0.95 * a)
    horizon = 830
    pen.line(partial([(250, horizon), (750, horizon)], ease_io((t - t_sun) / 0.7)), 6, C["gold"], a)
    rise = ease_io((t - t_sun - 0.3) / 1.8)
    if rise > 0:                                   # a low sun rising behind the horizon line
        sun = Pen()
        sun.disc(500, lerp(horizon + 95, horizon - 22, rise), 88, C["rust"], 0.9 * a)
        lay = sun.im
        clip = Image.new("L", lay.size, 0)
        ImageDraw.Draw(clip).rectangle((0, 0, lay.width, (horizon - 3) * SS), fill=255)
        lay.putalpha(Image.composite(lay.getchannel("A"), Image.new("L", lay.size, 0), clip))
        pen.im.alpha_composite(lay)
        pen.used = True


def motif_endcard(pen, t, s):
    p = ease_io((t - (EC["url_at"] + 0.3)) / 1.4)
    pts = curve(lambda u: lerp(250, 750, u), lambda u: hills(u, 1290, 0.0) * 0.35 + 1290 * 0.65)
    pen.line(partial(pts, p), 3, C["gold"], 0.9)


MOTIFS = {"unfinished_stroke": motif_unfinished_stroke, "hills": motif_hills,
          "paint_write_music": motif_paint_write_music, "two_rhythms": motif_two_rhythms,
          "arch_and_sun": motif_arch_and_sun, "endcard": motif_endcard}


def draw_motifs(frame, t):
    pen = Pen()
    s = SCENES[scene_index(t)]
    MOTIFS[s["motif"]](pen, t, s)
    if pen.used:
        frame.alpha_composite(pen.layer())


# ------------------------------------------------------------------ designed text
def tracked(draw, xy, text, fnt, fill, spacing):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += fnt.getlength(ch) + spacing
    return x


def tracked_width(text, fnt, spacing):
    return sum(fnt.getlength(ch) for ch in text) + spacing * (len(text) - 1)


def block_layout(b):
    fnt = title_font(b["size"])
    lh = round(b["size"] * 1.08)
    y = b["y"]
    items = []
    if "label" in b:
        items.append(("label", b["label"], SAFE["x0"], y - 62))
    for ln in b["lines"]:
        items.append(("line", ln, SAFE["x0"], y))
        y += lh
    return fnt, items


def appear(t, at, end, rise=0.5, fall=0.3):
    if at <= 0:                     # visible from the first frame (readable cover frame)
        a_in, dy = 1.0, 0.0
    else:
        a_in = ease((t - at) / rise)
        dy = (1 - a_in) * 18
    a_out = 1 - ease_io((t - (end - fall)) / fall)
    return a_in * a_out, dy


def draw_text(layer, t):
    d = ImageDraw.Draw(layer)
    for b in CFG["text"]:
        if not (b["start"] - 0.01 <= t < b["end"]) and not (b["start"] <= 0 and t < b["end"]):
            continue
        ink, accent, _ = scene_colors(b["start"] + 0.01)
        fnt, items = block_layout(b)
        for kind, it, x, y in items:
            if kind == "label":
                a, dy = appear(t, it["at"], b["end"])
                tracked(d, (x, y + dy), fmt(it["t"]).upper(), F_LABEL, C["gold"] + (int(255 * a),), 5)
                continue
            col = accent if it.get("accent") else ink
            words = it.get("words")
            if words:
                cx = x
                for part, at in zip(it["t"].split("  "), words):
                    a, dy = appear(t, at, b["end"])
                    if a > 0:
                        d.text((cx, y + dy), part, font=fnt, fill=col + (int(255 * a),))
                    cx += fnt.getlength(part + "  ")
            else:
                a, dy = appear(t, it["at"], b["end"])
                if a > 0:
                    d.text((x, y + dy), fmt(it["t"]), font=fnt, fill=col + (int(255 * a),))
        if b["start"] <= 0:         # hook: a gold rule draws itself under the question
            _, ln, x, y = items[-1]
            p = ease_io((t - 0.5) / 1.1)
            a, _ = appear(t, 0, b["end"])
            if p > 0 and a > 0:
                yy = y + round(b["size"] * 1.0)
                d.rounded_rectangle((x, yy, x + fnt.getlength(ln["t"]) * p, yy + 5), 2, fill=C["gold"] + (int(255 * a),))


# ------------------------------------------------------------------ end card
EC = CFG["endcard"]


def endcard_layout():
    els = []
    y = 330
    els.append(("logo", None, y, LOGO.height))
    y += LOGO.height + 30
    if not LOGO_IS_ORIGINAL:
        els.append(("brand", EC["brand_label_with_standin_logo"], y, 30))
        y += 30 + 56
    else:
        y += 26
    els.append(("title", EV["name"], y, 92))
    y += 92 + 52
    els.append(("dates", EV["dates_display"], y, 56))
    y += 56 + 24
    els.append(("place", EV["location_endcard"], y, 42))
    y += 42 + 70
    els.append(("cta", EV["cta"], y, 46 + 2 * 28))
    y += 46 + 2 * 28 + 48
    els.append(("url", EV["website"], y, 42))
    return els


def draw_endcard(frame, layer, t):
    if t < SCENES[-1]["start"]:
        return
    d = ImageDraw.Draw(layer)
    times = {"logo": EC["logo_at"], "brand": EC["logo_at"] + 0.15, "title": EC["title_at"], "dates": EC["dates_at"],
             "place": EC["place_at"], "cta": EC["cta_at"], "url": EC["url_at"]}
    for kind, text, y, h in endcard_layout():
        a = ease((t - times[kind]) / 0.6)
        if a <= 0:
            continue
        dy = (1 - a) * 16
        if kind == "logo":
            lg = LOGO.copy()
            lg.putalpha(lg.getchannel("A").point(lambda v: int(v * a)))
            frame.alpha_composite(lg, (int(CX - LOGO.width / 2), int(y + dy)))
        elif kind == "brand":
            wt = tracked_width(text, F_END_BRAND, 6)
            tracked(d, (CX - wt / 2, y + dy), text, F_END_BRAND, C["sage"] + (int(255 * a),), 6)
        elif kind == "cta":
            tw = F_END_CTA.getlength(text)
            x0 = CX - tw / 2 - 48
            d.rounded_rectangle((x0, y + dy, 2 * CX - x0, y + dy + h), h // 2, fill=C["deep_green"] + (int(255 * a),))
            d.text((CX - tw / 2, y + dy + 26), text, font=F_END_CTA, fill=C["cream"] + (int(255 * a),))
        else:
            fnt, col = {"title": (F_END_TITLE, C["deep_green"]), "dates": (F_END_DATES, C["rust"]),
                        "place": (F_END_PLACE, C["sage"]), "url": (F_END_URL, C["deep_green"])}[kind]
            tw = fnt.getlength(text)
            d.text((CX - tw / 2, y + dy), text, font=fnt, fill=col + (int(255 * a),))


# ------------------------------------------------------------------ captions
CAPS = [dict(c, t=fmt(c["t"])) for c in CFG["captions"]]
CAP_LH = 52
CAP_BOTTOM = CFG["caption_bottom"]


def caption_box(text):
    lines = text.split("\n")
    tw = max(F_CAPTION.getlength(l) for l in lines)
    h = CAP_LH * len(lines) + 30
    x0 = CX - tw / 2 - 26
    return lines, (x0, CAP_BOTTOM - h, 2 * CX - x0, CAP_BOTTOM)


def draw_captions(layer, t):
    d = ImageDraw.Draw(layer)
    _, _, bg = scene_colors(t)
    box, ink = (C["cream"], C["deep_green"]) if bg in ("deep_green", "sage") else (C["deep_green"], C["cream"])
    for c in CAPS:
        if not (c["start"] <= t < c["end"]):
            continue
        a = ease((t - c["start"]) / 0.12) * (1 - ease((t - (c["end"] - 0.12)) / 0.12))
        lines, (x0, y0, x1, y1) = caption_box(c["t"])
        d.rounded_rectangle((x0, y0, x1, y1), 16, fill=box + (int(225 * a),))
        for i, ln in enumerate(lines):
            d.text((CX - F_CAPTION.getlength(ln) / 2, y0 + 14 + i * CAP_LH), ln, font=F_CAPTION, fill=ink + (int(255 * a),))


def write_srt(fn):
    def ts(s):
        ms = int(round(s * 1000))
        return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"
    with open(fn, "w", encoding="utf-8") as f:
        for i, c in enumerate(CAPS, 1):
            f.write(f"{i}\n{ts(c['start'])} --> {ts(c['end'])}\n{c['t']}\n\n")


# ------------------------------------------------------------------ layout check
def text_boxes():
    """(name, x0, y0, x1, y1, t0, t1) of every piece of essential text."""
    boxes = []
    for b in CFG["text"]:
        fnt, items = block_layout(b)
        for kind, it, x, y in items:
            if kind == "label":
                w, hh = tracked_width(fmt(it["t"]).upper(), F_LABEL, 5), 36
            else:
                w, hh = fnt.getlength(fmt(it["t"])), round(b["size"] * 1.05)
            boxes.append((it["t"], x, y, x + w, y + hh, b["start"], b["end"]))
    for kind, text, y, h in endcard_layout():
        if kind == "logo":
            w = LOGO.width
        elif kind == "cta":
            w = F_END_CTA.getlength(text) + 96
        elif kind == "brand":
            w = tracked_width(text, F_END_BRAND, 6)
        else:
            w = {"title": F_END_TITLE, "dates": F_END_DATES, "place": F_END_PLACE, "url": F_END_URL}[kind].getlength(text)
        boxes.append((f"end card {kind}", CX - w / 2, y, CX + w / 2, y + h, SCENES[-1]["start"], DUR))
    return boxes


def check_layout():
    """Fail the build if essential text leaves the safe area, blocks have >2 lines, captions
    collide with designed text, or the CTA is on screen for less than 4 s."""
    x0, x1, y0, y1 = SAFE["x0"], SAFE["x1"], SAFE["y0"], SAFE["y1"]
    problems = []
    boxes = text_boxes()
    for name, bx0, by0, bx1, by1, *_ in boxes:
        if bx0 < x0 or bx1 > x1 or by0 < y0 or by1 > y1:
            problems.append(f"'{name}' ({bx0:.0f},{by0:.0f})-({bx1:.0f},{by1:.0f}) outside safe area")
    for b in CFG["text"]:
        if len(b["lines"]) > 2:
            problems.append(f"text block at {b['start']} has more than two lines")
    for c in CAPS:
        lines, (cx0, cy0, cx1, cy1) = caption_box(c["t"])
        if cx0 < x0 or cx1 > x1 or cy0 < y0 or cy1 > y1 or len(lines) > 2:
            problems.append(f"caption '{c['t']}' outside safe area")
        for name, bx0, by0, bx1, by1, t0, t1 in boxes:
            if c["start"] < t1 and t0 < c["end"] and by1 + 12 > cy0 and by0 < cy1:
                problems.append(f"caption '{c['t']}' overlaps '{name}'")
    cta_shown = DUR - EC["cta_at"]
    if cta_shown < 4.0:
        problems.append(f"CTA visible only {cta_shown:.1f}s")
    if problems:
        raise SystemExit("layout check failed:\n  " + "\n  ".join(problems))
    print(f"layout check ok (CTA visible {cta_shown:.1f}s)")


# ------------------------------------------------------------------ frames
def render(n, captions=False):
    t = n / FPS
    frame = background(t)
    draw_motifs(frame, t)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_endcard(frame, layer, t)
    draw_text(layer, t)
    frame.alpha_composite(layer)
    base = frame.convert("RGB")
    if not captions:
        return base
    cap = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_captions(cap, t)
    frame.alpha_composite(cap)
    return base, frame.convert("RGB")


# ------------------------------------------------------------------ audio
SR = 48000
AU = CFG["audio"]


def read_mono_48k(fn):
    x, sr = sf.read(fn, always_2d=True)
    x = x.mean(1)
    if sr != SR:
        g = math.gcd(sr, SR)
        x = resample_poly(x, SR // g, sr // g)
    return x


def load_music(n):
    """The supplied track from music_source_start, 48 kHz stereo, faded out at the end."""
    raw = subprocess.run([FFMPEG, "-nostdin", "-loglevel", "error", "-ss", str(AU["music_source_start"]), "-t", str(DUR),
                          "-i", path(AU["music"]), "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.float32).reshape(-1, 2).astype(np.float64)[:n]
    x = np.pad(x, ((0, n - len(x)), (0, 0)))
    t = np.arange(n) / SR
    fade = np.clip((DUR - t) / AU["music_fade_out"], 0, 1)
    return x * (np.sin(fade * np.pi / 2) ** 2)[:, None]


def limit(x, ceiling_db=-1.5):
    """Gentle peak limiter: gain dips only around the few peaks above the ceiling."""
    c = 10 ** (ceiling_db / 20)
    need = np.minimum(1.0, c / np.maximum(np.abs(x).max(1), 1e-9))
    g = uniform_filter1d(minimum_filter1d(need, int(0.01 * SR)), int(0.01 * SR))
    y = x * g[:, None]
    peak = np.abs(y).max()
    return y * (c / peak) if peak > c else y


def build_audio(with_vo):
    n = int(SR * DUR)
    meter = pyloudnorm.Meter(SR)
    music = load_music(n)
    m_lufs = meter.integrated_loudness(music)
    if not with_vo:
        return limit(music * 10 ** ((AU["vo_loudness_lufs"] + AU["music_gain_without_vo_db"] - m_lufs) / 20))
    vo = np.zeros(n)
    for clip in CFG["voiceover"]["clips"]:
        x = read_mono_48k(path(os.path.join(AU["vo_dir"], clip["id"] + ".wav")))
        i = int(round(clip["at"] * SR))
        fade = int(0.008 * SR)
        x[:fade] *= np.linspace(0, 1, fade)
        x[-fade:] *= np.linspace(1, 0, fade)
        assert i + len(x) <= n, f"narration clip {clip['id']} runs past the end"
        vo[i:i + len(x)] += x
    vo *= 10 ** ((AU["vo_loudness_lufs"] - meter.integrated_loudness(vo)) / 20)
    # Music sits under the voice and ducks a further duck_db while she speaks.
    g = 10 ** ((AU["vo_loudness_lufs"] + AU["music_gain_db"] - m_lufs) / 20)
    env = uniform_filter1d(np.abs(vo), int(0.05 * SR))
    speaking = uniform_filter1d((env > env.max() * 0.04).astype(float), int(0.35 * SR))
    duck = 10 ** (-AU["duck_db"] * np.clip(speaking * 1.5, 0, 1) / 20)
    return limit(music * (g * duck)[:, None] + vo[:, None])


def audio_report(fn):
    out = subprocess.run([FFMPEG, "-hide_banner", "-nostats", "-i", fn, "-af", "ebur128=peak=true", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    lines = [l.strip() for l in out.splitlines() if l.strip().startswith(("I:", "Peak:"))]
    return " ".join(lines[-2:])


# ------------------------------------------------------------------ contact sheet
SHEET = [(1.5, "0–4 s  Recognition"), (6.9, "4–8 s  Possibility"), (12.0, "8–13 s  Creative freedom"),
         (17.4, "13–18 s  Connection"), (23.0, "18–24 s  The experience"), (28.0, "24–30 s  Invitation")]


def contact_sheet(fn):
    tw, th, pad, head = 360, 640, 24, 54
    sheet = Image.new("RGB", (3 * tw + 4 * pad, 2 * (th + head) + 3 * pad + 70), (255, 255, 255))
    d = ImageDraw.Draw(sheet)
    d.text((pad, 22), f"Tribu del Alma · {EV['name']} · 30 s reel · contact sheet", font=font("title", 34), fill=C["deep_green"])
    for i, (t, label) in enumerate(SHEET):
        x = pad + (i % 3) * (tw + pad)
        y = 70 + pad + (i // 3) * (th + head + pad)
        n = int(round(t * FPS))
        d.text((x, y + 4), label, font=font("body", 20), fill=C["deep_green"])
        d.text((x, y + 28), f"frame {n} · {t:.1f} s", font=font("body", 15), fill=C["sage"])
        sheet.paste(render(n).resize((tw, th), Image.LANCZOS), (x, y + head))
        d.rectangle((x - 1, y + head - 1, x + tw, y + head + th), outline=(210, 206, 190))
    sheet.save(fn)


# ------------------------------------------------------------------ main
def encode_cmd(out, size):
    oh = size * H // W
    return [FFMPEG, "-nostdin", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
            "-r", str(FPS), "-i", "-", "-vf", f"scale={size}:{oh}:flags=lanczos", "-c:v", "libx264", "-preset", "slow",
            "-crf", "16", "-profile:v", "high", "-pix_fmt", "yuv420p", "-color_primaries", "bt709",
            "-color_trc", "bt709", "-colorspace", "bt709", "-r", str(FPS), "-movflags", "+faststart", out]


def mux(video, wav, out):
    subprocess.run([FFMPEG, "-nostdin", "-y", "-loglevel", "error", "-i", video, "-i", wav, "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-ar", str(SR), "-ac", "2", "-t", str(DUR),
                    "-movflags", "+faststart", out], check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=path("out"))
    ap.add_argument("--size", type=int, default=W)
    ap.add_argument("--frames", help="comma-separated frame numbers to save as PNG (QA), then exit")
    ap.add_argument("--sheet-only", action="store_true")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    check_layout()
    if args.frames:
        for n in map(int, args.frames.split(",")):
            base, cap = render(n, captions=True)
            base.save(os.path.join(args.out, f"frame_{n:04d}.png"))
            cap.save(os.path.join(args.out, f"frame_{n:04d}_cap.png"))
        return
    write_srt(os.path.join(args.out, f"{NAME}.srt"))
    contact_sheet(os.path.join(args.out, "contact-sheet.png"))
    if args.sheet_only:
        return
    tmp = tempfile.mkdtemp()
    v_main, v_cap = os.path.join(tmp, "main.mp4"), os.path.join(tmp, "cap.mp4")
    p_main = subprocess.Popen(encode_cmd(v_main, args.size), stdin=subprocess.PIPE)
    p_cap = subprocess.Popen(encode_cmd(v_cap, args.size), stdin=subprocess.PIPE)
    for n in range(TOTAL):
        base, cap = render(n, captions=True)
        p_main.stdin.write(base.tobytes())
        p_cap.stdin.write(cap.tobytes())
        if n % 150 == 0:
            print(f"  frame {n}/{TOTAL}", flush=True)
    for p in (p_main, p_cap):
        p.stdin.close()
        if p.wait():
            raise SystemExit("ffmpeg failed")
    for with_vo, videos in ((True, [(v_main, ""), (v_cap, "-captioned")]), (False, [(v_main, "-music-only")])):
        wav = os.path.join(tmp, f"mix_{with_vo}.wav")
        sf.write(wav, build_audio(with_vo), SR, subtype="PCM_24")
        for v, suffix in videos:
            out = os.path.join(args.out, f"{NAME}{suffix}.mp4")
            mux(v, wav, out)
            print(f"wrote {out}  [{audio_report(out)}]")
    print("logo:", LOGO_PATH)


if __name__ == "__main__":
    main()
