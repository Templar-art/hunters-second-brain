#!/usr/bin/env python3
"""
MVX Electrical — Meta ad creative generator.

Rebuilds the existing MVX ad layout (square 1:1 and story 9:16) with new copy.
Layout, fonts and colours are unchanged from the creatives already running:
only the wording differs. Brand Guidelines v0.1 — League Gothic display,
Poppins for everything else, black dominant, green as accent only.

Re-runnable: edit SERVICES below and run again. No credits, no paid APIs.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path

BASE = Path(__file__).parent
OUT = BASE / "out"
OUT.mkdir(exist_ok=True)

# ── Brand ────────────────────────────────────────────────────────────────
GREEN = (126, 192, 4)        # #7EC004 primary green, accent only
GREEN_DK = (94, 133, 25)     # #5E8519 small use
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
INK = (26, 26, 26)

LEAGUE = str(BASE / "fonts/LeagueGothic.ttf")
POP = "/Library/Fonts/Poppins-Regular.ttf"
POP_SB = "/Library/Fonts/Poppins-SemiBold.ttf"
POP_BOLD = "/Library/Fonts/Poppins-Bold.ttf"

LOGO_BLACK = BASE.parent / "mvx-hot-water/assets/mvx-logo-black.png"
LOGO_WHITE = BASE.parent / "mvx-hot-water/assets/mvx-logo-white.png"


def f(path, size):
    return ImageFont.truetype(path, size)


# ── Content. Words only; layout is fixed. ────────────────────────────────
SERVICES = {
    "aircon": {
        "photo": "79233.jpg",
        "head_green": "AIRCON NOT COOLING?",
        "head_white": "WE FIND THE FAULT",
        "bullets": [
            "Not cooling properly",
            "Tripping the switchboard",
            "Leaking water inside",
            "Noisy or smelly unit",
            "New systems installed",
        ],
        "cta": ("GET YOUR FREE", "QUOTE"),
    },
    "general": {
        # Real MVX crew on a real site, per Brand Guidelines §06:
        # "crew in hi-vis, tools in hand, capability you can see", and
        # explicitly NOT cheesy stock electricians.
        "photo": "liversaver10.jpg",
        "head_green": "ELECTRICAL PROBLEMS",
        "head_white": "AT HOME?",
        "bullets": [
            "Power keeps tripping",
            "Flickering lights",
            "Dead power points",
            "Old switchboard",
            "Safety switch problems",
        ],
        "cta": ("GET IN TOUCH", "TODAY"),
    },
    "hotwater": {
        # ⚠️ STILL NOT A HOT WATER PHOTO. Nothing in MVX's library shows a
        # hot water system. Using real crew-at-a-panel instead of stock, which
        # at least matches the "we're the electricians" message and is on-brand.
        # Replace with an actual changeover shot as soon as Matt has one.
        "photo": "liversaver9.jpg",
        "head_green": "NO HOT WATER?",
        "head_white": "WE'RE THE ELECTRICIANS",
        "bullets": [
            "No hot water at all",
            "Only running lukewarm",
            "Tank leaking",
            "Tripping the switchboard",
            "Old systems replaced",
        ],
        "cta": ("GET YOUR FREE", "QUOTE"),
    },
}


# ── Helpers ──────────────────────────────────────────────────────────────
def cover(img, w, h):
    """Scale + centre-crop to exactly w×h."""
    ar_t, ar_i = w / h, img.width / img.height
    if ar_i > ar_t:
        nh = h
        nw = int(h * ar_i)
    else:
        nw = w
        nh = int(w / ar_i)
    img = img.resize((nw, nh), Image.LANCZOS)
    return img.crop(((nw - w) // 2, (nh - h) // 2, (nw - w) // 2 + w, (nh - h) // 2 + h))


def pill(d, xy, text, font, bg, fg, pad=(34, 18), r=100):
    """Rounded location pill with a map-pin glyph."""
    x, y = xy
    pin_w = 30
    tw = d.textlength(text, font=font)
    w = int(tw + pin_w + 12 + pad[0] * 2)
    h = int(font.size + pad[1] * 2)
    d.rounded_rectangle([x, y, x + w, y + h], radius=r, fill=bg)
    # map pin: circle + tail
    cx, cy = x + pad[0] + pin_w / 2, y + h / 2
    d.ellipse([cx - 11, cy - 14, cx + 11, cy + 8], fill=fg)
    d.polygon([(cx - 7, cy + 4), (cx + 7, cy + 4), (cx, cy + 17)], fill=fg)
    d.ellipse([cx - 4.5, cy - 8, cx + 4.5, cy + 1], fill=bg)
    d.text((x + pad[0] + pin_w + 12, y + h / 2), text, font=font, fill=fg, anchor="lm")
    return h


def tick(d, cx, cy, r, colour, weight=7):
    """Green ring + check, drawn not fonted so it scales cleanly."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=colour, width=weight)
    s = r * 0.52
    d.line([(cx - s * 0.95, cy + s * 0.05), (cx - s * 0.18, cy + s * 0.78)],
           fill=colour, width=weight + 1)
    d.line([(cx - s * 0.18, cy + s * 0.78), (cx + s * 1.0, cy - s * 0.82)],
           fill=colour, width=weight + 1)


