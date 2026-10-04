"""Compose the 30 s TOLX video "WhatsApp orders without losing track".

Motion-graphics only (no stock footage, no photos of people, no real client data).
The chat, order card and board are an ILLUSTRATIVE workflow, labelled as such on screen;
they do not depict a TOLX client, a shipped product or a native WhatsApp integration.
Brand: TOLX helm drawn from the theme's SVG geometry (partials/helm.php), gold #D4A843 on
#09090B, Poppins headlines (as on the social card), Chakra Petch UI, Share Tech Mono labels.

Everything is laid out on a 1080x1350 "stage". --format feed renders the stage as-is (4:5,
LinkedIn / Instagram feed); --format reel puts it on a 1080x1920 canvas (9:16, Reels /
Stories / LinkedIn vertical) at y=250 so text clears the platform UI.
Frame n (zero-based) is shown at n/30 s; 900 frames.

Usage:
  python compose_tolx.py --out video.mp4 [--format reel|feed] [--size 540]
         [--music audio/music.wav] [--sfx audio/sfx.wav] [--srt captions.srt]
         [--storyboard sheet.png] [--cover cover.png] [--frames 0,120,600]
"""
import argparse
import math
import os
import subprocess
import tempfile
from functools import lru_cache

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from timeline import *  # noqa: F401,F403  (frame constants shared with the audio script)

HERE = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument("--out")
ap.add_argument("--format", choices=("reel", "feed"), default="reel")
ap.add_argument("--size", type=int, default=1080, help="output width (1080 final, 540 review)")
ap.add_argument("--music")
ap.add_argument("--sfx")
ap.add_argument("--srt")
ap.add_argument("--storyboard")
ap.add_argument("--cover")
ap.add_argument("--frames", help="comma-separated frames to dump as PNG next to --out (no video)")
ARGS = ap.parse_args()

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
W, SH = 1080, 1350                                  # stage
H, OY = (1920, 250) if ARGS.format == "reel" else (1350, 0)

# ---- brand tokens (theme style.css :root)
BG = (9, 9, 11)
SURFACE = (17, 17, 19)
SURFACE2 = (24, 24, 27)
RAISED = (21, 21, 24)
GOLD = (212, 168, 67)
GOLD_HI = (224, 184, 78)
TEXT = (240, 240, 240)
TEXT2 = (176, 176, 186)          # lighter than theme --text-sec for legibility on video
MUTED = (125, 125, 134)
GREEN = (80, 200, 120)

# important text stays inside this stage box (check_layout fails the build otherwise)
SAFE_X0, SAFE_X1, SAFE_Y0, SAFE_Y1 = 70, 1010, 20, 1290

FOOTNOTE = "Illustrative scenario. Not a client project."
GUIDE_TITLE = "How to manage WhatsApp orders without losing track"
CTA_URL = "tolx.ae/blog"          # change to the article URL once the guide is published


# ---------------------------------------------------------------- helpers
FONT_FILES = {
    "P8": "poppins-latin-800-normal.woff", "P7": "poppins-latin-700-normal.woff",
    "P5": "poppins-latin-500-normal.woff", "C7": "chakra-petch-latin-700-normal.woff",
    "C6": "chakra-petch-latin-600-normal.woff", "C5": "chakra-petch-latin-500-normal.woff",
    "C4": "chakra-petch-latin-400-normal.woff", "M": "share-tech-mono-latin-400-normal.woff",
}


@lru_cache(None)
def F(key, size):
    return ImageFont.truetype(os.path.join(HERE, "fonts", FONT_FILES[key]), size)


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
    """Opacity for something visible from frame a to b with fades."""
    if n < a or n >= b:
        return 0.0
    return min(ease(lin(n, a, a + fin)), 1 - ease(lin(n, b - fout, b)) if fout else 1.0)


def mix(c1, c2, t):
    return tuple(int(round(a + (b - a) * t)) for a, b in zip(c1, c2))


@lru_cache(None)
def text_sprite(text, fkey, size, color, track=0):
    f = F(fkey, size)
    asc, desc = f.getmetrics()
    if track:
        widths = [f.getlength(ch) + track for ch in text]
        w = int(sum(widths)) + 4
    else:
        w = int(math.ceil(f.getlength(text))) + 4
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
    """segments: tuple of (text, color) drawn on one line."""
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
    """Anti-aliased rounded rectangle sprite (drawn at ss x then downsampled)."""
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


LAYOUT = []        # text boxes recorded for check_layout()
CHECKING = False


def put(frame, sp, x, y, anchor="tl", a=1.0, s=1.0, text=False):
    """Composite sprite at stage coords. anchor: t/c/b + l/c/r."""
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
    frame.alpha_composite(sp, (px, py + OY)) if px >= 0 and py + OY >= 0 else paste_clipped(frame, sp, px, py + OY)


