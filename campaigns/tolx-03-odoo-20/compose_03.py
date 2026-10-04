"""Compose TOLX video 03 "Odoo 20 is here. Why move now?" (33.7 s).

For owners still on chats and spreadsheets who are new to Odoo. Three Odoo 20 features, as
described by Odoo's own announcement and release notes (released 24 Sept 2026):
  - AI agent: describe a process in plain language; it explains what it will do before it runs
    (Odoo's own example includes "alert on low stock").
  - Accounting AI agent: ask about receivables / cash flow, answers pulled from your reports.
  - Point of Sale offline mode.
The screens are TOLX-style recreations, NOT Odoo screenshots, and are labelled illustrative.
Figures and customer names are invented. "Odoo 20" is set in TOLX type (no Odoo logo); the
official Odoo Ready Partner badge (from the TOLX theme, unchanged) appears on the end card.
Shared brand/layout/audio code: ../tolx-kit. Frame n is shown at n/30 s.
"""
import math
import os
import sys
from functools import lru_cache

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "tolx-kit"))
import tolx_kit as K  # noqa: E402
from tolx_kit import (BG, GOLD, GREEN, MUTED, RAISED, RED, SURFACE, SURFACE2, TEXT, TEXT2, W,  # noqa: E402
                      back, ease, ease_io, lin, put, put_text, rrect, text_sprite)
from PIL import Image, ImageDraw  # noqa: E402

from timeline import *  # noqa: E402,F401,F403

ARGS = K.parse_args(__doc__)
K.setup(ARGS.format, END_CARD, TOTAL)
K.FOOTNOTE = "Illustrative screens and figures. Not a client project."

HEADLINES = [
    (PAIN, AGENT - 2, ((("Still on chats", TEXT),), (("and spreadsheets?", GOLD),))),
    (ONE, OFFER - 2, ((("One system.", TEXT),), (("AI built in.", GOLD),))),
]
STEPS = [
    (AGENT, ACCOUNT, "1", "AI agent", "Tell it what you need, in plain words."),
    (ACCOUNT, OFFLINE, "2", "Accounting assistant", "Answers from your own reports."),
    (OFFLINE, ONE, "3", "Offline POS", "The till keeps selling."),
]
STEP_LABELS = ["AI AGENT", "ACCOUNTING", "OFFLINE POS"]


def typed(text, n, start, cps=1.3):
    return text[:int(max(0, n - start) * cps)]


# ---------------------------------------------------------------- hook
SLAM_ODOO, SLAM_20, SLAM_HERE = 2, 14, 28            # frames where each word starts its reveal (SFX follow)
DEEP_GOLD = (120, 88, 22)


@lru_cache(None)
def tight(text, fkey, size, color):
    sp = text_sprite(text, fkey, size, color)
    return sp.crop(sp.getchannel("A").getbbox())


@lru_cache(None)
def extruded(text, fkey, size, face, depth):
    """Heavy title: a stack of darker copies offset down-right under the face colour (3D extrusion)."""
    top = tight(text, fkey, size, face)
    side = tight(text, fkey, size, DEEP_GOLD)
    im = Image.new("RGBA", (top.width + depth, top.height + depth), (0, 0, 0, 0))
    for k in range(depth, 0, -1):
        im.alpha_composite(side, (k, k))
    im.alpha_composite(top, (0, 0))
    return im


def slam(n, f, dur=8):
    """Scale for a word slamming in at frame f: big -> slight undershoot -> 1."""
    t = lin(n, f, f + dur)
    return 2.2 - 1.2 * back(t, 2.6), ease(lin(n, f, f + 3))


