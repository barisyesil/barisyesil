"""The animated synthwave hero banner (1000x340)."""
import random

import pixelfont as pf
from kit import P, SCAN_DEF, frame, scanlines, svg_open

W, H = 1000, 340
HORIZON = 250
VPX = 500
SUN_R = 78

CSS = """
@keyframes gridrun{0%{transform:translateY(0);opacity:.10}
100%{transform:translateY(78px);opacity:1}}
@keyframes twinkle{0%,100%{opacity:.18}50%{opacity:1}}
@keyframes roll{0%{transform:translateY(-70px)}100%{transform:translateY(370px)}}
@keyframes pulse{0%,100%{opacity:.35}50%{opacity:.8}}
.gl{animation:gridrun 3.2s cubic-bezier(.55,0,1,1) infinite}
.st{animation:twinkle 3s ease-in-out infinite}
.roll{animation:roll 7s linear infinite}
.glow{animation:pulse 4s ease-in-out infinite}
"""


def _defs():
    d = ['<defs>', SCAN_DEF]
    d.append('<linearGradient id="sung" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0%" stop-color="' + P["sun"] + '"/>'
             '<stop offset="45%" stop-color="#ff7a3d"/>'
             '<stop offset="100%" stop-color="' + P["magenta"] + '"/>'
             '</linearGradient>')
    d.append('<linearGradient id="rollg" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0%" stop-color="#fff" stop-opacity="0"/>'
             '<stop offset="50%" stop-color="#fff" stop-opacity="0.055"/>'
             '<stop offset="100%" stop-color="#fff" stop-opacity="0"/>'
             '</linearGradient>')
    d.append('<radialGradient id="haze" cx="50%" cy="65%" r="46%">'
             '<stop offset="0%" stop-color="' + P["magenta"] +
             '" stop-opacity="0.5"/>'
             '<stop offset="100%" stop-color="' + P["magenta"] +
             '" stop-opacity="0"/></radialGradient>')
    d.append('<clipPath id="floor"><rect x="12" y="%d" width="%d" height="%d"/>'
             '</clipPath>' % (HORIZON, W - 24, H - HORIZON - 12))
    d.append('<clipPath id="sky"><rect x="12" y="12" width="%d" height="%d"/>'
             '</clipPath>' % (W - 24, HORIZON - 12))
    d.append('</defs>')
    return "".join(d)


def _sky():
    s = ['<g clip-path="url(#sky)">']
    rnd = random.Random(1987)
    for _ in range(90):
        x = rnd.randrange(14, W - 16, 2)
        y = rnd.randrange(14, HORIZON - 24, 2)
        size = 2 if rnd.random() < 0.78 else 3
        col = P["bone"] if rnd.random() < 0.7 else P["cyan"]
        dur = 2.2 + rnd.random() * 3.4
        s.append('<rect class="st" x="%d" y="%d" width="%d" height="%d" '
                 'fill="%s" style="animation-duration:%.2fs;'
                 'animation-delay:-%.2fs"/>'
                 % (x, y, size, size, col, dur, rnd.random() * dur))
    s.append('<rect x="12" y="12" width="%d" height="%d" fill="url(#haze)"/>'
             % (W - 24, HORIZON - 12))

    # banded sun
    cy = HORIZON - 4
    s.append('<circle cx="%d" cy="%d" r="%d" fill="url(#sung)"/>'
             % (VPX, cy, SUN_R))
    band_y, gap, thick = cy - 6.0, 5.0, 2.0
    while band_y < cy + SUN_R:
        s.append('<rect x="%d" y="%g" width="%d" height="%g" fill="%s"/>'
                 % (VPX - SUN_R - 2, band_y, 2 * SUN_R + 4, thick, P["void"]))
        band_y += thick + gap
        thick += 1.5
        gap = max(3.0, gap - 0.3)

    # pixel skyline
    rnd2 = random.Random(7)
    x = 14
    while x < W - 14:
        bw = rnd2.choice([18, 22, 26, 30, 34])
        bh = rnd2.choice([16, 24, 30, 38, 46, 54])
        if abs((x + bw / 2.0) - VPX) < SUN_R - 4:
            bh = min(bh, 18)
        top = HORIZON - bh
        s.append('<rect x="%d" y="%d" width="%d" height="%d" fill="#1b0c33"/>'
                 % (x, top, bw, bh))
        s.append('<rect x="%d" y="%d" width="%d" height="2" fill="%s" '
                 'opacity="0.85"/>' % (x, top, bw, P["purple"]))
        for wy in range(top + 6, HORIZON - 4, 8):
            for wx in range(x + 4, x + bw - 4, 8):
                if rnd2.random() < 0.42:
                    wc = P["cyan"] if rnd2.random() < 0.5 else P["sun"]
                    s.append('<rect x="%d" y="%d" width="3" height="3" '
                             'fill="%s" opacity="0.9"/>' % (wx, wy, wc))
        x += bw + rnd2.choice([2, 4, 6])
    s.append('</g>')
    return "".join(s)