def paste_clipped(frame, sp, px, py):
    x0, y0 = max(0, -px), max(0, -py)
    if x0 >= sp.width or y0 >= sp.height:
        return
    frame.alpha_composite(sp.crop((x0, y0, sp.width, sp.height)), (px + x0, py + y0))


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

    def line(x1, y1, x2, y2, w):
        d.line((x1 * k, y1 * k, x2 * k, y2 * k), fill=color, width=max(1, int(w * k)))

    def ell(cx, cy, rx, ry, rot=0):
        pts = []
        for i in range(48):
            t = 2 * math.pi * i / 48
            ex, ey = rx * math.cos(t), ry * math.sin(t)
            c, s_ = math.cos(math.radians(rot)), math.sin(math.radians(rot))
            pts.append(((cx + ex * c - ey * s_) * k, (cy + ex * s_ + ey * c) * k))
        d.polygon(pts, fill=color)

    ring(40, 40, 30, 5)
    ring(40, 40, 7, 4)
    for x1, y1, x2, y2, w in [(40, 10, 40, 33, 3.5), (40, 47, 40, 70, 3.5), (10, 40, 33, 40, 3.5),
                              (47, 40, 70, 40, 3.5), (18.8, 18.8, 35.1, 35.1, 3), (44.9, 44.9, 61.2, 61.2, 3),
                              (61.2, 18.8, 44.9, 35.1, 3), (35.1, 44.9, 18.8, 61.2, 3)]:
        line(x1, y1, x2, y2, w)
    for cx, cy, rx, ry, rot in [(40, 3, 3.5, 5, 0), (40, 77, 3.5, 5, 0), (3, 40, 5, 3.5, 0), (77, 40, 5, 3.5, 0),
                                (66, 14, 3.2, 4.5, -45), (14, 14, 3.2, 4.5, 45), (66, 66, 3.2, 4.5, 45),
                                (14, 66, 3.2, 4.5, -45)]:
        ell(cx, cy, rx, ry, rot)
    return im.resize((size, size), Image.LANCZOS)


@lru_cache(None)
def wordmark(size):
    """'TOLX' + gold '.' in Chakra Petch 700, as in header.php."""
    return rich_sprite((("TOLX", TEXT), (".", GOLD)), "C7", size)


def brand_lockup(frame, x, y, hsize, wsize, a=1.0, anchor_center=False, rot=0.0):
    hm = helm(hsize)
    if rot:
        hm = hm.rotate(rot, resample=Image.BICUBIC)
    wm = wordmark(wsize)
    gap = int(hsize * 0.28)
    total = hsize + gap + wm.width
    x0 = x - total / 2 if anchor_center else x
    put(frame, hm, x0, y, "cl", a)
    put(frame, wm, x0 + hsize + gap, y + wsize * 0.04, "cl", a, text=True)


# ---------------------------------------------------------------- background
def make_bg():
    im = Image.new("RGB", (W, H + 120), BG)
    d = ImageDraw.Draw(im)
    line = mix(BG, (255, 255, 255), 0.035)          # faint grid, as on the social card
    for x in range(0, W + 1, 60):
        d.line((x, 0, x, H + 120), fill=line)
    for y in range(0, H + 121, 60):
        d.line((0, y, W, y), fill=line)
    return im.convert("RGBA")


BG_IMG = make_bg()
GLOW_IMG = Image.new("RGBA", (900, 900), (0, 0, 0, 0))
ImageDraw.Draw(GLOW_IMG).ellipse((150, 150, 750, 750), fill=GOLD + (60,))
GLOW_IMG = GLOW_IMG.filter(ImageFilter.GaussianBlur(150))


def background(n):
    off = int((n * 0.6) % 60)
    frame = BG_IMG.crop((0, off, W, off + H)).copy()
    gx = W / 2 + 140 * math.sin(n / 160)
    gy = OY + 330 + 60 * math.cos(n / 210)
    # the glow rises toward the centre for the end card
    gy += (430 - 330) * ease_io(lin(n, END_CARD - 20, END_CARD + 20))
    frame.alpha_composite(GLOW_IMG, (int(gx - 450), int(gy - 450)))
    return frame


# ---------------------------------------------------------------- headlines
# (start, end, lines). each line: tuple of (text, color) segments.
HEADLINES = [
    (6, KEY_IN - 6, ((("Taking orders", TEXT),), (("on ", TEXT), ("WhatsApp?", GOLD)))),
    (KEY_IN - 6, QUESTIONS - 4, ((("Here's the ", TEXT), ("order.", GOLD)),)),
    (BURY + 22, QUESTIONS - 4, ((("Here's the ", TEXT), ("order.", GOLD)), (("Now find it.", TEXT),))),
    (QUESTIONS - 4, TURN + 4, ((("Buried in", TEXT),), (("the group chat.", GOLD),))),
    (TURN + 4, STEP_LOG - 2, ((("Give every order", TEXT),), (("a place to live.", GOLD),))),
]
STEPS = [
    (STEP_LOG, STEP_ASSIGN, "1", "Log it", "Record every order in one shared list."),
    (STEP_ASSIGN, STEP_TRACK, "2", "Assign it", "One person owns it, so nobody has to guess."),
    (STEP_TRACK, STEP_FOLLOW, "3", "Track it", "Everyone sees the status without asking."),
    (STEP_FOLLOW, STATEMENT, "4", "Follow up", "The next step has a name and a date."),
]
HEAD_Y = 118


