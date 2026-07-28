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
STARF = "/Library/Fonts/Arial Unicode.ttf"   # Poppins has no star glyph

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
        # Hot water stock supplied by Hunter, 28 Jul: a tech at a wall-mounted
        # unit. Landscape crop for the square, portrait for the story.
        "photo": "hotwater-wide.jpg",
        "photo_sq": "hotwater-wide.jpg",
        "photo_st": "hotwater-tall.jpg",
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
def cover(img, w, h, fx=0.5, fy=0.5):
    """Scale + crop to exactly w×h. fx/fy bias which part is kept (0=left/top,
    1=right/bottom). On the square, the subject is biased right so the big
    headline isn't sitting on top of somebody's face."""
    ar_t, ar_i = w / h, img.width / img.height
    if ar_i > ar_t:
        nh, nw = h, int(h * ar_i)
    else:
        nw, nh = w, int(w / ar_i)
    img = img.resize((nw, nh), Image.LANCZOS)
    x = int((nw - w) * fx)
    y = int((nh - h) * fy)
    return img.crop((x, y, x + w, y + h))


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
    return int(58 * scale) + int(84 * scale) + int(46 * scale) + int(24 * scale)


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
    # "4.9" + five gold stars on one baseline, as on the incumbent creatives.
    sf = f(POP_SB, int(34 * scale))
    stf = f(STARF, int(31 * scale))
    rating = "4.9 "
    stars = "\u2605" * 5
    rw = d.textlength(rating, font=sf)
    sw = d.textlength(stars, font=stf)
    sx = cx - (rw + sw) / 2
    yy = y + int(84 * scale)          # clear of the Google descenders
    base = yy + sf.size * 0.78              # shared baseline
    d.text((sx, base), rating, font=sf, fill=INK, anchor="ls")
    d.text((sx + rw, base), stars, font=stf, fill=(251, 188, 5), anchor="ls")
    rf = f(POP, int(22 * scale))
    d.text((cx, yy + int(46 * scale)), "REVIEWS", font=rf, fill=(120, 120, 120), anchor="ma")


def badge_width(d, scale=1.0):
    gf = f(POP_BOLD, int(58 * scale))
    return d.textlength("Google", font=gf)


def footer(im, d, W, bottom, cta, cta_max_w, scale=0.82, logo_h=80, cta_start=104, top_limit=None):
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
    cf = fit(f"{a} {b_}", LEAGUE, cta_max_w, cta_start)
    # Never let the CTA push above the block it lives in (it was crossing the
    # green rule and sitting over the photo).
    if top_limit is not None:
        avail = row_y - 26 - top_limit
        while cf.size > 40 and cf.size > avail:
            cf = f(LEAGUE, cf.size - 2)
    aw = d.textlength(a + " ", font=cf)
    bw2 = d.textlength(b_, font=cf)
    sx = (W - (aw + bw2)) / 2
    cy = row_y - 26 - cf.size
    d.text((sx, cy), a + " ", font=cf, fill=BLACK)
    d.text((sx + aw, cy), b_, font=cf, fill=GREEN)
    return cy


def shadow(im, box, radius=26, blur=20, alpha=105, offset=(0, 12)):
    """Soft drop shadow behind a rounded block. Used on the story format so the
    green bar running behind the photo reads as a separate layer."""
    lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    x0, y0, x1, y1 = box
    ImageDraw.Draw(lay).rounded_rectangle(
        [x0 + offset[0], y0 + offset[1], x1 + offset[0], y1 + offset[1]],
        radius=radius, fill=(0, 0, 0, alpha))
    lay = lay.filter(ImageFilter.GaussianBlur(blur))
    im.paste(Image.alpha_composite(im.convert("RGBA"), lay).convert("RGB"), (0, 0))


def paste_logo(im, path, x, y, h):
    lg = Image.open(path).convert("RGBA")
    w = int(lg.width * (h / lg.height))
    lg = lg.resize((w, h), Image.LANCZOS)
    im.paste(lg, (int(x), int(y)), lg)
    return w


