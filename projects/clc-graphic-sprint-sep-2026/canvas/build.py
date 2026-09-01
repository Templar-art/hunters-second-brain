#!/usr/bin/env python3
"""Generates every Coast Life feed-post artboard on the locked CLC grid.

One source of truth for the grid so every slide stays identical on swipe.
Instagram build: carousels capped at 5 slides, one idea and one line per slide.
Edit POSTS below and re-run; then re-seed the canvas.
"""
import json, os, re

W, H = 1080, 1350
H_PLATE = 1440                # 3:4 editorial plate
MX = 112                      # side margin
CW = W - MX * 2               # 856 content width
PANEL_Y, PANEL_H = 52, 760    # photo window
TALL_H = 880                  # image-dominant window for service slides
FOOT_B = 72                   # footer baseline
LOGO_W, LOGO_H = 200, 71

BG_LIGHT = "#f5f7f9"          # cool off-white, faint navy tint (never warm cream)
BG_DEEP  = "#102f41"          # CLC deep navy ground
NAVY     = "#2a4f8d"          # wordmark navy, sampled from the logo
BLUE     = "#1884c7"          # icon / wave blue, sampled from the logo
STEEL    = "#2f6690"          # kicker steel
SKY      = "#97c8e8"          # kicker on deep grounds
INK      = "#16242e"
INK_SOFT = "rgba(22,36,46,0.78)"

FONTS = ("https://fonts.googleapis.com/css2?"
         "family=Poppins:wght@300;400;500;600&display=swap")


def shell(body, ground, link, h=None):
    return f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
  <link rel="stylesheet" href="{FONTS}">
  <style>
    body {{ margin: 0; font-family: Poppins, "Helvetica Neue", Helvetica, Arial, sans-serif; }}
    a {{ color: {link}; }} a:hover {{ color: {BLUE}; }}
  </style>
</helmet>
<div style="position: relative; width: {W}px; height: {h or H}px; background: {ground}; overflow: hidden;">
{body}
</div>
</x-dc>
</body>
</html>
"""


def footer(num, deep):
    logo = "cl-white.png" if deep else "cl-colour.png"
    col = "rgba(151,200,232,0.75)" if deep else "rgba(47,102,144,0.75)"
    left = f'<div style="font-size: 22px; letter-spacing: 0.16em; font-weight: 500; color: {col}; white-space: nowrap; flex: 0 0 auto;">{num}</div>' if num else '<div></div>'
    return f"""  <div style="position: absolute; left: {MX}px; right: {MX}px; bottom: {FOOT_B}px; display: flex; align-items: center; justify-content: space-between;">
{left}
    <img src="{logo}" alt="Coast Life Constructions" style="width: {LOGO_W}px; height: auto; display: block; flex: 0 0 auto;">
  </div>"""


def kicker(text, deep, top=None, abs_pos=True):
    col = SKY if deep else STEEL
    pos = f"position: absolute; left: {MX}px; right: {MX}px; top: {top}px;" if abs_pos else ""
    return (f'<div style="{pos} font-size: 25px; font-weight: 600; letter-spacing: 0.22em; '
            f'text-transform: uppercase; color: {col};">{text}</div>')


def head(text, deep, size=60, weight=300, maxw=CW):
    col = "#ffffff" if deep else INK
    return (f'<h2 style="margin: 0; font-size: {size}px; line-height: 1.12; font-weight: {weight}; '
            f'color: {col}; letter-spacing: -0.005em; max-width: {maxw}px; text-wrap: balance;">{text}</h2>')


def para(text, deep, size=40, maxw=740):
    col = "rgba(255,255,255,0.8)" if deep else INK_SOFT
    return (f'<p style="margin: 0; font-size: {size}px; line-height: 1.45; font-weight: 400; '
            f'color: {col}; max-width: {maxw}px; text-wrap: pretty;">{text}</p>')


def rule(deep, w=180):
    col = "rgba(151,200,232,0.5)" if deep else "rgba(47,102,144,0.35)"
    return f'<div style="width: {w}px; height: 2px; background: {col};"></div>'


# ---------------------------------------------------------------- slide kinds

def hero_size(text):
    """Heroes are set as large as the copy allows — scale is the whole point."""
    n = len(text)
    return 96 if n <= 40 else (84 if n <= 62 else 72)


def photo_cover(s):
    """HERO — full bleed, edge to edge. Deliberately unlike the framed base slides.
    Build stays fully visible above ~58%; type lives in the gradient, per Rob's approved card."""
    size = s.get('hero_size') or hero_size(s['headline'])
    kick = (f'<div style="font-size: 25px; font-weight: 600; letter-spacing: 0.24em; '
            f'text-transform: uppercase; color: {SKY};">{s["kicker"]}</div>') if s.get("kicker") else ""
    tint = (f'<div style="position: absolute; inset: 0; background: rgba(16,47,65,{s["tint"]});"></div>') if s.get("tint") else ""
    sub = (f'<div style="font-size: 34px; font-weight: 400; color: rgba(255,255,255,0.72); '
           f'max-width: 720px;">{s["sub"]}</div>') if s.get("sub") else ""
    body = f"""  <img src="{s['photo']}" alt="" style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; object-position: {s.get('focus','center')}; display: block;">
  {tint}
  <div style="position: absolute; inset: 0; background: linear-gradient(to bottom, rgba(10,31,44,0.40) 0%, rgba(10,31,44,0) 22%);"></div>
  <div style="position: absolute; inset: 0; background: linear-gradient(to top, rgba(8,26,38,0.93) 0%, rgba(8,26,38,0.80) 22%, rgba(9,29,42,0.34) 42%, rgba(10,31,44,0) 58%);"></div>
  <div style="position: absolute; left: {MX}px; right: {MX}px; bottom: {FOOT_B}px; display: flex; flex-direction: column; gap: 24px;">
    <div style="width: 96px; height: 3px; background: {BLUE};"></div>
    {kick}
    <h1 style="margin: 0; font-size: {size}px; line-height: 1.04; font-weight: 300; color: #ffffff; letter-spacing: -0.012em; max-width: {CW}px; text-wrap: balance;">{s['headline']}</h1>
    {sub}
    <div style="margin-top: 26px; display: flex; align-items: center; justify-content: space-between;">
      <div style="font-size: 22px; letter-spacing: 0.16em; font-weight: 500; color: rgba(151,200,232,0.8); white-space: nowrap; flex: 0 0 auto;">{s.get('num','')}</div>
      <img src="cl-white.png" alt="Coast Life Constructions" style="width: {LOGO_W}px; height: auto; display: block; flex: 0 0 auto;">
    </div>
  </div>"""
    return shell(body, BG_DEEP, "#ffffff")


def photo_static(s):
    deep = False
    body = f"""  <div style="position: absolute; left: {MX}px; top: {PANEL_Y}px; width: {CW}px; height: {PANEL_H}px; overflow: hidden; background: #dfe5ea;">
    <img src="{s['photo']}" alt="" style="width: 100%; height: 100%; object-fit: cover; object-position: {s.get('focus','center')}; display: block;">
  </div>
  <div style="position: absolute; left: {MX}px; right: {MX}px; top: {PANEL_Y + PANEL_H + 50}px; display: flex; flex-direction: column; gap: 20px;">
    {kicker(s['kicker'], deep, abs_pos=False)}
    {head(s['headline'], deep, size=s.get('size', 54))}
    <div style="font-size: 28px; font-weight: 400; color: {STEEL};">{s.get('sub','')}</div>
  </div>
{footer(None, deep)}"""
    return shell(body, BG_LIGHT, NAVY)


