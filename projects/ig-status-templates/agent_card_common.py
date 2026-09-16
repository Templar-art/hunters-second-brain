"""Shared builder for Harcourts Property Hub agent-contact cards.
Used by build_agent_card.py (team) and build_solo_agent.py (single agent).
"""

import base64
from pathlib import Path

from build_templates import BRAND_FONTS, DARK_BLUE, LIGHT_BLUE, FONTS, OUT, to_png

HERE = Path(__file__).parent
ASSETS = HERE / "assets"

W, H = 1080, 1350


def b64(path):
    return base64.b64encode(path.read_bytes()).decode()


def initials(name):
    return "".join(part[0].upper() for part in name.split()[:2])


def avatar_svg(cx, cy, r, name, photo_path=None):
    if photo_path is not None:
        img_data = b64(photo_path)
        clip_id = f"clip-{int(cx)}-{int(cy)}"
        return f"""
        <defs><clipPath id="{clip_id}"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath></defs>
        <image href="data:image/png;base64,{img_data}" x="{cx-r}" y="{cy-r}" width="{r*2}" height="{r*2}"
          preserveAspectRatio="xMidYMid slice" clip-path="url(#{clip_id})"/>
        <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{LIGHT_BLUE}" stroke-width="2.5" opacity="0.85"/>
        """
    return f"""
    <circle cx="{cx}" cy="{cy}" r="{r}" fill="#12335a"/>
    <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{LIGHT_BLUE}" stroke-width="2.5" opacity="0.85"/>
    <text x="{cx}" y="{cy + r*0.14}" font-family="Bw Vivant" font-size="{r*0.62}" fill="#ffffff"
      text-anchor="middle" dominant-baseline="middle" letter-spacing="1">{initials(name)}</text>
    """


def build_svg(agents, tagline="Your local property specialists"):
    wordmark = b64(ASSETS / "harcourts-primary-wordmark.png")
    n = len(agents)
    r = 168 if n == 1 else 148
    gap = 96
    total_w = r * 2 * n + gap * (n - 1)
    start_cx = W / 2 - total_w / 2 + r
    centers = [start_cx + i * (r * 2 + gap) for i in range(n)]
    cy = 760 if n == 1 else 730

    avatars = "".join(
        avatar_svg(cx, cy, r, a["name"], a.get("photo")) for cx, a in zip(centers, agents)
    )
    names = "".join(
        f"""
        <text x="{cx}" y="{cy + r + 64}" font-family="Circular Std Book" font-weight="700" font-size="{36 if n==1 else 32}"
          fill="#ffffff" text-anchor="middle">{a['name']}</text>
        <text x="{cx}" y="{cy + r + 102}" font-family="DM Mono" font-size="{21 if n==1 else 19}" fill="#c9d6e6"
          text-anchor="middle" letter-spacing="0.5">{a['phone']}</text>
        """
        for cx, a in zip(centers, agents)
    )

    return f"""
  <svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <linearGradient id="glow" x1="0%" y1="100%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="{DARK_BLUE}"/>
        <stop offset="55%" stop-color="#2c4d74"/>
        <stop offset="100%" stop-color="#a9cdec"/>
      </linearGradient>
      <filter id="grain">
        <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" stitchTiles="stitch" result="n"/>
        <feColorMatrix in="n" type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 0.02 0"/>
      </filter>
    </defs>

    <rect width="{W}" height="{H}" fill="url(#glow)"/>
    <rect width="{W}" height="{H}" filter="url(#grain)"/>

    <image href="data:image/png;base64,{wordmark}" x="{W/2 - 260}" y="190" width="520" height="221"/>
    <line x1="{W/2 - 60}" y1="452" x2="{W/2 + 60}" y2="452" stroke="{LIGHT_BLUE}" stroke-width="2" opacity="0.8"/>
    <text x="{W/2}" y="494" font-family="Circular Std Book" font-size="19" fill="#c9d6e6"
      text-anchor="middle" letter-spacing="1.5" opacity="0.85">{tagline}</text>

    {avatars}
    {names}
  </svg>
"""


def build_html(agents, tagline="Your local property specialists"):
    bw_vivant = b64(BRAND_FONTS / "BwVivant-Black.ttf")
    circular_std = b64(BRAND_FONTS / "CircularStd-Book.ttf")
    dm_mono = b64(FONTS / "DMMono-Regular.ttf")
    svg = build_svg(agents, tagline)
    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
  @font-face {{ font-family: 'Bw Vivant'; src: url(data:font/ttf;base64,{bw_vivant}) format('truetype'); }}
  @font-face {{ font-family: 'Circular Std Book'; src: url(data:font/ttf;base64,{circular_std}) format('truetype'); }}
  @font-face {{ font-family: 'DM Mono'; src: url(data:font/ttf;base64,{dm_mono}) format('truetype'); }}
  @page {{ size: {W/96}in {H/96}in; margin: 0; }}
  * {{ margin:0; padding:0; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
  body {{ width:{W}px; height:{H}px; overflow:hidden; background:{DARK_BLUE}; }}
</style></head>
<body>
{svg}
</body></html>
"""


def build(agents, out_name, tagline="Your local property specialists"):
    OUT.mkdir(exist_ok=True)
    html_path = OUT / f"{out_name}.html"
    png_path = OUT / f"{out_name}.png"
    html_path.write_text(build_html(agents, tagline))
    to_png(html_path, png_path, W, H)
    print("wrote", png_path)
    return png_path
