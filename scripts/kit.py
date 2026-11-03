"""Design system for the profile graphics: spec-sheet frames, embedded Geist, one accent colour."""
import base64
import html
import io
import math
import random
import re
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
FONTS = Path(__file__).resolve().parent / "fonts"

THEMES = {
    # bg matches GitHub's page colour; it is only used for knockouts, the SVGs themselves are transparent
    "light": dict(bg="#FFFFFF", ink="#111111", muted="#6E6E6E", line="#D6D6D3", faint="#E9E9E6",
                  accent="#2B47F0", on_accent="#FFFFFF"),
    "dark": dict(bg="#0D1117", ink="#E6EDF3", muted="#8B949E", line="#30363D", faint="#1C2128",
                 accent="#7385FF", on_accent="#0D1117"),
}

FACES = [("G", 400, "geist-400"), ("G", 500, "geist-500"), ("G", 600, "geist-600"),
         ("GM", 400, "geist-mono-400"), ("GM", 500, "geist-mono-500")]


def esc(s):
    return html.escape(str(s), quote=True)


def _font_css(chars):
    css = []
    text = "".join(sorted(set(chars))) or " "
    for family, weight, file in FACES:
        font = TTFont(FONTS / f"{file}.woff2")
        opts = subset.Options()
        opts.flavor = "woff2"
        opts.layout_features = ["kern", "liga", "calt", "tnum"]
        sub = subset.Subsetter(opts)
        sub.populate(text=text)
        sub.subset(font)
        buf = io.BytesIO()
        font.flavor = "woff2"
        font.save(buf)
        data = base64.b64encode(buf.getvalue()).decode()
        css.append(f"@font-face{{font-family:{family};font-weight:{weight};src:url(data:font/woff2;base64,{data}) format('woff2')}}")
    return "".join(css)


