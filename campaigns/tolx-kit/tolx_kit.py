"""TOLX video kit: shared brand, layout, motion and audio-mix code for the TOLX social series.

A video script does:
    import tolx_kit as K
    K.setup(fmt, end_card=..., total=...)       # "reel" (1080x1920) or "feed" (1080x1350)
    ... draw scene layers with K.put / K.put_text / sprites ...
    K.run(args, render, captions, picks, cover_frame)

Brand (from the TOLX WordPress theme): helm logo redrawn from partials/helm.php, gold #D4A843
on #09090B, Poppins headlines (as on the social card), Chakra Petch UI (site font), Share Tech
Mono labels. All layout happens on a 1080x1350 stage; the reel format places it at y=250 so
text clears the Instagram / LinkedIn UI. Frame n is shown at n/30 s.

Lead CTA (contact details from the theme's contact page and footer): discovery call via
tolx.ae/contact or WhatsApp. The site describes "usually 30 minutes for an initial call";
nothing on the site says the call is free, so the video doesn't say so either.
"""
import argparse
import math
import os
import subprocess
import tempfile
from functools import lru_cache

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFilter, ImageFont

KIT = os.path.dirname(os.path.abspath(__file__))
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
FPS = 30
W, SH = 1080, 1350
H, OY = 1920, 250
END_CARD, TOTAL = 810, 960

# ---- brand tokens (theme style.css :root)
BG = (9, 9, 11)
SURFACE = (17, 17, 19)
SURFACE2 = (24, 24, 27)
RAISED = (21, 21, 24)
GOLD = (212, 168, 67)
TEXT = (240, 240, 240)
TEXT2 = (176, 176, 186)          # lighter than theme --text-sec for legibility on video
MUTED = (125, 125, 134)
GREEN = (80, 200, 120)
RED = (235, 100, 90)
BLUE = (120, 170, 230)

SAFE_X0, SAFE_X1, SAFE_Y0, SAFE_Y1 = 70, 1010, 20, 1290
FOOTNOTE = "Illustrative scenario. Not a client project."
CTA_URL = "tolx.ae/contact"
PHONE = "+971 50 986 0063"
CALL_LENGTH = "30-minute"
TAGLINE = "SOFTWARE HOUSE  ·  ODOO PARTNER"
OPTIONS = [("ODOO", "Proven business apps,", "set up for your team"),
           ("CUSTOM SOFTWARE", "Built around exactly", "how you work")]
HEAD_Y = 118


def setup(fmt, end_card, total):
    global H, OY, END_CARD, TOTAL, BG_IMG
    H, OY = (1920, 250) if fmt == "reel" else (1350, 0)
    END_CARD, TOTAL = end_card, total
    BG_IMG = make_bg()


def parse_args(doc):
    ap = argparse.ArgumentParser(description=doc)
    ap.add_argument("--out")
    ap.add_argument("--format", choices=("reel", "feed"), default="reel")
    ap.add_argument("--size", type=int, default=1080, help="output width (1080 final, 540 review)")
    ap.add_argument("--vo", help="placed voiceover wav; music and SFX duck under it")
    ap.add_argument("--video-in", help="reuse an already rendered (silent) video instead of rendering frames")
    ap.add_argument("--music")
    ap.add_argument("--sfx")
    ap.add_argument("--srt", help="write the on-screen copy as SRT")
    ap.add_argument("--storyboard")
    ap.add_argument("--cover")
    ap.add_argument("--frames", help="comma-separated frames to dump as PNG next to --out (no video)")
    return ap.parse_args()


# ---------------------------------------------------------------- primitives
FONT_FILES = {
    "P9": "poppins-latin-900-normal.woff", "P9I": "poppins-latin-900-italic.woff",
    "P8": "poppins-latin-800-normal.woff", "P7": "poppins-latin-700-normal.woff",
    "P5": "poppins-latin-500-normal.woff", "C7": "chakra-petch-latin-700-normal.woff",
    "C6": "chakra-petch-latin-600-normal.woff", "C5": "chakra-petch-latin-500-normal.woff",
    "C4": "chakra-petch-latin-400-normal.woff", "M": "share-tech-mono-latin-400-normal.woff",
}


