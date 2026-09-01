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
FOOT_B = 72                   # footer baseline
LOGO_W, LOGO_H = 300, 106

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
            f'color: {col}; letter-spacing: -0.005em; max-width: {maxw}px; text-wrap: pretty;">{text}</h2>')


def para(text, deep, size=40, maxw=740):
    col = "rgba(255,255,255,0.8)" if deep else INK_SOFT
    return (f'<p style="margin: 0; font-size: {size}px; line-height: 1.45; font-weight: 400; '
            f'color: {col}; max-width: {maxw}px; text-wrap: pretty;">{text}</p>')


def rule(deep, w=180):
    col = "rgba(151,200,232,0.5)" if deep else "rgba(47,102,144,0.35)"
    return f'<div style="width: {w}px; height: 2px; background: {col};"></div>'


# ---------------------------------------------------------------- slide kinds

def photo_cover(s):
    deep = False
    sub = f'\n    <div style="font-size: 32px; font-weight: 400; color: {STEEL};">{s["sub"]}</div>' if s.get("sub") else ""
    body = f"""  <div style="position: absolute; left: {MX}px; top: {PANEL_Y}px; width: {CW}px; height: {PANEL_H}px; overflow: hidden; background: #dfe5ea;">
    <img src="{s['photo']}" alt="" style="width: 100%; height: 100%; object-fit: cover; object-position: {s.get('focus','center')}; display: block;">
  </div>
  <div style="position: absolute; left: {MX}px; right: {MX}px; top: {PANEL_Y + PANEL_H + 54}px; display: flex; flex-direction: column; gap: 20px;">
    {kicker(s['kicker'], deep, abs_pos=False)}
    {head(s['headline'], deep, size=s.get('size', 60))}{sub}
  </div>
{footer(s.get('num'), deep)}"""
    return shell(body, BG_LIGHT, NAVY)


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
    body = f"""  <div style="position: absolute; inset: 0; background: radial-gradient(120% 85% at 18% 8%, rgba(24,132,199,0.34) 0%, rgba(24,132,199,0) 62%);"></div>
  {s.get('svg','')}
  <div style="position: absolute; left: {MX}px; right: {MX}px; top: 300px; display: flex; flex-direction: column; gap: 30px;">
    {kicker(s['kicker'], deep, abs_pos=False)}
    {head(s['headline'], deep, size=s.get('size', 74))}{sub}
  </div>
{footer(s.get('num'), deep)}"""
    return shell(body, BG_DEEP, "#ffffff")


def light_cover(s):
    deep = False
    sub = f'\n    <div style="font-size: 32px; font-weight: 400; color: {STEEL};">{s["sub"]}</div>' if s.get("sub") else ""
    body = f"""  {s.get('svg','')}
  <div style="position: absolute; left: {MX}px; right: {MX}px; top: 300px; display: flex; flex-direction: column; gap: 30px;">
    {kicker(s['kicker'], deep, abs_pos=False)}
    {head(s['headline'], deep, size=s.get('size', 74))}{sub}
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
    body = f"""  <div style="position: absolute; left: {MX}px; right: {MX}px; top: 230px; display: flex; flex-direction: column; gap: 52px;">
    <blockquote style="margin: 0; font-size: 66px; line-height: 1.2; font-weight: 300; color: {INK}; letter-spacing: -0.005em; text-wrap: pretty;">{s['headline']}</blockquote>
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
    body = f"""  {s.get('svg','')}
  {kicker(s['kicker'], deep, top=140)}
  <div style="position: absolute; left: {MX}px; right: {MX}px; top: 210px;">
    {head(s['headline'], deep, size=84, weight=300)}
  </div>
  <div style="position: absolute; left: {MX}px; top: 400px; display: flex; flex-direction: column;">{items}</div>
  <div style="position: absolute; left: {MX}px; bottom: 250px; display: flex; flex-direction: column; gap: 22px;">
    {rule(deep, w=200)}
    {para(s['sub'], deep, size=34, maxw=640)}
  </div>
{footer(None, deep)}"""
    return shell(body, BG_LIGHT, NAVY)


KINDS = {"photo_cover": photo_cover, "photo_static": photo_static, "ph_static": ph_static,
         "deep_cover": deep_cover, "light_cover": light_cover, "qa": qa, "step": step,
         "point": point, "cta": cta, "quote": quote, "stack": stack}

# ---------------------------------------------------------------- line motifs

