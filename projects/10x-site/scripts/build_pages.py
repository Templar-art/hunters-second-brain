#!/usr/bin/env python3
"""Generate the five interior pages of the 10x site against the Prestige layer.

Copy is taken verbatim from the live WordPress pages, with three edits applied
consistently: the tracked eyebrows ("// Branding", "// Why Systems Matter") are
dropped per DESIGN.md's No-Eyebrow Rule, the numbered list markers ("1. Strategy
& Positioning") lose their numbers per the No-Numbers Rule since these are lists
rather than ordered sequences, and en/em dashes are removed per the No-Dashes
Rule. Nothing is invented.
"""
import json, os, html

ROOT = "/Users/10xhunter/Documents/Hunters Second Brain/projects/10x-site"
MAN = json.load(open(os.path.join(ROOT, "assets/manifest.json")))
# Media (images/video) is hosted on the live WordPress media library so the
# static site doesn't need to ship these files itself. prestige.css/js stay
# local (site-relative). See wiki/projects/10x-website.md for the export.
MEDIA_BASE = "https://10xvisuals.com.au/wp-content/uploads/2026/08/"


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
    <a href="mailto:marketing@10xvisuals.com.au">marketing@10xvisuals.com.au</a>
    <a href="tel:+61431516634">0431 516 634</a>
  </div>
</div>"""

FOOTER = """<footer>
  <div class="wrap inner">
    <p class="mark">10X VISUALS</p>
    <div class="fl">
      <a href="mailto:marketing@10xvisuals.com.au">Email</a>
      <a href="tel:+61431516634">0431 516 634</a>
      <a href="https://www.instagram.com/10xvisuals_/" rel="noopener">Instagram</a>
      <a href="/privacy-policy">Privacy Policy</a>
      <p>&copy; 2026 10x Visuals Pty Ltd</p>
    </div>
  </div>
</footer>"""

# Shared source for both generators (build_case_studies.py imports this
# constant rather than redeclaring it - ENG-09). index.html's own inline
# copy of this same form is NOT generated and must be kept in sync with
# this constant by hand; that duplicate is a documented exception, not
# an oversight.
FORM = """    <form id="enquiry" novalidate>
      <div class="fields">
        <div class="field" id="f-name">
          <label for="i-name">Name</label>
          <input id="i-name" name="name" type="text" autocomplete="name" maxlength="80" required aria-describedby="e-name"/>
          <p class="err" id="e-name" role="alert">Please add your name.</p>
        </div>
        <div class="field" id="f-email">
          <label for="i-email">Email</label>
          <input id="i-email" name="email" type="email" autocomplete="email" inputmode="email" maxlength="120" required aria-describedby="e-email"/>
          <p class="err" id="e-email" role="alert">Please add a valid email, including the @.</p>
        </div>
        <div class="field" id="f-phone">
          <label for="i-phone">Phone</label>
          <input id="i-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" maxlength="24" required aria-describedby="e-phone"/>
          <p class="err" id="e-phone" role="alert">Please add a contact number, at least eight digits.</p>
        </div>
      </div>
      <div class="submit"><button class="tlink magnetic" type="submit">Send enquiry</button></div>
      <p class="form-alt">We&rsquo;ll only use this to reply.</p>
      <p class="form-alt">Or reach us directly on <a href="tel:+61431516634">0431 516 634</a> or <a href="mailto:marketing@10xvisuals.com.au">marketing@10xvisuals.com.au</a>.</p>
    </form>
    <p class="form-done" id="formDone" role="status" tabindex="-1">Thank you. We will be in touch within one business day.</p>
    <p class="form-fail" id="formFail" role="alert">That didn't send. Call 0431 516 634 or email marketing@10xvisuals.com.au and we will pick it up.</p>"""


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


