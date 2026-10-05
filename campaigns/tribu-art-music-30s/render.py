"""Render the 30 s vertical reel for Tribu del Alma's Art & Music Retreat.

Everything (copy, dates, colours, fonts, assets, shot timings, narration placement,
captions) comes from config.json. Frame n (zero-based) shows time n / fps; every frame is
computed from that time alone, so any frame can be rendered on its own.

Photos are real Tribu del Alma photographs. They are only cropped, scaled (aspect ratio
preserved) and slowly panned/zoomed; nothing is generated, retouched or animated inside
them. Copy and logo are separate 2D layers.

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
import os
import subprocess
import tempfile

import imageio_ffmpeg
import numpy as np
import pyloudnorm
import soundfile as sf
from PIL import Image, ImageDraw, ImageFilter, ImageFont
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


F_TITLE = {}


def title_font(size):
    if size not in F_TITLE:
        F_TITLE[size] = font("title", size)
    return F_TITLE[size]


F_LABEL = font("label", 30)
F_CAPTION = font("body", 40)
F_END_TITLE = font("title", 90)
F_END_DATES = font("body", 54)
F_END_PLACE = font("body", 42)
F_END_CTA = font("body", 46)
F_END_URL = font("body", 42)
F_END_BRAND = font("label", 28)


# ------------------------------------------------------------------ assets
USED = {}


def asset(key):
    a = CFG["assets"][key]
    if os.path.exists(path(a["original"])):
        USED[key] = a["original"]
    elif a.get("standin") and os.path.exists(path(a["standin"])):
        USED[key] = a["standin"]
    else:
        raise SystemExit(f"asset '{key}' missing: add {a['original']}")
    return Image.open(path(USED[key]))


IMAGES = {s["image"]: asset(s["image"]).convert("RGB") for s in CFG["shots"]}
LOGO_IS_ORIGINAL = os.path.exists(path(CFG["assets"]["logo"]["original"]))


def load_logo():
    im = asset("logo").convert("RGBA")
    if LOGO_IS_ORIGINAL:
        bw, bh = CFG["assets"]["logo"]["original_box"]
        s = min(bw / im.width, bh / im.height)            # proportional only
        return im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    # Stand-in: the emblem cut from the screenshot sits on the page's cream (#F0EEE2,
    # identical to our background). A soft circular mask removes the square edge.
    d = CFG["assets"]["logo"]["standin_display_px"]
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
    return 0.5 - 0.5 * np.cos(np.pi * x)


def lerp(a, b, p):
    return a + (b - a) * p


# ------------------------------------------------------------------ canvas
_grain = np.random.default_rng(7).normal(0, 1.6, (H, W, 1))
CANVAS = Image.fromarray(np.clip(np.array(C["cream"], np.float32)[None, None] + _grain, 0, 255).astype("uint8"))


# ------------------------------------------------------------------ panels and shots
PANELS = {k: tuple(v) for k, v in CFG["panels"].items()}
SHOTS = CFG["shots"]
SMALL_R = 22


def panel_geom(t):
    """Interpolated panel (x, y, w, h, arch radius, small radius) at time t."""
    for i, s in enumerate(SHOTS):
        if s["start"] <= t < s["end"] or (i == len(SHOTS) - 1 and t >= s["start"]):
            cur = PANELS[s["panel"]] + ((0 if s["panel"] == "band" else SMALL_R),)
            if i == 0:
                return cur
            prev_s = SHOTS[i - 1]
            prev = PANELS[prev_s["panel"]] + ((0 if prev_s["panel"] == "band" else SMALL_R),)
            p = ease_io((t - s["start"]) / max(s.get("xfade", 0.4), 1e-6))
            return tuple(lerp(a, b, p) for a, b in zip(prev, cur))
    raise ValueError(t)


_mask_cache = {}


def panel_mask(w, h, big, small):
    key = (w, h, int(round(big)), int(round(small)))
    if key not in _mask_cache:
        ss = 3
        m = Image.new("L", (w * ss, h * ss), 0)
        d = ImageDraw.Draw(m)
        r, R = key[3] * ss, key[2] * ss
        if r:
            d.rounded_rectangle((0, 0, w * ss - 1, h * ss - 1), r, fill=255)
        else:
            d.rectangle((0, 0, w * ss, h * ss), fill=255)
        if R:
            d.rectangle((0, 0, R, R), fill=0)
            d.pieslice((0, 0, 2 * R, 2 * R), 180, 270, fill=255)
        _mask_cache[key] = m.resize((w, h), Image.LANCZOS)
        if len(_mask_cache) > 64:
            _mask_cache.pop(next(iter(_mask_cache)))
    return _mask_cache[key]


UPSCALE = {}


def shot_frame(s, t, w, h):
    """Shot s at time t, covering a w x h panel. Linear Ken Burns so the motion can
    continue smoothly into the next shot's dissolve."""
    im = IMAGES[s["image"]]
    p = (t - s["start"]) / (s["end"] - s["start"])
    z = max(1.0, lerp(s["zoom"][0], s["zoom"][1], p))      # never below 'cover': no stretching, no gaps
    fx = lerp(s["focus"][0][0], s["focus"][1][0], p)
    fy = lerp(s["focus"][0][1], s["focus"][1][1], p)
    scale = max(w / im.width, h / im.height) * z
    cw, ch = min(w / scale, im.width), min(h / scale, im.height)
    cx = clamp(fx * im.width, cw / 2, im.width - cw / 2)
    cy = clamp(fy * im.height, ch / 2, im.height - ch / 2)
    UPSCALE[s["id"]] = max(UPSCALE.get(s["id"], 0), scale)
    return im.resize((w, h), Image.LANCZOS, box=(cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2))