def _floor():
    s = ['<g clip-path="url(#floor)">']
    s.append('<rect x="12" y="%d" width="%d" height="%d" fill="#12042b"/>'
             % (HORIZON, W - 24, H - HORIZON - 12))
    for k in range(-11, 12):
        s.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" '
                 'stroke-width="1.6" opacity="0.7"/>'
                 % (VPX, HORIZON, VPX + k * 105, H, P["grid"]))
    n = 9
    for i in range(n):
        s.append('<rect class="gl" x="12" y="%d" width="%d" height="2" '
                 'fill="%s" style="animation-delay:-%.3fs"/>'
                 % (HORIZON, W - 24, P["magenta"], 3.2 * i / float(n)))
    s.append('</g>')
    return "".join(s)


PHRASES = ["AI / ML ENGINEER", "RAG ARCHITECT",
           "NLP DEVELOPER", "FULL-STACK BUILDER"]
SLOT = 4.5
TYPE_D, HOLD_D, ERASE_D = 1.5, 1.6, 0.7


def _events(n, t0):
    """(time, visible_char_count) key points for one phrase's slot."""
    ev = [(t0, 0)]
    for k in range(1, n + 1):
        ev.append((t0 + TYPE_D * k / n, k))
    ev.append((t0 + TYPE_D + HOLD_D, n))
    for k in range(n - 1, -1, -1):
        ev.append((t0 + TYPE_D + HOLD_D + ERASE_D * (n - k) / n, k))
    ev.append((t0 + SLOT, 0))
    return ev


def _smil(pairs, total, scale, base=0.0):
    """Turn (time, count) pairs into strictly-increasing keyTimes/values."""
    keys, vals = [], []
    for t, c in pairs:
        k = min(1.0, max(0.0, t / total))
        if keys and k <= keys[-1]:
            k = min(1.0, keys[-1] + 1e-6)
        if keys and k <= keys[-1]:
            continue
        keys.append(k)
        vals.append(base + c * scale)
    if not keys or keys[0] > 0.0:
        keys.insert(0, 0.0)
        vals.insert(0, base)
    return (";".join("%.6f" % k for k in keys),
            ";".join("%g" % v for v in vals))


def _typewriter():
    total = SLOT * len(PHRASES)
    px = 4
    adv = pf.advance(px)
    prompt = "> "
    span = (len(prompt) + max(len(p) for p in PHRASES)) * adv - px
    x0 = VPX - span / 2.0
    tx0 = x0 + len(prompt) * adv
    y = 134

    s = [pf.text_rects(prompt, x0, y, px, P["magenta"])]
    cursor = []
    for i, ph in enumerate(PHRASES):
        ev = _events(len(ph), i * SLOT)
        # the clip is closed outside this phrase's own slot
        pairs = [(0.0, 0)] + ev + [(total, 0)]
        keys, vals = _smil(pairs, total, adv)
        s.append('<clipPath id="tw%d"><rect x="%g" y="%d" width="0" '
                 'height="%d"><animate attributeName="width" '
                 'calcMode="discrete" dur="%gs" repeatCount="indefinite" '
                 'keyTimes="%s" values="%s"/></rect></clipPath>'
                 % (i, tx0, y - 10, pf.BASE_H * px + 20, total, keys, vals))
        s.append('<g clip-path="url(#tw%d)">%s</g>'
                 % (i, pf.text_rects(ph, tx0, y, px, P["sun"])))
        cursor.extend(ev)

    ck, cv = _smil(sorted(cursor), total, adv, base=tx0)
    s.append('<rect y="%d" width="%d" height="%d" fill="%s">'
             '<animate attributeName="x" calcMode="discrete" dur="%gs" '
             'repeatCount="indefinite" keyTimes="%s" values="%s"/>'
             '<animate attributeName="opacity" calcMode="discrete" dur="1s" '
             'repeatCount="indefinite" keyTimes="0;0.5" values="1;0.15"/>'
             '</rect>'
             % (y, px, pf.BASE_H * px, P["cyan"], total, ck, cv))
    return "".join(s)


def build():
    name = "BARIŞ YEŞİLDAĞ"
    px = 9
    nx = (W - pf.text_width(name, px)) / 2.0
    ny = 64

    s = [svg_open(W, H, "Baris Yesildag - AI, ML and Full-Stack Engineer")]
    s.append('<title>Barış Yeşildağ — AI / ML and Full-Stack Engineer</title>')
    s.append(_defs())
    s.append('<style>%s</style>' % CSS)
    s.append('<rect width="%d" height="%d" fill="%s"/>' % (W, H, P["void"]))
    s.append(_sky())
    s.append('<rect class="glow" x="12" y="%d" width="%d" height="3" '
             'fill="%s"/>' % (HORIZON - 1, W - 24, P["cyan"]))
    s.append(_floor())
    s.append(pf.centered_text("// SYSTEM ONLINE", VPX, 26, 3, P["cyan"],
                              opacity="0.9"))
    s.append(pf.text_rects(name, nx - 3, ny, px, P["magenta"], opacity="0.8"))
    s.append(pf.text_rects(name, nx + 3, ny, px, P["cyan"], opacity="0.8"))
    s.append(pf.text_rects(name, nx, ny, px, P["bone"]))
    s.append(_typewriter())
    s.append('<rect class="roll" x="0" y="0" width="%d" height="70" '
             'fill="url(#rollg)"/>' % W)
    s.append(scanlines(W, H))
    s.append(frame(W, H))
    s.append('</svg>')
    return "".join(s)
