"""Builds every graphic in README.md, light and dark. Run: python scripts/build.py"""
import math

from data import load
from kit import (THEMES, button, cursor, doc, esc, frame, halftone_disc, halftone_sphere, hline,
                 text, vline, write)


def short(n):
    return f"{n / 1000:.1f}k".replace(".0k", "k") if n >= 1000 else str(n)


def project_name(repo):
    owner, name = repo.split("/")
    if name == "agents":
        return owner.upper()
    return name.replace("-core", "").replace("-", "").upper()


def meta_row(t, W, left, mid, right, live=True):
    out = [text(24, 30, left, t, 11, cls="m up", color="ink"), hline(0, W, 46, t)]
    if mid:
        out.append(text(W * .42, 30, mid, t, 11, cls="m up"))
    if right:
        if live:
            out.append(f'<rect class="blink" x="{W - 24 - len(right) * 7.5 - 14:.0f}" y="23" width="7" height="7" fill="{t["accent"]}"/>')
        out.append(text(W - 24, 30, right, t, 11, cls="m up", color="ink", anchor="end"))
    return "".join(out)


def spec_rows(x, y, w, rows, t, label_w=96, size=14, h=34):
    out = []
    for i, (k, v) in enumerate(rows):
        ry = y + i * h
        out.append(hline(x, x + w, ry, t))
        out.append(text(x, ry + h * .65, k, t, 11, cls="m up"))
        out.append(text(x + label_w, ry + h * .65, v, t, size, cls="s", color="ink"))
    out.append(hline(x, x + w, y + len(rows) * h, t))
    return "".join(out)


def stagger(svg, delay):
    return f'<g class="in" style="animation-delay:{delay:.2f}s">{svg}</g>'


# --------------------------------------------------------------------------- hero

def hero(t, d):
    W, H = 1000, 660
    cx, cy, R = 500, 230, 136
    css = f"""
.scan{{animation:scan 7s linear infinite}}
@keyframes scan{{from{{transform:translateY({cy - R - 70}px)}}to{{transform:translateY({cy + R + 40}px)}}}}
@keyframes c1{{0%{{transform:translate(318px,150px)}}50%{{transform:translate(372px,118px)}}100%{{transform:translate(344px,196px)}}}}
@keyframes c2{{0%{{transform:translate(610px,270px)}}50%{{transform:translate(560px,300px)}}100%{{transform:translate(630px,322px)}}}}
@keyframes c3{{0%{{transform:translate(520px,98px)}}50%{{transform:translate(590px,128px)}}100%{{transform:translate(548px,84px)}}}}
"""
    b = [frame(24, 24, W - 48, H - 48, t, ticks=True),
         text(44, 47, "[FIG. 01]  DJ / PROFILE", t, 11, cls="m up"),
         text(W / 2, 47, "DEV JHAWAR", t, 11, cls="m up", color="ink", anchor="middle"),
         text(W - 44, 47, "BHUBANESWAR — 20.29°N 85.82°E", t, 11, cls="m up", anchor="end"),
         hline(24, W - 24, 60, t)]

    orbit = f"M{cx - 280},{cy} a280,58 0 1,1 560,0 a280,58 0 1,1 -560,0"
    b.append(f'<g transform="rotate(-13 {cx} {cy})"><path d="{orbit}" stroke="{t["muted"]}" stroke-width="1" stroke-dasharray="2 5"/></g>')
    b.append(halftone_sphere(cx, cy, R, t, id_="sphere"))
    b.append(f'<clipPath id="band"><rect class="scan" x="{cx - 260}" y="0" width="520" height="7"/></clipPath>'
             f'<g clip-path="url(#band)"><rect x="{cx - 230}" y="{cy - R - 80}" width="460" height="{2 * R + 140}" fill="{t["bg"]}"/>'
             f'<use href="#sphere" fill="{t["ink"]}"/></g>')
    b.append(f'<g transform="rotate(-13 {cx} {cy})"><g><animateMotion dur="16s" repeatCount="indefinite" path="{orbit}"/>'
             f'<rect x="-4" y="-4" width="8" height="8" fill="{t["ink"]}"/><path d="M-14 0H-6M6 0H14" stroke="{t["ink"]}" stroke-width="3"/>'
             f'<text x="12" y="-10" class="m" font-size="10" fill="{t["ink"]}">SAT-01</text></g></g>')

    callouts = [((cx - 128, cy - 52), (96, 132), "[A] AGENTS", "LangGraph · MCP · tools"),
                ((cx + 120, cy - 70), (760, 104), "[B] RAG", "retrieval that cites sources"),
                ((cx + 112, cy + 82), (760, 330), "[C] BACKEND", "FastAPI · Redis · Postgres")]
    for (px, py), (lx, ly), head, sub in callouts:
        ex = lx - 8 if lx > cx else lx + 168
        b.append(stagger(f'<path d="M{px} {py}L{ex} {ly - 4}" stroke="{t["ink"]}" stroke-width="1"/>'
                         f'<rect x="{px - 2.5}" y="{py - 2.5}" width="5" height="5" fill="{t["ink"]}"/>'
                         + text(lx, ly, head, t, 11, cls="m up", color="ink")
                         + text(lx, ly + 17, sub, t, 12.5, cls="s"), .6))

    b.append(cursor(t, "planner-agent", "accent", "c1", -3, 9, (344, 140)))
    b.append(cursor(t, "research-agent", "accent", "c2", -6, 11, (600, 300)))
    b.append(cursor(t, "dev", "ink", "c3", -2, 8, (560, 100)))

    b.append(stagger(f'<rect x="56" y="420" width="7" height="7" fill="{t["accent"]}" class="blink"/>'
                     + text(72, 427, "AI engineer / backend / open source", t, 11, cls="m up", color="accent"), .1))
    b.append(stagger(f'<text x="52" y="486" class="d" font-size="52" fill="{t["ink"]}">Building AI systems that</text>'
                     f'<text x="52" y="544" class="d" font-size="52" fill="{t["ink"]}">work in the <tspan fill="{t["accent"]}">real world.</tspan></text>', .2))
    para = ["I'm Dev, a CSE student at KIIT. I build", "agents, RAG pipelines and the backends",
            "under them, and I fix bugs in the open", "source tools I rely on."]
    for i, line in enumerate(para):
        b.append(stagger(text(700, 436 + i * 20, line, t, 13.5, cls="s", color="ink"), .35 + i * .05))
    b1, w1 = button(700, 516, "Portfolio ↗", t)
    b2, _ = button(700 + w1 + 10, 516, "Résumé", t, dashed=True)
    b.append(stagger(b1 + b2, .5))

    # upstream strip, driven by live data
    names = []
    for p in d["merged"]:
        n = project_name(p["repo"])
        if n not in names:
            names.append(n)
    names = names[:8]
    n_merged = len(d["merged"])
    b.append(hline(24, W - 24, 574, t))
    b.append(text(W / 2, 596, f"{n_merged} pull requests merged upstream into", t, 11, cls="m up", anchor="middle"))
    for i, o in enumerate(names):
        x = 92 + i * (816 / max(1, len(names) - 1))
        b.append(stagger(text(round(x, 1), 618, o, t, 12.5, cls="m", color="ink", anchor="middle", weight=500), .6 + i * .06))
    return doc(W, H, t, "".join(b), css, f"Dev Jhawar — building AI systems that work in the real world. {n_merged} PRs merged upstream.")