def ph_static(s):
    """A deliberately marked placeholder frame — no photo on hand, nothing invented."""
    deep = False
    body = f"""  <div style="position: absolute; left: {MX}px; top: {PANEL_Y}px; width: {CW}px; height: {PANEL_H}px; overflow: hidden;
       background: repeating-linear-gradient(135deg, #e4e9ee 0px, #e4e9ee 2px, #dbe2e8 2px, #dbe2e8 14px);
       display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 16px;">
    <div style="width: 120px; height: 120px; border: 2px solid rgba(47,102,144,0.4);"></div>
    <div style="font-size: 22px; font-weight: 600; letter-spacing: 0.2em; text-transform: uppercase; color: {STEEL};">Portrait of Rob required</div>
    <div style="font-size: 22px; color: rgba(22,36,46,0.5);">{s['note']}</div>
  </div>
  <div style="position: absolute; left: {MX}px; right: {MX}px; top: {PANEL_Y + PANEL_H + 50}px; display: flex; flex-direction: column; gap: 20px;">
    {kicker(s['kicker'], deep, abs_pos=False)}
    {head(s['headline'], deep, size=s.get('size', 54))}
    <div style="font-size: 28px; font-weight: 400; color: {STEEL};">{s.get('sub','')}</div>
  </div>
{footer(None, deep)}"""
    return shell(body, BG_LIGHT, NAVY)


def deep_cover(s):
    deep = True
    sub = f'\n    <div style="font-size: 32px; font-weight: 400; color: rgba(255,255,255,0.66);">{s["sub"]}</div>' if s.get("sub") else ""
    body = f"""  <div style="position: absolute; inset: 0; background: radial-gradient(130% 90% at 14% 4%, rgba(24,132,199,0.42) 0%, rgba(24,132,199,0) 64%);"></div>
  {s.get('svg','')}
  <div style="position: absolute; left: {MX}px; right: {MX}px; bottom: 260px; display: flex; flex-direction: column; gap: 26px;">
    <div style="width: 96px; height: 3px; background: {BLUE};"></div>
    {kicker(s['kicker'], deep, abs_pos=False)}
    {head(s['headline'], deep, size=s.get('hero_size') or hero_size(s['headline']))}{sub}
  </div>
{footer(s.get('num'), deep)}"""
    return shell(body, BG_DEEP, "#ffffff")


def light_cover(s):
    deep = False
    sub = f'\n    <div style="font-size: 32px; font-weight: 400; color: {STEEL};">{s["sub"]}</div>' if s.get("sub") else ""
    body = f"""  {s.get('svg','')}
  <div style="position: absolute; left: {MX}px; right: {MX}px; bottom: 260px; display: flex; flex-direction: column; gap: 26px;">
    <div style="width: 96px; height: 3px; background: {BLUE};"></div>
    {kicker(s['kicker'], deep, abs_pos=False)}
    {head(s['headline'], deep, size=s.get('hero_size') or hero_size(s['headline']))}{sub}
  </div>
{footer(s.get('num'), deep)}"""
    return shell(body, BG_LIGHT, NAVY)


def qa(s):
    deep = s.get('deep', False)
    ground = BG_DEEP if deep else BG_LIGHT
    body = f"""  {kicker(s['kicker'], deep, top=150)}
  <div style="position: absolute; left: {MX}px; right: {MX}px; top: 50%; transform: translateY(-64%);">
    {head(s['headline'], deep, size=s.get('size', 76), weight=300)}
  </div>
  <div style="position: absolute; left: {MX}px; top: 50%; transform: translateY(60%); display: flex; flex-direction: column; gap: 26px;">
    {rule(deep, w=120)}
    {''.join(para(p, deep, size=38, maxw=700) for p in s['body'])}
  </div>
{footer(s.get('num'), deep)}"""
    return shell(body, ground, "#ffffff" if deep else NAVY)


def step(s):
    deep = s.get('deep', False)
    ground = BG_DEEP if deep else BG_LIGHT
    numcol = "rgba(151,200,232,0.16)" if deep else "rgba(47,102,144,0.13)"
    body = f"""  <div style="position: absolute; left: {MX - 14}px; top: 300px; font-size: 340px; line-height: 0.8; font-weight: 600; color: {numcol}; letter-spacing: -0.04em;">{s['numeral']}</div>
  <div style="position: absolute; left: {MX}px; right: {MX}px; top: 50%; transform: translateY(-38%); display: flex; flex-direction: column; gap: 30px;">
    {head(s['headline'], deep, size=s.get('size', 76), weight=300)}
    {rule(deep, w=120)}
    {''.join(para(p, deep, size=38, maxw=700) for p in s['body'])}
  </div>
{footer(s.get('num'), deep)}"""
    return shell(body, ground, "#ffffff" if deep else NAVY)


def point(s):
    deep = s.get('deep', False)
    ground = BG_DEEP if deep else BG_LIGHT
    body = f"""  {kicker(s['kicker'], deep, top=150) if s.get('kicker') else ''}
  <div style="position: absolute; left: {MX}px; right: {MX}px; top: 50%; transform: translateY(-52%); display: flex; flex-direction: column; gap: 36px;">
    {head(s['headline'], deep, size=s.get('size', 76), weight=300)}
    {rule(deep, w=120)}
    {''.join(para(p, deep, size=38, maxw=700) for p in s['body'])}
  </div>
{footer(s.get('num'), deep)}"""
    return shell(body, ground, "#ffffff" if deep else NAVY)


def cta(s):
    deep = True
    body = f"""  <div style="position: absolute; inset: 0; background: radial-gradient(110% 80% at 82% 92%, rgba(24,132,199,0.3) 0%, rgba(24,132,199,0) 60%);"></div>
  <div style="position: absolute; left: {MX}px; right: {MX}px; top: 50%; transform: translateY(-54%); display: flex; flex-direction: column; gap: 36px;">
    {head(s['headline'], deep, size=s.get('size', 76), weight=300)}
    {rule(deep, w=120)}
    {para(s['meta'], deep, size=30, maxw=640)}
  </div>
{footer(s.get('num'), deep)}"""
    return shell(body, BG_DEEP, "#ffffff")


def quote(s):
    deep = False
    body = f"""  <div style="position: absolute; left: {MX}px; right: {MX}px; top: 50%; transform: translateY(-54%); display: flex; flex-direction: column; gap: 56px;">
    <blockquote style="margin: 0; font-size: 74px; line-height: 1.2; font-weight: 300; color: {INK}; letter-spacing: -0.005em; text-wrap: pretty;">{s['headline']}</blockquote>
    <div style="display: flex; flex-direction: column; gap: 20px;">
      {rule(deep, w=200)}
      <div style="font-size: 30px; font-weight: 500; color: {STEEL};">{s['attrib']}</div>
      <div style="font-size: 22px; color: rgba(22,36,46,0.5);">{s['note']}</div>
    </div>
  </div>
{footer(None, deep)}"""
    return shell(body, BG_LIGHT, NAVY)