def hero(base, alt, label, h1_lines, lede, value_line=None):
    lines = "\n      ".join(f'<span class="ln"><span>{l}</span></span>' for l in h1_lines)
    value_p = f'\n      <p class="lede-h">{value_line}</p>' if value_line else ""
    return f"""<header id="top" class="hero-sm">
  {picture(base, alt, "100vw", cls='class="hero-img"', eager=True)}
  <div class="hero-veil"></div>
  <div class="hero-inner">
    <div class="fade d1">
      <div class="hero-rule"></div>
      <p class="label hero-kicker" style="color:var(--ivory);margin-bottom:22px;">{label}</p>
    </div>
    <h1>
      {lines}
    </h1>
    <div class="hero-meta fade d3">
      <p class="lede-h">{lede}</p>{value_p}
      <a class="tlink magnetic" href="#close">Start a project</a>
    </div>
  </div>
  <div class="scroll-cue fade d3" aria-hidden="true"><span class="sc-rule"></span>Scroll</div>
</header>"""


def prose(heading, paras, dark=False, pad_top_zero=False, statement=False):
    """statement=True renders the page's one big thesis in the same
    editorial split as the homepage's studio section: a wide Prata
    heading in a left rail beside the prose, no hairline eyebrow. Every
    other heading on the page stays at label scale (h-small), matching
    how the homepage treats its own section headings."""
    cls = ' class="dark"' if dark else ""
    if statement:
        ps = "\n        ".join(f'<p class="lede">{p}</p>' for p in paras)
        return f"""<section{cls} class="pad-wide">
  <div class="wrap ed stagger">
    <h2 class="statement reveal h2m"><span>{heading}</span></h2>
    <div class="reveal">
        {ps}
    </div>
  </div>
</section>"""
    ps = "\n    ".join(f'<p class="lede reveal">{p}</p>' for p in paras)
    style = ' style="padding-top:0;"' if pad_top_zero else ""
    return f"""<section{cls}{style}>
  <div class="wrap stagger">
    <h2 class="reveal h2m h-small"><span>{heading}</span></h2>
    {ps}
  </div>
</section>"""


def offer(heading, items, dark=False):
    rows = []
    for name, paras in items:
        body = "".join(f"<p>{p}</p>" for p in paras)
        rows.append(f'      <div class="row"><span class="rt">{name}</span><div class="rd">{body}</div></div>')
    rows = "\n".join(rows)
    cls = ' class="dark"' if dark else ""
    return f"""<section{cls}>
  <div class="wrap stagger">
    <h2 class="reveal h2m h-small"><span>{heading}</span></h2>
    <div class="offer reveal stgr">
{rows}
    </div>
  </div>
</section>"""


def interlude(base, alt, quote):
    return f"""<div class="interlude">
  {picture(base, alt, "100vw", extra=' data-par="0.12"')}
  <div class="veil"></div>
  <div class="inner reveal">
    <p class="quote">{quote}</p>
  </div>
</div>"""


# ---------------------------------------------------------------- pages

PAGES = {}

PAGES["branding.html"] = dict(
    title="Branding &amp; Design | 10x Visuals",
    desc="Strategy, identity and the guidelines that keep it intact. Branding for property, construction and the businesses behind them.",
    hero_base="hero-branding",
    hero_alt="A refined living space at Stonehaven, photographed for Whitefox.",
    label="Branding",
    h1=["Where strategy", "becomes identity."],
    lede="We design brands with clarity, confidence and lasting impact.",
    value_line="One clear identity, working the same way across every place people encounter your business.",
    intro=("Branding that creates clarity", [
        "Your brand is more than a logo. It is the perception people form the moment they encounter your business.",
        "We develop clear, strategic identities that define who you are, communicate what you stand for, and position your brand to be recognised and remembered.",
    ]),
    why=("Perception drives decisions", [
        "People often decide how they feel about a business within seconds. Branding influences that moment.",
        "When your identity is clear, professional and consistent, it builds confidence and credibility, helping potential clients feel they are choosing a business they can trust.",
    ]),
    offer_heading="What goes into a powerful brand.",
    items=[
        ("Strategy &amp; Positioning", ["Before design begins, clarity comes first. We define how your business should be positioned in the market, who it speaks to, and what makes it different.",
                                        "This strategic foundation ensures every visual and communication decision moving forward has direction and purpose."]),
        ("Brand Identity", ["Your logo is the most recognisable symbol of your business. We design distinctive, balanced marks that represent your brand clearly and scale across everything from websites to signage.",
                            "The goal is a logo that feels timeless, confident and instantly recognisable."]),
        ("Visual Identity", ["Beyond the logo, your brand needs a visual language. We develop colour palettes, typography systems, layouts and graphic elements that create a cohesive look across every platform.",
                             "This identity ensures your brand feels consistent and professional wherever it appears."]),
        ("Website Design", ["Your website is often the first place people experience your brand.",
                            "We design websites that reflect your identity, communicate your message clearly, and create a polished digital presence that strengthens trust and perception."]),
        ("Brand Guidelines", ["Consistency is what turns design into a brand. We create clear brand guidelines that outline how your identity should be used across marketing, digital platforms and future materials.",
                              "This ensures your brand remains consistent as your business grows."]),
        ("Capability Documents", ["Businesses evolve, and sometimes their identity needs to evolve with them.",
                                  "Whether it is a full rebrand or a refined update, we help modernise brands while maintaining the strength of what already works."]),
    ],
    quote="Average brands compete. Great brands dominate.",
    interlude_base="work-salisbury",
    interlude_alt="Kennedys Lane, a completed build delivered by Salisbury Building Projects, seen from above.",
    close=("The right brand changes everything.", "Tell us what you're building. We will tell you what it needs."),
)

