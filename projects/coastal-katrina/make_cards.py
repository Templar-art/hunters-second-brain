"""Rebuild Katrina Walsh's (Coastal) title + end cards as 4K PNGs.

Matched by eye to Hunter's screenshots of her films (2026-10-28):
- presents: "KATRINA WALSH" large thin caps over smaller medium "PRESENTS", white, centred, no shadow.
- end card: charcoal vertical gradient, name + number upper-centre, COASTAL° wordmark bottom-centre.

Usage: python3 make_cards.py [preview_background.jpg]
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).parent
OUT = HERE / "out"
VAULT = HERE.parents[1]
LOGO_WHITE = VAULT / "raw/coastal/coastal-logo-WHITE.png"
HN = "/System/Library/Fonts/HelveticaNeue.ttc"
LIGHT, MEDIUM = 7, 10  # HelveticaNeue.ttc face indices
W, H = 3840, 2160
WHITE = (255, 255, 255, 255)


def font(index, size):
    return ImageFont.truetype(HN, size, index=index)


def centred(draw, text, fnt, cy, tracking=0):
    """Draw text centred on x, with its cap height centred on cy. tracking in px between letters."""
    widths = [draw.textlength(c, font=fnt) for c in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = (W - total) / 2
    top, bottom = fnt.getbbox("H")[1], fnt.getbbox("H")[3]
    y = cy - (top + bottom) / 2
    for c, w in zip(text, widths):
        draw.text((x, y), c, font=fnt, fill=WHITE)
        x += w + tracking


def presents():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Name spans ~64% of frame width in the reference; PRESENTS ~27%.
    centred(d, "KATRINA WALSH", font(LIGHT, 300), cy=H * 0.40)
    centred(d, "PRESENTS", font(MEDIUM, 190), cy=H * 0.40 + 300, tracking=4)
    return img


def end_card():
    img = Image.new("RGBA", (W, H))
    top, bottom = (42, 46, 49), (29, 33, 36)
    px = img.load()
    for y in range(H):
        t = y / (H - 1)
        c = tuple(round(a + (b - a) * t) for a, b in zip(top, bottom)) + (255,)
        for x in range(W):
            px[x, y] = c
    d = ImageDraw.Draw(img)
    centred(d, "KATRINA WALSH", font(LIGHT, 190), cy=H * 0.30)
    centred(d, "0429 899 295", font(LIGHT, 190), cy=H * 0.30 + 225)
    logo = Image.open(LOGO_WHITE).convert("RGBA")
    lw = int(W * 0.30)
    logo = logo.resize((lw, round(logo.height * lw / logo.width)), Image.LANCZOS)
    img.alpha_composite(logo, ((W - lw) // 2, int(H * 0.87) - logo.height // 2))
    return img


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    p = presents()
    p.save(OUT / "katrina-walsh-presents-4k.png")
    e = end_card()
    e.convert("RGB").save(OUT / "katrina-walsh-end-card-4k.png")
    if len(sys.argv) > 1:
        bg = Image.open(sys.argv[1]).convert("RGBA")
        scale = max(W / bg.width, H / bg.height)
        bg = bg.resize((round(bg.width * scale), round(bg.height * scale)), Image.LANCZOS)
        bg = bg.crop(((bg.width - W) // 2, (bg.height - H) // 2, (bg.width + W) // 2, (bg.height + H) // 2))
        bg.alpha_composite(p)
        bg.convert("RGB").resize((1920, 1080)).save(OUT / "preview-presents.jpg", quality=88)
    e.convert("RGB").resize((1920, 1080)).save(OUT / "preview-end-card.jpg", quality=88)
    print("written to", OUT)
