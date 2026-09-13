"""Section plates, dividers, the CRT placeholder card and the footer."""
import random

import pixelfont as pf
from kit import P, SCAN_DEF, bitmap, frame, scanlines, svg_open

# 16x16 sprites. Keys: b=body/purple  c=cyan  m=magenta  w=bone  s=sun
ICONS = {
    "floppy": [
        "................",
        ".bbbbbbbbbbbbbb.",
        ".b....cccc....b.",
        ".b....cccc....b.",
        ".b....cccc....b.",
        ".b....cccc....b.",
        ".b............b.",
        ".b............b.",
        ".b.wwwwwwwwww.b.",
        ".b.w........w.b.",
        ".b.w..mmmm..w.b.",
        ".b.w..mmmm..w.b.",
        ".b.w........w.b.",
        ".b.wwwwwwwwww.b.",
        ".bbbbbbbbbbbbbb.",
        "................",
    ],
    "chip": [
        "................",
        "...c..c..c..c...",
        "...c..c..c..c...",
        ".bbbbbbbbbbbbbb.",
        ".b............b.",
        ".b.mmmmmmmmmm.b.",
        ".b.m........m.b.",
        ".b.m..wwww..m.b.",
        ".b.m..wwww..m.b.",
        ".b.m........m.b.",
        ".b.mmmmmmmmmm.b.",
        ".b............b.",
        ".bbbbbbbbbbbbbb.",
        "...c..c..c..c...",
        "...c..c..c..c...",
        "................",
    ],
    "pad": [
        "................",
        "................",
        "..bbbbbbbbbbbb..",
        ".bbbbbbbbbbbbbb.",
        ".bbbbwbbbbbmbbb.",
        ".bbbwwwbbbmbmbb.",
        ".bbbbwbbbbbmbbb.",
        ".bbbbbbbbbbbbbb.",
        ".bbbbbbbbbbbbbb.",
        "..bbbb....bbbb..",
        "...bb......bb...",
        "................",
        "................",
        "................",
        "................",
        "................",
    ],
    "crt": [
        "................",
        ".bbbbbbbbbbbbbb.",
        ".b............b.",
        ".b.wwwwwwwwww.b.",
        ".b.w........w.b.",
        ".b.w.....c..w.b.",
        ".b.w..m..c..w.b.",
        ".b.w..m.cc..w.b.",
        ".b.w.mm.cc..w.b.",
        ".b.wwwwwwwwww.b.",
        ".b............b.",
        ".bbbbbbbbbbbbbb.",
        ".....bbbbbb.....",
        "....bbbbbbbb....",
        "................",
        "................",
    ],
    "mail": [
        "................",
        "................",
        ".cccccccccccccc.",
        ".cwwwwwwwwwwwwc.",
        ".cww........wwc.",
        ".c.ww......ww.c.",
        ".c..ww....ww..c.",
        ".c...ww..ww...c.",
        ".c....wwww....c.",
        ".c............c.",
        ".c............c.",
        ".cccccccccccccc.",
        "................",
        "................",
        "................",
        "................",
    ],
}

ICON_COLORS = {
    "b": P["purple"], "c": P["cyan"], "m": P["magenta"],
    "w": P["bone"], "s": P["sun"],
}


def plate(title, icon, out_name):
    """A section header plaque: pixel icon + title in a bordered panel."""
    ipx, tpx = 3, 4
    icon_w = 16 * ipx
    pad, gap = 20, 16
    tw = pf.text_width(title, tpx)
    H = 64
    W = int(pad + icon_w + gap + tw + pad)

    s = [svg_open(W, H, title)]
    s.append('<title>%s</title>' % title)
    s.append('<defs>%s</defs>' % SCAN_DEF)
    s.append('<rect width="%d" height="%d" fill="%s"/>' % (W, H, P["panel"]))
    # faint grid texture inside the plate
    for gx in range(0, W, 8):
        s.append('<rect x="%d" y="0" width="1" height="%d" fill="%s" '
                 'opacity="0.25"/>' % (gx, H, P["grid"]))
    s.append(bitmap(ICONS[icon], pad, (H - icon_w) / 2.0, ipx, ICON_COLORS))
    ty = (H - pf.BASE_H * tpx) / 2.0
    s.append(pf.text_rects(title, pad + icon_w + gap, ty + 2, tpx,
                           P["magenta"], opacity="0.75"))
    s.append(pf.text_rects(title, pad + icon_w + gap, ty, tpx, P["bone"]))
    s.append(scanlines(W, H, 0.22))
    s.append(frame(W, H))
    s.append('</svg>')
    return out_name, "".join(s)


