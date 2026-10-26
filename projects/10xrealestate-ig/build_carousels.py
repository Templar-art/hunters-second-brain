"""Editorial 4:5 carousels for @10xrealestate_.

Slide types: cover (full-bleed hero + address), full (full-bleed + room label),
stack (two photos on navy), end (navy card with the 10X mark).
Fixed skeleton on every slide: mark top-left, index top-right.
Run: python3 build_carousels.py
"""
import io, json, os
import cairosvg
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

Image.MAX_IMAGE_PIXELS = None
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = "/Users/10xhunter/Documents/Posting for 10xRealestate/To Post"
LOGO = "/Users/10xhunter/Desktop/_Brand & Tools/10x-Visuals/Logos & Symbols/10xVisuals_10X Symbol Blue X.svg"
FONTS = "/Users/10xhunter/Library/Fonts/"
W, H, M = 1080, 1350, 64
NAVY = (0x10, 0x2F, 0x41)
X_ON_DARK = (0x6F, 0x92, 0xC8)


def font(weight, size):
    return ImageFont.truetype(f"{FONTS}Poppins-{weight}.ttf", size)


def tracked(draw, xy, text, fnt, fill, track, anchor="l"):
    """Letter-spaced text. anchor l/r/m on x; y is the text middle."""
    widths = [draw.textlength(c, font=fnt) for c in text]
    total = sum(widths) + track * (len(text) - 1)
    x, y = xy
    if anchor == "r":
        x -= total
    elif anchor == "m":
        x -= total / 2
    for c, w in zip(text, widths):
        draw.text((x, y), c, font=fnt, fill=fill, anchor="lm")
        x += w + track
    return total


def mark(width, ten=None, xcol=X_ON_DARK):
    m = Image.open(io.BytesIO(cairosvg.svg2png(url=LOGO, output_width=width))).convert("RGBA")
    px = m.load()
    ref = (0x61 + 0xA8 + 0xD8) / 3
    for y in range(m.height):
        for x in range(m.width):
            r, g, b, a = px[x, y]
            if not a:
                continue
            if r > 200 and g > 200 and b > 200:
                if ten:
                    px[x, y] = ten + (a,)
            else:
                k = ((r + g + b) / 3) / ref
                px[x, y] = tuple(min(255, int(c * k)) for c in xcol) + (a,)
    return m


PAPER = (0xF6, 0xF4, 0xF0)
X_ON_LIGHT = (0x2C, 0x4A, 0x7A)
MARK = mark(118)
MARK_LIGHT = mark(118, NAVY, X_ON_LIGHT)


