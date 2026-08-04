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
from build_pages import FORM, MEDIA_BASE, NAV, FOOTER  # single shared source, see build_pages.py FORM comment (ENG-09)


def srcset(base, ext):
    return ", ".join(f"{MEDIA_BASE}{base}-{w}.{ext} {w}w" for w in MAN[base]["widths"])


def picture(base, alt, sizes, cls="", eager=False, extra=""):
    widths = MAN[base]["widths"]
    largest = widths[-1]
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (
        f'<picture><source type="image/webp" srcset="{srcset(base,"webp")}" sizes="{sizes}"/>'
        f'<img {cls} src="{MEDIA_BASE}{base}-{largest}.jpg" srcset="{srcset(base,"jpg")}" sizes="{sizes}" '
        f'{load} alt="{alt}"{extra}/></picture>'
    )


# NAV/FOOTER imported from build_pages.py above (ENG-09) — both are
# now just removal-notice placeholders; see that file's comment.

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

<div id="pg-lightbox" role="dialog" aria-modal="true" aria-label="Photo" aria-hidden="true">
  <button type="button" id="pgClose" class="lb-close">Close</button>
  <button type="button" id="pgPrev" class="pg-nav pg-prev" aria-label="Previous photo">&larr;</button>
  <img id="pgImg" alt=""/>
  <button type="button" id="pgNext" class="pg-nav pg-next" aria-label="Next photo">&rarr;</button>
</div>

<script src="assets/prestige.js"></script>
</body>
</html>
"""


# ---------------------------------------------------------------- case-study components

def cs_hero(base, alt, video=None, video_mobile=None):
    """Full-bleed opening frame. Mirrors the homepage's .work-item.bleed
    full-bleed plate exactly (not build_pages.py's hero(), which builds a
    <header> banner — the wrong shape for a case-study opening image).

    video, when given, is a filename under assets/ (not manifest-driven —
    it's a single delivery file, not a responsive srcset). The existing
    largest still for `base` is reused as the poster, so there's no new
    asset to source just for the loading frame. autoplay/muted/loop are
    native attributes so the video plays with no JS; prestige.js only
    steps in to stop it for prefers-reduced-motion.

    video_mobile, when given, is a smaller/lower-bitrate cut served via a
    media-queried <source> ahead of the full one — same technique <picture>
    uses for responsive images, supported on <video> too. Without it,
    every visitor downloads the same ~12MB file regardless of viewport
    (flagged in /impeccable audit)."""
    if video:
        # Project videos are never uploaded to WordPress (they're the raw
        # delivery cuts, often 20-40MB) — always served from local assets/,
        # unlike the still images which mostly are WP-hosted.
        poster = f"{MEDIA_BASE}{base}-{MAN[base]['widths'][-1]}.jpg"
        mobile_source = (
            f'<source src="assets/{video_mobile}" type="video/mp4" media="(max-width: 640px)"/>'
            if video_mobile else ""
        )
        return f"""<div class="work-item bleed">
  <div class="plate reveal"><video class="hero-video" poster="{poster}" autoplay muted loop playsinline preload="auto" aria-label="{alt}">{mobile_source}<source src="assets/{video}" type="video/mp4"/></video>
    <button type="button" class="sound-toggle" aria-pressed="false" aria-label="Turn sound on">
      <svg class="so-off" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 9v6h4l5 5V4L8 9H4z" fill="currentColor"/><path d="M17 7l6 10M23 7l-6 10" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
      <svg class="so-on" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 9v6h4l5 5V4L8 9H4z" fill="currentColor"/><path d="M16 8.5c1.2 1 2 2.6 2 4.5s-.8 3.5-2 4.5M18.5 6c2 1.6 3.2 4 3.2 7s-1.2 5.4-3.2 7" stroke="currentColor" stroke-width="1.5" fill="none" stroke-linecap="round"/></svg>
    </button>
  </div>
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


def cs_gallery(slug, count, client):
    """Full photo set for the project: a horizontal-scroll carousel of every
    real delivered photo, each opening the shared #pg-lightbox (prestige.js)
    at full size on click. Distinct from cs_sequence()'s curated bleed/two-up
    rhythm — this is the exhaustive "every photo" strip, not a highlight reel.
    The strip breaks out of .wrap (edge-to-edge) so it reads as a filmstrip,
    not a page-filling grid. count=0 renders nothing (no hollow section ships
    for projects with no gallery photos yet, e.g. SOL which ships video-only)."""
    if not count:
        return ""
    items = "\n    ".join(
        f'<a href="assets/gallery-{slug}-{n}-full.jpg" class="pg-item" data-full-webp="assets/gallery-{slug}-{n}-full.webp">'
        f'<picture><source type="image/webp" srcset="assets/gallery-{slug}-{n}-thumb.webp"/>'
        f'<img src="assets/gallery-{slug}-{n}-thumb.jpg" loading="lazy" decoding="async" alt="{client} — photo {n}"/></picture></a>'
        for n in range(1, count + 1)
    )
    return f"""<section class="pad-tight">
  <div class="wrap">
    <h2 class="reveal h2m h-small"><span>Every frame.</span></h2>
  </div>
  <div class="pg-strip reveal stgr">
    {items}
  </div>
</section>"""


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
    sequence=[],   # ENG-02 closed as not needed: SOL ships with the hero video below,
                   # no separate image sequence — see wiki/projects/10x-website.md
    quote=None,    # no confirmed client quote yet; not a placeholder
    hero_video="sol-hero.mp4",
    hero_video_mobile="sol-hero-mobile.mp4",
    close=("Building something with this much craft?", "Tell us what you're building. We will tell you what it needs."),
)

