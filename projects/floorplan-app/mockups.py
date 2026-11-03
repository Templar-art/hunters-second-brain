#!/usr/bin/env python3
"""Three page-look mockups for one job, for choosing a design direction.

    mockups.py <job slug>   ->  jobs/<slug>/mockups/{a-gallery,b-architect,c-warm}.{svg,pdf,png}

Each look only swaps presentation (floor fills, wall colour, type, page layout) on the already
checked plan SVG; geometry comes from the same out/<slug>-10x-plan.svg the main page uses.
Single-storey layout only (prototype scope).
"""
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import render as R

HERE = Path(__file__).resolve().parent
BLUE = "#61a8d8"
ET.register_namespace("", R.SVG)
ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")


def flat(fills):
    """<defs> replacing the fp-* texture patterns with flat colours (same ids, so the skin still points at them)."""
    out = []
    for k, c in fills.items():
        out.append(f'<pattern id="fp-{k}" patternUnits="userSpaceOnUse" width="60" height="60"><rect width="60" height="60" fill="{c}"/>'
                   + ('<path d="M0 0.25H60M0.25 0V60" stroke="#00000014" stroke-width="0.6"/>' if k == "tile" else "")
                   + ('<path d="M0 0.4H60M0.4 0V30M30.4 30V60M0 30.4H60" stroke="#00000012" stroke-width="0.6"/>' if k in ("pavers", "deck") else "")
                   + "</pattern>")
    return "".join(out)


LOOKS = {
    "a-gallery": dict(defs=None, wall=None, page="#ffffff", ink="#1d2126", mute="#6c737b", label="#1d2126"),
    "b-architect": dict(defs=flat({"wood": "#ffffff", "carpet": "#ffffff", "concrete": "#f1f2f3", "deck": "#f4f4f4",
                                   "tile": "#f3f6f8", "pavers": "#f4f4f4"}),
                        wall="#111417", shadow=False, page="#ffffff", ink="#111417", mute="#7a8087", label="#111417"),
    "c-warm": dict(defs=flat({"wood": "#ece3d6", "carpet": "#e4e0da", "concrete": "#dedbd6", "deck": "#e7ddcd",
                              "tile": "#dde5e3", "pavers": "#e9e2d7"}),
                   wall="#2e2a26", page="#f7f3ed", ink="#2e2a26", mute="#8a8177", label="#2e2a26"),
}


def restyle_plan(svg, look):
    if look["defs"]:
        svg = re.sub(r'<pattern id="fp-(wood|carpet|concrete|deck|tile|pavers)".*?</pattern>', "", svg, flags=re.S)
        svg = svg.replace("<defs>", "<defs>" + look["defs"], 1) if "<defs>" in svg else re.sub(r"(<svg[^>]*>)", r"\1<defs>" + look["defs"] + "</defs>", svg, 1)
    if look["wall"]:
        svg = svg.replace(R.WALL, look["wall"]).replace("#777777", look["wall"])  # old-style exports keep CubiCasa grey walls
    if look.get("shadow") is False:
        svg = svg.replace('filter="url(#fp-shadow)"', "")
    svg = svg.replace(f'fill="{R.INK}"', f'fill="{look["label"]}"')
    return svg


def plan_block(svg_text, box):
    """Place the single-storey plan, as large as fits in box, centred. Returns (svg, x0, y1 on page)."""
    root = ET.fromstring(svg_text)
    vb = [float(v) for v in root.get("viewBox").split()]
    pr, b, _ = R.storey_pieces(root)[0]
    bw, bh = box[2] - box[0], box[3] - box[1]
    s = min(bw / (b[2] - b[0]), bh / (b[3] - b[1]))
    px = box[0] + (bw - (b[2] - b[0]) * s) / 2 - b[0] * s
    py = box[1] + (bh - (b[3] - b[1]) * s) / 2 - b[1] * s
    for k, v in zip(("x", "y", "width", "height"), vb):
        pr.set(k, f"{v}")
    pr.attrib.pop("id", None)
    g = f'<g transform="translate({px:.2f} {py:.2f}) scale({s:.6f})">{ET.tostring(pr, encoding="unicode")}</g>'
    return g, px + b[0] * s, py + b[3] * s, px + b[2] * s, py + b[1] * s


