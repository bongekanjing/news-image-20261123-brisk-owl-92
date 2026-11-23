"""Build entry.png for news-image-20261123.

The grader runs this in a network-less container: it composes the page from the
modules beside it, checks the result against the gate's limits, and copies it to
the output directory. Running it twice must produce identical bytes, so nothing
here depends on time, randomness or the environment.
"""
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from render import deck
from render.page import build

HERE = os.path.dirname(os.path.abspath(__file__))
MAX_BYTES = 1048576
MAX_SIDE = 1024


def png_header(path):
    """Read width, height and colour type straight from the IHDR chunk."""
    with open(path, "rb") as fh:
        head = fh.read(33)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("not a PNG")
    length = struct.unpack(">I", head[8:12])[0]
    if head[12:16] != b"IHDR" or length != 13:
        raise SystemExit("bad IHDR")
    w, h, depth, ctype = struct.unpack(">IIBB", head[16:26])
    return w, h, depth, ctype


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", os.path.join(HERE, "out"))
    os.makedirs(out_dir, exist_ok=True)
    tmp = os.path.join(out_dir, "entry.png")

    build(tmp)

    w, h, depth, ctype = png_header(tmp)
    if (w, h) != (MAX_SIDE, MAX_SIDE):
        raise SystemExit("image is %dx%d" % (w, h))
    if depth != 8 or ctype != 2:
        raise SystemExit("unexpected PNG depth/colour type %d/%d" % (depth, ctype))
    size = os.path.getsize(tmp)
    if size > MAX_BYTES:
        raise SystemExit("%d bytes exceeds 1 MiB" % size)

    # the deck must still name the day the contest is about
    if "23 NOVEMBER 2026" not in deck.DAY:
        raise SystemExit("deck names the wrong day")

    print("entry.png %dx%d %d bytes, %d cards, %d briefs"
          % (w, h, size, len(deck.CARDS), len(deck.STRIP)))


if __name__ == "__main__":
    main()
