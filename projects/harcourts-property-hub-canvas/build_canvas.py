#!/usr/bin/env python3
"""Build the 'Datum Line' canvas: survey/blueprint-inspired abstract art
piece for Harcourts Property Hub. Generates canvas.html (inline SVG,
embedded fonts) then rasterizes to canvas.png and canvas.pdf via headless
Chrome, matching the pattern already used by elevra-invoices.
"""

import base64
import math
import subprocess
from pathlib import Path

HERE = Path(__file__).parent
FONTS = Path("/Users/10xhunter/.claude/skills/canvas-design/canvas-fonts")
CHROME = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")

W, H = 1600, 2000

INK = "#dce8f4"        # hairline white-blue, drafting pencil on film
FIELD_DEEP = "#0b1f38"  # deep blueprint navy, edges
FIELD_MID = "#12335a"   # lighter navy, center glow
ACCENT = "#3ba0e8"      # the single point of true information
FAINT = "rgba(220,232,244,0.055)"
FAINT2 = "rgba(220,232,244,0.11)"


def font_b64(name):
    return base64.b64encode((FONTS / name).read_bytes()).decode()


def grid_lines():
    lines = []
    step = 100
    for x in range(160, 1441, step):
        lines.append(f'<line x1="{x}" y1="140" x2="{x}" y2="1860" stroke="{FAINT}" stroke-width="1"/>')
    for y in range(140, 1861, step):
        lines.append(f'<line x1="160" y1="{y}" x2="1440" y2="{y}" stroke="{FAINT}" stroke-width="1"/>')
    return "\n      ".join(lines)


def corner_marks():
    marks = []
    size = 14
    for (cx, cy) in [(120, 120), (1480, 120), (120, 1880), (1480, 1880)]:
        marks.append(
            f'<g stroke="{INK}" stroke-width="1.3" opacity="0.75">'
            f'<line x1="{cx-size}" y1="{cy}" x2="{cx+size}" y2="{cy}"/>'
            f'<line x1="{cx}" y1="{cy-size}" x2="{cx}" y2="{cy+size}"/>'
            f"</g>"
        )
    return "\n      ".join(marks)


def parcel():
    pts = [
        (650, 300, "A", "41.220"),
        (1250, 258, "B", "41.860"),
        (1322, 618, "C", "38.905"),
        (982, 782, "D", "37.410"),
        (640, 648, "E", "39.075"),
    ]
    path = "M " + " L ".join(f"{x},{y}" for x, y, _, _ in pts) + " Z"
    out = [f'<path d="{path}" fill="none" stroke="{INK}" stroke-width="1.6" opacity="0.9"/>']

    cx = sum(p[0] for p in pts) / len(pts)
    cy = sum(p[1] for p in pts) / len(pts)

    for x, y, label, elev in pts:
        ang = math.atan2(y - cy, x - cx)
        dx, dy = math.cos(ang), math.sin(ang)
        tx1, ty1 = x - dy * 11, y + dx * 11
        tx2, ty2 = x + dy * 11, y - dx * 11
        out.append(f'<line x1="{tx1:.1f}" y1="{ty1:.1f}" x2="{tx2:.1f}" y2="{ty2:.1f}" stroke="{INK}" stroke-width="1.4"/>')
        lx, ly = x + dx * 30, y + dy * 30
        out.append(
            f'<text x="{lx:.1f}" y="{ly:.1f}" font-family="DM Mono" font-size="11" '
            f'fill="{INK}" opacity="0.7" text-anchor="middle">{label}</text>'
        )
        out.append(
            f'<text x="{lx:.1f}" y="{ly+14:.1f}" font-family="DM Mono" font-size="9" '
            f'fill="{INK}" opacity="0.4" text-anchor="middle">RL {elev}</text>'
        )

    bx, by = 895, 486
    out.append(f'<circle cx="{bx}" cy="{by}" r="16" fill="none" stroke="{ACCENT}" stroke-width="1" opacity="0.55"/>')
    out.append(f'<circle cx="{bx}" cy="{by}" r="4.5" fill="{ACCENT}"/>')
    out.append(f'<line x1="{bx-24}" y1="{by}" x2="{bx+24}" y2="{by}" stroke="{ACCENT}" stroke-width="0.8" opacity="0.6"/>')
    out.append(f'<line x1="{bx}" y1="{by-24}" x2="{bx}" y2="{by+24}" stroke="{ACCENT}" stroke-width="0.8" opacity="0.6"/>')
    out.append(
        f'<text x="{bx+34}" y="{by+4}" font-family="DM Mono" font-size="11" '
        f'fill="{ACCENT}" opacity="0.85" letter-spacing="1">BM.01</text>'
    )

    # Reduction line: a quiet plumb line dropping from the lowest survey
    # point down to a terminus above the anchor mark, so the vast lower
    # field reads as held in tension rather than simply empty.
    dx, dy = 982, 782
    ty = 1600
    out.append(f'<line x1="{dx}" y1="{dy+6}" x2="{dx}" y2="{ty}" stroke="{INK}" stroke-width="0.7" opacity="0.28" stroke-dasharray="1 5"/>')
    out.append(f'<line x1="{dx-9}" y1="{ty}" x2="{dx+9}" y2="{ty}" stroke="{INK}" stroke-width="1" opacity="0.5"/>')
    out.append(
        f'<text x="{dx+18}" y="{ty+4}" font-family="DM Mono" font-size="9.5" '
        f'fill="{INK}" opacity="0.4" letter-spacing="1">RD 9.98</text>'
    )
    return "\n      ".join(out)