# --------------------------------------------------------------------------- section header

def header(t, idx, title, meta):
    W, H = 1000, 92
    b = [hline(0, W, 22, t, draw=True),
         f'<rect x="0" y="20" width="44" height="3" fill="{t["accent"]}"/>',
         text(0, 66, f"[{idx}]", t, 13, cls="m", color="accent"),
         stagger(f'<text x="56" y="70" class="d" font-size="36" fill="{t["ink"]}">{esc(title)}</text>', 0),
         text(W, 66, meta, t, 11, cls="m up", anchor="end")]
    return doc(W, H, t, "".join(b), "", f"{idx} — {title}")


# --------------------------------------------------------------------------- flagship card

def flagship(t):
    W, H = 1000, 440
    rx, ry, R = 782, 248, 150
    css = f"""
.sweep{{transform-origin:{rx}px {ry}px;animation:sweep 6s linear infinite}}
@keyframes sweep{{to{{transform:rotate(360deg)}}}}
.blip{{opacity:.18;animation:blip 6s steps(1) infinite}}
@keyframes blip{{0%,40%{{opacity:1}}41%,100%{{opacity:.18}}}}
"""
    b = [frame(0, 0, W, H, t), meta_row(t, W, "[P.01] WatchTower", "Multi-agent system", "Live — watch-tower-seven.vercel.app"),
         vline(560, 46, H, t),
         stagger(f'<text x="30" y="122" class="d" font-size="62" fill="{t["ink"]}">WatchTower</text>', 0)]
    desc = ["Describe anything on the public web you want watched,",
            "in plain English. Agents check it on a schedule, decide",
            "whether it really happened, and send one complete alert."]
    for i, line in enumerate(desc):
        b.append(stagger(text(32, 164 + i * 23, line, t, 15.5, cls="s"), .1 + i * .05))
    b.append(spec_rows(32, 254, 496, [("Stack", "Next.js / FastAPI / LangGraph / Groq / Redis"),
                                      ("Alerts", "Email / web push / Telegram / signed webhooks"),
                                      ("Scale", "Scheduler + worker fleet on SKIP LOCKED leases")], t))
    b.append(text(32, 410, "→ Live app", t, 12, cls="m up", color="accent")
             + text(150, 410, "→ Source", t, 12, cls="m up", color="accent")
             + text(256, 410, "→ Architecture", t, 12, cls="m up", color="accent"))

    b.append(text(584, 72, "[FIG. 02] Active watches", t, 11, cls="m up"))
    b.append(halftone_disc(rx, ry, R, t))
    for r in (R, R * 2 / 3, R / 3):
        b.append(f'<circle cx="{rx}" cy="{ry}" r="{r:.0f}" stroke="{t["line"]}"/>')
    b.append(f'<path d="M{rx - R - 14} {ry}H{rx + R + 14}M{rx} {ry - R - 14}V{ry + R + 14}" stroke="{t["line"]}"/>')
    b.append(f'<g class="sweep"><line x1="{rx}" y1="{ry}" x2="{rx + R}" y2="{ry}" stroke="{t["ink"]}" stroke-width="1.5"/>'
             f'<rect x="{rx + R - 3}" y="{ry - 3}" width="6" height="6" fill="{t["ink"]}"/></g>')
    blips = [(32, .62, "Flight < ₹4k", -1), (146, .6, "Restock · size 9", -1),
             (222, .78, "Visa slot open", 1), (318, .6, "CVE in deps", -1)]
    for ang, dist, label, side in blips:
        a = math.radians(ang)
        bx, by = rx + R * dist * math.cos(a), ry + R * dist * math.sin(a)
        lx = bx + 10 * side
        lw = len(label) * 6.4 + 8
        kx = lx - 4 if side > 0 else lx - lw + 4
        b.append(f'<g class="blip still" style="animation-delay:{ang / 360 * 6 - 6:.2f}s"><rect x="{bx - 4:.1f}" y="{by - 4:.1f}" width="8" height="8" fill="{t["accent"]}"/>'
                 f'<rect x="{kx:.1f}" y="{by - 8:.1f}" width="{lw:.1f}" height="16" fill="{t["bg"]}"/>'
                 + text(round(lx, 1), round(by + 4, 1), label, t, 10.5, cls="m", color="ink", anchor="start" if side > 0 else "end") + "</g>")
    b.append(f'<rect x="{rx - 3}" y="{ry - 3}" width="6" height="6" fill="{t["ink"]}"/>')
    b.append(text(rx, 424, "Describe → schedule → check → judge → notify", t, 10.5, cls="m up", anchor="middle"))
    return doc(W, H, t, "".join(b), css, "WatchTower — describe what to watch on the web; AI agents check, judge and notify")