def draw_headline(frame, n):
    for a, b, lines in HEADLINES:
        if a <= n < b:
            # lines appear one after another; the whole block fades out
            fin = ease(lin(n, a, a + 9))
            fout = 1 - ease(lin(n, b - 7, b))
            for i, segs in enumerate(lines):
                t = ease(lin(n, a + 4 * i, a + 4 * i + 10))
                put(frame, rich_sprite(segs, "P8", 74), W / 2, HEAD_Y + i * 92 + 24 * (1 - t), "tc",
                    a=min(fin, t, fout), text=True)
    for a, b, num, title, sub in STEPS:
        if a <= n < b:
            t = ease(lin(n, a, a + 10))
            fout = 1 - ease(lin(n, b - 7, b)) if b != STATEMENT else 1 - ease(lin(n, b - 8, b))
            al = min(t, fout)
            head = rich_sprite(((num + "  ", GOLD), (title, TEXT)), "P8", 74)
            put(frame, head, W / 2, HEAD_Y + 20 * (1 - t), "tc", a=al, text=True)
            for i, ln in enumerate(wrap(sub, "C5", 38, 820)):
                put_text(frame, ln, "C5", 38, TEXT2, W / 2, HEAD_Y + 106 + i * 48, "tc",
                         a=min(al, ease(lin(n, a + 6, a + 16))))
    # progress rail for the four steps
    if STEP_LOG <= n < STATEMENT:
        al = min(ease(lin(n, STEP_LOG, STEP_LOG + 10)), 1 - ease(lin(n, STATEMENT - 8, STATEMENT)))
        labels = ["LOG", "ASSIGN", "TRACK", "FOLLOW UP"]
        x0, x1, y = 140, 940, 318
        seg = (x1 - x0) / 4
        cur = sum(n >= s[0] for s in STEPS) - 1
        for i, lab in enumerate(labels):
            sx = x0 + i * seg
            active = i <= cur
            fill = GOLD if active else (48, 48, 54)
            prog = ease(lin(n, STEPS[i][0], STEPS[i][0] + 12)) if i == cur else (1.0 if active else 0.0)
            put(frame, rrect(int(seg - 14), 6, 3, (48, 48, 54)), sx + 7, y, "tl", al)
            if prog > 0:
                put(frame, rrect(max(6, int((seg - 14) * prog)), 6, 3, fill), sx + 7, y, "tl", al)
            put_text(frame, lab, "M", 22, GOLD if active else MUTED, sx + seg / 2, y + 18, "tc", a=al, track=2)


# ---------------------------------------------------------------- phone + chat
PX, PY, PW, PH = 300, 372, 480, 856          # phone body (stage coords)
SCR_X, SCR_Y, SCR_W, SCR_H = PX + 14, PY + 14, PW - 28, PH - 28
CHAT_TOP = SCR_Y + 104                       # below the in-app header
CHAT_BOTTOM = SCR_Y + SCR_H - 84             # above the input bar
SENDER_COL = {"Ravi": (120, 170, 230), "Ali": (226, 136, 110), "Sara": (150, 205, 140)}


@lru_cache(None)
def bubble(sender, text, key=False):
    you = sender == "You"
    maxw = 326
    lines = wrap(text, "C5", 27, maxw - 36)
    tw = max(F("C5", 27).getlength(l) for l in lines)
    name_h = 0 if you else 30
    w = int(max(tw, 0 if you else F("C6", 22).getlength(sender)) + 36)
    h = int(name_h + 36 * len(lines) + 26)
    fill = (70, 56, 24, 255) if you else (32, 32, 37, 255)
    outline = GOLD + (255,) if key else None
    im = rrect(w, h, 20, fill, outline, 3 if key else 0).copy()
    if not you:
        im.alpha_composite(text_sprite(sender, "C6", 22, SENDER_COL.get(sender, GOLD)), (16, 10))
    for i, l in enumerate(lines):
        im.alpha_composite(text_sprite(l, "C5", 27, TEXT), (16, name_h + 12 + 36 * i))
    return im


GAP = 12
BUBBLES = [(f, s, t, bubble(s, t, i == KEY_INDEX)) for i, (f, s, t) in enumerate(CHAT)]


def chat_positions(n):
    """Bottom-anchored stack. Returns list of (index, y_top, appear_t) for visible bubbles."""
    contrib = [(sp.height + GAP) * ease(lin(n, f, f + 7)) for f, _, _, sp in BUBBLES]
    out, below = [], 0.0
    for i in range(len(BUBBLES) - 1, -1, -1):
        if contrib[i] <= 0:
            continue
        sp = BUBBLES[i][3]
        y = CHAT_BOTTOM - below - sp.height
        out.append((i, y, lin(n, BUBBLES[i][0], BUBBLES[i][0] + 7)))
        below += contrib[i]
    return out


def rewind_offset(n):
    """After the burying, scroll back so the order bubble sits mid-screen."""
    if n < TURN:
        return 0.0
    pos = dict((i, y) for i, y, _ in chat_positions(TURN))
    key_y = pos[KEY_INDEX] + BUBBLES[KEY_INDEX][3].height / 2
    target = SCR_Y + SCR_H / 2 + 40
    return (target - key_y) * ease_io(lin(n, TURN, TURN + 26))


@lru_cache(None)
def phone_shell():
    im = rrect(PW, PH, 58, (28, 28, 32, 255), (70, 70, 78, 255), 2).copy()
    scr = rrect(SCR_W, SCR_H, 46, (13, 13, 15, 255))
    im.alpha_composite(scr, (14, 14))
    return im


