"""
5x7 pixel bitmap font + SVG rect emitter.

Every glyph is 5 cells wide and 7 cells tall (the BASE box). Accented Turkish
characters borrow two optional zones: two rows ABOVE the base box and one row
BELOW it, so the full canvas per glyph is 5x10:

    rows -3..-1  above zone (breve arc / dot, last row kept clear)
    rows  0..6   base box
    row   7      below zone (cedilla)

Plain letters leave the above/below zones empty, so a line of ordinary text
still occupies exactly 7 rows of ink. Only the diacritics reach outside.
"""

ABOVE_ROWS = 3
BELOW_ROWS = 1
GLYPH_W = 5
BASE_H = 7
FULL_H = ABOVE_ROWS + BASE_H + BELOW_ROWS

BASE = {
    "A": ".###.|#...#|#...#|#####|#...#|#...#|#...#",
    "B": "####.|#...#|#...#|####.|#...#|#...#|####.",
    "C": ".###.|#...#|#....|#....|#....|#...#|.###.",
    "D": "####.|#...#|#...#|#...#|#...#|#...#|####.",
    "E": "#####|#....|#....|####.|#....|#....|#####",
    "F": "#####|#....|#....|####.|#....|#....|#....",
    "G": ".###.|#...#|#....|#.###|#...#|#...#|.###.",
    "H": "#...#|#...#|#...#|#####|#...#|#...#|#...#",
    "I": "#####|..#..|..#..|..#..|..#..|..#..|#####",
    "J": "..###|...#.|...#.|...#.|...#.|#..#.|.##..",
    "K": "#...#|#..#.|#.#..|##...|#.#..|#..#.|#...#",
    "L": "#....|#....|#....|#....|#....|#....|#####",
    "M": "#...#|##.##|#.#.#|#...#|#...#|#...#|#...#",
    "N": "#...#|##..#|#.#.#|#..##|#...#|#...#|#...#",
    "O": ".###.|#...#|#...#|#...#|#...#|#...#|.###.",
    "P": "####.|#...#|#...#|####.|#....|#....|#....",
    "Q": ".###.|#...#|#...#|#...#|#.#.#|#..#.|.##.#",
    "R": "####.|#...#|#...#|####.|#.#..|#..#.|#...#",
    "S": ".####|#....|#....|.###.|....#|....#|####.",
    "T": "#####|..#..|..#..|..#..|..#..|..#..|..#..",
    "U": "#...#|#...#|#...#|#...#|#...#|#...#|.###.",
    "V": "#...#|#...#|#...#|#...#|#...#|.#.#.|..#..",
    "W": "#...#|#...#|#...#|#...#|#.#.#|##.##|#...#",
    "X": "#...#|#...#|.#.#.|..#..|.#.#.|#...#|#...#",
    "Y": "#...#|#...#|.#.#.|..#..|..#..|..#..|..#..",
    "Z": "#####|....#|...#.|..#..|.#...|#....|#####",
    "0": ".###.|#...#|#..##|#.#.#|##..#|#...#|.###.",
    "1": "..#..|.##..|..#..|..#..|..#..|..#..|.###.",
    "2": ".###.|#...#|....#|...#.|..#..|.#...|#####",
    "3": "#####|...#.|..##.|....#|....#|#...#|.###.",
    "4": "...#.|..##.|.#.#.|#..#.|#####|...#.|...#.",
    "5": "#####|#....|####.|....#|....#|#...#|.###.",
    "6": "..##.|.#...|#....|####.|#...#|#...#|.###.",
    "7": "#####|....#|...#.|..#..|.#...|.#...|.#...",
    "8": ".###.|#...#|#...#|.###.|#...#|#...#|.###.",
    "9": ".###.|#...#|#...#|.####|....#|...#.|.##..",
    " ": ".....|.....|.....|.....|.....|.....|.....",
    ".": ".....|.....|.....|.....|.....|.....|..#..",
    ",": ".....|.....|.....|.....|.....|..#..|.#...",
    ":": ".....|..#..|.....|.....|.....|..#..|.....",
    "-": ".....|.....|.....|.###.|.....|.....|.....",
    "_": ".....|.....|.....|.....|.....|.....|#####",
    "+": ".....|..#..|..#..|#####|..#..|..#..|.....",
    "/": "....#|....#|...#.|..#..|.#...|#....|#....",
    ">": "#....|.#...|..#..|...#.|..#..|.#...|#....",
    "<": "....#|...#.|..#..|.#...|..#..|...#.|....#",
    "!": "..#..|..#..|..#..|..#..|..#..|.....|..#..",
    "?": ".###.|#...#|....#|...#.|..#..|.....|..#..",
    "(": "...#.|..#..|.#...|.#...|.#...|..#..|...#.",
    ")": ".#...|..#..|...#.|...#.|...#.|..#..|.#...",
    "[": ".###.|.#...|.#...|.#...|.#...|.#...|.###.",
    "]": ".###.|...#.|...#.|...#.|...#.|...#.|.###.",
    "*": ".....|#.#.#|.###.|#####|.###.|#.#.#|.....",
    "=": ".....|.....|#####|.....|#####|.....|.....",
    "%": "#...#|#..#.|...#.|..#..|.#...|.#..#|#...#",
    "@": ".###.|#...#|#.###|#.#.#|#.###|#....|.###.",
    "&": ".##..|#..#.|.##..|.##.#|#..#.|#...#|.##.#",
    "·": ".....|.....|.....|..#..|.....|.....|.....",
    "'": "..#..|..#..|.....|.....|.....|.....|.....",
    "\\": "#....|#....|.#...|..#..|...#.|....#|....#",
}

