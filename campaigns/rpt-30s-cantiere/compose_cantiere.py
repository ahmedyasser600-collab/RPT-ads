"""Compose the 30s RPT reel "Dal bagno all'intero edificio" (photo-based, no 3D).

Real construction photos ("Prima") and AI-generated design concepts ("Dopo") are separate
layers in a framed 3:4 window on the brand canvas. Because the "Dopo" images are
illustrative concepts, not finished RPT work, a footnote is shown whenever one is on screen.
Copy, labels, subtitles and logo are 2D layers drawn here, never baked into images.
Frame n is zero-based and shown at n/30 s; 900 frames.

Usage:
  python compose_cantiere.py --out reel.mp4 [--size 540] [--vo audio/vo.wav]
         [--music audio/music.wav] [--sfx audio/sfx.wav] [--srt captions.srt]
         [--storyboard storyboard.png]
"""
import argparse
import os
import subprocess
import tempfile

import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
ap = argparse.ArgumentParser()
ap.add_argument("--out", required=True)
ap.add_argument("--size", type=int, default=1080, help="output width (1080 final, 540 review)")
ap.add_argument("--vo")
ap.add_argument("--music")
ap.add_argument("--sfx")
ap.add_argument("--srt")
ap.add_argument("--storyboard")
ARGS = ap.parse_args()

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
W, H, FPS, TOTAL = 1080, 1920, 30, 900
YELLOW = (245, 187, 29)              # #F5BB1D, sampled from the supplied raster logo
BLACK = (20, 20, 20)
PAPER = (244, 241, 236)
SAFE_X0, SAFE_X1, SAFE_Y0, SAFE_Y1 = 100, 900, 240, 1530   # important text stays inside


def font(weight, size):
    return ImageFont.truetype(os.path.join(HERE, "fonts", f"plus-jakarta-sans-latin-{weight}-normal.woff"), size)


F_HEAD, F_SUB, F_LABEL, F_CARD = font(800, 64), font(600, 38), font(600, 26), font(600, 20)
F_CTA, F_URL, F_PLACE = font(800, 74), font(800, 54), font(500, 32)