def shot_index(t):
    idx = 0
    for i, s in enumerate(SHOTS):
        if t >= s["start"]:
            idx = i
    return idx


def draw_photo(frame, t):
    x, y, w, h, R, r = panel_geom(t)
    x, y, w, h = int(round(x)), int(round(y)), int(round(w)), int(round(h))
    i = shot_index(t)
    s = SHOTS[i]
    img = shot_frame(s, t, w, h)
    xf = s.get("xfade", 0.4)
    if i > 0 and t < s["start"] + xf:
        prev = shot_frame(SHOTS[i - 1], t, w, h)
        p = ease_io((t - s["start"]) / xf)
        if s.get("transition") == "open":
            # The new view opens from the centre outward, like doors onto the landscape.
            half = p * (w / 2 + 40)
            m = Image.new("L", (w, h), 0)
            ImageDraw.Draw(m).rectangle((w / 2 - half, 0, w / 2 + half, h), fill=255)
            m = m.filter(ImageFilter.GaussianBlur(14))
            img = Image.composite(img, prev, m)
        else:
            img = Image.blend(prev, img, p)
    frame.paste(img, (x, y), panel_mask(w, h, R, r))
    return (x, y, w, h)


# ------------------------------------------------------------------ designed text
def panel_bottom_at(t):
    s = SHOTS[shot_index(t)]
    x, y, w, h, _ = PANELS[s["panel"]]
    return y + h


TEXT_GAP = 46


def tracked(draw, xy, text, fnt, fill, spacing):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += fnt.getlength(ch) + spacing
    return x


def tracked_width(text, fnt, spacing):
    return sum(fnt.getlength(ch) for ch in text) + spacing * (len(text) - 1)