SVG_ROOFS = f'''<svg style="position: absolute; right: 74px; top: 700px; width: 640px; height: 380px; opacity: 0.5;" viewBox="0 0 320 190" fill="none" stroke="{BLUE}" stroke-width="1.6" stroke-linejoin="round">
    <path d="M8 120 L48 84 L88 120 M8 120 v52 h80 v-52"/>
    <path d="M112 120 L152 84 L192 120 M112 120 v52 h80 v-52 M152 120 v52" />
    <path d="M216 104 L256 62 L296 104 M216 104 v68 h80 v-68 M240 172 v-40 h32 v40"/>
  </svg>'''

SVG_PLAN = f'''<svg style="position: absolute; right: -40px; bottom: 200px; width: 520px; height: 520px; opacity: 0.22;" viewBox="0 0 200 200" fill="none" stroke="{NAVY}" stroke-width="1.4">
    <rect x="16" y="40" width="150" height="112"/>
    <path d="M16 96h150M92 40v112"/>
    <rect x="30" y="112" width="30" height="40"/>
    <path d="M124 96v56M124 124h42"/>
  </svg>'''

SVG_COAST = f'''<svg style="position: absolute; right: 30px; top: 0; width: 340px; height: 1350px; opacity: 0.3;" viewBox="0 0 120 450" fill="none" stroke="{BLUE}" stroke-width="1.6" stroke-linejoin="round">
    <path d="M92 0c-6 22-4 38 4 54 9 18 6 32-6 46-14 16-18 30-10 46 9 18 6 33-8 48-13 14-16 28-8 44 9 18 5 34-9 49-12 13-15 27-8 42 8 17 6 33-7 47-11 12-14 25-8 39 5 12 4 22-2 35"/>
    <path d="M112 0c-8 26-6 44 3 62 10 20 7 35-7 51-15 17-19 32-10 49 9 19 6 35-9 51-14 15-17 30-9 47 9 19 5 36-10 52-13 14-16 29-8 45 8 17 6 34-7 49-12 13-15 27-9 42" opacity="0.55"/>
  </svg>'''

SVG_DOC = f'''<svg style="position: absolute; right: 60px; bottom: 210px; width: 460px; height: 460px; opacity: 0.16;" viewBox="0 0 200 200" fill="none" stroke="{SKY}" stroke-width="1.4">
    <rect x="30" y="24" width="104" height="140"/>
    <rect x="58" y="46" width="104" height="140"/>
    <path d="M74 78h72M74 100h72M74 122h50"/>
  </svg>'''


def n(i, total):
    return f"{i:02d} / {total:02d}"


# ---------------------------------------------------------------------- posts
# Copy is verbatim from PLAN.md. Nothing here is invented.

POSTS = []

# ---- Post 1 -----------------------------------------------------------------
POSTS.append(dict(id="P01", page="Post 1 · Ask a builder", date="Tue 8 Sep · Carousel", slides=[
    dict(kind="photo_cover", name="Main", kicker="Before you sign", photo="chambers.jpg", focus="center 58%",
         headline="Three questions to ask a builder before you sign", size=62,
         sub="Worth screenshotting.", num=n(1, 5)),
    dict(kind="qa", kicker="One", headline="“Who will I actually be dealing with?”", num=n(2, 5),
         body=["The builder, or a project manager you haven’t met?"]),
    dict(kind="qa", deep=True, kicker="Two", headline="“Is the quote itemised?”", num=n(3, 5),
         body=["A lump sum tells you nothing about what’s included."]),
    dict(kind="qa", kicker="Three", headline="“How many builds are you running right now?”", size=70, num=n(4, 5),
         body=["It tells you how much attention yours will get."]),
    dict(kind="cta", headline="Ask us all three. We’d rather you did.", num=n(5, 5),
         meta="Gold Coast · QBCC licensed · Master Builders Queensland"),
]))

# ---- Post 2 -----------------------------------------------------------------
POSTS.append(dict(id="P02", page="Post 2 · Warranty", date="Thu 10 Sep · Static", slides=[
    dict(kind="photo_static", name="P02Warranty", kicker="At handover", photo="garden.jpg", focus="center 55%",
         headline="One year of maintenance cover, on top of the seven-year QBCC structural warranty.",
         size=44, sub="Coast Life Constructions · QBCC licensed"),
]))