def ease(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


def ease_io(x):
    x = max(0.0, min(1.0, x))
    return 4 * x ** 3 if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2


def lin(n, a, b):
    return max(0.0, min(1.0, (n - a) / max(1, b - a)))


# ---------------------------------------------------------------- assets
def photo(name, crop=None):
    im = Image.open(os.path.join(HERE, "photos", name)).convert("RGB")
    if crop:
        im = im.crop(crop)
    assert abs(im.width / im.height - 0.75) < 0.01, (name, im.size)   # 3:4, never stretched
    return im


REAL, CONCEPT = "Prima", "Dopo"
FOOTNOTE = "Immagini “dopo” a scopo illustrativo"
IMG = {
    "o1": (photo("originals/01_original_demolition.jpg"), REAL),
    "c1": (photo("concepts/01_concept_bathroom.webp"), CONCEPT),
    "o2": (photo("originals/02_original_room.jpg"), REAL),
    "c2": (photo("concepts/02_concept_study.webp"), CONCEPT),
    "o3": (photo("originals/03_original_staircase_portal.jpg"), REAL),
    # crop keeps the staircase and leaves the worker at the right edge out of frame
    "o4": (photo("originals/04_original_staircase_wide.jpg", crop=(0, 150, 1280, 1857)), REAL),
    "c3": (photo("concepts/03_concept_staircase_portal.webp"), CONCEPT),
    "c4": (photo("concepts/04_concept_staircase_wide.webp"), CONCEPT),
}


def load_logo():
    src = Image.open(os.path.join(REPO, "reels/assets/logo.webp")).convert("RGB")
    r, g, b = src.split()
    alpha = ImageChops.darker(ImageChops.darker(r, g), b).point(lambda v: max(0, min(255, int((250 - v) * 255 / 60))))
    src.putalpha(alpha)
    return src.crop(alpha.getbbox())


LOGO = load_logo()


def logo_w(w):  # proportional resize only
    return LOGO.resize((w, round(LOGO.height * w / LOGO.width)), Image.LANCZOS)


LOGO_S, LOGO_L = logo_w(190), logo_w(600)

# Canvas with a faint, fixed paper grain.
_g = np.random.default_rng(5).normal(0, 2.2, (H, W, 1))
CANVAS = Image.fromarray(np.clip(np.array(PAPER, dtype=np.float32)[None, None, :] + _g, 0, 255).astype("uint8"), "RGB").convert("RGBA")

# Main photo window (3:4).
FX, FY, FW, FH = 140, 450, 800, 1067


def shadow(w, h, blur=26, alpha=70):
    s = Image.new("RGBA", (w + 4 * blur, h + 4 * blur), (0, 0, 0, 0))
    ImageDraw.Draw(s).rectangle((2 * blur, 2 * blur, 2 * blur + w, 2 * blur + h), fill=(60, 45, 30, alpha))
    return s.filter(ImageFilter.GaussianBlur(blur)), 2 * blur


SHADOW_MAIN = shadow(FW, FH)


# ---------------------------------------------------------------- layers
def label_chip(text, kind, fnt=F_LABEL, pad=(16, 9)):
    lines = text.split("\n")
    lh = int(fnt.size * 1.25)
    w = int(max(fnt.getlength(l) for l in lines)) + 2 * pad[0]
    h = lh * (len(lines) - 1) + fnt.size + 2 * pad[1] + 4
    chip = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(chip)
    bg, fg = ((20, 20, 20, 225), (255, 255, 255)) if kind == REAL else (YELLOW + (240,), BLACK)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 10, fill=bg)
    for i, line in enumerate(lines):
        d.text((pad[0], pad[1] + i * lh), line, font=fnt, fill=fg)
    return chip


F_CHIP = font(800, 36)
CHIPS = {REAL: label_chip(REAL, REAL, F_CHIP, (20, 10)), CONCEPT: label_chip(CONCEPT, CONCEPT, F_CHIP, (20, 10))}


def framed(key, w, h, zoom=1.0, focus=(0.5, 0.5), chip=True):
    """Photo `key` filling a w x h window, pushed in by `zoom` around `focus`, with its label."""
    im, kind = IMG[key]
    cw, ch = im.width / zoom, im.height / zoom
    cx = min(max(focus[0] * im.width, cw / 2), im.width - cw / 2)
    cy = min(max(focus[1] * im.height, ch / 2), im.height - ch / 2)
    out = im.resize((w, h), Image.LANCZOS, box=(cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2)).convert("RGBA")
    if chip:
        out.alpha_composite(CHIPS[kind], (18, 18))
    return out


# Shots: key, first frame, last frame, zoom from -> to, focus. Zero-based inclusive frames.
SHOTS = [
    ("o1", 0, 101, 1.00, 1.045, (0.45, 0.62)),       # real demolition, slow push
    ("c1", 90, 209, 1.00, 1.040, (0.50, 0.45)),      # wipe in at 90
    ("o2", 210, 314, 1.00, 1.060, (0.46, 0.39)),     # push toward the existing window
    ("c2", 300, 419, 1.00, 1.035, (0.42, 0.40)),     # dissolve in at 300
    ("o3", 420, 479, 1.06, 1.00, (0.45, 0.50)),      # pull back: growing sense of scale
    ("o4", 480, 551, 1.05, 1.00, (0.40, 0.55)),
    ("c3", 540, 629, 1.00, 1.040, (0.45, 0.45)),     # wipe in at 540 (through the portal)
    ("c4", 630, 737, 1.00, 1.040, (0.55, 0.50)),     # cut, matching gentle push
]
WIPES = {90: ("o1", "c1", 12), 540: ("o4", "c3", 12)}      # start frame: (from, to, length)
DISSOLVE = (300, 15)                                         # o2 -> c2


