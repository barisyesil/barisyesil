"""The About-section desk vignette: CRT, acoustic guitar, synth, coffee."""
import random

import pixelfont as pf
from kit import P, SCAN_DEF, bitmap, frame, scanlines, svg_open

PX = 4
CW, CH = 96, 67           # cells
W, H = CW * PX, CH * PX   # 384 x 268

WOOD = "#c98b3f"
WOOD_D = "#8a5a24"
DESK = "#4a2d7a"
DESK_D = "#2f1b52"
INK = "#0a0118"

C = {
    "n": WOOD, "N": WOOD_D, "#": INK, "w": P["bone"], "c": P["cyan"],
    "m": P["magenta"], "s": P["sun"], "b": P["purple"], "k": P["panel"],
    "d": DESK, "D": DESK_D, "g": P["grid"],
}

GUITAR = [
    "......nn........",
    ".....nnnn.......",
    ".....n##n.......",
    ".....nnnn.......",
    "......nn........",
    "......nn........",
    "......nn........",
    "......ww........",
    "......nn........",
    "......nn........",
    "......ww........",
    "......nn........",
    "......nn........",
    "......ww........",
    "......nn........",
    "......nn........",
    ".....nnnn.......",
    "....nnnnnn......",
    "...nnnnnnnn.....",
    "..nnnnnnnnnn....",
    "..nnnnnnnnnn....",
    ".nnnnnnnnnnnn...",
    ".nnnn####nnnn...",
    ".nnn######nnn...",
    ".nnn######nnn...",
    ".nnnn####nnnn...",
    ".nnnnnnnnnnnn...",
    "..nnnnnnnnnn....",
    "..nnnnnnnnnn....",
    "..nnnnnnnnnn....",
    ".nnnnn##nnnnn...",
    "nnnnnnnnnnnnnn..",
    "nnnnnnnnnnnnnn..",
    "nnnnnnnnnnnnnn..",
    "nnnnnnnnnnnnnn..",
    "nnnnnnnnnnnnnn..",
    ".nnnnnnnnnnnn...",
    "..nnnnnnnnnn....",
    "...nnnnnnnn.....",
    "....nnnnnn......",
    ".....nnnn.......",
]

SYNTH = [
    "kkkkkkkkkkkkkkkkkkkkkkkkkkkkkk",
    "k.c...m...c...m...c...m...c..k",
    "kwwwwwwwwwwwwwwwwwwwwwwwwwwwwk",
    "kw#w#ww#w#w#ww#w#ww#w#w#ww#w#k",
    "kwwwwwwwwwwwwwwwwwwwwwwwwwwwwk",
    "kwwwwwwwwwwwwwwwwwwwwwwwwwwwwk",
    "kkkkkkkkkkkkkkkkkkkkkkkkkkkkkk",
]

MUG = [
    "wwwwwww.",
    "w#####ww",
    "w#sss#.w",
    "w#sss#ww",
    "w#####w.",
    "wwwwwww.",
    ".wwwww..",
]

CASSETTE = [
    "mmmmmmmmmmmm",
    "m..........m",
    "m.wwwwwwww.m",
    "m.w.k..k.w.m",
    "m.w.k..k.w.m",
    "m.wwwwwwww.m",
    "m..........m",
    "mmmmmmmmmmmm",
]


def _at(art, col, row, colors=None, px=None):
    px = px or PX
    return bitmap(art, col * PX, row * PX, px, colors or C)


def _at_px(art, x, y, px):
    return bitmap(art, x, y, px, C)