PAGES["content-creation.html"] = dict(
    title="Content, Photography &amp; Film | 10x Visuals",
    desc="Cinematic photography and film for property, construction and the brands behind them.",
    hero_base="hero-content",
    hero_alt="The garden and firepit terrace at Stonehaven in late afternoon light.",
    label="Content",
    h1=["Visuals that speak", "for your brand."],
    lede="High quality photo and video content designed to strengthen perception and capture attention.",
    value_line="Photography and film that let people judge the quality of your work before you say a word.",
    intro=("Content that brings your brand to life", [
        "Content is often the first way people experience your brand. High quality photography and videography allow businesses to communicate clearly, showcase their work, and build trust with their audience.",
        "We create cinematic visuals that highlight what makes your business unique and present it with clarity, professionalism and impact.",
    ]),
    why=("Where first impressions are made", [
        "People respond to what they can see and experience. Strong visual content captures attention, builds credibility, and helps potential clients understand the quality of your work instantly.",
        "Whether it is a project showcase, brand story or social media campaign, powerful visuals elevate perception and make your business far more memorable.",
    ]),
    offer_heading="Crafting visual experiences.",
    items=[
        ("Photography", ["Professional photography captures the details that define your business.",
                         "From architectural spaces and project showcases to brand imagery, high quality photography creates a strong visual foundation that can be used across websites, marketing and campaigns."]),
        ("Videography", ["Video allows brands to communicate movement, atmosphere and story.",
                         "We produce cinematic video content that highlights the character of a space, project or brand, helping businesses create a stronger emotional connection with their audience."]),
        ("Project Showcases", ["For industries such as construction, architecture and property, documenting completed projects is essential.",
                               "We capture finished builds and developments through carefully composed photography and video, creating powerful assets for portfolios, marketing and future opportunities."]),
        ("Brand Story Content", ["Behind every business is a story worth sharing.",
                                 "Through thoughtful visuals and carefully crafted scenes, we create content that reflects the personality, culture and values that define a brand."]),
        ("Social &amp; Marketing Content", ["Consistent visual content helps businesses stay visible and relevant.",
                                            "We produce versatile assets designed for social media, campaigns and digital marketing, ensuring brands always have professional visuals ready to communicate with their audience."]),
        ("Editing &amp; Production", ["The final impact of content comes from careful refinement.",
                                      "Colour grading, editing and visual composition transform raw footage and images into polished, cinematic assets that elevate the overall presentation of a brand."]),
    ],
    quote="Cinematic content for businesses that refuse to look average.",
    interlude_base="work-sol",
    interlude_alt="SOL by Skye Development Group, the completed canal side compound lit at night.",
    close=("The right visuals change everything.", "Tell us what you're building. We will tell you what it needs."),
)