def fit(text, font_path, max_w, start):
    """Largest size at or below `start` that fits max_w."""
    size = start
    while size > 20:
        fo = f(font_path, size)
        if fo.getbbox(text)[2] <= max_w:
            return fo
        size -= 2
    return f(font_path, 20)


def star(d, cx, cy, r, colour):
    """Five-pointed star as a polygon. Poppins has no star glyph."""
    import math
    pts = []
    for i in range(10):
        ang = math.radians(-90 + i * 36)
        rad = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    d.polygon(pts, fill=colour)


def badge_height(scale=1.0):
    """Total drawn height of the Google badge, so callers can lay it out."""
    return int(58 * scale) + int(66 * scale) + int(46 * scale) + int(24 * scale)


def google_badge(im, d, cx, y, scale=1.0):
    """4.9 stars + the Google review mark, same as the incumbent creatives.
    `y` is the TOP of the block; height is badge_height(scale)."""
    g_cols = [(66, 133, 244), (234, 67, 53), (251, 188, 5), (66, 133, 244),
              (52, 168, 83), (234, 67, 53)]
    gf = f(POP_BOLD, int(58 * scale))
    letters = list("Google")
    widths = [d.textlength(c, font=gf) for c in letters]
    x = cx - sum(widths) / 2
    for c, col, wd in zip(letters, g_cols, widths):
        d.text((x, y), c, font=gf, fill=col)
        x += wd
    # Stars are drawn as polygons: Poppins has no ★ glyph and renders tofu.
    sf = f(POP_SB, int(34 * scale))
    rating = "4.9 "
    rw = d.textlength(rating, font=sf)
    sr = 15 * scale                      # star radius
    step = sr * 2.25
    sw = step * 4 + sr * 2
    sx = cx - (rw + sw) / 2
    yy = y + int(66 * scale)
    d.text((sx, yy), rating, font=sf, fill=INK)
    scy = yy + sf.size * 0.58
    for i in range(5):
        star(d, sx + rw + sr + i * step, scy, sr, (251, 188, 5))
    rf = f(POP, int(22 * scale))
    d.text((cx, yy + int(46 * scale)), "REVIEWS", font=rf, fill=(120, 120, 120), anchor="ma")


def badge_width(d, scale=1.0):
    gf = f(POP_BOLD, int(58 * scale))
    return d.textlength("Google", font=gf)


def footer(im, d, W, bottom, cta, cta_max_w, scale=0.82, logo_h=80):
    """CTA line + logo/badge row, laid out from the bottom edge up so
    nothing ever clips off the canvas. Returns the top y of the block."""
    bh = badge_height(scale)
    lg = Image.open(LOGO_BLACK).convert("RGBA")
    logo_w = int(lg.width * (logo_h / lg.height))
    bw = badge_width(d, scale)
    gap_x = 70
    row_h = max(bh, logo_h)
    row_y = bottom - row_h
    total = logo_w + gap_x + bw
    lx = (W - total) / 2
    paste_logo(im, LOGO_BLACK, lx, row_y + (row_h - logo_h) / 2, logo_h)
    google_badge(im, d, lx + logo_w + gap_x + bw / 2, row_y + (row_h - bh) / 2, scale)

    a, b_ = cta
    cf = fit(f"{a} {b_}", LEAGUE, cta_max_w, 104)
    aw = d.textlength(a + " ", font=cf)
    bw2 = d.textlength(b_, font=cf)
    sx = (W - (aw + bw2)) / 2
    cy = row_y - 34 - cf.size
    d.text((sx, cy), a + " ", font=cf, fill=BLACK)
    d.text((sx + aw, cy), b_, font=cf, fill=GREEN)
    return cy


def paste_logo(im, path, x, y, h):
    lg = Image.open(path).convert("RGBA")
    w = int(lg.width * (h / lg.height))
    lg = lg.resize((w, h), Image.LANCZOS)
    im.paste(lg, (int(x), int(y)), lg)
    return w


