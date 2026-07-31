#!/usr/bin/env python3
"""Generate the case-study pages of the 10x site against the Prestige layer.

Mirrors scripts/build_pages.py exactly: same ROOT, same manifest, same
picture()/srcset() helpers, same NAV/FOOTER/FORM/close_block()/shell().
No new CSS classes. A case study composes existing components:

    cs_hero()     -> the homepage's full-bleed .bleed/.plate pattern
    cs_brief()     -> prose(..., statement=True)'s .ed/.statement split
    cs_sequence()  -> the homepage's alternating .bleed/.two-up rhythm
    cs_quote()     -> the homepage testimonial's .tq/.tattr markup

quote=None is a real branch, not a placeholder: cs_quote() is simply not
called. sequence=[] is allowed for the same reason: cs_sequence() returns
an empty string rather than rendering a hollow section.
"""
import json, os, sys

ROOT = "/Users/10xhunter/Documents/Hunters Second Brain/projects/10x-site"
MAN = json.load(open(os.path.join(ROOT, "assets/manifest.json")))
sys.path.insert(0, os.path.dirname(__file__))
from build_pages import FORM  # single shared source, see build_pages.py FORM comment (ENG-09)


def srcset(base, ext):
    return ", ".join(f"assets/{base}-{w}.{ext} {w}w" for w in MAN[base]["widths"])


def picture(base, alt, sizes, cls="", eager=False, extra=""):
    widths = MAN[base]["widths"]
    largest = widths[-1]
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (
        f'<picture><source type="image/webp" srcset="{srcset(base,"webp")}" sizes="{sizes}"/>'
        f'<img {cls} src="assets/{base}-{largest}.jpg" srcset="{srcset(base,"jpg")}" sizes="{sizes}" '
        f'{load} alt="{alt}"{extra}/></picture>'
    )


NAV = """<nav id="mainNav">
  <div class="bar">
    <a href="index.html" class="wordmark serif">10X&nbsp;VISUALS</a>
    <div class="links">
      <a class="nlink" href="branding.html">Branding</a>
      <a class="nlink" href="content-creation.html">Content</a>
      <a class="nlink" href="lead-generation.html">Lead Gen</a>
      <a class="nlink" href="systems-processes.html">AI Systems</a>
      <a class="nlink" href="contact-us.html">Contact</a>
    </div>
    <button type="button" id="menuToggle" class="nlink only" aria-haspopup="true" aria-expanded="false" aria-controls="menuOverlay">Menu</button>
  </div>
</nav>

<div id="menuOverlay" role="dialog" aria-modal="true" aria-label="Site menu" aria-hidden="true">
  <div class="mo-top">
    <a href="index.html" class="wordmark serif">10X&nbsp;VISUALS</a>
    <button type="button" id="menuClose" class="tlink">Close</button>
  </div>
  <nav class="mo-links" aria-label="Site">
    <a href="branding.html">Branding</a>
    <a href="content-creation.html">Content</a>
    <a href="lead-generation.html">Lead Gen</a>
    <a href="systems-processes.html">AI Systems</a>
    <a href="contact-us.html">Contact</a>
  </nav>
  <div class="mo-foot">
    <a href="mailto:hello@10xvisuals.com.au">hello@10xvisuals.com.au</a>
    <a href="tel:+61431516634">0431 516 634</a>
  </div>
</div>"""

FOOTER = """<footer>
  <div class="wrap inner">
    <p class="mark">10X VISUALS</p>
    <div class="fl">
      <a href="mailto:hello@10xvisuals.com.au">Email</a>
      <a href="tel:+61431516634">0431 516 634</a>
      <a href="https://www.instagram.com/10xvisuals_/" rel="noopener">Instagram</a>
      <a href="/privacy-policy">Privacy Policy</a>
      <p>&copy; 2026 10x Visuals Pty Ltd</p>
    </div>
  </div>
</footer>"""

def close_block(heading, lede):
    return f"""<section id="close" class="on-paper pad-wide">
  <div class="wrap left stagger">
    <div class="reveal"><div class="hero-rule"></div></div>
    <h2 class="reveal h2m statement"><span>{heading}</span></h2>
    <p class="lede reveal">{lede}</p>
{FORM}
  </div>
</section>"""


def shell(title, desc, hero_base, body, preload_base=None):
    pre = ""
    if preload_base:
        pre = ('<link rel="preload" as="image" type="image/webp" imagesrcset="'
               + srcset(preload_base, "webp") + '" imagesizes="100vw" fetchpriority="high"/>\n')
    return f"""<!DOCTYPE html>
<html lang="en-AU">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>{title}</title>
<meta name="description" content="{desc}"/>
{pre}<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Prata&family=Montserrat:wght@300;400;500;600&display=swap" rel="stylesheet"/>
<link rel="stylesheet" href="assets/prestige.css"/>
</head>
<body>

<span id="scrollProgress" aria-hidden="true"></span>

{NAV}

<main>
{body}
</main>

{FOOTER}

<script src="assets/prestige.js"></script>
</body>
</html>
"""


# ---------------------------------------------------------------- case-study components