def draw_hook(frame, n):
    """Smooth staggered reveal (no slam / shake / flash): words rise and fade in, gold underline sweeps."""
    if n >= PAIN + 8:
        return
    out = 1 - ease(lin(n, PAIN - 6, PAIN + 8))
    g, pad = K.glow(700, 420, GOLD, 80, 80)
    put(frame, g, W / 2 - 350 - pad, 640 - 210 - pad, "tl", a=ease(lin(n, SLAM_20, SLAM_20 + 24)) * out)
    for txt, sz, col, dep, x, y, f in (("ODOO", 250, TEXT, 10, W / 2, 365, SLAM_ODOO),
                                       ("20", 470, GOLD, 14, W / 2 + 10, 650, SLAM_20),
                                       ("IS HERE", 104, TEXT, 6, W / 2, 905, SLAM_HERE)):
        if n >= f:
            dy, a, sc = K.reveal(n, f)
            put(frame, extruded(txt, "P9I", sz, col, dep), x, y + dy, "cc", a=a * out, s=sc, text=True)
    K.underline(frame, n, SLAM_HERE + 10, 975, 520, out)
    put(frame, K.label_chip("RELEASED SEPTEMBER 2026"), W / 2, 1010, "tc", a=ease(lin(n, 46, 56)) * out, text=True)


# ---------------------------------------------------------------- pain recap
@lru_cache(None)
def mini_chat():
    w, h = 420, 330
    im = rrect(w, h, 26, (20, 20, 23, 255), (70, 70, 78, 255), 2).copy()
    im.alpha_composite(text_sprite("Shop Team", "C7", 26, TEXT), (24, 18))
    for i, (who, msg, y) in enumerate([("Ali", "Any update??", 70), ("Ravi", "Not me", 150),
                                       ("Sara", "New order: Khalid, 12 cases", 230)]):
        b = rrect(min(370, 60 + len(msg) * 14), 66, 16, (32, 32, 37, 255),
                  GOLD + (255,) if i == 2 else None, 2 if i == 2 else 0).copy()
        b.alpha_composite(text_sprite(who, "C6", 18, (150, 205, 140)), (14, 6))
        b.alpha_composite(text_sprite(msg, "C5", 22, TEXT), (14, 30))
        im.alpha_composite(b, (20, y))
    return im


@lru_cache(None)
def mini_sheet():
    w, h = 420, 330
    im = rrect(w, h, 20, (236, 236, 232, 255)).copy()
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, 56), 20, fill=(54, 54, 60))
    d.rectangle((0, 36, w - 1, 56), fill=(54, 54, 60))
    im.alpha_composite(text_sprite("Stock_FINAL_v7.xlsx", "M", 22, (230, 230, 230)), (20, 14))
    for r, (name, q) in enumerate([("Phone case", "12"), ("Charger", "8"), ("Cable", "30"), ("Power bank", "6")]):
        y = 80 + r * 60
        d.line((16, y - 8, w - 16, y - 8), fill=(205, 205, 200), width=2)
        im.alpha_composite(text_sprite(name, "C5", 26, (30, 30, 34)), (22, y + 4))
        im.alpha_composite(text_sprite(q, "C7", 28, RED if r == 0 else (30, 30, 34)), (330, y + 2))
    return im


def draw_pain(frame, n):
    if not (PAIN <= n < AGENT + 10):
        return
    out = 1 - ease(lin(n, AGENT - 6, AGENT + 10))
    for k, (sp, x, rot, f) in enumerate([(mini_chat(), 300, -5, PAIN + 6), (mini_sheet(), 780, 5, PAIN + 16)]):
        t = lin(n, f, f + 12)
        im = sp.rotate(rot, resample=Image.BICUBIC, expand=True)
        put(frame, im, x, 690 + 40 * (1 - ease(t)), "cc", a=ease(t * 1.4) * out, s=0.85 + 0.15 * back(t, 1.8))
    # strike-through: "this is what we're replacing"
    st = ease_io(lin(n, AGENT - 26, AGENT - 10))
    if st > 0:
        lay = Image.new("RGBA", (W, 1350), (0, 0, 0, 0))
        ImageDraw.Draw(lay).line((120, 860, 120 + 840 * st, 520), fill=RED + (230,), width=10)
        put(frame, lay, 0, 0, "tl", a=out)


# ---------------------------------------------------------------- 1 AI agent
PROMPT = "Alert me when phone cases drop below 5."
PLAN = ["Watch stock for Phone case, black", "When on hand drops below 5, notify you",
        "Suggest a reorder from your supplier"]