@lru_cache(None)
def phone_header():
    im = Image.new("RGBA", (SCR_W, 104), (0, 0, 0, 0))
    im.alpha_composite(rrect(SCR_W, 104, 1, (20, 20, 23, 255)), (0, 0))
    d = ImageDraw.Draw(im)
    d.line((0, 103, SCR_W, 103), fill=(255, 255, 255, 18))
    im.alpha_composite(text_sprite("<", "C6", 30, TEXT2), (14, 40))
    av = circle(48, (45, 45, 52, 255))
    im.alpha_composite(av, (44, 34))
    im.alpha_composite(text_sprite("ST", "C7", 20, GOLD), (54, 45))
    im.alpha_composite(text_sprite("Shop Team", "C7", 27, TEXT), (104, 32))
    im.alpha_composite(text_sprite("Ali, Ravi, Sara, You", "C4", 20, MUTED), (104, 64))
    return im


@lru_cache(None)
def phone_input():
    im = Image.new("RGBA", (SCR_W, 84), (13, 13, 15, 255))
    im.alpha_composite(rrect(SCR_W - 90, 52, 26, (30, 30, 34, 255)), (16, 16))
    im.alpha_composite(text_sprite("Message", "C4", 24, MUTED), (40, 26))
    im.alpha_composite(circle(52, GOLD + (255,)), (SCR_W - 66, 16))
    return im


def draw_phone(frame, n):
    if n >= STEP_LOG + 20:
        return
    # phone recedes once the order lifts out
    t_out = ease_io(lin(n, TURN + 34, STEP_LOG + 18))
    a_phone = 1 - t_out
    s_in = back(lin(n, 0, 14), 1.2) if n < 14 else 1.0
    dy = 60 * t_out
    scr = Image.new("RGBA", (SCR_W, SCR_H), (0, 0, 0, 0))
    off = rewind_offset(n)
    key_box = None
    for i, y, t in chat_positions(n):
        f, sender, text, sp = BUBBLES[i]
        yy = y + off
        if yy > SCR_Y + SCR_H or yy + sp.height < CHAT_TOP - 40:
            continue
        you = sender == "You"
        x = SCR_X + SCR_W - 16 - sp.width if you else SCR_X + 16
        s = 0.7 + 0.3 * back(t, 2.0)
        bs = sp if abs(s - 1) < 0.002 else sp.resize((max(1, int(sp.width * s)), max(1, int(sp.height * s))),
                                                      Image.BILINEAR)
        bx = x + (sp.width - bs.width) * (1 if you else 0)
        by = yy + (sp.height - bs.height)
        if i == KEY_INDEX:
            key_box = (x, yy, sp.width, sp.height)
            if n >= TURN + 30:
                continue            # it has lifted out (drawn by draw_order)
        scr.alpha_composite(fade_sprite(bs, clamp(t * 1.6)), (int(bx - SCR_X), int(by - SCR_Y)))
    # in-app header and input bar sit over the scrolling chat
    scr.alpha_composite(phone_header(), (0, 0))
    scr.alpha_composite(phone_input(), (0, SCR_H - 84))
    mask = rrect(SCR_W, SCR_H, 46, (255, 255, 255, 255)).getchannel("A")
    clipped = Image.new("RGBA", (SCR_W, SCR_H), (0, 0, 0, 0))
    clipped.paste(scr, (0, 0), mask)
    body = phone_shell().copy()
    body.alpha_composite(clipped, (14, 14))
    # dim the chat while the questions are up
    if QUESTIONS <= n < TURN + 30:
        dim = 0.55 * min(ease(lin(n, QUESTIONS, QUESTIONS + 10)), 1 - ease(lin(n, TURN, TURN + 14)))
        shade = Image.new("RGBA", body.size, (0, 0, 0, int(255 * dim)))
        shade.putalpha(Image.eval(body.getchannel("A"), lambda v: int(v * dim)))
        body.alpha_composite(shade)
    put(frame, body, PX + PW / 2, PY + PH / 2 + dy, "cc", a=a_phone, s=s_in * (1 - 0.08 * t_out))
    # gold callout on the order bubble
    if key_box and KEY_IN + 4 <= n < BURY + 30:
        x, y, w, h = key_box
        al = min(ease(lin(n, KEY_IN + 4, KEY_IN + 12)), 1 - ease(lin(n, BURY + 18, BURY + 30)))
        g, pad = glow(w, h, GOLD, 18, 120)
        put(frame, g, x - pad, y - pad, "tl", al * (0.6 + 0.4 * math.sin(n / 4) ** 2))
        put(frame, bubble(*CHAT[KEY_INDEX][1:], True), x, y, "tl", al)
    return key_box


def draw_questions(frame, n):
    qs = ["Who's handling it?", "Was it confirmed?", "Did anyone follow up?"]
    for k, (q, f) in enumerate(zip(qs, QUESTION_FRAMES)):
        if n < f or n >= TURN + 8:
            continue
        t = lin(n, f, f + 10)
        al = min(ease(t * 1.5), 1 - ease(lin(n, TURN - 4, TURN + 8)))
        sp = q_chip(q)
        y = PY + 250 + k * 150
        x = W / 2 + (-60 if k % 2 == 0 else 60)
        put(frame, sp, x, y, "cc", a=al, s=0.6 + 0.4 * back(t, 2.2))