def stack(s):
    deep = False
    items = "".join(
        f'<div style="font-size: 64px; line-height: 1.3; font-weight: {400 if it.get("soft") else 500}; '
        f'color: {"rgba(22,36,46,0.5)" if it.get("soft") else INK}; letter-spacing: -0.01em;">{it["t"]}</div>'
        for it in s['items'])
    body = f"""  {kicker(s['kicker'], deep, top=210)}
  <div style="position: absolute; left: {MX}px; right: {MX}px; top: 240px;">
    {head(s['headline'], deep, size=88, weight=300)}
  </div>
  <div style="position: absolute; left: {MX}px; top: 480px; display: flex; flex-direction: column;">{items}</div>
  <div style="position: absolute; left: {MX}px; bottom: 210px; display: flex; flex-direction: column; gap: 20px;">
    {rule(deep, w=200)}
    {para(s['sub'], deep, size=36, maxw=680)}
  </div>
{footer(None, deep)}"""
    return shell(body, BG_LIGHT, NAVY)



def service(s):
    """Photo on every slide; the service name IS the headline — no eyebrow, no numeral."""
    deep = False
    body = f"""  <div style="position: absolute; left: {MX}px; top: {PANEL_Y}px;">{_fill(s, CW, TALL_H)}</div>
  <div style="position: absolute; left: {MX}px; right: {MX}px; top: {PANEL_Y + TALL_H + 42}px; display: flex; flex-direction: column; gap: 16px;">
    {head(s['headline'], deep, size=s.get('size', 72), weight=300)}
    {para(s['body'][0], deep, size=34, maxw=800)}
  </div>
{footer(s.get('num'), deep)}"""
    return shell(body, BG_LIGHT, NAVY)


def close_graphic(s):
    """The one slide with no photograph — it has to earn the swipe on type alone."""
    deep = True
    body = f"""  <div style="position: absolute; inset: 0; background: radial-gradient(115% 80% at 84% 88%, rgba(24,132,199,0.32) 0%, rgba(24,132,199,0) 62%);"></div>
  <div style="position: absolute; left: {MX}px; right: {MX}px; top: 50%; transform: translateY(-50%); display: flex; flex-direction: column; gap: 44px;">
    {head(s['headline'], deep, size=s.get('size', 92), weight=300, maxw=800)}
    <div style="display: flex; flex-direction: column; gap: 12px;">
      {''.join(f'<div style="font-size: 36px; font-weight: 400; line-height: 1.4; color: rgba(255,255,255,0.76);">{l}</div>' for l in s['lines'])}
    </div>
  </div>
{footer(s.get('num'), deep)}"""
    return shell(body, BG_DEEP, "#ffffff")



def slot(w, h, label, note=""):
    """A marked placeholder frame. Never a stand-in photo — it says what shot is missing."""
    sub = f'<div style="font-size: 20px; color: rgba(22,36,46,0.5); text-align: center; max-width: {w-80}px;">{note}</div>' if note else ""
    return f"""<div style="width: {w}px; height: {h}px; overflow: hidden;
       background: repeating-linear-gradient(135deg, #e4e9ee 0px, #e4e9ee 2px, #dbe2e8 2px, #dbe2e8 14px);
       display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 12px;">
    <div style="width: {min(88, h//4)}px; height: {min(88, h//4)}px; border: 2px solid rgba(47,102,144,0.4);"></div>
    <div style="font-size: 21px; font-weight: 600; letter-spacing: 0.18em; text-transform: uppercase; color: {STEEL}; text-align: center;">{label}</div>
    {sub}
  </div>"""


def _fill(spec, w, h):
    """Either a real photo or a marked slot, same footprint."""
    if spec.get("photo"):
        return (f'<div style="width: {w}px; height: {h}px; overflow: hidden; background: #dfe5ea;">'
                f'<img src="{spec["photo"]}" alt="" style="width: 100%; height: 100%; object-fit: cover; '
                f'object-position: {spec.get("focus","center")}; display: block;"></div>')
    return slot(w, h, spec.get("label", "Image required"), spec.get("note", ""))


def detail_spread(s):
    """Two-image detail spread: large primary, small secondary, caption in the remaining column."""
    deep = False
    PRIM_H, SEC_H = 700, 340
    ROW_Y = PANEL_Y + PRIM_H + 24
    COL = (CW - 32) // 2
    body = f"""  <div style="position: absolute; left: {MX}px; top: {PANEL_Y}px;">{_fill(s['primary'], CW, PRIM_H)}</div>
  <div style="position: absolute; left: {MX}px; right: {MX}px; top: {ROW_Y}px; display: flex; gap: 32px; align-items: flex-start;">
    {_fill(s['secondary'], COL, SEC_H)}
    <div style="width: {COL}px; display: flex; flex-direction: column; gap: 18px; padding-top: 4px;">
      <h2 style="margin: 0; font-size: 46px; line-height: 1.14; font-weight: 300; color: {INK}; letter-spacing: -0.005em; text-wrap: balance;">{s['headline']}</h2>
      <p style="margin: 0; font-size: 28px; line-height: 1.45; font-weight: 400; color: {INK_SOFT};">{s['body'][0]}</p>
    </div>
  </div>
{footer(s.get('num'), deep)}"""
    return shell(body, BG_LIGHT, NAVY)


# ---------------------------------------------------------------- editorial plate
# Structure extracted from a supplied reference: brand mark top, inset image,
# tracked caption bottom, even vertical rhythm, ground tone drawn from the
# photograph itself. Mechanism only — no reference asset, mark or wording is used.

BRAND_HUE = 211 / 360      # between the logo's #1884c7 and #2a4f8d
_GROUND_CACHE = {}

def ground_from(photo, variant='blue'):
    """A Coast Life ground, varied per post.

    The mechanism is borrowed — one ground per post, derived from its photograph,
    so the grid reads as one book. The HUE is not: it is locked to Coast Life's own
    blue family, so only the value moves. Sampling the photo's hue produced sage,
    tan and greige — a different brand's world.
    """
    key = (photo, variant)
    if not photo:
        return {"light": "#e8eaec", "grey": "#a9adb1"}.get(variant, "#1d3a52")
    if key in _GROUND_CACHE:
        return _GROUND_CACHE[key]
    from PIL import Image
    import colorsys
    im = Image.open(photo).convert("RGB")
    im.thumbnail((60, 60))
    px = list(im.get_flattened_data()) if hasattr(im, "get_flattened_data") else list(im.getdata())
    r = sum(p[0] for p in px) / len(px) / 255
    g = sum(p[1] for p in px) / len(px) / 255
    b = sum(p[2] for p in px) / len(px) / 255
    ph, pl, ps = colorsys.rgb_to_hls(r, g, b)

    # hue: Coast Life blue, nudged a few degrees by the image so posts differ subtly
    h = (BRAND_HUE + (ph - 0.5) * 0.035) % 1.0
    # value from the photograph; hue stays Coast Life's. Ranges per variant.
    if variant == 'light':
        l = 0.855 + pl * 0.085
        l = min(max(l, 0.850), 0.940)
        sat = 0.105 - (l - 0.850) * 0.50
    elif variant == 'grey':
        l = 0.600 + pl * 0.150
        l = min(max(l, 0.600), 0.750)
        sat = 0.040
    else:
        l = 0.19 + pl * 0.32
        l = min(max(l, 0.17), 0.42)   # ceiling holds the white caption at >=4.5:1
        sat = 0.36 - (l - 0.17) * 0.40

    rr, gg, bb = colorsys.hls_to_rgb(h, l, sat)
    out = "#%02x%02x%02x" % (int(rr * 255), int(gg * 255), int(bb * 255))
    _GROUND_CACHE[key] = out
    return out


def _ink_for(variant, ground):
    """Pale tint on the deep ground; the brand dark ink on light and grey."""
    if variant in ("light", "grey"):
        return "#16242e"
    return _tint(ground)


def _logo_for(variant):
    # The real two-tone colour mark on light grounds, the official white master on deep.
    # Never a flat single-colour silhouette — that has been rejected before.
    return "cl-colour.png" if variant in ("light", "grey") else "cl-white.png"