def grade(im):
    im = ImageEnhance.Contrast(im).enhance(1.07)
    im = ImageEnhance.Color(im).enhance(1.05)
    r, g, b = im.split()
    r = r.point(lambda v: min(255, int(v * 1.02)))
    b = b.point(lambda v: int(v * 0.98))
    im = Image.merge("RGB", (r, g, b))
    vig = Image.new("L", im.size, 0)
    ImageDraw.Draw(vig).ellipse((-im.width * 0.25, -im.height * 0.25, im.width * 1.25, im.height * 1.25), fill=255)
    vig = vig.filter(ImageFilter.GaussianBlur(im.width // 6))
    dark = ImageEnhance.Brightness(im).enhance(0.82)
    return Image.composite(im, dark, vig)


def load(path, size):
    im = ImageOps.exif_transpose(Image.open(path))
    im.draft("RGB", (size[0] * 2, size[1] * 2))
    im = ImageOps.fit(im.convert("RGB"), size, Image.LANCZOS, centering=(0.5, 0.5))
    return grade(im)


def gradient(size, top_alpha, bottom_alpha):
    g = Image.new("L", (1, 256))
    for y in range(256):
        g.putpixel((0, y), int(top_alpha + (bottom_alpha - top_alpha) * (y / 255) ** 1.6))
    return g.resize(size)


def shade(canvas, box, top_alpha, bottom_alpha):
    x0, y0, x1, y1 = box
    layer = Image.new("RGBA", (x1 - x0, y1 - y0), (0, 0, 0, 255))
    layer.putalpha(gradient(layer.size, top_alpha, bottom_alpha))
    canvas.alpha_composite(layer, (x0, y0))


def chrome(canvas, n, total, theme):
    if theme in ("photo", "split"):
        shade(canvas, (0, 0, 660 if theme == "split" else W, 200), 70, 0)
    light = theme == "light"
    canvas.alpha_composite(MARK_LIGHT if light else MARK, (M, M - 8))
    d = ImageDraw.Draw(canvas)
    ink = NAVY + (230,) if theme in ("light", "split") else (255, 255, 255, 230)
    tracked(d, (W - M, M + MARK.height // 2 - 8), f"{n:02d} / {total:02d}", font("Medium", 22), ink, 4, "r")


def mat(p, label):
    """Single photo on warm paper with generous margins: the gallery wall slide."""
    c = Image.new("RGBA", (W, H), PAPER + (255,))
    side = 96
    pw = W - 2 * side
    ph = int(pw * 2 / 3)
    top = (H - ph) // 2 + 10
    c.paste(load(p, (pw, ph)), (side, top))
    if label:
        d = ImageDraw.Draw(c)
        y = top + ph + 64
        d.line((side, y, side + 40, y), fill=X_ON_LIGHT, width=3)
        tracked(d, (side + 56, y), label.upper(), font("Medium", 22), NAVY + (255,), 7)
    return c


def split(p, label):
    """Tall crop on the left, quiet paper panel on the right with the room name."""
    c = Image.new("RGBA", (W, H), PAPER + (255,))
    pw = 660
    c.paste(load(p, (pw, H)), (0, 0))
    d = ImageDraw.Draw(c)
    x = pw + 60
    d.line((x, H - 240, x + 40, H - 240), fill=X_ON_LIGHT, width=3)
    words = (label or "").upper().split()
    for i, w in enumerate(words):
        tracked(d, (x, H - 180 + i * 44), w, font("Medium", 24), NAVY + (255,), 7)
    return c


def cover(p, listing):
    c = load(p, (W, H)).convert("RGBA")
    shade(c, (0, int(H * 0.45), W, H), 0, 225)
    d = ImageDraw.Draw(c)
    d.text((M, H - 200), listing["title"], font=font("Light", 82), fill="white", anchor="lm")
    d.line((M, H - 128, M + 40, H - 128), fill=X_ON_DARK, width=3)
    tracked(d, (M + 56, H - 128), listing["area"], font("Medium", 22), (255, 255, 255, 220), 7)
    return c


def full(p, label):
    c = load(p, (W, H)).convert("RGBA")
    if label:
        shade(c, (0, H - 260, W, H), 0, 150)
        d = ImageDraw.Draw(c)
        d.line((M, H - M - 2, M + 40, H - M - 2), fill=X_ON_DARK, width=3)
        tracked(d, (M + 56, H - M - 2), label.upper(), font("Medium", 22), (255, 255, 255, 230), 7)
    return c


def stack(p1, p2, label):
    c = Image.new("RGBA", (W, H), NAVY + (255,))
    inset, gap, top = 40, 16, 196
    bottom = 150 if label else 120
    ph = (H - top - bottom - gap) // 2
    c.paste(load(p1, (W - 2 * inset, ph)), (inset, top))
    c.paste(load(p2, (W - 2 * inset, ph)), (inset, top + ph + gap))
    if label:
        d = ImageDraw.Draw(c)
        y = H - 80
        d.line((M, y, M + 40, y), fill=X_ON_DARK, width=3)
        tracked(d, (M + 56, y), label.upper(), font("Medium", 22), (255, 255, 255, 220), 7)
    return c


def end():
    c = Image.new("RGBA", (W, H), NAVY + (255,))
    big = mark(300)
    c.alpha_composite(big, ((W - big.width) // 2, H // 2 - big.height // 2 - 60))
    d = ImageDraw.Draw(c)
    tracked(d, (W // 2, H // 2 + 110), "PHOTOGRAPHY  ·  FILM", font("Medium", 24), (255, 255, 255, 230), 8, "m")
    tracked(d, (W // 2, H - 120), "@10XREALESTATE_", font("Medium", 20), (255, 255, 255, 150), 6, "m")
    return c


def build(key, listing, photos):
    out = f"{HERE}/carousels/{key}"
    os.makedirs(out, exist_ok=True)
    for f in os.listdir(out):
        os.remove(f"{out}/{f}")
    slides = listing["slides"]
    total = len(slides) + 1
    for n, s in enumerate(slides, 1):
        kind = s[0]
        if kind == "cover":
            c = cover(photos[s[1]], listing)
        elif kind == "full":
            c = full(photos[s[1]], s[2] if len(s) > 2 else None)
        elif kind == "mat":
            c = mat(photos[s[1]], s[2] if len(s) > 2 else None)
        elif kind == "split":
            c = split(photos[s[1]], s[2] if len(s) > 2 else None)
        else:
            c = stack(photos[s[1]], photos[s[2]], s[3] if len(s) > 3 else None)
        theme = {"stack": "navy", "mat": "light", "split": "split"}.get(kind, "photo")
        chrome(c, n, total, theme)
        c.convert("RGB").save(f"{out}/{n:02d}.jpg", quality=93)
    e = end()
    chrome(e, total, total, "navy")
    e.convert("RGB").save(f"{out}/{total:02d}.jpg", quality=93)


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