@lru_cache(None)
def q_chip(q):
    ts = text_sprite(q, "P7", 40, BG)
    w, h = ts.width + 64, 86
    im = rrect(w, h, 43, GOLD + (255,)).copy()
    im.alpha_composite(ts, (32, (h - ts.height) // 2 + 2))
    return im


# ---------------------------------------------------------------- order card
CARD_X, CARD_Y, CARD_W, CARD_H = 140, 408, 800, 640
FIELDS = [("CUSTOMER", "Khalid"), ("ITEMS", "12 × phone cases"), ("DELIVERY", "Thursday")]


def typed(text, n, start, cps=1.2):
    k = int(max(0, n - start) * cps)
    return text[:k]


def order_card_full(n):
    im = rrect(CARD_W, CARD_H, 26, RAISED + (255,), GOLD + (90,), 2).copy()
    put_local = lambda sp, x, y: im.alpha_composite(sp, (int(x), int(y)))  # noqa: E731
    put_local(text_sprite("ORDER #1042", "M", 30, GOLD, 3), 40, 34)
    put_local(text_sprite("from Shop Team chat", "C4", 22, MUTED), 40, 76)
    st = status_chip("NEW" if n < MOVE_CONFIRMED else "CONFIRMED")
    if n >= STEP_ASSIGN + 30:
        put_local(st, CARD_W - 40 - st.width, 36)
    ImageDraw.Draw(im).line((40, 124, CARD_W - 40, 124), fill=(255, 255, 255, 22), width=2)
    rows = FIELDS + [("OWNER", None), ("NEXT STEP", None)]
    for r, (lab, val) in enumerate(rows):
        y = 150 + r * 92
        put_local(text_sprite(lab, "M", 22, MUTED, 2), 40, y + 12)
        if lab == "OWNER":
            if n >= STEP_ASSIGN + 8:
                t = back(lin(n, STEP_ASSIGN + 8, STEP_ASSIGN + 20), 2.0)
                av = avatar("S", 48)
                sz = max(1, int(48 * clamp(t, 0, 1.3)))
                put_local(av.resize((sz, sz), Image.BILINEAR), 250 + (48 - sz) / 2, y + (48 - sz) / 2 - 2)
                put_local(text_sprite("Sara", "C6", 34, TEXT), 312, y)
            else:
                put_local(text_sprite("Unassigned", "C4", 32, (90, 90, 98)), 250, y + 2)
        elif lab == "NEXT STEP":
            if n >= STEP_ASSIGN + 38:
                put_local(text_sprite(typed("Confirm stock & time", n, STEP_ASSIGN + 38, 1.4), "C6", 34, TEXT),
                          250, y)
            else:
                put_local(text_sprite("-", "C4", 32, (90, 90, 98)), 250, y + 2)
        else:
            start = STEP_LOG + 10 + r * 20
            s = typed(val, n, start)
            if s:
                put_local(text_sprite(s, "C6", 34, TEXT), 250, y)
            if start <= n < start + len(val) / 1.2 + 6 and (n // 6) % 2 == 0:
                cx = 250 + F("C6", 34).getlength(s) + 6
                ImageDraw.Draw(im).rectangle((cx, y + 6, cx + 3, y + 42), fill=GOLD)
        if r < len(rows) - 1:
            ImageDraw.Draw(im).line((40, y + 74, CARD_W - 40, y + 74), fill=(255, 255, 255, 12), width=1)
    return im


@lru_cache(None)
def status_chip(label):
    col = {"NEW": (120, 170, 230), "CONFIRMED": GOLD, "DELIVERED": GREEN}[label]
    ts = text_sprite(label, "M", 22, col, 2)
    im = rrect(ts.width + 34, 44, 22, col + (36,), col + (150,), 2).copy()
    im.alpha_composite(ts, (17, (44 - ts.height) // 2 + 1))
    return im


@lru_cache(None)
def avatar(letter, d):
    im = circle(d, (150, 205, 140, 255)).copy()
    ts = text_sprite(letter, "C7", int(d * 0.5), BG)
    im.alpha_composite(ts, ((d - ts.width) // 2 + 1, (d - ts.height) // 2))
    return im


# board (step 3)
BOARD_Y, BOARD_H = 400, 560
COLS = ["NEW", "CONFIRMED", "DELIVERED"]
COL_W, COL_GAP = 296, 26
COL_X0 = (W - (3 * COL_W + 2 * COL_GAP)) // 2
MINI_W, MINI_H = COL_W - 28, 172


def col_x(i):
    return COL_X0 + i * (COL_W + COL_GAP)


@lru_cache(None)
def board_column(label):
    im = rrect(COL_W, BOARD_H, 22, SURFACE + (235,), (255, 255, 255, 20), 1).copy()
    im.alpha_composite(text_sprite(label, "M", 24, TEXT2, 2), (20, 20))
    return im


@lru_cache(None)
def ghost_card(title, sub, owner):
    im = rrect(MINI_W, 112, 16, SURFACE2 + (255,), (255, 255, 255, 14), 1).copy()
    im.alpha_composite(text_sprite(title, "C6", 26, (150, 150, 158)), (18, 16))
    im.alpha_composite(text_sprite(sub, "C4", 21, (110, 110, 118)), (18, 52))
    im.alpha_composite(fade_sprite(avatar(owner, 30), 0.6), (MINI_W - 46, 66))
    return im


GHOSTS = {0: [("#1043  Fatima", "3 × chargers")], 1: [("#1039  Omar", "50 × screen guards")],
          2: [("#1036  Priya", "2 × power banks"), ("#1031  Hassan", "6 × cables")]}


@lru_cache(None)
def mini_card(status):
    im = rrect(MINI_W, MINI_H, 18, RAISED + (255,), GOLD + (230,), 3).copy()
    im.alpha_composite(text_sprite("#1042  Khalid", "C7", 28, TEXT), (18, 16))
    im.alpha_composite(text_sprite("12 × phone cases", "C5", 23, TEXT2), (18, 56))
    im.alpha_composite(text_sprite("Due Thu", "M", 21, GOLD, 1), (18, 96))
    im.alpha_composite(avatar("S", 38), (MINI_W - 56, 90))
    im.alpha_composite(status_chip(status).resize((int(status_chip(status).width * 0.8), 35), Image.LANCZOS),
                       (18, 126))
    return im


def board_slot(i, row):
    return col_x(i) + 14, BOARD_Y + 70 + row * 124


def draw_order(frame, n):
    """The order: lifted bubble -> full card (steps 1-2) -> mini card on the board (3-4)."""
    if n < TURN + 30 or n >= STATEMENT + 10:
        return
    # 1) lift: bubble flies from its chat position into the card slot
    kb = BUBBLES[KEY_INDEX][3]
    pos = dict((i, y) for i, y, _ in chat_positions(TURN))
    bx0 = SCR_X + 16
    by0 = pos[KEY_INDEX] + rewind_offset(TURN + 40)
    t_lift = ease_io(lin(n, TURN + 30, STEP_LOG + 4))
    if n < STEP_LOG + 4:
        cx = bx0 + kb.width / 2 + (W / 2 - bx0 - kb.width / 2) * t_lift
        cy = by0 + kb.height / 2 + (CARD_Y + CARD_H / 2 - by0 - kb.height / 2) * t_lift
        sx = 1 + (CARD_W / kb.width - 1) * t_lift
        sy = 1 + (CARD_H / kb.height - 1) * t_lift
        if t_lift < 0.6:
            g, pad = glow(kb.width, kb.height, GOLD, 22, 140)
            put(frame, g, cx - kb.width / 2 - pad, cy - kb.height / 2 - pad, "tl", 1 - t_lift)
        card = order_card_full(n)
        w, h = int(kb.width * sx), int(kb.height * sy)
        body = rrect(max(8, w), max(8, h), int(20 + 6 * t_lift), RAISED + (255,), GOLD + (200,), 3)
        put(frame, body, cx, cy, "cc")
        put(frame, kb, cx, cy, "cc", a=1 - ease(lin(n, TURN + 30, TURN + 46)), s=min(sx, sy))
        put(frame, card, cx, cy, "cc", a=ease(lin(t_lift, 0.08, 0.5)), s=min(w / CARD_W, h / CARD_H))
        return
    # 2) full card
    if n < BOARD_IN:
        put(frame, order_card_full(n), CARD_X, CARD_Y, "tl")
        return
    # 3) board: columns slide in, card shrinks into column NEW, then moves right
    t_b = ease_io(lin(n, BOARD_IN, BOARD_IN + 18))
    fade_end = 1 - ease(lin(n, STATEMENT - 4, STATEMENT + 10))
    for i, lab in enumerate(COLS):
        tt = ease(lin(n, BOARD_IN + 4 * i, BOARD_IN + 4 * i + 16))
        put(frame, board_column(lab), col_x(i), BOARD_Y + 40 * (1 - tt), "tl", a=tt * fade_end)
        for r, (ti, su) in enumerate(GHOSTS[i]):
            gx = col_x(i) + 14
            gy = BOARD_Y + 70 + MINI_H + 18 + r * 126      # below the slot the order card uses
            put(frame, ghost_card(ti, su, "ARO"[(i + r) % 3]), gx, gy, "tl", a=tt * fade_end)
    if n >= MOVE_DELIVERED:
        col, status = 2, "DELIVERED"
    elif n >= MOVE_CONFIRMED:
        col, status = 1, "CONFIRMED"
    else:
        col, status = 0, "NEW"
    mv = 0.0
    prev = col
    if MOVE_CONFIRMED <= n < MOVE_CONFIRMED + 16:
        mv, prev = ease_io(lin(n, MOVE_CONFIRMED, MOVE_CONFIRMED + 16)), 0
    elif MOVE_DELIVERED <= n < MOVE_DELIVERED + 16:
        mv, prev = ease_io(lin(n, MOVE_DELIVERED, MOVE_DELIVERED + 16)), 1
    tx, ty = board_slot(col, 0)
    if prev != col:
        px_, _ = board_slot(prev, 0)
        tx = px_ + (tx - px_) * mv
    mini = mini_card(status)
    if t_b < 1:
        # morph from full card to mini card
        cx = (CARD_X + CARD_W / 2) + (tx + MINI_W / 2 - CARD_X - CARD_W / 2) * t_b
        cy = (CARD_Y + CARD_H / 2) + (ty + MINI_H / 2 - CARD_Y - CARD_H / 2) * t_b
        s_full = 1 + (MINI_W / CARD_W - 1) * t_b
        put(frame, order_card_full(n), cx, cy, "cc", a=1 - ease(lin(t_b, 0.3, 0.8)), s=s_full)
        put(frame, mini, cx, cy, "cc", a=ease(lin(t_b, 0.4, 0.9)), s=s_full * CARD_W / MINI_W)
    else:
        lift = 1.04 if prev != col else 1.0
        if prev != col:
            g, pad = glow(MINI_W, MINI_H, GOLD, 16, 90)
            put(frame, g, tx - pad, ty - pad, "tl", 0.8 * fade_end)
        put(frame, mini, tx + MINI_W / 2, ty + MINI_H / 2, "cc", a=fade_end, s=lift)
    # 4) follow-up reminder under the board
    if n >= FOLLOW_CHIP:
        t = lin(n, FOLLOW_CHIP, FOLLOW_CHIP + 12)
        put(frame, follow_card(), W / 2, BOARD_Y + BOARD_H + 40 + 110, "cc",
            a=min(ease(t * 1.4), fade_end), s=0.7 + 0.3 * back(t, 2.0))


@lru_cache(None)
def follow_card():
    w, h = 880, 190
    im = rrect(w, h, 24, (40, 33, 16, 255), GOLD + (255,), 3).copy()
    d = ImageDraw.Draw(im)
    # bell icon
    bx, by = 40, 46
    d.pieslice((bx, by, bx + 70, by + 80), 180, 360, fill=GOLD)
    d.rectangle((bx, by + 40, bx + 70, by + 72), fill=GOLD)
    d.rectangle((bx - 8, by + 70, bx + 78, by + 80), fill=GOLD)
    d.ellipse((bx + 26, by + 82, bx + 44, by + 98), fill=GOLD)
    im.alpha_composite(text_sprite("FOLLOW-UP  ·  SAT 10:00  ·  SARA", "M", 24, GOLD, 2), (150, 32))
    im.alpha_composite(text_sprite("Call Khalid: happy with the order?", "C6", 34, TEXT), (150, 76))
    im.alpha_composite(text_sprite("Ask about a reorder.", "C5", 30, TEXT2), (150, 122))
    return im


# ---------------------------------------------------------------- statement + end card
def draw_statement(frame, n):
    if not (STATEMENT <= n < END_CARD + 6):
        return
    out = 1 - ease(lin(n, END_CARD - 4, END_CARD + 6))
    lines = [(("Every order gets", TEXT),), (("an owner, a status", GOLD),), (("and a next step.", GOLD),)]
    for i, segs in enumerate(lines):
        t = ease(lin(n, STATEMENT + 3 * i, STATEMENT + 3 * i + 12))
        put(frame, rich_sprite(segs, "P8", 74), W / 2, 300 + i * 94 + 24 * (1 - t), "tc", a=min(t, out), text=True)
    for k, (lab, f) in enumerate(zip(("OWNER", "STATUS", "NEXT STEP"), STATEMENT_PILLS)):
        t = lin(n, f, f + 10)
        sp = pill(lab)
        put(frame, sp, [262, 540, 818][k], 640, "cc", a=min(ease(t * 1.5), out), s=0.6 + 0.4 * back(t, 2.2))
    sub = "The right tool depends on your workflow and budget. Not every shop needs a full ERP."
    for i, ln in enumerate(wrap(sub, "C5", 38, 820)):
        put_text(frame, ln, "C5", 38, TEXT2, W / 2, 780 + i * 50, "tc",
                 a=min(ease(lin(n, STATEMENT + 34, STATEMENT + 48)), out))


@lru_cache(None)
def pill(lab):
    ts = text_sprite(lab, "M", 30, GOLD, 3)
    im = rrect(250, 76, 38, GOLD + (30,), GOLD + (255,), 2).copy()
    im.alpha_composite(ts, ((250 - ts.width) // 2, (76 - ts.height) // 2 + 1))
    return im


def draw_end_card(frame, n):
    if n < END_CARD:
        return
    t = lin(n, END_CARD, END_CARD + 20)
    rot = -90 * (1 - ease(t))
    hm = helm(230).rotate(rot, resample=Image.BICUBIC)
    put(frame, hm, W / 2, 300, "cc", a=ease(t * 1.4), s=0.8 + 0.2 * ease(t))
    put(frame, wordmark(120), W / 2, 500, "cc", a=ease(lin(n, END_CARD + 8, END_CARD + 20)), text=True)
    tg = "Sales, stock and team in one organised system."
    put_text(frame, tg, "C5", 34, TEXT2, W / 2, 580, "tc", a=ease(lin(n, END_CARD + 14, END_CARD + 26)))
    a2 = ease(lin(n, END_CARD + 22, END_CARD + 34))
    put_text(frame, "FREE GUIDE", "M", 28, GOLD, W / 2, 700, "tc", a=a2, track=4)
    for i, ln in enumerate(wrap(GUIDE_TITLE, "P7", 50, 860)):
        put_text(frame, ln, "P7", 50, TEXT, W / 2, 748 + i * 64, "tc", a=a2)
    a3 = lin(n, END_CARD + 32, END_CARD + 44)
    btn = cta_button()
    put(frame, btn, W / 2, 1010, "cc", a=ease(a3 * 1.3), s=0.85 + 0.15 * back(a3, 2.0))


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


def draw_chrome(frame, n):
    # small brand mark (until the end card takes over)
    a = window(n, 0, END_CARD + 4, 10, 8)
    brand_lockup(frame, SAFE_X0 + 10, 56, 44, 34, a)
    if TURN + 8 <= n < END_CARD:
        al = window(n, TURN + 8, END_CARD, 10, 8)
        put(frame, label_chip("ILLUSTRATIVE WORKFLOW"), SAFE_X1 - 10, 56, "cr", a=al, text=True)
    # footnote whenever the illustrative workflow is on screen
    al = window(n, 6, TOTAL + 1, 10, 0)
    put_text(frame, FOOTNOTE, "M", 22, MUTED, W / 2, 1258, "tc", a=al, track=1)


@lru_cache(None)
def label_chip(text):
    ts = text_sprite(text, "M", 21, GOLD, 2)
    im = rrect(ts.width + 30, 40, 20, GOLD + (22,), GOLD + (110,), 1).copy()
    im.alpha_composite(ts, (15, (40 - ts.height) // 2 + 1))
    return im


# ---------------------------------------------------------------- frames
def render(n):
    frame = background(n)
    draw_phone(frame, n)
    draw_questions(frame, n)
    draw_order(frame, n)
    draw_headline(frame, n)
    draw_statement(frame, n)
    draw_end_card(frame, n)
    draw_chrome(frame, n)
    return frame.convert("RGB")


def check_layout():
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


CAPTIONS = [  # on-screen copy, mirrored into an SRT for platforms that accept caption files
    (6, KEY_IN - 6, "Taking orders on WhatsApp?"),
    (KEY_IN - 6, QUESTIONS - 4, "Here's the order. Now find it."),
    (QUESTIONS - 4, TURN + 4, "Buried in the group chat. Who's handling it? Was it confirmed? Did anyone follow up?"),
    (TURN + 4, STEP_LOG, "Give every order a place to live."),
    (STEP_LOG, STEP_ASSIGN, "1. Log it: record every order in one shared list, not only in the chat."),
    (STEP_ASSIGN, STEP_TRACK, "2. Assign it: one person owns it, so nobody has to guess."),
    (STEP_TRACK, STEP_FOLLOW, "3. Track it: everyone sees the status without asking."),
    (STEP_FOLLOW, STATEMENT, "4. Follow up: the next step has a name and a date."),
    (STATEMENT, END_CARD, "Every order gets an owner, a status and a next step. The right tool depends on your "
                          "workflow and budget."),
    (END_CARD, TOTAL, f"Free guide: {GUIDE_TITLE}. {CTA_URL}"),
]


def write_srt(path):
    def ts(f):
        ms = int(round(f / FPS * 1000))
        return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"
    with open(path, "w", encoding="utf-8") as fh:
        for i, (a, b, text) in enumerate(CAPTIONS, 1):
            fh.write(f"{i}\n{ts(a)} --> {ts(b)}\n{text}\n\n")


def mux_audio(video, out):
    inputs, chains, labels, idx = ["-i", video], [], [], 1
    for name, path, gain in (("mu", ARGS.music, -2), ("fx", ARGS.sfx, -4)):
        if path:
            inputs += ["-i", path]
            chains.append(f"[{idx}:a]aresample=48000,volume={gain}dB[{name}]")
            labels.append(f"[{name}]")
            idx += 1
    chains.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0,"
                  "loudnorm=I=-14:TP=-1.5:LRA=9,aresample=48000[aout]")   # social platforms normalise near -14 LUFS
    subprocess.run([FFMPEG, "-nostdin", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(chains),
                    "-map", "0:v", "-map", "[aout]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                    "-ac", "2", "-t", str(TOTAL / FPS), "-movflags", "+faststart", out], check=True)


def storyboard(path):
    picks = [(60, "Hook"), (135, "The order"), (240, "Buried + questions"), (320, "Lift out"),
             (410, "1 Log"), (490, "2 Assign"), (590, "3 Track"), (670, "4 Follow up"),
             (760, "Statement"), (880, "End card")]
    tw = 216
    th = tw * H // W
    f = F("C6", 16)
    sheet = Image.new("RGB", (5 * (tw + 12) + 12, 2 * (th + 40) + 12), (255, 255, 255))
    d = ImageDraw.Draw(sheet)
    for i, (n, text) in enumerate(picks):
        x, y = 12 + (i % 5) * (tw + 12), 12 + (i // 5) * (th + 40)
        sheet.paste(render(n).resize((tw, th), Image.LANCZOS), (x, y + 28))
        d.text((x, y + 4), f"f{n} ({n / FPS:.1f}s) {text}", font=f, fill=(0, 0, 0))
    sheet.save(path)


def main():
    check_layout()
    if ARGS.srt:
        write_srt(ARGS.srt)
    if ARGS.storyboard:
        storyboard(ARGS.storyboard)
    if ARGS.cover:
        render(245).save(ARGS.cover)   # the hook: "Buried in the group chat."
    if ARGS.frames:
        base = os.path.splitext(ARGS.out or "frame")[0]
        for n in map(int, ARGS.frames.split(",")):
            render(n).save(f"{base}_f{n:03d}.png")
        return
    if not ARGS.out:
        return
    has_audio = ARGS.music or ARGS.sfx
    video = tempfile.mktemp(suffix=".mp4") if has_audio else ARGS.out
    ow = ARGS.size
    oh = ow * H // W // 2 * 2
    cmd = [FFMPEG, "-nostdin", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-vf", f"scale={ow}:{oh}:flags=lanczos", "-c:v", "libx264", "-preset", "medium",
           "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart", video]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for n in range(TOTAL):
        proc.stdin.write(render(n).tobytes())
    proc.stdin.close()
    if proc.wait():
        raise SystemExit("ffmpeg failed")
    if has_audio:
        mux_audio(video, ARGS.out)
        os.remove(video)


if __name__ == "__main__":
    main()