def _tint(hex_ground, l=0.955, sat=0.10):
    import colorsys
    r, g, b = (int(hex_ground[i:i+2], 16) / 255 for i in (1, 3, 5))
    h, _, _ = colorsys.rgb_to_hls(r, g, b)
    rr, gg, bb = colorsys.hls_to_rgb(h, l, sat)
    return "#%02x%02x%02x" % (int(rr * 255), int(gg * 255), int(bb * 255))


# plate geometry on 1080 x 1440
PL_TOP      = 150
PL_LOGO_W   = 340
PL_LOGO_H   = 120
PL_IMG_W    = 636
PL_IMG_H    = 696
PL_IMG_Y    = 396
PL_CAP_Y    = 1238


def plate_text(s):
    """Close plate: no photograph. The statement occupies the image band."""
    v = s.get("variant", "blue")
    ground = s.get("ground") or ground_from(None, v)
    ink = _ink_for(v, ground)
    return shell(f"""  <img src="{_logo_for(v)}" alt="Coast Life Constructions" style="position: absolute; left: 50%; top: {PL_TOP}px; transform: translateX(-50%); width: {PL_LOGO_W}px; height: auto; display: block; opacity: {0.96 if v in ("light","grey") else 0.9};">
  <div style="position: absolute; left: 50%; top: {PL_IMG_Y}px; transform: translateX(-50%); width: {PL_IMG_W + 40}px; height: {PL_IMG_H}px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 34px; text-align: center;">
    <div style="font-size: 58px; line-height: 1.18; font-weight: 300; color: {ink}; letter-spacing: -0.005em; text-wrap: balance;">{s['caption']}</div>
    <div style="width: 76px; height: 2px; background: {ink}; opacity: 0.5;"></div>
  </div>
  <div style="position: absolute; left: 50%; top: {PL_CAP_Y}px; transform: translateX(-50%); width: {PL_IMG_W + 60}px; text-align: center;
       font-size: 23px; font-weight: 500; letter-spacing: 0.15em; line-height: 1.62; color: {ink}; opacity: {0.7 if v in ('light','grey') else 0.82};">{s.get('meta','').upper()}</div>""",
                 ground, ink, h=H_PLATE)


def plate(s):
    v = s.get("variant", "blue")
    ground = s.get("ground") or ground_from(s.get("photo"), v)
    ink = _ink_for(v, ground)
    cap = s["caption"].upper()
    if s.get("photo"):
        tint = (f'<div style="position: absolute; inset: 0; background: {ground}; opacity: {s["tint"]};"></div>'
                if s.get("tint") else "")
        art = (f'<img src="{s["photo"]}" alt="" style="width: 100%; height: 100%; object-fit: cover; '
               f'object-position: {s.get("focus","center")}; display: block;">{tint}')
    else:
        art = slot(PL_IMG_W, PL_IMG_H, s.get("label", "Image required"), s.get("note", ""))
    body = f"""  <img src="{_logo_for(v)}" alt="Coast Life Constructions" style="position: absolute; left: 50%; top: {PL_TOP}px; transform: translateX(-50%); width: {PL_LOGO_W}px; height: auto; display: block; opacity: {0.96 if v in ("light","grey") else 0.9};">
  <div style="position: absolute; left: 50%; top: {PL_IMG_Y}px; transform: translateX(-50%); width: {PL_IMG_W}px; height: {PL_IMG_H}px; overflow: hidden; background: rgba(0,0,0,0.06); position: absolute;">
{art}
  </div>
  <div style="position: absolute; left: 50%; top: {PL_CAP_Y}px; transform: translateX(-50%); width: {PL_IMG_W + 60}px; text-align: center;
       font-size: 23px; font-weight: 500; letter-spacing: 0.15em; line-height: 1.62; color: {ink}; opacity: {0.78 if v in ("light","grey") else 0.9}; text-wrap: balance;">{cap}</div>"""
    return shell(body, ground, ink, h=H_PLATE)

KINDS = {"plate": plate, "plate_text": plate_text, "service": service, "detail_spread": detail_spread, "close_graphic": close_graphic, "photo_cover": photo_cover, "photo_static": photo_static, "ph_static": ph_static,
         "deep_cover": deep_cover, "light_cover": light_cover, "qa": qa, "step": step,
         "point": point, "cta": cta, "quote": quote, "stack": stack}

# ---------------------------------------------------------------- line motifs

SVG_ROOFS = f'''<svg style="position: absolute; right: 74px; top: 700px; width: 640px; height: 380px; opacity: 0.5;" viewBox="0 0 320 190" fill="none" stroke="{BLUE}" stroke-width="1.6" stroke-linejoin="round">
    <path d="M8 120 L48 84 L88 120 M8 120 v52 h80 v-52"/>
    <path d="M112 120 L152 84 L192 120 M112 120 v52 h80 v-52 M152 120 v52" />
    <path d="M216 104 L256 62 L296 104 M216 104 v68 h80 v-68 M240 172 v-40 h32 v40"/>
  </svg>'''

SVG_PLAN = f'''<svg style="position: absolute; right: -70px; top: 80px; width: 720px; height: 720px; opacity: 0.26;" viewBox="0 0 200 200" fill="none" stroke="{NAVY}" stroke-width="1.4">
    <rect x="16" y="40" width="150" height="112"/>
    <path d="M16 96h150M92 40v112"/>
    <rect x="30" y="112" width="30" height="40"/>
    <path d="M124 96v56M124 124h42"/>
  </svg>'''

SVG_COAST = f'''<svg style="position: absolute; right: 30px; top: 0; width: 340px; height: 1350px; opacity: 0.3;" viewBox="0 0 120 450" fill="none" stroke="{BLUE}" stroke-width="1.6" stroke-linejoin="round">
    <path d="M92 0c-6 22-4 38 4 54 9 18 6 32-6 46-14 16-18 30-10 46 9 18 6 33-8 48-13 14-16 28-8 44 9 18 5 34-9 49-12 13-15 27-8 42 8 17 6 33-7 47-11 12-14 25-8 39 5 12 4 22-2 35"/>
    <path d="M112 0c-8 26-6 44 3 62 10 20 7 35-7 51-15 17-19 32-10 49 9 19 6 35-9 51-14 15-17 30-9 47 9 19 5 36-10 52-13 14-16 29-8 45 8 17 6 34-7 49-12 13-15 27-9 42" opacity="0.55"/>
  </svg>'''

SVG_COAST_DEEP = f'''<svg style="position: absolute; right: 20px; top: 0; width: 330px; height: 1350px; opacity: 0.2;" viewBox="0 0 120 450" fill="none" stroke="{SKY}" stroke-width="1.6" stroke-linejoin="round">
    <path d="M92 0c-6 22-4 38 4 54 9 18 6 32-6 46-14 16-18 30-10 46 9 18 6 33-8 48-13 14-16 28-8 44 9 18 5 34-9 49-12 13-15 27-8 42 8 17 6 33-7 47-11 12-14 25-8 39 5 12 4 22-2 35"/>
    <path d="M112 0c-8 26-6 44 3 62 10 20 7 35-7 51-15 17-19 32-10 49 9 19 6 35-9 51-14 15-17 30-9 47 9 19 5 36-10 52-13 14-16 29-8 45 8 17 6 34-7 49-12 13-15 27-9 42" opacity="0.55"/>
  </svg>'''

