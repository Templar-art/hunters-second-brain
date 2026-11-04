"""Trivelle store graphics v3 (1080x1080): 4-in-1 device + the real Microcurrent Gel tube.
Shot types follow the category's proven product-page structure (kit hero, benefit callouts,
3-step how-to, gel card, where-to-use, comparison, in-the-box, guarantee) — our own layouts,
our own photos, no stats or before/afters we can't back."""
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
import os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S, O = f"{R}/device-v2/stills", f"{R}/device-v2/graphics"
TUBE = f"{R}/device-v2/supplier-photos/gel-tube-cut.png"
FD = f"{R}/fonts"
os.makedirs(O, exist_ok=True)
N = 1080
INK, MUTE, BG, WHITE = (29, 42, 38), (88, 100, 96), (225, 232, 229), (255, 255, 255)
LIME = (196, 206, 38)  # matches the gel tube


def f(w, s):
    if w == "D":
        return ImageFont.truetype(f"{FD}/Anton-Regular.ttf", s)
    ft = ImageFont.truetype(f"{FD}/Montserrat.ttf", s)
    ft.set_variation_by_name(w)
    return ft


def fit(p, w, h, c=(0.5, 0.5)):
    return ImageOps.fit(Image.open(p).convert("RGB"), (w, h), Image.LANCZOS, centering=c)


def rounded(im, r):
    m = Image.new("L", im.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, *im.size), r, fill=255)
    o = Image.new("RGBA", im.size); o.paste(im, (0, 0), m); return o


def tube(canvas, x, y, h, angle=0, shadow=True):
    t = Image.open(TUBE).convert("RGBA")
    t = t.resize((int(t.width * h / t.height), h), Image.LANCZOS)
    if angle: t = t.rotate(angle, expand=True, resample=Image.BICUBIC)
    if shadow:
        sh = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        a = t.split()[3].point(lambda v: int(v * 0.30))
        blk = Image.new("RGBA", t.size, (20, 30, 25, 255)); blk.putalpha(a)
        sh.paste(blk, (x + 18, y + 22), blk)
        canvas.alpha_composite(sh.filter(ImageFilter.GaussianBlur(22)))
    canvas.alpha_composite(t, (x, y))
    return t.size


def wrap(d, text, font, width):
    out, line = [], ""
    for w in text.split():
        t = (line + " " + w).strip()
        if d.textlength(t, font=font) > width and line: out.append(line); line = w
        else: line = t
    return out + [line]


def para(d, xy, text, font, width, fill, lh):
    x, y = xy
    for l in wrap(d, text, font, width): d.text((x, y), l, font=font, fill=fill); y += lh
    return y


def badge(d, cx, cy, r=82, bg=INK, fg=WHITE):
    d.ellipse((cx-r, cy-r, cx+r, cy+r), fill=bg)
    d.ellipse((cx-r+8, cy-r+8, cx+r-8, cy+r-8), outline=fg, width=2)
    for t, ft, dy in (("30", f("D", 62), -24), ("DAY", f("SemiBold", 19), 26), ("MONEY-BACK", f("SemiBold", 13), 50)):
        w = d.textlength(t, font=ft); d.text((cx - w/2, cy + dy - ft.size*0.6), t, font=ft, fill=fg)


def eyebrow(d, xy, t, fill=MUTE):
    d.text(xy, t.upper(), font=f("SemiBold", 20), fill=fill, spacing=4)


def save(im, n):
    im.convert("RGB").save(f"{O}/{n}.jpg", quality=94); print(n)


# 01 — Kit hero: device on the counter + the gel beside it, clean offer strip
im = fit(f"{S}/01-hero-v2-pilot.png", N, N, (0.42, 0.5)).convert("RGBA")
tube(im, 700, 300, 560, angle=-4)
d = ImageDraw.Draw(im)
d.rectangle((0, 0, N, 150), fill=(255, 255, 255, 0))
eyebrow(d, (60, 56), "Trivelle  ·  4-in-1 Sculpt & Glow", INK)
d.text((60, 86), "The full at-home ritual.", font=f("D", 58), fill=INK)
d.rounded_rectangle((0, 930, N, N), 0, fill=INK)
x = 60
for t in ("Heat", "Red light", "EMS", "Vacuum"):
    d.ellipse((x, 992, x+14, 1006), fill=LIME); d.text((x+24, 982), t, font=f("SemiBold", 28), fill=WHITE)
    x += d.textlength(t, font=f("SemiBold", 28)) + 70
d.text((x + 10, 984), "+ gel included", font=f("Regular", 26), fill=(200, 210, 205))
save(im, "01-kit-hero")

