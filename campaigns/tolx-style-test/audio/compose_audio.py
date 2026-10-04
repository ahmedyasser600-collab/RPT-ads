"""Audio for the style test: smooth bed, two Gia lines, a few soft accents."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tolx-kit"))
import tolx_audio as A  # noqa: E402

DUR = 10.0
music = A.build_music_smooth(DUR, DUR - 1.4)      # soft resolve in the last second
sfx = np.zeros(int(A.SR * DUR))
A.add(sfx, A.swish(0.8, 0.02, 400, 3500, rise=False), 12 / 30)        # scribble draws on
A.add(sfx, A.chime(0.035), 18 / 30 + 0.15)                              # sheet tile
A.add(sfx, A.swish(0.9, 0.03, 300, 4000), 5.0 - 0.6)                   # shot change
A.add(sfx, A.soft_keys(A.hz("E6"), 0.035, 0.9), 5.0 + 10 / 30)          # sparks
A.add(sfx, A.chime(0.035), 5.0 + 18 / 30 + 0.15)                        # box tile
A.write_stereo(os.path.join(HERE, "music.wav"), music, 0.55, DUR)
A.write_stereo(os.path.join(HERE, "sfx.wav"), sfx, 0.45, DUR)
A.place_vo([("Your spreadsheet says twelve in stock...", 0.4, 4.9), ("But the shelf? Only three!", 5.3, 9.6)],
           os.path.join(HERE, "vo_lines"), "g", os.path.join(HERE, "vo_gia.wav"), DUR, base_tempo=1.06, fx=A.ENERGY_FX)