def divider():
    """A dithered magenta-to-cyan ramp. Transparent background on purpose:
    it sits between sections and must read on light and dark alike."""
    W, H = 1000, 22
    blk = 8
    n = W // blk
    rnd = random.Random(42)

    def lerp(a, b, t):
        return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))

    def hx(c):
        return "#%02x%02x%02x" % c

    mg = (0xFF, 0x2E, 0x97)
    pu = (0xA4, 0x5C, 0xFF)
    cy = (0x00, 0xE5, 0xFF)
    s = [svg_open(W, H, "section divider")]
    for i in range(n):
        t = i / float(n - 1)
        col = lerp(mg, pu, t * 2) if t < 0.5 else lerp(pu, cy, (t - 0.5) * 2)
        # taper the ends and dither the body so it reads as pixels, not a gradient
        edge = min(i, n - 1 - i) / (n * 0.18)
        h = blk if edge >= 1 else max(2, int(blk * max(edge, 0.25)))
        y = (H - h) / 2.0
        op = 1.0 if rnd.random() > 0.22 else 0.45
        s.append('<rect x="%d" y="%g" width="%d" height="%d" fill="%s" '
                 'opacity="%.2f"/>' % (i * blk, y, blk - 1, h, hx(col), op))
    # centre diamond marker
    cx = W // 2
    for k, half in enumerate((2, 4, 6, 4, 2)):
        s.append('<rect x="%d" y="%d" width="%d" height="3" fill="%s"/>'
                 % (cx - half, 4 + k * 3, half * 2, P["bone"]))
    s.append('</svg>')
    return "divider.svg", "".join(s)


def placeholder():
    """Stand-in card for a project that has no screenshot yet."""
    W, H = 800, 450
    bars = [P["bone"], P["sun"], P["cyan"], "#3ddc84",
            P["magenta"], "#ff5555", P["purple"]]
    s = [svg_open(W, H, "No screenshot yet")]
    s.append('<title>No screenshot yet — drop a PNG or GIF in assets/projects/'
             '</title>')
    s.append('<defs>%s' % SCAN_DEF)
    s.append('<clipPath id="pc"><rect x="12" y="12" width="%d" height="%d"/>'
             '</clipPath></defs>' % (W - 24, H - 24))
    s.append('<style>@keyframes bl{0%,49%{opacity:1}50%,100%{opacity:.12}}'
             '.bl{animation:bl 1.1s steps(1) infinite}'
             '@keyframes sl{0%{transform:translateY(-40px)}'
             '100%{transform:translateY(470px)}}'
             '.sl{animation:sl 5s linear infinite}</style>')
    s.append('<rect width="%d" height="%d" fill="%s"/>' % (W, H, P["void"]))
    s.append('<g clip-path="url(#pc)">')
    bw = (W - 24) / float(len(bars))
    for i, c in enumerate(bars):
        s.append('<rect x="%g" y="12" width="%g" height="180" fill="%s" '
                 'opacity="0.75"/>' % (12 + i * bw, bw, c))
    s.append('<rect x="12" y="192" width="%d" height="%d" fill="#12042b"/>'
             % (W - 24, H - 204))
    rnd = random.Random(3)
    for _ in range(240):
        x = rnd.randrange(14, W - 16, 2)
        y = rnd.randrange(196, H - 16, 2)
        s.append('<rect x="%d" y="%d" width="%d" height="2" fill="%s" '
                 'opacity="%.2f"/>'
                 % (x, y, rnd.choice([2, 4, 6]), P["muted"],
                    0.10 + rnd.random() * 0.30))
    s.append(pf.centered_text("NO SIGNAL", W / 2.0, 240, 8, P["bone"],
                              extra='class="bl"'))
    s.append(pf.centered_text("DROP A SCREENSHOT OR GIF IN", W / 2.0, 320, 3,
                              P["muted"]))
    s.append(pf.centered_text("ASSETS/PROJECTS/", W / 2.0, 348, 3, P["cyan"]))
    s.append('<rect class="sl" x="12" y="0" width="%d" height="40" '
             'fill="#ffffff" opacity="0.04"/>' % (W - 24))
    s.append('</g>')
    s.append(scanlines(W, H, 0.35))
    s.append(frame(W, H))
    s.append('</svg>')
    return "projects/_placeholder.svg", "".join(s)