def counts_svg(job, x, y, ink, size=46, right=True):
    """Bed / bath / car row; x is the right edge when right=True."""
    c, o, items = job.get("counts", {}), [], []
    for key, icon in (("beds", "bed"), ("baths", "bath"), ("cars", "car")):
        if c.get(key) not in (None, ""):
            items.append((f"{c[key]:g}" if isinstance(c[key], (int, float)) else R.esc(c[key]), icon))
    step = size * 2.6
    start = x - step * len(items) if right else x
    for i, (v, icon) in enumerate(items):
        cx = start + i * step
        o.append(f'<text x="{cx}" y="{y}" font-size="{size}" font-weight="300" fill="{ink}">{v}</text>'
                 f'<g transform="translate({cx + size * 0.75} {y - size * 0.78}) scale({size / 42:.3f})">{R.ICONS[icon].format(c=ink)}</g>')
    return "".join(o)


def addr_parts(job):
    a = job.get("address") or "Address"
    return [p.strip() for p in a.rsplit(",", 1)] if "," in a else [a, ""]


def disclaimer(x, y, mute, width=118, size=19):
    return "".join(f'<text x="{x}" y="{y + i * size * 1.42}" font-size="{size}" font-weight="300" fill="{mute}">{R.esc(l)}</text>'
                   for i, l in enumerate(R.wrap(R.DISCLAIMER, width)))


def logo(x, y, w, h, anchor="xMaxYMid"):
    return f'<image href="{R.img_data(R.LOGOS / "10x-dark.svg")}" x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="{anchor} meet"/>'


def north(job, x, y, ink):
    if job.get("north") is None:
        return ""
    return (f'<g transform="translate({x} {y}) rotate({float(job["north"]):g})"><circle r="30" fill="none" stroke="{ink}" stroke-width="2"/>'
            f'<path d="M0 -22 L9 10 L0 4 L-9 10 Z" fill="{ink}"/></g>')


W, H = 2970, 2100


def page_a(job, plan, L):
    """Gallery: plan as big as the page allows, everything else in one quiet band underneath."""
    g, x0, y1, x1, _ = plan_block(plan, (110, 110, W - 110, 1700))
    street, suburb = addr_parts(job)
    o = [g, f'<text x="{x0:.0f}" y="{y1 + 62:.0f}" font-size="26" font-weight="500" letter-spacing="6" fill="{L["mute"]}">'
            f'{R.esc((job.get("floor_title") or "GROUND FLOOR").upper())}</text>',
         f'<rect x="110" y="1800" width="{W - 220}" height="3" fill="{BLUE}"/>',
         f'<text x="110" y="1905" font-size="64" font-weight="300" fill="{L["ink"]}">{R.esc(street)}</text>',
         f'<text x="110" y="1975" font-size="30" font-weight="500" letter-spacing="8" fill="{L["mute"]}">{R.esc(suburb.upper())}</text>',
         counts_svg(job, 1700, 1905, L["ink"], 50, right=True),
         f'<text x="1700" y="1975" font-size="30" font-weight="300" text-anchor="end" fill="{L["mute"]}">{R.esc(R.area_strip(job))}</text>',
         north(job, 1800, 1890, L["ink"]),
         disclaimer(1880, 1890, L["mute"], 62, 17),
         logo(W - 110 - 250, 1860, 250, 118)]
    return o