# ── Square 1080×1080 ─────────────────────────────────────────────────────
def build_square(key, cfg):
    W = H = 1080
    photo_h = 742
    im = Image.new("RGB", (W, H), WHITE)

    ph = cover(Image.open(BASE / "photos" / cfg["photo"]).convert("RGB"), W, photo_h)
    # Dark scrim so white type survives the frame, per brand legibility rule
    scrim = Image.new("RGB", (W, photo_h), (38, 38, 38))
    ph = Image.blend(ph, scrim, 0.62)
    im.paste(ph, (0, 0))
    d = ImageDraw.Draw(im)

    M = 58
    pill(d, (M, 52), "Gold Coast", f(POP_SB, 34), WHITE, BLACK)

    # Headline, left column
    col_w = 545
    hl = fit(cfg["head_green"], LEAGUE, col_w, 118)
    words = cfg["head_white"].split()
    # break the white line into at most 2 lines that fit
    lines, cur = [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if f(LEAGUE, 118).getbbox(t)[2] <= col_w or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    lines.append(cur)
    hw = min([fit(l, LEAGUE, col_w, 118).size for l in lines])
    hwf = f(LEAGUE, hw)

    y = 272
    d.text((M, y), cfg["head_green"], font=hl, fill=GREEN)
    y += int(hl.size * 0.92)
    for l in lines:
        d.text((M, y), l, font=hwf, fill=WHITE)
        y += int(hwf.size * 0.92)

    # Checklist, right column
    bf = f(POP, 35)
    bx, r = 618, 31
    n = len(cfg["bullets"])
    gap = 124
    by = (photo_h - (n - 1) * gap) // 2
    for i, b in enumerate(cfg["bullets"]):
        cy = by + i * gap
        tick(d, bx + r, cy, r, GREEN, 7)
        tx = bx + r * 2 + 26
        if d.textlength(b, font=bf) > W - tx - 40:
            ws = b.split()
            mid = len(ws) // 2 + len(ws) % 2
            d.text((tx, cy - 24), " ".join(ws[:mid]), font=bf, fill=WHITE, anchor="lm")
            d.text((tx, cy + 24), " ".join(ws[mid:]), font=bf, fill=WHITE, anchor="lm")
        else:
            d.text((tx, cy), b, font=bf, fill=WHITE, anchor="lm")

    # Green rule, then the white CTA block (laid out from the bottom up)
    d.rectangle([0, photo_h, W, photo_h + 16], fill=GREEN)
    footer(im, d, W, H - 42, cfg["cta"], W - 130, scale=0.80, logo_h=78)

    p = OUT / f"mvx-{key}-1x1.png"
    im.save(p)
    return p


# ── Story 1080×1920 ──────────────────────────────────────────────────────
def build_story(key, cfg):
    W, H = 1080, 1920
    im = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(im)
    M = 62

    # Headline: green line then black line, pill sits to the right of line 1
    hg = fit(cfg["head_green"], LEAGUE, W - M * 2 - 300, 118)
    d.text((M, 150), cfg["head_green"], font=hg, fill=GREEN)
    pill(d, (M + hg.getbbox(cfg["head_green"])[2] + 40, 168), "Gold Coast",
         f(POP_SB, 32), BLACK, WHITE)
    hw = fit(cfg["head_white"], LEAGUE, W - M * 2, 118)
    d.text((M, 150 + int(hg.size * 0.94)), cfg["head_white"], font=hw, fill=BLACK)

    # 2x2 checklist (story drops the 5th bullet)
    bf = f(POP, 33)
    y0 = 150 + int(hg.size * 0.94) + int(hw.size * 0.94) + 60
    r = 27
    for i, b in enumerate(cfg["bullets"][:4]):
        cx = M + r + (i % 2) * 470
        cy = y0 + (i // 2) * 108
        tick(d, cx, cy, r, GREEN_DK, 6)
        tx = cx + r + 22
        if d.textlength(b, font=bf) > 400:
            ws = b.split()
            mid = len(ws) // 2 + len(ws) % 2
            d.text((tx, cy - 21), " ".join(ws[:mid]), font=bf, fill=INK, anchor="lm")
            d.text((tx, cy + 21), " ".join(ws[mid:]), font=bf, fill=INK, anchor="lm")
        else:
            d.text((tx, cy), b, font=bf, fill=INK, anchor="lm")

    # Photo block with the offset green slabs behind it
    py = y0 + 260
    pw, ph_ = W - M * 2 - 40, 640
    d.rectangle([0, py + 200, W, py + ph_ - 60], fill=GREEN)
    ph = cover(Image.open(BASE / "photos" / cfg["photo"]).convert("RGB"), pw, ph_)
    mask = Image.new("L", (pw, ph_), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, pw, ph_], radius=26, fill=255)
    im.paste(ph, (M + 20, py), mask)

    # CTA + logos on white
    # Base green slab, matching the incumbent story layout
    d.rectangle([0, H - 132, W, H], fill=GREEN)
    footer(im, d, W, H - 132 - 46, cfg["cta"], W - 150, scale=0.80, logo_h=74)

    p = OUT / f"mvx-{key}-9x16.png"
    im.save(p)
    return p


if __name__ == "__main__":
    for key, cfg in SERVICES.items():
        print(build_square(key, cfg))
        print(build_story(key, cfg))
