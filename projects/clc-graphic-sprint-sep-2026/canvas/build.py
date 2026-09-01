#!/usr/bin/env python3
"""Generates every Coast Life feed-post artboard on the locked CLC grid.

One source of truth for the grid so every slide stays identical on swipe.
Instagram build: carousels capped at 5 slides, one idea and one line per slide.
Edit POSTS below and re-run; then re-seed the canvas.
"""
import json, os, re

W, H = 1080, 1350
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


def shell(body, ground, link):
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
<div style="position: relative; width: {W}px; height: {H}px; background: {ground}; overflow: hidden;">
{body}
</div>
</x-dc>
</body>
</html>
"""


def footer(num, deep):
    logo = "cl-white.png" if deep else "cl-colour.png"
    col = "rgba(151,200,232,0.75)" if deep else "rgba(47,102,144,0.75)"
    left = f'<div style="font-size: 22px; letter-spacing: 0.16em; font-weight: 500; color: {col};">{num}</div>' if num else '<div></div>'
    return f"""  <div style="position: absolute; left: {MX}px; right: {MX}px; bottom: {FOOT_B}px; display: flex; align-items: center; justify-content: space-between;">
{left}
    <img src="{logo}" alt="Coast Life Constructions" style="width: {LOGO_W}px; height: auto; display: block;">
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
      <div style="font-size: 22px; letter-spacing: 0.16em; font-weight: 500; color: rgba(151,200,232,0.8);">{s.get('num','')}</div>
      <img src="cl-white.png" alt="Coast Life Constructions" style="width: {LOGO_W}px; height: auto; display: block;">
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
  <div style="position: absolute; left: {MX}px; right: {MX}px; top: 340px;">
    {head(s['headline'], deep, size=s.get('size', 76), weight=300)}
  </div>
  <div style="position: absolute; left: {MX}px; bottom: 340px; display: flex; flex-direction: column; gap: 26px;">
    {rule(deep, w=120)}
    {''.join(para(p, deep, size=38, maxw=700) for p in s['body'])}
  </div>
{footer(s.get('num'), deep)}"""
    return shell(body, ground, "#ffffff" if deep else NAVY)


def step(s):
    deep = s.get('deep', False)
    ground = BG_DEEP if deep else BG_LIGHT
    numcol = "rgba(151,200,232,0.16)" if deep else "rgba(47,102,144,0.13)"
    body = f"""  <div style="position: absolute; left: {MX - 14}px; top: 200px; font-size: 340px; line-height: 0.8; font-weight: 600; color: {numcol}; letter-spacing: -0.04em;">{s['numeral']}</div>
  <div style="position: absolute; left: {MX}px; right: {MX}px; top: 600px; display: flex; flex-direction: column; gap: 30px;">
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
  <div style="position: absolute; left: {MX}px; right: {MX}px; top: 340px; display: flex; flex-direction: column; gap: 36px;">
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
    body = f"""  <div style="position: absolute; left: {MX}px; top: {PANEL_Y}px; width: {CW}px; height: {TALL_H}px; overflow: hidden; background: #dfe5ea;">
    <img src="{s['photo']}" alt="" style="width: 100%; height: 100%; object-fit: cover; object-position: {s.get('focus','center')}; display: block;">
  </div>
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


KINDS = {"service": service, "close_graphic": close_graphic, "photo_cover": photo_cover, "photo_static": photo_static, "ph_static": ph_static,
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
  caption="New builds, extensions, renovations.\n\nThree kinds of job, and one builder across all of them — from the first chat through to handover.\n\nIf you're weighing up which one your place needs, that's a conversation worth having early.",
  tags="#CoastLifeConstructions #GoldCoastBuilder #CustomHomes #HomeRenovation #HomeExtension #GoldCoastHomes #CustomHomeBuilder #DesignAndBuild #QLDBuilder #Burleigh #Bonogin #VarsityLakes #ResidentialConstruction",
  approve="Confirm which service each of the three photos actually belongs to — new build, extension or renovation. Their site only confirms Gundara Street as a renovation.",
  slides=[
    dict(kind="photo_cover", name="Main", photo="hero-crew.jpg", focus="center 38%",
         headline="New builds, extensions, renovations.",
         sub="Three kinds of job. One builder, start to finish.", num=n(1, 5)),
    dict(kind="service", photo="newbuild-frame.jpg", focus="center 46%", headline="New builds", num=n(2, 5),
         body=["Designed around your block, your orientation, and how you actually live."]),
    dict(kind="service", photo="alfresco.jpg", focus="center 55%", headline="Extensions", num=n(3, 5),
         body=["More house without moving. Ground floor, second storey, or in underneath."]),
    dict(kind="service", photo="kitchen.jpg", focus="center 50%", headline="Renovations", num=n(4, 5),
         body=["When the bones are good and it’s the layout that’s wrong."]),
    dict(kind="close_graphic", headline="Ready to get started?", num=n(5, 5),
         lines=["Tell us which one yours is and we’ll take it from there.",
                "Gold Coast · QBCC licensed · Master Builders Queensland"]),
])

P(id="P01", page="Post 1 · New builds", date="Tue 8 Sep · Carousel", pillar="Services & positioning",
  objective="Enquiries", cta="Ready to get started?",
  caption="A custom build is mostly decisions, and the early ones carry the most weight.\n\nThe block, the layout, the materials. Get those three settled properly and the rest of the build is a lot calmer than people expect.\n\nSimple, well chosen materials often make a more timeless result. That one's worth sitting with.",
  tags="#CoastLifeConstructions #GoldCoastBuilder #CustomHomes #CustomHomeBuilder #NewBuild #BuildingAHome #GoldCoastHomes #DesignAndBuild #QLDBuilder #Burleigh #ResidentialConstruction",
  approve="All three points condense their own blog article on early custom-build decisions. No approval timeframe or council outcome may be implied.",
  slides=[
    dict(kind="photo_cover", name="P01Cover", kicker="New builds", photo="chambers.jpg", focus="center 62%",
         headline="A custom build is decided long before it’s started",
         sub="The three that matter most.", num=n(1, 5)),
    dict(kind="point", kicker="One", headline="The block decides more than you think", size=70, num=n(2, 5),
         body=["Levels, drainage, soil, orientation and access all shape what’s worth building."]),
    dict(kind="point", deep=True, kicker="Two", headline="The layout is the house", num=n(3, 5),
         body=["Flow, light, and how the inside meets the outside. Everything else is finish."]),
    dict(kind="point", kicker="Three", headline="Choose materials early", num=n(4, 5),
         body=["Late selections are the most common cause of delays that didn’t need to happen."]),
    dict(kind="close_graphic", headline="Ready to get started?", num=n(5, 5),
         lines=["Bring your block and a rough idea. We’ll tell you what’s realistic.",
                "Custom homes · Gold Coast"]),
])

P(id="P02", page="Post 2 · Warranty", date="Thu 10 Sep · Static", pillar="Trust & process",
  objective="Trust", cta="Our full process is on the website — link in bio.",
  caption="Handover isn't the end of the job.\n\nNew build, extension or renovation — every one comes with a one-year maintenance warranty on top of the seven-year QBCC structural guarantee. Twelve months to live in the place, notice the small things, and have us come back and sort them.\n\nIt's on our process page in writing, same as everything else.",
  tags="#CoastLifeConstructions #GoldCoastBuilder #QBCC #MasterBuildersQLD #CustomHomes #HomeRenovation #HomeWarranty #GoldCoastHomes #QLDBuilder #ResidentialConstruction",
  approve="Warranty wording is verbatim from their process page — confirm it is still current for 2026 contracts. Highest-risk claim in the sprint.",
  slides=[
    dict(kind="photo_cover", name="P02Warranty", photo="living.jpg", focus="center 46%",
         headline="One year of maintenance cover, on top of the seven-year QBCC structural warranty.",
         hero_size=58, sub="New builds · Extensions · Renovations"),
])

P(id="P03", page="Post 3 · Extensions", date="Sun 13 Sep · Carousel", pillar="Services & positioning",
  objective="Saves", cta="Ready to get started?",
  caption="Three ways to add space without leaving the street you like.\n\nOut the back, up a storey, or in underneath. Which one suits comes down to your block, your levels and how much disruption you can live with.\n\nAn extension can often be staged so you stay living there while it happens.",
  tags="#CoastLifeConstructions #GoldCoastBuilder #HomeExtension #HomeRenovation #SecondStorey #GoldCoastHomes #CustomHomeBuilder #DesignAndBuild #QLDBuilder #Burleigh #Bonogin #ResidentialConstruction",
  approve="Three extension types are taken from their own blog. Do not state that any given option is available on a reader's block — that depends on council and the site.",
  slides=[
    dict(kind="photo_cover", name="P03Cover", kicker="Extensions", photo="pool.jpg", focus="center 55%",
         headline="Three ways to add space without moving",
         sub="Out the back, up, or underneath.", num=n(1, 5)),
    dict(kind="point", kicker="Out the back", headline="Ground-floor addition", num=n(2, 5),
         body=["The simplest when there’s room on the block and the levels allow it."]),
    dict(kind="point", deep=True, kicker="Up", headline="Second storey", num=n(3, 5),
         body=["More house on the same footprint. The structure below decides what’s possible."]),
    dict(kind="point", kicker="Underneath", headline="Build in under the house", num=n(4, 5),
         body=["Common on a sloping Gold Coast block, and often the least disruptive."]),
    dict(kind="close_graphic", headline="Ready to get started?", num=n(5, 5),
         lines=["Send us your address and what you’re hoping to add.",
                "Extensions and additions · Gold Coast"]),
])

P(id="P04", page="Post 4 · Renovations", date="Tue 15 Sep · Carousel", pillar="Services & positioning",
  objective="Saves", cta="Ready to get started?",
  caption="What we look at first on a renovation, before anyone talks about tiles.\n\nWhat the house is actually getting wrong, what the layout could be, and what's realistic for the budget you're working with.\n\nKitchens and bathrooms get the attention, but it's usually the layout that changes how a house feels to live in.",
  tags="#CoastLifeConstructions #GoldCoastBuilder #HomeRenovation #RenovationGoldCoast #KitchenRenovation #BathroomRenovation #GoldCoastHomes #CustomHomeBuilder #QLDBuilder #Bonogin #ResidentialConstruction",
  approve="Points condense their own 'what adds the most value when renovating' article. No ROI, percentage or dollar claim of any kind.",
  slides=[
    dict(kind="photo_cover", name="P04Cover", kicker="Renovations", photo="reno-portrait.jpg", focus="center 45%",
         headline="What we look at first, before anyone mentions tiles",
         sub="Three questions, in this order.", num=n(1, 5)),
    dict(kind="point", kicker="First", headline="What is the house getting wrong?", size=70, num=n(2, 5),
         body=["Space, layout, condition, or all three. The answer sets the scope."]),
    dict(kind="point", deep=True, kicker="Second", headline="What could the layout be?", num=n(3, 5),
         body=["Opening up living areas, better flow, more light. That’s what changes daily life."]),
    dict(kind="point", kicker="Third", headline="What’s realistic for the budget?", size=70, num=n(4, 5),
         body=["Said plainly and early, so nothing gets designed that can’t be built."]),
    dict(kind="close_graphic", headline="Ready to get started?", num=n(5, 5),
         lines=["A walk through the house is the fastest way to answer all three.",
                "Renovations and extensions · Gold Coast"]),
])

P(id="P05", page="Post 5 · Client review", date="Thu 17 Sep · Static", pillar="Social proof",
  objective="Trust", cta="More client reviews are on our website.",
  caption="Naomi's renovation, Bonogin.\n\nThe part of her review that stuck with us wasn't about the finish — it was about being kept informed the whole way through. That's the part that's actually within our control every single day, on every job.\n\nThanks Naomi.",
  tags="#CoastLifeConstructions #GoldCoastBuilder #ClientReview #HomeRenovation #Bonogin #GoldCoastHomes #CustomHomeBuilder #QLDBuilder #RenovationGoldCoast",
  approve="HIGHEST SENSITIVITY. The quote shown is a paraphrase and must be replaced with the verbatim published review. Get Naomi's written permission for name and suburb in a graphic. Confirm the job was a renovation before labelling it one.",
  slides=[
    dict(kind="quote", name="P05Review",
         headline="“We were kept fully informed the whole way through.”",
         attrib="Naomi Ortado · Renovation, Bonogin",
         note="Verbatim wording, service type and written permission to be confirmed before publishing."),
])

P(id="P06", page="Post 6 · Which one is yours", date="Sun 20 Sep · Carousel", pillar="Educational",
  objective="Saves", cta="Ready to get started?",
  caption="Renovate, extend, or start again.\n\nThe way we'd approach it: start with the problem, not the solution. Is it space, layout, condition, or all three? The answer usually makes the decision for you.\n\nRenovations and extensions can look cheaper up front and carry more unknowns. New builds are more predictable but ask for more design and a longer approval run. Neither is automatically right.",
  tags="#CoastLifeConstructions #GoldCoastBuilder #HomeRenovation #HomeExtension #KnockdownRebuild #CustomHomeBuilder #GoldCoastHomes #DesignAndBuild #QLDBuilder #Burleigh #ResidentialConstruction",
  approve="Condensed from their own 'where to start' article. Never imply an approval timeframe or a council outcome.",
  slides=[
    dict(kind="photo_cover", name="P06Cover", photo="drawings.jpg", focus="center 42%", tint=0.55,
         headline="Renovate, extend, or start again?",
         sub="Start with the problem, not the solution.", num=n(1, 5)),
    dict(kind="step", numeral="01", headline="Renovate", num=n(2, 5),
         body=["When the bones are good and it’s the layout that’s wrong."]),
    dict(kind="step", deep=True, numeral="02", headline="Extend", num=n(3, 5),
         body=["When the house works, there just isn’t enough of it."]),
    dict(kind="step", numeral="03", headline="Start again", num=n(4, 5),
         body=["When repair costs start creeping toward a new build."]),
    dict(kind="close_graphic", headline="Ready to get started?", num=n(5, 5),
         lines=["Not sure which one yours is? That’s a good first conversation.",
                "Longer version on our blog · link in bio"]),
])

P(id="P07", page="Post 7 · Secondary dwellings", date="Tue 22 Sep · Carousel", pillar="Services & positioning",
  objective="Enquiries", cta="Ready to get started?",
  caption="Secondary dwellings — the one we get asked about most often lately.\n\nSelf-contained living on the same block. Family, guests, or rental. Its own kitchen, bathroom and living space.\n\nWhat's possible comes down to your lot, your zoning and your council, so it's worth checking before you get attached to a plan.",
  tags="#CoastLifeConstructions #GoldCoastBuilder #SecondaryDwelling #GrannyFlatQLD #HomeExtension #MultigenerationalLiving #GoldCoastHomes #CustomHomeBuilder #QLDBuilder #ResidentialConstruction",
  approve="Do NOT publish a floor-area figure, a zoning rule, or any suggestion that approval is likely. Their blog cites general council guidance only. Also confirm 'asked about most often lately' with Rob — drop the line if he can't back it.",
  slides=[
    dict(kind="photo_cover", name="P07Cover", kicker="Secondary dwellings", photo="rear-dwelling.jpg", focus="62% 58%",
         headline="A second home on the block you already own",
         sub="Family, guests, or rental.", num=n(1, 5)),
    dict(kind="point", kicker="What it is", headline="Self-contained, on the same lot", size=70, num=n(2, 5),
         body=["Its own kitchen, bathroom, bedroom and living space."]),
    dict(kind="point", deep=True, kicker="What it’s for", headline="Family close by, not on top of you", size=66, num=n(3, 5),
         body=["Multi-generational living, guests, or an income from the same block."]),
    dict(kind="point", kicker="What decides it", headline="Your lot, your zoning, your council", size=66, num=n(4, 5),
         body=["Worth checking what’s possible before you get attached to a plan."]),
    dict(kind="close_graphic", headline="Ready to get started?", num=n(5, 5),
         lines=["Send us your address and we’ll tell you what’s worth exploring.",
                "Secondary dwellings · Gold Coast"]),
])

P(id="P08", page="Post 8 · Service area", date="Thu 24 Sep · Static", pillar="Services & positioning",
  objective="Local awareness", cta="If you're nearby and thinking about a project, we're easy to get hold of.",
  caption="Where we've been building.\n\nBurleigh, Bonogin, Varsity Lakes and across the Gold Coast — new builds, extensions and renovations.\n\nIf you're in the area and thinking about a project, we're easy to get hold of.",
  tags="#CoastLifeConstructions #GoldCoastBuilder #GoldCoastHomes #Burleigh #Bonogin #VarsityLakes #CustomHomeBuilder #HomeRenovation #HomeExtension #QLDBuilder #ResidentialConstruction",
  approve="Only Burleigh, Bonogin and Varsity Lakes are supported by public evidence. Do not add a suburb Rob hasn't confirmed. Northern NSW and Brisbane stay off until he confirms licensing and appetite.",
  slides=[
    dict(kind="stack", name="P08ServiceArea", kicker="Service area", headline="Where we build", svg=SVG_COAST,
         items=[dict(t="Burleigh"), dict(t="Bonogin"), dict(t="Varsity Lakes"),
                dict(t="and across the Gold Coast", soft=True)],
         sub="New builds, extensions and renovations."),
])

P(id="P09", page="Post 9 · Renovation mistakes", date="Sun 27 Sep · Carousel", pillar="Educational",
  objective="Saves", cta="Ready to get started?",
  caption="Three renovation mistakes we see every year — and every one of them is easier to avoid before the job starts than to fix once it has.\n\nFinishes chosen too late. No contingency for what's behind the wall. And expectations nobody said out loud.\n\nNone of them are dramatic. They're just expensive.",
  tags="#CoastLifeConstructions #GoldCoastBuilder #HomeRenovation #RenovationPlanning #RenovationGoldCoast #CustomHomeBuilder #GoldCoastHomes #QLDBuilder #Burleigh #ResidentialConstruction",
  approve="'Simple, well chosen materials often create a more timeless result' is near-verbatim from their blog — confirm Rob is happy for it to become a signature line.",
  slides=[
    dict(kind="deep_cover", name="P09Cover", kicker="Renovations", svg=SVG_DOC,
         headline="Three renovation mistakes we see every year",
         sub="All three are avoidable before you start.", num=n(1, 5)),
    dict(kind="point", kicker="One", headline="Choosing finishes last", num=n(2, 5),
         body=["The most common cause of delays that didn’t need to happen."]),
    dict(kind="point", deep=True, kicker="Two", headline="Leaving no contingency", num=n(3, 5),
         body=["Every existing home has something nobody has seen yet."]),
    dict(kind="point", kicker="Three", headline="Leaving expectations unspoken", size=70, num=n(4, 5),
         body=["Scope, timing, how you’ll talk. Agreed early, or argued about later."]),
    dict(kind="close_graphic", headline="Ready to get started?", num=n(5, 5),
         lines=["Planning something for next year? Now’s the right time to talk it through.",
                "Renovations · Gold Coast"]),
])

P(id="P10", page="Post 10 · One builder", date="Tue 29 Sep · Carousel", pillar="Trust & process",
  objective="Trust", cta="Ready to get started?",
  caption="New build, extension or renovation — it's the same bloke either way.\n\nRob takes the first call, walks the site, prices it, runs it and hands it over. There's no relay, and no project manager you meet once.\n\nIt's the main reason we only take on one or two projects at a time.",
  tags="#CoastLifeConstructions #GoldCoastBuilder #FamilyOwnedBusiness #CustomHomeBuilder #HomeRenovation #GoldCoastHomes #DesignAndBuild #QLDBuilder #VarsityLakes #ResidentialConstruction",
  approve="Rob is the point of contact from first chat to handover — their own published claim. Do NOT say Rob is on site every stage or every day; that wording is unconfirmed and previously flagged.",
  slides=[
    dict(kind="photo_cover", name="P10Cover", photo="team.jpg", focus="42% 36%",
         headline="Same builder, first call to handover",
         sub="Whichever of the three it is.", num=n(1, 5)),
    dict(kind="point", kicker="On a new build", headline="Rob walks the block with you", size=70, num=n(2, 5),
         body=["Before there’s a plan, let alone a price."]),
    dict(kind="point", deep=True, kicker="On an extension", headline="One person owns the disruption", size=66, num=n(3, 5),
         body=["You’re living there while it happens. Somebody has to be accountable for that."]),
    dict(kind="point", kicker="On a renovation", headline="No relay, no handballing", num=n(4, 5),
         body=["The person who quoted it is the person who finishes it."]),
    dict(kind="close_graphic", headline="Ready to get started?", num=n(5, 5),
         lines=["Rob takes the first call himself.",
                "Coast Life Constructions · Gold Coast"]),
])

P(id="P11", page="Post 11 · Meet Rob", date="Thu 1 Oct · Static", pillar="People & brand story",
  objective="Profile visits", cta="Say hello — details are in the bio.",
  caption="Rob Williamson — builder and director, and the person you'll actually be dealing with.\n\nFirst chat, site visit, quote, contract, construction, handover. Same bloke the whole way through, whether it's a new build, an extension or a renovation.\n\nOver twenty years in construction, and still the one answering the phone.",
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
  caption="Fewer builds, better results.\n\nWe take on one or two projects at a time so every build gets our full focus. It's not a marketing line — it's the reason the work looks the way it does, and the reason we sometimes can't start straight away.\n\nNew builds. Extensions. Renovations. Secondary dwellings. Gold Coast.",
  tags="#CoastLifeConstructions #GoldCoastBuilder #CustomHomes #HomeRenovation #HomeExtension #SecondaryDwelling #GoldCoastHomes #CustomHomeBuilder #DesignAndBuild #QLDBuilder #Burleigh #ResidentialConstruction",
  approve="Confirm the four service lines are what Rob wants enquiries for right now, particularly secondary dwellings. Never publish the internal builds-per-year figure — public framing stays 'one or two projects at a time'.",
  slides=[
    dict(kind="photo_cover", name="P12Cover", photo="kitchen2.jpg", focus="center 36%",
         headline="One or two builds at a time. On purpose.",
         sub="Fewer builds, better results.", num=n(1, 5)),
    dict(kind="point", kicker="What it means", headline="Your job isn’t queued behind six others", size=68, num=n(2, 5),
         body=["The attention it gets is the attention it needs."]),
    dict(kind="point", deep=True, headline="New builds, extensions, renovations, secondary dwellings", size=56, num=n(3, 5),
         body=["Four kinds of job, one standard across all of them."]),
    dict(kind="point", kicker="Honestly", headline="It means we can’t always start straight away", size=64, num=n(4, 5),
         body=["It also means the job in front of us is the one that matters."]),
    dict(kind="close_graphic", headline="Ready to get started?", num=n(5, 5),
         lines=["Planning something for next year? Now’s a good time to talk.",
                "Gold Coast · QBCC licensed · Master Builders Queensland"]),
])


# ---------------------------------------------------------------------- build
def main():
    artboards, pages, notes = [], [], []
    written = []
    for pi, post in enumerate(POSTS, start=1):
        pid = f"page-{pi}"
        pages.append({"id": pid, "name": post["page"]})
        for si, s in enumerate(post["slides"], start=1):
            name = s.get("name") or f"{post['id']}S{si:02d}"
            fn = f"{name}.dc.html"
            with open(fn, "w") as fh:
                fh.write(KINDS[s["kind"]](s))
            written.append(fn)
            artboards.append({
                "file": fn, "x": (si - 1) * 1240, "y": 0, "w": W, "h": H,
                "page": pid,
                "title": f"{post['id']} · {'Cover' if si == 1 and len(post['slides']) > 1 else ('Static' if len(post['slides']) == 1 else f'Slide {si:02d}')}",
            })
        notes.append({
            "id": f"note-{pi}", "x": 0, "y": -210, "w": 860, "page": pid,
            "text": f"{post['page'].upper()} — {post['date']}\n"
                    f"{len(post['slides'])} artboard{'s' if len(post['slides']) > 1 else ''} at 1080 x 1350. "
                    f"Copy is verbatim from the four-week plan; captions and hashtags live there.",
        })

    canvas = {"artboards": artboards, "annotations": notes, "pages": pages,
              "launch": {"view": "canvas", "page": "page-1"}}
    with open("canvas.json", "w") as fh:
        json.dump(canvas, fh, indent=2)
    print(f"{len(written)} artboards, {len(pages)} pages")
    print(" ".join(f"--artboard {f}" for f in written))


if __name__ == "__main__":
    main()