@lru_cache(None)
def F(key, size):
    return ImageFont.truetype(os.path.join(KIT, "fonts", FONT_FILES[key]), size)


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def lin(n, a, b):
    return clamp((n - a) / max(1, b - a))


def ease(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


def ease_io(x):
    x = clamp(x)
    return 4 * x ** 3 if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2


def back(x, s=1.7):
    x = clamp(x)
    return 1 + (s + 1) * (x - 1) ** 3 + s * (x - 1) ** 2


def window(n, a, b, fin=8, fout=8):
    if n < a or n >= b:
        return 0.0
    return min(ease(lin(n, a, a + fin)), 1 - ease(lin(n, b - fout, b)) if fout else 1.0)


def mix(c1, c2, t):
    return tuple(int(round(a + (b - a) * t)) for a, b in zip(c1, c2))


@lru_cache(None)
def text_sprite(text, fkey, size, color, track=0):
    f = F(fkey, size)
    asc, desc = f.getmetrics()
    widths = [f.getlength(ch) + track for ch in text] if track else None
    w = int(sum(widths)) + 4 if track else int(math.ceil(f.getlength(text))) + 4
    im = Image.new("RGBA", (max(1, w), asc + desc), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if track:
        x = 2
        for ch, cw in zip(text, widths):
            d.text((x, 0), ch, font=f, fill=color)
            x += cw
    else:
        d.text((2, 0), text, font=f, fill=color)
    return im


@lru_cache(None)
def rich_sprite(segments, fkey, size):
    parts = [text_sprite(t, fkey, size, c) for t, c in segments]
    im = Image.new("RGBA", (sum(p.width - 4 for p in parts) + 4, parts[0].height), (0, 0, 0, 0))
    x = 0
    for p in parts:
        im.alpha_composite(p, (x, 0))
        x += p.width - 4
    return im


def wrap(text, fkey, size, maxw):
    f, lines, cur = F(fkey, size), [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if f.getlength(trial) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


@lru_cache(None)
def rrect(w, h, r, fill, outline=None, width=0, ss=3):
    im = Image.new("RGBA", (w * ss, h * ss), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle((0, 0, w * ss - 1, h * ss - 1), r * ss, fill=fill,
                                         outline=outline, width=width * ss)
    return im.resize((w, h), Image.LANCZOS)


@lru_cache(None)
def circle(d, fill, outline=None, width=0, ss=3):
    im = Image.new("RGBA", (d * ss, d * ss), (0, 0, 0, 0))
    ImageDraw.Draw(im).ellipse((0, 0, d * ss - 1, d * ss - 1), fill=fill, outline=outline, width=width * ss)
    return im.resize((d, d), Image.LANCZOS)


@lru_cache(None)
def glow(w, h, color, radius, alpha):
    pad = radius * 2
    im = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle((pad, pad, pad + w, pad + h), 24, fill=color + (alpha,))
    return im.filter(ImageFilter.GaussianBlur(radius)), pad


def fade_sprite(sp, a):
    if a >= 0.999:
        return sp
    sp = sp.copy()
    sp.putalpha(sp.getchannel("A").point(lambda v: int(v * a)))
    return sp


LAYOUT = []
CHECKING = False


def put(frame, sp, x, y, anchor="tl", a=1.0, s=1.0, text=False):
    """Composite a sprite at stage coords. anchor: t/c/b + l/c/r."""
    if a <= 0.004 or s <= 0.01:
        return
    if abs(s - 1) > 0.002:
        sp = sp.resize((max(1, int(sp.width * s)), max(1, int(sp.height * s))), Image.BILINEAR)
    sp = fade_sprite(sp, a)
    vx = {"l": 0, "c": sp.width / 2, "r": sp.width}[anchor[1]]
    vy = {"t": 0, "c": sp.height / 2, "b": sp.height}[anchor[0]]
    px, py = int(round(x - vx)), int(round(y - vy))
    if CHECKING and text:
        LAYOUT.append((px, py, px + sp.width, py + sp.height))
    py += OY
    x0, y0 = max(0, -px), max(0, -py)
    if x0 >= sp.width or y0 >= sp.height:
        return
    if x0 or y0:
        sp = sp.crop((x0, y0, sp.width, sp.height))
    frame.alpha_composite(sp, (px + x0, py + y0))


def put_text(frame, text, fkey, size, color, x, y, anchor="tl", a=1.0, s=1.0, track=0):
    put(frame, text_sprite(text, fkey, size, color, track), x, y, anchor, a, s, text=True)


# ---------------------------------------------------------------- brand
@lru_cache(None)
def helm(size, color=GOLD):
    """TOLX helm from partials/helm.php (80x80 viewBox), drawn at 4x for anti-aliasing."""
    ss = 4
    k = size * ss / 80
    im = Image.new("RGBA", (size * ss, size * ss), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)

    def ring(cx, cy, r, w):
        d.ellipse(((cx - r - w / 2) * k, (cy - r - w / 2) * k, (cx + r + w / 2) * k, (cy + r + w / 2) * k),
                  outline=color, width=max(1, int(w * k)))

    def ell(cx, cy, rx, ry, rot=0):
        c, s_ = math.cos(math.radians(rot)), math.sin(math.radians(rot))
        pts = []
        for i in range(48):
            t = 2 * math.pi * i / 48
            ex, ey = rx * math.cos(t), ry * math.sin(t)
            pts.append(((cx + ex * c - ey * s_) * k, (cy + ex * s_ + ey * c) * k))
        d.polygon(pts, fill=color)

    ring(40, 40, 30, 5)
    ring(40, 40, 7, 4)
    for x1, y1, x2, y2, w in [(40, 10, 40, 33, 3.5), (40, 47, 40, 70, 3.5), (10, 40, 33, 40, 3.5),
                              (47, 40, 70, 40, 3.5), (18.8, 18.8, 35.1, 35.1, 3), (44.9, 44.9, 61.2, 61.2, 3),
                              (61.2, 18.8, 44.9, 35.1, 3), (35.1, 44.9, 18.8, 61.2, 3)]:
        d.line((x1 * k, y1 * k, x2 * k, y2 * k), fill=color, width=max(1, int(w * k)))
    for cx, cy, rx, ry, rot in [(40, 3, 3.5, 5, 0), (40, 77, 3.5, 5, 0), (3, 40, 5, 3.5, 0), (77, 40, 5, 3.5, 0),
                                (66, 14, 3.2, 4.5, -45), (14, 14, 3.2, 4.5, 45), (66, 66, 3.2, 4.5, 45),
                                (14, 66, 3.2, 4.5, -45)]:
        ell(cx, cy, rx, ry, rot)
    return im.resize((size, size), Image.LANCZOS)


@lru_cache(None)
def wordmark(size):
    return rich_sprite((("TOLX", TEXT), (".", GOLD)), "C7", size)


def brand_lockup(frame, x, y, hsize, wsize, a=1.0):
    put(frame, helm(hsize), x, y, "cl", a)
    put(frame, wordmark(wsize), x + hsize + int(hsize * 0.28), y + wsize * 0.04, "cl", a, text=True)


@lru_cache(None)
def label_chip(text):
    ts = text_sprite(text, "M", 21, GOLD, 2)
    im = rrect(ts.width + 30, 40, 20, GOLD + (22,), GOLD + (110,), 1).copy()
    im.alpha_composite(ts, (15, (40 - ts.height) // 2 + 1))
    return im


@lru_cache(None)
def q_chip(q, fill=GOLD, color=BG):
    ts = text_sprite(q, "P7", 40, color)
    w, h = ts.width + 64, 86
    im = rrect(w, h, 43, fill + (255,)).copy()
    im.alpha_composite(ts, (32, (h - ts.height) // 2 + 2))
    return im


@lru_cache(None)
def pill(lab, color=GOLD, size=26):
    ts = text_sprite(lab, "M", size, color, 2)
    h = size + 22
    im = rrect(ts.width + 34, h, h // 2, color + (36,), color + (160,), 2).copy()
    im.alpha_composite(ts, (17, (h - ts.height) // 2 + 1))
    return im


# ---------------------------------------------------------------- background
def make_bg():
    im = Image.new("RGB", (W, H + 120), BG)
    d = ImageDraw.Draw(im)
    line = mix(BG, (255, 255, 255), 0.035)
    for x in range(0, W + 1, 60):
        d.line((x, 0, x, H + 120), fill=line)
    for y in range(0, H + 121, 60):
        d.line((0, y, W, y), fill=line)
    return im.convert("RGBA")


BG_IMG = None
GLOW_IMG = Image.new("RGBA", (900, 900), (0, 0, 0, 0))
ImageDraw.Draw(GLOW_IMG).ellipse((150, 150, 750, 750), fill=GOLD + (60,))
GLOW_IMG = GLOW_IMG.filter(ImageFilter.GaussianBlur(150))


def background(n):
    off = int((n * 0.6) % 60)
    frame = BG_IMG.crop((0, off, W, off + H)).copy()
    gx = W / 2 + 140 * math.sin(n / 160)
    gy = OY + 330 + 60 * math.cos(n / 210) + 100 * ease_io(lin(n, END_CARD - 20, END_CARD + 20))
    frame.alpha_composite(GLOW_IMG, (int(gx - 450), int(gy - 450)))
    return frame


# ---------------------------------------------------------------- headlines + steps
def draw_headlines(frame, n, headlines):
    """headlines: (start, end, lines); each line a tuple of (text, color) segments."""
    for a, b, lines in headlines:
        if a <= n < b:
            fin, fout = ease(lin(n, a, a + 9)), 1 - ease(lin(n, b - 7, b))
            for i, segs in enumerate(lines):
                t = ease(lin(n, a + 4 * i, a + 4 * i + 10))
                put(frame, rich_sprite(segs, "P8", 74), W / 2, HEAD_Y + i * 92 + 24 * (1 - t), "tc",
                    a=min(fin, t, fout), text=True)


def draw_steps(frame, n, steps, labels):
    """steps: (start, end, number, title, one-line subtitle). Draws headline + progress rail."""
    for a, b, num, title, sub in steps:
        if a <= n < b:
            t = ease(lin(n, a, a + 10))
            al = min(t, 1 - ease(lin(n, b - 7, b)))
            put(frame, rich_sprite(((num + "  ", GOLD), (title, TEXT)), "P8", 74), W / 2, HEAD_Y + 20 * (1 - t), "tc",
                a=al, text=True)
            put_text(frame, sub, "C5", 38, TEXT2, W / 2, HEAD_Y + 106, "tc", a=min(al, ease(lin(n, a + 6, a + 16))))
    s0, s1 = steps[0][0], steps[-1][1]
    if s0 <= n < s1:
        al = min(ease(lin(n, s0, s0 + 10)), 1 - ease(lin(n, s1 - 8, s1)))
        x0, x1, y = 140, 940, 318
        seg = (x1 - x0) / len(labels)
        cur = sum(n >= st[0] for st in steps) - 1
        for i, lab in enumerate(labels):
            sx = x0 + i * seg
            active = i <= cur
            prog = ease(lin(n, steps[i][0], steps[i][0] + 12)) if i == cur else (1.0 if active else 0.0)
            put(frame, rrect(int(seg - 14), 6, 3, (48, 48, 54)), sx + 7, y, "tl", al)
            if prog > 0:
                put(frame, rrect(max(6, int((seg - 14) * prog)), 6, 3, GOLD), sx + 7, y, "tl", al)
            put_text(frame, lab, "M", 22, GOLD if active else MUTED, sx + seg / 2, y + 18, "tc", a=al, track=2)


# ---------------------------------------------------------------- statement + end card
@lru_cache(None)
def option_card(title, l1, l2):
    w, h = 420, 230
    im = rrect(w, h, 24, RAISED + (255,), GOLD + (200,), 2).copy()
    ts = text_sprite(title, "M", 34, GOLD, 3)
    im.alpha_composite(ts, ((w - ts.width) // 2, 40))
    ImageDraw.Draw(im).line((60, 100, w - 60, 100), fill=GOLD + (90,), width=2)
    for i, ln in enumerate((l1, l2)):
        t2 = text_sprite(ln, "C5", 32, TEXT)
        im.alpha_composite(t2, ((w - t2.width) // 2, 122 + i * 42))
    return im


def draw_statement(frame, n, start, lines, beats):
    """'Ready to move beyond X?' + Odoo / custom-software cards. beats: frames for card1, card2, sub."""
    if not (start <= n < END_CARD + 6):
        return
    out = 1 - ease(lin(n, END_CARD - 4, END_CARD + 6))
    for i, segs in enumerate(lines):
        t = ease(lin(n, start + 3 * i, start + 3 * i + 12))
        put(frame, rich_sprite(segs, "P8", 74), W / 2, 250 + i * 94 + 24 * (1 - t), "tc", a=min(t, out), text=True)
    for k in range(2):
        t = lin(n, beats[k], beats[k] + 12)
        put(frame, option_card(*OPTIONS[k]), [300, 780][k], 640, "cc", a=min(ease(t * 1.5), out),
            s=0.7 + 0.3 * back(t, 2.0))
    put_text(frame, "or", "P7", 40, GOLD, W / 2, 640, "cc", a=min(ease(lin(n, beats[1] - 4, beats[1] + 6)), out))
    put_text(frame, "Sized to your workflow and budget.", "C5", 38, TEXT2, W / 2, 820, "tc",
             a=min(ease(lin(n, beats[2], beats[2] + 14)), out))


@lru_cache(None)
def cta_button():
    ts = text_sprite(CTA_URL, "C7", 48, BG)
    w = ts.width + 140
    im = rrect(w, 100, 50, GOLD + (255,)).copy()
    im.alpha_composite(ts, (44, (100 - ts.height) // 2 + 2))
    d = ImageDraw.Draw(im)
    ax = 44 + ts.width + 22                          # arrow drawn (the font subset has no U+2192)
    d.line((ax, 50, ax + 40, 50), fill=BG, width=6)
    d.line((ax + 24, 34, ax + 41, 50), fill=BG, width=6)
    d.line((ax + 24, 66, ax + 41, 50), fill=BG, width=6)
    return im


def draw_end_card(frame, n):
    if n < END_CARD:
        return
    e = END_CARD
    t = lin(n, e, e + 20)
    hm = helm(190).rotate(-90 * (1 - ease(t)), resample=Image.BICUBIC)
    put(frame, hm, W / 2, 230, "cc", a=ease(t * 1.4), s=0.8 + 0.2 * ease(t))
    put(frame, wordmark(104), W / 2, 400, "cc", a=ease(lin(n, e + 8, e + 20)), text=True)
    put_text(frame, TAGLINE, "M", 26, GOLD, W / 2, 462, "tc", a=ease(lin(n, e + 14, e + 26)), track=3)
    a2 = ease(lin(n, e + 20, e + 32))
    put(frame, rich_sprite((("Book a ", TEXT), (CALL_LENGTH, GOLD)), "P8", 64), W / 2, 580, "tc", a=a2, text=True)
    put(frame, rich_sprite((("discovery call", GOLD),), "P8", 64), W / 2, 662, "tc", a=a2, text=True)
    put_text(frame, "We map your workflow and suggest the right fit.", "C5", 34, TEXT2, W / 2, 762, "tc",
             a=ease(lin(n, e + 28, e + 40)))
    a3 = lin(n, e + 36, e + 48)
    put(frame, cta_button(), W / 2, 912, "cc", a=ease(a3 * 1.3), s=0.85 + 0.15 * back(a3, 2.0))
    put_text(frame, f"or WhatsApp {PHONE}", "C6", 38, TEXT, W / 2, 1000, "tc", a=ease(lin(n, e + 46, e + 58)))


def draw_chrome(frame, n, illustrative_from):
    brand_lockup(frame, SAFE_X0 + 10, 56, 44, 34, window(n, 0, END_CARD + 4, 10, 8))
    if illustrative_from <= n < END_CARD:
        put(frame, label_chip("ILLUSTRATIVE WORKFLOW"), SAFE_X1 - 10, 56, "cr",
            a=window(n, illustrative_from, END_CARD, 10, 8), text=True)
    put_text(frame, FOOTNOTE, "M", 22, MUTED, W / 2, 1258, "tc", a=window(n, 6, TOTAL + 1, 10, 0), track=1)


# ---------------------------------------------------------------- output
def check_layout(render):
    global CHECKING
    CHECKING = True
    bad = []
    for n in range(0, TOTAL, 5):
        LAYOUT.clear()
        render(n)
        for x0, y0, x1, y1 in LAYOUT:
            if x0 < SAFE_X0 - 2 or x1 > SAFE_X1 + 2 or y0 < SAFE_Y0 or y1 > SAFE_Y1:
                bad.append((n, (x0, y0, x1, y1)))
    CHECKING = False
    if bad:
        raise SystemExit(f"text outside safe area: {bad[:8]} ({len(bad)} total)")
    print("layout ok")


def write_srt(path, captions):
    def ts(f):
        ms = int(round(f / FPS * 1000))
        return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"
    with open(path, "w", encoding="utf-8") as fh:
        for i, (a, b, text) in enumerate(captions, 1):
            fh.write(f"{i}\n{ts(a)} --> {ts(b)}\n{text}\n\n")


def mux_audio(args, video, out):
    """Voice loudness-matched (-16 LUFS stem); music/SFX lowered and side-chain ducked under it
    (measured ~10-20 dB voice-over-bed on video 01); whole mix normalised to about -14 LUFS."""
    dur = TOTAL / FPS
    inputs, chains, labels, idx = ["-i", video], [], [], 1
    if args.vo:
        inputs += ["-i", args.vo]
        chains.append(f"[{idx}:a]aresample=48000,highpass=f=80,acompressor=threshold=0.1:ratio=3:attack=5:release=120,"
                      f"loudnorm=I=-16:TP=-2:LRA=7,aresample=48000,apad=whole_dur={dur},asplit[vo][key]")
        idx += 1
    for name, path, gain in (("mu", args.music, -7.5 if args.vo else -2), ("fx", args.sfx, -7 if args.vo else -4)):
        if path:
            inputs += ["-i", path]
            chains.append(f"[{idx}:a]aresample=48000,volume={gain}dB[{name}]")
            labels.append(f"[{name}]")
            idx += 1
    chains.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0[bed]")
    if args.vo:
        chains.append("[bed][key]sidechaincompress=threshold=0.08:ratio=3:attack=15:release=350[duck]")
        chains.append("[vo][duck]amix=inputs=2:normalize=0[pre]")
    else:
        chains.append("[bed]anull[pre]")
    chains.append("[pre]loudnorm=I=-14:TP=-1.5:LRA=9,aresample=48000[aout]")
    subprocess.run([FFMPEG, "-nostdin", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(chains),
                    "-map", "0:v", "-map", "[aout]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                    "-ac", "2", "-t", str(dur), "-movflags", "+faststart", out], check=True)


def storyboard(path, render, picks):
    tw = 216
    th = tw * H // W
    f = F("C6", 16)
    rows = (len(picks) + 4) // 5
    sheet = Image.new("RGB", (5 * (tw + 12) + 12, rows * (th + 40) + 12), (255, 255, 255))
    d = ImageDraw.Draw(sheet)
    for i, (n, text) in enumerate(picks):
        x, y = 12 + (i % 5) * (tw + 12), 12 + (i // 5) * (th + 40)
        sheet.paste(render(n).resize((tw, th), Image.LANCZOS), (x, y + 28))
        d.text((x, y + 4), f"f{n} ({n / FPS:.1f}s) {text}", font=f, fill=(0, 0, 0))
    sheet.save(path)


def run(args, render, captions, picks, cover_frame):
    check_layout(render)
    if args.srt:
        write_srt(args.srt, captions)
    if args.storyboard:
        storyboard(args.storyboard, render, picks)
    if args.cover:
        render(cover_frame).save(args.cover)
    if args.frames:
        base = os.path.splitext(args.out or "frame")[0]
        for n in map(int, args.frames.split(",")):
            render(n).save(f"{base}_f{n:03d}.png")
        return
    if not args.out:
        return
    has_audio = args.music or args.sfx or args.vo
    if args.video_in:
        mux_audio(args, args.video_in, args.out)
        return
    video = tempfile.mktemp(suffix=".mp4") if has_audio else args.out
    ow = args.size
    oh = ow * H // W // 2 * 2
    proc = subprocess.Popen([FFMPEG, "-nostdin", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                             "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-vf", f"scale={ow}:{oh}:flags=lanczos",
                             "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                             "-movflags", "+faststart", video], stdin=subprocess.PIPE)
    for n in range(TOTAL):
        proc.stdin.write(render(n).tobytes())
    proc.stdin.close()
    if proc.wait():
        raise SystemExit("ffmpeg failed")
    if has_audio:
        mux_audio(args, video, args.out)
        os.remove(video)