def doc(w, h, t, body, css="", title=""):
    chars = "".join(html.unescape(m) for m in re.findall(r">([^<>]+)<", body))
    chars += chars.upper() + chars.lower()  # labels use text-transform
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}" fill="none">
<title>{esc(title)}</title>
<style>
{_font_css(chars)}
.s{{font-family:G,'Helvetica Neue',Arial,sans-serif;letter-spacing:-.01em}}
.d{{font-family:G,'Helvetica Neue',Arial,sans-serif;font-weight:500;letter-spacing:-.035em}}
.m{{font-family:GM,ui-monospace,Menlo,Consolas,monospace;font-weight:400;letter-spacing:.02em}}
.up{{text-transform:uppercase;letter-spacing:.08em}}
.in{{animation:in .8s cubic-bezier(.2,.7,.2,1) both}}
@keyframes in{{from{{opacity:0;transform:translateY(8px)}}}}
.blink{{animation:blink 1.1s steps(1) infinite}}
@keyframes blink{{50%{{opacity:0}}}}
.draw{{stroke-dasharray:1;stroke-dashoffset:1;animation:draw 1.4s cubic-bezier(.6,0,.2,1) .2s forwards}}
@keyframes draw{{to{{stroke-dashoffset:0}}}}
{css}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}.draw{{stroke-dashoffset:0}}.still{{opacity:1!important}}}}
</style>
{body}
</svg>
"""


# --------------------------------------------------------------------------- primitives

def text(x, y, s, t, size=12, cls="m", color="muted", anchor="start", weight=None, extra=""):
    w = f' font-weight="{weight}"' if weight else ""
    return (f'<text x="{x}" y="{y}" class="{cls}" font-size="{size}"{w} fill="{t[color]}" '
            f'text-anchor="{anchor}"{extra}>{esc(s)}</text>')


def hline(x1, x2, y, t, color="line", draw=False):
    cls = ' class="draw" pathLength="1"' if draw else ""
    return f'<line{cls} x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{t[color]}" stroke-width="1"/>'


def vline(x, y1, y2, t, color="line"):
    return f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="{t[color]}" stroke-width="1"/>'


def cross(x, y, t, s=6, color="ink"):
    return (f'<path d="M{x - s} {y}H{x + s}M{x} {y - s}V{y + s}" stroke="{t[color]}" stroke-width="1"/>')


def frame(x, y, w, h, t, ticks=False):
    """Hairline frame with crosshair corners and optional ruler ticks on the sides."""
    o = [f'<rect x="{x + .5}" y="{y + .5}" width="{w - 1}" height="{h - 1}" stroke="{t["line"]}"/>']
    for cx in (x, x + w):
        for cy in (y, y + h):
            o.append(cross(cx + .5, cy + .5, t))
    if ticks:
        for side in (x - 14, x + w + 6):
            for k, ty in enumerate(range(int(y) + 8, int(y + h) - 4, 8)):
                ln = 8 if k % 5 == 0 else 4
                o.append(f'<line x1="{side + (8 - ln if side < x else 0)}" y1="{ty + .5}" x2="{side + (8 if side < x else ln)}" '
                         f'y2="{ty + .5}" stroke="{t["line"]}"/>')
    return "".join(o)


def dot_status(x, y, t, label, color="accent"):
    return (f'<rect class="blink" x="{x}" y="{y - 7}" width="7" height="7" fill="{t[color]}"/>'
            + text(x + 14, y, label, t, 11, cls="m up", color="ink"))


def button(x, y, label, t, dashed=False, solid=False):
    w = len(label) * 7.6 + 28
    dash = ' stroke-dasharray="3 3"' if dashed else ""
    fill = t["accent"] if solid else "none"
    col = "on_accent" if solid else "accent"
    return (f'<rect x="{x + .5}" y="{y + .5}" width="{w:.0f}" height="30" fill="{fill}" stroke="{t["accent"]}"{dash}/>'
            + text(x + w / 2, y + 20, label, t, 12.5, color=col, anchor="middle")), w


def cursor(t, label, color, path_css, delay=0, dur=14, home=(0, 0)):
    """Multiplayer-style agent cursor with a name tag; moves along a CSS keyframe path."""
    w = len(label) * 6.6 + 14
    fill = t[color]
    txt = t["on_accent"] if color == "accent" else t["bg"]
    return (f'<g style="transform:translate({home[0]}px,{home[1]}px);animation:{path_css} {dur}s ease-in-out {delay}s infinite alternate">'
            f'<path d="M0 0L0 15L4 11L7 18L9.5 17L6.6 10.2L12 10.2Z" fill="{fill}" stroke="{t["bg"]}" stroke-width="1"/>'
            f'<rect x="12" y="15" width="{w:.0f}" height="17" rx="2" fill="{fill}"/>'
            f'<text x="{12 + w / 2:.1f}" y="27" class="m" font-size="10.5" fill="{txt}" text-anchor="middle">{esc(label)}</text></g>')


# --------------------------------------------------------------------------- halftone

def halftone_sphere(cx, cy, r, t, step=5.0, seed=3, color="accent", halo=True, id_=None):
    rnd = random.Random(seed)
    L = (-0.55, -0.62, 0.56)
    n = math.sqrt(sum(c * c for c in L))
    L = tuple(c / n for c in L)
    out = []
    span = r * (1.42 if halo else 1.02)
    y = cy - span
    row = 0
    while y <= cy + span:
        x = cx - span + (step / 2 if row % 2 else 0)
        while x <= cx + span:
            dx, dy = (x - cx) / r, (y - cy) / r
            d2 = dx * dx + dy * dy
            if d2 <= 1:
                z = math.sqrt(1 - d2)
                light = max(0.0, dx * L[0] + dy * L[1] + z * L[2])
                cov = 0.02 + 0.95 * (1 - light) ** 2.2
                cov += (rnd.random() - .5) * .16
                cov += 0.30 * (math.sqrt(d2) ** 8)  # darker limb
            elif halo:
                dist = math.sqrt(d2) - 1
                cov = 0.16 * math.exp(-dist * 5) if dy < 0.55 else 0
                cov *= 1 if rnd.random() > .25 else 0
            else:
                cov = 0
            cov = max(0.0, min(.78, cov))
            rad = step * .5 * math.sqrt(cov)
            if rad > .35:
                out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rad:.2f}"/>')
            x += step
        y += step * .866
        row += 1
    ident = f' id="{id_}"' if id_ else ""
    return f'<g{ident} fill="{t[color]}">{"".join(out)}</g>'


def halftone_disc(cx, cy, r, t, step=5.0, seed=5, color="accent"):
    """Flat radar-style disc: density falls off from the centre, with dithering."""
    rnd = random.Random(seed)
    out = []
    y = cy - r
    row = 0
    while y <= cy + r:
        x = cx - r + (step / 2 if row % 2 else 0)
        while x <= cx + r:
            d = math.hypot(x - cx, y - cy) / r
            if d <= 1:
                ring = 0.5 + 0.5 * math.cos(d * math.pi * 6)
                cov = 0.02 + 0.09 * ring + 0.07 * (1 - d) + (rnd.random() - .5) * .05
                rad = step * .5 * math.sqrt(max(0, cov))
                if rad > .3:
                    out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rad:.2f}"/>')
            x += step
        y += step * .866
        row += 1
    return f'<g fill="{t[color]}">{"".join(out)}</g>'


def pixels(x, y, rows, t, size=8, gap=1, color="accent", cls_fn=None):
    """1-bit pixel art from a list of strings ('#' = on)."""
    out = []
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch == "#":
                cls = cls_fn(i, j) if cls_fn else ""
                out.append(f'<rect{cls} x="{x + i * size}" y="{y + j * size}" width="{size - gap}" height="{size - gap}" fill="{t[color]}"/>')
    return "".join(out)


def write(name, theme, svg):
    path = ASSETS / f"{name}-{theme}.svg"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(svg, encoding="utf-8", newline="\n")
    return path