# ---- Post 3 -----------------------------------------------------------------
POSTS.append(dict(id="P03", page="Post 3 · Our process", date="Sun 13 Sep · Carousel", slides=[
    dict(kind="photo_cover", name="P03Cover", kicker="Our process", photo="aerial.jpg", focus="center 52%",
         headline="How a Coast Life build actually runs", size=64,
         sub="Seven stages. Three conversations.", num=n(1, 5)),
    dict(kind="step", numeral="01", headline="Talk, then look", num=n(2, 5),
         body=["An obligation-free chat, then we come and read the site."]),
    dict(kind="step", deep=True, numeral="02", headline="Plan, price, sign", num=n(3, 5),
         body=["Design with your architect or ours, then a fully itemised quote."]),
    dict(kind="step", numeral="03", headline="Build, then hand over", num=n(4, 5),
         body=["Every stage managed, then the keys and a maintenance warranty."]),
    dict(kind="cta", headline="Stage one is just a chat.", num=n(5, 5),
         meta="Custom homes, renovations and extensions · Gold Coast"),
]))

# ---- Post 4 -----------------------------------------------------------------
POSTS.append(dict(id="P04", page="Post 4 · Reading a quote", date="Tue 15 Sep · Carousel", slides=[
    dict(kind="deep_cover", name="P04Cover", kicker="Reading a quote", svg=SVG_DOC,
         headline="Why two quotes for the same house look nothing alike", size=70,
         sub="It’s usually not the builder’s margin.", num=n(1, 5)),
    dict(kind="point", kicker="One", headline="Inclusions aren’t standard", num=n(2, 5),
         body=["Site costs, allowances and finishes — in one quote, priced later in the other."]),
    dict(kind="point", deep=True, kicker="Two", headline="Allowances hide the difference", size=70, num=n(3, 5),
         body=["Two tiling allowances, double apart, read as the same line item."]),
    dict(kind="point", kicker="Three", headline="Check the drawing revision", num=n(4, 5),
         body=["Priced off an older set? You’re comparing two different houses."]),
    dict(kind="cta", headline="Comparing quotes? Happy to walk you through ours.", size=68, num=n(5, 5),
         meta="We quote fully itemised. You see what’s in and what isn’t."),
]))

# ---- Post 5 -----------------------------------------------------------------
POSTS.append(dict(id="P05", page="Post 5 · Client review", date="Thu 17 Sep · Static", slides=[
    dict(kind="quote", name="P05Review",
         headline="“We were kept fully informed the whole way through.”",
         attrib="Naomi Ortado · Bonogin",
         note="Verbatim review wording and written permission to be confirmed before publishing."),
]))

# ---- Post 6 -----------------------------------------------------------------
POSTS.append(dict(id="P06", page="Post 6 · Renovate or rebuild", date="Sun 20 Sep · Carousel", slides=[
    dict(kind="photo_cover", name="P06Cover", kicker="Where to start", photo="bath.jpg", focus="center 50%",
         headline="Renovate, extend, or start again?", size=64,
         sub="Start with the problem, not the solution.", num=n(1, 5)),
    dict(kind="step", numeral="01", headline="Renovate", num=n(2, 5),
         body=["When the bones are good and it’s the layout that’s wrong."]),
    dict(kind="step", deep=True, numeral="02", headline="Extend", num=n(3, 5),
         body=["When the house works, there just isn’t enough of it."]),
    dict(kind="step", numeral="03", headline="Start again", num=n(4, 5),
         body=["When repair costs start creeping toward a new build."]),
    dict(kind="cta", headline="Not sure which one you’re looking at?", size=70, num=n(5, 5),
         meta="That’s what the first chat is for. Longer version on our blog."),
]))

# ---- Post 7 -----------------------------------------------------------------
POSTS.append(dict(id="P07", page="Post 7 · First meeting", date="Tue 22 Sep · Carousel", slides=[
    dict(kind="light_cover", name="P07Cover", kicker="First meeting", svg=SVG_PLAN,
         headline="Bring three things to your first builder meeting", size=70,
         sub="It makes the first hour worth ten.", num=n(1, 5)),
    dict(kind="step", numeral="01", headline="Whatever plans you have", num=n(2, 5),
         body=["Sketches on paper count. None of it has to be finished."]),
    dict(kind="step", deep=True, numeral="02", headline="A real budget range", num=n(3, 5),
         body=["Not a number you’re guarding. It changes what we can honestly recommend."]),
    dict(kind="step", numeral="03", headline="Must-haves, separated from nice-to-haves", size=62, num=n(4, 5),
         body=["The separating is the useful part. Also the hardest."]),
    dict(kind="cta", headline="Got those three? Let’s have the first chat.", size=70, num=n(5, 5),
         meta="Obligation-free. Phone, email or in person."),
]))