PAGES["lead-generation.html"] = dict(
    title="Lead Generation | 10x Visuals",
    desc="Campaigns, search visibility and landing pages built to produce enquiries, not impressions.",
    hero_base="hero-leadgen",
    hero_alt="The front elevation and lawn at Stonehaven, 47 Somerset Drive.",
    label="Lead Gen",
    h1=["Turn attention", "into enquiries."],
    lede="Strategic advertising and search visibility designed to bring the right people to your business.",
    value_line="Search and advertising built to reach people already looking for what you offer.",
    intro=("Lead generation that drives real enquiries", [
        "Great marketing does more than attract attention. It connects businesses with the people actively looking for their services.",
        "Through targeted advertising and search visibility, we help businesses generate consistent enquiries and build predictable growth.",
    ]),
    why=("Where growth begins", [
        "The right strategy ensures your business appears when people are ready to act.",
        "Strong lead generation connects you with high intent audiences, turning visibility into enquiries and opportunities into real growth.",
    ]),
    offer_heading="Driving consistent enquiries.",
    items=[
        ("Meta Advertising", ["Platforms like Facebook and Instagram allow businesses to reach highly targeted audiences.",
                              "Through strategic campaign design, we create advertising that introduces brands, builds awareness and generates new opportunities."]),
        ("Google Ads", ["Google Ads places your business directly in front of people searching for your services.",
                        "We build and manage targeted campaigns designed to capture high intent traffic and convert searches into enquiries."]),
        ("Search Engine Optimisation", ["Search visibility ensures your business is discovered organically.",
                                        "Through technical optimisation, content strategy and search positioning, we help businesses improve their rankings and attract long term traffic."]),
        ("Landing Pages", ["Strong advertising needs strong destinations.",
                           "We design and optimise landing pages that guide visitors toward action, increasing the likelihood that traffic turns into real enquiries."]),
        ("Conversion Optimisation", ["Small improvements can create major differences in results.",
                                     "We refine campaign structure, messaging and user journeys to maximise the number of leads generated from existing traffic."]),
        ("Performance Tracking", ["Growth is driven by data.",
                                  "Through tracking and reporting systems, we monitor campaign performance and continuously refine strategies to ensure lead generation remains efficient and scalable."]),
    ],
    quote="Traffic is easy. Leads are what matter.",
    interlude_base="work-elysium",
    interlude_alt="Elysium, a completed large scale apartment development delivered by Shape Construction.",
    close=("Stop relying on referrals.", "Tell us what you're building. We will tell you what it needs."),
)

PAGES["systems-processes.html"] = dict(
    title="AI Systems &amp; Automation | 10x Visuals",
    desc="Automation, CRM and infrastructure that let a small team run at volume.",
    hero_base="hero-systems",
    hero_alt="The alfresco dining terrace at Stonehaven, open to the pool.",
    label="AI Systems",
    h1=["Build a business", "that runs smarter."],
    lede="Automation, systems and infrastructure designed to streamline operations and support scalable growth.",
    value_line="Automation and CRM that keep every enquiry moving, without extra admin.",
    intro=("AI systems that support growth", [
        "As businesses grow, complexity increases. Systems and processes create the structure that allows teams to operate efficiently, manage leads effectively, and maintain consistency across every stage of the client journey.",
        "We help businesses implement smarter workflows and automation that reduce friction and create scalable foundations for growth.",
    ]),
    why=("Where efficiency begins", [
        "When systems are clear and connected, businesses operate with greater speed and confidence. Automation removes repetitive tasks, improves communication, and ensures every opportunity is managed properly.",
        "The result is a business that runs smoother, responds faster, and scales without unnecessary complexity.",
    ]),
    offer_heading="Building smarter infrastructure.",
    items=[
        ("CRM Setup", ["Customer relationship management systems provide visibility across leads, clients and ongoing projects.",
                       "We implement CRM platforms that help businesses track opportunities, manage communication and maintain organised pipelines."]),
        ("Workflow Automation", ["Automation removes manual tasks and repetitive processes.",
                                 "By connecting tools and creating automated workflows, businesses can reduce administrative work and focus more time on high value activities."]),
        ("Sales Pipelines", ["A structured pipeline ensures opportunities are managed properly from enquiry to conversion.",
                             "We design clear sales processes that help businesses track progress, follow up consistently and convert more leads into clients."]),
        ("Lead Management", ["Incoming enquiries need to be handled efficiently.",
                             "Through automated responses, lead routing and structured tracking systems, we ensure opportunities are captured and managed effectively."]),
        ("Integrations", ["Businesses often rely on multiple platforms.",
                          "We connect marketing tools, CRM systems and communication software so information flows seamlessly between systems."]),
        ("Process Optimisation", ["As businesses grow, workflows can become inefficient.",
                                  "We analyse operational processes and refine them to improve speed, organisation and overall productivity."]),
    ],
    quote="The future of your business is automated. We'll build it.",
    interlude_base="interlude",
    interlude_alt="A hinterland residence at twilight, interiors lit, pool glowing.",
    close=("Ready to run a smarter business?", "Tell us what you're building. We will tell you what it needs."),
)