def shot_img(key, n, w=FW, h=FH, chip=True):
    for k, a, b, z0, z1, focus in SHOTS:
        if k == key:
            p = ease_io(lin(n, a, b))
            return framed(key, w, h, z0 + (z1 - z0) * p, focus, chip)
    raise KeyError(key)


def window(n):
    """The main photo window for frames 0-719. During a wipe or dissolve exactly one whole
    label is shown (never a cut-off or cross-faded one): the outgoing image's until the
    transition has passed the label, then the incoming image's."""
    for start, (a, b, length) in WIPES.items():
        if start <= n < start + length:
            p = ease_io((n - start + 1) / length)
            img = shot_img(a, n, chip=False)
            edge = int(FW * p)
            img.paste(shot_img(b, n, chip=False).crop((0, 0, edge, FH)), (0, 0))
            if 0 < edge < FW:
                ImageDraw.Draw(img).rectangle((edge - 5, 0, edge + 5, FH), fill=YELLOW + (255,))
            incoming = edge >= 18 + CHIPS[IMG[b][1]].width
            img.alpha_composite(CHIPS[IMG[b if incoming else a][1]], (18, 18))
            return img
    s, length = DISSOLVE
    if s <= n < s + length:
        p = ease_io((n - s + 1) / length)
        img = Image.blend(shot_img("o2", n, chip=False), shot_img("c2", n, chip=False), p)
        img.alpha_composite(CHIPS[IMG["c2" if p >= 0.5 else "o2"][1]], (18, 18))
        return img
    order = [(0, "o1"), (90, "c1"), (210, "o2"), (300, "c2"), (420, "o3"), (480, "o4"), (540, "c3"), (630, "c4")]
    key = [k for f, k in order if n >= f][-1]
    return shot_img(key, n)


# ---------------------------------------------------------------- copy
HEADLINES = [  # text, first frame, last frame
    ("Dal bagno…", 4, 87),
    ("Diamo forma\nalle idee.", 96, 206),
    ("Agli ambienti\ndi casa.", 214, 296),
    ("Nuove\npossibilità.", 306, 416),
    ("Fino all'intero\nedificio.", 424, 536),
    ("Pensiamo\nin grande.", 546, 716),
    ("Qual è il tuo\nprossimo\nprogetto?", 732, 806),
]
HEAD_X, HEAD_Y, HEAD_LH = SAFE_X0, 252, 72

# Subtitles follow audio/vo.wav (speech spans printed by audio/place_vo.py), in seconds.
SUBTITLES = [
    (0.30, 4.00, "Dal bagno di casa\nagli interventi su un intero edificio."),
    (4.20, 7.34, "Ogni progetto parte\nda uno spazio da trasformare"),
    (7.34, 9.30, "e da un'idea da costruire."),
    (9.50, 13.28, "Con Ristrutturare per Te,\nguardiamo oltre il cantiere"),
    (13.28, 15.50, "e immaginiamo\nnuove possibilità."),
    (15.80, 19.37, "Qui ti mostriamo lavori in corso\ne possibili finiture:"),
    (19.37, 22.50, "dal singolo ambiente\nai progetti più grandi."),
    (24.10, 26.00, "Hai uno spazio da rinnovare?"),
    (27.30, 28.60, "Parliamone insieme."),     # in the SRT; the end card already shows this line
]
SUB_BOTTOM = SAFE_Y1
END_CARD = 810


def write_srt(path):
    def ts(s):
        ms = int(round(s * 1000))
        return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"
    with open(path, "w", encoding="utf-8") as f:
        for i, (a, b, text) in enumerate(SUBTITLES, 1):
            f.write(f"{i}\n{ts(a)} --> {ts(b)}\n{text}\n\n")