SVG_DOC = f'''<svg style="position: absolute; right: -30px; top: 90px; width: 660px; height: 660px; opacity: 0.2;" viewBox="0 0 200 200" fill="none" stroke="{SKY}" stroke-width="1.4">
    <rect x="30" y="24" width="104" height="140"/>
    <rect x="58" y="46" width="104" height="140"/>
    <path d="M74 78h72M74 100h72M74 122h50"/>
  </svg>'''


def n(i, total):
    return f"{i:02d} / {total:02d}"


# ---------------------------------------------------------------------- posts
# Copy is verbatim from PLAN.md. Nothing here is invented.

POSTS = []

def P(**kw):
    POSTS.append(kw)

# Every post is anchored to a service: new builds, extensions, renovations,
# secondary dwellings. Copy is grounded in Coast Life's own published pages.

P(id="P00", page="Lead · Who we service", date="Carousel", pillar="Services & positioning",
  objective="Profile visits", cta="Ready to get started?",
  caption="New builds, extensions, renovations.\n\nThree service lines, and one builder across all of them, from first consultation through to handover.\n\nIf you are assessing which applies to your property, that is a conversation worth having early.",
  tags="#CoastLifeConstructions #GoldCoastBuilder #CustomHomes #HomeRenovation #HomeExtension #GoldCoastHomes #CustomHomeBuilder #DesignAndBuild #QLDBuilder #Burleigh #Bonogin #VarsityLakes #ResidentialConstruction",
  approve="Confirm which service each of the three photos actually belongs to — new build, extension or renovation. Their site only confirms Gundara Street as a renovation.",
  slides=[
    dict(kind="photo_cover", name="Main", photo="hero-crew.jpg", focus="center 38%",
         headline="New builds, extensions, renovations.",
         sub="Three service lines. One builder, from first consultation to handover.", num=n(1, 5)),
    dict(kind="service", photo="newbuild-frame.jpg", focus="center 46%", headline="New builds", num=n(2, 5),
         body=["Designed to the block, the orientation and the way you intend to live."]),
    dict(kind="service", photo="extension-under.jpg", focus="center 52%", headline="Extensions", num=n(3, 5),
         body=["Additional space without relocating. Ground floor, second storey, or beneath the home."]),
    dict(kind="service", photo="kitchen.jpg", focus="center 50%", headline="Renovations", num=n(4, 5),
         body=["For homes that are structurally sound but no longer laid out well."]),
    dict(kind="close_graphic", headline="Ready to get started?", num=n(5, 5),
         lines=["Tell us which service applies to your property.",
                "Gold Coast · QBCC licensed · Master Builders Queensland"]),
])

P(id="P01", page="Post 1 · New builds", date="Tue 8 Sep · Carousel", pillar="Services & positioning",
  objective="Enquiries", cta="Ready to get started?",
  caption="A custom build is a sequence of decisions, and the early ones carry the most weight.\n\nThe block, the layout, the materials. Settle those three properly and the remainder of the build runs considerably more predictably.\n\nSimple, well chosen materials often make a more timeless result.",
  tags="#CoastLifeConstructions #GoldCoastBuilder #CustomHomes #CustomHomeBuilder #NewBuild #BuildingAHome #GoldCoastHomes #DesignAndBuild #QLDBuilder #Burleigh #ResidentialConstruction",
  approve="All three points condense their own blog article on early custom-build decisions. No approval timeframe or council outcome may be implied.",
  slides=[
    dict(kind="photo_cover", name="P01Cover", kicker="New builds", photo="chambers.jpg", focus="center 62%",
         headline="A custom build is determined long before it begins",
         sub="The three decisions that carry the most weight.", num=n(1, 5)),
    dict(kind="point", kicker="One", headline="The block determines the design", size=70, num=n(2, 5),
         body=["Levels, drainage, soil, orientation and access define what can be built."]),
    dict(kind="point", deep=True, kicker="Two", headline="The layout is the house", num=n(3, 5), photo="mondaro-corner.jpg", focus="center 50%",
         body=["Circulation, natural light, and the connection between inside and out. Everything else is finish."]),
    dict(kind="point", kicker="Three", headline="Choose materials early", num=n(4, 5),
         body=["Late selections are the most common cause of avoidable delay."],
         photo="mondaro-ply.jpg", focus="center 50%"),
    dict(kind="close_graphic", headline="Ready to get started?", num=n(5, 5),
         lines=["Bring your site details and a concept. We will advise what is achievable.",
                "Custom homes · Gold Coast"]),
])

P(id="P02", page="Post 2 · Warranty", date="Thu 10 Sep · Static", pillar="Trust & process",
  objective="Trust", cta="Our full process is on the website — link in bio.",
  caption="Handover is not the end of the job.\n\nNew build, extension or renovation, every project carries a one-year maintenance warranty in addition to the seven-year QBCC structural warranty. Twelve months to occupy the home, identify the small items, and have us return and resolve them.\n\nIt is set out in writing on our process page.",
  tags="#CoastLifeConstructions #GoldCoastBuilder #QBCC #MasterBuildersQLD #CustomHomes #HomeRenovation #HomeWarranty #GoldCoastHomes #QLDBuilder #ResidentialConstruction",
  approve="Warranty wording is verbatim from their process page — confirm it is still current for 2026 contracts. Highest-risk claim in the sprint.",
  slides=[
    dict(kind="photo_cover", name="P02Warranty", photo="living.jpg", focus="center 46%",
         headline="One year of maintenance cover, on top of the seven-year QBCC structural warranty.",
         hero_size=58, sub="New builds · Extensions · Renovations"),
])

P(id="P03", page="Post 3 · Extensions", date="Sun 13 Sep · Carousel", pillar="Services & positioning",
  objective="Saves", cta="Ready to get started?",
  caption="Three ways to add space without relocating.\n\nGround floor, second storey, or beneath the home. Which one suits depends on the block, the levels, and the disruption you can accommodate.\n\nAn extension can often be staged so you remain in the home throughout.",
  tags="#CoastLifeConstructions #GoldCoastBuilder #HomeExtension #HomeRenovation #SecondStorey #GoldCoastHomes #CustomHomeBuilder #DesignAndBuild #QLDBuilder #Burleigh #Bonogin #ResidentialConstruction",
  approve="Three extension types are taken from their own blog. Do not state that any given option is available on a reader's block — that depends on council and the site.",
  slides=[
    dict(kind="photo_cover", name="P03Cover", kicker="Extensions", photo="pool.jpg", focus="center 55%",
         headline="Three ways to add space without relocating",
         sub="Ground floor, second storey, or beneath the home.", num=n(1, 5)),
    dict(kind="point", kicker="Out the back", headline="Ground-floor addition", num=n(2, 5),
         body=["The most straightforward option where the block has room and the levels permit."]),
    dict(kind="point", deep=True, kicker="Up", headline="Second storey", num=n(3, 5),
         body=["Additional floor area on the existing footprint. The structure below determines what is possible."]),
    dict(kind="point", kicker="Underneath", headline="Build in beneath the home", num=n(4, 5),
         body=["Common on sloping Gold Coast blocks, and typically the least disruptive."],
         photo="mondaro-sandstone.jpg", focus="center 50%"),
    dict(kind="close_graphic", headline="Ready to get started?", num=n(5, 5),
         lines=["Send your address and the space you need. We will assess the site.",
                "Extensions and additions · Gold Coast"]),
])

