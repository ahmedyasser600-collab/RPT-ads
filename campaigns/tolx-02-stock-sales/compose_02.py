"""Compose TOLX video 02 "When Excel stops working" (stock & sales), 34 s.

Motion graphics only. The spreadsheet, files, product record, devices, alert and dashboard are an
ILLUSTRATIVE workflow (labelled on screen). Products, numbers and names are invented; no client,
no prices, no savings claims. The generic features shown (stock updated at sale, one shared stock
figure, minimum-stock flag with a draft purchase order, a daily summary) are standard in inventory
software such as Odoo; the video does not claim any specific integration or hardware.
Shared brand/layout/audio code: ../tolx-kit. Frame n is shown at n/30 s.

Usage: see README.md
"""
import math
import os
import sys
from functools import lru_cache

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "tolx-kit"))
import tolx_kit as K  # noqa: E402
from tolx_kit import (BG, BLUE, GOLD, GREEN, MUTED, RAISED, RED, SURFACE, SURFACE2, TEXT, TEXT2, W,  # noqa: E402
                      back, ease, ease_io, lin, put, put_text, rrect, text_sprite)
from PIL import Image, ImageDraw  # noqa: E402

from timeline import *  # noqa: E402,F401,F403

ARGS = K.parse_args(__doc__)
K.setup(ARGS.format, END_CARD, TOTAL)

ITEM = "Phone case, black"

HEADLINES = [
    (6, SHELF - 4, ((("Your spreadsheet", TEXT),), (("says ", TEXT), ("12.", GOLD)))),
    (SHELF - 4, FILES - 2, ((("The shelf", TEXT),), (("says ", TEXT), ("3.", (235, 100, 90))))),
    (FILES - 2, QUESTIONS - 2, ((("Which file", TEXT),), (("is right?", GOLD),))),
    (QUESTIONS - 2, TURN + 4, ((("Five files.", TEXT),), (("Five numbers.", GOLD),))),
    (TURN + 4, STEP_SELL - 2, ((("One system.", TEXT),), (("One number.", GOLD),))),
]
STEPS = [
    (STEP_SELL, STEP_SYNC, "1", "Sell", "Stock updates the moment you sell."),
    (STEP_SYNC, STEP_REORDER, "2", "Same number", "Shop, warehouse and owner see it."),
    (STEP_REORDER, STEP_SEE, "3", "Reorder in time", "Low stock is flagged early."),
    (STEP_SEE, STATEMENT, "4", "See the day", "Sales and stock at a glance."),
]
STEP_LABELS = ["SELL", "SYNC", "REORDER", "SEE IT"]


# ---------------------------------------------------------------- spreadsheet (hook)
SX, SY, SW, SHT = 110, 380, 860, 500
ROWS = [(ITEM, "12"), ("Charger 20W", "8"), ("USB-C cable", "30"), ("Screen guard", "45"), ("Power bank", "6")]


@lru_cache(None)
def sheet_img():
    im = rrect(SW, SHT, 20, (236, 236, 232, 255)).copy()
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, SW - 1, 64), 20, fill=(54, 54, 60))
    d.rectangle((0, 40, SW - 1, 64), fill=(54, 54, 60))
    im.alpha_composite(text_sprite("Stock_FINAL_v7.xlsx", "M", 28, (230, 230, 230), 1), (28, 16))
    cols = [(28, "ITEM"), (520, "IN STOCK"), (700, "NOTES")]
    for x, lab in cols:
        im.alpha_composite(text_sprite(lab, "M", 22, (110, 110, 118), 2), (x, 86))
    for r, (name, qty) in enumerate(ROWS):
        y = 132 + r * 70
        d.line((20, y - 8, SW - 20, y - 8), fill=(205, 205, 200), width=2)
        im.alpha_composite(text_sprite(name, "C5", 32, (30, 30, 34)), (28, y + 6))
        im.alpha_composite(text_sprite(qty, "C7", 34, (30, 30, 34)), (540, y + 4))
    im.alpha_composite(text_sprite("ask Ali?", "C4", 26, (120, 120, 126)), (700, 140))
    for x in (500, 680):
        d.line((x, 76, x, SHT - 20), fill=(205, 205, 200), width=2)
    return im


