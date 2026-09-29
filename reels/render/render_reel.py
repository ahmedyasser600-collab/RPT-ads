"""Render the 40s 9:16 Reel (silent video track) for Ristrutturare Per Te.

Voice-over and music are added in the editor following the timeline in
reels/reel-40s-esigenze-budget-tempi.md; all cuts here are placed on that timeline.

Usage: python3 render_reel.py <images_dir> <fonts_dir> <out.mp4>
"""
import math
import subprocess
import sys

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFilter, ImageFont

IMG_DIR, FONT_DIR, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
W, H, FPS, DUR = 1080, 1920, 30, 40.0

YELLOW = (245, 190, 30)
BLACK = (20, 20, 20)
GREY = (242, 242, 240)
MID = (110, 110, 110)
SAGE = (157, 179, 160)
BEIGE = (221, 208, 184)
TERRAZZO = (232, 226, 216)


def font(weight, size):
    return ImageFont.truetype(f"{FONT_DIR}/plus-jakarta-sans-latin-{weight}-normal.woff", size)


F_HEAD = font(800, 78)
F_BIG = font(800, 118)
F_CTA = font(800, 72)
F_URL = font(800, 58)
F_LABEL = font(500, 34)
F_SMALL = font(400, 22)


def load(name):
    return Image.open(f"{IMG_DIR}/{name}").convert("RGB")


BEFORE = load("10.png")      # R6: bagno "prima"
DEMO = load("9.png")         # R9: bagno demolito, pronto da misurare
IMPIANTI = load("5.png")     # R3
POSA = load("7.png")         # R5
VETRO = load("3.png")        # R1
FINITO = load("6.png")       # R4
DETTAGLIO = load("4.png")    # R2


def make_logo():
    src = Image.open(f"{IMG_DIR}/8.webp").convert("RGB")
    px = src.load()
    alpha = Image.new("L", src.size, 0)
    ap = alpha.load()
    for y in range(src.height):
        for x in range(src.width):
            r, g, b = px[x, y]
            # Key out the near-white background, keeping anti-aliased edges.
            ap[x, y] = max(0, min(255, int((250 - min(r, g, b)) * 255 / 60)))
    logo = src.copy()
    logo.putalpha(alpha)
    return logo.crop(alpha.getbbox())


LOGO = make_logo()


def logo_at(width):
    h = round(LOGO.height * width / LOGO.width)
    return LOGO.resize((width, h), Image.LANCZOS)


LOGO_SMALL = logo_at(270)
LOGO_BIG = logo_at(620)

# Photo card (brand layout from the static key visual).
CARD_X, CARD_Y, CARD_W, CARD_H = 60, 560, 960, 830
RADIUS = 36


def rounded_mask(w, h, r):
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), r, fill=255)
    return m


CARD_MASK = rounded_mask(CARD_W, CARD_H, RADIUS)
SHADOW = Image.new("RGBA", (CARD_W + 80, CARD_H + 80), (0, 0, 0, 0))
ImageDraw.Draw(SHADOW).rounded_rectangle((40, 50, CARD_W + 40, CARD_H + 40), RADIUS, fill=(0, 0, 0, 60))
SHADOW = SHADOW.filter(ImageFilter.GaussianBlur(18))


def ease(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


def crop(src, cx, cy, zoom, w=CARD_W, h=CARD_H):
    """Cover-crop src to w:h around (cx, cy) in 0..1 coords, with extra zoom."""
    ar = w / h
    if src.width / src.height > ar:
        ch = src.height / zoom
        cw = ch * ar
    else:
        cw = src.width / zoom
        ch = cw / ar
    x0 = min(max(cx * src.width - cw / 2, 0), src.width - cw)
    y0 = min(max(cy * src.height - ch / 2, 0), src.height - ch)
    return src.resize((w, h), Image.LANCZOS, box=(x0, y0, x0 + cw, y0 + ch)).filter(
        ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))


def cool(img):
    """Colder, slightly desaturated grade for the 'before' shots."""
    grey = img.convert("L").convert("RGB")
    img = Image.blend(img, grey, 0.35)
    r, g, b = img.split()
    return Image.merge("RGB", (r.point(lambda v: v * 0.94), g, b.point(lambda v: min(255, v * 1.06 + 6))))


def paste_card(frame, img):
    frame.paste(SHADOW, (CARD_X - 40, CARD_Y - 40), SHADOW)
    frame.paste(img, (CARD_X, CARD_Y), CARD_MASK)