# --------------------------------------------------------------------------- card illustrations (each returns svg, css)

def art_gridmind(t, x0, y0):
    cols, rows, cw, ch, c0 = 7, 5, 52, 20, 70
    css = ".cell{opacity:0;animation:cell 7s steps(1) infinite}@keyframes cell{0%{opacity:0}6%,80%{opacity:1}86%,100%{opacity:0}}"
    colx = lambda c: x0 + (0 if c == 0 else c0 + (c - 1) * cw)
    o = [text(x0 + 6, y0 - 8, "Company", t, 9.5, cls="m up")]
    for i, h in enumerate(["Founded", "HQ", "Funding", "CEO", "Stack", "Hiring"]):
        o.append(text(colx(i + 1) + 6, y0 - 8, h, t, 9.5, cls="m up"))
    for r in range(rows + 1):
        o.append(hline(x0, colx(cols), y0 + r * ch, t))
    for c in range(cols + 1):
        o.append(vline(colx(c), y0, y0 + rows * ch, t))
    for r, n in enumerate(["Acme", "Globex", "Initech", "Umbrella", "Hooli"]):
        o.append(text(x0 + 6, y0 + r * ch + 14, n, t, 11, cls="s", color="ink"))
        for c in range(1, cols):
            k = r * (cols - 1) + (c - 1)
            o.append(f'<rect class="cell still" style="animation-delay:{(k * .17) % 5:.2f}s" x="{colx(c) + 6}" y="{y0 + r * ch + 7}" '
                     f'width="{14 + (k * 7) % 22}" height="6" fill="{t["accent"]}"/>')
    return "".join(o), css


def art_policylens(t, x0, y0):
    css = ".hl{opacity:0;animation:hl 6s steps(1) infinite}@keyframes hl{0%,30%{opacity:1}31%,100%{opacity:0}}"
    o = [f'<rect x="{x0 + .5}" y="{y0 + .5}" width="120" height="124" stroke="{t["line"]}" fill="{t["bg"]}"/>',
         text(x0 + 8, y0 + 16, "POLICY.PDF", t, 9.5, cls="m"), text(x0 + 112, y0 + 16, "P.14", t, 9.5, cls="m", anchor="end")]
    widths = [96, 88, 100, 70, 92, 84, 98, 60, 90]
    for i, w in enumerate(widths):
        o.append(f'<rect x="{x0 + 10}" y="{y0 + 28 + i * 10}" width="{w}" height="4" fill="{t["line"]}"/>')
    notes = ["Waiting period: 30 days", "Excludes cosmetic surgery", "Claim within 15 days"]
    for k, line in enumerate((2, 5, 7)):
        y = y0 + 28 + line * 10
        cls = "hl still" if k == 0 else "hl"
        o.append(f'<g class="{cls}" style="animation-delay:{k * 2}s"><rect x="{x0 + 8}" y="{y - 3}" width="{widths[line] + 4}" height="10" fill="{t["accent"]}"/>'
                 f'<path d="M{x0 + widths[line] + 14} {y + 2}H{x0 + 170}" stroke="{t["ink"]}"/>'
                 + text(x0 + 176, y + 6, notes[k], t, 11.5, cls="s", color="ink")
                 + text(x0 + 176, y + 20, f"[p.14 ¶{line + 1}]", t, 10, cls="m", color="accent") + "</g>")
    return "".join(o), css


