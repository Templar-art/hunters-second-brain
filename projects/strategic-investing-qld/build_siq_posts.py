#!/usr/bin/env /usr/bin/python3
"""
Strategic Investing QLD — social post generator.  "Quiet Equity" house system.
Deep ink navy + warm cream + burnished gold. Marcellus serif headlines (never caps,
gold keyword highlights) over Inter. PIL. Free (no paid ops).

Aligned to the established SIQ brand (see design-philosophy.md + the mortgage ad kit):
  navy #132A43 · gold #B7893B · cream #F3ECDE · thin gold rule · drawn home line-work.

Renders 9 posts (~20 slides) at 1080x1350 (4:5 IG portrait) to out/post-NN/.
Re-runnable. Templates: statement_cover · list_slide · numbered_step · why_support · tip_card
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

# ---------------------------------------------------------------- canvas / grid
W, H = 1080, 1350
MARGIN = 100
CW = W - 2 * MARGIN            # content width 880
HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "out")
FONTS = os.path.join(HERE, "fonts")

# ---------------------------------------------------------------- palette (Quiet Equity)
NAVY      = (19, 42, 67)        # #132A43 deep ink navy — holds typographic weight
NAVY_TOP  = (15, 34, 56)        # subtle darker top for gradient
NAVY_LINE = (38, 60, 86)        # #263C56 quiet connective lines
GOLD      = (183, 137, 59)      # #B7893B burnished gold — spent rarely
GOLD_SOFT = (201, 160, 90)      # #C9A05A
CREAM     = (243, 236, 222)     # #F3ECDE warm cream — the air everything breathes in
CREAM_DIM = (198, 185, 162)     # #C6B9A2 quieter cream for support text
SLATE     = (150, 165, 184)     # muted labels
CREAM_BG  = (241, 233, 218)     # inverse-tile paper
SLATE_NAVY= (74, 94, 118)       # muted navy for support text on cream
PHOTOS    = os.path.join(HERE, "photos")

# ---------------------------------------------------------------- fonts
MARCELLUS = os.path.join(FONTS, "Marcellus-Regular.ttf")
INTER_VAR = os.path.join(FONTS, "Inter-Variable.ttf")

def serif(size):
    return ImageFont.truetype(MARCELLUS, size)

def inter(size, weight="Regular"):
    f = ImageFont.truetype(INTER_VAR, size)
    try:
        f.set_variation_by_name(weight)
    except Exception:
        f.set_variation_by_name(weight.encode())
    return f

# ---------------------------------------------------------------- primitives
def new_canvas():
    img = Image.new("RGB", (W, H), NAVY)
    px = img.load()
    for y in range(H):
        t = y / H
        r = int(NAVY_TOP[0] + (NAVY[0] - NAVY_TOP[0]) * t)
        g = int(NAVY_TOP[1] + (NAVY[1] - NAVY_TOP[1]) * t)
        b = int(NAVY_TOP[2] + (NAVY[2] - NAVY_TOP[2]) * t)
        for x in range(W):
            px[x, y] = (r, g, b)
    return img

def measure(draw, text, font):
    b = draw.textbbox((0, 0), text, font=font)
    return b[2] - b[0], b[3] - b[1]

def tracked(draw, xy, text, font, fill, tracking=0, anchor="la"):
    widths = [measure(draw, ch, font)[0] for ch in text]
    total = sum(widths) + tracking * (len(text) - 1) if text else 0
    x, y = xy
    if anchor.startswith("m"):
        x -= total / 2
    for ch, wch in zip(text, widths):
        draw.text((x, y), ch, font=font, fill=fill)
        x += wch + tracking
    return total

def gold_bar(draw, y, w=64, x=None, center=True, thick=3):
    """Thin burnished-gold rule — the ad's divider motif, subtly graduated."""
    if x is None:
        x = (W - w) / 2 if center else MARGIN
    steps = max(int(w), 1)
    for i in range(steps):
        t = i / steps
        col = tuple(int(GOLD[j] + (GOLD_SOFT[j] - GOLD[j]) * t) for j in range(3))
        draw.rectangle([x + i, y, x + i + 1, y + thick], fill=col)

