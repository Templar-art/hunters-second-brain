"""Seamless editorial carousels for @10xrealestate_ (v5).

Each carousel is composed on ONE long canvas (9 slides x 1080 wide) and then
sliced, so photos run across the swipe seams. Patterns from the reference set
Hunter liked: mixed-weight headline, one photo cut into staggered bands, tilted
prints cut by a seam, a film strip of details, a frame split ON the seam.
carousels.json lists 12 [index, label] photos, filling in order:
  0 cover, 1 bands, 2-3 tilted prints, 4-7 film strip, 8 seam split,
  9 inset, 10 full bleed, 11 closing hero
Run: python3 build_carousels.py
"""
import io, json, os
import numpy as np
from scipy import ndimage
import cairosvg
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps, ImageStat

Image.MAX_IMAGE_PIXELS = None
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = "/Users/10xhunter/Documents/Posting for 10xRealestate/To Post"
LOGO = "/Users/10xhunter/Desktop/_Brand & Tools/10x-Visuals/Logos & Symbols/10xVisuals_10X Symbol Blue X.svg"
FONTS = "/Users/10xhunter/Library/Fonts/"
W, H, M = 1080, 1350, 64
SLIDES = 9
PAPER = (0xF6, 0xF4, 0xF0)
INK = (0x16, 0x1A, 0x1E)
BLUE = (0x61, 0xA8, 0xD8)
BORDER = 14


def font(weight, size):
    return ImageFont.truetype(f"{FONTS}Poppins-{weight}.ttf", size)


def tracked(draw, xy, text, fnt, fill, track, anchor="l"):
    widths = [draw.textlength(c, font=fnt) for c in text]
    total = sum(widths) + track * (len(text) - 1)
    x, y = xy
    if anchor == "r":
        x -= total
    for c, w in zip(text, widths):
        draw.text((x, y), c, font=fnt, fill=fill, anchor="lm")
        x += w + track


def mark(width, ten):
    """Original 10X symbol: blue X untouched, the '10' recoloured."""
    m = Image.open(io.BytesIO(cairosvg.svg2png(url=LOGO, output_width=width))).convert("RGBA")
    px = m.load()
    for y in range(m.height):
        for x in range(m.width):
            r, g, b, a = px[x, y]
            if a and r > 200 and g > 200 and b > 200:
                px[x, y] = ten + (a,)
    return m


MARK_WHITE = mark(118, (255, 255, 255))
MARK_INK = mark(118, INK)