def check_layout():
    """Fail early if any copy leaves the safe area or runs into the logo."""
    logo_x0 = SAFE_X1 - LOGO_S.width
    for text, _, _ in HEADLINES:
        for i, line in enumerate(text.split("\n")):
            w = F_HEAD.getlength(line)
            right = HEAD_X + w
            y0 = HEAD_Y + i * HEAD_LH
            limit = logo_x0 - 24 if y0 < HEAD_Y + LOGO_S.height else SAFE_X1
            assert right <= limit, f"headline too wide: {line!r} ({right:.0f} > {limit})"
    for _, _, text in SUBTITLES:
        w = max(F_SUB.getlength(l) for l in text.split("\n"))
        assert SAFE_X0 + 20 + w + 20 <= SAFE_X1, f"subtitle too wide: {text!r} ({w:.0f})"
    assert FX + 18 + CHIPS[CONCEPT].width <= SAFE_X1, "concept label too wide"
    assert FX + F_NOTE.getlength(FOOTNOTE) <= SAFE_X1, "footnote too wide"
    last = HEAD_Y + 2 * HEAD_LH + F_HEAD.size + 14            # bottom of a 3-line headline (with descenders)
    assert last <= 480 and 480 + F_NOTE.size + 6 <= CARDS[0][2], "footnote collides on the panel layout"


def fade(n, a, b, dur=8):
    return ease((n - a) / dur) * (1 - ease((n - (b - dur)) / dur))


def draw_headline(layer, n):
    d = ImageDraw.Draw(layer)
    for text, a, b in HEADLINES:
        p = fade(n, a, b)
        if p <= 0:
            continue
        dy = int((1 - ease((n - a) / 12)) * 16)
        for i, line in enumerate(text.split("\n")):
            d.text((HEAD_X, HEAD_Y + i * HEAD_LH + dy), line, font=F_HEAD, fill=BLACK + (int(255 * p),))


F_NOTE = font(500, 24)
DOPO_ON_SCREEN = [(90, 210), (300, 420), (540, END_CARD + 12)]   # frames where a "Dopo" image is visible


def draw_footnote(layer, n):
    p = max(fade(n, a, b, 6) for a, b in DOPO_ON_SCREEN)
    if p <= 0:
        return
    y = 412 if n < PANEL_IN else 480              # below the 2-line / 3-line headline, above the photos
    ImageDraw.Draw(layer).text((FX, y), FOOTNOTE, font=F_NOTE, fill=(95, 88, 80, int(255 * p)))


def draw_subtitle(layer, n):
    t = n / FPS
    if n >= END_CARD:
        return
    d = ImageDraw.Draw(layer)
    for a, b, text in SUBTITLES:
        p = ease((t - a) / 0.12) * (1 - ease((t - (b - 0.12)) / 0.12))
        if p <= 0:
            continue
        lines = text.split("\n")
        w = max(F_SUB.getlength(l) for l in lines)
        y0 = SUB_BOTTOM - len(lines) * 50 - 26
        d.rounded_rectangle((SAFE_X0, y0, SAFE_X0 + w + 40, SUB_BOTTOM), 16, fill=(255, 255, 255, int(232 * p)))
        for i, line in enumerate(lines):
            d.text((SAFE_X0 + 20, y0 + 13 + i * 50), line, font=F_SUB, fill=BLACK + (int(255 * p),))