FAQS = [
    ("What types of businesses do you work with?",
     "We work with a wide range of businesses across different industries. Our clients include construction companies, trades, real estate groups, property developers, professional services, and growing brands that want to strengthen their marketing and digital presence. As a full service agency, we adapt our strategies to suit each industry and business stage."),
    ("What services do you offer?",
     "Our services cover the full spectrum of modern marketing and digital growth. This includes branding, website design, photography and videography, paid advertising, SEO, and business systems such as automation and CRM implementation."),
    ("Do you offer one off shoots or projects?",
     "Yes. While many of our clients work with us on ongoing marketing and content projects, we also offer one off services such as photography, videography, branding work and website builds. Whether it is a single project or a long term partnership, we tailor the scope to suit your needs."),
    ("Can you work alongside our existing team or agency?",
     "Absolutely. We often collaborate with internal teams, external marketing partners and business owners to support specific parts of a project. Whether it is content production, advertising or systems, we can integrate into existing workflows where needed."),
    ("Do you work with small businesses or only larger companies?",
     "We work with businesses at different stages of growth. Some clients are established organisations looking to scale their marketing, while others are smaller businesses building a strong foundation. What matters most is working with businesses that value quality and are serious about improving their brand and marketing."),
]

# ---------------------------------------------------------------- write

if __name__ == "__main__":
    written = []
    for fn, d in PAGES.items():
        body = "\n\n".join([
            hero(d["hero_base"], d["hero_alt"], d["label"], d["h1"], d["lede"], d.get("value_line")),
            prose(*d["intro"], statement=True),
            prose(*d["why"], dark=True),
            offer(d["offer_heading"], d["items"]),
            interlude(d["interlude_base"], d["interlude_alt"], d["quote"]),
            close_block(*d["close"]),
        ])
        open(os.path.join(ROOT, fn), "w").write(
            shell(d["title"], d["desc"], d["hero_base"], body, preload_base=d["hero_base"]))
        written.append(fn)

    # contact page
    faq_rows = "\n".join(
        f'      <details><summary>{q}</summary><p class="a">{a}</p></details>' for q, a in FAQS)
    contact_body = "\n\n".join([
        hero("hero-contact", "The guest studio at Stonehaven, 47 Somerset Drive.", "Contact",
             ["Let's connect."], "Tell us what you're building. We will tell you what it needs."),
        f"""<section class="dark">
  <div class="wrap">
    <h2 class="sr">Enquire</h2>
    <div class="split">
      <div class="reveal">
        <h3 class="fq" style="font-size:clamp(21px,2.4vw,30px);">Use the form, or call us. Either reaches the same three people.</h3>
        <dl class="direct">
          <dt>Phone</dt><dd><a href="tel:+61431516634">0431 516 634</a></dd>
          <dt>Email</dt><dd><a href="mailto:marketing@10xvisuals.com.au">marketing@10xvisuals.com.au</a></dd>
          <dt>Instagram</dt><dd><a href="https://www.instagram.com/10xvisuals_/" rel="noopener">@10xvisuals_</a></dd>
        </dl>
      </div>
      <div class="reveal">
{FORM}
      </div>
    </div>
  </div>
</section>""",
        f"""<section>
  <div class="wrap stagger">
    <h2 class="reveal h2m h-small"><span>Questions we often get.</span></h2>
    <div class="faq reveal stgr">
{faq_rows}
    </div>
  </div>
</section>""",
    ])
    open(os.path.join(ROOT, "contact-us.html"), "w").write(
        shell("Contact | 10x Visuals", "Talk to 10x Visuals about branding, content, lead generation or systems.",
              "hero-contact", contact_body, preload_base="hero-contact"))
    written.append("contact-us.html")

    for f in written:
        print(f"{f:20} {os.path.getsize(os.path.join(ROOT,f)):>7} bytes")