# Davenport, Salisbury, Elysium, Broncos and Stonehaven each now have a
# full delivered photo set (cs_gallery, gallery_slug/gallery_count) plus a
# hero video.
# sequence stays [] for all five — the curated bleed/two-up rhythm isn't
# used here, the exhaustive gallery grid covers it instead.

PAGES["davenport.html"] = dict(
    title="Davenport | 10x Visuals",
    desc="Davenport, a refined hillside residence marketed by PRD Burleigh, captured for its atmosphere rather than its floor area.",
    client="PRD Burleigh",
    discipline="Film &amp; Photography",
    hero_base="work-davenport",
    hero_alt="Davenport, a refined hillside residence marketed by PRD Burleigh, looking out over the pool.",
    brief=["A refined hillside residence, captured for its atmosphere rather than its floor area."],
    sequence=[],
    quote=None,
    hero_video="davenport-hero.mp4",
    hero_video_mobile="davenport-hero-mobile.mp4",
    gallery_slug="davenport",
    gallery_count=32,
    close=("Building somewhere with a view like this?", "Tell us what you're building. We will tell you what it needs."),
)

PAGES["salisbury.html"] = dict(
    title="Kennedys Lane | 10x Visuals",
    desc="Kennedys Lane, a completed build delivered by Salisbury Building Projects, documented from the air.",
    client="Salisbury Building Projects",
    discipline="Film &amp; Photography",
    hero_base="work-salisbury",
    hero_alt="Kennedys Lane, a completed build delivered by Salisbury Building Projects, seen from above.",
    brief=["A completed build for Salisbury Building Projects, captured from the air to show the property in full."],
    sequence=[],
    quote=None,
    hero_video="salisbury-hero.mp4",
    hero_video_mobile="salisbury-hero-mobile.mp4",
    gallery_slug="salisbury",
    gallery_count=46,
    close=("Finishing a build worth showing off?", "Tell us what you're building. We will tell you what it needs."),
)

PAGES["elysium.html"] = dict(
    title="Elysium | 10x Visuals",
    desc="Elysium, a completed large scale apartment development delivered by Shape Construction, documented for scale and quality once complete.",
    client="Shape Construction",
    discipline="Film &amp; Photography",
    hero_base="work-elysium",
    hero_alt="Elysium, a completed large scale apartment development delivered by Shape Construction.",
    brief=["A large scale apartment build, documented for scale and quality once complete."],
    sequence=[],
    quote=None,
    hero_video="elysium-hero.mp4",
    hero_video_mobile="elysium-hero-mobile.mp4",
    gallery_slug="elysium",
    gallery_count=50,
    close=("Delivering something on this scale?", "Tell us what you're building. We will tell you what it needs."),
)

PAGES["broncos-leagues-club.html"] = dict(
    title="Broncos Leagues Club | 10x Visuals",
    desc="The refurbished Broncos Leagues Club interior, delivered by Ashley Cooper Construction, recorded from before to completion.",
    client="Ashley Cooper Construction",
    discipline="Progress &amp; Completion",
    hero_base="work-broncos",
    hero_alt="The refurbished Broncos Leagues Club interior, delivered by Ashley Cooper Construction.",
    brief=["A major refurbishment recorded from before to completion for the builder’s portfolio."],
    sequence=[],
    quote=None,
    hero_video="broncos-hero.mp4",
    hero_video_mobile="broncos-hero-mobile.mp4",
    gallery_slug="broncos",
    gallery_count=40,
    close=("Documenting a project of your own?", "Tell us what you're building. We will tell you what it needs."),
)

PAGES["stonehaven.html"] = dict(
    title="Stonehaven | 10x Visuals",
    desc="Stonehaven at 47 Somerset Drive, marketed by Whitefox: a new build on acreage, shot across dusk and daylight.",
    client="Whitefox &nbsp;&middot;&nbsp; 47 Somerset Drive",
    discipline="Film &amp; Photography",
    hero_base="work-stonehaven",
    hero_alt="Stonehaven, the front elevation at 47 Somerset Drive, symmetrical under a clear sky.",
    brief=["A new build on acreage, shot across dusk and daylight for the facade, the interiors and the grounds."],
    sequence=[],
    quote=None,
    hero_video="stonehaven-hero.mp4",
    hero_video_mobile="stonehaven-hero-mobile.mp4",
    gallery_slug="stonehaven",
    gallery_count=57,
    close=("Building something worth this kind of presentation?", "Tell us what you're building. We will tell you what it needs."),
)

# ---------------------------------------------------------------- write

if __name__ == "__main__":
    written = []
    for fn, d in PAGES.items():
        sections = [cs_hero(d["hero_base"], d["hero_alt"], d.get("hero_video"), d.get("hero_video_mobile")),
                    cs_brief(d["title"].split(" | ")[0], d["client"], d["discipline"], d["brief"])]
        seq = cs_sequence(d["sequence"])
        if seq:
            sections.append(seq)
        gallery = cs_gallery(d.get("gallery_slug"), d.get("gallery_count", 0), d["client"])
        if gallery:
            sections.append(gallery)
        if d["quote"]:
            sections.append(cs_quote(d["quote"]["text"], d["quote"]["attr"]))

        body = "\n\n".join(sections)
        # A video hero doesn't want its poster still preloaded as a competing
        # download; only preload the image when there's no video to paint first.
        preload = None if d.get("hero_video") else d["hero_base"]
        open(os.path.join(ROOT, fn), "w").write(
            shell(d["title"], d["desc"], d["hero_base"], body, preload_base=preload))
        written.append(fn)

    for f in written:
        print(f"{f:20} {os.path.getsize(os.path.join(ROOT, f)):>7} bytes")
