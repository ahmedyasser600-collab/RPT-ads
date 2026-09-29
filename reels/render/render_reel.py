"""Render the 40s 9:16 Reel for Ristrutturare Per Te.

Full-screen vertical photos (assets/*.png, 1520x2688) with the brand layout from the
static key visual: headline top-left, logo top-right, yellow accents, Plus Jakarta Sans.
All cuts and text reveals sit on the voice-over timeline in
reels/reel-40s-esigenze-budget-tempi.md.

Usage:
  python3 render_reel.py <assets_dir> <fonts_dir> <out.mp4> [--vo <dir with vo1..vo8.mp3>] [--music <file>]
"""
import argparse
import os
import subprocess
import tempfile

import imageio_ffmpeg
from PIL import Image, ImageChops, ImageDraw, ImageFont

ap = argparse.ArgumentParser()
ap.add_argument("assets")
ap.add_argument("fonts")
ap.add_argument("out")
ap.add_argument("--vo")
ap.add_argument("--music")
ARGS = ap.parse_args()

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
W, H, FPS, DUR = 1080, 1920, 30, 40.0

YELLOW = (245, 190, 30)
BLACK = (20, 20, 20)
GREY = (242, 242, 240)
MID = (90, 90, 90)


def font(weight, size):
    return ImageFont.truetype(f"{ARGS.fonts}/plus-jakarta-sans-latin-{weight}-normal.woff", size)


F_HEAD = font(800, 78)
F_BIG = font(800, 118)
F_CTA = font(800, 72)
F_URL = font(800, 58)
F_LABEL = font(500, 34)
F_SMALL = font(400, 22)


def load(name):
    return Image.open(f"{ARGS.assets}/{name}").convert("RGB")


BEFORE = load("prima.png")
SOPRALLUOGO = load("sopralluogo.png")
CAMPIONI = load("campioni.png")
IMPIANTI = load("impianti.png")
POSA = load("posa.png")
VETRO = load("vetro.png")
DOPO = load("dopo.png")
DETTAGLIO = load("dettaglio.png")


def make_logo():
    src = Image.open(f"{ARGS.assets}/logo.webp").convert("RGB")
    # Key out the near-white background on the darkest channel, keeping anti-aliased edges.
    r, g, b = src.split()
    darkest = ImageChops.darker(ImageChops.darker(r, g), b)
    alpha = darkest.point(lambda v: max(0, min(255, int((250 - v) * 255 / 60))))
    logo = src.copy()
    logo.putalpha(alpha)
    return logo.crop(alpha.getbbox())


LOGO = make_logo()


def logo_at(width):
    return LOGO.resize((width, round(LOGO.height * width / LOGO.width)), Image.LANCZOS)


LOGO_SMALL = logo_at(270)
LOGO_BIG = logo_at(620)

# Light scrim at the top so the black headline and the logo always read on photos.
SCRIM = Image.new("RGBA", (W, 820), GREY + (0,))
_sd = ImageDraw.Draw(SCRIM)
for y in range(820):
    k = 1 - y / 820
    _sd.line((0, y, W, y), fill=GREY + (int(235 * min(1, k * 1.35) ** 1.4),))