def grade(im):
    im = ImageEnhance.Contrast(im).enhance(1.07)
    im = ImageEnhance.Color(im).enhance(1.05)
    r, g, b = im.split()
    r = r.point(lambda v: min(255, int(v * 1.02)))
    b = b.point(lambda v: int(v * 0.98))
    im = Image.merge("RGB", (r, g, b))
    vig = Image.new("L", im.size, 0)
    ImageDraw.Draw(vig).ellipse((-im.width * 0.25, -im.height * 0.25, im.width * 1.25, im.height * 1.25), fill=255)
    vig = vig.filter(ImageFilter.GaussianBlur(max(im.size) // 6))
    return Image.composite(im, ImageEnhance.Brightness(im).enhance(0.85), vig)


def load(path, size, centering=(0.5, 0.5)):
    im = ImageOps.exif_transpose(Image.open(path))
    im.draft("RGB", (size[0] * 2, size[1] * 2))
    return grade(ImageOps.fit(im.convert("RGB"), size, Image.LANCZOS, centering=centering))


def place(canvas, path, box, border=False):
    x0, y0, x1, y1 = box
    if border:
        ImageDraw.Draw(canvas).rectangle((x0 - BORDER, y0 - BORDER, x1 + BORDER - 1, y1 + BORDER - 1), fill=PAPER)
    canvas.paste(load(path, (x1 - x0, y1 - y0)), (x0, y0))


def shade(canvas, box, top_alpha, bottom_alpha):
    x0, y0, x1, y1 = box
    g = Image.new("L", (1, 256))
    for y in range(256):
        g.putpixel((0, y), int(top_alpha + (bottom_alpha - top_alpha) * (y / 255) ** 1.6))
    layer = Image.new("RGBA", (x1 - x0, y1 - y0), (0, 0, 0, 255))
    layer.putalpha(g.resize(layer.size))
    canvas.alpha_composite(layer, (x0, y0))


def caption(d, xy, n, label, light=False):
    """Small numbered caption: blue index, then the room in light type."""
    if not label:
        return
    x, y = xy
    tracked(d, (x, y), f"{n:02d}", font("Medium", 24), (255, 255, 255, 255) if light else BLUE + (255,), 3)
    d.text((x + 54, y), label, font=font("Regular", 30), anchor="lm",
           fill=(255, 255, 255, 235) if light else INK + (235,))


def bands(canvas, path, box, offsets, gap=22):
    """One photo cut into horizontal bands, each nudged sideways."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    im = load(path, (int(w * 1.2), int(h * 1.2)))  # zoom in and sit low: keeps the top band off bare ceiling
    im = im.crop(((im.width - w) // 2, im.height - h, (im.width + w) // 2, im.height))
    n = len(offsets)
    bh = (im.height - gap * (n - 1)) // n
    for k, dx in enumerate(offsets):
        top = k * (bh + gap)
        canvas.paste(im.crop((0, top, im.width, top + bh)), (x0 + dx, y0 + top))


def split(canvas, path, box, cut, drop, gap=24):
    """One photo cut vertically at x=cut, right half dropped by `drop`."""
    x0, y0, x1, y1 = box
    im = load(path, (x1 - x0, y1 - y0))
    c = cut - x0
    canvas.paste(im.crop((0, 0, c - gap // 2, im.height)), (x0, y0))
    canvas.paste(im.crop((c + gap // 2, 0, im.width, im.height)), (cut + gap // 2, y0 + drop))


def tilt(canvas, path, centre, size, angle):
    """Bordered print, slightly rotated, with a soft shadow."""
    w, h = size
    card = Image.new("RGBA", (w + 2 * BORDER, h + 2 * BORDER), PAPER + (255,))
    card.paste(load(path, size), (BORDER, BORDER))
    pad = 60
    sh = Image.new("RGBA", (card.width + 2 * pad, card.height + 2 * pad), (0, 0, 0, 0))
    sh.paste((0, 0, 0, 70), (pad + 6, pad + 14, pad + 6 + card.width, pad + 14 + card.height))
    sh = sh.filter(ImageFilter.GaussianBlur(22))
    sh.alpha_composite(card, (pad, pad))
    sh = sh.rotate(angle, resample=Image.BICUBIC, expand=True)
    canvas.alpha_composite(sh, (centre[0] - sh.width // 2, centre[1] - sh.height // 2))


def fit(d, text, weight, size, maxw):
    while d.textlength(text, font=font(weight, size)) > maxw:
        size -= 4
    return font(weight, size)


def sky_mask(im):
    """Sky pixels connected to the top edge, as a soft L mask."""
    a = np.asarray(im).astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    lab, _ = ndimage.label(((b > r + 12) & (b > 110)) | ((r + g + b) > 690))
    sky = np.isin(lab, list(set(np.unique(lab[0])) - {0}))
    roof = np.percentile([np.argmax(~sky[:, x]) for x in range(60, W - 60, 10)], 30)
    return Image.fromarray((sky * 255).astype("uint8")).filter(ImageFilter.GaussianBlur(1.2)), roof


def cover(c, path, listing):
    """Street name set huge. Where the photo has sky, the house stands in front of it."""
    if listing.get("cover_crop"):
        src = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
        l, t, r, b = listing["cover_crop"]
        src = src.crop((int(l * src.width), int(t * src.height), int(r * src.width), int(b * src.height)))
        im = grade(ImageOps.fit(src, (W, H), Image.LANCZOS))
    else:
        im = load(path, (W, H))
    c.paste(im, (0, 0))
    mask, roof = sky_mask(im)
    behind = roof > 300 and listing.get("cover_mode") != "front"  # front when the skyline is ragged (trees)
    if behind:  # deepen the sky so white type holds against it
        g = Image.linear_gradient("L").resize((W, H)).point(lambda v: int(150 * max(0, 1 - v / 255 * H / (roof + 120))))
        deep = ImageEnhance.Color(ImageEnhance.Brightness(im).enhance(0.78)).enhance(1.15)
        c.paste(Image.composite(deep, im, Image.fromarray(np.minimum(np.asarray(g), np.asarray(mask)))), (0, 0))
    d = ImageDraw.Draw(c)
    big = fit(d, listing["street"], "SemiBold", 300, W - 2 * 80)  # survives the 3:4 grid crop
    x0, y0, x1, y1 = d.textbbox((0, 0), listing["street"], font=big, anchor="ls")
    th = y1 - y0
    if behind:
        base = int(roof + th * 0.16)
    elif roof > 300:  # open sky but a ragged edge: set the name clear of it
        base = max(int(roof - 40), 240 + th)  # keep the kicker clear of the logo
    else:
        base = H - 330
    base = max(base, 170 + th)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(layer).text(((W - (x1 - x0)) // 2 - x0, base), listing["street"], font=big, fill="white", anchor="ls")
    shadow = layer.copy()
    shadow.putalpha(shadow.getchannel("A").point(lambda v: v * 0.5).filter(ImageFilter.GaussianBlur(16)))
    if behind:
        for l in (shadow, layer):
            l.putalpha(Image.fromarray(np.minimum(np.asarray(l.getchannel("A")), np.asarray(mask))))
    shade(c, (0, int(H * listing.get("cover_shade", 0.55)), W, H), 0, 200)  # deeper on busy interiors
    if not behind:
        shade(c, (0, int(H * 0.35), W, int(H * 0.55)), 0, 0)
    c.alpha_composite(shadow)
    c.alpha_composite(layer)
    d = ImageDraw.Draw(c)
    kx = (W - (x1 - x0)) // 2
    tracked(d, (kx + 4, base - th - 34), listing["kicker"], font("Medium", 26), (255, 255, 255, 235), 9)
    d.text((M, H - 190), listing["suffix"], anchor="lm", fill="white", font=font("LightItalic", 104))
    d.line((M, H - 96, M + 44, H - 96), fill=BLUE, width=3)
    tracked(d, (M + 60, H - 96), listing["area"], font("Medium", 24), (255, 255, 255, 230), 8)


def compose(listing, photos):
    p = [photos[i] for i, _ in listing["photos"]]
    lab = [l for _, l in listing["photos"]]
    c = Image.new("RGBA", (W * SLIDES, H), PAPER + (255,))
    d = ImageDraw.Draw(c)
    s = lambda n: W * (n - 1)  # left edge of slide n

    # 1 · cover
    cover(c, p[0], listing)
    d = ImageDraw.Draw(c)

    # 2-3 · photo cut into staggered bands, running into slide 3
    bands(c, p[1], (s(2) + 120, 170, s(3) + 640, 170 + 960), (0, 70, -36))
    caption(d, (s(2) + 120, 1225), 1, lab[1])

    # 3-4 · two tilted prints, the first cut by the seam
    tilt(c, p[2], (s(4) - 10, 800), (640, 480), -4)
    tilt(c, p[3], (s(4) + 600, 470), (480, 600), 3)
    caption(d, (s(3) + 740, 1120), 2, lab[2])
    caption(d, (s(4) + 370, 830), 3, lab[3])

    # 5 · place name, then a film strip of four details
    d.text((s(5) + M - 4, 330), listing["place"], anchor="lm", fill=INK,
           font=fit(d, listing["place"], "LightItalic", 150, W - 2 * M))
    d.line((s(5) + M, 450, s(5) + M + 40, 450), fill=BLUE, width=3)
    fw, fh, fg = 228, 400, 16
    fx = s(5) + (W - (4 * fw + 3 * fg)) // 2
    for k in range(4):
        x = fx + k * (fw + fg)
        place(c, p[4 + k], (x, 620, x + fw, 620 + fh))
        caption(d, (x, 1065), 4 + k, lab[4 + k])

    # 6-7 · one frame cut on the swipe seam, right half dropped; inset over it
    split(c, p[8], (s(6) + 140, 130, s(7) + 720, 130 + 960), s(7), 80)
    place(c, p[9], (s(7) + 560, 840, s(7) + 1010, 840 + 400), border=True)
    caption(d, (s(6) + 140, 1225), 8, lab[8])
    caption(d, (s(7) + 140, 1290), 9, lab[9])

    # 8 · full bleed
    place(c, p[10], (s(8), 0, s(9), H))
    shade(c, (s(8), H - 300, s(9), H), 0, 150)
    d = ImageDraw.Draw(c)
    caption(d, (s(8) + M, H - M - 10), 10, lab[10], light=True)

    # 9 · close on the hero, set below the chrome, address to sign off
    place(c, p[11], (s(9), 150, s(10), 1150))
    caption(d, (s(9) + M, 1205), 11, lab[11])
    d.text((s(9) + M, H - M - 10), listing["address"], anchor="lm", fill=INK + (225,), font=font("Regular", 30))
    return c


def compose_b(listing, photos):
    """Layout B 'Gallery': ink pages, left-set cover, seamless panorama, 2x2 grid,
    vertical place name, staggered columns across the seam, full-bleed close."""
    p = [photos[i] for i, _ in listing["photos"]]
    lab = [l for _, l in listing["photos"]]
    c = Image.new("RGBA", (W * SLIDES, H), INK + (255,))
    s = lambda n: W * (n - 1)

    # 1 · cover: full bleed, name set flush left low
    c.paste(load(p[0], (W, H)), (0, 0))
    shade(c, (0, int(H * 0.4), W, H), 0, 215)
    d = ImageDraw.Draw(c)
    big = fit(d, listing["street"], "SemiBold", 230, W - 2 * M - 20)
    top = d.textbbox((M - 6, H - 300), listing["street"], font=big, anchor="ls")[1]
    tracked(d, (M + 2, top - 40), listing["kicker"], font("Medium", 26), (255, 255, 255, 235), 9)
    d.text((M - 6, H - 300), listing["street"], anchor="ls", fill="white", font=big)
    d.text((M, H - 230), listing["suffix"], anchor="lm", fill="white", font=font("LightItalic", 96))
    d.line((M, H - 120, M + 44, H - 120), fill=BLUE, width=3)
    tracked(d, (M + 60, H - 120), listing["area"], font("Medium", 24), (255, 255, 255, 230), 8)

    # 2-3 · one panorama running straight across the seam
    place(c, p[1], (s(2) + M, 200, s(3) + W - M, 1130))
    caption(d, (s(2) + M, 1200), 1, lab[1], light=True)

    # 4 · 2x2 grid
    gw, gh, gg = 460, 500, 24
    gx, gy = s(4) + (W - 2 * gw - gg) // 2, 190
    for k in range(4):
        x, y = gx + (k % 2) * (gw + gg), gy + (k // 2) * (gh + gg + 50)
        place(c, p[2 + k], (x, y, x + gw, y + gh))
        caption(d, (x, y + gh + 26), 2 + k, lab[2 + k], light=True)

    # 5 · place name set vertically, tall photo beside it
    place(c, p[6], (s(5) + 360, 170, s(5) + W - M, 1180))
    caption(d, (s(5) + 360, 1240), 6, lab[6], light=True)
    pf = fit(d, listing["place"], "LightItalic", 170, 1000)
    tw = int(d.textlength(listing["place"], font=pf)) + 20
    t = Image.new("RGBA", (tw, 230), (0, 0, 0, 0))
    ImageDraw.Draw(t).text((0, 115), listing["place"], anchor="lm", fill="white", font=pf)
    t = t.rotate(90, expand=True)
    c.alpha_composite(t, (s(5) + 70, 1180 - t.height))
    d.line((s(5) + 120, 1240, s(5) + 160, 1240), fill=BLUE, width=3)

    # 6-7 · three tall columns, staggered, the middle one cut by the seam
    cols = [(s(6) + 110, 230), (s(6) + 690, 120), (s(7) + 420, 300)]
    for k, (x, y) in enumerate(cols):
        place(c, p[7 + k], (x, y, x + 520, y + 860))
        caption(d, (x, y + 900), 7 + k, lab[7 + k], light=True)

    # 8 · full bleed
    place(c, p[10], (s(8), 0, s(9), H))
    shade(c, (s(8), H - 300, s(9), H), 0, 150)
    d = ImageDraw.Draw(c)
    caption(d, (s(8) + M, H - M - 10), 10, lab[10], light=True)

    # 9 · hero full bleed, address over it
    place(c, p[11], (s(9), 0, s(10), H))
    shade(c, (s(9), H - 380, s(10), H), 0, 190)
    d = ImageDraw.Draw(c)
    caption(d, (s(9) + M, H - 150), 11, lab[11], light=True)
    d.text((s(9) + M, H - M - 10), listing["address"], anchor="lm", fill=(255, 255, 255, 235), font=font("Regular", 30))
    return c


def compose_c(listing, photos):
    """Layout C 'Magazine': paper cover with the name under the photo, overlapping
    collage, a frame across the seam, room index page, full bleed, framed hero."""
    p = [photos[i] for i, _ in listing["photos"]]
    lab = [l for _, l in listing["photos"]]
    c = Image.new("RGBA", (W * SLIDES, H), PAPER + (255,))
    d = ImageDraw.Draw(c)
    s = lambda n: W * (n - 1)

    # 1 · cover: photo on top, name in ink on the paper below
    place(c, p[0], (0, 0, W, 860))
    d = ImageDraw.Draw(c)
    tracked(d, (M + 2, 930), listing["kicker"], font("Medium", 24), INK + (220,), 9)
    big = fit(d, listing["street"], "SemiBold", 190, W - 2 * M - 300)
    d.text((M - 4, 1110), listing["street"], anchor="ls", fill=INK, font=big)
    sx = M + int(d.textlength(listing["street"], font=big)) + 22
    suf = font("LightItalic", 90)
    if sx + d.textlength(listing["suffix"], font=suf) > W - M:  # long suffix: drop it under the name
        d.text((M, 1205), listing["suffix"], anchor="ls", fill=INK, font=fit(d, listing["suffix"], "LightItalic", 90, W - 2 * M))
    else:
        d.text((sx, 1110), listing["suffix"], anchor="ls", fill=INK, font=suf)
    d.line((M, 1270, M + 44, 1270), fill=BLUE, width=3)
    tracked(d, (M + 60, 1270), listing["area"], font("Medium", 24), INK + (200,), 8)

    # 2-3 · collage: one wide frame, a small one, and a third cut by the seam
    place(c, p[1], (s(2) + M, 170, s(2) + W - M, 760))
    caption(d, (s(2) + M, 800), 1, lab[1])
    place(c, p[2], (s(2) + M, 870, s(2) + 560, 1250))
    caption(d, (s(2) + M, 1295), 2, lab[2])
    place(c, p[3], (s(2) + 720, 860, s(3) + 520, 1250), border=True)
    caption(d, (s(3) + 40, 1295), 3, lab[3])
    pf = fit(d, listing["place"], "LightItalic", 130, W - 2 * M - 40)
    d.text((s(3) + M, 330), listing["place"], anchor="lm", fill=INK, font=pf)
    d.line((s(3) + M, 440, s(3) + M + 40, 440), fill=BLUE, width=3)
    place(c, p[4], (s(3) + 580, 500, s(3) + W - M, 1160))
    caption(d, (s(3) + 580, 1205), 4, lab[4])

    # 4-5 · one big frame across the seam, bordered inset over its right side
    place(c, p[5], (s(4) + 220, 190, s(5) + 560, 1060))
    caption(d, (s(4) + 220, 1110), 5, lab[5])
    place(c, p[6], (s(5) + 600, 640, s(5) + W - M, 1200), border=True)
    caption(d, (s(5) + 600, 1260), 6, lab[6])

    # 6 · two tilted prints
    tilt(c, p[7], (s(6) + 420, 470), (600, 450), -3)
    tilt(c, p[8], (s(6) + 640, 950), (520, 420), 4)
    caption(d, (s(6) + M, 1250), 7, lab[7])
    caption(d, (s(6) + 420, 1250), 8, lab[8])

    # 7 · tall column + room index set in type
    place(c, p[9], (s(7), 0, s(7) + 520, H))
    d = ImageDraw.Draw(c)
    caption(d, (s(7) + 40, H - 60), 9, lab[9], light=True)
    y = 260
    for n, l in enumerate(lab[1:], 1):
        if not l:
            continue
        tracked(d, (s(7) + 600, y), f"{n:02d}", font("Medium", 24), BLUE + (255,), 3)
        d.text((s(7) + 660, y), l, anchor="lm", fill=INK + (235,), font=font("Light", 44))
        y += 78

    # 8 · full bleed
    place(c, p[10], (s(8), 0, s(9), H))
    shade(c, (s(8), H - 300, s(9), H), 0, 150)
    d = ImageDraw.Draw(c)
    caption(d, (s(8) + M, H - M - 10), 10, lab[10], light=True)

    # 9 · framed hero + address
    place(c, p[11], (s(9) + M, 170, s(10) - M, 1100))
    caption(d, (s(9) + M, 1160), 11, lab[11])
    d.text((s(9) + M, H - M - 10), listing["address"], anchor="lm", fill=INK + (225,), font=font("Regular", 30))
    return c


LAYOUTS = {"A": compose, "B": compose_b, "C": compose_c}


def chrome(slide, n):
    """Mark + index, inked dark on paper and white on photos."""
    box = (M, M - 8, M + MARK_WHITE.width, M - 8 + MARK_WHITE.height)
    light = ImageStat.Stat(slide.crop(box).convert("L")).mean[0] > 150
    if not light:
        shade(slide, (0, 0, W, 200), 60, 0)
    slide.alpha_composite(MARK_INK if light else MARK_WHITE, box[:2])
    d = ImageDraw.Draw(slide)
    ibox = (W - 200, M, W - M, M + 60)
    ilight = ImageStat.Stat(slide.crop(ibox).convert("L")).mean[0] > 150
    tracked(d, (W - M, M + MARK_WHITE.height // 2 - 8), f"{n:02d} / {SLIDES:02d}",
            font("Medium", 22), (INK + (230,)) if ilight else (255, 255, 255, 230), 4, "r")


def build(key, listing, photos):
    out = f"{HERE}/carousels/{key}"
    os.makedirs(out, exist_ok=True)
    for f in os.listdir(out):
        os.remove(f"{out}/{f}")
    strip = LAYOUTS[listing.get("layout", "A")](listing, photos)
    for n in range(1, SLIDES + 1):
        sl = strip.crop((W * (n - 1), 0, W * n, H))
        chrome(sl, n)
        sl.convert("RGB").save(f"{out}/{n:02d}.jpg", quality=93)
    strip.convert("RGB").resize((W * SLIDES // 4, H // 4)).save(f"{out}/_strip.jpg", quality=85)


def photos_for(listing):
    """Sorted photo paths. `folders` concatenates shoots in order (indices run on);
    `dir` + `match` reads straight from another folder, e.g. the website photo dump."""
    if listing.get("dir"):
        d = listing["dir"]
        return sorted(os.path.join(d, f) for f in os.listdir(d)
                      if listing.get("match", "") in f and f.lower().endswith((".jpg", ".jpeg", ".png"))
                      and not (listing.get("exclude") and listing["exclude"] in f))
    out = []
    for folder in listing.get("folders", [listing.get("folder")]):
        fs = []
        for root, _, files in os.walk(f"{SRC}/{folder}"):
            fs += [os.path.join(root, f) for f in files if f.lower().endswith((".jpg", ".jpeg", ".png"))]
        out += sorted(fs)
    return out


if __name__ == "__main__":
    import sys  # optional: build_carousels.py <config.json> <out dir>, e.g. the construction page
    if len(sys.argv) > 2:
        HERE = os.path.abspath(sys.argv[2])
    cfg = json.load(open(sys.argv[1] if len(sys.argv) > 1 else f"{HERE}/carousels.json"))
    for key, listing in cfg.items():
        build(key, listing, photos_for(listing))
        print("built", key)