# 02 — Four rituals: product centred, four callouts around it
im = Image.new("RGBA", (N, N), BG + (255,)); d = ImageDraw.Draw(im)
ph = rounded(fit(f"{S}/02-macro-head.png", 460, 560), 230); im.alpha_composite(ph, (310, 300))
eyebrow(d, (60, 60), "One device, four rituals")
d.text((60, 92), "Everything a salon does,", font=f("D", 56), fill=INK)
d.text((60, 160), "in ten minutes at home.", font=f("D", 56), fill=(62, 86, 80))
cards = [((60, 330), "Warm", "Gentle heat for a relaxing, massage-like feel."),
         ((780, 330), "Glow", "Red light mode for a radiant-looking finish."),
         ((60, 700), "Lift", "EMS micro-pulses for a toning, firming feel."),
         ((780, 700), "Smooth", "Vacuum massage to smooth the look of skin.")]
for k, ((x, y), h, b) in enumerate(cards):
    d.rounded_rectangle((x, y, x+240, y+250), 22, fill=WHITE)
    d.text((x+24, y+22), f"0{k+1}", font=f("SemiBold", 20), fill=MUTE)
    d.text((x+24, y+50), h, font=f("D", 46), fill=INK)
    para(d, (x+24, y+120), b, f("Regular", 21), 196, MUTE, 29)
    ax = x + 240 if x < 500 else x
    d.line((ax, y+125, 340 if x < 500 else 740, y+125 + (60 if y < 500 else -60)), fill=INK, width=2)
d.text((60, 1000), "Cordless  ·  USB rechargeable  ·  Face & body", font=f("Medium", 24), fill=INK)
save(im, "02-four-rituals")

# 03 — How to use: 3 photo steps, gel first
im = Image.new("RGBA", (N, N), WHITE + (255,)); d = ImageDraw.Draw(im)
eyebrow(d, (60, 60), "10 minutes, 3–5 times a week")
d.text((60, 92), "How to use Trivelle", font=f("D", 64), fill=INK)
cols = [(None, "Apply the gel", "A thin, even layer on clean, dry skin."),
        ("s3-arm.png", "Glide slowly", "Pick a mode and level, then move in slow upward strokes."),
        ("s6-sofa-screen.png", "Wipe & moisturise", "Remove leftover gel, then your usual skincare.")]
for k, (img, h, b) in enumerate(cols):
    x = 60 + k*330
    if img:
        im.alpha_composite(rounded(fit(f"{S}/{img}", 300, 470, (0.5, 0.35)), 24), (x, 230))
    else:
        tile = Image.new("RGBA", (300, 470), BG + (255,)); im.alpha_composite(rounded(tile, 24), (x, 230))
        tube(im, x + 85, 255, 420, shadow=False)
    d.ellipse((x+16, 246, x+64, 294), fill=INK)
    w = d.textlength(str(k+1), font=f("D", 30)); d.text((x+40-w/2, 252), str(k+1), font=f("D", 30), fill=WHITE)
    d.text((x, 730), h, font=f("D", 40), fill=INK)
    para(d, (x, 790), b, f("Regular", 23), 290, MUTE, 32)
d.text((60, 1000), "Start on the lowest level and work up.", font=f("Medium", 24), fill=INK)
save(im, "03-how-to-use")

# 04 — The gel: hero of the tube, what it does (no ingredient claims we can't verify)
im = Image.new("RGBA", (N, N), BG + (255,)); d = ImageDraw.Draw(im)
d.ellipse((520, 170, 1040, 690), fill=(236, 240, 222))
tube(im, 600, 150, 820, angle=-6)
eyebrow(d, (60, 120), "Included in every kit")
d.text((60, 152), "Pro-grade", font=f("D", 72), fill=INK)
d.text((60, 236), "microcurrent gel", font=f("D", 72), fill=INK)
y = 380
for h, b in (("Glides", "Lets the device move smoothly without dragging on skin."),
             ("Conducts", "Helps the EMS mode reach the skin evenly."),
             ("Light", "Water-based and clear. Wipes off clean, no sticky feel.")):
    d.rectangle((60, y+8, 66, y+92), fill=LIME)
    d.text((88, y), h, font=f("D", 36), fill=INK)
    para(d, (88, y+50), b, f("Regular", 23), 400, MUTE, 31)
    y += 165
d.text((60, 1000), "80 g tube  ·  a small amount covers each area", font=f("Medium", 24), fill=INK)
save(im, "04-gel")