def footer():
    W, H = 1000, 150
    HZ = 54
    s = [svg_open(W, H, "Thanks for playing")]
    s.append('<title>Thanks for playing — insert coin to continue</title>')
    s.append('<defs>%s' % SCAN_DEF)
    s.append('<clipPath id="ff"><rect x="12" y="%d" width="%d" height="%d"/>'
             '</clipPath>' % (HZ, W - 24, H - HZ - 12))
    s.append('<linearGradient id="fg" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0%" stop-color="' + P["magenta"] +
             '" stop-opacity="0.35"/>'
             '<stop offset="100%" stop-color="' + P["magenta"] +
             '" stop-opacity="0"/></linearGradient></defs>')
    run = H - HZ - 12
    s.append('<style>'
             '@keyframes gr{0%{transform:translateY(0);opacity:.1}'
             '100%{transform:translateY(' + str(run) + 'px);opacity:1}}'
             '.g{animation:gr 3.4s cubic-bezier(.55,0,1,1) infinite}'
             '@keyframes bl{0%,49%{opacity:1}50%,100%{opacity:.15}}'
             '.bl{animation:bl 1.2s steps(1) infinite}'
             '</style>')
    s.append('<rect width="%d" height="%d" fill="%s"/>' % (W, H, P["void"]))
    s.append('<rect x="12" y="12" width="%d" height="%d" fill="url(#fg)"/>'
             % (W - 24, HZ - 12))
    s.append(pf.centered_text("THANKS FOR PLAYING", W / 2.0, 20, 4, P["bone"]))
    s.append('<g clip-path="url(#ff)">')
    s.append('<rect x="12" y="%d" width="%d" height="%d" fill="#12042b"/>'
             % (HZ, W - 24, H - HZ - 12))
    for k in range(-9, 10):
        s.append('<line x1="500" y1="%d" x2="%d" y2="%d" stroke="%s" '
                 'stroke-width="1.5" opacity="0.7"/>'
                 % (HZ, 500 + k * 120, H, P["grid"]))
    for i in range(7):
        s.append('<rect class="g" x="12" y="%d" width="%d" height="2" '
                 'fill="%s" style="animation-delay:-%.3fs"/>'
                 % (HZ, W - 24, P["cyan"], 3.4 * i / 7.0))
    s.append('</g>')
    s.append('<rect x="12" y="%d" width="%d" height="2" fill="%s" '
             'opacity="0.9"/>' % (HZ - 1, W - 24, P["magenta"]))
    s.append(pf.centered_text("INSERT COIN TO CONTINUE", W / 2.0, 104, 3,
                              P["sun"], extra='class="bl"'))
    s.append(scanlines(W, H, 0.28))
    s.append(frame(W, H))
    s.append('</svg>')
    return "footer.svg", "".join(s)


PLATES = [
    ("ABOUT ME", "floppy", "sec-about.svg"),
    ("TECH STACK", "chip", "sec-stack.svg"),
    ("FEATURED PROJECTS", "pad", "sec-projects.svg"),
    ("GITHUB STATS", "crt", "sec-stats.svg"),
    ("GET IN TOUCH", "mail", "sec-contact.svg"),
]


def all_parts():
    out = [plate(t, i, n) for t, i, n in PLATES]
    out.append(divider())
    out.append(placeholder())
    out.append(footer())
    return out


def tag(label, out_name):
    """Small category label used down the left of the tech-stack table."""
    tpx = 3
    pad = 14
    pre = ">>"
    prew = pf.text_width(pre, tpx) + 8
    tw = pf.text_width(label, tpx)
    H = 36
    W = int(pad + prew + tw + pad)
    ty = (H - pf.BASE_H * tpx) / 2.0

    s = [svg_open(W, H, label)]
    s.append('<title>%s</title>' % label.replace("&", "&amp;"))
    s.append('<rect width="%d" height="%d" fill="%s"/>' % (W, H, P["panel"]))
    s.append('<rect x="1" y="1" width="%d" height="%d" fill="none" '
             'stroke="%s" stroke-width="2"/>' % (W - 2, H - 2, P["magenta"]))
    s.append(pf.text_rects(pre, pad, ty, tpx, P["cyan"]))
    s.append(pf.text_rects(label, pad + prew, ty, tpx, P["bone"]))
    s.append('</svg>')
    return out_name, "".join(s)


TAGS = [
    ("FRONTEND", "tag-frontend.svg"),
    ("BACKEND", "tag-backend.svg"),
    ("MOBILE", "tag-mobile.svg"),
    ("AI / ML", "tag-ai.svg"),
    ("TOOLS", "tag-tools.svg"),
]


def all_tags():
    return [tag(t, n) for t, n in TAGS]
