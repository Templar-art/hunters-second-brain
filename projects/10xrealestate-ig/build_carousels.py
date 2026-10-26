"""Seamless editorial carousels for @10xrealestate_ (v4).

Each carousel is composed on ONE long canvas (9 slides x 1080 wide) and then
sliced, so photos can run across the swipe seams: a two-slide panorama, frames
that overlap and get cut by the seam, tall bleeds, inset details.
Photo order in carousels.json fills slots A..J:
  A cover · B panorama · C tall bleed · D overlap across seam · E tall bleed right
  F frame straddling seam · G inset detail · H full bleed · I top bleed · J overlap inset
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


def compose(listing, photos):
    p = [photos[i] for i in listing["photos"]]
    c = Image.new("RGB", (W * SLIDES, H), PAPER)
    s = lambda n: W * (n - 1)  # left edge of slide n

    # 1 · cover
    place(c, p[0], (0, 0, W, H))
    # 2-3 · panorama across the seam
    place(c, p[1], (s(2) + 110, 190, s(4) - 110, 190 + 970))
    # 4-5 · tall bleed left, frame overlapping it and cut by the seam, tall bleed right
    place(c, p[2], (s(4), 0, s(4) + 660, H))
    place(c, p[4], (s(6) - 560, 0, s(6), H))
    place(c, p[3], (s(4) + 560, 700, s(4) + 560 + 900, 700 + 600), border=True)
    # 6-7 · large frame straddling the seam, tall detail overlapping its corner
    place(c, p[5], (s(6) + 200, 150, s(7) + 640, 150 + 960))
    place(c, p[6], (s(7) + 560, 760, s(7) + 1000, 760 + 500), border=True)
    # 8 · full bleed
    place(c, p[7], (s(8), 0, s(9), H))
    # 9 · top bleed with an inset overlapping its lower edge
    place(c, p[8], (s(9), 0, s(10), 700))
    place(c, p[9], (s(9) + 300, 600, s(10) - 80, 600 + 467), border=True)

    c = c.convert("RGBA")
    shade(c, (0, int(H * 0.45), W, H), 0, 225)
    d = ImageDraw.Draw(c)
    if listing.get("kicker"):
        tracked(d, (M, H - 278), listing["kicker"], font("Medium", 22), (255, 255, 255, 220), 8)
    d.text((M, H - 200), listing["title"], font=font("Light", 82), fill="white", anchor="lm")
    d.line((M, H - 128, M + 40, H - 128), fill=BLUE, width=3)
    tracked(d, (M + 56, H - 128), listing["area"], font("Medium", 22), (255, 255, 255, 220), 7)
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