DOT_ABOVE = ".....|..#..|....."
BREVE_ABOVE = "#...#|.###.|....."
DIAERESIS_ABOVE = "#...#|.....|....."
CEDILLA_BELOW = "..#.."

COMPOSED = {
    "Ş": ("S", None, CEDILLA_BELOW),
    "Ç": ("C", None, CEDILLA_BELOW),
    "İ": ("I", DOT_ABOVE, None),
    "Ğ": ("G", BREVE_ABOVE, None),
    "Ü": ("U", DIAERESIS_ABOVE, None),
    "Ö": ("O", DIAERESIS_ABOVE, None),
}


def _rows(ch):
    ch = ch.upper()
    if ch in COMPOSED:
        base_ch, above, below = COMPOSED[ch]
        base = BASE[base_ch].split("|")
    else:
        base = BASE.get(ch, BASE[" "]).split("|")
        above = below = None
    above_rows = above.split("|") if above else ["....."] * ABOVE_ROWS
    below_rows = below.split("|") if below else ["....."] * BELOW_ROWS
    return base, above_rows, below_rows


def glyph_cells(ch):
    """Yield (col, row) lit cells. row 0 is the top of the BASE box."""
    base, above, below = _rows(ch)
    for i, row in enumerate(above):
        for x, c in enumerate(row):
            if c == "#":
                yield x, i - ABOVE_ROWS
    for i, row in enumerate(base):
        for x, c in enumerate(row):
            if c == "#":
                yield x, i
    for i, row in enumerate(below):
        for x, c in enumerate(row):
            if c == "#":
                yield x, BASE_H + i


def text_width(text, px, tracking=1):
    if not text:
        return 0
    return (len(text) * (GLYPH_W + tracking) - tracking) * px


def advance(px, tracking=1):
    """Horizontal distance from one glyph origin to the next."""
    return (GLYPH_W + tracking) * px


def text_rects(text, x, y, px, fill, tracking=1, opacity=None, extra=""):
    """Render text as merged <rect> runs; (x, y) is the base box top-left."""
    out = []
    attrs = ' fill="%s"' % fill
    if opacity is not None:
        attrs += ' opacity="%s"' % opacity
    if extra:
        attrs += " " + extra
    for idx, ch in enumerate(text):
        ox = x + idx * advance(px, tracking)
        cells = {}
        for cx, cy in glyph_cells(ch):
            cells.setdefault(cy, []).append(cx)
        for row in sorted(cells):
            cols = sorted(cells[row])
            run_start = prev = cols[0]
            for c in cols[1:] + [None]:
                if c is not None and c == prev + 1:
                    prev = c
                    continue
                w = (prev - run_start + 1) * px
                out.append(
                    '<rect x="%g" y="%g" width="%g" height="%g"%s/>'
                    % (ox + run_start * px, y + row * px, w, px, attrs)
                )
                if c is not None:
                    run_start = prev = c
    return "".join(out)


def centered_text(text, cx, y, px, fill, tracking=1, opacity=None, extra=""):
    x = cx - text_width(text, px, tracking) / 2.0
    return text_rects(text, x, y, px, fill, tracking, opacity, extra)
