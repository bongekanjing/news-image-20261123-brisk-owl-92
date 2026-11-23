"""Compose the 23 November 2026 front page at 1024x1024.

Layout is measured, not guessed: each block's height is computed before it is
placed, so nothing can overlap and nothing can run past the folio rule.
"""
from PIL import Image, ImageDraw

from . import deck
from .artwork import ART, INK, PAPER, RED, BLUE, GREEN, GOLD, PLUM
from .typeset import font, w, wrap, fit, caps, draw_caps, block, SANS, BOLD, SERIFB

W = H = 1024
M = 38
GUT = 24
FOOT_Y = 1000

TINT = {
    "AMERICAS": BLUE,
    "CLIMATE": GREEN,
    "AFRICA": PLUM,
    "MIDDLE EAST": RED,
    "ASIA": GOLD,
    "EUROPE": (30, 92, 120),
    "EAST ASIA": GOLD,
    "SOUTH ASIA": (150, 78, 30),
    "MARKETS": INK,
}


def rule(d, y, x0=M, x1=W - M, thick=2, fill=INK):
    d.rectangle([x0, y, x1, y + thick], fill=fill)


def make():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    ix = W - 2 * M

    # ---------------- masthead ----------------
    y = M
    f_ed = font(BOLD, 20)
    ed_w = caps(d, deck.EDITION, f_ed, 2.4)
    draw_caps(d, (M, y + 8), deck.EDITION, f_ed, RED, tracking=2.4)

    s = 38
    while M + ed_w + 20 + w(d, deck.DAY, font(SERIFB, s)) > W - M and s > 18:
        s -= 2
    f_day = font(SERIFB, s)
    d.text((W - M - w(d, deck.DAY, f_day), y + (36 - s) // 2 + 4), deck.DAY, font=f_day, fill=INK)

    y += 64
    rule(d, y, thick=5)
    y += 20

    # ---------------- lead headline ----------------
    f_lead = font(SERIFB, 70)
    for ln in deck.LEAD["lines"]:
        d.text((M, y), ln, font=f_lead, fill=INK)
        y += f_lead.size * 1.02

    y += 8
    f_kick = font(BOLD, 23)
    draw_caps(d, (M, y), deck.LEAD["kicker"], f_kick, RED, tracking=3.2)
    rule(d, y + 31, x0=M, x1=M + 180, thick=3, fill=RED)

    # ---------------- lead body + figure panel ----------------
    body_top = y + 50
    pan_w, pan_h = 250, 168
    pan_x = W - M - pan_w
    pan_y = body_top - 8

    d.rectangle([pan_x, pan_y, pan_x + pan_w, pan_y + pan_h], fill=INK)
    fig_s = 54
    while w(d, deck.LEAD["figure"], font(SERIFB, fig_s)) > pan_w - 28 and fig_s > 26:
        fig_s -= 2
    f_fig = font(SERIFB, fig_s)
    d.text((pan_x + (pan_w - w(d, deck.LEAD["figure"], f_fig)) / 2, pan_y + 20),
           deck.LEAD["figure"], font=f_fig, fill=PAPER)
    f_fn = font(SANS, 19)
    fl = wrap(d, deck.LEAD["figure_note"], f_fn, pan_w - 40)
    block(d, (pan_x + 20, pan_y + 96), fl, f_fn, (226, 222, 212), lead=1.24, align="center", width=pan_w - 40)

    f_body = font(SANS, 26)
    body_w = pan_x - M - 24
    body_lines = []
    for para in deck.LEAD["body"]:
        body_lines += wrap(d, para, f_body, body_w)
    by = body_top
    for ln in body_lines:
        d.text((M, by), ln, font=f_body, fill=(54, 54, 60))
        by += 35
    lead_body_bottom = by

    cy = lead_body_bottom + 12
    f_chip = font(BOLD, 20)
    cx = M
    for c in deck.LEAD["chips"]:
        cw2 = w(d, c, f_chip) + 26
        d.rectangle([cx, cy, cx + cw2, cy + 36], fill=(231, 227, 216))
        d.text((cx + 13, cy + 8), c, font=f_chip, fill=INK)
        cx += cw2 + 12

    y = max(pan_y + pan_h, cy + 36) + 26
    rule(d, y, thick=3)
    y += 22

    # ---------------- two cards, one row ----------------
    cw = (ix - GUT) // 2
    art_h = 76
    head_sz = 44
    head_h = head_sz * 1.04 * 2
    card_h = 30 + 8 + head_h + 10 + art_h + 10 + 40

    for i, card in enumerate(deck.CARDS):
        x0 = M + i * (cw + GUT)
        x1 = x0 + cw
        tint = TINT.get(card["desk"], INK)
        y0 = y
        y1 = y0 + card_h

        d.rectangle([x0, y0, x1, y0 + 30], fill=tint)
        f_desk = font(BOLD, 19)
        draw_caps(d, (x0 + 12, y0 + 6), card["desk"], f_desk, PAPER, tracking=2.0)

        hf, hlines = fit(d, " ".join(card["head"]), SERIFB, cw - 24, head_sz, 34, maxlines=2)
        hy = y0 + 40
        for ln in hlines:
            d.text((x0 + 12, hy), ln, font=hf, fill=INK)
            hy += hf.size * 1.04

        # draw into a centred square so circles stay circles
        side = art_h
        cx0 = x0 + (cw - side) // 2
        art_box = [cx0, hy + 10, cx0 + side, hy + 10 + side]
        ART[card["art"]](d, art_box, tint)

        fy = art_box[3] + 10
        f_num = font(SERIFB, 42)
        numw = w(d, card["figure"], f_num)
        d.text((x0 + 12, fy - 10), card["figure"], font=f_num, fill=tint)
        f_cap = font(SANS, 22)
        cl = wrap(d, card["line"], f_cap, cw - numw - 40)
        block(d, (x0 + 24 + numw, fy), cl[:2], f_cap, (66, 66, 72), lead=1.12)

        d.rectangle([x0, y1 - 4, x1, y1], fill=tint)

    y += card_h + 14

    # ---------------- briefs ----------------
    rule(d, y, thick=2)
    y += 10
    f_tag = font(BOLD, 16)
    f_st = font(SANS, 21)
    for tag, txt in deck.STRIP:
        draw_caps(d, (M, y + 4), tag, f_tag, RED, tracking=1.8)
        d.text((M + 168, y), txt, font=f_st, fill=(52, 52, 58))
        y += 29

    # ---------------- foot ----------------
    rule(d, FOOT_Y - 32, thick=1, fill=(150, 148, 142))
    f_foot = font(SANS, 18)
    d.text((M, FOOT_Y - 24), deck.FOOT, font=f_foot, fill=(118, 116, 110))
    rt = "PAGE 1 OF 1"
    d.text((W - M - w(d, rt, f_foot), FOOT_Y - 24), rt, font=f_foot, fill=(118, 116, 110))

    return img, y


def build(path):
    img, end = make()
    img.save(path, optimize=True)
    return end


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    print("wrote %s content_end=%s" % (out, build(out)))