# 05 — Where to use: four real-use photos
im = Image.new("RGBA", (N, N), WHITE + (255,)); d = ImageDraw.Draw(im)
eyebrow(d, (60, 56), "Made for skin that's lived a little")
d.text((60, 88), "Use it where you need it", font=f("D", 60), fill=INK)
for k, (img, t, c) in enumerate([("s1-stomach.png", "Stomach", (0.5, 0.45)), ("s5-thigh-front.png", "Thighs", (0.5, 0.6)),
                                 ("s3-arm.png", "Arms", (0.5, 0.35)), ("s4-jaw.png", "Jawline", (0.5, 0.3))]):
    x, y = 60 + (k % 2)*490, 200 + (k // 2)*420
    im.alpha_composite(rounded(fit(f"{S}/{img}", 470, 400, c), 24), (x, y))
    w = d.textlength(t, font=f("SemiBold", 26))
    d.rounded_rectangle((x+20, y+330, x+52+w, y+380), 25, fill=WHITE)
    d.text((x+36, y+340), t, font=f("SemiBold", 26), fill=INK)
save(im, "05-where-to-use")

# 06 — Comparison (qualitative only)
im = Image.new("RGBA", (N, N), BG + (255,)); d = ImageDraw.Draw(im)
eyebrow(d, (60, 60), "The honest comparison")
d.text((60, 92), "Why Trivelle?", font=f("D", 68), fill=INK)
cols = ["Trivelle", "Creams", "Salon"]; cx = [620, 800, 960]
rows = ["Heat, red light, EMS and vacuum in one", "Use at home, any time", "One-off price, no appointments",
        "10 minutes, a few times a week", "30-day money-back guarantee"]
have = [(1, 0, 1), (1, 1, 0), (1, 1, 0), (1, 1, 0), (1, 0, 0)]
d.rounded_rectangle((540, 200, 700, 980), 26, fill=INK)
for c, x in zip(cols, cx):
    w = d.textlength(c, font=f("SemiBold", 26)); d.text((x-w/2, 228), c, font=f("SemiBold", 26), fill=WHITE if c == "Trivelle" else INK)
for i, (r, h) in enumerate(zip(rows, have)):
    y = 330 + i*128
    d.line((60, y-24, 1020, y-24), fill=(205, 212, 208), width=2)
    para(d, (60, y), r, f("Medium", 26), 440, INK, 34)
    for v, x in zip(h, cx):
        cy = y + 28
        if v:
            d.ellipse((x-24, cy-24, x+24, cy+24), fill=LIME if x == cx[0] else INK)
            d.line((x-11, cy, x-3, cy+9, x+12, cy-9), fill=INK if x == cx[0] else WHITE, width=5)
        else:
            for s in (1, -1): d.line((x-12, cy-12*s, x+12, cy+12*s), fill=(170, 178, 174), width=5)
save(im, "06-comparison")

# 07 — In the box: flatlay + the real gel tube
im = fit(f"{S}/03-flatlay.png", N, N).convert("RGBA")
tube(im, 820, 560, 420, angle=12)
d = ImageDraw.Draw(im)
d.rounded_rectangle((50, 690, 540, 1030), 28, fill=WHITE)
d.text((86, 718), "What's in the box", font=f("D", 42), fill=INK)
for i, t in enumerate(["Trivelle 4-in-1 device", "Microcurrent gel, 80 g", "USB charging cable", "English user manual"]):
    yy = 790 + i*52; d.ellipse((88, yy+10, 106, yy+28), fill=LIME); d.text((124, yy), t, font=f("Regular", 27), fill=INK)
save(im, "07-in-the-box")

# 08 — Guarantee
im = fit(f"{S}/05-shelf.png", N, N).convert("RGBA")
ov = Image.new("RGBA", (N, N), (0, 0, 0, 0)); ImageDraw.Draw(ov).rectangle((0, 0, 560, N), fill=BG + (240,))
im.alpha_composite(ov); d = ImageDraw.Draw(im)
badge(d, 150, 170)
d.text((60, 300), "Try it for", font=f("D", 64), fill=INK)
d.text((60, 375), "30 days.", font=f("D", 64), fill=INK)
para(d, (60, 480), "Use Trivelle for a month. If it isn't for you, send it back for a full refund. No fuss.",
     f("Regular", 26), 440, MUTE, 38)
y = 700
for t in ("Free shipping Australia-wide", "Tracked delivery", "Fast, real support"):
    d.ellipse((62, y+10, 78, y+26), fill=INK); d.text((96, y), t, font=f("Medium", 25), fill=INK); y += 52
save(im, "08-guarantee")
