"""Type helpers: cached fonts, measured wrapping, and tracked capitals."""
import os
from PIL import ImageFont

DIR = "/usr/share/fonts/truetype/dejavu/"
SANS = "DejaVuSans.ttf"
BOLD = "DejaVuSans-Bold.ttf"
SERIF = "DejaVuSerif.ttf"
SERIFB = "DejaVuSerif-Bold.ttf"
COND = "DejaVuSansCondensed-Bold.ttf"

_f = {}


def font(name, size):
    k = (name, int(size))
    if k not in _f:
        _f[k] = ImageFont.truetype(DIR + name, int(size))
    return _f[k]


def w(d, text, f):
    return d.textlength(text, font=f)


def wrap(d, text, f, maxw):
    """Greedy wrap to maxw; returns lines that each fit."""
    out, cur = [], ""
    for word in text.split():
        t = (cur + " " + word) if cur else word
        if w(d, t, f) <= maxw:
            cur = t
        else:
            if cur:
                out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def fit(d, text, name, maxw, start, minv=12, maxlines=None):
    """Largest size <= start whose wrapped form fits maxw in <= maxlines."""
    s = int(start)
    while s > minv:
        f = font(name, s)
        lines = wrap(d, text, f, maxw)
        bad = any(w(d, l, f) > maxw for l in lines)
        if not bad and (maxlines is None or len(lines) <= maxlines):
            return f, lines
        s -= 1
    f = font(name, minv)
    return f, wrap(d, text, f, maxw)


def caps(d, text, f, tracking=0.0):
    """Width of tracked capitals, drawn one glyph at a time."""
    total = 0.0
    for i, ch in enumerate(text):
        total += d.textlength(ch, font=f)
        if i < len(text) - 1:
            total += tracking
    return total


def draw_caps(d, xy, text, f, fill, tracking=0.0):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=f, fill=fill)
        x += d.textlength(ch, font=f) + tracking
    return x


def block(d, xy, lines, f, fill, lead=1.12, align="left", width=None):
    """Draw pre-wrapped lines; returns y after the last baseline."""
    x, y = xy
    step = f.size * lead
    for ln in lines:
        lw = w(d, ln, f)
        dx = x if align == "left" else (x + (width - lw) / 2 if align == "center" else x + width - lw)
        d.text((dx, y), ln, font=f, fill=fill)
        y += step
    return y