PUNCT = ".,?:"


def tight_len(text, fnt):
    return fnt.getlength(text) - sum(fnt.size * 0.1 for ch in text if ch in PUNCT)


def draw_tight(d, xy, text, fnt, fill):
    """Draw text pulling punctuation in: the web-subset font spaces it too loosely."""
    x, y = xy
    run = ""
    for ch in text:
        if ch in PUNCT:
            d.text((x, y), run, font=fnt, fill=fill)
            x += fnt.getlength(run) - fnt.size * 0.1
            d.text((x, y), ch, font=fnt, fill=fill)
            x += fnt.getlength(ch)
            run = ""
        else:
            run += ch
    d.text((x, y), run, font=fnt, fill=fill)


def wrap(text, fnt, max_w):
    if "\n" in text:
        return text.split("\n")
    lines, cur = [], ""
    for word in text.split():
        test = (cur + " " + word).strip()
        if tight_len(test, fnt) <= max_w or not cur:
            cur = test
        else:
            lines.append(cur)
            cur = word
    return lines + [cur]


def headline(frame, text, t, t0, x=60, y=250, max_w=660, fnt=F_HEAD, underline=True):
    """Brand headline: fade + 20px slide in, yellow line drawn under it."""
    if t < t0:
        return
    p = ease((t - t0) / 0.35)
    layer = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    lh = int(fnt.size * 1.05)
    lines = wrap(text, fnt, max_w)
    dy = int((1 - p) * 20)
    for i, line in enumerate(lines):
        draw_tight(d, (x, y + i * lh + dy), line, fnt, BLACK + (int(255 * p),))
    if underline:
        lp = ease((t - t0 - 0.15) / 0.3)
        uy = y + len(lines) * lh + 18
        if lp > 0:
            d.rectangle((x, uy, x + int(140 * lp), uy + 10), fill=YELLOW + (255,))
    frame.alpha_composite(layer)


def label(frame, text, t, t0, x, y):
    if t < t0:
        return
    p = ease((t - t0) / 0.25)
    layer = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    tracked = " ".join(text)  # wide letter-spacing, as in PADOVA E PROVINCIA
    d.ellipse((x, y + 12, x + 16, y + 28), fill=YELLOW + (int(255 * p),))
    d.text((x + 30, y), tracked, font=F_LABEL, fill=BLACK + (int(255 * p),))
    frame.alpha_composite(layer)


def disclaimer(frame, y=CARD_Y + CARD_H + 16):
    d = ImageDraw.Draw(frame)
    txt = "Concept illustrativo generato con AI"
    d.text((CARD_X + CARD_W - F_SMALL.getlength(txt), y), txt, font=F_SMALL, fill=MID)


def tape(frame, x_end, y, height=110):
    """Yellow tape measure band with tick marks, visible up to x_end."""
    if x_end <= 0:
        return
    d = ImageDraw.Draw(frame)
    d.rectangle((0, y, x_end, y + height), fill=YELLOW)
    for i, x in enumerate(range(10, int(x_end), 18)):
        tl = 46 if i % 5 == 0 else 24
        d.rectangle((x, y, x + 3, y + tl), fill=BLACK)
        d.rectangle((x, y + height - tl, x + 3, y + height), fill=BLACK)


# ---------------------------------------------------------------- scenes

def scene_before(frame, t):  # 1: 0.0-4.6
    z = 1.0 + 0.08 * (t / 4.6)
    paste_card(frame, cool(crop(BEFORE, 0.5, 0.5, z)))
    headline(frame, "Bagno piccolo?\nDatato? Scomodo?", t, 0.3)


CROPS = [(4.6, 0.55, 0.40), (6.0, 0.30, 0.68), (7.4, 0.76, 0.74)]  # doccia, lavabo, sanitari


def scene_disagi(frame, t):  # 2: 4.6-8.8
    start, cx, cy = [c for c in CROPS if c[0] <= t][-1]
    z = 1.9 + 0.1 * (t - start)
    paste_card(frame, cool(crop(BEFORE, cx, cy, z)))
    headline(frame, "Ogni giorno, gli stessi disagi.", t, 4.8)


TILE_COLORS = [SAGE, BEIGE, TERRAZZO, SAGE, TERRAZZO, BEIGE, BEIGE, SAGE, TERRAZZO, TERRAZZO, SAGE, BEIGE]


