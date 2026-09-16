#!/usr/bin/env python3
"""Build the 5 Harcourts Property Hub Instagram status templates
(Coming Soon / Just Listed / Just Sold / Sold Off Market / Open Home Times).

No Canva dependency: HTML + inline SVG rendered to 1080x1080 PNG via
headless Chrome, same pattern as elevra-invoices/make_invoice.py and the
Datum Line canvas piece.

Each template is driven by one dict below (LISTINGS). To reuse for a real
listing: swap `photo` to a real property image path (or leave the gradient
placeholder), edit the text fields, and rerun.

    python3 build_templates.py
"""

import base64
import subprocess
from pathlib import Path

HERE = Path(__file__).parent
ASSETS = HERE / "assets"
OUT = HERE / "output"
BRAND_FONTS = ASSETS / "fonts"
FONTS = Path("/Users/10xhunter/.claude/skills/canvas-design/canvas-fonts")
CHROME = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")

W = H = 1080  # default: 1:1 feed post

WHITE = "#ffffff"
LIGHT_BLUE = "#3ba0e8"
DARK_BLUE = "#0a1c3e"


def font_b64(name):
    return base64.b64encode((FONTS / name).read_bytes()).decode()


def brand_font_b64(name):
    return base64.b64encode((BRAND_FONTS / name).read_bytes()).decode()


def icon_b64():
    return base64.b64encode((ASSETS / "harcourts-icon.png").read_bytes()).decode()


LISTINGS = [
    {
        "slug": "coming-soon",
        "headline": "Coming Soon",
        "kicker": "12 Seaview Terrace, Burleigh Heads",
        "detail": "Register your interest — details Spring 2026",
    },
    {
        "slug": "just-listed",
        "headline": "Just Listed",
        "kicker": "12 Seaview Terrace, Burleigh Heads",
        "detail": "4 Bed · 3 Bath · 2 Car",
    },
    {
        "slug": "just-sold",
        "headline": "Just Sold",
        "kicker": "12 Seaview Terrace, Burleigh Heads",
        "detail": "Sold after multiple offers",
    },
    {
        "slug": "sold-off-market",
        "headline": "Sold Off Market",
        "kicker": "Sanctuary Cove",
        "detail": "Matched privately, before it reached the market",
    },
    {
        "slug": "open-home-times",
        "headline": "Open Home",
        "kicker": "12 Seaview Terrace, Burleigh Heads",
        "detail": "Saturday 10:00 – 10:30am  ·  Wednesday 5:00 – 5:30pm",
    },
]


def build_svg(headline, kicker, detail, w=W, h=H):
    return f"""
  <svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <linearGradient id="hero" x1="0%" y1="100%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="{DARK_BLUE}"/>
        <stop offset="55%" stop-color="#2c4d74"/>
        <stop offset="100%" stop-color="#a9cdec"/>
      </linearGradient>
      <radialGradient id="hotspot" cx="78%" cy="12%" r="55%">
        <stop offset="0%" stop-color="#ffffff" stop-opacity="0.16"/>
        <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
      </radialGradient>
      <filter id="grain">
        <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" stitchTiles="stitch" result="n"/>
        <feColorMatrix in="n" type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 0.025 0"/>
      </filter>
      <linearGradient id="textScrim" x1="0%" y1="100%" x2="0%" y2="0%">
        <stop offset="0%" stop-color="{DARK_BLUE}" stop-opacity="0.55"/>
        <stop offset="100%" stop-color="{DARK_BLUE}" stop-opacity="0"/>
      </linearGradient>
    </defs>

    <rect width="{w}" height="{h}" fill="url(#hero)"/>
    <rect width="{w}" height="{h}" fill="url(#hotspot)"/>
    <rect width="{w}" height="{h}" filter="url(#grain)"/>

    <text x="{w/2}" y="{h/2}" font-family="DM Mono" font-size="12" fill="#ffffff"
      opacity="0.28" text-anchor="middle" letter-spacing="3">REPLACE WITH LISTING PHOTO</text>

    <rect x="0" y="{h*0.62}" width="{w}" height="{h*0.38}" fill="url(#textScrim)"/>

    <g transform="translate(64,64)">
      <circle cx="34" cy="34" r="34" fill="{DARK_BLUE}" opacity="0.92"/>
      <image href="data:image/png;base64,{icon_b64()}" x="14" y="12" width="40" height="45"/>
    </g>

    <g transform="translate(64,{h-64})">
      <text x="0" y="-102" font-family="Bw Vivant" font-size="62"
        fill="{WHITE}" letter-spacing="4">{headline.upper()}</text>
      <text x="0" y="-60" font-family="Circular Std Book" font-size="21" fill="{WHITE}"
        opacity="0.92" letter-spacing="1.2">{kicker}</text>
      <text x="0" y="-30" font-family="Circular Std Book" font-size="17" fill="{WHITE}"
        opacity="0.72" letter-spacing="1">{detail}</text>
    </g>
  </svg>
"""


def build_html(headline, kicker, detail, w=W, h=H):
    bw_vivant = brand_font_b64("BwVivant-Black.ttf")
    circular_std = brand_font_b64("CircularStd-Book.ttf")
    dm_mono = font_b64("DMMono-Regular.ttf")
    svg = build_svg(headline, kicker, detail, w, h)
    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
  @font-face {{ font-family: 'Bw Vivant'; src: url(data:font/ttf;base64,{bw_vivant}) format('truetype'); }}
  @font-face {{ font-family: 'Circular Std Book'; src: url(data:font/ttf;base64,{circular_std}) format('truetype'); }}
  @font-face {{ font-family: 'DM Mono'; src: url(data:font/ttf;base64,{dm_mono}) format('truetype'); }}
  @page {{ size: {w/96}in {h/96}in; margin: 0; }}
  * {{ margin:0; padding:0; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
  body {{ width:{w}px; height:{h}px; overflow:hidden; background:{DARK_BLUE}; }}
</style></head>
<body>
{svg}
</body></html>
"""


def to_png(html_path, png_path, w=W, h=H, scale=2):
    subprocess.run(
        [
            str(CHROME), "--headless=new", "--disable-gpu",
            f"--window-size={w},{h}",
            f"--force-device-scale-factor={scale}",
            "--hide-scrollbars",
            f"--screenshot={png_path}",
            html_path.as_uri(),
        ],
        check=True, capture_output=True,
    )


def build_one(listing, slug_suffix="", w=W, h=H):
    html_path = OUT / f"{listing['slug']}{slug_suffix}.html"
    png_path = OUT / f"{listing['slug']}{slug_suffix}.png"
    html_path.write_text(build_html(listing["headline"], listing["kicker"], listing["detail"], w, h))
    to_png(html_path, png_path, w, h)
    print("wrote", png_path)


def main():
    OUT.mkdir(exist_ok=True)
    for listing in LISTINGS:
        build_one(listing)

    # 4:5 feed banner variant of Sold Off Market (1080x1350)
    sold_off_market = next(l for l in LISTINGS if l["slug"] == "sold-off-market")
    build_one(sold_off_market, slug_suffix="-4x5", w=1080, h=1350)


if __name__ == "__main__":
    main()