@lru_cache(None)
def spark(d, col=GOLD):
    im = Image.new("RGBA", (d * 3, d * 3), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    c = d * 1.5
    r1, r2 = d * 1.45, d * 0.32
    pts = []
    for i in range(8):
        a = math.pi / 4 * i - math.pi / 2
        r = r1 if i % 2 == 0 else r2
        pts.append((c + r * math.cos(a), c + r * math.sin(a)))
    dr.polygon(pts, fill=col)
    return im.resize((d, d), Image.LANCZOS)


def prompt_bubble(text, show_cursor):
    lines = K.wrap(text, "C6", 34, 820) or [""]
    w = int(max(K.F("C6", 34).getlength(l) for l in lines)) + 60
    h = 40 + 46 * len(lines)
    im = rrect(max(w, 120), h, 24, (70, 56, 24, 255)).copy()
    for i, l in enumerate(lines):
        im.alpha_composite(text_sprite(l, "C6", 34, TEXT), (30, 18 + 46 * i))
    if show_cursor:
        cx = 30 + K.F("C6", 34).getlength(lines[-1]) + 4
        ImageDraw.Draw(im).rectangle((cx, 26 + 46 * (len(lines) - 1), cx + 3, 58 + 46 * (len(lines) - 1)), fill=GOLD)
    return im


@lru_cache(None)
def plan_card(k_steps, state):
    """state: 'ask' (approve buttons) or 'active'."""
    w, h = 860, 470
    im = rrect(w, h, 26, RAISED + (255,), GOLD + (170,), 2).copy()
    im.alpha_composite(spark(34), (34, 30))
    im.alpha_composite(text_sprite("AI AGENT", "M", 26, GOLD, 3), (82, 32))
    im.alpha_composite(text_sprite("Here's what I'll do:", "C7", 36, TEXT), (34, 84))
    for i in range(k_steps):
        y = 150 + i * 70
        im.alpha_composite(K.circle(44, GOLD + (40,), GOLD + (255,), 2), (34, y))
        num = text_sprite(str(i + 1), "C7", 24, GOLD)
        im.alpha_composite(num, (34 + (44 - num.width) // 2 + 1, y + 7))
        im.alpha_composite(text_sprite(PLAN[i], "C5", 32, TEXT), (96, y + 4))
    if state == "ask":
        btn = rrect(220, 70, 35, GOLD + (255,)).copy()
        ts = text_sprite("Approve", "C7", 32, BG)
        btn.alpha_composite(ts, ((220 - ts.width) // 2, (70 - ts.height) // 2 + 2))
        im.alpha_composite(btn, (34, 372))
        ghost = rrect(160, 70, 35, (0, 0, 0, 0), (255, 255, 255, 80), 2).copy()
        ts = text_sprite("Edit", "C6", 30, TEXT2)
        ghost.alpha_composite(ts, ((160 - ts.width) // 2, (70 - ts.height) // 2 + 2))
        im.alpha_composite(ghost, (274, 372))
    elif state == "active":
        im.alpha_composite(K.pill("ACTIVE  ·  RUNS AUTOMATICALLY", GREEN, 26), (34, 378))
    return im


def draw_agent(frame, n):
    if not (AGENT + 6 <= n < ACCOUNT + 8):
        return
    out = 1 - ease(lin(n, ACCOUNT - 6, ACCOUNT + 8))
    t = lin(n, AGENT + 6, AGENT + 16)
    txt = typed(PROMPT, n, PROMPT_TYPE)
    done = len(txt) == len(PROMPT)
    pb = prompt_bubble(txt, not done and (n // 6) % 2 == 0)
    put(frame, pb, K.SAFE_X1 - 10, 400, "tr", a=ease(t * 1.4) * out)
    if n >= PLAN_IN:
        k = sum(n >= f for f in PLAN_STEPS)
        state = "active" if n >= APPROVE + 3 else ("ask" if n >= PLAN_STEPS[-1] + 6 else "none")
        tp = lin(n, PLAN_IN, PLAN_IN + 12)
        press = 1 - 0.04 * math.sin(math.pi * lin(n, APPROVE - 4, APPROVE + 4))
        put(frame, plan_card(k, state), W / 2, 450 + pb.height, "tc", a=ease(tp * 1.4) * out,
            s=(0.9 + 0.1 * back(tp, 1.8)) * press)


# ---------------------------------------------------------------- 2 accounting assistant
QUESTION = "How much do customers owe me?"
ROWS = [("Falcon Bay Trading", "AED 12,400", "45 days"), ("Bluewave Cafe", "AED 8,900", "32 days"),
        ("Sunrise Mobiles", "AED 6,150", "18 days")]


@lru_cache(None)
def answer_card(k_rows):
    w, h = 860, 560
    im = rrect(w, h, 26, RAISED + (255,), GOLD + (170,), 2).copy()
    im.alpha_composite(spark(34), (34, 30))
    im.alpha_composite(text_sprite("ACCOUNTING AGENT", "M", 26, GOLD, 3), (82, 32))
    im.alpha_composite(text_sprite("Customers owe you", "C6", 32, TEXT2), (34, 88))
    im.alpha_composite(text_sprite("AED 48,250", "P8", 92, TEXT), (30, 122))
    im.alpha_composite(text_sprite("across 23 open invoices", "C5", 30, TEXT2), (34, 240))
    d = ImageDraw.Draw(im)
    d.line((34, 296, w - 34, 296), fill=(255, 255, 255, 22), width=2)
    im.alpha_composite(text_sprite("LARGEST BALANCES", "M", 22, MUTED, 2), (34, 312))
    for i in range(k_rows):
        name, amt, age = ROWS[i]
        y = 352 + i * 54
        im.alpha_composite(text_sprite(name, "C6", 30, TEXT), (34, y))
        a = text_sprite(amt, "C7", 30, GOLD)
        im.alpha_composite(a, (560 - a.width, y))
        g = text_sprite(age, "M", 24, RED if i == 0 else TEXT2, 1)
        im.alpha_composite(g, (w - 34 - g.width, y + 4))
    im.alpha_composite(text_sprite("Source: Aged Receivable report", "M", 20, MUTED, 1), (34, h - 40))
    return im


def draw_account(frame, n):
    if not (ACCOUNT + 6 <= n < OFFLINE + 8):
        return
    out = 1 - ease(lin(n, OFFLINE - 6, OFFLINE + 8))
    t = lin(n, ACCOUNT + 6, ACCOUNT + 16)
    txt = typed(QUESTION, n, Q_TYPE)
    pb = prompt_bubble(txt, len(txt) < len(QUESTION) and (n // 6) % 2 == 0)
    put(frame, pb, K.SAFE_X1 - 10, 400, "tr", a=ease(t * 1.4) * out)
    if n >= ANSWER_IN:
        k = sum(n >= f for f in ANSWER_ROWS)
        ta = lin(n, ANSWER_IN, ANSWER_IN + 12)
        put(frame, answer_card(k), W / 2, 520, "tc", a=ease(ta * 1.4) * out, s=0.9 + 0.1 * back(ta, 1.8))


# ---------------------------------------------------------------- 3 offline POS
@lru_cache(None)
def wifi(d, col, crossed):
    ss = 3
    im = Image.new("RGBA", (d * ss, d * ss), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    c = d * ss / 2
    for i, r in enumerate((0.45, 0.32, 0.19)):
        rr = r * d * ss
        dr.arc((c - rr, c - rr + d * 0.25 * ss, c + rr, c + rr + d * 0.25 * ss), 225, 315, fill=col, width=int(0.07 * d * ss))
    dr.ellipse((c - 0.06 * d * ss, c + 0.2 * d * ss, c + 0.06 * d * ss, c + 0.32 * d * ss), fill=col)
    if crossed:
        dr.line((0.15 * d * ss, 0.15 * d * ss, 0.85 * d * ss, 0.85 * d * ss), fill=RED, width=int(0.08 * d * ss))
    return im.resize((d, d), Image.LANCZOS)


@lru_cache(None)
def pos_status(state):
    w, h = 860, 90
    col = {"online": GREEN, "offline": RED, "synced": GREEN}[state]
    label = {"online": "ONLINE", "offline": "OFFLINE  ·  STILL SELLING",
             "synced": "BACK ONLINE  ·  3 ORDERS SYNCED"}[state]
    im = rrect(w, h, 20, col + (34,), col + (200,), 2).copy()
    im.alpha_composite(wifi(54, col, state == "offline"), (24, 18))
    im.alpha_composite(text_sprite(label, "M", 30, col, 2), (96, 26))
    return im


@lru_cache(None)
def pos_order(num, items, synced):
    w, h = 860, 104
    im = rrect(w, h, 18, SURFACE + (255,), (255, 255, 255, 26), 2).copy()
    im.alpha_composite(text_sprite(f"Order #{num}", "C7", 34, TEXT), (30, 16))
    im.alpha_composite(text_sprite(items, "C5", 26, TEXT2), (30, 60))
    tag = K.pill("SYNCED" if synced else "SAVED ON DEVICE", GREEN if synced else GOLD, 20)
    im.alpha_composite(tag, (w - 30 - tag.width, (h - tag.height) // 2))
    return im


ORDERS = [("0412", "2 × phone case"), ("0413", "1 × charger 20W"), ("0414", "3 × USB-C cable")]


@lru_cache(None)
def till_header():
    w, h = 860, 120
    im = rrect(w, h, 22, (26, 26, 30, 255), (255, 255, 255, 30), 2).copy()
    im.alpha_composite(text_sprite("POINT OF SALE  ·  KIOSK 2", "M", 26, TEXT2, 2), (30, 24))
    im.alpha_composite(text_sprite("Mall kiosk  ·  2 staff", "C5", 28, MUTED), (30, 66))
    return im


def draw_offline(frame, n):
    if not (OFFLINE + 6 <= n < ONE + 8):
        return
    out = 1 - ease(lin(n, ONE - 6, ONE + 8))
    t = lin(n, OFFLINE + 6, OFFLINE + 18)
    put(frame, till_header(), W / 2, 380, "tc", a=ease(t * 1.4) * out)
    state = "synced" if n >= BACK_ONLINE else ("offline" if n >= GO_OFFLINE else "online")
    flash = 1 + 0.05 * math.sin(math.pi * lin(n, GO_OFFLINE, GO_OFFLINE + 8)) + \
        0.05 * math.sin(math.pi * lin(n, BACK_ONLINE, BACK_ONLINE + 8))
    put(frame, pos_status(state), W / 2, 545, "cc", a=ease(t * 1.4) * out, s=flash)
    for k, f in enumerate(POS_ORDERS):
        if n < f:
            continue
        to = lin(n, f, f + 10)
        put(frame, pos_order(*ORDERS[k], n >= BACK_ONLINE + 4 + 3 * k), W / 2, 620 + k * 122 + 30 * (1 - ease(to)),
            "tc", a=ease(to * 1.5) * out)


# ---------------------------------------------------------------- one system
TILE_LABELS = ["SALES", "STOCK", "ACCOUNTING", "TEAM"]


@lru_cache(None)
def sys_tile(label):
    w, h = 380, 200
    im = rrect(w, h, 22, SURFACE + (255,), (255, 255, 255, 34), 2).copy()
    ts = text_sprite(label, "M", 34, TEXT, 3)
    im.alpha_composite(ts, ((w - ts.width) // 2, (h - ts.height) // 2))
    return im


def draw_one(frame, n):
    if not (ONE <= n < OFFER + 6):
        return
    out = 1 - ease(lin(n, OFFER - 6, OFFER + 6))
    m = ease_io(lin(n, MERGE, MERGE + 18))
    gap = 40 - 28 * m
    starts = [(-200, 300), (W + 200, 300), (-200, 1200), (W + 200, 1200)]
    for k, (lab, f) in enumerate(zip(TILE_LABELS, TILES_IN)):
        t = ease_io(lin(n, f, f + 16))
        gx = W / 2 + (-1 if k % 2 == 0 else 1) * (190 + gap / 2)
        gy = 760 + (-1 if k < 2 else 1) * (100 + gap / 2)
        x = starts[k][0] + (gx - starts[k][0]) * t
        y = starts[k][1] + (gy - starts[k][1]) * t
        put(frame, sys_tile(lab), x, y, "cc", a=min(1, t * 2) * out)
    if m > 0:
        fw, fh = int(760 + gap + 60), int(400 + gap + 60)
        put(frame, rrect(fw, fh, 30, (0, 0, 0, 0), GOLD + (255,), 4), W / 2, 760, "cc", a=m * out)
        put(frame, K.pill("ODOO 20", GOLD, 30), W / 2, 760 - fh / 2, "cc", a=m * out, text=True)
        put(frame, spark(56), W / 2 + fw / 2 - 10, 760 - fh / 2 + 10, "cc", a=m * out, s=0.8 + 0.2 * back(m, 2.0))


# ---------------------------------------------------------------- end card badge
@lru_cache(None)
def partner_badge():
    """Official Odoo Ready Partner artwork from the TOLX theme, unchanged (proportional resize only),
    on a white card so its grey lettering stays legible on the dark background."""
    art = Image.open(os.path.join(HERE, "assets", "odoo_ready_partners_rgb.png")).convert("RGBA")
    art = art.crop(art.getbbox())
    w = 250
    art = art.resize((w, int(art.height * w / art.width)), Image.LANCZOS)
    card = rrect(w + 56, art.height + 40, 20, (255, 255, 255, 255)).copy()
    card.alpha_composite(art, (28, 20))
    return card


def draw_badge(frame, n):
    if n < END_CARD + 50:
        return
    t = lin(n, END_CARD + 50, END_CARD + 62)
    put(frame, partner_badge(), W / 2, 1150, "cc", a=ease(t * 1.4), s=0.9 + 0.1 * back(t, 1.8))


# ---------------------------------------------------------------- frames
OFFER_LINES = ((("Odoo 20, set up", TEXT),), (("around your business.", GOLD),))


def render(n):
    frame = K.background(n)
    draw_hook(frame, n)
    draw_pain(frame, n)
    draw_agent(frame, n)
    draw_account(frame, n)
    draw_offline(frame, n)
    draw_one(frame, n)
    K.draw_headlines(frame, n, HEADLINES)
    K.draw_steps(frame, n, STEPS, STEP_LABELS)
    K.draw_statement(frame, n, OFFER, OFFER_LINES, OFFER_BEATS)
    K.draw_end_card(frame, n)
    draw_badge(frame, n)
    K.draw_chrome(frame, n, AGENT + 8)
    return frame.convert("RGB")


CAPTIONS = [
    (4, PAIN, "Odoo 20 is here! Released September 2026."),
    (PAIN, AGENT, "Still on chats and spreadsheets?"),
    (AGENT, ACCOUNT, "1. AI agent: tell it what you need, in plain words. It shows the plan before it runs."),
    (ACCOUNT, OFFLINE, "2. Accounting assistant: answers from your own reports."),
    (OFFLINE, ONE, "3. Offline POS: the till keeps selling, then syncs."),
    (ONE, OFFER, "One system: sales, stock, accounting, team. AI built in."),
    (OFFER, END_CARD, "Odoo 20, set up around your business, or custom software built around exactly how you work."),
    (END_CARD, TOTAL, f"Book a {K.CALL_LENGTH} discovery call: {K.CTA_URL} or WhatsApp {K.PHONE}"),
]
PICKS = [(60, "Hook"), (170, "Pain"), (300, "Agent plan"), (370, "Agent active"), (480, "Accounting"),
         (600, "Offline"), (670, "Synced"), (760, "One system"), (840, "Offer"), (980, "End card")]

if __name__ == "__main__":
    K.run(ARGS, render, CAPTIONS, PICKS, cover_frame=60)