# ---- Post 8 -----------------------------------------------------------------
POSTS.append(dict(id="P08", page="Post 8 · Service area", date="Thu 24 Sep · Static", slides=[
    dict(kind="stack", name="P08ServiceArea", kicker="Service area", headline="Where we build", svg=SVG_COAST,
         items=[dict(t="Burleigh"), dict(t="Bonogin"), dict(t="Varsity Lakes"),
                dict(t="and across the Gold Coast", soft=True)],
         sub="Custom homes, renovations and extensions."),
]))

# ---- Post 9 -----------------------------------------------------------------
POSTS.append(dict(id="P09", page="Post 9 · Planning mistakes", date="Sun 27 Sep · Carousel", slides=[
    dict(kind="deep_cover", name="P09Cover", kicker="Planning", svg=SVG_DOC,
         headline="Three renovation mistakes we see every year", size=70,
         sub="All three are avoidable before you start.", num=n(1, 5)),
    dict(kind="point", kicker="One", headline="Choosing finishes last", num=n(2, 5),
         body=["The most common cause of delays that didn’t need to happen."]),
    dict(kind="point", deep=True, kicker="Two", headline="Leaving no contingency", num=n(3, 5),
         body=["Every existing home has something nobody has seen yet."]),
    dict(kind="point", kicker="Three", headline="Leaving expectations unspoken", size=70, num=n(4, 5),
         body=["Scope, timing, how you’ll talk. Agreed early, or argued about later."]),
    dict(kind="cta", headline="Planning something for next year?", size=72, num=n(5, 5),
         meta="Now’s the right time to talk it through."),
]))

# ---- Post 10 ----------------------------------------------------------------
POSTS.append(dict(id="P10", page="Post 10 · Communication", date="Tue 29 Sep · Carousel", slides=[
    dict(kind="photo_cover", name="P10Cover", kicker="On communication", photo="team.jpg", focus="center 45%",
         headline="Most build stress is not knowing what’s next", size=62,
         sub="So we try to remove that part.", num=n(1, 5)),
    dict(kind="point", kicker="One", headline="Agree the update rhythm in week one", size=70, num=n(2, 5),
         body=["Weekly call, site meeting, email. Whichever suits — decided early."]),
    dict(kind="point", deep=True, kicker="Two", headline="One point of contact", num=n(3, 5),
         body=["You deal with Rob, first chat through to handover. No relay."]),
    dict(kind="point", kicker="Three", headline="Bad news early beats good news late", size=68, num=n(4, 5),
         body=["Something behind a wall is normal. Hearing about it a fortnight later isn’t."]),
    dict(kind="cta", headline="That’s how we try to run it.", num=n(5, 5),
         meta="Coast Life Constructions · Gold Coast"),
]))

# ---- Post 11 ----------------------------------------------------------------
POSTS.append(dict(id="P11", page="Post 11 · Meet Rob", date="Thu 1 Oct · Static", slides=[
    dict(kind="ph_static", name="P11MeetRob", kicker="The builder",
         headline="You’ll deal with Rob. First chat to handover.", size=50,
         sub="Rob Williamson · Builder & Director",
         note="A phone portrait on site in good light is enough"),
]))

# ---- Post 12 ----------------------------------------------------------------
POSTS.append(dict(id="P12", page="Post 12 · How we work", date="Sun 4 Oct · Carousel", slides=[
    dict(kind="photo_cover", name="P12Cover", kicker="How we work", photo="rear.jpg", focus="center 50%",
         headline="One or two builds at a time. On purpose.", size=64,
         sub="Fewer builds, better results.", num=n(1, 5)),
    dict(kind="point", kicker="What it means", headline="Your job isn’t queued behind six others", size=68, num=n(2, 5),
         body=["The attention it gets is the attention it needs."]),
    dict(kind="point", deep=True, kicker="What we build", headline="Homes, renovations, extensions, secondary dwellings", size=58, num=n(3, 5),
         body=["New builds, full renovations, second storeys, self-contained living."]),
    dict(kind="point", kicker="Honestly", headline="It means we can’t always start straight away", size=66, num=n(4, 5),
         body=["It also means the job in front of us is the one that matters."]),
    dict(kind="cta", headline="Planning something for next year?", size=72, num=n(5, 5),
         meta="Gold Coast · QBCC licensed · Master Builders Queensland"),
]))


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
