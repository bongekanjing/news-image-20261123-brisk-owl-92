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
    """A boat heeling over, its bow already under the water."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    waterline = y0 + h * 0.64
    # a hull tilted so the bow goes under: the deck line runs down into the water
    hull = [(x0 + w * 0.08, y0 + h * 0.50), (x1 - w * 0.10, y0 + h * 0.70),
            (x1 - w * 0.24, y0 + h * 0.84), (x0 + w * 0.22, y0 + h * 0.70)]
    d.polygon(hull, fill=INK)
    # the mast leans the same way the hull does
    d.line([x0 + w * 0.34, y0 + h * 0.56, x0 + w * 0.50, y0 + h * 0.16],
           fill=INK, width=max(3, int(w * 0.028)))
    # figures crowd the high (stern) end, away from the water
    for i in range(3):
        fx = x0 + w * (0.30 + i * 0.10)
        fy = y0 + h * (0.30 + i * 0.045)
        _ell(d, [fx - w * 0.030, fy, fx + w * 0.030, fy + h * 0.10], INK)
    # the waterline cuts across the hull, so part of the boat is submerged
    d.line([x0, waterline, x1, waterline], fill=tint, width=max(3, int(h * 0.045)))
    for row in range(2):
        yy = y1 - h * (0.22 - row * 0.13)
        pts = []
        for i in range(21):
            fx = x0 + (x1 - x0) * i / 20
            pts.append((fx, yy + (h * 0.05) * (1 if (i // 3) % 2 else -1)))
        d.line(pts, fill=tint, width=max(2, int(h * 0.035)), joint="curve")


def ship(d, box, tint):
    """A warship listing hard, holed at the waterline, with a smoke column."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    waterline = y0 + h * 0.80
    # the hull is rotated: the bow rides up, the stern is going under
    hull = [(x0 + w * 0.12, y0 + h * 0.62), (x1 - w * 0.10, y0 + h * 0.76),
            (x1 - w * 0.18, y0 + h * 0.92), (x0 + w * 0.22, y0 + h * 0.86)]
    d.polygon(hull, fill=INK)
    d.rectangle([x0 + w * 0.36, y0 + h * 0.44, x0 + w * 0.60, y0 + h * 0.68], fill=INK)
    d.line([x0 + w * 0.52, y0 + h * 0.44, x0 + w * 0.48, y0 + h * 0.22],
           fill=INK, width=max(2, int(w * 0.02)))
    # the breach: a notch blown out of the hull at the waterline
    d.polygon([(x1 - w * 0.34, waterline - h * 0.10), (x1 - w * 0.20, waterline - h * 0.02),
               (x1 - w * 0.30, waterline + h * 0.10)], fill=PAPER)
    # smoke leans off the stern, so the plume reads as damage not exhaust
    for i in range(4):
        r = w * (0.055 + i * 0.014)
        cx = x0 + w * (0.50 - i * 0.075)
        cy = y0 + h * (0.28 - i * 0.058)
        _ell(d, [cx - r, cy - r, cx + r, cy + r], tint)
    # the waterline cuts the hull
    d.line([x0 + w * 0.02, waterline, x1 - w * 0.02, waterline], fill=tint, width=3)


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
    """A packed boat low in the water, seen against a distant shore."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    water = y0 + h * 0.66
    # the far shore: a low, uneven horizon well above the waterline
    d.line([x0, y0 + h * 0.26, x0 + w * 0.30, y0 + h * 0.20], fill=tint,
           width=max(3, int(h * 0.05)))
    d.line([x0 + w * 0.30, y0 + h * 0.20, x1, y0 + h * 0.30], fill=tint,
           width=max(3, int(h * 0.05)))
    # the open water
    d.line([x0, water, x1, water], fill=tint, width=max(3, int(h * 0.05)))
    # a low, overladen hull sitting *in* the water, not floating above it
    hull = [(x0 + w * 0.16, water - h * 0.10), (x1 - w * 0.14, water - h * 0.13),
            (x1 - w * 0.22, water + h * 0.08), (x0 + w * 0.24, water + h * 0.08)]
    d.polygon(hull, fill=INK)
    # heads crowded along the gunwale
    for i in range(5):
        fx = x0 + w * (0.28 + i * 0.11)
        _ell(d, [fx - w * 0.035, water - h * 0.27, fx + w * 0.035, water - h * 0.17], INK)
    # one raised arm, so it reads as people, not cargo
    d.line([x0 + w * 0.60, water - h * 0.28, x0 + w * 0.62, water - h * 0.44],
           fill=INK, width=max(2, int(h * 0.04)))


ART = {"capitol": capitol, "globe": globe, "boat": boat,
       "ship": ship, "exam": exam, "crossing": crossing}