P(id="P04", page="Post 4 · Renovations", date="Tue 15 Sep · Carousel", pillar="Services & positioning",
  objective="Saves", cta="Ready to get started?",
  caption="What we assess first on a renovation.\n\nWhat the home is failing to do, what the layout should become, and what is achievable within the budget.\n\nKitchens and bathrooms attract the attention, but it is usually the layout that determines how a home functions.",
  tags="#CoastLifeConstructions #GoldCoastBuilder #HomeRenovation #RenovationGoldCoast #KitchenRenovation #BathroomRenovation #GoldCoastHomes #CustomHomeBuilder #QLDBuilder #Bonogin #ResidentialConstruction",
  approve="Points condense their own 'what adds the most value when renovating' article. No ROI, percentage or dollar claim of any kind.",
  slides=[
    dict(kind="photo_cover", name="P04Cover", kicker="Renovations", photo="reno-portrait.jpg", focus="center 45%",
         headline="What we assess first on a renovation",
         sub="Three questions, in this order.", num=n(1, 5)),
    dict(kind="point", kicker="First", headline="What is the home failing to do?", size=70, num=n(2, 5),
         body=["Space, layout, condition, or a combination. The answer defines the scope."]),
    dict(kind="point", deep=True, kicker="Second", headline="What should the layout become?", num=n(3, 5),
         body=["Opening living areas, improving circulation, increasing natural light."]),
    dict(kind="point", kicker="Third", headline="What is achievable within the budget?", size=70, num=n(4, 5),
         body=["Established early, so nothing is designed that cannot be delivered."]),
    dict(kind="close_graphic", headline="Ready to get started?", num=n(5, 5),
         lines=["A site walkthrough answers all three.",
                "Renovations and extensions · Gold Coast"]),
])

P(id="P05", hero="kitchen.jpg", page="Post 5 · Client review", date="Thu 17 Sep · Static", pillar="Social proof",
  objective="Trust", cta="More client reviews are on our website.",
  caption="Naomi's renovation, Bonogin.\n\nThe part of her review that stayed with us was not about the finish. It was about being kept informed throughout. That is the part within our control every day, on every project.\n\nThank you Naomi.",
  tags="#CoastLifeConstructions #GoldCoastBuilder #ClientReview #HomeRenovation #Bonogin #GoldCoastHomes #CustomHomeBuilder #QLDBuilder #RenovationGoldCoast",
  approve="HIGHEST SENSITIVITY. The quote shown is a paraphrase and must be replaced with the verbatim published review. Get Naomi's written permission for name and suburb in a graphic. Confirm the job was a renovation before labelling it one.",
  slides=[
    dict(kind="quote", name="P05Review",
         headline="“We were kept fully informed the whole way through.”",
         attrib="Naomi Ortado · Renovation, Bonogin",
         note="Verbatim wording, service type and written permission to be confirmed before publishing."),
])

P(id="P06", hero="drawings.jpg", hero_tint=0.30, page="Post 6 · Which one is yours", date="Sun 20 Sep · Carousel", pillar="Educational",
  objective="Saves", cta="Ready to get started?",
  caption="Renovate, extend, or start again.\n\nBegin with the problem, not the solution. Is it space, layout, condition, or a combination? The answer generally makes the decision for you.\n\nRenovations and extensions can appear cheaper initially and carry more unknowns. New builds are more predictable but require full design and a longer approval process. Neither is automatically correct.",
  tags="#CoastLifeConstructions #GoldCoastBuilder #HomeRenovation #HomeExtension #KnockdownRebuild #CustomHomeBuilder #GoldCoastHomes #DesignAndBuild #QLDBuilder #Burleigh #ResidentialConstruction",
  approve="Condensed from their own 'where to start' article. Never imply an approval timeframe or a council outcome.",
  slides=[
    dict(kind="photo_cover", name="P06Cover", photo="drawings.jpg", focus="center 42%", tint=0.55,
         headline="Renovate, extend, or start again?",
         sub="Begin with the problem, not the solution.", num=n(1, 5)),
    dict(kind="step", numeral="01", headline="Renovate", num=n(2, 5),
         body=["For homes that are structurally sound but no longer laid out well."]),
    dict(kind="step", deep=True, numeral="02", headline="Extend", num=n(3, 5),
         body=["The home functions well. There is not enough of it."]),
    dict(kind="step", numeral="03", headline="Start again", num=n(4, 5),
         body=["Repair costs approach the cost of building new."]),
    dict(kind="close_graphic", headline="Ready to get started?", num=n(5, 5),
         lines=["If you are unsure which applies, that is the first conversation.",
                "Longer version on our blog · link in bio"]),
])

P(id="P07", page="Post 7 · Secondary dwellings", date="Tue 22 Sep · Carousel", pillar="Services & positioning",
  objective="Enquiries", cta="Ready to get started?",
  caption="Secondary dwellings — the one we get asked about most often lately.\n\nSelf-contained living on the same block. Family, guests, or rental income. Its own kitchen, bathroom and living space.\n\nWhat's possible comes down to your lot, your zoning and your council, so it's worth checking before you get attached to a plan.",
  tags="#CoastLifeConstructions #GoldCoastBuilder #SecondaryDwelling #GrannyFlatQLD #HomeExtension #MultigenerationalLiving #GoldCoastHomes #CustomHomeBuilder #QLDBuilder #ResidentialConstruction",
  approve="Do NOT publish a floor-area figure, a zoning rule, or any suggestion that approval is likely. Their blog cites general council guidance only. Also confirm 'asked about most often lately' with Rob — drop the line if he can't back it.",
  slides=[
    dict(kind="photo_cover", name="P07Cover", kicker="Secondary dwellings", photo="rear-dwelling.jpg", focus="62% 58%",
         headline="A second dwelling on the block you already own",
         sub="Family, guests, or rental income.", num=n(1, 5)),
    dict(kind="point", kicker="What it is", headline="Self-contained, on the same lot", size=70, num=n(2, 5),
         body=["Its own kitchen, bathroom, bedroom and living space."]),
    dict(kind="point", deep=True, kicker="What it’s for", headline="Independent accommodation on one title", size=66, num=n(3, 5),
         body=["Multi-generational living, guest accommodation, or rental return."]),
    dict(kind="point", kicker="What decides it", headline="Zoning and council determine what is possible", size=66, num=n(4, 5),
         body=["Worth confirming before a design is committed to."]),
    dict(kind="close_graphic", headline="Ready to get started?", num=n(5, 5),
         lines=["Send your address and we will confirm what is worth exploring.",
                "Secondary dwellings · Gold Coast"]),
])

P(id="P08", hero="chambers.jpg", page="Post 8 · Service area", date="Thu 24 Sep · Static", pillar="Services & positioning",
  objective="Local awareness", cta="If you're nearby and thinking about a project, we're easy to get hold of.",
  caption="Where we build.\n\nBurleigh, Bonogin, Varsity Lakes and across the Gold Coast. New builds, extensions and renovations.\n\nIf you are in the area and considering a project, we are straightforward to reach.",
  tags="#CoastLifeConstructions #GoldCoastBuilder #GoldCoastHomes #Burleigh #Bonogin #VarsityLakes #CustomHomeBuilder #HomeRenovation #HomeExtension #QLDBuilder #ResidentialConstruction",
  approve="Only Burleigh, Bonogin and Varsity Lakes are supported by public evidence. Do not add a suburb Rob hasn't confirmed. Northern NSW and Brisbane stay off until he confirms licensing and appetite.",
  slides=[
    dict(kind="stack", name="P08ServiceArea", kicker="Service area", headline="Where we build", svg=SVG_COAST,
         items=[dict(t="Burleigh"), dict(t="Bonogin"), dict(t="Varsity Lakes"),
                dict(t="and across the Gold Coast", soft=True)],
         sub="New builds, extensions and renovations."),
])