def cs_hero(base, alt, video=None):
    """Full-bleed opening frame. Mirrors the homepage's .work-item.bleed
    full-bleed plate exactly (not build_pages.py's hero(), which builds a
    <header> banner — the wrong shape for a case-study opening image).

    video, when given, is a filename under assets/ (not manifest-driven —
    it's a single delivery file, not a responsive srcset). The existing
    largest still for `base` is reused as the poster, so there's no new
    asset to source just for the loading frame. autoplay/muted/loop are
    native attributes so the video plays with no JS; prestige.js only
    steps in to stop it for prefers-reduced-motion."""
    if video:
        poster = f"assets/{base}-{MAN[base]['widths'][-1]}.jpg"
        return f"""<div class="work-item bleed">
  <div class="plate reveal"><video class="hero-video" poster="{poster}" autoplay muted loop playsinline preload="auto" aria-label="{alt}"><source src="assets/{video}" type="video/mp4"/></video></div>
</div>"""
    return f"""<div class="work-item bleed">
  <div class="plate reveal">{picture(base, alt, "100vw", eager=True)}</div>
</div>"""


def cs_brief(title, client, discipline, paras):
    """Project title as the page's one statement heading, in the same
    .ed/.statement editorial split prose(..., statement=True) uses."""
    ps = "\n        ".join(f'<p class="lede">{p}</p>' for p in paras)
    return f"""<section class="pad-wide">
  <div class="wrap ed stagger">
    <h2 class="statement reveal h2m"><span>{title}</span></h2>
    <div class="reveal">
        <p class="w-client">{client} &nbsp;&middot;&nbsp; {discipline}</p>
        {ps}
    </div>
  </div>
</section>"""


def cs_sequence(images):
    """Alternating .bleed / .two-up rhythm, same as the homepage work
    grid. images: list of {"base":..., "alt":...}. Even index -> full
    bleed, odd pair -> two-up. Empty list renders nothing (no hollow
    section ships when sequence=[])."""
    if not images:
        return ""
    blocks = []
    i = 0
    while i < len(images):
        if i % 3 == 0 or i == len(images) - 1:
            img = images[i]
            blocks.append(f"""<div class="work-item bleed">
  <div class="plate reveal">{picture(img["base"], img["alt"], "100vw")}</div>
</div>""")
            i += 1
        else:
            pair = images[i:i + 2]
            cells = "\n    ".join(
                f'<div class="plate reveal">{picture(p["base"], p["alt"], "(max-width:820px) 100vw, 47vw")}</div>'
                for p in pair
            )
            blocks.append(f"""<div class="work-item wrap two-up">
    {cells}
  </div>""")
            i += len(pair)
    return "\n\n".join(blocks)


def cs_quote(text, attr):
    """Mirrors the homepage #testimonial section's .tq/.tattr markup
    verbatim. Not called at all when quote is None."""
    return f"""<section class="dark">
  <div class="wrap stagger">
    <div class="reveal"><div class="hero-rule"></div></div>
    <blockquote class="tq reveal">{text}</blockquote>
    <p class="label tattr reveal">{attr}</p>
  </div>
</section>"""


# ---------------------------------------------------------------- pages

PAGES = {}

PAGES["sol.html"] = dict(
    title="SOL | 10x Visuals",
    desc="A canal side compound for Skye Development Group, filmed and photographed for the architecture, the water and the finish.",
    client="Skye Development Group",
    discipline="Film &amp; Photography",
    hero_base="work-sol",
    hero_alt="SOL by Skye Development Group, the completed canal side compound lit at night.",
    brief=[
        "A canal side compound on the Gold Coast, delivered by Skye Development Group.",
        "10x shot the architecture, the waterfront setting and the premium finishes across both day and night, for use in the developer's own marketing.",
    ],
    sequence=[],   # populated in ENG-02 once frames are selected (CONTENT-01)
    quote=None,    # no confirmed client quote yet; not a placeholder
    hero_video="sol-hero.mp4",  # working cut, Hunter is re-editing a final version
    close=("Building something with this much craft?", "Tell us what you're building. We will tell you what it needs."),
)

# Davenport, Bespoke, Elysium, Broncos Leagues Club, Stonehaven follow the
# same shape in later tickets (ENG-04 through ENG-08).

# ---------------------------------------------------------------- write

if __name__ == "__main__":
    written = []
    for fn, d in PAGES.items():
        sections = [cs_hero(d["hero_base"], d["hero_alt"], d.get("hero_video")),
                    cs_brief(d["title"].split(" | ")[0], d["client"], d["discipline"], d["brief"])]
        seq = cs_sequence(d["sequence"])
        if seq:
            sections.append(seq)
        if d["quote"]:
            sections.append(cs_quote(d["quote"]["text"], d["quote"]["attr"]))
        sections.append(close_block(*d["close"]))

        body = "\n\n".join(sections)
        # A video hero doesn't want its poster still preloaded as a competing
        # download; only preload the image when there's no video to paint first.
        preload = None if d.get("hero_video") else d["hero_base"]
        open(os.path.join(ROOT, fn), "w").write(
            shell(d["title"], d["desc"], d["hero_base"], body, preload_base=preload))
        written.append(fn)

    for f in written:
        print(f"{f:20} {os.path.getsize(os.path.join(ROOT, f)):>7} bytes")
