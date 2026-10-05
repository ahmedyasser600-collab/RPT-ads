"""Extract the stand-in logo emblem from the supplied website screenshot PDF.

tribudelalma.com was blocked by the render environment's network policy, so the original
logo PNG could not be downloaded. The round emblem in the screenshot header (about 118 px)
is cut out pixel for pixel: no redrawing, recolouring or generation. Drop the original logo
into assets/originals/ and the renderer uses it instead.

Usage: python tools/extract_standins.py <screenshot.pdf>      (needs poppler's pdfimages)
"""
import os
import subprocess
import sys
import tempfile

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "assets", "standin")
EMBLEM = (118, 44, 236, 162)             # page-1 pixel box of the header emblem


def main(pdf):
    tmp = tempfile.mkdtemp()
    subprocess.run(["pdfimages", "-j", "-f", "1", "-l", "1", pdf, os.path.join(tmp, "p")], check=True)
    page = Image.open(os.path.join(tmp, "p-000.jpg")).convert("RGB")
    os.makedirs(OUT, exist_ok=True)
    page.crop(EMBLEM).save(os.path.join(OUT, "emblem-screenshot.png"))
    print("emblem-screenshot.png")


if __name__ == "__main__":
    main(sys.argv[1])
