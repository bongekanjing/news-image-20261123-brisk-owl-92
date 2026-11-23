"""Flat pictograms. Every mark is drawn from primitives so it survives a 300px downsample."""
from PIL import Image, ImageDraw

INK = (26, 26, 30)
PAPER = (247, 245, 240)
RED = (163, 32, 30)
BLUE = (36, 74, 128)
GREEN = (28, 96, 86)
GOLD = (176, 126, 26)
PLUM = (110, 60, 100)


def _ell(d, box, fill, outline=None, wid=3):
    d.ellipse(box, fill=fill, outline=outline, width=wid)


def capitol(d, box, tint):
    """Domed legislature: steps, colonnade, dome, flag."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    d.rectangle([x0, y1 - h * 0.10, x1, y1], fill=tint)
    for i in range(3):
        d.rectangle([x0 + w * 0.06 + i * w * 0.03, y1 - h * 0.16 + i * h * 0.03,
                     x1 - w * 0.06 - i * w * 0.03, y1 - h * 0.13 + i * h * 0.05], fill=INK)
    d.rectangle([x0 + w * 0.20, y1 - h * 0.46, x1 - w * 0.20, y1 - h * 0.13], fill=INK)
    cols = 6
    for c in range(cols):
        cx = x0 + w * 0.23 + c * (w * 0.54 / (cols - 1))
        d.rectangle([cx - w * 0.012, y1 - h * 0.44, cx + w * 0.012, y1 - h * 0.16], fill=PAPER)
    d.rectangle([x0 + w * 0.18, y1 - h * 0.50, x1 - w * 0.18, y1 - h * 0.46], fill=INK)
    _ell(d, [x0 + w * 0.34, y1 - h * 0.86, x1 - w * 0.34, y1 - h * 0.48], tint)
    d.rectangle([x0 + w * 0.485, y1 - h * 0.99, x0 + w * 0.515, y1 - h * 0.85], fill=INK)


def globe(d, box, tint):
    """Globe with a meridian and a widening crack, clipped to the disc."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2

    _ell(d, box, tint)
    d.arc(box, 0, 360, fill=PAPER, width=max(2, int(w * 0.03)))
    _ell(d, [x0 + w * 0.33, y0, x1 - w * 0.33, y1], None, PAPER, max(2, int(w * 0.025)))
    d.line([x0, cy, x1, cy], fill=PAPER, width=max(2, int(w * 0.025)))

    # the crack lives on an alpha-only layer, then is masked to the sphere
    cw, ch = int(w), int(h)
    crack = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    cd = ImageDraw.Draw(crack)
    pts = [(w * 0.20, h * 0.92), (w * 0.40, h * 0.58), (w * 0.33, h * 0.46),
           (w * 0.58, h * 0.38), (w * 0.50, h * 0.24), (w * 0.74, h * 0.10)]
    cd.line(pts, fill=INK + (255,), width=max(3, int(w * 0.05)), joint="curve")

    disc = Image.new("L", (cw, ch), 0)
    ImageDraw.Draw(disc).ellipse([0, 0, cw - 1, ch - 1], fill=255)
    alpha = Image.composite(crack.getchannel("A"), Image.new("L", (cw, ch), 0), disc)
    crack.putalpha(alpha)

    base = d._image.convert("RGBA")
    base.alpha_composite(crack, (int(x0), int(y0)))
    d._image.paste(base.convert("RGB"))


def boat(d, box, tint):
    """A small boat heeling under a wave."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    hull = [(x0 + w * 0.10, y0 + h * 0.56), (x1 - w * 0.06, y0 + h * 0.52),
            (x1 - w * 0.20, y0 + h * 0.74), (x0 + w * 0.26, y0 + h * 0.76)]
    d.polygon(hull, fill=tint)
    d.line([x0 + w * 0.16, y0 + h * 0.56, x1 - w * 0.12, y0 + h * 0.53],
           fill=INK, width=max(2, int(h * 0.03)))
    d.line([x0 + w * 0.40, y0 + h * 0.56, x0 + w * 0.44, y0 + h * 0.20],
           fill=INK, width=max(3, int(w * 0.025)))
    # figures in the boat
    for i in range(3):
        fx = x0 + w * (0.44 + i * 0.12)
        _ell(d, [fx - w * 0.028, y0 + h * 0.34, fx + w * 0.028, y0 + h * 0.44], INK)
    # wave crests
    for row in range(2):
        yy = y1 - h * (0.24 - row * 0.14)
        pts = []
        for i in range(21):
            fx = x0 + (x1 - x0) * i / 20
            pts.append((fx, yy + (h * 0.05) * (1 if (i // 3) % 2 else -1)))
        d.line(pts, fill=tint, width=max(2, int(h * 0.035)), joint="curve")


def ship(d, box, tint):
    """A warship listing, with a smoke column."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    hull = [(x0 + w * 0.14, y0 + h * 0.66), (x1 - w * 0.10, y0 + h * 0.58),
            (x1 - w * 0.16, y0 + h * 0.76), (x0 + w * 0.22, y0 + h * 0.80)]
    d.polygon(hull, fill=INK)
    d.rectangle([x0 + w * 0.34, y0 + h * 0.42, x0 + w * 0.58, y0 + h * 0.66], fill=INK)
    d.line([x0 + w * 0.50, y0 + h * 0.42, x0 + w * 0.50, y0 + h * 0.22],
           fill=INK, width=max(2, int(w * 0.02)))
    # smoke
    for i in range(4):
        r = w * (0.055 + i * 0.012)
        cx = x0 + w * (0.52 + i * 0.085)
        cy = y0 + h * (0.30 - i * 0.062)
        _ell(d, [cx - r, cy - r, cx + r, cy + r], tint)
    # water
    d.line([x0 + w * 0.04, y0 + h * 0.82, x1 - w * 0.04, y0 + h * 0.82], fill=tint, width=3)


def exam(d, box, tint):
    """A sheet with a red cross through it."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    d.rectangle([x0 + w * 0.18, y0 + h * 0.10, x1 - w * 0.18, y1 - h * 0.10], fill=PAPER, outline=INK, width=3)
    for i in range(4):
        yy = y0 + h * (0.26 + i * 0.16)
        d.line([x0 + w * 0.26, yy, x1 - w * 0.34, yy], fill=INK, width=max(2, int(h * 0.024)))
    d.line([x0 + w * 0.24, y0 + h * 0.20, x1 - w * 0.24, y1 - h * 0.20], fill=RED, width=max(4, int(w * 0.05)))
    d.line([x1 - w * 0.24, y0 + h * 0.20, x0 + w * 0.24, y1 - h * 0.20], fill=RED, width=max(4, int(w * 0.05)))


def crossing(d, box, tint):
    """A small boat against a long coastline."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    d.ellipse([x0, y1 - h * 0.30, x1, y1 + h * 0.30], fill=tint)
    d.line([x0, y0 + h * 0.42, x1, y0 + h * 0.34], fill=INK, width=max(3, int(h * 0.035)))
    # little boat
    bx0 = x0 + w * 0.44
    d.polygon([(bx0, y0 + h * 0.60), (bx0 + w * 0.20, y0 + h * 0.58),
               (bx0 + w * 0.17, y0 + h * 0.70), (bx0 + w * 0.03, y0 + h * 0.71)], fill=INK)
    d.line([bx0 + w * 0.09, y0 + h * 0.60, bx0 + w * 0.10, y0 + h * 0.46], fill=INK, width=3)


ART = {"capitol": capitol, "globe": globe, "boat": boat,
       "ship": ship, "exam": exam, "crossing": crossing}
