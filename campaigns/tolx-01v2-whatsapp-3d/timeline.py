"""Shot list for TOLX video 01 v2 "WhatsApp orders" (30 fps). Shot lengths are set from the measured Gia takes."""
FPS = 30

_SHOTS = [  # (clip, overlay, frames)
    ("clips/s1_phone_counter.mp4", "phone", 96),
    ("clips/s2_phone_packing.mp4", "buried", 126),
    ("clips/s3_parcel.mp4", "parcel", 100),
    ("clips/s4_van.mp4", "status", 132),
    ("clips/s5_tablet.mp4", "reminder", 102),
    ("clips/s6_dispatch_room.mp4", "offer", 102),
]
OFFSETS = {}
SHOTS, _t = [], 0
for clip, ov, length in _SHOTS:
    SHOTS.append({"clip": clip, "overlay": ov, "start": _t, "len": length, "offset": OFFSETS.get(ov, 0)})
    _t += length
END_CARD = _t                     # 658 (21.9 s)
TOTAL = END_CARD + 138            # 796 frames (26.5 s)


def shot_at(n):
    for k, s in enumerate(SHOTS):
        if s["start"] <= n < s["start"] + s["len"]:
            return k, s
    return None, None