def _monitor(col, row):
    """CRT with code scrolling behind the glass."""
    w, h = 40, 30
    x, y = col * PX, row * PX
    ww, hh = w * PX, h * PX
    s = []
    s.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>'
             % (x, y, ww, hh, P["purple"]))
    s.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>'
             % (x + PX, y + PX, ww - 2 * PX, hh - 2 * PX, INK))
    sx, sy = x + 3 * PX, y + 3 * PX
    sw, sh = ww - 6 * PX, hh - 6 * PX
    s.append('<clipPath id="scr"><rect x="%d" y="%d" width="%d" height="%d"/>'
             '</clipPath>' % (sx, sy, sw, sh))
    s.append('<rect x="%d" y="%d" width="%d" height="%d" fill="#06010f"/>'
             % (sx, sy, sw, sh))
    # scrolling "code": two stacked copies of the same block so the loop seams
    rnd = random.Random(11)
    rows = []
    block_h = sh
    yy = 0
    while yy < block_h:
        indent = rnd.choice([0, 0, 1, 1, 2, 3])
        segs, cx = [], indent * PX
        for _ in range(rnd.randint(1, 3)):
            wseg = rnd.randint(2, 8) * PX
            if cx + wseg > sw - PX:
                break
            col_ = rnd.choice([P["cyan"], P["magenta"], P["sun"],
                               P["bone"], P["muted"]])
            segs.append((cx, wseg, col_))
            cx += wseg + PX
        rows.append((yy, segs))
        yy += 2 * PX
    body = []
    for rep in (0, 1):
        for yy, segs in rows:
            for cx, wseg, col_ in segs:
                body.append('<rect x="%d" y="%d" width="%d" height="%d" '
                            'fill="%s" opacity="0.9"/>'
                            % (sx + cx, sy + yy + rep * block_h, wseg, PX,
                               col_))
    s.append('<g clip-path="url(#scr)"><g class="code">%s</g>'
             '<rect class="glare" x="%d" y="%d" width="%d" height="%d" '
             'fill="#ffffff" opacity="0.05"/></g>'
             % ("".join(body), sx, sy, sw, 6 * PX))
    s.append('<rect x="%d" y="%d" width="%d" height="%d" fill="url(#scan)" '
             'opacity="0.5"/>' % (sx, sy, sw, sh))
    # power LED, stand and base
    s.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s" '
             'class="led"/>' % (x + ww - 3 * PX, y + hh - 2 * PX, PX, PX,
                                P["cyan"]))
    s.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>'
             % (x + ww / 2 - 4 * PX, y + hh, 8 * PX, 3 * PX, DESK_D))
    s.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>'
             % (x + ww / 2 - 8 * PX, y + hh + 3 * PX, 16 * PX, 2 * PX, DESK))
    return "".join(s)


CSS = """
@keyframes scrollcode{0%{transform:translateY(0)}
100%{transform:translateY(-96px)}}
@keyframes glare{0%{transform:translateY(-30px);opacity:0}
40%{opacity:.07}100%{transform:translateY(110px);opacity:0}}
@keyframes led{0%,100%{opacity:1}50%{opacity:.25}}
@keyframes steam{0%{transform:translateY(0);opacity:0}
25%{opacity:.55}100%{transform:translateY(-26px);opacity:0}}
@keyframes keylit{0%,100%{opacity:.25}50%{opacity:1}}
@keyframes sunrise{0%,100%{opacity:.75}50%{opacity:1}}
.code{animation:scrollcode 9s linear infinite}
.glare{animation:glare 6s ease-in-out infinite}
.led{animation:led 2.4s steps(1) infinite}
.steam{animation:steam 3.6s ease-out infinite}
.kl{animation:keylit 2s ease-in-out infinite}
.poster{animation:sunrise 5s ease-in-out infinite}
"""


def _poster(col, row):
    """Small synthwave poster pinned to the wall."""
    w, h = 20, 17
    x, y = col * PX, row * PX
    ww, hh = w * PX, h * PX
    s = ['<g class="poster">']
    s.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>'
             % (x, y, ww, hh, P["magenta"]))
    s.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>'
             % (x + PX, y + PX, ww - 2 * PX, hh - 2 * PX, "#1b0c33"))
    cx, cy, r = x + ww / 2, y + hh * 0.60, 5 * PX
    s.append('<clipPath id="po"><rect x="%d" y="%d" width="%d" height="%d"/>'
             '</clipPath>' % (x + PX, y + PX, ww - 2 * PX, hh - 2 * PX))
    s.append('<g clip-path="url(#po)">')
    s.append('<circle cx="%g" cy="%g" r="%g" fill="%s"/>'
             % (cx, cy, r, P["sun"]))
    for i in range(3):
        s.append('<rect x="%g" y="%g" width="%g" height="%g" fill="#1b0c33"/>'
                 % (cx - r, cy + i * 2.2 * PX - PX, 2 * r, PX * 0.9))
    s.append('<rect x="%d" y="%g" width="%d" height="%d" fill="%s"/>'
             % (x + PX, cy + r * 0.55, ww - 2 * PX,
                int(y + hh - PX - (cy + r * 0.55)), "#12042b"))
    for k in range(4):
        s.append('<rect x="%d" y="%g" width="%d" height="1.5" fill="%s" '
                 'opacity="0.8"/>'
                 % (x + PX, cy + r * 0.55 + 3 + k * (3 + k * 1.6),
                    ww - 2 * PX, P["cyan"]))
    s.append('</g></g>')
    return "".join(s)


