"""Shared palette, SVG helpers and chrome for the generated pixel-art assets."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pixelfont as pf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets")

# ---------------------------------------------------------------- palette --
# Change these nine values and re-run tools/gen_assets.py to re-skin every
# asset at once. The same hexes are pasted into the stat-card URLs in README.md.
P = {
    "void":    "#0d0221",
    "panel":   "#1a0b2e",
    "grid":    "#3d2a63",
    "magenta": "#ff2e97",
    "cyan":    "#00e5ff",
    "purple":  "#a45cff",
    "sun":     "#ffcc00",
    "bone":    "#e8e3ff",
    "muted":   "#7a6ba3",
}

SCAN_DEF = ('<pattern id="scan" width="1" height="3" '
            'patternUnits="userSpaceOnUse">'
            '<rect width="1" height="1" fill="#000"/></pattern>')


def svg_open(w, h, label):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
            'viewBox="0 0 %d %d" role="img" aria-label="%s">'
            % (w, h, w, h, label))


def write(name, body):
    path = os.path.join(OUT, name)
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(body)
    print("  %-30s %6.1f KB" % (name, len(body.encode("utf-8")) / 1024.0))


def scanlines(w, h, opacity=0.30):
    return ('<rect width="%d" height="%d" fill="url(#scan)" opacity="%s"/>'
            % (w, h, opacity))


def frame(w, h, stroke=None, corner=None, bg=None):
    """Inset double border with chunky pixel corner blocks."""
    stroke = stroke or P["magenta"]
    corner = corner or P["cyan"]
    out = []
    if bg:
        out.append('<rect width="%d" height="%d" fill="%s"/>' % (w, h, bg))
    out.append('<rect x="3.5" y="3.5" width="%g" height="%g" fill="none" '
               'stroke="%s" stroke-width="3"/>' % (w - 7, h - 7, stroke))
    out.append('<rect x="10.5" y="10.5" width="%g" height="%g" fill="none" '
               'stroke="%s" stroke-width="1" opacity="0.5"/>'
               % (w - 21, h - 21, P["purple"]))
    for cx, cy in ((0, 0), (w - 14, 0), (0, h - 14), (w - 14, h - 14)):
        out.append('<rect x="%g" y="%g" width="14" height="14" fill="%s"/>'
                   % (cx, cy, P["void"]))
        out.append('<rect x="%g" y="%g" width="8" height="8" fill="%s"/>'
                   % (cx + 3, cy + 3, corner))
    return "".join(out)


def bitmap(art, x, y, px, colors):
    """Draw a small sprite from an ASCII map.

    `art` is a list of equal-length strings; every character other than a space
    or '.' is looked up in the `colors` dict to get its fill. Horizontal runs of
    the same key merge into one rect.
    """
    out = []
    for row, line in enumerate(art):
        col = 0
        while col < len(line):
            key = line[col]
            if key in (" ", "."):
                col += 1
                continue
            run = 1
            while col + run < len(line) and line[col + run] == key:
                run += 1
            fill = colors.get(key)
            if fill:
                out.append('<rect x="%g" y="%g" width="%g" height="%g" '
                           'fill="%s"/>'
                           % (x + col * px, y + row * px, run * px, px, fill))
            col += run
    return "".join(out)