# ---- word-level headline wrapping with gold keyword highlights (Marcellus) ----
def _norm(word):
    return word.strip(".,?!:;’'\"()").lower()

def headline(draw, text, font, top, max_w, base=CREAM, gold_words=None,
             center=True, leading=1.14):
    gold_words = {_norm(w) for w in (gold_words or [])}
    words = text.split()
    space = measure(draw, " ", font)[0]
    # greedy wrap into lines of words
    lines, cur, curw = [], [], 0
    for wd in words:
        ww = measure(draw, wd, font)[0]
        add = ww + (space if cur else 0)
        if curw + add <= max_w or not cur:
            cur.append(wd); curw += add
        else:
            lines.append(cur); cur = [wd]; curw = ww
    if cur:
        lines.append(cur)
    lh = int(font.size * leading)
    y = top
    for line in lines:
        lw = sum(measure(draw, w, font)[0] for w in line) + space * (len(line) - 1)
        x = (W - lw) / 2 if center else MARGIN
        for wd in line:
            col = GOLD if _norm(wd) in gold_words else base
            draw.text((x, y), wd, font=font, fill=col)
            x += measure(draw, wd, font)[0] + space
        y += lh
    return y

def count_lines(draw, text, font, max_w):
    words, cur, curw, n = text.split(), [], 0, 0
    space = measure(draw, " ", font)[0]
    for wd in words:
        ww = measure(draw, wd, font)[0]; add = ww + (space if cur else 0)
        if curw + add <= max_w or not cur:
            cur.append(wd); curw += add
        else:
            n += 1; cur = [wd]; curw = ww
    return n + (1 if cur else 0)

def block(draw, text, font, fill, top, max_w, center=True, leading=1.3):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if measure(draw, trial, font)[0] <= max_w:
            cur = trial
        else:
            lines.append(cur); cur = wd
    if cur:
        lines.append(cur)
    lh = int(font.size * leading)
    y = top
    for ln in lines:
        w, _ = measure(draw, ln, font)
        x = (W - w) / 2 if center else MARGIN
        draw.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y

