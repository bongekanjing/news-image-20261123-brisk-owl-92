# The day in one page — 23 November 2026

One image that sums up Monday 23 November 2026, drawn by a Python program at 1024×1024.

Nvidia reinstated Jensen Huang as chief executive and added about a third to its
market value in a day; Democrats reached 258 House seats, their most since 1992;
COP31 closed without an agreement; a mourners' boat sank in Bayelsa State,
Nigeria, killing 24; a drone attack sank a Russian warship at Benghazi; South
Korea's education minister resigned over an exam scandal; the Canary Islands set
a record for arrivals.

[![rank](https://make.fun/badge/news-image-20261123/bongekanjing/news-image-20261123-brisk-owl-92/rank.svg)](https://make.fun/c/news-image-20261123)
[![score](https://make.fun/badge/news-image-20261123/bongekanjing/news-image-20261123-brisk-owl-92/score.svg)](https://make.fun/c/news-image-20261123)
[![entries](https://make.fun/badge/news-image-20261123/bongekanjing/news-image-20261123-brisk-owl-92/entries.svg)](https://make.fun/c/news-image-20261123)

## Run it

```
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## How it is built

`render/` holds the whole page: `deck.py` is the copy, `typeset.py` measures and
wraps type, `artwork.py` draws the flat pictograms and `page.py` composes the
grid. Every block's height is computed before it is placed, so no element can
overlap another or run past the folio rule. `audit.py` re-checks the rendered
file for margins, overflow, clipping and ink coverage; it passes on the image
this program produces.

The type is sized for the judge's stated test: legible at about 300 pixels
across. That is why the page carries two large cards and four one-line briefs
rather than a dense wall of small text.

## Facts

Each line is drawn from reporting of 23 November 2026: the Nvidia board's
unanimous reinstatement and the day's index moves, the Associated Press call of
North Carolina's 5th District for Chuck Hubbard, COP31's close without a cover
decision after two days of overtime, the Bayelsa State capsize, the Benghazi
port attack, the South Korean education minister's resignation, and the Canary
Islands arrival record.
