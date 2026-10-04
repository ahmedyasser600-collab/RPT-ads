"""Compose TOLX video 04 "UAE e-invoicing is coming" (34 s), series style from video 03.

Facts (checked 4 Oct 2026): UAE Ministry of Finance Ministerial Decisions No. 243 and 244 of 2025,
as amended by Ministerial Decision No. 66 of 2026:
  pilot 1 Jul 2026; revenue >= AED 50M: appoint an Accredited Service Provider by 30 Oct 2026, go live
  1 Jan 2027; revenue < AED 50M: appoint an ASP by 31 Mar 2027, go live 1 Jul 2027. B2B and B2G
  invoices move to structured e-invoices (PINT AE) exchanged through accredited service providers,
  with data reported to the Federal Tax Authority.
The flow diagram is simplified and labelled so. The video makes no claim that TOLX is an accredited
service provider or that any specific Odoo version has a certified UAE e-invoicing connector; the
offer is to get sales, VAT and invoicing into one system and ready to connect. Not tax advice.
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
K.FOOTNOTE = "Dates: UAE Ministerial Decisions 243 & 244/2025, amended. Not tax advice."

HEADLINES = [
    (DEADLINES, FORMAT - 2, ((("The ", TEXT), ("deadlines.", GOLD)),)),
    (FORMAT, EXCEL - 2, ((("No more", TEXT),), (("PDF invoices.", GOLD),))),
    (EXCEL, READY - 2, ((("Invoicing from", TEXT),), (("Excel or Word?", GOLD),))),
    (READY, OFFER - 2, ((("Get ready", TEXT),), (("before the deadline.", GOLD),))),
]


# ---------------------------------------------------------------- hook
def draw_hook(frame, n):
    if n >= DEADLINES + 8:
        return
    out = 1 - ease(lin(n, DEADLINES - 6, DEADLINES + 8))
    dx, dy = K.shake(n, [(SLAMS[0] + 6, 6), (SLAMS[1] + 6, 8), (SLAMS[2] + 6, 16), (SLAMS[3] + 4, 6)])
    g, pad = K.glow(760, 260, GOLD, 80, 95)
    put(frame, g, W / 2 - 380 - pad + dx, 640 - 130 - pad + dy, "tl",
        a=ease(lin(n, SLAMS[2], SLAMS[2] + 10)) * out * (0.75 + 0.25 * math.sin(n / 7) ** 2))
    items = [("UAE", "P9I", 120, TEXT, 8, 300), ("E-INVOICING", "P9I", 126, TEXT, 10, 445),
             ("JULY 2027", "P9I", 164, GOLD, 16, 640), ("IS YOUR BUSINESS READY?", "P9I", 62, TEXT, 6, 815)]
    for (txt, fk, sz, col, dep, y), f in zip(items, SLAMS):
        if n >= f:
            s, a = K.slam(n, f, 7 if f == SLAMS[3] else 8)
            put(frame, K.extruded(txt, fk, sz, col, dep), W / 2 + dx, y + dy, "cc", a=a * out, s=s, text=True)
    put(frame, K.label_chip("FOR BUSINESS-TO-BUSINESS INVOICES"), W / 2, 920, "tc",
        a=ease(lin(n, SLAMS[3] + 12, SLAMS[3] + 22)) * out, text=True)
    K.flash(frame, n, SLAMS[2] + 5)


# ---------------------------------------------------------------- deadlines
MILESTONES = [("1 JUL 2026", "Pilot programme", "Selected businesses"),
              ("1 JAN 2027", "Go live: revenue AED 50M+", "Provider appointed by 30 Oct 2026"),
              ("31 MAR 2027", "Appoint an accredited provider", "Revenue under AED 50M"),
              ("1 JUL 2027", "Go live: revenue under AED 50M", "Most SMEs")]
MS_Y = [400, 590, 780, 970]
LINE_X = 170


@lru_cache(None)
def milestone_card(i, hot):
    date, title, sub = MILESTONES[i]
    w, h = 740, 158
    im = rrect(w, h, 22, (40, 33, 16, 255) if hot else SURFACE + (255,),
               GOLD + (255,) if hot else (255, 255, 255, 28), 3 if hot else 2).copy()
    im.alpha_composite(text_sprite(date, "M", 30, GOLD if hot else TEXT2, 3), (30, 22))
    im.alpha_composite(text_sprite(title, "C7", 36, TEXT if hot else (200, 200, 206)), (30, 64))
    im.alpha_composite(text_sprite(sub, "C5", 26, TEXT2 if hot else MUTED), (30, 110))
    return im


def draw_deadlines(frame, n):
    if not (DEADLINES <= n < FORMAT + 8):
        return
    out = 1 - ease(lin(n, FORMAT - 6, FORMAT + 8))
    grow = ease_io(lin(n, DEADLINES + 4, DEADLINES + 40))
    if grow > 0:
        put(frame, rrect(6, max(6, int((MS_Y[-1] + 79 - MS_Y[0]) * grow)), 3, (70, 70, 78)), LINE_X - 3,
            MS_Y[0] + 79, "tl", a=out)
    for i, f in enumerate(MILESTONES_IN):
        if n < f:
            continue
        t = lin(n, f, f + 12)
        hot = (i == 3 and n >= HL_JULY) or (i == 2 and n >= HL_MARCH)
        y = MS_Y[i]
        pulse = 1 + (0.15 * math.sin(n / 3) ** 2 if hot else 0)
        put(frame, K.circle(40, (GOLD if hot else (90, 90, 98)) + (255,)), LINE_X, y + 79, "cc", a=ease(t * 1.4) * out,
            s=pulse)
        dim = 0.55 if (n >= HL_JULY and not hot) else 1.0
        put(frame, milestone_card(i, hot), 230, y + 40 * (1 - ease(t)), "tl", a=ease(t * 1.4) * out * dim)


# ---------------------------------------------------------------- format: PDF -> structured -> ASP
CX = W / 2


@lru_cache(None)
def pdf_card():
    w, h = 300, 220
    im = rrect(w, h, 16, (236, 236, 232, 255)).copy()
    d = ImageDraw.Draw(im)
    for k in range(5):
        d.line((30, 70 + 26 * k, w - 30 - (60 if k == 4 else 0), 70 + 26 * k), fill=(190, 190, 186), width=8)
    im.alpha_composite(K.pill("PDF", RED, 26), (24, 16))
    return im


@lru_cache(None)
def data_card(k_rows):
    w, h = 620, 250
    im = rrect(w, h, 20, RAISED + (255,), GOLD + (220,), 3).copy()
    im.alpha_composite(text_sprite("E-INVOICE  ·  STRUCTURED DATA", "M", 24, GOLD, 2), (28, 22))
    rows = [("<SellerTRN>", "100xxxxxxxxxx03"), ("<TaxRate>", "5%"), ("<Total>", "AED 1,575.00")]
    for i in range(k_rows):
        a, b = rows[i]
        y = 76 + i * 52
        im.alpha_composite(text_sprite(a, "M", 28, (150, 205, 140)), (28, y))
        im.alpha_composite(text_sprite(b, "C6", 30, TEXT), (300, y - 2))
    return im


@lru_cache(None)
def node(label, sub, w=420, gold=False):
    h = 112 if sub else 86
    im = rrect(w, h, 20, (40, 33, 16, 255) if gold else SURFACE + (255,), GOLD + (255,) if gold else (255, 255, 255, 40), 2).copy()
    ts = text_sprite(label, "M", 26, GOLD if gold else TEXT, 2)
    im.alpha_composite(ts, ((w - ts.width) // 2, 20))
    if sub:
        t2 = text_sprite(sub, "C5", 24, TEXT2)
        im.alpha_composite(t2, ((w - t2.width) // 2, 62))
    return im


def arrow(frame, x0, y0, x1, y1, a, prog=1.0):
    if prog <= 0 or a <= 0:
        return
    lay = Image.new("RGBA", (W, 1350), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    xe, ye = x0 + (x1 - x0) * prog, y0 + (y1 - y0) * prog
    d.line((x0, y0, xe, ye), fill=GOLD + (int(220 * a),), width=5)
    if prog >= 0.98:
        ang = math.atan2(y1 - y0, x1 - x0)
        for s_ in (-1, 1):
            d.line((x1, y1, x1 - 22 * math.cos(ang + s_ * 0.5), y1 - 22 * math.sin(ang + s_ * 0.5)),
                   fill=GOLD + (int(220 * a),), width=5)
    put(frame, lay, 0, 0, "tl")


def draw_format(frame, n):
    if not (FORMAT <= n < EXCEL + 8):
        return
    out = 1 - ease(lin(n, EXCEL - 6, EXCEL + 8))
    # PDF appears, gets crossed, morphs into structured data
    if n < MORPH + 10:
        t = lin(n, PDF_IN, PDF_IN + 10)
        a = ease(t * 1.4) * (1 - ease(lin(n, MORPH, MORPH + 10))) * out
        put(frame, pdf_card(), CX, 520, "cc", a=a, s=0.85 + 0.15 * back(t, 1.8))
        x = ease_io(lin(n, PDF_X, PDF_X + 8))
        if x > 0:
            lay = Image.new("RGBA", (W, 1350), (0, 0, 0, 0))
            d = ImageDraw.Draw(lay)
            d.line((CX - 140, 420, CX - 140 + 280 * x, 420 + 200 * x), fill=RED + (240,), width=12)
            d.line((CX + 140, 420, CX + 140 - 280 * x, 420 + 200 * x), fill=RED + (240,), width=12)
            put(frame, lay, 0, 0, "tl", a=a)
    if n >= MORPH:
        t = lin(n, MORPH, MORPH + 12)
        k = sum(n >= f for f in DATA_ROWS)
        put(frame, data_card(k), CX, 520, "cc", a=ease(t * 1.4) * out, s=0.8 + 0.2 * back(t, 1.8))
        put(frame, K.pill("PINT AE  ·  XML", GOLD, 22), CX, 668, "cc", a=ease(lin(n, DATA_ROWS[-1], DATA_ROWS[-1] + 8)) * out,
            text=True)
    if n >= ASP_IN:
        t = lin(n, ASP_IN, ASP_IN + 12)
        arrow(frame, CX, 700, CX, 760, out, ease_io(t))
        put(frame, node("YOUR ACCREDITED PROVIDER", "Accredited Service Provider (ASP)", 560, True), CX, 822, "cc",
            a=ease(t * 1.4) * out, text=True)
    if n >= SPLIT_IN:
        t = lin(n, SPLIT_IN, SPLIT_IN + 12)
        arrow(frame, CX - 60, 880, 300, 960, out, ease_io(t))
        arrow(frame, CX + 60, 880, 780, 960, out, ease_io(t))
        put(frame, node("BUYER", "via their provider", 360), 300, 1020, "cc", a=ease(t * 1.4) * out, text=True)
        put(frame, node("FTA", "Federal Tax Authority", 360), 780, 1020, "cc", a=ease(t * 1.4) * out, text=True)
        put_text(frame, "SIMPLIFIED", "M", 20, MUTED, CX, 1100, "tc", a=ease(t) * out, track=2)
    if PACKET <= n < PACKET + 40:
        for k, (x0, x1, y1) in enumerate(((CX - 60, 300, 960), (CX + 60, 780, 960))):
            p = ease_io(lin(n, PACKET + 6 * k, PACKET + 6 * k + 20))
            if 0 < p < 1:                                    # from under the provider box to buyer / FTA
                x, y = x0 + (x1 - x0) * p, 880 + (y1 - 880) * p
                put(frame, K.circle(22, GOLD + (255,)), x, y, "cc", a=out)


# ---------------------------------------------------------------- Excel / Word
@lru_cache(None)
def doc_card(name, kind):
    w, h = 400, 300
    col = (60, 110, 200) if kind == "W" else (40, 140, 80)
    im = rrect(w, h, 20, (236, 236, 232, 255)).copy()
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, 70), 20, fill=col)
    d.rectangle((0, 50, w - 1, 70), fill=col)
    im.alpha_composite(text_sprite(name, "M", 22, (245, 245, 245)), (20, 22))
    for k in range(6):
        d.line((26, 100 + 30 * k, w - 26 - (90 if k % 3 == 2 else 0), 100 + 30 * k), fill=(190, 190, 186), width=8)
    return im


@lru_cache(None)
def stamp():
    ts = K.tight("NOT  E-INVOICE  READY", "P9I", 62, RED)
    w, h = ts.width + 90, 150                                  # box sized to the text
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((4, 4, w - 5, h - 5), 18, fill=(28, 10, 10, 235), outline=RED + (255,), width=8)
    im.alpha_composite(ts, ((w - ts.width) // 2, (h - ts.height) // 2))
    return im.rotate(-6, resample=Image.BICUBIC, expand=True)


def draw_excel(frame, n):
    if not (EXCEL <= n < READY + 8):
        return
    out = 1 - ease(lin(n, READY - 6, READY + 8))
    dx, dy = K.shake(n, [(STAMP + 5, 12)])
    for k, (name, kind, x, rot, f) in enumerate([("Invoice_final_v2.docx", "W", 320, -6, DOCS_IN[0]),
                                                 ("Invoices_2027.xlsx", "X", 760, 5, DOCS_IN[1])]):
        t = lin(n, f, f + 12)
        sp = doc_card(name, kind).rotate(rot, resample=Image.BICUBIC, expand=True)
        put(frame, sp, x + dx, 680 + dy + 40 * (1 - ease(t)), "cc", a=ease(t * 1.4) * out, s=0.85 + 0.15 * back(t, 1.8))
    if n >= STAMP:
        s, a = K.slam(n, STAMP, 7)
        put(frame, stamp(), W / 2 + dx, 690 + dy, "cc", a=a * out, s=s, text=True)


# ---------------------------------------------------------------- readiness checklist
CHECK_ITEMS = ["Customer TRNs on every record", "VAT calculated on every line", "All invoices from one system",
               "Ready to connect to your provider"]


@lru_cache(None)
def check_row(text, done):
    w, h = 860, 120
    im = rrect(w, h, 20, (24, 38, 28, 255) if done else SURFACE + (255,),
               GREEN + (200,) if done else (255, 255, 255, 30), 2).copy()
    box = K.circle(62, GREEN + (255,)) if done else K.circle(62, (0, 0, 0, 0), (110, 110, 118, 255), 3)
    im.alpha_composite(box, (30, 29))
    if done:
        d = ImageDraw.Draw(im)
        d.line((46, 61, 58, 74), fill=BG, width=8)
        d.line((57, 74, 78, 47), fill=BG, width=8)
    im.alpha_composite(text_sprite(text, "C6", 34, TEXT if done else TEXT2), (120, 36))
    return im


def draw_ready(frame, n):
    if not (READY <= n < OFFER + 6):
        return
    out = 1 - ease(lin(n, OFFER - 6, OFFER + 6))
    for k, (txt, f) in enumerate(zip(CHECK_ITEMS, CHECKS)):
        t = lin(n, READY + 6 + 5 * k, READY + 18 + 5 * k)
        pop = 1 + 0.06 * math.sin(math.pi * lin(n, f, f + 8))
        put(frame, check_row(txt, n >= f), W / 2, 420 + k * 150, "tc", a=ease(t * 1.4) * out, s=pop)


# ---------------------------------------------------------------- end card badge (same as video 03)
@lru_cache(None)
def partner_badge():
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
OFFER_LINES = ((("Get e-invoice ready", TEXT),), (("with TOLX.", GOLD),))


def render(n):
    frame = K.background(n)
    draw_hook(frame, n)
    draw_deadlines(frame, n)
    draw_format(frame, n)
    draw_excel(frame, n)
    draw_ready(frame, n)
    K.draw_headlines(frame, n, HEADLINES)
    K.draw_statement(frame, n, OFFER, OFFER_LINES, OFFER_BEATS)
    K.draw_end_card(frame, n)
    draw_badge(frame, n)
    K.draw_chrome(frame, n, FORMAT + 8)
    return frame.convert("RGB")


CAPTIONS = [
    (4, DEADLINES, "UAE e-invoicing: July 2027. Is your business ready?"),
    (DEADLINES, FORMAT, "The deadlines: pilot 1 Jul 2026; revenue AED 50M+ live 1 Jan 2027; under AED 50M appoint "
                        "an accredited provider by 31 Mar 2027 and go live 1 Jul 2027."),
    (FORMAT, EXCEL, "No more PDF invoices: structured e-invoices go through your accredited provider to the buyer and "
                    "the FTA (simplified)."),
    (EXCEL, READY, "Invoicing from Excel or Word? Not e-invoice ready."),
    (READY, OFFER, "Get ready before the deadline: customer TRNs, VAT on every line, all invoices from one system, "
                   "ready to connect to your provider."),
    (OFFER, END_CARD, "Get e-invoice ready with TOLX: Odoo, or custom software built around exactly how you work."),
    (END_CARD, TOTAL, f"Book a {K.CALL_LENGTH} discovery call: {K.CTA_URL} or WhatsApp {K.PHONE}"),
]
PICKS = [(70, "Hook"), (200, "Deadlines: July"), (300, "Deadlines: March"), (420, "Structured data"),
         (500, "Provider flow"), (590, "Not ready"), (790, "Checklist"), (850, "Offer"), (1000, "End card")]

if __name__ == "__main__":
    K.run(ARGS, render, CAPTIONS, PICKS, cover_frame=75)