# ---------------------------------------------------------------- house line-work motif
def houses(img, alpha=18, color=GOLD):
    """Faint bottom-anchored pitched-roof homes in fine line-work."""
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    base = H - 150
    g = (*color, alpha)
    plots = [(70, 150, 150, 70), (250, 130, 120, 60), (430, 175, 175, 82),
             (650, 140, 135, 66), (840, 165, 160, 76)]
    for x, w, wh, rh in plots:
        top = base - wh
        d.rectangle([x, top, x + w, base], outline=g, width=2)
        d.line([x - 12, top, x + w / 2, top - rh], fill=g, width=2)
        d.line([x + w / 2, top - rh, x + w + 12, top], fill=g, width=2)
        dw, dh = w * 0.24, wh * 0.45
        dx = x + (w - dw) / 2
        d.rectangle([dx, base - dh, dx + dw, base], outline=g, width=2)
    img.paste(Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB"), (0, 0))

def ghost_serif(img, ch="SI", alpha=12):
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    d.text((W / 2, H / 2 - 30), ch, font=serif(560), fill=(*GOLD, alpha), anchor="mm")
    img.paste(Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB"), (0, 0))

# ---------------------------------------------------------------- shared furniture
def brand_mark(draw, y=H - 108, on_light=False):
    gold_bar(draw, y, w=52, thick=2)
    f = inter(19, "Medium")
    left, mid, right = "STRATEGIC INVESTING", "   ·   ", "QLD"
    tr = 3
    tw = lambda s: sum(measure(draw, ch, f)[0] for ch in s) + tr * (len(s) - 1)
    total = tw(left) + tw(mid) + tw(right)
    x = (W - total) / 2
    yy = y + 22
    main = NAVY if on_light else CREAM
    dim = SLATE_NAVY if on_light else SLATE
    x += tracked(draw, (x, yy), left, f, main, tr)
    x += tracked(draw, (x, yy), mid, f, dim, tr)
    tracked(draw, (x, yy), right, f, GOLD, tr)

# ---------------------------------------------------------------- photo helpers
def load_photo(name):
    return Image.open(os.path.join(PHOTOS, name)).convert("RGB")

def fit_cover(img, w, h):
    """Resize + centre-crop to fill (w, h)."""
    iw, ih = img.size
    scale = max(w / iw, h / ih)
    nw, nh = int(iw * scale + 0.5), int(ih * scale + 0.5)
    img = img.resize((nw, nh), Image.LANCZOS)
    x, y = (nw - w) // 2, (nh - h) // 2
    return img.crop((x, y, x + w, y + h))

def grade(img):
    """Unify stock to the house look: gentle contrast + slight desaturate + warm
    tint + a faint navy wash so every photo shares one temperature."""
    img = ImageEnhance.Contrast(img).enhance(1.07)
    img = ImageEnhance.Color(img).enhance(0.90)
    warm = Image.new("RGB", img.size, (196, 150, 84))
    img = Image.blend(img, Image.composite(warm, img, Image.new("L", img.size, 22)), 1.0)
    navy = Image.new("RGB", img.size, NAVY)
    img = Image.composite(navy, img, Image.new("L", img.size, 20))
    return img

def vscrim(size, color=NAVY, top=0, bottom=235, start=0.42):
    """Vertical gradient scrim, transparent up top → opaque color at the base."""
    w, h = size
    ov = Image.new("RGBA", size, (0, 0, 0, 0))
    px = ov.load()
    s = int(h * start)
    for yy in range(s, h):
        t = (yy - s) / max(h - s, 1)
        a = int(top + (bottom - top) * (t ** 1.4))
        for xx in range(w):
            px[xx, yy] = (*color, a)
    return ov

def slide_badge(draw, pos, total):
    """Carousel position, e.g. 02/04. Only shown on multi-slide carousels."""
    tracked(draw, (W - MARGIN - 58, MARGIN - 4), f"{pos:02d}", inter(21, "SemiBold"), GOLD, 2)
    draw.text((W - MARGIN - 26, MARGIN - 4), f"/{total:02d}", font=inter(21, "Light"), fill=SLATE)

def dots(draw, active, count, y=H - 168):
    r, gap = 5, 26
    x0 = (W - (count - 1) * gap) / 2
    for i in range(count):
        cx = x0 + i * gap
        if i == active:
            draw.ellipse([cx - r, y - r, cx + r, y + r], fill=GOLD)
        else:
            draw.ellipse([cx - r, y - r, cx + r, y + r], outline=SLATE, width=2)

def kicker(draw, text, y=MARGIN + 26):
    tracked(draw, (W / 2, y), text.upper(), inter(23, "SemiBold"), GOLD, 6, anchor="ma")
    gold_bar(draw, y + 44, w=42, thick=2)

# ---------------------------------------------------------------- templates
def statement_cover(kick, head, sub=None, gold_words=None, contact=None,
                    idx=None, n=9, motif="houses"):
    img = new_canvas()
    if motif == "houses":
        houses(img, 20)
    elif motif == "monogram":
        ghost_serif(img, "SI", 11)
    d = ImageDraw.Draw(img)
    kicker(d, kick)
    hf = serif(92)
    n_lines = count_lines(d, head, hf, CW)
    top = (H - n_lines * int(hf.size * 1.14)) / 2 - 80
    y = headline(d, head, hf, top, CW, base=CREAM, gold_words=gold_words)
    if sub:
        gold_bar(d, y + 34, w=66, thick=3)
        y = block(d, sub, inter(33, "Light"), CREAM_DIM, y + 74, CW - 80)
    if contact:
        cy = H - 214
        for line in contact:
            tracked(d, (W / 2, cy), line, inter(24, "Medium"), GOLD_SOFT, 2, anchor="ma")
            cy += 42
    brand_mark(d)
    return img

def list_slide(kick, head, items=None, gold_words=None, sub=None,
               active=None, count=None):
    img = new_canvas()
    houses(img, 14)
    d = ImageDraw.Draw(img)
    if active is not None:
        slide_badge(d, active + 1, count)
    kicker(d, kick)
    hf = serif(72)
    # measure the content group so it can be vertically centred (kills dead space)
    lh_sub = int(31 * 1.3)
    gh = count_lines(d, head, hf, CW) * int(hf.size * 1.12)
    if sub:
        gh += 22 + count_lines(d, sub, inter(31, "Light"), CW - 60) * lh_sub
    if items:
        gh += 74 + len(items) * 88 - 22
    top = max(MARGIN + 150, (H - 150 - gh) // 2)
    y = headline(d, head, hf, top, CW, base=CREAM, gold_words=gold_words)
    if sub:
        y = block(d, sub, inter(31, "Light"), SLATE, y + 22, CW - 60)
    if items:
        y += 74
        rf = inter(37, "Regular")
        for it in items:
            gold_bar(d, y + 22, w=24, x=MARGIN + 30, center=False, thick=3)
            d.text((MARGIN + 84, y), it, font=rf, fill=CREAM)
            y += 88
    if active is not None:
        dots(d, active, count)
    brand_mark(d)
    return img

def numbered_step(kick, num, head, sub=None, active=None, count=None):
    img = new_canvas()
    houses(img, 14)
    d = ImageDraw.Draw(img)
    if active is not None:
        slide_badge(d, active + 1, count)
    kicker(d, kick)
    nf, hf = serif(300), serif(58)
    num_h = 214          # visual height of the numeral
    gh = num_h + 58 + count_lines(d, head, hf, CW) * int(hf.size * 1.12)
    if sub:
        gh += 26 + count_lines(d, sub, inter(31, "Light"), CW - 60) * int(31 * 1.3)
    top = max(MARGIN + 150, (H - 150 - gh) // 2)
    d.text((W / 2, top + num_h / 2), num, font=nf, fill=GOLD, anchor="mm")
    gold_bar(d, top + num_h + 24, w=58, thick=3)
    y = headline(d, head, hf, top + num_h + 58, CW, base=CREAM)
    if sub:
        block(d, sub, inter(31, "Light"), SLATE, y + 26, CW - 60)
    if active is not None:
        dots(d, active, count)
    brand_mark(d)
    return img

def why_support(kick, head, points, gold_words=None, idx=None):
    img = new_canvas()
    houses(img, 16)
    d = ImageDraw.Draw(img)
    kicker(d, kick)
    y = headline(d, head, serif(70), MARGIN + 156, CW, base=CREAM, gold_words=gold_words)
    y += 92
    for i, (t, sub) in enumerate(points):
        tracked(d, (MARGIN + 28, y + 8), f"0{i+1}", serif(40), GOLD, 1)
        d.text((MARGIN + 122, y - 6), t, font=serif(44), fill=CREAM)
        if sub:
            d.text((MARGIN + 124, y + 52), sub, font=inter(27, "Light"), fill=CREAM_DIM)
        y += 152
        if i < len(points) - 1:
            d.line([MARGIN + 122, y - 42, W - MARGIN - 20, y - 42], fill=NAVY_LINE, width=2)
    brand_mark(d)
    return img

def tip_card(label, statement, gold_words=None, idx=None):
    img = new_canvas()
    ghost_serif(img, "SI", 9)
    d = ImageDraw.Draw(img)
    lf = inter(25, "SemiBold")
    lw = sum(measure(d, ch, lf)[0] for ch in label) + 4 * (len(label) - 1) + 84
    lx = (W - lw) / 2
    ly = MARGIN + 44
    d.rounded_rectangle([lx, ly, lx + lw, ly + 62], radius=31, outline=GOLD, width=2)
    tracked(d, (W / 2, ly + 17), label, lf, GOLD, 4, anchor="ma")
    hf = serif(82)
    words = statement.split()
    space = measure(d, " ", hf)[0]
    lines, cur, curw = [], [], 0
    for wd in words:
        ww = measure(d, wd, hf)[0]; add = ww + (space if cur else 0)
        if curw + add <= CW or not cur:
            cur.append(wd); curw += add
        else:
            lines.append(cur); cur = [wd]; curw = ww
    if cur:
        lines.append(cur)
    lh = int(hf.size * 1.16)
    top = (H - lh * len(lines)) / 2 - 30
    y = headline(d, statement, hf, top, CW, base=CREAM, gold_words=gold_words)
    gold_bar(d, y + 24, w=66, thick=3)
    brand_mark(d)
    return img

def photo_band(photo_name, kick, head, sub=None, gold_words=None, img_h=742):
    """Image top, thin gold rule, navy band with serif headline (the ad look)."""
    img = new_canvas()
    photo = grade(fit_cover(load_photo(photo_name), W, img_h))
    img.paste(photo, (0, 0))
    d = ImageDraw.Draw(img)
    gold_bar(d, img_h - 2, w=W, x=0, thick=5)
    ky = img_h + 54
    tracked(d, (W / 2, ky), kick.upper(), inter(23, "SemiBold"), GOLD, 6, anchor="ma")
    gold_bar(d, ky + 44, w=42, thick=2)
    y = headline(d, head, serif(60), ky + 96, CW, base=CREAM, gold_words=gold_words)
    if sub:
        block(d, sub, inter(29, "Light"), CREAM_DIM, y + 20, CW - 80)
    brand_mark(d)
    return img

def photo_full(photo_name, kick, head, sub=None, gold_words=None):
    """Full-bleed graded photo, navy scrim from the base, serif line low."""
    img = grade(fit_cover(load_photo(photo_name), W, H))
    img = Image.alpha_composite(img.convert("RGBA"),
                                vscrim((W, H), start=0.30, bottom=246)).convert("RGB")
    d = ImageDraw.Draw(img)
    n = count_lines(d, head, serif(72), CW)
    head_top = H - 250 - n * int(serif(72).size * 1.14)
    tracked(d, (W / 2, head_top - 66), kick.upper(), inter(22, "SemiBold"), GOLD_SOFT, 6, anchor="ma")
    gold_bar(d, head_top - 24, w=42, thick=2)
    y = headline(d, head, serif(72), head_top, CW, base=CREAM, gold_words=gold_words)
    if sub:
        block(d, sub, inter(29, "Light"), CREAM_DIM, y + 18, CW - 80)
    brand_mark(d)
    return img

def cream_quote(quote, kick, gold_words=None):
    """Warm-cream inverse tile — navy serif quote. Flips the grid rhythm."""
    img = Image.new("RGB", (W, H), CREAM_BG)
    houses(img, alpha=13, color=NAVY)
    d = ImageDraw.Draw(img)
    tracked(d, (W / 2, MARGIN + 26), kick.upper(), inter(23, "SemiBold"), GOLD, 6, anchor="ma")
    gold_bar(d, MARGIN + 70, w=42, thick=2)
    hf = serif(74)
    n = count_lines(d, quote, hf, CW)
    top = (H - n * int(hf.size * 1.18)) / 2 + 24
    d.text((W / 2, top - 92), "“", font=serif(150), fill=GOLD, anchor="mm")
    y = headline(d, quote, hf, top, CW, base=NAVY, gold_words=gold_words, leading=1.18)
    gold_bar(d, y + 26, w=66, thick=3)
    brand_mark(d, on_light=True)
    return img

def monogram_tile():
    """Brand stamp — a clean grid anchor."""
    img = new_canvas()
    houses(img, 12)
    d = ImageDraw.Draw(img)
    d.text((W / 2, H / 2 - 70), "SI", font=serif(360), fill=GOLD, anchor="mm")
    gold_bar(d, H / 2 + 120, w=70, thick=3)
    tracked(d, (W / 2, H / 2 + 168), "STRATEGIC INVESTING QLD",
            inter(26, "Medium"), CREAM, 5, anchor="ma")
    tracked(d, (W / 2, H / 2 + 214), "QLD PROPERTY INVESTING, MADE CLEARER",
            inter(17, "Regular"), SLATE, 3, anchor="ma")
    return img

# ---------------------------------------------------------------- render helpers
def save(img, post, slide=1, single=False):
    d = os.path.join(OUT, f"post-{post:02d}")
    os.makedirs(d, exist_ok=True)
    name = f"post-{post:02d}.png" if single else f"post-{post:02d}-{slide:02d}.png"
    img.save(os.path.join(d, name), "PNG")
    print("  ->", os.path.relpath(os.path.join(d, name), HERE))

# ---------------------------------------------------------------- build all
def build():
    os.makedirs(OUT, exist_ok=True)

    print("Post 1 — Welcome")
    save(statement_cover("Strategic Investing · QLD",
                         "Welcome to Strategic Investing QLD",
                         "QLD property investing made clearer.",
                         gold_words=["QLD"], motif="houses"), 1, single=True)

    print("Post 2 — Who this is for")
    save(list_slide("Who this is for", "Is this you?",
                    gold_words=["you?"], active=0, count=4,
                    sub="Investors at every stage. This page is built for you."), 2, 1)
    save(numbered_step("Stage 01", "01", "Just starting out",
                       "No investment property yet.", active=1, count=4), 2, 2)
    save(numbered_step("Stage 02", "02", "Already own 1 to 3",
                       "Building an investment portfolio.", active=2, count=4), 2, 3)
    save(numbered_step("Stage 03", "03", "Experienced investor",
                       "Four or more properties.", active=3, count=4), 2, 4)

    print("Post 3 — Why QLD")
    save(why_support("Why Queensland", "Why investors keep looking at QLD",
                     [("Diverse markets", "Different regions, different opportunities."),
                      ("Long-term demand drivers", "Population, infrastructure and lifestyle."),
                      ("Range of strategies", "Growth, cashflow or a balance of both.")],
                     gold_words=["QLD"]), 3, single=True)

    print("Post 4 — Common mistakes")
    save(list_slide("Educational", "Five common property investing mistakes",
                    gold_words=["five"], active=0, count=6,
                    sub="Most of them happen before you even buy."), 4, 1)
    mistakes = [
        ("01", "Buying on hype instead of a plan"),
        ("02", "Ignoring buffers and cashflow pressure"),
        ("03", "A property that doesn’t match the goal"),
        ("04", "Having no hold or exit strategy"),
        ("05", "Copying someone else’s strategy blindly"),
    ]
    for i, (num, txt) in enumerate(mistakes):
        save(numbered_step("Mistake", num, txt, active=i + 1, count=6), 4, i + 2)

    print("Post 5 — Case study")
    save(list_slide("Case study", "From uncertainty to a clearer plan",
                    gold_words=["clearer"], active=0, count=4,
                    sub="Sometimes clarity is the whole strategy."), 5, 1)
    save(numbered_step("Starting point", "01", "Unsure whether to invest",
                       "Worried about risk and the next move.", active=1, count=4), 5, 2)
    save(numbered_step("The process", "02", "A strategy conversation",
                       "Goals, current position and options reviewed.", active=2, count=4), 5, 3)
    save(numbered_step("Outcome", "03", "Clearer next steps",
                       "A realistic plan and more confidence.", active=3, count=4), 5, 4)

    print("Post 6 — Strategy chat")
    save(list_slide("What to expect", "What happens in a strategy chat?",
                    items=["Review your current position",
                           "Clarify your goals and timeline",
                           "Talk through possible options",
                           "Outline practical next steps"],
                    gold_words=["chat?"]), 6, single=True)

    print("Post 7 — The right team")
    save(list_slide("Support", "You don’t have to figure it out alone",
                    items=["Strategy", "Finance", "Tax", "Property professionals"],
                    gold_words=["alone"]), 7, single=True)

    print("Post 8 — Strategy tip")
    save(tip_card("STRATEGY TIP 01",
                  "Decide your outcome before you pick the suburb.",
                  gold_words=["outcome"]), 8, single=True)

    print("Post 9 — What a strategy balances")
    save(why_support("Strategy basics", "What a good strategy balances",
                     [("Your goal", "Growth, cashflow or a mix of both."),
                      ("Your cashflow", "What you can comfortably hold."),
                      ("Your timeline", "How long you plan to stay invested."),
                      ("Your risk comfort", "How much movement you can sit with.")],
                     gold_words=["balances"]), 9, single=True)

    # ---- Filler posts (variety for the grid) -------------------------------
    print("Post 10 — Photo band (home)")
    save(photo_band("home.jpg", "QLD property",
                    "Build a portfolio that fits your life",
                    "Strategy first. Property second.",
                    gold_words=["life"]), 10, single=True)

    print("Post 11 — Photo full (good questions)")
    save(photo_full("coffee-chat.jpg", "Where it starts",
                    "Good strategy starts with good questions",
                    "Where are you now, where do you want to be, and what’s the plan in between.",
                    gold_words=["questions"]), 11, single=True)

    print("Post 12 — Photo band (suburb aerial)")
    save(photo_band("suburb-aerial.jpg", "Queensland",
                    "Different suburbs, different strategies",
                    "The right area depends on your goal, not the hype.",
                    gold_words=["strategies"]), 12, single=True)

    print("Post 13 — Cream quote")
    save(cream_quote("Start with the outcome, not the address.",
                     "On strategy", gold_words=["outcome,"]), 13, single=True)

    print("Post 14 — Cream quote")
    save(cream_quote("Clarity is the whole strategy.",
                     "Principle", gold_words=["Clarity"]), 14, single=True)

    print("Post 15 — Monogram tile")
    save(monogram_tile(), 15, single=True)

    print("Post 16 — Strategy Tip 02")
    save(tip_card("STRATEGY TIP 02",
                  "Buy for the strategy, not the postcode.",
                  gold_words=["strategy,"]), 16, single=True)

    print("Post 17 — Strategy Tip 03")
    save(tip_card("STRATEGY TIP 03",
                  "Cashflow keeps you in the game. Plan for it.",
                  gold_words=["Cashflow"]), 17, single=True)

    # ---- Informative expansion -------------------------------------------
    print("Post 18 — Growth vs cashflow")
    save(why_support("Property basics", "Growth vs cashflow",
                     [("Growth", "Your property’s value rising over time."),
                      ("Cashflow", "Rent measured against your costs today."),
                      ("Most plans blend both", "The mix follows your goal.")],
                     gold_words=["cashflow"]), 18, single=True)

    print("Post 19 — What is equity")
    save(list_slide("Property basics", "What is equity?",
                    sub="The part of your property you actually own. Its value, minus what you still owe.",
                    items=["It grows as you pay down the loan",
                           "It grows if the property rises in value",
                           "Investors use it to fund the next move"],
                    gold_words=["equity?"]), 19, single=True)

    print("Post 20 — Rentvesting")
    save(list_slide("Strategy", "Rentvesting, simply",
                    sub="Rent where you want to live. Invest where the numbers work.",
                    items=["Live near work, lifestyle or family",
                           "Buy where growth or yield stacks up",
                           "Keep your flexibility while you build"],
                    gold_words=["Rentvesting,"]), 20, single=True)

    print("Post 21 — Photo band (know your numbers)")
    save(photo_band("planning.jpg", "Property basics",
                    "Know your numbers first",
                    "Borrowing power, your buffer, and a target yield, before you fall for a listing.",
                    gold_words=["numbers"]), 21, single=True)

    print("Post 22 — Cream quote")
    save(cream_quote("Time in the market beats timing the market.",
                     "Principle", gold_words=["Time"]), 22, single=True)

    print("Post 23 — Cream quote")
    save(cream_quote("You make much of your return the day you buy well.",
                     "Principle", gold_words=["buy"]), 23, single=True)

    print("\nDone. All slides in", os.path.relpath(OUT, HERE))

if __name__ == "__main__":
    build()