def art_casecompass(t, x0, y0):
    css = (".bar{transform-box:fill-box;transform-origin:left;animation:bar 6s cubic-bezier(.6,0,.2,1) infinite}"
           "@keyframes bar{0%{transform:scaleX(0)}25%,85%{transform:scaleX(1)}100%{transform:scaleX(0)}}")
    cols = [(0, "Similar cases"), (196, "Match"), (286, "Outcome"), (356, "Relief")]
    o = [text(x0 + c, y0 - 8, h, t, 9.5, cls="m up") for c, h in cols]
    rows = [("Airline refund denied", .94, True, "₹42,000"), ("Flight cancelled, no refund", .88, True, "₹18,500"),
            ("Travel agent no-show", .81, True, "₹65,000"), ("Insurer rejected claim", .74, False, "—"),
            ("Defective phone, no repair", .69, True, "₹12,000")]
    for i, (label, sim, won, relief) in enumerate(rows):
        top = y0 + i * 22
        yb = top + 15
        o.append(hline(x0, x0 + 430, top, t))
        o.append(text(x0, yb, label, t, 11.5, cls="s", color="ink"))
        o.append(f'<rect x="{x0 + 196}" y="{yb - 6}" width="70" height="4" fill="{t["line"]}"/>'
                 f'<rect class="bar" style="animation-delay:{i * .15:.2f}s" x="{x0 + 196}" y="{yb - 6}" width="{70 * sim:.0f}" height="4" fill="{t["accent"]}"/>')
        o.append(text(x0 + 286, yb, "Won" if won else "Lost", t, 10.5, cls="m up", color="accent" if won else "muted"))
        o.append(text(x0 + 356, yb, relief, t, 11.5, cls="s", color="ink"))
    o.append(hline(x0, x0 + 430, y0 + len(rows) * 22, t))
    return "".join(o), css


def art_tidyflow(t, x0, y0):
    css = ".route{opacity:0;animation:route 7.5s steps(1) infinite}@keyframes route{0%,19%{opacity:1}20%,100%{opacity:0}}"
    files = ["IMG_2231.jpg", "invoice(3).pdf", "Untitled 4.docx", "scan_0001.png", "notes_final_v2.txt"]
    folders = ["Photos/", "Finance/", "Documents/", "Scans/"]
    dest = [0, 1, 2, 3, 2]
    fx = x0 + 290
    o = [text(x0, y0 - 8, "~/Downloads · 5 files", t, 9.5, cls="m up"), text(fx, y0 - 8, "Proposed", t, 9.5, cls="m up")]
    fy = [y0 + 12 + j * 26 for j in range(len(folders))]
    for j, name in enumerate(folders):
        o.append(f'<path d="M{fx} {fy[j] - 8}h5l2 2h7v8h-14z" stroke="{t["ink"]}"/>' + text(fx + 20, fy[j], name, t, 11, cls="m", color="ink"))
    for i, f in enumerate(files):
        y = y0 + 12 + i * 22
        elbow = x0 + 170 + i * 12
        path = f"M{x0 + 136} {y - 4}H{elbow}V{fy[dest[i]] - 4}H{fx - 8}"
        o.append(text(x0, y, f, t, 11, cls="m", color="ink"))
        o.append(f'<path d="{path}" stroke="{t["line"]}"/>')
        cls = "route still" if i == 0 else "route"
        o.append(f'<g class="{cls}" style="animation-delay:{i * 1.5}s"><path d="{path}" stroke="{t["accent"]}" stroke-width="1.5"/>'
                 f'<rect x="{x0 - 10}" y="{y - 7}" width="5" height="5" fill="{t["accent"]}"/>'
                 f'<rect x="{fx - 9}" y="{fy[dest[i]] - 6}" width="4" height="4" fill="{t["accent"]}"/></g>')
    o.append(text(x0, y0 + 124, "Apply this plan? [y/n]", t, 11, cls="m", color="ink")
             + f'<rect class="blink" x="{x0 + 166}" y="{y0 + 114}" width="7" height="12" fill="{t["accent"]}"/>')
    return "".join(o), css