P(id="P09", hero="reno-portrait.jpg", page="Post 9 · Renovation mistakes", date="Sun 27 Sep · Carousel", pillar="Educational",
  objective="Saves", cta="Ready to get started?",
  caption="Three renovation planning errors we see every year. Each is easier to avoid at planning stage than to correct once work has started.\n\nFinishes selected too late. No contingency for what sits behind the wall. Expectations that were never stated.\n\nNone of them are dramatic. They are simply expensive.",
  tags="#CoastLifeConstructions #GoldCoastBuilder #HomeRenovation #RenovationPlanning #RenovationGoldCoast #CustomHomeBuilder #GoldCoastHomes #QLDBuilder #Burleigh #ResidentialConstruction",
  approve="'Simple, well chosen materials often create a more timeless result' is near-verbatim from their blog — confirm Rob is happy for it to become a signature line.",
  slides=[
    dict(kind="deep_cover", name="P09Cover", kicker="Renovations", svg=SVG_DOC,
         headline="Three renovation planning errors we see every year",
         sub="All three are avoidable at planning stage.", num=n(1, 5)),
    dict(kind="point", kicker="One", headline="Choosing finishes last", num=n(2, 5),
         body=["The most common cause of avoidable delay."]),
    dict(kind="point", deep=True, kicker="Two", headline="Leaving no contingency", num=n(3, 5),
         body=["Every existing home holds something that has not yet been seen."]),
    dict(kind="point", kicker="Three", headline="Leaving expectations unspoken", size=70, num=n(4, 5),
         body=["Scope, programme and communication. Agreed early, or disputed later."]),
    dict(kind="close_graphic", headline="Ready to get started?", num=n(5, 5),
         lines=["Planning a project for next year? Planning stage is the time to review it.",
                "Renovations · Gold Coast"]),
])

P(id="P10", page="Post 10 · One builder", date="Tue 29 Sep · Carousel", pillar="Trust & process",
  objective="Trust", cta="Ready to get started?",
  caption="New build, extension or renovation, it is the same builder throughout.\n\nRob takes the first call, attends the site, prices the work, runs the project and hands it over. There is no handover between staff, and no project manager you meet once.\n\nIt is the principal reason we take on only one or two projects at a time.",
  tags="#CoastLifeConstructions #GoldCoastBuilder #FamilyOwnedBusiness #CustomHomeBuilder #HomeRenovation #GoldCoastHomes #DesignAndBuild #QLDBuilder #VarsityLakes #ResidentialConstruction",
  approve="Rob is the point of contact from first chat to handover — their own published claim. Do NOT say Rob is on site every stage or every day; that wording is unconfirmed and previously flagged.",
  slides=[
    dict(kind="photo_cover", name="P10Cover", photo="team.jpg", focus="42% 36%",
         headline="Same builder, first call to handover",
         sub="Across all three service lines.", num=n(1, 5)),
    dict(kind="point", kicker="On a new build", headline="Rob attends the site with you", size=70, num=n(2, 5),
         body=["Before there is a design, let alone a price."]),
    dict(kind="point", deep=True, kicker="On an extension", headline="One person is accountable for the disruption", size=66, num=n(3, 5),
         body=["You remain in the home throughout. Accountability matters."]),
    dict(kind="point", kicker="On a renovation", headline="No handover between staff", num=n(4, 5),
         body=["The person who quoted it is the person who finishes it."],
         photo="mondaro-saw.jpg", focus="center 50%"),
    dict(kind="close_graphic", headline="Ready to get started?", num=n(5, 5),
         lines=["Rob takes the first call himself.",
                "Coast Life Constructions · Gold Coast"]),
])

P(id="P11", page="Post 11 · Meet Rob", date="Thu 1 Oct · Static", pillar="People & brand story",
  objective="Profile visits", cta="Say hello — details are in the bio.",
  caption="Rob Williamson, builder and director, and the person you will be dealing with.\n\nFirst consultation, site visit, quote, contract, construction, handover. The same builder throughout, whether the project is a new build, an extension or a renovation.\n\nOver twenty years in construction, and still the one answering the phone.",
  tags="#CoastLifeConstructions #GoldCoastBuilder #MeetTheBuilder #FamilyOwnedBusiness #CustomHomeBuilder #GoldCoastHomes #QLDBuilder #HomeRenovation #ResidentialConstruction",
  approve="Needs Rob's photo and permission. 'Over twenty years' is Rob personally, never the company (business 2020, company entity 2023). No homes-completed number. Do not ship on the placeholder.",
  slides=[
    dict(kind="ph_static", name="P11MeetRob", kicker="The builder",
         headline="You’ll deal with Rob. First chat to handover.", size=50,
         sub="Rob Williamson · Builder & Director",
         note="A phone portrait on site in good light is enough"),
])

P(id="P12", page="Post 12 · One or two at a time", date="Sun 4 Oct · Carousel", pillar="Services & positioning",
  objective="Enquiries", cta="Ready to get started?",
  caption="Fewer builds, better results.\n\nWe take on one or two projects at a time so every build receives our full attention. It is not a marketing line. It is the reason the work is what it is, and the reason we cannot always commence immediately.\n\nNew builds. Extensions. Renovations. Secondary dwellings. Gold Coast.",
  tags="#CoastLifeConstructions #GoldCoastBuilder #CustomHomes #HomeRenovation #HomeExtension #SecondaryDwelling #GoldCoastHomes #CustomHomeBuilder #DesignAndBuild #QLDBuilder #Burleigh #ResidentialConstruction",
  approve="Confirm the four service lines are what Rob wants enquiries for right now, particularly secondary dwellings. Never publish the internal builds-per-year figure — public framing stays 'one or two projects at a time'.",
  slides=[
    dict(kind="photo_cover", name="P12Cover", photo="kitchen2.jpg", focus="center 36%",
         headline="One or two builds at a time. On purpose.",
         sub="Fewer builds, better results.", num=n(1, 5)),
    dict(kind="point", kicker="What it means", headline="Your project is not queued behind six others", size=68, num=n(2, 5),
         body=["It receives the attention it requires."]),
    dict(kind="point", deep=True, headline="New builds, extensions, renovations, secondary dwellings", size=56, num=n(3, 5),
         body=["Four service lines, one standard across all of them."]),
    dict(kind="point", kicker="Honestly", headline="We cannot always commence immediately", size=64, num=n(4, 5),
         body=["It also means the project in front of us receives full attention."]),
    dict(kind="close_graphic", headline="Ready to get started?", num=n(5, 5),
         lines=["Planning a project for next year? Now is the time to begin the conversation.",
                "Gold Coast · QBCC licensed · Master Builders Queensland"]),
])


