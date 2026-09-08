#!/usr/bin/env python3
"""Generates the five listing artboards from one spec.

Design Components artboards share nothing at runtime, so every shared value here
would otherwise be hand-copied five times (it drifted twice already). Edit this
file, rerun it, then re-seed the canvas.
"""

from html import escape

LIGHT_BLUE = "#3ba0e8"
NAVY = "#0a1c3e"
WHITE = "#ffffff"

HEROES = {
    "aerial": ("hero-aerial.jpg", "Aerial view of 14 Stonehaven Court, Brookfield"),
    "terrace": ("hero-terrace.jpg", "Firepit terrace at 14 Stonehaven Court, Brookfield"),
}

ADDRESS = "14 Stonehaven Court, Brookfield"

# file stem -> (status chip, hero key, detail line or list of times)
SPEC = {
    "Main": ("Just Listed", "aerial", "Offers over [YOUR PRICE]"),
    "ComingSoon": ("Coming Soon", "terrace", "To market [MONTH]"),
    "JustSold": ("Sold", "aerial", None),
    "SoldOffMarket": ("Sold Off Market", "terrace", "Ask us about off-market opportunities"),
    "OpenHome": ("Open Home", "aerial", ["Saturday 10:00 – 10:30am", "Sunday 11:00 – 11:30am"]),
}

TEMPLATE = """<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@400;600;700;800&display=swap">
  <style>
    body {{ margin: 0; }}
    a {{ color: {light_blue}; }} a:hover {{ color: {white}; }}
  </style>
</helmet>
<div style="position: relative; width: 1080px; height: 1080px; overflow: hidden; background: {navy}; font-family: 'Nunito Sans', 'Avenir Next', 'Segoe UI', system-ui, sans-serif; font-kerning: normal;">
  <img src="{hero_file}" alt="{hero_alt}" style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover;">
  <div style="position: absolute; left: 0; right: 0; top: 0; height: 280px; background: linear-gradient(180deg, rgba(10,28,62,0.58) 0%, rgba(10,28,62,0) 100%);"></div>
  <div style="position: absolute; left: 0; right: 0; bottom: 0; height: 58%; background: {{{{scrimFill}}}};"></div>

  <img src="harcourts-wordmark.png" alt="Harcourts" style="position: absolute; top: 68px; right: 72px; width: 196px; height: auto;">

  <div style="position: absolute; left: 76px; right: 76px; bottom: 84px; display: flex; flex-direction: column; align-items: flex-start; gap: 14px;">
    <div style="font-size: 26px; font-weight: 800; letter-spacing: 0.08em; text-transform: uppercase; color: {white};">{status}</div>
    <div style="display: flex; flex-direction: column; align-items: flex-start; gap: 18px;">
      <div style="font-size: 56px; font-weight: 800; line-height: 1.1; letter-spacing: -0.01em; color: {white}; text-wrap: balance;">{address}</div>
{detail}
    </div>
  </div>
</div>
</x-dc>
<script data-dc-script data-props='{{"scrim":{{"editor":"range","default":0.86,"min":0.4,"max":1,"step":0.02}},"$preview":{{"width":1080,"height":1080}}}}'>
class Component extends DCLogic {{
  renderVals() {{
    const s = this.props.scrim ?? 0.86;
    return {{
      scrimFill: `linear-gradient(180deg, rgba(10,28,62,0) 0%, rgba(10,28,62,${{(s * 0.46).toFixed(3)}}) 42%, rgba(10,28,62,${{s.toFixed(3)}}) 100%)`
    }};
  }}
}}
</script>
</body>
</html>
"""

DETAIL_LINE = '      <div style="font-size: 26px; font-weight: 600; color: rgba(255,255,255,0.92);">{text}</div>'
TIMES_OPEN = '      <div style="display: flex; flex-direction: column; gap: 10px;">'
TIMES_ROW = '        <div style="font-size: 30px; font-weight: 700; color: #ffffff;">{text}</div>'
TIMES_CLOSE = '      </div>'


def detail_markup(detail):
    # Real per-listing copy (address, price, times) is typed by a person and may
    # contain &, <, >, or quotes (e.g. "Smith & Sons Court") - escape it so it can
    # never break the surrounding markup. Spec strings use a literal Unicode en dash
    # (not the &ndash; entity) so a plain escape() is exact, no placeholder needed.
    if detail is None:
        return ""
    if isinstance(detail, list):
        rows = [TIMES_ROW.format(text=escape(t)) for t in detail]
        return "\n".join([TIMES_OPEN, *rows, TIMES_CLOSE])
    return DETAIL_LINE.format(text=escape(detail))


for stem, (status, hero_key, detail) in SPEC.items():
    hero_file, hero_alt = HEROES[hero_key]
    html = TEMPLATE.format(
        light_blue=LIGHT_BLUE, navy=NAVY, white=WHITE,
        hero_file=hero_file, hero_alt=hero_alt,
        status=status, address=escape(ADDRESS),
        detail=detail_markup(detail),
    )
    # collapse the blank line left when an artboard has no detail row
    html = html.replace('</div>\n\n    </div>', '</div>\n    </div>')
    with open(f"{stem}.dc.html", "w") as fh:
        fh.write(html)
    print(f"wrote {stem}.dc.html")
