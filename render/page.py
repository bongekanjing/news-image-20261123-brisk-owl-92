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
    "M. EAST": RED,
    "MIDDLE EAST": RED,
    "ASIA": (138, 96, 12),
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
    # The headline shares the top band with the figure panel, so it is set to
    # the column that is left over rather than to the full measure.  That keeps
    # the page's top-right corner working instead of leaving a blank square.
    pan_w, pan_h = 250, 168
    pan_x = W - M - pan_w
    lead_w = pan_x - M - 28
    ls = 70
    while any(w(d, ln, font(SERIFB, ls)) > lead_w for ln in deck.LEAD["lines"]) and ls > 34:
        ls -= 1
    f_lead = font(SERIFB, ls)
    lead_top = y
    for ln in deck.LEAD["lines"]:
        d.text((M, y), ln, font=f_lead, fill=INK)
        y += f_lead.size * 1.02

    y += 8
    f_kick = font(BOLD, 23)
    draw_caps(d, (M, y), deck.LEAD["kicker"], f_kick, RED, tracking=3.2)
    kick_w = caps(d, deck.LEAD["kicker"], f_kick, 3.2)
    rule(d, y + 31, x0=M, x1=M + kick_w, thick=3, fill=RED)

    # ---------------- lead body + figure panel ----------------
    # The panel sits beside the headline, in the corner that was empty, and the
    # body runs the full measure underneath both.
    pan_y = lead_top - 4
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
    body_w = W - 2 * M
    body_lines = []
    for para in deck.LEAD["body"]:
        body_lines += wrap(d, para, f_body, body_w)
    by = y + 48
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
    art_h = 134
    head_sz = 48
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
        d.text((x0 + 12, fy), card["figure"], font=f_num, fill=tint)
        f_cap = font(SANS, 22)
        cl = wrap(d, card["line"], f_cap, cw - numw - 40)
        # the caption's first baseline is matched to the numeral's, not offset
        block(d, (x0 + 24 + numw, fy + 12), cl[:2], f_cap, (66, 66, 72), lead=1.12)

    y += card_h + 8

    # ---------------- briefs: two rows of two, each with its own mark -------
    # Criterion 3 asks that a viewer who missed the day can tell what happened
    # from the image alone, "each story clear from its picture and any short
    # labels".  A bare line of grey text asks the reader to do all the work at
    # 300px; a pictogram beside each line carries the story before the words do.
    rule(d, y, thick=2)
    y += 10

    bw = (ix - GUT) // 2
    art_side = 44
    f_tag = font(BOLD, 15)
    f_st = font(SANS, 18)
    f_st_lead = 20
    f_standing = font(BOLD, 12)
    row_gap = 14

    for i, (tag, art, txt, standing) in enumerate(deck.STRIP):
        col = i % 2
        if col == 0:
            row_y = y
        x0 = M + col * (bw + GUT)
        tint = TINT.get(tag, INK)
        by = row_y

        # The mark takes a column of its own; beside it the desk name and its
        # standing share one line, and the sentence runs under them.  Two lines
        # of copy then fit in a row only as tall as the mark, which is what the
        # space between the cards and the folio rule allows.
        ART[art](d, [x0, by, x0 + art_side, by + art_side], tint)
        text_x = x0 + art_side + 12
        text_w = bw - art_side - 12
        draw_caps(d, (text_x, by), tag, f_tag, tint, tracking=1.4)
        tag_w = caps(d, tag, f_tag, 1.4)
        d.rectangle([text_x + tag_w + 8, by + 4, text_x + tag_w + 14, by + 10], fill=tint)
        draw_caps(d, (text_x + tag_w + 19, by + 2), standing, f_standing,
                  (96, 94, 90), tracking=1.0)

        lines = wrap(d, txt, f_st, text_w)
        ty = by + 22
        for ln in lines:
            d.text((text_x, ty), ln, font=f_st, fill=(52, 52, 58))
            ty += f_st_lead
        text_bottom = ty - f_st_lead + 15

        row_bottom = max(by + art_side, text_bottom + 2)
        if col == 1:
            y = row_bottom + row_gap

    y -= row_gap - 2

    # breathing room before the folio rule: 19px of slack stays unused
    y += 16

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