def art_transformer(t, x0, y0):
    css = ".q{animation:q 6s steps(6) infinite}@keyframes q{to{transform:translateY(96px)}}"
    de = ["ein", "Hund", "läuft", "im", "Park"]
    en = ["a", "dog", "runs", "in", "the", "park"]
    align = [0, 1, 2, 3, 3, 4]
    gx, gy, cw, ch = x0 + 52, y0 + 6, 30, 16
    o = [text(x0, y0 - 8, "Cross-attention · EN → DE", t, 9.5, cls="m up")]
    o.append(f'<rect class="q" x="{gx - 52}" y="{gy}" width="{52 + 5 * cw}" height="{ch}" fill="{t["faint"]}"/>')
    for j, w in enumerate(de):
        o.append(text(gx + j * cw + cw / 2, gy + 6 * ch + 14, w, t, 9.5, cls="m", anchor="middle"))
    for i, w in enumerate(en):
        o.append(text(gx - 8, gy + i * ch + 11.5, w, t, 10, cls="m", color="ink", anchor="end"))
        for j in range(5):
            wgt = .92 if j == align[i] else max(.04, .34 - abs(j - align[i]) * .12 + ((i * 5 + j) % 3) * .03)
            side = max(2, 13 * math.sqrt(wgt))
            o.append(f'<rect x="{gx + j * cw + (cw - side) / 2:.1f}" y="{gy + i * ch + (ch - side) / 2:.1f}" width="{side:.1f}" height="{side:.1f}" fill="{t["accent"]}"/>')
    sx = x0 + 262
    for i, (k, v) in enumerate([("Heads", "8"), ("d_model", "512"), ("Layers", "6 + 6"), ("Task", "EN → DE"), ("Data", "Multi30K")]):
        y = y0 + 12 + i * 22
        o.append(hline(sx, sx + 170, y - 15, t) + text(sx, y, k, t, 9.5, cls="m up") + text(sx + 170, y, v, t, 11.5, cls="m", color="ink", anchor="end"))
    o.append(hline(sx, sx + 170, y0 + 12 + 5 * 22 - 15, t))
    return "".join(o), css


def art_pennypilot(t, x0, y0):
    css = (".msg{animation:msg 10s ease infinite both}"
           "@keyframes msg{0%{opacity:0;transform:translateY(6px)}5%,82%{opacity:1;transform:none}92%,100%{opacity:0}}")
    chat = [("u", "200 food"), ("b", "Logged ₹200 · Food"), ("u", "how much on food this month?"),
            ("b", "₹4,820 across 23 entries"), ("a", "Food is 52% above your usual")]
    o = []
    right = x0 + 436
    for i, (who, s) in enumerate(chat):
        y = y0 + i * 26
        w = len(s) * 6.7 + 22
        x = right - w if who == "u" else x0
        if who == "u":
            box = f'<rect x="{x + .5:.1f}" y="{y + .5}" width="{w:.0f}" height="20" stroke="{t["line"]}" fill="{t["bg"]}"/>'
            col = "ink"
        elif who == "b":
            box = f'<rect x="{x}" y="{y}" width="{w:.0f}" height="20" fill="{t["accent"]}"/>'
            col = "on_accent"
        else:
            box = f'<rect x="{x + .5}" y="{y + .5}" width="{w + 16:.0f}" height="20" stroke="{t["accent"]}" stroke-dasharray="3 3" fill="{t["bg"]}"/>'
            col = "accent"
            s = "! " + s
        o.append(f'<g class="msg still" style="animation-delay:{i * 1.1:.1f}s">{box}'
                 + text(round(x + 11, 1), y + 14, s, t, 11, cls="m", color=col) + "</g>")
    o.append(text(x0, y0 + 5 * 26 + 6, "@PennyPilot_bot", t, 9.5, cls="m up"))
    return "".join(o), css


def card(t, num, fig, name, status, desc, stack, links, art, art_y=82):
    W, H = 490, 430
    art_svg, art_css = art(t, 26, art_y)
    b = [frame(0, 0, W, H, t),
         text(20, 30, f"[P.{num}] {name}", t, 11, cls="m up", color="ink"),
         f'<rect class="blink" x="{W - 20 - len(status) * 7.5 - 14:.0f}" y="23" width="7" height="7" fill="{t["accent"]}"/>',
         text(W - 20, 30, status, t, 11, cls="m up", color="ink", anchor="end"),
         hline(0, W, 46, t),
         f'<g fill="{t["faint"]}">' + "".join(f'<rect x="{x}" y="{y}" width="2" height="2"/>' for x in range(14, W, 16) for y in range(56, 200, 16)) + "</g>",
         art_svg,
         text(W - 20, 198, f"[FIG. {fig}]", t, 10, cls="m", anchor="end"),
         hline(0, W, 208, t),
         stagger(f'<text x="20" y="262" class="d" font-size="40" fill="{t["ink"]}">{esc(name)}</text>', 0)]
    b += [stagger(text(22, 296 + i * 21, line, t, 14.5, cls="s"), .1 + i * .05) for i, line in enumerate(desc)]
    b.append(spec_rows(22, 352, W - 44, [("Stack", stack)], t, label_w=70, size=13.5))
    b.append("".join(text(22 + i * 120, 410, f"→ {l}", t, 11.5, cls="m up", color="accent") for i, l in enumerate(links)))
    return doc(W, H, t, "".join(b), art_css, f"{name} — {' '.join(desc)}")


