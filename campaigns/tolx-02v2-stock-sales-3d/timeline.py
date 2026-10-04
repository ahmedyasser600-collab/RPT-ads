"""Shot list for TOLX video 02 v2 (30 fps). Shot lengths are set from the measured Gia takes."""
FPS = 30

_SHOTS = [  # (clip, overlay, frames)
    ("clips/s1_shelves.mp4", "shelves", 108),
    ("clips/s2_three_boxes.mp4", "three", 102),
    ("clips/s3_desk.mp4", "files", 120),
    ("clips/s4_counter.mp4", "sale", 114),
    ("clips/s5_warehouse.mp4", "sync", 144),
    ("clips/s6_top_shelf.mp4", "alert", 108),
    ("clips/s7_tidy_shop.mp4", "offer", 114),
]
SHOTS, _t = [], 0
OFFSETS = {"alert": 43}           # start the tilt-up clip later so the lone top-shelf box is in frame
for clip, ov, length in _SHOTS:
    SHOTS.append({"clip": clip, "overlay": ov, "start": _t, "len": length, "offset": OFFSETS.get(ov, 0)})
    _t += length
END_CARD = _t                     # 830 (27.7 s)
TOTAL = END_CARD + 138            # 968 frames (32.3 s)


def shot_at(n):
    for k, s in enumerate(SHOTS):
        if s["start"] <= n < s["start"] + s["len"]:
            return k, s
    return None, None