# ---- Mondaro — project journal ---------------------------------------------
P(id="P13", page="Mondaro · Project journal", date="Carousel", pillar="Trust & process",
  objective="Trust", cta="Ready to get started?",
  caption="Mondaro, frame stage.\\n\\nThe frame is where tolerance is either established or lost. Every trade that follows inherits it: cabinetry, glazing, linings and finishes all sit off the accuracy set here.\\n\\nIt is the least photogenic stage of a build and the one that determines the most.",
  tags="#CoastLifeConstructions #GoldCoastBuilder #CustomHomes #CustomHomeBuilder #TimberFrame #BuildingAHome #ResidentialConstruction #QLDBuilder #GoldCoastHomes #UnderConstruction #Craftsmanship",
  approve="Confirm the suburb and that the project may be named publicly — 'Mondaro' is the project name and the location is unverified. Confirm client permission. No timeline, engineering or compliance claim: describe practice, never certify an outcome.",
  slides=[
    dict(kind="photo_cover", name="P13Cover", kicker="Mondaro", photo="mondaro-truss.jpg", focus="center 50%",
         headline="Structure decides everything that follows", hero_size=84,
         sub="Project journal · Frame stage", num=n(1, 5)),
    dict(kind="point", kicker="Set-out", headline="Every dimension downstream is measured from here", size=68, num=n(2, 5),
         body=["Levels and set-out established before a single stud is stood."],
         photo="mondaro-slab.jpg", focus="center 55%"),
    dict(kind="point", kicker="Material", headline="Engineered joists, specified and stacked", size=68, num=n(3, 5),
         body=["Selected for span and stability, not for what was quickest to source."],
         photo="mondaro-joists.jpg", focus="center 50%"),
    dict(kind="service", photo="mondaro-studs.jpg", focus="center 48%", headline="Braced, plumb, checked", num=n(4, 5),
         body=["Verified before anything is lined, because after that it is concealed."]),
    dict(kind="close_graphic", headline="Ready to get started?", num=n(5, 5),
         lines=["We take on one or two projects at a time.",
                "Gold Coast · QBCC licensed · Master Builders Queensland"]),
])



# ---- Variant comparison pages ----------------------------------------------
# Same eight plates, three grounds. Pick one and it rolls across all 14 posts.

def _variant_slides(tag):
    return [
      dict(kind="photo_cover", name=f"{tag}01", photo="hero-crew.jpg", focus="center 38%",
           headline="New builds, extensions, renovations."),
      dict(kind="point", name=f"{tag}02", photo="newbuild-frame.jpg", focus="center 46%",
           headline="New builds", body=["Designed to the block, the orientation and the way you intend to live."]),
      dict(kind="point", name=f"{tag}03", photo="mondaro-truss.jpg", focus="center 50%",
           headline="Structure", body=["Structure decides everything that follows."]),
      dict(kind="point", name=f"{tag}04", photo="mondaro-slab.jpg", focus="center 55%",
           headline="Set-out", body=["Levels and set-out established before a single stud is stood."]),
      dict(kind="point", name=f"{tag}05", photo="kitchen.jpg", focus="center 50%",
           headline="Renovations", body=["For homes that are structurally sound but no longer laid out well."]),
      dict(kind="point", name=f"{tag}06", photo="chambers.jpg", focus="center 62%",
           headline="Custom", body=["A custom build is determined long before it begins."]),
      dict(kind="point", name=f"{tag}07", photo="mondaro-sandstone.jpg", focus="center 50%",
           headline="Material", body=["Common on sloping Gold Coast blocks, and typically the least disruptive."]),
      dict(kind="close_graphic", name=f"{tag}08", headline="Ready to get started?",
           lines=["We take on one or two projects at a time.",
                  "Gold Coast · QBCC licensed · Master Builders Queensland"]),
    ]

P(id="P90", variant="light", page="Variant · Light ground, colour mark", date="Comparison",
  pillar="—", objective="—", cta="—", caption="Variant comparison sheet — not for publication.",
  tags="", approve="Comparison only.", slides=_variant_slides("V1S"))

P(id="P91", variant="grey", page="Variant · Grey ground, colour mark", date="Comparison",
  pillar="—", objective="—", cta="—", caption="Variant comparison sheet — not for publication.",
  tags="", approve="Comparison only.", slides=_variant_slides("V2S"))

P(id="P92", variant="blue", page="Variant · Blue ground, white mark", date="Comparison",
  pillar="—", objective="—", cta="—", caption="Variant comparison sheet — not for publication.",
  tags="", approve="Comparison only.", slides=_variant_slides("V3S"))



def to_plate(post):
    """Recast an authored post into the editorial-plate system.

    One ground per post, sampled from its hero photograph, so a carousel reads as
    one object on swipe and the grid reads as one book.
    """
    hero = post.get("hero") or next((sl.get("photo") for sl in post["slides"] if sl.get("photo")), None)
    pool = [sl.get("photo") for sl in post["slides"] if sl.get("photo")]
    spare = [q for q in pool if q != hero]
    v = post.get("variant", "blue")
    ground = ground_from(hero, v)
    out = []
    for sl in post["slides"]:
        k = sl["kind"]
        if k in ("close_graphic", "cta"):
            meta = " · ".join(sl.get("lines", [])) if sl.get("lines") else sl.get("meta", "")
            out.append(dict(kind="plate_text", name=sl.get("name"), caption=sl["headline"],
                            meta=meta, ground=ground, variant=v))
            continue
        if k in ("photo_cover", "deep_cover", "light_cover"):
            cap = sl["headline"]
        elif k == "quote":
            cap = sl["headline"].strip("\u201c\u201d") + "  —  " + sl.get("attrib", "")
        elif k == "stack":
            cap = sl["sub"]
        elif k == "ph_static":
            cap = sl["headline"]
        else:
            cap = (sl.get("body") or [sl.get("headline", "")])[0]
        p = dict(kind="plate", name=sl.get("name"), caption=cap, ground=ground,
                 photo=sl.get("photo"), focus=sl.get("focus", "center"), tint=post.get("hero_tint"), variant=v)
        if not p["photo"]:
            if k == "ph_static":
                p.update(label="Portrait of Rob required", note=sl.get("note", ""))
            elif k in ("detail_spread",):
                p.update(photo=sl.get("primary", {}).get("photo"),
                         label=sl.get("primary", {}).get("label", "Detail shot required"),
                         note=sl.get("primary", {}).get("note", ""))
            else:
                p.update(photo=(spare.pop(0) if spare else hero))
        out.append(p)
    return out

# ---------------------------------------------------------------------- build
def main():
    artboards, pages, notes = [], [], []
    written = []
    for pi, post in enumerate(POSTS, start=1):
        pid = f"page-{pi}"
        pages.append({"id": pid, "name": post["page"]})
        slides = to_plate(post)
        for si, s in enumerate(slides, start=1):
            name = s.get("name") or f"{post['id']}S{si:02d}"
            fn = f"{name}.dc.html"
            with open(fn, "w") as fh:
                fh.write(KINDS[s["kind"]](s))
            written.append(fn)
            artboards.append({
                "file": fn, "x": (si - 1) * 1240, "y": 0, "w": W, "h": H_PLATE,
                "page": pid,
                "title": f"{post['id']} · {'Cover' if si == 1 and len(slides) > 1 else ('Static' if len(slides) == 1 else f'Slide {si:02d}')}",
            })
        notes.append({
            "id": f"note-{pi}", "x": 0, "y": -210, "w": 860, "page": pid,
            "text": f"{post['page'].upper()} — {post['date']}\n"
                    f"{len(post['slides'])} artboard{'s' if len(post['slides']) > 1 else ''} at 1080 x 1440 (3:4). "
                    f"Copy is verbatim from the four-week plan; captions and hashtags live there.",
        })

    canvas = {"artboards": artboards, "annotations": notes, "pages": pages,
              "launch": {"view": "canvas", "page": next((f"page-{i}" for i, po in enumerate(POSTS, 1) if po.get("variant")), "page-1")}}
    with open("canvas.json", "w") as fh:
        json.dump(canvas, fh, indent=2)
    print(f"{len(written)} artboards, {len(pages)} pages")
    print(" ".join(f"--artboard {f}" for f in written))


if __name__ == "__main__":
    main()