CARDS = [
    ("gridmind", "02", "03", "GridMind", "Live",
     ["A spreadsheet that researches for you. Rows are",
      "things, columns are questions, and one agent per",
      "cell searches the web and cites its sources."],
     "Svelte 5 / FastAPI / LangGraph / Groq / Supabase", ["Live", "Source"], art_gridmind, 82),
    ("policylens", "03", "04", "PolicyLens", "Live",
     ["Upload any insurance policy PDF and ask it",
      "questions in plain English. Every answer points",
      "to the exact page and clause it came from."],
     "FastAPI / Jina v3 / pgvector / Groq / Docker", ["Live", "Source"], art_policylens, 62),
    ("casecompass", "04", "05", "CaseCompass", "Live",
     ["Describe a consumer dispute in plain words and see",
      "how Indian consumer commissions decided similar",
      "cases: who won, the refund, and the laws cited."],
     "FastAPI / Jina v3 / hybrid retrieval / Groq", ["Live", "Source"], art_casecompass, 76),
    ("tidyflow", "05", "06", "TidyFlow", "macOS · Windows",
     ["Point it at a messy folder. It reads every file,",
      "proposes a clean set of folders, shows where things",
      "will go, and moves nothing until you agree."],
     "Tauri / React / TypeScript / Python", ["Download", "Source"], art_tidyflow, 66),
    ("transformer", "06", "07", "Transformer", "Research",
     ["“Attention Is All You Need” rebuilt from first",
      "principles in PyTorch: multi-head attention, positional",
      "encoding and a 6 + 6 encoder-decoder for EN → DE."],
     "PyTorch / multi-head attention / Noam schedule", ["Source"], art_transformer, 70),
    ("pennypilot", "07", "08", "PennyPilot", "Live bot",
     ["An expense tracker that lives in Telegram. Log spends",
      "by text, voice note or receipt photo, ask questions in",
      "plain English, and get alerts when spending spikes."],
     "Python / MCP / LangGraph / Whisper / Telegram", ["Try the bot", "Source"], art_pennypilot, 58),
]


# --------------------------------------------------------------------------- open source

def opensource(t, d):
    prs = d["merged"]
    n = len(prs)
    by_repo = {}
    for p in prs:
        r = by_repo.setdefault(p["repo"], {"stars": p["stars"], "count": 0})
        r["count"] += 1
    W = 1000
    top = 262
    H = top + len(prs) * 30 + 26
    b = [frame(0, 0, W, H, t), meta_row(t, W, "[FIG. 09] Upstream contributions", "", "Refreshed daily"),
         vline(560, 46, top, t)]
    num_w = len(str(n)) * 86
    b.append(stagger(f'<text x="26" y="200" class="d" font-size="160" fill="{t["accent"]}">{n}</text>', 0))
    b.append(stagger(f'<text x="{40 + num_w}" y="140" class="d" font-size="28" fill="{t["ink"]}">pull requests</text>'
                     f'<text x="{40 + num_w}" y="174" class="d" font-size="28" fill="{t["ink"]}">merged upstream</text>', .1))
    b.append(stagger(text(32, 236, f"Into {len(by_repo)} open source projects · {d['opened']} opened in total", t, 11, cls="m up"), .2))

    b.append(text(584, 72, "By project", t, 11, cls="m up"))
    rows = sorted(by_repo.items(), key=lambda kv: -kv[1]["stars"])
    rh = min(20, 170 / max(1, len(rows)))
    for i, (repo, info) in enumerate(rows):
        y = 96 + i * rh
        stars = f"★ {short(info['stars'])}" if info["stars"] >= 100 else ""
        sq = "".join(f'<rect x="{960 - k * 11 - 8}" y="{y - 8}" width="8" height="8" fill="{t["accent"]}"/>' for k in range(info["count"]))
        b.append(stagger(text(584, y, repo, t, 12.5, cls="s", color="ink") + text(860, y, stars, t, 10.5, cls="m", anchor="end") + sq, .2 + i * .04))

    b.append(hline(0, W, top, t))
    for i, p in enumerate(prs):
        y = top + i * 30
        title = p["title"] if len(p["title"]) <= 82 else p["title"][:79].rstrip() + "..."
        row = (text(26, y + 20, project_name(p["repo"]), t, 11, cls="m up", color="ink")
               + text(170, y + 20, title, t, 13.5, cls="s", color="ink")
               + f'<rect x="{W - 90}" y="{y + 12}" width="7" height="7" fill="{t["accent"]}"/>'
               + text(W - 24, y + 20, "Merged", t, 10.5, cls="m up", color="accent", anchor="end"))
        if i:
            row = hline(26, W - 24, y, t, color="faint") + row
        b.append(stagger(row, .3 + i * .05))
    return doc(W, H, t, "".join(b), "", f"{n} pull requests merged into {len(by_repo)} open source projects")