def scene_piastrelle(frame, t):  # 3: 8.8-12.6
    card = Image.new("RGB", (CARD_W, CARD_H), (255, 255, 255))
    d = ImageDraw.Draw(card)
    size, gap = 250, 40
    ox = (CARD_W - (4 * size + 3 * gap)) // 2
    oy = (CARD_H - (3 * size + 2 * gap)) // 2
    for i, col in enumerate(TILE_COLORS):
        r, c = divmod(i, 4)
        # The hand pushes the samples aside on "piastrelle" (~11.0s), staggered.
        p = ease((t - 10.9 - 0.04 * (11 - i)) / 0.5)
        x = ox + c * (size + gap) + int(p * 1100)
        y = oy + r * (size + gap)
        d.rounded_rectangle((x, y, x + size, y + size), 14, fill=col, outline=(200, 200, 196), width=2)
        if col is TERRAZZO:
            for k in range(9):
                sx, sy = x + 30 + (k * 71) % 190, y + 30 + (k * 53) % 190
                d.ellipse((sx, sy, sx + 12, sy + 9), fill=(196, 186, 170))
    paste_card(frame, card)
    headline(frame, "Non partire dalle piastrelle.", t, 9.0)


WORDS = [("Esigenze", 13.9), ("Budget", 14.9), ("Tempi", 16.2)]


def scene_esigenze(frame, t):  # 4: 12.6-17.4
    tape(frame, ease((t - 12.6) / 0.8) * W, 640)
    label(frame, "COMINCIA DA", t, 12.9, 60, 540)
    layer = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for i, (word, t0) in enumerate(WORDS):
        if t >= t0:
            p = ease((t - t0) / 0.3)
            y = 830 + i * 170 + int((1 - p) * 20)
            draw_tight(d, (60, y), word + ".", F_BIG, BLACK + (int(255 * p),))
            lp = ease((t - t0 - 0.1) / 0.3)
            d.rectangle((60, y + 142, 60 + int(120 * lp), y + 152), fill=YELLOW + (255,))
    frame.alpha_composite(layer)


def scene_misura(frame, t):  # 5: 17.4-22.0
    z = 1.0 + 0.06 * ((t - 17.4) / 4.6)
    card = crop(DEMO, 0.5, 0.5, z)
    d = ImageDraw.Draw(card)
    # Dimension line drawn across the back wall on "misuriamo" (~19.8s).
    p = ease((t - 19.6) / 1.0)
    if p > 0:
        y, x0, x1 = 300, 250, 250 + int(470 * p)
        d.rectangle((x0, y - 4, x1, y + 4), fill=YELLOW)
        d.rectangle((x0 - 4, y - 26, x0 + 4, y + 26), fill=YELLOW)
        d.rectangle((x1 - 4, y - 26, x1 + 4, y + 26), fill=YELLOW)
    paste_card(frame, card)
    headline(frame, "Prima\nascoltiamo.\nPoi misuriamo.", t, 17.6)


PHASES = [(22.0, IMPIANTI, "IMPIANTI"), (23.4, POSA, "POSA"), (25.0, VETRO, "FINITURE")]


def scene_fasi(frame, t):  # 6: 22.0-28.4
    start, img, name = [p for p in PHASES if p[0] <= t][-1]
    z = 1.0 + 0.05 * (t - start)
    paste_card(frame, crop(img, 0.5, 0.5, z))
    headline(frame, "Seguiamo ogni fase.", t, 22.3)
    label(frame, name, t, start, 60, CARD_Y + CARD_H + 40)


def scene_risultato(frame, t):  # 7: 28.4-33.6
    if t < 30.8:
        after = crop(FINITO, 0.5, 0.5, 1.0 + 0.04 * max(0, t - 29.4))
        p = ease((t - 28.4) / 1.0)
        wx = int(CARD_W * p)
        card = cool(crop(BEFORE, 0.5, 0.5, 1.08))
        if wx > 0:
            card.paste(after.crop((0, 0, wx, CARD_H)), (0, 0))
            if p < 1:
                ImageDraw.Draw(card).rectangle((wx - 5, 0, wx + 5, CARD_H), fill=YELLOW)
    else:
        card = crop(DETTAGLIO, 0.5, 0.5, 1.0 + 0.05 * (t - 30.8))
    paste_card(frame, card)
    headline(frame, "Pratico.\nLuminoso.\nSu misura per te.", t, 28.8)


END_THUMB = None