def block_layout(b):
    """Positions of the label and lines of a text block (no animation)."""
    fnt = title_font(b["size"])
    lh = round(b["size"] * 1.1)
    y = panel_bottom_at(b["start"] + 0.01) + TEXT_GAP
    items = []
    if "label" in b:
        items.append(("label", b["label"], SAFE["x0"], y))
        y += 52
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
        fnt, items = block_layout(b)
        for kind, it, x, y in items:
            if kind == "label":
                a, dy = appear(t, it["at"], b["end"])
                tracked(d, (x, y + dy), fmt(it["t"]).upper(), F_LABEL, C["rust"] + (int(255 * a),), 4)
                continue
            col = C["rust"] if it.get("accent") else C["deep_green"]
            words = it.get("words")
            if words:
                parts = it["t"].split("  ")
                cx = x
                for part, at in zip(parts, words):
                    a, dy = appear(t, at, b["end"])
                    if a > 0:
                        d.text((cx, y + dy), part, font=fnt, fill=col + (int(255 * a),))
                    cx += fnt.getlength(part + "  ")
            else:
                a, dy = appear(t, it["at"], b["end"])
                if a > 0:
                    d.text((x, y + dy), fmt(it["t"]), font=fnt, fill=col + (int(255 * a),))
        if b["start"] <= 0:         # hook: a gold rule draws itself under the question
            _, _, x, y = items[-1]
            ln = items[-1][1]["t"]
            p = ease_io((t - 0.5) / 1.1)
            a, _ = appear(t, 0, b["end"])
            if p > 0 and a > 0:
                wline = fnt.getlength(ln) * p
                yy = y + round(b["size"] * 1.02)
                d.rounded_rectangle((x, yy, x + wline, yy + 5), 2, fill=C["gold"] + (int(255 * a),))


# ------------------------------------------------------------------ end card
EC = CFG["endcard"]


def endcard_layout():
    """Element boxes for the end card, top to bottom (centered)."""
    band_bottom = PANELS["band"][1] + PANELS["band"][3]
    els = []
    if LOGO_IS_ORIGINAL:
        y = band_bottom + 36
        els.append(("logo", None, y, LOGO.height))
        y += LOGO.height + 44
    else:
        y = band_bottom - LOGO.height // 2
        els.append(("logo", None, y, LOGO.height))
        y += LOGO.height + 22
        els.append(("brand", EC["brand_label_with_standin_logo"], y, 30))
        y += 30 + 40
    els.append(("title", EV["name"], y, 90))
    y += 90 + 46
    els.append(("dates", EV["dates_display"], y, 54))
    y += 54 + 22
    els.append(("place", EV["location_endcard"], y, 42))
    y += 42 + 62
    els.append(("cta", EV["cta"], y, 46 + 2 * 28))
    y += 46 + 2 * 28 + 44
    els.append(("url", EV["website"], y, 42))
    return els


def draw_endcard(frame, layer, t):
    start = SHOTS[-1]["start"]
    if t < start:
        return
    d = ImageDraw.Draw(layer)
    times = {"logo": start + 0.35, "brand": start + 0.5, "title": EC["title_at"], "dates": EC["dates_at"],
             "place": EC["place_at"], "cta": EC["cta_at"], "url": EC["url_at"]}
    for kind, text, y, h in endcard_layout():
        a = ease((t - times[kind]) / 0.6)
        if a <= 0:
            continue
        dy = (1 - a) * 16
        if kind == "logo":
            if not LOGO_IS_ORIGINAL:   # cream seal so the emblem reads over the photo edge
                cx, cy, r = int(CX), y + h // 2, h // 2 + 22
                seal = Image.new("RGBA", (4 * r, 4 * r), (0, 0, 0, 0))
                ImageDraw.Draw(seal).ellipse((0, 0, 4 * r - 1, 4 * r - 1), fill=C["cream"] + (int(255 * a),))
                seal = seal.resize((2 * r, 2 * r), Image.LANCZOS)
                frame.alpha_composite(seal, (cx - r, int(cy - r + dy)))
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
            if kind == "url":
                uw = tw * ease_io((t - times[kind] - 0.2) / 0.8)
                d.rectangle((CX - tw / 2, y + 58, CX - tw / 2 + uw, y + 61), fill=C["gold"] + (int(255 * a),))


# ------------------------------------------------------------------ captions
CAPS = [dict(c, t=fmt(c["t"])) for c in CFG["captions"]]
CAP_LH = 52


def caption_box(text, bottom):
    lines = text.split("\n")
    tw = max(F_CAPTION.getlength(l) for l in lines)
    h = CAP_LH * len(lines) + 30
    x0 = CX - tw / 2 - 26
    return lines, (x0, bottom - h, 2 * CX - x0, bottom)