# --------------------------------------------------------------------------- toolchain

STACK = [
    ("AI / ML", "PyTorch / TensorFlow / scikit-learn / Hugging Face / FAISS"),
    ("LLM systems", "LangGraph / LangChain / MCP / Groq / Jina embeddings / RAG evals"),
    ("Backend", "FastAPI / Node.js / SQLAlchemy / WebSockets / arq workers"),
    ("Data", "PostgreSQL / pgvector / Redis / Supabase"),
    ("Infra", "Docker / GitHub Actions / AWS / Vercel / Render / Railway"),
    ("Languages", "Python / C++ / TypeScript / Java / SQL"),
    ("Frontend", "React / Next.js / Svelte / Tauri / Astro"),
]


def toolchain(t):
    W, rh, top = 1000, 46, 46
    H = top + len(STACK) * rh + 20
    css = f".sel{{animation:sel {len(STACK) * 2}s steps({len(STACK)}) infinite}}@keyframes sel{{to{{transform:translateY({len(STACK) * rh}px)}}}}"
    b = [frame(0, 0, W, H, t), meta_row(t, W, "[FIG. 10] Toolchain", "", f"{len(STACK)} groups", live=False),
         f'<g class="sel"><rect x="1" y="{top + 10}" width="{W - 2}" height="{rh}" fill="{t["faint"]}"/>'
         f'<rect x="1" y="{top + 10}" width="3" height="{rh}" fill="{t["accent"]}"/></g>']
    for i, (k, v) in enumerate(STACK):
        y = top + 10 + i * rh
        b.append(stagger((hline(26, W - 26, y, t) if i else "")
                         + text(26, y + 29, f"{i + 1:02d}", t, 11, cls="m", color="accent")
                         + text(64, y + 29, k, t, 11, cls="m up")
                         + text(250, y + 29, v, t, 16, cls="s", color="ink"), i * .06))
    return doc(W, H, t, "".join(b), css, "Toolchain: " + "; ".join(f"{k}: {v}" for k, v in STACK))


# --------------------------------------------------------------------------- telemetry

def telemetry(t, d):
    W, H = 1000, 380
    css = (".colscan{animation:colscan 9s linear infinite}@keyframes colscan{from{transform:translateX(0)}to{transform:translateX(689px)}}"
           ".lang{transform-box:fill-box;transform-origin:left;animation:grow 1.2s cubic-bezier(.6,0,.2,1) both}@keyframes grow{from{transform:scaleX(0)}}")
    tiles = [(str(len(d["merged"])), "Merged upstream"), (str(d["opened"]), "PRs opened upstream"),
             (f"{d['contributions']:,}", "Contributions (12 mo)"), (f"{d['commits']:,}", "Commits (12 mo)"),
             (f"{d['longest_streak']}d", "Longest streak")]
    b = [f'<defs><pattern id="ph" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
         f'<line x1="0" y1="0" x2="0" y2="5" stroke="{t["ink"]}" stroke-width="1.2"/></pattern>'
         f'<pattern id="pd" width="4" height="4" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r=".9" fill="{t["ink"]}"/></pattern></defs>',
         frame(0, 0, W, H, t), meta_row(t, W, "[FIG. 11] Telemetry", "", "Refreshed daily")]
    tw = W / len(tiles)
    for i, (v, label) in enumerate(tiles):
        x = i * tw
        if i:
            b.append(vline(x, 46, 156, t))
        col = "accent" if i == 0 else "ink"
        b.append(stagger(f'<text x="{x + 24}" y="112" class="d" font-size="44" fill="{t[col]}">{esc(v)}</text>'
                         + text(x + 26, 138, label, t, 10.5, cls="m up"), i * .07))
    b.append(hline(0, W, 156, t))

    # contribution density, no calendar labels
    days = d["days"]
    mx = max(days) or 1
    gx, gy, cell = 32, 206, 13
    b.append(text(gx, 188, "Contribution density", t, 11, cls="m up"))
    dots = []
    for k, c in enumerate(days):
        col, row = divmod(k, 7)
        cx, cy = gx + col * cell + 6, gy + row * cell + 6
        if c:
            dots.append(f'<circle cx="{cx}" cy="{cy}" r="{1.6 + 3.6 * math.sqrt(c / mx):.2f}"/>')
        else:
            dots.append(f'<circle cx="{cx}" cy="{cy}" r="1" fill="{t["line"]}"/>')
    b.append(f'<g fill="{t["accent"]}">{"".join(dots)}</g>')
    b.append(f'<rect class="colscan" x="{gx}" y="{gy - 6}" width="1" height="{7 * cell + 12}" fill="{t["ink"]}"/>')
    b.append(text(gx, gy + 7 * cell + 30, "Each dot is a day; bigger means busier.", t, 11.5, cls="s"))

    # languages
    lx, lw = 770, 198
    b.append(text(lx, 188, "Languages · by bytes", t, 11, cls="m up"))
    fills = [t["accent"], t["ink"], "url(#ph)", t["muted"], "url(#pd)", t["line"]]
    x = lx
    for i, (name, pct) in enumerate(d["langs"]):
        w = lw * pct / 100
        b.append(f'<rect class="lang" style="animation-delay:{.3 + i * .1:.1f}s" x="{x:.1f}" y="200" width="{max(w - 2, 1.5):.1f}" height="12" fill="{fills[i]}"/>')
        x += w
    for i, (name, pct) in enumerate(d["langs"]):
        y = 240 + i * 20
        b.append(f'<rect x="{lx}" y="{y - 9}" width="10" height="10" fill="{fills[i]}" stroke="{t["line"]}"/>'
                 + text(lx + 18, y, name, t, 13, cls="s", color="ink") + text(lx + lw, y, f"{pct:.1f}%", t, 11, cls="m", anchor="end"))
    return doc(W, H, t, "".join(b), css, f"GitHub telemetry: {len(d['merged'])} PRs merged upstream, {d['contributions']} contributions in 12 months")