def scene_cta(frame, t):  # 8: 33.6-40.0
    global END_THUMB
    p = ease((t - 33.6) / 0.5)
    layer = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    lg = LOGO_BIG.copy()
    lg.putalpha(lg.getchannel("A").point(lambda a: int(a * p)))
    layer.paste(lg, ((W - lg.width) // 2, 230 + int((1 - p) * 20)), lg)
    frame.alpha_composite(layer)

    if t >= 34.2:
        q = ease((t - 34.2) / 0.35)
        layer = Image.new("RGBA", frame.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        y = 640 + int((1 - q) * 20)
        a = int(255 * q)
        lines = wrap("Raccontaci il\ntuo progetto.", F_CTA, 820)
        for i, line in enumerate(lines):
            draw_tight(d, (60, y + i * 78), line, F_CTA, BLACK + (a,))
        # Arrow after the last line, as in "Parliamo del tuo bagno →".
        ax = 60 + int(tight_len(lines[-1], F_CTA)) + 28
        ay = y + (len(lines) - 1) * 78 + 46
        d.rectangle((ax, ay - 4, ax + 52, ay + 4), fill=BLACK + (a,))
        d.polygon([(ax + 60, ay), (ax + 36, ay - 22), (ax + 36, ay + 22)], fill=BLACK + (a,))
        lp = ease((t - 34.4) / 0.4)
        ly = y + len(lines) * 78 + 26
        d.rectangle((60, ly, 60 + int(360 * lp), ly + 10), fill=YELLOW + (255,))
        frame.alpha_composite(layer)

    if t >= 36.2:  # URL on "Ristrutturare Per Te"
        q = ease((t - 36.2) / 0.3)
        layer = Image.new("RGBA", frame.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        url = "rpt-1.netlify.app"
        tw = F_URL.getlength(url)
        y = 900
        d.rounded_rectangle((60, y, 60 + tw + 64, y + 100), 20, fill=YELLOW + (int(255 * q),))
        d.text((92, y + 18), url, font=F_URL, fill=BLACK + (int(255 * q),))
        frame.alpha_composite(layer)

    if t >= 37.8:  # pin on "Padova e provincia"
        q = ease((t - 37.8) / 0.3)
        layer = Image.new("RGBA", frame.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        x, y, a = 60, 1060, int(255 * q)
        d.ellipse((x, y, x + 34, y + 34), fill=YELLOW + (a,))
        d.polygon([(x + 3, y + 24), (x + 31, y + 24), (x + 17, y + 50)], fill=YELLOW + (a,))
        d.ellipse((x + 11, y + 11, x + 23, y + 23), fill=GREY + (a,))
        d.text((x + 56, y + 6), " ".join("PADOVA E PROVINCIA"), font=F_LABEL, fill=BLACK + (a,))
        frame.alpha_composite(layer)

    if END_THUMB is None:
        END_THUMB = crop(FINITO, 0.5, 0.62, 1.0, CARD_W, 300)
    frame.paste(END_THUMB, (CARD_X, 1180), rounded_mask(CARD_W, 300, RADIUS))
    disclaimer(frame, 1180 + 300 + 14)


SCENES = [(0.0, scene_before), (4.6, scene_disagi), (8.8, scene_piastrelle), (12.6, scene_esigenze),
          (17.4, scene_misura), (22.0, scene_fasi), (28.4, scene_risultato), (33.6, scene_cta)]


def render(t):
    frame = Image.new("RGBA", (W, H), GREY + (255,))
    start, fn = [s for s in SCENES if s[0] <= t][-1]
    fn(frame, t)
    if fn is not scene_cta:
        # Logo always on screen, fixed top-right (same position as the key visual).
        frame.alpha_composite(LOGO_SMALL, (W - 60 - LOGO_SMALL.width, 230))
        if fn is not scene_esigenze:
            disclaimer(frame)
    # Short fade from/to the cut on each scene change.
    k = min(t - start, 0.12) / 0.12
    if k < 1 and start > 0:
        frame = Image.blend(Image.new("RGBA", (W, H), GREY + (255,)), frame, 0.4 + 0.6 * k)
    return frame.convert("RGB")


def main():
    cmd = [imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
           "-movflags", "+faststart", OUT]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(int(DUR * FPS)):
        proc.stdin.write(render(i / FPS).tobytes())
    proc.stdin.close()
    sys.exit(proc.wait())


if __name__ == "__main__":
    main()