# ---------------------------------------------------------------- panels (720-809) and end card
CARD_W, CARD_H = 380, 507
CARDS = [  # key, target x, y
    ("c1", SAFE_X0 + 10, 510),
    ("c2", SAFE_X1 - 10 - CARD_W, 510),
    ("c4", (W - CARD_W) // 2, 1040),
]
CARD_CHIP = label_chip(CONCEPT, CONCEPT, F_LABEL, (14, 8))
SHADOW_CARD = shadow(CARD_W, CARD_H, 18, 60)
PANEL_IN = 720


def card_img(key, n):
    img = framed(key, CARD_W, CARD_H, 1.0 + 0.03 * lin(n, PANEL_IN, END_CARD), (0.5, 0.5), chip=False)
    img.alpha_composite(CARD_CHIP, (12, 12))
    return img


def draw_panels(frame, n):
    out = ease(lin(n, END_CARD, END_CARD + 12))                   # cards leave for the end card
    if out >= 1:
        return
    for i, (key, x, y) in enumerate(CARDS):
        alpha = 1.0
        if key == "c4":                                            # the big window shrinks into its card
            p = ease_io(lin(n, PANEL_IN, PANEL_IN + 18))
            cw, ch = int(FW + (CARD_W - FW) * p), int(FH + (CARD_H - FH) * p)
            cx, cy = int(FX + (x - FX) * p), int(FY + (y - FY) * p)
            if p < 1:
                img = framed("c4", cw, ch, 1.04, (0.55, 0.5), chip=False)
                big = cw > 600
                img.alpha_composite(CHIPS[CONCEPT] if big else CARD_CHIP, (18, 18) if big else (12, 12))
            else:
                img = card_img(key, n)
        else:
            p = ease(lin(n, PANEL_IN + 6 + 5 * i, PANEL_IN + 24 + 5 * i))
            cx, cy, img = x, y + int((1 - p) * 60), card_img(key, n)
            alpha = p
        cy += int(out * 50)
        alpha *= 1 - out
        if alpha <= 0:
            continue
        sh, off = SHADOW_CARD if img.size == (CARD_W, CARD_H) else shadow(img.width, img.height, 18, 60)
        if alpha < 1:
            img.putalpha(img.getchannel("A").point(lambda v, a=alpha: int(v * a)))
            sh = sh.copy()
            sh.putalpha(sh.getchannel("A").point(lambda v, a=alpha: int(v * a)))
        frame.alpha_composite(sh, (cx - off + 6, cy - off + 12))
        frame.alpha_composite(img, (cx, cy))


def draw_end_card(frame, n):
    d = ImageDraw.Draw(frame)
    p = ease(lin(n, END_CARD + 6, END_CARD + 20))
    lg = LOGO_L.copy()
    lg.putalpha(lg.getchannel("A").point(lambda v: int(v * p)))
    frame.alpha_composite(lg, ((W - lg.width) // 2, 330 + int((1 - p) * 20)))
    a = int(255 * ease(lin(n, END_CARD + 14, END_CARD + 26)))
    dy = int((1 - ease(lin(n, END_CARD + 14, END_CARD + 26))) * 24)
    if a:
        d.text((SAFE_X0, 760 + dy), "Parliamone insieme.", font=F_CTA, fill=BLACK + (a,))
        uw = int(360 * ease_io(lin(n, END_CARD + 22, END_CARD + 36)))
        if uw:
            d.rectangle((SAFE_X0, 860, SAFE_X0 + uw, 870), fill=YELLOW)
    a = int(255 * ease(lin(n, END_CARD + 24, END_CARD + 34)))
    if a:
        x, y = SAFE_X0, 910
        d.ellipse((x, y, x + 34, y + 34), fill=YELLOW + (a,))
        d.polygon([(x + 3, y + 24), (x + 31, y + 24), (x + 17, y + 50)], fill=YELLOW + (a,))
        d.ellipse((x + 11, y + 11, x + 23, y + 23), fill=PAPER + (a,))
        d.text((x + 56, y + 2), " ".join("PADOVA E PROVINCIA"), font=F_PLACE, fill=BLACK + (a,))
    a = int(255 * ease(lin(n, END_CARD + 30, END_CARD + 40)))
    if a:
        url = "ristrutturareperte.it"
        d.rounded_rectangle((SAFE_X0, 1000, SAFE_X0 + F_URL.getlength(url) + 64, 1096), 20, fill=YELLOW + (a,))
        d.text((SAFE_X0 + 32, 1018), url, font=F_URL, fill=BLACK + (a,))


# ---------------------------------------------------------------- frames
def render(n):
    frame = CANVAS.copy()
    if n < PANEL_IN:
        sh, off = SHADOW_MAIN
        frame.alpha_composite(sh, (FX - off + 8, FY - off + 16))
        frame.alpha_composite(window(n), (FX, FY))
    else:
        draw_panels(frame, n)
    if n >= END_CARD:
        draw_end_card(frame, n)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_headline(layer, n)
    draw_footnote(layer, n)
    draw_subtitle(layer, n)
    frame.alpha_composite(layer)
    if n < END_CARD + 6:                                          # small logo until the big one takes over
        a = 1 - ease(lin(n, END_CARD, END_CARD + 6))
        lg = LOGO_S if a >= 1 else LOGO_S.copy()
        if a < 1:
            lg.putalpha(lg.getchannel("A").point(lambda v: int(v * a)))
        frame.alpha_composite(lg, (SAFE_X1 - LOGO_S.width, HEAD_Y + 4))
    return frame.convert("RGB")


def mix(video, out):
    inputs, chains, labels = ["-i", video], [], []
    idx = 1
    if ARGS.vo:
        inputs += ["-i", ARGS.vo]
        chains.append(f"[{idx}:a]aresample=48000,loudnorm=I=-15:TP=-2:LRA=7,aresample=48000,apad,asplit[vo][key]")
        idx += 1
    for name, path, gain in (("mu", ARGS.music, -3), ("fx", ARGS.sfx, -6)):
        if path:
            inputs += ["-i", path]
            chains.append(f"[{idx}:a]aresample=48000,volume={gain}dB[{name}]")
            labels.append(f"[{name}]")
            idx += 1
    chains.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0[bed]")
    if ARGS.vo:
        chains.append("[bed][key]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=500[duck]")
        chains.append("[vo][duck]amix=inputs=2:normalize=0,alimiter=limit=0.84:level=false[aout]")
    else:
        chains.append("[bed]alimiter=limit=0.84:level=false[aout]")
    subprocess.run([FFMPEG, "-nostdin", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(chains),
                    "-map", "0:v", "-map", "[aout]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-ar", "48000", "-ac", "2", "-t", str(TOTAL / FPS), "-movflags", "+faststart", out], check=True)


def storyboard(path):
    picks = [(45, "0-3 s  Prima: demolizione"), (150, "3-7 s  Dopo: bagno"),
             (255, "7-10 s  Prima: stanza"), (360, "10-14 s  Dopo: studio"),
             (450, "14-16 s  Prima: scala (portale)"), (510, "16-18 s  Prima: scala"),
             (585, "18-21 s  Dopo: scala (portale)"), (675, "21-24 s  Dopo: scala"),
             (775, "24-27 s  Tre progetti"), (880, "27-30 s  End card")]
    tw, th = 270, 480
    f = font(600, 15)
    sheet = Image.new("RGB", (5 * (tw + 12) + 12, 2 * (th + 44) + 12), (255, 255, 255))
    d = ImageDraw.Draw(sheet)
    for i, (n, text) in enumerate(picks):
        x, y = 12 + (i % 5) * (tw + 12), 12 + (i // 5) * (th + 44)
        sheet.paste(render(n).resize((tw, th), Image.LANCZOS), (x, y + 32))
        d.text((x, y + 6), f"f{n}  {text}", font=f, fill=(0, 0, 0))
    sheet.save(path)


def main():
    check_layout()
    if ARGS.srt:
        write_srt(ARGS.srt)
    if ARGS.storyboard:
        storyboard(ARGS.storyboard)
    has_audio = ARGS.vo or ARGS.music or ARGS.sfx
    video = tempfile.mktemp(suffix=".mp4") if has_audio else ARGS.out
    ow = ARGS.size
    oh = ow * H // W
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
        mix(video, ARGS.out)
        os.remove(video)


if __name__ == "__main__":
    main()