def page_b(job, plan, L):
    """Architect: monochrome drawing, a title block in the corner like a real drawing sheet."""
    g, x0, y1, x1, _ = plan_block(plan, (150, 260, W - 150, 1640))
    street, suburb = addr_parts(job)
    ink, mute = L["ink"], L["mute"]
    o = [f'<rect x="60" y="60" width="{W - 120}" height="{H - 120}" fill="none" stroke="{ink}" stroke-width="2"/>',
         f'<text x="130" y="175" font-size="28" font-weight="600" letter-spacing="10" fill="{ink}">{R.esc(street.upper())}</text>',
         f'<text x="130" y="220" font-size="22" font-weight="400" letter-spacing="10" fill="{mute}">{R.esc(suburb.upper())}</text>',
         f'<rect x="130" y="245" width="90" height="4" fill="{BLUE}"/>',
         g,
         f'<text x="{(x0 + x1) / 2:.0f}" y="{y1 + 70:.0f}" font-size="24" font-weight="600" letter-spacing="10" text-anchor="middle" fill="{ink}">'
         f'{R.esc((job.get("floor_title") or "GROUND FLOOR").upper())}</text>',
         f'<path d="M60 1760H{W - 60}M1050 1760V{H - 60}M2050 1760V{H - 60}" stroke="{ink}" stroke-width="2"/>',
         f'<text x="130" y="1840" font-size="20" font-weight="600" letter-spacing="6" fill="{mute}">ACCOMMODATION</text>',
         counts_svg(job, 130, 1950, ink, 52, right=False),
         f'<text x="1120" y="1840" font-size="20" font-weight="600" letter-spacing="6" fill="{mute}">AREAS</text>']
    for i, part in enumerate(R.area_strip(job).split("   |   ")):
        k, v = part.split(":")
        o.append(f'<text x="1120" y="{1905 + i * 48}" font-size="30" font-weight="300" fill="{ink}">{R.esc(k)}</text>'
                 f'<text x="1980" y="{1905 + i * 48}" font-size="30" font-weight="500" text-anchor="end" fill="{ink}">{R.esc(v.strip())}</text>')
    o += [north(job, 2000, 1830, ink), disclaimer(2120, 1830, mute, 64, 16), logo(W - 130 - 230, 1940, 230, 100)]
    return o


def page_c(job, plan, L):
    """Warm: paper ground, tonal rooms, a left column that reads like a brochure page."""
    col = 720
    g, x0, y1, x1, _ = plan_block(plan, (col + 80, 140, W - 110, H - 140))
    street, suburb = addr_parts(job)
    ink, mute = L["ink"], L["mute"]
    words, lines, cur = street.split(), [], ""
    for w in words:  # wrap the street onto short lines
        if len(cur) + len(w) > 14 and cur:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    lines.append(cur)
    o = [f'<rect width="{col}" height="{H}" fill="#efe8de"/>',
         f'<text x="110" y="250" font-size="24" font-weight="500" letter-spacing="9" fill="{mute}">FLOOR PLAN</text>']
    for i, ln in enumerate(lines):
        o.append(f'<text x="110" y="{380 + i * 92}" font-size="80" font-weight="300" fill="{ink}">{R.esc(ln)}</text>')
    yy = 380 + len(lines) * 92
    o += [f'<text x="110" y="{yy + 10}" font-size="30" font-weight="500" letter-spacing="9" fill="{mute}">{R.esc(suburb.upper())}</text>',
          f'<rect x="110" y="{yy + 70}" width="80" height="4" fill="{BLUE}"/>',
          counts_svg(job, 110, yy + 210, ink, 50, right=False)]
    for i, part in enumerate(R.area_strip(job).split("   |   ")):
        k, v = part.split(":")
        y = yy + 330 + i * 64
        o.append(f'<text x="110" y="{y}" font-size="32" font-weight="300" fill="{mute}">{R.esc(k)}</text>'
                 f'<text x="{col - 110}" y="{y}" font-size="32" font-weight="500" text-anchor="end" fill="{ink}">{R.esc(v.strip())}</text>'
                 f'<path d="M110 {y + 22}H{col - 110}" stroke="#d9cfc2" stroke-width="1.5"/>')
    o += [north(job, col - 150, 250, ink), disclaimer(110, H - 420, mute, 52, 16), logo(110, H - 200, 260, 110, "xMinYMid"),
          g, f'<text x="{x0:.0f}" y="{y1 + 62:.0f}" font-size="26" font-weight="500" letter-spacing="6" fill="{mute}">'
             f'{R.esc((job.get("floor_title") or "GROUND FLOOR").upper())}</text>']
    return o


def main(slug):
    job_dir = HERE / "jobs" / slug
    job = json.loads((job_dir / "job.json").read_text())
    plan_src = (job_dir / "out" / f"{slug}-10x-plan.svg").read_text()
    out = job_dir / "mockups"
    out.mkdir(exist_ok=True)
    for name, fn in (("a-gallery", page_a), ("b-architect", page_b), ("c-warm", page_c)):
        L = LOOKS[name]
        body = fn(job, restyle_plan(plan_src, L), L)
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
               f'font-family="Poppins, Montserrat, sans-serif"><rect width="{W}" height="{H}" fill="{L["page"]}"/>'
               + "".join(body) + "</svg>")
        R.export(svg, out / name)
        print(out / f"{name}.png")


if __name__ == "__main__":
    main(sys.argv[1])
