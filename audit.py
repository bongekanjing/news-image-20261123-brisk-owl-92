"""Objective audit: geometry, clipping, margins, ink coverage. No vision, no guessing."""
import sys
from PIL import Image, ImageDraw

sys.path.insert(0, ".")
from render import page as P, deck
from render.typeset import font, wrap, SANS

IMG = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
PAPER = (247, 245, 240)
M = P.M


def main():
    im = Image.open(IMG).convert("RGB")
    W, H = im.size
    fails = []

    if (W, H) != (1024, 1024):
        fails.append("size %dx%d, want 1024x1024" % (W, H))
    import os
    b = os.path.getsize(IMG)
    if b > 1048576:
        fails.append("%d bytes over 1 MiB" % b)

    # 1. nothing but paper in the margins
    for name, xs, ys in (
        ("left", range(0, M - 2), range(0, H)),
        ("right", range(W - M + 2, W), range(0, H)),
    ):
        bad = sum(1 for y in ys for x in xs if im.getpixel((x, y)) != PAPER)
        if bad:
            fails.append("%s margin dirty: %d px" % (name, bad))

    # 2. content must stop above the folio rule
    rule_y = P.FOOT_Y - 32
    ink = 0
    for y in range(rule_y - 1, 0, -1):
        if any(im.getpixel((x, y)) != PAPER for x in range(W)):
            ink = y
            break
    if ink >= rule_y:
        fails.append("content runs to y=%d, folio rule at %d" % (ink, rule_y))

    # 3. every fitted string must fit its measure
    d = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    ix = W - 2 * M
    cw = (ix - P.GUT) // 2
    f_body = font(SANS, 26)
    pan_w = 250
    pan_x = W - M - pan_w
    body_w = pan_x - M - 24
    for para in deck.LEAD["body"]:
        for ln in wrap(d, para, f_body, body_w):
            if d.textlength(ln, font=f_body) > body_w + 0.5:
                fails.append("lead body line overflows: %r" % ln)
    for card in deck.CARDS:
        head = " ".join(card["head"])
        from render.typeset import fit
        hf, hl = fit(d, head, P.SERIFB, cw - 24, 44, 30, maxlines=2)
        for ln in hl:
            if d.textlength(ln, font=hf) > cw - 24 + 0.5:
                fails.append("%s headline overflows: %r" % (card["desk"], ln))
    # panel figure
    fig_s = 54
    while d.textlength(deck.LEAD["figure"], font=font(P.SERIFB, fig_s)) > pan_w - 28 and fig_s > 26:
        fig_s -= 2
    if d.textlength(deck.LEAD["figure"], font=font(P.SERIFB, fig_s)) > pan_w - 24:
        fails.append("figure %r wider than panel" % deck.LEAD["figure"])

    # 4. date must be present and plausible
    if "23 NOVEMBER 2026" not in deck.DAY or "23 November 2026" not in deck.FOOT:
        fails.append("date string wrong")

    # 5. ink coverage: a full page, not a sparse one
    total = W * H
    inked = sum(1 for y in range(0, H, 4) for x in range(0, W, 4) if im.getpixel((x, y)) != PAPER)
    cov = inked / (total / 16)
    if cov < 0.08:
        fails.append("ink coverage only %.1f%%" % (cov * 100))

    print("bytes %d  ink_bottom %d  rule %d  coverage %.1f%%" % (b, ink, rule_y, cov * 100))
    if fails:
        print("FAIL")
        for f in fails:
            print("  -", f)
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