# ── Square 1080×1080 ─────────────────────────────────────────────────────
def build_square(key, cfg):
    W = H = 1080
    photo_h = int(H * 0.723)   # green rule sits at ~72% in the original
    im = Image.new("RGB", (W, H), WHITE)

    ph = cover(Image.open(BASE / "photos" / cfg.get("photo_sq", cfg["photo"])).convert("RGB"),
               W, photo_h, fx=cfg.get("fx_sq", 0.5), fy=cfg.get("fy_sq", 0.5))
    # Dark scrim so white type survives the frame, per brand legibility rule
    scrim = Image.new("RGB", (W, photo_h), (38, 38, 38))
    ph = Image.blend(ph, scrim, 0.62)
    im.paste(ph, (0, 0))
    d = ImageDraw.Draw(im)

    M = 58
    pill(d, (M, 52), "Gold Coast", f(POP_SB, 34), WHITE, BLACK)

    # Headline, left column. BOTH the green and white lines wrap, and the whole
    # block is sized to FILL the column top to bottom. Sizing off the longest
    # single line left short headlines floating in void space.
    col_w = int(W * 0.505)
    top = int(H * 0.145)
    avail_h = int(photo_h * 0.94) - top
    LEAD = 0.885

    def wrap(text, font):
        out, cur = [], ""
        for w_ in text.split():
            t = (cur + " " + w_).strip()
            if font.getbbox(t)[2] <= col_w or not cur:
                cur = t
            else:
                out.append(cur); cur = w_
        out.append(cur)
        return out

    size, g_lines, w_lines = 40, [cfg["head_green"]], [cfg["head_white"]]
    for s_ in range(200, 40, -2):
        fo = f(LEAGUE, s_)
        gl, wl = wrap(cfg["head_green"], fo), wrap(cfg["head_white"], fo)
        widest = max(fo.getbbox(t)[2] for t in gl + wl)
        if widest <= col_w and (len(gl) + len(wl)) * s_ * LEAD <= avail_h:
            size, g_lines, w_lines = s_, gl, wl
            break
    hf = f(LEAGUE, size)

    y = top
    for l in g_lines:
        d.text((M, y), l, font=hf, fill=GREEN)
        y += int(hf.size * LEAD)
    for l in w_lines:
        d.text((M, y), l, font=hf, fill=WHITE)
        y += int(hf.size * LEAD)

    # Checklist, right column
    bf = f(POP, int(W * 0.0345))
    bx, r = int(W * 0.575), int(W * 0.029)
    n = len(cfg["bullets"])
    gap = int(H * 0.118)
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
    footer(im, d, W, H - 26, cfg["cta"], W - 110, scale=0.70, logo_h=72,
           cta_start=126, top_limit=photo_h + 16 + 14)

    p = OUT / f"mvx-{key}-1x1.png"
    im.save(p)
    return p


# ── Story 1080×1920 ──────────────────────────────────────────────────────
def build_story(key, cfg):
    """One photo sits behind the lower two thirds. The white CTA panel is drawn
    OVER it, so the photo shows above the panel and again below the green band.
    It is a single image, not two crops."""
    W, H = 1080, 1920
    im = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(im)
    M = 62

    # Headline: green line, then black line, pill inline with line 1
    hg = fit(cfg["head_green"], LEAGUE, W - M * 2 - 300, 118)
    d.text((M, 150), cfg["head_green"], font=hg, fill=GREEN)
    pill(d, (M + hg.getbbox(cfg["head_green"])[2] + 40, 168), "Gold Coast",
         f(POP_SB, 32), BLACK, WHITE)
    hw = fit(cfg["head_white"], LEAGUE, W - M * 2, 118)
    d.text((M, 150 + int(hg.size * 0.94)), cfg["head_white"], font=hw, fill=BLACK)

    # 2x2 checklist (story carries the first four bullets)
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

    # ONE photo, inset with rounded corners, running to the bottom of the frame
    py = y0 + 168
    pw = W - (M + 20) * 2
    ph_h = H - 26 - py
    ph = cover(Image.open(BASE / "photos" / cfg.get("photo_st", cfg["photo"])).convert("RGB"), pw, ph_h)
    mask = Image.new("L", (pw, ph_h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, pw, ph_h], radius=26, fill=255)

    # Green slabs bleed to the edges behind the photo
    d.rectangle([0, py + 200, W, py + 640], fill=GREEN)

    # Photo lifts off the green bar
    shadow(im, (M + 20, py, M + 20 + pw, py + ph_h), radius=26, blur=22, alpha=110)
    im.paste(ph, (M + 20, py), mask)
    d = ImageDraw.Draw(im)

    # White CTA panel drawn OVER the photo, lifted off it by its own shadow
    panel_top, panel_h, band_h = 1418, 300, 62
    shadow(im, (-40, panel_top, W + 40, panel_top + panel_h),
           radius=0, blur=24, alpha=115, offset=(0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([0, panel_top, W, panel_top + panel_h], fill=WHITE)
    d.rectangle([0, panel_top + panel_h, W, panel_top + panel_h + band_h], fill=GREEN)

    footer(im, d, W, panel_top + panel_h - 22, cfg["cta"], W - 150,
           scale=0.70, logo_h=70, cta_start=112, top_limit=panel_top + 18)

    p = OUT / f"mvx-{key}-9x16.png"
    im.save(p)
    return p


if __name__ == "__main__":
    for key, cfg in SERVICES.items():
        print(build_square(key, cfg))
        print(build_story(key, cfg))
