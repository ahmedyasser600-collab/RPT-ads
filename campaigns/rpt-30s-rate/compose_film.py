"""Composite the 30s RPT reel: Blender frames + 2D brand layers + audio.

All campaign text, subtitles, the financing panel and the logo are 2D layers here,
never part of the 3D geometry. Frame n (1-based) is shown at (n-1)/30 s.

Usage:
  python3 compose_film.py --frames <dir with frame_0001.png..> --out reel.mp4
         [--vo vo.wav] [--music audio/music.wav] [--sfx audio/sfx.wav]
         [--review]           # adds the REVIEW tag and the unresolved-disclosure placeholder
         [--srt subtitles.srt]
Missing 3D frames reuse the nearest earlier rendered frame (for animatics only).
"""
import argparse
import glob
import os
import re
import subprocess
import tempfile

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
ap = argparse.ArgumentParser()
ap.add_argument("--frames", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--vo")
ap.add_argument("--music")
ap.add_argument("--sfx")
ap.add_argument("--srt")
ap.add_argument("--review", action="store_true")
ap.add_argument("--fonts", default=os.path.join(HERE, "fonts"))
ARGS = ap.parse_args()

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
W, H, FPS, TOTAL = 1080, 1920, 30, 900
END_CARD = 781                       # frames 781-900: 2D end card (26.0-30.0 s)
YELLOW = (245, 187, 29)              # #F5BB1D, sampled from the supplied raster logo
BLACK = (20, 20, 20)
PAPER = (244, 241, 236)
RED = (200, 40, 40)


def font(weight, size):
    return ImageFont.truetype(f"{ARGS.fonts}/plus-jakarta-sans-latin-{weight}-normal.woff", size)


F_HEAD, F_SUB, F_LABEL = font(800, 76), font(600, 42), font(500, 32)
F_RATE1, F_RATE2 = font(800, 58), font(800, 92)
F_CTA, F_URL, F_TAG = font(800, 74), font(800, 54), font(600, 26)


def t_of(n):
    return (n - 1) / FPS


def ease(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


# ---------------------------------------------------------------- logo (supplied raster, unchanged)
def load_logo():
    from PIL import ImageChops
    src = Image.open(os.path.join(REPO, "reels/assets/logo.webp")).convert("RGB")
    r, g, b = src.split()
    alpha = ImageChops.darker(ImageChops.darker(r, g), b).point(lambda v: max(0, min(255, int((250 - v) * 255 / 60))))
    src.putalpha(alpha)
    return src.crop(alpha.getbbox())


LOGO = load_logo()


def logo_w(w):  # proportional resize only
    return LOGO.resize((w, round(LOGO.height * w / LOGO.width)), Image.LANCZOS)


LOGO_S, LOGO_L = logo_w(230), logo_w(620)

# ---------------------------------------------------------------- copy + timing
HEADLINES = [  # (text, in s, out s)
    ("Il bagno\nche desideri.", 0.4, 3.75),
    ("Ogni dettaglio\nconta.", 4.3, 8.75),
    ("Spazi pensati\nper te.", 9.3, 15.75),
]
# Subtitles follow the narration draft; re-time to the delivered WAV.
SUBTITLES = [
    (0.5, 3.9, "Il bagno che desideri parte\nda un progetto pensato per te."),
    (4.3, 7.0, "Spazi più pratici,\nmateriali scelti con cura"),
    (7.0, 9.4, "e dettagli che fanno\nla differenza."),
    (10.2, 14.2, "Con Ristrutturare per Te puoi\nrinnovare il tuo bagno,"),
    (16.2, 19.6, "anche con pagamento a rate\nfino a dieci anni."),
    (20.3, 22.7, "Lavoriamo a Padova\ne provincia."),
    (23.4, 25.6, "Visita ristrutturareperte.it"),
    (25.6, 28.2, "e raccontaci il tuo progetto."),
]
RATE_IN, RATE_OUT = 16.2, 22.85
DISCLOSURE_PLACEHOLDER = "[NOTE LEGALI DEL FINANZIAMENTO: DA FORNIRE]"


def write_srt(path):
    def ts(s):
        ms = int(round(s * 1000))
        return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"
    with open(path, "w", encoding="utf-8") as f:
        for i, (a, b, text) in enumerate(SUBTITLES, 1):
            f.write(f"{i}\n{ts(a)} --> {ts(b)}\n{text}\n\n")


# ---------------------------------------------------------------- drawing helpers
PUNCT = ".,?:"


def draw_tight(d, xy, text, fnt, fill):
    """Pull punctuation in (the web-subset font spaces it loosely)."""
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


def tight_len(text, fnt):
    return fnt.getlength(text) - sum(fnt.size * 0.1 for ch in text if ch in PUNCT)


def fade(t, a, b, dur=0.3):
    return ease((t - a) / dur) * (1 - ease((t - (b - dur)) / dur))


TOP_SCRIM = Image.new("RGBA", (W, 640), (0, 0, 0, 0))
_d = ImageDraw.Draw(TOP_SCRIM)
for y in range(640):
    _d.line((0, y, W, y), fill=PAPER + (int(200 * (1 - y / 640) ** 1.6),))


def headline(layer, t):
    d = ImageDraw.Draw(layer)
    for text, a, b in HEADLINES:
        p = fade(t, a, b)
        if p <= 0:
            continue
        dy = int((1 - ease((t - a) / 0.35)) * 20)
        lines = text.split("\n")
        for i, line in enumerate(lines):
            draw_tight(d, (60, 250 + i * 82 + dy), line, F_HEAD, BLACK + (int(255 * p),))
        lp = ease((t - a - 0.15) / 0.3) * p
        uy = 250 + len(lines) * 82 + 16
        d.rectangle((60, uy, 60 + int(140 * lp), uy + 10), fill=YELLOW + (int(255 * p),))


def subtitle(layer, t):
    d = ImageDraw.Draw(layer)
    for a, b, text in SUBTITLES:
        p = fade(t, a, b, 0.12)
        if p <= 0:
            continue
        lines = text.split("\n")
        w = max(F_SUB.getlength(l) for l in lines)
        y0 = 1530 - len(lines) * 54 - 26           # bottom edge at y=1530: clear of the caption/UI area
        d.rounded_rectangle((52, y0, 52 + w + 40, 1530), 18, fill=(255, 255, 255, int(228 * p)))
        for i, line in enumerate(lines):
            d.text((72, y0 + 14 + i * 54), line, font=F_SUB, fill=BLACK + (int(255 * p),))


def rate_panel(layer, t):
    p = fade(t, RATE_IN, RATE_OUT, 0.4)
    if p <= 0:
        return
    d = ImageDraw.Draw(layer)
    dy = int((1 - ease((t - RATE_IN) / 0.45)) * 50)
    x0, y0, x1, y1 = 60, 250 + dy, 760, 590 + dy   # top-left block, clear of the right-side app controls
    d.rounded_rectangle((x0, y0, x1, y1), 30, fill=YELLOW + (int(250 * p),))
    a = int(255 * p)
    d.text((x0 + 44, y0 + 44), "Pagamento a rate", font=F_RATE1, fill=BLACK + (a,))
    draw_tight(d, (x0 + 44, y0 + 130), "fino a 10 anni", F_RATE2, BLACK + (a,))
    if ARGS.review:
        d.text((x0 + 44, y0 + 280), DISCLOSURE_PLACEHOLDER, font=F_TAG, fill=RED + (a,))


def end_card(t):
    frame = Image.new("RGBA", (W, H), PAPER + (255,))
    d = ImageDraw.Draw(frame)
    p = ease((t - 26.0) / 0.5)
    lg = LOGO_L.copy()
    lg.putalpha(lg.getchannel("A").point(lambda v: int(v * p)))
    frame.alpha_composite(lg, ((W - lg.width) // 2, 300 + int((1 - p) * 20)))
    if t >= 26.4:
        a = int(255 * ease((t - 26.4) / 0.35))
        lines = ["Parliamo del tuo", "nuovo bagno."]
        for i, line in enumerate(lines):
            draw_tight(d, (60, 760 + i * 84), line, F_CTA, BLACK + (a,))
        ax = 60 + int(tight_len(lines[-1], F_CTA)) + 26
        ay = 760 + 84 + 46
        d.rectangle((ax, ay - 4, ax + 52, ay + 4), fill=BLACK + (a,))
        d.polygon([(ax + 60, ay), (ax + 36, ay - 22), (ax + 36, ay + 22)], fill=BLACK + (a,))
        d.rectangle((60, 960, 60 + int(360 * ease((t - 26.6) / 0.4)), 970), fill=YELLOW)
    if t >= 26.8:
        a = int(255 * ease((t - 26.8) / 0.3))
        x, y = 60, 1010
        d.ellipse((x, y, x + 34, y + 34), fill=YELLOW + (a,))
        d.polygon([(x + 3, y + 24), (x + 31, y + 24), (x + 17, y + 50)], fill=YELLOW + (a,))
        d.ellipse((x + 11, y + 11, x + 23, y + 23), fill=PAPER + (a,))
        d.text((x + 56, y + 6), " ".join("PADOVA E PROVINCIA"), font=F_LABEL, fill=BLACK + (a,))
    if t >= 27.0:
        a = int(255 * ease((t - 27.0) / 0.3))
        url = "ristrutturareperte.it"
        d.rounded_rectangle((60, 1100, 60 + F_URL.getlength(url) + 64, 1196), 20, fill=YELLOW + (a,))
        d.text((92, 1118), url, font=F_URL, fill=BLACK + (a,))
    return frame


# ---------------------------------------------------------------- frames
SRC = {}
for path in glob.glob(os.path.join(ARGS.frames, "frame_*.png")):
    SRC[int(re.findall(r"(\d+)\.png$", path)[0])] = path
if not SRC:
    raise SystemExit("no frames found")


def frame_3d(n):
    avail = [k for k in SRC if k <= n] or [min(SRC)]
    img = Image.open(SRC[max(avail)]).convert("RGBA")
    return img.resize((W, H), Image.LANCZOS) if img.size != (W, H) else img


def render(n):
    t = t_of(n)
    if n >= END_CARD:
        frame = end_card(t)
        if n < END_CARD + 9:  # 0.3 s crossfade from the hero shot
            frame = Image.blend(frame_3d(END_CARD - 1), frame, (n - END_CARD + 1) / 9)
    else:
        frame = frame_3d(n)
        frame.alpha_composite(TOP_SCRIM)
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        headline(layer, t)
        rate_panel(layer, t)
        frame.alpha_composite(layer)
        frame.alpha_composite(LOGO_S, (W - 60 - LOGO_S.width, 230))
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    subtitle(layer, t)
    frame.alpha_composite(layer)
    if ARGS.review:
        d = ImageDraw.Draw(frame)
        d.rounded_rectangle((60, 150, 520, 194), 12, fill=RED)
        d.text((76, 157), "REVIEW · NON PUBBLICARE", font=F_TAG, fill=(255, 255, 255))
    return frame.convert("RGB")


def mix(video, out):
    inputs, chains, labels = ["-i", video], [], []
    idx = 1
    if ARGS.vo:
        inputs += ["-i", ARGS.vo]
        chains.append(f"[{idx}:a]aresample=48000,loudnorm=I=-15:TP=-1.5:LRA=7,asplit[vo][key]")
        idx += 1
    for name, path, gain in (("mu", ARGS.music, -2), ("fx", ARGS.sfx, -4)):
        if path:
            inputs += ["-i", path]
            chains.append(f"[{idx}:a]aresample=48000,volume={gain}dB[{name}]")
            labels.append(f"[{name}]")
            idx += 1
    bed = "".join(labels)
    chains.append(f"{bed}amix=inputs={len(labels)}:normalize=0[bed]")
    if ARGS.vo:
        chains.append("[bed][key]sidechaincompress=threshold=0.04:ratio=5:attack=25:release=450[duck]")
        chains.append("[vo][duck]amix=inputs=2:normalize=0,alimiter=limit=0.89[aout]")
    else:
        chains.append("[bed]alimiter=limit=0.89[aout]")
    subprocess.run([FFMPEG, "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(chains),
                    "-map", "0:v", "-map", "[aout]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-ar", "48000", "-ac", "2", "-t", str(TOTAL / FPS), "-movflags", "+faststart", out], check=True)


def main():
    if ARGS.srt:
        write_srt(ARGS.srt)
    has_audio = ARGS.vo or ARGS.music or ARGS.sfx
    video = tempfile.mktemp(suffix=".mp4") if has_audio else ARGS.out
    cmd = [FFMPEG, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
           "-pix_fmt", "yuv420p", "-movflags", "+faststart", video]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for n in range(1, TOTAL + 1):
        proc.stdin.write(render(n).tobytes())
    proc.stdin.close()
    if proc.wait():
        raise SystemExit("ffmpeg failed")
    if has_audio:
        mix(video, ARGS.out)
        os.remove(video)


if __name__ == "__main__":
    main()
