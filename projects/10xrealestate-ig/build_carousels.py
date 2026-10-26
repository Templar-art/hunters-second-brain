"""Seamless editorial carousels for @10xrealestate_ (v5).

Each carousel is composed on ONE long canvas (9 slides x 1080 wide) and then
sliced, so photos run across the swipe seams. Patterns from the reference set
Hunter liked: mixed-weight headline, one photo cut into staggered bands, tilted
prints cut by a seam, a film strip of details, a frame split ON the seam.
carousels.json lists 13 [index, label] photos, filling in order:
  0 cover, 1 bands, 2-3 tilted prints, 4-7 film strip, 8 seam split,
  9 inset, 10 full bleed, 11 top bleed, 12 closing inset
Run: python3 build_carousels.py
"""
import io, json, os
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


def load(path, size):
    im = ImageOps.exif_transpose(Image.open(path))
    im.draft("RGB", (size[0] * 2, size[1] * 2))
    return grade(ImageOps.fit(im.convert("RGB"), size, Image.LANCZOS, centering=(0.5, 0.5)))


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
    tracked(d, (x, y), f"{n:02d}", font("Medium", 20), BLUE + (255,), 3)
    d.text((x + 46, y), label, font=font("Light", 25), anchor="lm",
           fill=(255, 255, 255, 235) if light else INK + (235,))


def bands(canvas, path, box, offsets, gap=22):
    """One photo cut into horizontal bands, each nudged sideways."""
    x0, y0, x1, y1 = box
    im = load(path, (x1 - x0, y1 - y0))
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


def compose(listing, photos):
    p = [photos[i] for i, _ in listing["photos"]]
    lab = [l for _, l in listing["photos"]]
    c = Image.new("RGBA", (W * SLIDES, H), PAPER + (255,))
    d = ImageDraw.Draw(c)
    s = lambda n: W * (n - 1)  # left edge of slide n

    # 1 · cover, mixed-weight headline
    place(c, p[0], (0, 0, W, H))
    shade(c, (0, int(H * 0.40), W, H), 0, 215)
    d = ImageDraw.Draw(c)
    tracked(d, (M, H - 400), listing["kicker"], font("Medium", 22), (255, 255, 255, 225), 8)
    d.text((M - 6, H - 300), listing["street"], anchor="lm", fill="white",
           font=fit(d, listing["street"], "SemiBold", 168, W - 2 * M))
    d.text((M, H - 170), listing["suffix"], anchor="lm", fill="white", font=font("LightItalic", 96))
    d.line((M, H - 84, M + 40, H - 84), fill=BLUE, width=3)
    tracked(d, (M + 56, H - 84), listing["area"], font("Medium", 20), (255, 255, 255, 220), 7)

    # 2-3 · photo cut into staggered bands, running into slide 3
    bands(c, p[1], (s(2) + 120, 170, s(3) + 640, 170 + 960), (0, 70, -36))
    caption(d, (s(2) + 120, 1225), 1, lab[1])

    # 3-4 · two tilted prints, the first cut by the seam
    tilt(c, p[2], (s(4) - 10, 430), (640, 480), -4)
    tilt(c, p[3], (s(4) + 600, 905), (480, 600), 3)
    caption(d, (s(3) + 760, 760), 2, lab[2])
    caption(d, (s(4) + 120, 1225), 3, lab[3])

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

    # 9 · top bleed, bordered inset across its edge, address to sign off
    place(c, p[11], (s(9), 0, s(10), 720))
    place(c, p[12], (s(9) + 420, 600, s(10) - 70, 600 + 440), border=True)
    caption(d, (s(9) + M, 760), 11, lab[11])
    caption(d, (s(9) + 420, 1090), 12, lab[12])
    d.text((s(9) + M, H - M - 10), listing["address"], anchor="lm", fill=INK + (200,), font=font("Light", 25))
    return c


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
    strip = compose(listing, photos)
    for n in range(1, SLIDES + 1):
        sl = strip.crop((W * (n - 1), 0, W * n, H))
        chrome(sl, n)
        sl.convert("RGB").save(f"{out}/{n:02d}.jpg", quality=93)
    strip.convert("RGB").resize((W * SLIDES // 4, H // 4)).save(f"{out}/_strip.jpg", quality=85)


def photos_for(folder):
    fs = []
    for root, _, files in os.walk(f"{SRC}/{folder}"):
        fs += [os.path.join(root, f) for f in files if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    return sorted(fs)


if __name__ == "__main__":
    cfg = json.load(open(f"{HERE}/carousels.json"))
    for key, listing in cfg.items():
        build(key, listing, photos_for(listing["folder"]))
        print("built", key)
