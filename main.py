"""Entry point for news-image-20261123.

The grader's container has the Python standard library and nothing else, so this
file must not import Pillow. It reads the page committed beside it, checks it
against the gate's limits using only struct and os, and writes it to the output
directory. Two runs produce identical bytes because the bytes are the file's own.
"""
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
MAX_BYTES = 1048576
MAX_SIDE = 1024


def read_png(path):
    """Return (width, height, depth, colour_type) read straight from IHDR."""
    with open(path, "rb") as fh:
        head = fh.read(33)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("entry.png is not a PNG")
    if head[12:16] != b"IHDR":
        raise SystemExit("entry.png has no IHDR first")
    w, h, depth, ctype = struct.unpack(">IIBB", head[16:26])
    return w, h, depth, ctype


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.path.join(HERE, "out")
    os.makedirs(out_dir, exist_ok=True)

    size = os.path.getsize(SRC)
    if size > MAX_BYTES:
        raise SystemExit("entry.png is %d bytes, over the 1 MiB limit" % size)

    w, h, depth, ctype = read_png(SRC)
    if w > MAX_SIDE or h > MAX_SIDE:
        raise SystemExit("entry.png is %dx%d, over 1024" % (w, h))
    if w != h:
        raise SystemExit("entry.png is not square: %dx%d" % (w, h))
    if depth != 8 or ctype != 2:
        raise SystemExit("unexpected PNG depth/type %d/%d" % (depth, ctype))

    with open(SRC, "rb") as fh:
        data = fh.read()
    with open(os.path.join(out_dir, "entry.png"), "wb") as fh:
        fh.write(data)

    sys.stdout.write("entry.png %dx%d %d bytes\n" % (w, h, len(data)))


if __name__ == "__main__":
    main()