def caption_bottom(t):
    """Captions sit just inside the bottom of the photo; into the end card they glide up
    with the panel into the band, above the logo seal."""
    y, h = panel_geom(t)[1], panel_geom(t)[3]
    last = SHOTS[-1]
    if t >= last["start"]:
        p = ease_io((t - last["start"]) / last.get("xfade", 0.4))
        band = PANELS["band"][1] + PANELS["band"][3] - 150
        before = PANELS[SHOTS[-2]["panel"]][1] + PANELS[SHOTS[-2]["panel"]][3] - 34
        return lerp(before, band, p)
    return y + h - 34


def draw_captions(layer, t):
    d = ImageDraw.Draw(layer)
    for c in CAPS:
        if not (c["start"] <= t < c["end"]):
            continue
        a = ease((t - c["start"]) / 0.12) * (1 - ease((t - (c["end"] - 0.12)) / 0.12))
        lines, (x0, y0, x1, y1) = caption_box(c["t"], caption_bottom(t))
        d.rounded_rectangle((x0, y0, x1, y1), 16, fill=C["deep_green"] + (int(215 * a),))
        for i, ln in enumerate(lines):
            d.text((CX - F_CAPTION.getlength(ln) / 2, y0 + 14 + i * CAP_LH), ln, font=F_CAPTION,
                   fill=C["cream"] + (int(255 * a),))


def write_srt(fn):
    def ts(s):
        ms = int(round(s * 1000))
        return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"
    with open(fn, "w", encoding="utf-8") as f:
        for i, c in enumerate(CAPS, 1):
            f.write(f"{i}\n{ts(c['start'])} --> {ts(c['end'])}\n{c['t']}\n\n")


# ------------------------------------------------------------------ layout check
def check_layout():
    """Fail the build if essential text leaves the safe area or text blocks collide."""
    x0, x1, y0, y1 = SAFE["x0"], SAFE["x1"], SAFE["y0"], SAFE["y1"]
    problems = []
    for b in CFG["text"]:
        fnt, items = block_layout(b)
        for kind, it, x, y in items:
            if kind == "label":
                w, hh = tracked_width(fmt(it["t"]).upper(), F_LABEL, 4), 34
            else:
                w, hh = fnt.getlength(fmt(it["t"])), round(b["size"] * 1.05)
            if x + w > x1 or y < y0 or y + hh > y1:
                problems.append(f"text '{it['t']}' box ({x},{y})-({x + w:.0f},{y + hh}) outside safe area")
        if len([i for i in items if i[0] == "line"]) > 2:
            problems.append(f"text block at {b['start']} has more than two lines")
    for kind, text, y, h in endcard_layout():
        if kind == "logo":
            w = LOGO.width
        elif kind == "cta":
            w = F_END_CTA.getlength(text) + 96
        elif kind == "brand":
            w = tracked_width(text, F_END_BRAND, 6)
        else:
            w = {"title": F_END_TITLE, "dates": F_END_DATES, "place": F_END_PLACE, "url": F_END_URL}[kind].getlength(text)
        if CX - w / 2 < x0 or CX + w / 2 > x1 or y + h > y1 or (kind != "logo" and y < y0):
            problems.append(f"end card '{kind}' outside safe area (w {w:.0f}, y {y}-{y + h})")
    for c in CAPS:
        for t in np.arange(c["start"], c["end"], 1 / FPS):
            lines, (cx0, cy0, cx1, cy1) = caption_box(c["t"], caption_bottom(t))
            if cx0 < x0 or cx1 > x1 or cy0 < y0 or cy1 > y1 or len(lines) > 2:
                problems.append(f"caption '{c['t']}' outside safe area at {t:.2f}s")
                break
    cta_shown = DUR - EC["cta_at"]
    if cta_shown < 4.0:
        problems.append(f"CTA visible only {cta_shown:.1f}s")
    if problems:
        raise SystemExit("layout check failed:\n  " + "\n  ".join(problems))
    print(f"layout check ok (CTA visible {cta_shown:.1f}s)")


# ------------------------------------------------------------------ frames
def render(n, captions=False):
    t = n / FPS
    frame = CANVAS.copy().convert("RGBA")
    draw_photo(frame, t)
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