def draw_sheet(frame, n):
    if n >= QUESTIONS + 10:
        return
    t_in = back(lin(n, 0, 14), 1.3)
    a = 1 - ease(lin(n, FILES, FILES + 10))
    s = (0.9 + 0.1 * t_in) * (1 - 0.06 * ease(lin(n, FILES, FILES + 10)))
    dy = -40 * ease_io(lin(n, SHELF, SHELF + 14))           # nudge up to make room for the shelf
    put(frame, sheet_img(), W / 2, SY + SHT / 2 + dy, "cc", a=a * min(1, t_in + 0.001), s=s)
    # highlighted "12" cell; turns red when the shelf disagrees
    cell_x, cell_y = SX + 520, SY + 132 + dy
    if 20 <= n < FILES + 10:
        red = ease(lin(n, SHELF + 6, SHELF + 14))
        col = K.mix(GOLD, RED, red)
        pulse = 0.6 + 0.4 * math.sin(n / 4) ** 2
        put(frame, rrect(130, 62, 10, col + (40,), col + (255,), 4), cell_x - 10, cell_y - 4, "tl",
            a=a * pulse * ease(lin(n, 20, 30)))


@lru_cache(None)
def shelf_img():
    w, h = 640, 250
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, h - 34, w, h - 10), 8, fill=(92, 72, 50))
    d.rectangle((24, h - 10, 44, h), fill=(70, 54, 38))
    d.rectangle((w - 44, h - 10, w - 24, h), fill=(70, 54, 38))
    for i in range(3):
        x = 70 + i * 130
        box = rrect(112, 150, 10, (30, 30, 34, 255), (90, 90, 98, 255), 2).copy()
        bd = ImageDraw.Draw(box)
        bd.rounded_rectangle((26, 26, 86, 124), 14, outline=(150, 150, 160), width=4)
        im.alpha_composite(box, (x, h - 34 - 150))
    return im


def draw_shelf(frame, n):
    if not (SHELF <= n < FILES + 10):
        return
    t = lin(n, SHELF, SHELF + 12)
    a = ease(t * 1.4) * (1 - ease(lin(n, FILES, FILES + 10)))
    put(frame, shelf_img(), 420, 1070 + 30 * (1 - ease(t)), "cc", a=a)
    put(frame, count_badge("3", RED), 830, 1050, "cc", a=a, s=0.6 + 0.4 * back(lin(n, SHELF + 6, SHELF + 16), 2.4))
    put_text(frame, "ON THE SHELF", "M", 22, TEXT2, 830, 1120, "tc", a=a, track=2)