def build():
    FLOOR = 60 * PX          # y of the floor line
    DESKTOP = 45 * PX        # y of the desk surface

    s = [svg_open(W, H, "A desk with a CRT, an acoustic guitar and a synth")]
    s.append('<title>Where the work happens: a CRT, an acoustic guitar, '
             'a synth and cold coffee</title>')
    s.append('<defs>%s' % SCAN_DEF)
    s.append('<radialGradient id="mglow" cx="50%" cy="50%" r="50%">'
             '<stop offset="0%" stop-color="' + P["cyan"] +
             '" stop-opacity="0.16"/>'
             '<stop offset="100%" stop-color="' + P["cyan"] +
             '" stop-opacity="0"/></radialGradient></defs>')
    s.append('<style>%s</style>' % CSS)
    s.append('<rect width="%d" height="%d" fill="%s"/>' % (W, H, P["void"]))

    # wall grid, then floor
    for gx in range(0, W, 6 * PX):
        s.append('<rect x="%d" y="0" width="1" height="%d" fill="%s" '
                 'opacity="0.30"/>' % (gx, FLOOR, P["grid"]))
    for gy in range(0, FLOOR, 6 * PX):
        s.append('<rect x="0" y="%d" width="%d" height="1" fill="%s" '
                 'opacity="0.30"/>' % (gy, W, P["grid"]))
    s.append('<rect x="0" y="%d" width="%d" height="%d" fill="#100626"/>'
             % (FLOOR, W, H - FLOOR))
    s.append('<rect x="0" y="%d" width="%d" height="%d" fill="%s" '
             'opacity="0.9"/>' % (FLOOR, W, PX, P["purple"]))

    s.append(_poster(68, 4))
    s.append('<rect x="%d" y="%d" width="%d" height="%d" fill="url(#mglow)"/>'
             % (16 * PX, 4 * PX, 56 * PX, 44 * PX))
    s.append(_monitor(23, 10))

    # desk slab + legs
    s.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>'
             % (22 * PX, DESKTOP, W - 22 * PX, 3 * PX, DESK))
    s.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>'
             % (22 * PX, DESKTOP + 3 * PX, W - 22 * PX, PX, DESK_D))
    s.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>'
             % (26 * PX, DESKTOP + 4 * PX, 3 * PX, FLOOR - DESKTOP - 4 * PX,
                DESK_D))
    s.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>'
             % (W - 9 * PX, DESKTOP + 4 * PX, 3 * PX,
                FLOOR - DESKTOP - 4 * PX, DESK_D))

    s.append(_at(CASSETTE, 74, 37))
    s.append(_at(MUG, 66, 38))
    for i, dx in enumerate((67.5, 69, 70.5)):
        s.append('<rect class="steam" x="%g" y="%d" width="%d" height="%d" '
                 'fill="%s" opacity="0" style="animation-delay:-%.1fs"/>'
                 % (dx * PX, 35 * PX, PX, 2 * PX, P["bone"], i * 1.2))

    s.append(_at(SYNTH, 26, 38))
    for i, cx in enumerate((30, 37, 45, 52)):
        s.append('<rect class="kl" x="%d" y="%d" width="%d" height="%d" '
                 'fill="%s" style="animation-delay:-%.1fs"/>'
                 % (cx * PX, 41 * PX, PX, 2 * PX,
                    P["cyan"] if i % 2 else P["magenta"], i * 0.7))

    # the guitar gets its own, larger pixel size: it is the point of the scene
    gpx = 5
    s.append(_at_px(GUITAR, 6, FLOOR - len(GUITAR) * gpx, gpx))

    s.append(scanlines(W, H, 0.22))
    s.append(frame(W, H))
    s.append('</svg>')
    return "desk-scene.svg", "".join(s)