# --------------------------------------------------------------------------- footer / contact

def footer(t):
    W, H = 1000, 486
    b = [f'<defs><pattern id="hatch" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
         f'<line x1="0" y1="0" x2="0" y2="7" stroke="{t["line"]}" stroke-width="1.4"/>'
         f'<animateTransform attributeName="patternTransform" type="translate" from="0 0" to="7 0" dur="3s" repeatCount="indefinite" additive="sum"/></pattern></defs>',
         f'<rect x="0" y="34" width="30" height="30" fill="{t["accent"]}"/>',
         text(15, 54, "dj", t, 14, cls="d", color="on_accent", anchor="middle"),
         f'<text x="42" y="56" class="d" font-size="24" fill="{t["ink"]}">Dev Jhawar</text>',
         text(0, 96, "AI engineer and backend developer. I build", t, 14, cls="s"),
         text(0, 116, "agents, RAG systems and the infra under them.", t, 14, cls="s")]
    cols = [(470, "[Contact]", ["dev.jhawar.cs@gmail.com", "linkedin/dev-jhawar11"]),
            (690, "[Elsewhere]", ["devjhawar.com", "github/DEVJHAWAR11", "Résumé"]),
            (860, "[Status]", ["Open to roles", "Bhubaneswar, IN", "UTC +5:30"])]
    for x, head, items in cols:
        b.append(text(x, 50, head, t, 12, cls="m", color="accent"))
        for i, it in enumerate(items):
            b.append(text(x, 78 + i * 22, it, t, 14, cls="s", color="ink"))
    b += [hline(0, W, 160, t),
          text(0, 186, "© Dev Jhawar", t, 12, cls="s"),
          text(W / 2, 186, "Drawn in SVG · refreshed daily by GitHub Actions", t, 12, cls="s", anchor="middle"),
          text(W, 186, "EOF", t, 11, cls="m up", anchor="end"),
          f'<text x="{W / 2}" y="{H - 58}" text-anchor="middle" class="s" font-weight="600" font-size="262" letter-spacing="-9" '
          f'fill="url(#hatch)" stroke="{t["line"]}" stroke-width="1.5">jhawar</text>']
    return doc(W, H, t, "".join(b), "", "Contact Dev Jhawar: dev.jhawar.cs@gmail.com · linkedin.com/in/dev-jhawar11 · devjhawar.com")


HEADERS = [("featured", "01", "Featured builds", "07 entries"),
           ("opensource", "02", "Open source", None),
           ("toolchain", "03", "Toolchain", "What I build with"),
           ("telemetry", "04", "Telemetry", "Live from GitHub"),
           ("now", "05", "Right now", "~/now.yaml"),
           ("contact", "06", "Contact", "Say hello")]


def main():
    d = load()
    for name, t in THEMES.items():
        write("hero", name, hero(t, d))
        for slug, idx, title, meta in HEADERS:
            write(f"h-{slug}", name, header(t, idx, title, meta or f"{len(d['merged'])} merged PRs"))
        write("card-watchtower", name, flagship(t))
        for slug, num, fig, title, status, desc, stack, links, art, art_y in CARDS:
            write(f"card-{slug}", name, card(t, num, fig, title, status, desc, stack, links, art, art_y))
        write("opensource", name, opensource(t, d))
        write("toolchain", name, toolchain(t))
        write("telemetry", name, telemetry(t, d))
        write("footer", name, footer(t))
    print(f"built: {len(d['merged'])} merged PRs, {d['opened']} opened")


if __name__ == "__main__":
    main()
