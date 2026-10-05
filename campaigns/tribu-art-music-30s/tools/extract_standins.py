"""Extract stand-in photographs from the supplied website screenshot PDF.

Why: tribudelalma.com was blocked by the render environment's network policy, so the
original files listed in config.json ("original") could not be downloaded. The supplied
screenshot PDF (screencapture-tribu-art-music-...pdf, a 3-page full-page capture at
2880 px width) contains three of the real Tribu del Alma photographs at roughly 1:1
scale. They are cut out here pixel-for-pixel: no upscaling, retouching, generation or
fill. Only clean rectangles are kept; the demo page's rounded corners and its caption
overlay ("A little space... / Finca Pura Vida") are left out.

Drop the original files into assets/originals/ and the renderer uses them instead.

Usage: python tools/extract_standins.py <screenshot.pdf>      (needs poppler's pdfimages)
"""
import os
import subprocess
import sys
import tempfile

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "assets", "standin")

# Page-image pixel boxes (left, top, right, bottom), measured against the cream page
# background (240, 238, 226).
FINCA = (1372, 276, 2770, 1606)          # full photo incl. rounded top-left corner
FINCA_CLEAN = (1372 + 0, 572, 2770, 1400)  # below the corner arc, above the caption overlay
FINCA_TALL = (1720, 276, 2770, 1400)     # right of the corner arc, above the caption overlay
PAINT = (0, 2731, 1610, 3786)            # page 1, ends at the page edge; dark panel starts at x 1612
GUITAR_P2 = (181, 2993, 1300, 3786)      # page 2 bottom; top-right corner is rounded
GUITAR_P3 = (181, 0, 1300, 106)          # page 3 top: continuation of the same photo
EMBLEM = (118, 44, 236, 162)             # header emblem (logo mark), ~105 px wide


def main(pdf):
    tmp = tempfile.mkdtemp()
    subprocess.run(["pdfimages", "-j", pdf, os.path.join(tmp, "p")], check=True)
    pages = [Image.open(os.path.join(tmp, f"p-00{i}.jpg")).convert("RGB") for i in range(3)]
    os.makedirs(OUT, exist_ok=True)

    def save(im, name):
        im.save(os.path.join(OUT, name), quality=95, subsampling=0)
        print(f"{name}: {im.size[0]}x{im.size[1]}")

    save(pages[0].crop(FINCA_CLEAN), "finca-wide.jpg")
    save(pages[0].crop(FINCA_TALL), "finca-tall.jpg")
    save(pages[0].crop(PAINT), "painting-outdoors.jpg")
    top, bottom = pages[1].crop(GUITAR_P2), pages[2].crop(GUITAR_P3)
    music = Image.new("RGB", (top.width, top.height + bottom.height))
    music.paste(top, (0, 0))
    music.paste(bottom, (0, top.height))
    # Drop the rounded top-right corner of the demo layout: keep rows below the arc.
    save(music.crop((0, 110, music.width, music.height)), "music-terrace.jpg")
    pages[0].crop(EMBLEM).save(os.path.join(OUT, "emblem-screenshot.png"))
    print("emblem-screenshot.png")


if __name__ == "__main__":
    main(sys.argv[1])