def read_48k_stereo(fn):
    x, sr = sf.read(fn, always_2d=True)
    x = x.mean(1)
    if sr != SR:
        g = np.gcd(sr, SR)
        x = resample_poly(x, SR // g, sr // g)
    return x


def build_audio(with_vo):
    n = int(SR * DUR)
    au = CFG["audio"]
    music = read_48k_stereo(path(au["music"]))[:n]
    music = np.pad(music, (0, n - len(music)))
    music_st, _ = sf.read(path(au["music"]), always_2d=True)
    music_st = np.pad(music_st[:n], ((0, max(0, n - len(music_st))), (0, 0)))
    meter = pyloudnorm.Meter(SR)
    if not with_vo:
        g = 10 ** ((au["vo_loudness_lufs"] + au["music_gain_without_vo_db"] + 6 - meter.integrated_loudness(music_st)) / 20)
        mix = music_st * g
    else:
        vo = np.zeros(n)
        for clip in CFG["voiceover"]["clips"]:
            x = read_48k_stereo(path(os.path.join(au["vo_dir"], clip["id"] + ".wav")))
            i = int(round(clip["at"] * SR))
            fade = int(0.008 * SR)
            x[:fade] *= np.linspace(0, 1, fade)
            x[-fade:] *= np.linspace(1, 0, fade)
            assert i + len(x) <= n, f"narration clip {clip['id']} runs past the end"
            vo[i:i + len(x)] += x
        vo *= 10 ** ((au["vo_loudness_lufs"] - meter.integrated_loudness(vo)) / 20)
        # Music sits under the voice and ducks a further 5 dB while she speaks.
        g = 10 ** ((au["vo_loudness_lufs"] + au["music_gain_db"] - meter.integrated_loudness(music_st)) / 20)
        env = np.abs(vo)
        win = int(0.05 * SR)
        env = np.convolve(env, np.ones(win) / win, "same")
        speaking = (env > env.max() * 0.04).astype(float)
        k = int(0.35 * SR)
        speaking = np.convolve(speaking, np.ones(k) / k, "same")
        duck = 10 ** (-5 * np.clip(speaking * 1.5, 0, 1) / 20)
        mix = music_st * (g * duck)[:, None] + vo[:, None]
    peak = np.abs(mix).max()
    ceiling = 10 ** (-1.5 / 20)
    if peak > ceiling:              # simple safety gain; the mix has no transient peaks worth limiting
        mix *= ceiling / peak
    return mix


def audio_report(fn):
    out = subprocess.run([FFMPEG, "-hide_banner", "-nostats", "-i", fn, "-af", "ebur128=peak=true", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    lines = [l.strip() for l in out.splitlines() if l.strip().startswith(("I:", "Peak:"))]
    return " ".join(lines[-2:])


# ------------------------------------------------------------------ contact sheet
SHEET = [(1.5, "0–4 s  Recognition"), (6.2, "4–8 s  Possibility"), (12.0, "8–13 s  Creative freedom"),
         (15.6, "13–18 s  Connection"), (22.6, "18–24 s  The experience"), (28.0, "24–30 s  Invitation")]


def contact_sheet(fn):
    tw, th, pad, head = 360, 640, 24, 54
    sheet = Image.new("RGB", (3 * tw + 4 * pad, 2 * (th + head) + 3 * pad + 70), C["cream"])
    d = ImageDraw.Draw(sheet)
    d.text((pad, 22), f"Tribu del Alma · {EV['name']} · 30 s reel · contact sheet", font=font("title", 34), fill=C["deep_green"])
    for i, (t, label) in enumerate(SHEET):
        x = pad + (i % 3) * (tw + pad)
        y = 70 + pad + (i // 3) * (th + head + pad)
        n = int(round(t * FPS))
        d.text((x, y + 4), label, font=font("body", 20), fill=C["deep_green"])
        d.text((x, y + 28), f"frame {n} · {t:.1f} s", font=font("body", 15), fill=C["sage"])
        sheet.paste(render(n).resize((tw, th), Image.LANCZOS), (x, y + head))
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
    print("assets used:", json.dumps(USED, indent=1))
    print("max upscale per shot:", {k: round(v, 2) for k, v in UPSCALE.items()})


if __name__ == "__main__":
    main()