@lru_cache(None)
def count_badge(num, col):
    im = K.circle(120, col + (255,)).copy()
    ts = text_sprite(num, "P8", 64, BG)
    im.alpha_composite(ts, ((120 - ts.width) // 2 + 1, (120 - ts.height) // 2 + 4))
    return im


# ---------------------------------------------------------------- file versions
FILES_LIST = [("Stock_FINAL.xlsx", "12"), ("Stock_FINAL_v2.xlsx", "9"), ("Stock_Sara_edit.xlsx", "7"),
              ("Stock_warehouse.xlsx", "10"), ("Stock_FINAL_FINAL.xlsx", "3")]


@lru_cache(None)
def file_card(name, qty):
    w, h = 640, 112
    im = rrect(w, h, 18, (32, 32, 37, 255), (70, 70, 78, 255), 2).copy()
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((22, 22, 82, 90), 8, fill=(220, 220, 214))
    d.polygon([(66, 22), (82, 38), (66, 38)], fill=(170, 170, 164))
    for k in range(3):
        d.line((32, 52 + 11 * k, 72, 52 + 11 * k), fill=(150, 150, 146), width=3)
    im.alpha_composite(text_sprite(name, "C6", 30, TEXT), (104, 18))
    im.alpha_composite(text_sprite(ITEM, "C4", 24, MUTED), (104, 62))
    q = text_sprite(qty, "P8", 54, GOLD)
    im.alpha_composite(q, (w - 30 - q.width, (h - q.height) // 2 + 4))
    return im


def file_pos(i):
    return W / 2 + (-34 if i % 2 else 34), 440 + i * 138


def draw_files(frame, n):
    if not (FILES <= n < TURN + 40):
        return
    dim = 0.5 * min(ease(lin(n, QUESTIONS, QUESTIONS + 10)), 1 - ease(lin(n, TURN - 6, TURN + 4)))
    collapse = ease_io(lin(n, TURN, TURN + 30))
    for i, (f, (name, qty)) in enumerate(zip(FILE_FRAMES, FILES_LIST)):
        if n < f:
            continue
        t = lin(n, f, f + 10)
        x, y = file_pos(i)
        x += (W / 2 - x) * collapse
        y += (640 - y) * collapse
        rot = (4 if i % 2 else -4) * (1 - collapse)
        sp = file_card(name, qty)
        if rot:
            sp = sp.rotate(rot, resample=Image.BICUBIC, expand=True)
        put(frame, sp, x, y + 30 * (1 - ease(t)), "cc", a=ease(t * 1.5) * (1 - dim) * (1 - collapse),
            s=(0.8 + 0.2 * back(t, 1.8)) * (1 - 0.3 * collapse))


def draw_questions(frame, n):
    qs = ["Who updated it last?", "What sold today?", "When do we reorder?"]
    for k, (q, f) in enumerate(zip(qs, QUESTION_FRAMES)):
        if n < f or n >= TURN + 8:
            continue
        t = lin(n, f, f + 10)
        al = min(ease(t * 1.5), 1 - ease(lin(n, TURN - 4, TURN + 8)))
        put(frame, K.q_chip(q), W / 2 + (-50 if k % 2 == 0 else 50), 560 + k * 160, "cc", a=al,
            s=0.6 + 0.4 * back(t, 2.2))


# ---------------------------------------------------------------- product record
PC_W, PC_H = 760, 420


def stock_value(n):
    """On-hand quantity in the system: 6, then 4 after the sale."""
    return 6 if n < COUNT_DOWN + 6 else 4


@lru_cache(None)
def product_card(qty, low):
    im = rrect(PC_W, PC_H, 26, RAISED + (255,), GOLD + (150,), 2).copy()
    im.alpha_composite(text_sprite("PRODUCT  ·  PC-BLK", "M", 24, GOLD, 3), (40, 34))
    im.alpha_composite(text_sprite(ITEM, "C7", 44, TEXT), (40, 72))
    ImageDraw.Draw(im).line((40, 140, PC_W - 40, 140), fill=(255, 255, 255, 22), width=2)
    im.alpha_composite(text_sprite("ON HAND", "M", 24, MUTED, 2), (40, 170))
    col = RED if low else TEXT
    q = text_sprite(qty, "P8", 150, col)
    im.alpha_composite(q, (34, 190))
    im.alpha_composite(text_sprite("MINIMUM", "M", 24, MUTED, 2), (430, 170))
    im.alpha_composite(text_sprite("5", "P7", 64, TEXT2), (430, 204))
    im.alpha_composite(text_sprite("ONE RECORD,", "M", 22, TEXT2, 2), (430, 300))
    im.alpha_composite(text_sprite("ALL LOCATIONS", "M", 22, TEXT2, 2), (430, 330))
    return im


def product_layout(n):
    """(center x, center y, scale) of the product record through steps 1-3."""
    if n < STEP_SYNC + 4:
        return W / 2, 640, 1.0
    t = ease_io(lin(n, STEP_SYNC + 4, STEP_SYNC + 24))
    return W / 2, 640 + (545 - 640) * t, 1.0 - 0.32 * t


def draw_product(frame, n):
    if not (TURN + 14 <= n < STEP_SEE + 10):
        return
    t = lin(n, TURN + 14, TURN + 30)
    out = 1 - ease(lin(n, STEP_SEE - 6, STEP_SEE + 10))
    cx, cy, s = product_layout(n)
    low = n >= ALERT_IN
    put(frame, product_card(str(stock_value(n)), low), cx, cy, "cc", a=ease(t * 1.4) * out,
        s=s * (0.85 + 0.15 * back(t, 1.8)))
    # count-down flash
    if COUNT_DOWN <= n < COUNT_DOWN + 20:
        g, pad = K.glow(220, 170, GOLD, 22, 150)
        put(frame, g, cx - PC_W * s / 2 + 30 - pad, cy - PC_H * s / 2 + 190 - pad, "tl",
            a=math.sin(math.pi * lin(n, COUNT_DOWN, COUNT_DOWN + 20)) * 0.9)


@lru_cache(None)
def sale_ticket():
    w, h = 560, 150
    im = rrect(w, h, 20, (36, 31, 18, 255), GOLD + (255,), 3).copy()
    im.alpha_composite(text_sprite("SALE #2201  ·  SHOP", "M", 24, GOLD, 2), (30, 24))
    im.alpha_composite(text_sprite("2 × " + ITEM, "C6", 36, TEXT), (30, 64))
    im.alpha_composite(K.pill("PAID", GREEN, 20), (w - 120, 22))
    return im


def draw_sale(frame, n):
    if not (SALE_IN <= n < STEP_SYNC + 6):
        return
    t = lin(n, SALE_IN, SALE_IN + 14)
    go = ease_io(lin(n, COUNT_DOWN - 12, COUNT_DOWN + 4))           # ticket flies into the record
    out = 1 - ease(lin(n, COUNT_DOWN - 8, COUNT_DOWN + 1))
    x0 = -300 + (W / 2 - -300) * ease(t)                           # slides in under the record
    x = x0 + (W / 2 - 250 - x0) * go                               # then drops into the ON HAND figure
    y = 1000 + (730 - 1000) * go
    put(frame, sale_ticket(), x, y, "cc", a=min(ease(t * 1.5), out), s=1 - 0.7 * go)
    put_text(frame, "6  ->  4", "M", 34, GOLD, W / 2, 880, "tc",
             a=ease(lin(n, COUNT_DOWN + 4, COUNT_DOWN + 12)) * (1 - ease(lin(n, STEP_SYNC - 8, STEP_SYNC))))


# ---------------------------------------------------------------- sync devices
DEVICES = [("SHOP", 210), ("WAREHOUSE", 540), ("OWNER'S PHONE", 870)]


@lru_cache(None)
def device_panel(label, qty, low):
    w, h = 280, 250
    im = rrect(w, h, 22, SURFACE + (255,), (255, 255, 255, 30), 2).copy()
    im.alpha_composite(text_sprite(label, "M", 22, TEXT2, 2), ((w - text_sprite(label, "M", 22, TEXT2, 2).width) // 2, 22))
    nm = text_sprite(ITEM, "C5", 24, MUTED)
    im.alpha_composite(nm, ((w - nm.width) // 2, 66))
    q = text_sprite(qty, "P8", 110, RED if low else TEXT)
    im.alpha_composite(q, ((w - q.width) // 2, 92))
    return im


def draw_sync(frame, n):
    if not (STEP_SYNC + 14 <= n < STEP_SEE + 10):
        return
    out = 1 - ease(lin(n, STEP_SEE - 6, STEP_SEE + 10))
    cx, cy, s = product_layout(n)
    src_y = cy + PC_H * s / 2
    low = n >= ALERT_IN
    shift = ease_io(lin(n, STEP_REORDER, STEP_REORDER + 16))         # devices make room for the alert
    for k, ((label, x), f) in enumerate(zip(DEVICES, SYNC_PULSES)):
        t = lin(n, STEP_SYNC + 14 + 5 * k, STEP_SYNC + 28 + 5 * k)
        y = 910
        al = ease(t * 1.4) * out * (1 - 0.65 * shift)
        # connector line with a travelling pulse
        lay = Image.new("RGBA", (W, 1350), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        d.line((cx, src_y, x, y - 125), fill=GOLD + (int(90 * al),), width=3)
        put(frame, lay, 0, 0, "tl")
        if f <= n < f + 18:
            p = ease_io(lin(n, f, f + 18))
            put(frame, K.circle(22, GOLD + (255,)), cx + (x - cx) * p, src_y + (y - 125 - src_y) * p, "cc", a=al)
        put(frame, device_panel(label, str(stock_value(max(n, COUNT_DOWN + 6))), low), x, y, "cc", a=al,
            s=0.8 + 0.2 * back(t, 1.8))


# ---------------------------------------------------------------- reorder alert
@lru_cache(None)
def alert_card(po_done):
    w, h = 880, 300
    im = rrect(w, h, 24, (44, 22, 20, 255), RED + (255,), 3).copy()
    d = ImageDraw.Draw(im)
    d.polygon([(52, 92), (92, 22), (132, 92)], fill=RED)
    im.alpha_composite(text_sprite("!", "P8", 46, BG), (84, 30))
    im.alpha_composite(text_sprite("LOW STOCK", "M", 26, RED, 3), (160, 26))
    im.alpha_composite(text_sprite(f"{ITEM}: 4 left (min. 5)", "C6", 36, TEXT), (160, 62))
    im.alpha_composite(text_sprite("Suggested: reorder 20 from your supplier", "C5", 30, TEXT2), (52, 136))
    if po_done:
        im.alpha_composite(K.pill("PURCHASE ORDER #0318  ·  DRAFT", GREEN, 24), (52, 206))
    else:
        btn = rrect(420, 66, 33, GOLD + (255,)).copy()
        ts = text_sprite("Create purchase order", "C7", 30, BG)
        btn.alpha_composite(ts, ((420 - ts.width) // 2, (66 - ts.height) // 2 + 2))
        im.alpha_composite(btn, (52, 204))
    return im


def draw_alert(frame, n):
    if not (ALERT_IN <= n < STEP_SEE + 6):
        return
    t = lin(n, ALERT_IN, ALERT_IN + 12)
    out = 1 - ease(lin(n, STEP_SEE - 6, STEP_SEE + 6))
    press = 1 - 0.06 * math.sin(math.pi * lin(n, PO_CLICK - 4, PO_CLICK + 4))
    put(frame, alert_card(n >= PO_CLICK + 2), W / 2, 1040, "cc", a=min(ease(t * 1.4), out),
        s=(0.7 + 0.3 * back(t, 2.0)) * press)


# ---------------------------------------------------------------- dashboard
TILE_DATA = [("SALES TODAY", "34", TEXT), ("LOW STOCK", "3 items", RED), ("TOP SELLER", "Phone cases", GOLD)]


@lru_cache(None)
def tile(label, value, col):
    w, h = 880, 150
    im = rrect(w, h, 22, SURFACE + (255,), (255, 255, 255, 30), 2).copy()
    im.alpha_composite(text_sprite(label, "M", 26, TEXT2, 3), (40, (h - 30) // 2))
    v = text_sprite(value, "P8", 60, col)
    im.alpha_composite(v, (w - 40 - v.width, (h - v.height) // 2 + 6))
    return im


@lru_cache(None)
def bars():
    w, h = 880, 190
    im = rrect(w, h, 22, SURFACE + (255,), (255, 255, 255, 30), 2).copy()
    d = ImageDraw.Draw(im)
    vals = [3, 5, 4, 7, 6, 9, 8, 5, 6, 4, 7, 10]
    for i, v in enumerate(vals):
        x = 40 + i * 68
        d.rounded_rectangle((x, h - 30 - v * 12, x + 40, h - 30), 6, fill=GOLD if i == 11 else (70, 70, 78))
    im.alpha_composite(text_sprite("SALES BY HOUR", "M", 22, TEXT2, 2), (40, 18))
    return im


def draw_dashboard(frame, n):
    if not (STEP_SEE <= n < STATEMENT + 6):
        return
    out = 1 - ease(lin(n, STATEMENT - 6, STATEMENT + 6))
    for k, f in enumerate(TILES):
        t = lin(n, f, f + 12)
        put(frame, tile(*TILE_DATA[k]), W / 2, 460 + k * 170, "cc", a=min(ease(t * 1.4), out),
            s=0.85 + 0.15 * back(t, 1.8))
    t = lin(n, TILES[-1] + 8, TILES[-1] + 20)
    put(frame, bars(), W / 2, 1060, "cc", a=min(ease(t * 1.4), out))


# ---------------------------------------------------------------- frames
STATEMENT_LINES = ((("Ready to move", TEXT),), (("beyond Excel?", GOLD),))


def render(n):
    frame = K.background(n)
    draw_sheet(frame, n)
    draw_shelf(frame, n)
    draw_files(frame, n)
    draw_questions(frame, n)
    draw_sync(frame, n)
    draw_product(frame, n)
    draw_sale(frame, n)
    draw_alert(frame, n)
    draw_dashboard(frame, n)
    K.draw_headlines(frame, n, HEADLINES)
    K.draw_steps(frame, n, STEPS, STEP_LABELS)
    K.draw_statement(frame, n, STATEMENT, STATEMENT_LINES, STATEMENT_BEATS)
    K.draw_end_card(frame, n)
    K.draw_chrome(frame, n, TURN + 8)
    return frame.convert("RGB")


CAPTIONS = [
    (6, SHELF - 4, "Your spreadsheet says 12."),
    (SHELF - 4, FILES - 2, "The shelf says 3."),
    (FILES - 2, QUESTIONS - 2, "Which file is right?"),
    (QUESTIONS - 2, TURN + 4, "Five files. Five numbers. Who updated it last? What sold today? When do we reorder?"),
    (TURN + 4, STEP_SELL, "One system. One number."),
    (STEP_SELL, STEP_SYNC, "1. Sell: stock updates the moment you sell."),
    (STEP_SYNC, STEP_REORDER, "2. Same number: shop, warehouse and owner see it."),
    (STEP_REORDER, STEP_SEE, "3. Reorder in time: low stock is flagged early."),
    (STEP_SEE, STATEMENT, "4. See the day: sales and stock at a glance."),
    (STATEMENT, END_CARD, "Ready to move beyond Excel? Odoo, or custom software built around exactly how you work."),
    (END_CARD, TOTAL, f"Book a {K.CALL_LENGTH} discovery call: {K.CTA_URL} or WhatsApp {K.PHONE}"),
]
PICKS = [(60, "Hook"), (130, "Shelf"), (190, "Files"), (250, "Questions"), (330, "One number"),
         (420, "1 Sell"), (540, "2 Sync"), (660, "3 Reorder"), (750, "4 See"), (860, "Statement"),
         (1000, "End card")]

if __name__ == "__main__":
    K.run(ARGS, render, CAPTIONS, PICKS, cover_frame=135)