def scale_bar():
    x0, y0 = 200, 1660
    seg = 70
    out = [f'<line x1="{x0}" y1="{y0}" x2="{x0+seg*4}" y2="{y0}" stroke="{INK}" stroke-width="1.2"/>']
    for i in range(5):
        x = x0 + seg * i
        h = 10 if i % 2 == 0 else 6
        out.append(f'<line x1="{x}" y1="{y0-h}" x2="{x}" y2="{y0+h}" stroke="{INK}" stroke-width="1.2"/>')
        out.append(
            f'<text x="{x}" y="{y0+26}" font-family="DM Mono" font-size="10" '
            f'fill="{INK}" opacity="0.55" text-anchor="middle">{i*5}</text>'
        )
    out.append(
        f'<text x="{x0}" y="{y0-22}" font-family="DM Mono" font-size="10" '
        f'fill="{INK}" opacity="0.55" letter-spacing="2">SCALE (M)</text>'
    )
    return "\n      ".join(out)


def compass():
    cx, cy = 1360, 260
    out = [
        f'<circle cx="{cx}" cy="{cy}" r="34" fill="none" stroke="{INK}" stroke-width="0.9" opacity="0.5"/>',
        f'<line x1="{cx}" y1="{cy-46}" x2="{cx}" y2="{cy+30}" stroke="{INK}" stroke-width="1.1" opacity="0.75"/>',
        f'<path d="M {cx-6},{cy-30} L {cx},{cy-46} L {cx+6},{cy-30} Z" fill="{INK}" opacity="0.75"/>',
        f'<text x="{cx}" y="{cy-56}" font-family="DM Mono" font-size="12" fill="{INK}" '
        f'opacity="0.75" text-anchor="middle" letter-spacing="1">N</text>',
    ]
    return "\n      ".join(out)


def margin_text():
    x, y = 1472, 1830
    return (
        f'<text x="{x}" y="{y}" font-family="DM Mono" font-size="10.5" fill="{INK}" '
        f'opacity="0.4" letter-spacing="2.5" transform="rotate(-90 {x} {y})">'
        "37°49'23&quot;S · 144°57'54&quot;E · AHD71"
        "</text>"
    )


def build_svg():
    return f"""
  <svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <radialGradient id="field" cx="42%" cy="34%" r="75%">
        <stop offset="0%" stop-color="{FIELD_MID}"/>
        <stop offset="100%" stop-color="{FIELD_DEEP}"/>
      </radialGradient>
      <filter id="grain">
        <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" stitchTiles="stitch" result="noise"/>
        <feColorMatrix in="noise" type="matrix"
          values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 0.02 0"/>
      </filter>
    </defs>

    <rect width="{W}" height="{H}" fill="url(#field)"/>
    <rect width="{W}" height="{H}" filter="url(#grain)"/>

    <circle cx="-80" cy="-40" r="920" fill="none" stroke="{INK}" stroke-width="1" opacity="0.05"/>

    <rect x="100" y="100" width="{W-200}" height="{H-200}" fill="none" stroke="{INK}" stroke-width="1.1" opacity="0.5"/>
    {grid_lines()}
    {corner_marks()}

    {parcel()}
    {scale_bar()}
    {compass()}
    {margin_text()}

    <text x="180" y="1745" font-family="Italiana" font-size="58" fill="{INK}" letter-spacing="10" opacity="0.94">DATUM</text>
    <text x="182" y="1782" font-family="DM Mono" font-size="11.5" fill="{INK}" opacity="0.5" letter-spacing="3">PLAN REF. 04–26 · PARCEL 5 · AHD71</text>

    <line x1="160" y1="1810" x2="1440" y2="1810" stroke="{INK}" stroke-width="0.6" opacity="0.25"/>
    <text x="1440" y="1745" font-family="DM Mono" font-size="10.5" fill="{INK}" opacity="0.45" text-anchor="end" letter-spacing="2">LOT 5 ON PLAN 04–26</text>
    <text x="1440" y="1764" font-family="DM Mono" font-size="10.5" fill="{INK}" opacity="0.3" text-anchor="end" letter-spacing="2">AREA 812.4 m²</text>
  </svg>
"""


def build_html():
    italiana = font_b64("Italiana-Regular.ttf")
    dm_mono = font_b64("DMMono-Regular.ttf")
    svg = build_svg()
    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
  @font-face {{ font-family: 'Italiana'; src: url(data:font/ttf;base64,{italiana}) format('truetype'); }}
  @font-face {{ font-family: 'DM Mono'; src: url(data:font/ttf;base64,{dm_mono}) format('truetype'); }}
  @page {{ size: {W/96}in {H/96}in; margin: 0; }}
  * {{ margin:0; padding:0; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
  body {{ width:{W}px; height:{H}px; overflow:hidden; background:{FIELD_DEEP}; }}
  svg text {{ dominant-baseline: alphabetic; }}
</style></head>
<body>
{svg}
</body></html>
"""


def to_png(html_path, png_path, scale=2):
    subprocess.run(
        [
            str(CHROME), "--headless=new", "--disable-gpu",
            f"--window-size={W},{H}",
            f"--force-device-scale-factor={scale}",
            "--hide-scrollbars",
            f"--screenshot={png_path}",
            html_path.as_uri(),
        ],
        check=True, capture_output=True,
    )


def to_pdf(html_path, pdf_path):
    subprocess.run(
        [
            str(CHROME), "--headless=new", "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={pdf_path}",
            html_path.as_uri(),
        ],
        check=True, capture_output=True,
    )


def main():
    html_path = HERE / "canvas.html"
    png_path = HERE / "canvas.png"
    pdf_path = HERE / "canvas.pdf"
    html_path.write_text(build_html())
    to_png(html_path, png_path)
    to_pdf(html_path, pdf_path)
    print("wrote", html_path, png_path, pdf_path)


if __name__ == "__main__":
    main()