def ease(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


def frame_of(src, cx=0.5, cy=0.5, zoom=1.0, w=W, h=H):
    """Cover-crop src to w:h around (cx, cy) with a gentle zoom (source is 1.4x the output)."""
    ar = w / h
    if src.width / src.height > ar:
        ch = src.height / zoom
        cw = ch * ar
    else:
        cw = src.width / zoom
        ch = cw / ar
    x0 = min(max(cx * src.width - cw / 2, 0), src.width - cw)
    y0 = min(max(cy * src.height - ch / 2, 0), src.height - ch)
    return src.resize((w, h), Image.BICUBIC, box=(x0, y0, x0 + cw, y0 + ch)).convert("RGBA")


def cool(img):
    """Colder, slightly desaturated grade for the 'before' shots."""
    rgb = img.convert("RGB")
    rgb = Image.blend(rgb, rgb.convert("L").convert("RGB"), 0.3)
    r, g, b = rgb.split()
    rgb = Image.merge("RGB", (r.point(lambda v: v * 0.95), g, b.point(lambda v: min(255, v * 1.05 + 5))))
    return rgb.convert("RGBA")


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


def headline(frame, text, t, t0, x=60, y=250, fnt=F_HEAD):
    """Brand headline: fade + 20px slide in, yellow line drawn under it."""
    if t < t0:
        return
    p = ease((t - t0) / 0.35)
    layer = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    lh = int(fnt.size * 1.05)
    lines = text.split("\n")
    dy = int((1 - p) * 20)
    for i, line in enumerate(lines):
        draw_tight(d, (x, y + i * lh + dy), line, fnt, BLACK + (int(255 * p),))
    lp = ease((t - t0 - 0.15) / 0.3)
    uy = y + len(lines) * lh + 18
    if lp > 0:
        d.rectangle((x, uy, x + int(140 * lp), uy + 10), fill=YELLOW + (255,))
    frame.alpha_composite(layer)


def pill_label(frame, text, t, t0, x=60, y=1400):
    """Uppercase tracked label on a light pill, readable over photos."""
    if t < t0:
        return
    p = ease((t - t0) / 0.25)
    layer = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    tracked = " ".join(text)
    tw = F_LABEL.getlength(tracked)
    d.rounded_rectangle((x, y, x + tw + 84, y + 70), 35, fill=GREY + (int(235 * p),))
    d.ellipse((x + 26, y + 27, x + 42, y + 43), fill=YELLOW + (int(255 * p),))
    d.text((x + 56, y + 14), tracked, font=F_LABEL, fill=BLACK + (int(255 * p),))
    frame.alpha_composite(layer)


def disclaimer(frame, y=1500):
    d = ImageDraw.Draw(frame)
    txt = "Concept illustrativo generato con AI"
    tw = F_SMALL.getlength(txt)
    d.rounded_rectangle((W - 60 - tw - 24, y - 6, W - 60 + 4, y + 30), 14, fill=GREY + (200,))
    d.text((W - 60 - tw - 10, y), txt, font=F_SMALL, fill=MID)


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


def photo(frame, img):
    frame.alpha_composite(img)
    frame.alpha_composite(SCRIM)


# ---------------------------------------------------------------- scenes

def scene_before(frame, t):  # 1: 0.0-4.6
    photo(frame, cool(frame_of(BEFORE, zoom=1.0 + 0.05 * t / 4.6)))
    headline(frame, "Bagno piccolo?\nDatato? Scomodo?", t, 0.3)


# Push-ins on the 'before' photo (max zoom 1.35 keeps it at or above native resolution).
CROPS = [(4.6, 0.55, 0.52), (6.0, 0.28, 0.62), (7.4, 0.72, 0.72)]  # doccia, lavabo, sanitari


def scene_disagi(frame, t):  # 2: 4.6-8.8
    start, cx, cy = [c for c in CROPS if c[0] <= t][-1]
    photo(frame, cool(frame_of(BEFORE, cx, cy, 1.28 + 0.05 * (t - start))))
    headline(frame, "Ogni giorno,\ngli stessi disagi.", t, 4.8)


def scene_piastrelle(frame, t):  # 3: 8.8-12.6
    photo(frame, frame_of(CAMPIONI, zoom=1.0 + 0.05 * (t - 8.8) / 3.8))
    headline(frame, "Non partire\ndalle piastrelle.", t, 9.0)


WORDS = [("Esigenze", 13.9), ("Budget", 14.9), ("Tempi", 16.2)]


def scene_esigenze(frame, t):  # 4: 12.6-17.4 (brand graphic)
    tape(frame, ease((t - 12.6) / 0.8) * W, 640)
    layer = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    if t >= 12.9:
        p = ease((t - 12.9) / 0.25)
        d.ellipse((60, 552, 76, 568), fill=YELLOW + (int(255 * p),))
        d.text((90, 540), " ".join("COMINCIA DA"), font=F_LABEL, fill=BLACK + (int(255 * p),))
    for i, (word, t0) in enumerate(WORDS):
        if t >= t0:
            p = ease((t - t0) / 0.3)
            y = 830 + i * 170 + int((1 - p) * 20)
            draw_tight(d, (60, y), word + ".", F_BIG, BLACK + (int(255 * p),))
            lp = ease((t - t0 - 0.1) / 0.3)
            d.rectangle((60, y + 142, 60 + int(120 * lp), y + 152), fill=YELLOW + (255,))
    frame.alpha_composite(layer)


def scene_misura(frame, t):  # 5: 17.4-22.0
    photo(frame, frame_of(SOPRALLUOGO, zoom=1.0 + 0.05 * (t - 17.4) / 4.6))
    headline(frame, "Prima\nascoltiamo.\nPoi misuriamo.", t, 17.6)


PHASES = [(22.0, IMPIANTI, "IMPIANTI"), (23.4, POSA, "POSA"), (25.0, VETRO, "FINITURE")]


def scene_fasi(frame, t):  # 6: 22.0-28.4
    start, img, name = [p for p in PHASES if p[0] <= t][-1]
    photo(frame, frame_of(img, zoom=1.0 + 0.03 * (t - start)))
    headline(frame, "Seguiamo\nogni fase.", t, 22.3)
    pill_label(frame, name, t, start)


def scene_risultato(frame, t):  # 7: 28.4-33.6
    if t < 30.8:
        img = cool(frame_of(BEFORE, zoom=1.05))
        p = ease((t - 28.4) / 1.0)
        wx = int(W * p)
        if wx > 0:
            after = frame_of(DOPO, zoom=1.05 - 0.03 * max(0, t - 29.4) / 1.4)
            img.paste(after.crop((0, 0, wx, H)), (0, 0))
            if p < 1:
                ImageDraw.Draw(img).rectangle((wx - 6, 0, wx + 6, H), fill=YELLOW)
    else:
        img = frame_of(DETTAGLIO, zoom=1.0 + 0.04 * (t - 30.8) / 2.8)
    photo(frame, img)
    headline(frame, "Pratico.\nLuminoso.\nSu misura per te.", t, 28.8)


END_THUMB = None
THUMB_Y, THUMB_H = 1180, 300


def scene_cta(frame, t):  # 8: 33.6-40.0 (brand end card)
    global END_THUMB
    p = ease((t - 33.6) / 0.5)
    lg = LOGO_BIG.copy()
    lg.putalpha(lg.getchannel("A").point(lambda a: int(a * p)))
    frame.alpha_composite(lg, ((W - lg.width) // 2, 230 + int((1 - p) * 20)))

    layer = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    if t >= 34.2:
        q = ease((t - 34.2) / 0.35)
        y, a = 640 + int((1 - q) * 20), int(255 * q)
        lines = ["Raccontaci il", "tuo progetto."]
        for i, line in enumerate(lines):
            draw_tight(d, (60, y + i * 78), line, F_CTA, BLACK + (a,))
        # Arrow after the last line, as in "Parliamo del tuo bagno ->".
        ax = 60 + int(tight_len(lines[-1], F_CTA)) + 28
        ay = y + 78 + 46
        d.rectangle((ax, ay - 4, ax + 52, ay + 4), fill=BLACK + (a,))
        d.polygon([(ax + 60, ay), (ax + 36, ay - 22), (ax + 36, ay + 22)], fill=BLACK + (a,))
        lp = ease((t - 34.4) / 0.4)
        d.rectangle((60, y + 182, 60 + int(360 * lp), y + 192), fill=YELLOW + (255,))
    if t >= 36.2:  # URL on "Ristrutturare Per Te"
        q = int(255 * ease((t - 36.2) / 0.3))
        url = "rpt-1.netlify.app"
        d.rounded_rectangle((60, 900, 60 + F_URL.getlength(url) + 64, 1000), 20, fill=YELLOW + (q,))
        d.text((92, 918), url, font=F_URL, fill=BLACK + (q,))
    if t >= 37.8:  # pin on "Padova e provincia"
        a = int(255 * ease((t - 37.8) / 0.3))
        x, y = 60, 1060
        d.ellipse((x, y, x + 34, y + 34), fill=YELLOW + (a,))
        d.polygon([(x + 3, y + 24), (x + 31, y + 24), (x + 17, y + 50)], fill=YELLOW + (a,))
        d.ellipse((x + 11, y + 11, x + 23, y + 23), fill=GREY + (a,))
        d.text((x + 56, y + 6), " ".join("PADOVA E PROVINCIA"), font=F_LABEL, fill=BLACK + (a,))
    frame.alpha_composite(layer)

    if END_THUMB is None:
        END_THUMB = frame_of(DOPO, 0.5, 0.62, 1.0, W - 120, THUMB_H)
        mask = Image.new("L", END_THUMB.size, 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, END_THUMB.width - 1, THUMB_H - 1), 36, fill=255)
        END_THUMB.putalpha(mask)
    frame.alpha_composite(END_THUMB, (60, THUMB_Y))
    disclaimer(frame, THUMB_Y + THUMB_H + 16)


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
    # Short dip on each scene change.
    k = min(t - start, 0.12) / 0.12
    if k < 1 and start > 0:
        frame = Image.blend(Image.new("RGBA", (W, H), GREY + (255,)), frame, 0.4 + 0.6 * k)
    return frame.convert("RGB")


# Voice-over clip start times (seconds), one clip per scene.
VO_STARTS = [0.3, 4.8, 9.0, 12.9, 17.6, 22.3, 28.8, 34.2]


def mix_audio(video, out):
    """Place vo1..vo8 on the timeline, duck the optional music under them, mux."""
    inputs, filters = ["-i", video], []
    for i, t0 in enumerate(VO_STARTS, 1):
        inputs += ["-i", os.path.join(ARGS.vo, f"vo{i}.mp3")]
        ms = int(t0 * 1000)
        filters.append(f"[{i}:a]aresample=48000,adelay={ms}|{ms},apad[v{i}]")
    vo_labels = "".join(f"[v{i}]" for i in range(1, 9))
    filters.append(f"{vo_labels}amix=inputs=8:normalize=0,atrim=0:{DUR},"
                   f"loudnorm=I=-14:TP=-1.5:LRA=7[vo]")
    if ARGS.music:
        inputs += ["-i", ARGS.music]
        filters.append("[vo]asplit[vo1][vokey]")
        filters.append(f"[9:a]aresample=48000,atrim=0:{DUR},volume=-12dB,"
                       f"afade=t=out:st={DUR - 1.2}:d=1.2[mu]")
        filters.append("[mu][vokey]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[duck]")
        filters.append("[vo1][duck]amix=inputs=2:normalize=0[aout]")
        out_label = "[aout]"
    else:
        out_label = "[vo]"
    cmd = [FFMPEG, "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(filters),
           "-map", "0:v", "-map", out_label, "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
           "-shortest", "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True)


def main():
    silent = ARGS.out if not ARGS.vo else tempfile.mktemp(suffix=".mp4")
    cmd = [FFMPEG, "-y", "-loglevel", "error",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
           "-movflags", "+faststart", silent]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(int(DUR * FPS)):
        proc.stdin.write(render(i / FPS).tobytes())
    proc.stdin.close()
    if proc.wait():
        raise SystemExit("ffmpeg failed")
    if ARGS.vo:
        mix_audio(silent, ARGS.out)
        os.remove(silent)


if __name__ == "__main__":
    main()
