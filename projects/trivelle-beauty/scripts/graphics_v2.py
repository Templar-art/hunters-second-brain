"""Trivelle store graphics (1080x1080) built from our own stills. No claims we can't back."""
from PIL import Image, ImageDraw, ImageFont, ImageOps
import os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S, O = f"{R}/device-v2/stills", f"{R}/device-v2/graphics"
os.makedirs(O, exist_ok=True)
F = "/Users/10xhunter/Library/Fonts/Poppins-"
FD = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "fonts")
def f(w, s):
    """Brand kit: Anton display (Bold/Black), Montserrat body."""
    if w in ("Bold", "Black"):
        return ImageFont.truetype(f"{FD}/Anton-Regular.ttf", int(s * 1.08))
    ft = ImageFont.truetype(f"{FD}/Montserrat.ttf", s)
    ft.set_variation_by_name({"SemiBold": "SemiBold", "Medium": "Medium", "Regular": "Regular"}.get(w, "Regular"))
    return ft
INK, SAGE, LIME, BG, MUTE = (29, 42, 38), (62, 86, 80), (139, 0, 0), (225, 232, 229), (88, 100, 96)  # brand kit: #1D2A26 / #8B0000 / #E1E8E5
N = 1080

def fit(path, w, h):
    return ImageOps.fit(Image.open(path).convert("RGB"), (w, h), Image.LANCZOS)

def rounded(im, r):
    m = Image.new("L", im.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, *im.size), r, fill=255)
    out = Image.new("RGBA", im.size); out.paste(im, (0, 0), m); return out

def badge(d, cx, cy, r=78):
    d.ellipse((cx-r, cy-r, cx+r, cy+r), fill=INK)
    d.ellipse((cx-r+7, cy-r+7, cx+r-7, cy+r-7), outline=(255,255,255), width=2)
    for t, ft, dy in (("30", f("Bold", 54), -30), ("DAY", f("SemiBold", 20), 22), ("MONEY-BACK", f("Medium", 13), 46)):
        w = d.textlength(t, font=ft); d.text((cx-w/2, cy+dy-ft.size*0.62), t, font=ft, fill=(255, 255, 255))

def wrap(d, text, font, width):
    out, line = [], ""
    for w in text.split():
        t = (line + " " + w).strip()
        if d.textlength(t, font=font) > width and line: out.append(line); line = w
        else: line = t
    return out + [line]

# 1 — Feature panel: three rituals over the benefits still
im = fit(f"{S}/01-hero-v2-pilot.png", N, N); d = ImageDraw.Draw(im)
d.text((70, 70), "Four rituals.", font=f("Bold", 64), fill=INK)
d.text((70, 145), "One device.", font=f("Bold", 64), fill=SAGE)
y = 250
for k, (h, b) in enumerate([("Warm", "Gentle heat for a relaxing massage feel"),
                            ("Glow", "Red light mode for a radiant-looking finish"),
                            ("Lift", "EMS micro-pulses for a toning, firming feel"),
                            ("Smooth", "Vacuum massage to smooth the look of skin")]):
    x = 620
    d.rounded_rectangle((x, y, x+400, y+150), 22, fill=(255, 255, 255))
    d.ellipse((x+24, y+28, x+64, y+68), fill=INK); d.text((x+38, y+28), str(k+1), font=f("Bold", 24), fill=(255,255,255))
    d.text((x+82, y+24), h, font=f("Bold", 38), fill=INK)
    for i, l in enumerate(wrap(d, b, f("Regular", 21), 290)): d.text((x+82, y+76+i*28), l, font=f("Regular", 21), fill=MUTE)
    y += 168
badge(d, 950, 140)
d.text((70, 990), "10 minutes, 3–5x a week  ·  Face & body  ·  Cordless", font=f("Medium", 26), fill=INK)
im.save(f"{O}/01-feature-panel.jpg", quality=94)

# 2 — How to use: 3 steps
im = Image.new("RGB", (N, N), BG); d = ImageDraw.Draw(im)
d.text((70, 60), "How to use", font=f("Regular", 52), fill=MUTE)
d.text((70, 120), "your Trivelle", font=f("Bold", 60), fill=INK)
steps = [("s1-stomach.png", "Apply the gel", "Spread a thin, even layer of conductive gel on clean, dry skin."),
         ("s5-thigh-front.png", "Glide for 10 minutes", "Pick your mode and level on the screen, then move slowly over each area."),
         ("s6-sofa-screen.png", "Repeat 3–5x a week", "Wipe off leftover gel and follow with your usual skincare.")]
y = 250
for k, (img, h, b) in enumerate(steps):
    ph = rounded(fit(f"{S}/{img}", 240, 230), 22); im.paste(ph, (70, y), ph)
    d.text((345, y+20), f"STEP {k+1}", font=f("SemiBold", 22), fill=SAGE)
    d.text((345, y+52), h, font=f("Bold", 40), fill=INK)
    for i, l in enumerate(wrap(d, b, f("Regular", 25), 640)): d.text((345, y+112+i*36), l, font=f("Regular", 25), fill=MUTE)
    y += 265
im.save(f"{O}/02-how-to-use.jpg", quality=94)

# 3 — Comparison: Trivelle vs creams vs salon (qualitative, no stats)
im = Image.new("RGB", (N, N), BG); d = ImageDraw.Draw(im)
d.text((70, 60), "Why Trivelle?", font=f("Bold", 64), fill=INK)
cols = ["Trivelle", "Creams", "Salon"]; cx = [600, 790, 960]
rows = ["Heat, red light, EMS and vacuum in one", "Use at home, any time", "One-off price, no appointments",
        "10 minutes, a few times a week", "30-day money-back guarantee"]
have = [(1, 0, 1), (1, 1, 0), (1, 1, 0), (1, 1, 0), (1, 0, 0)]
d.rounded_rectangle((520, 190, 680, 960), 26, fill=INK)
for c, x in zip(cols, cx):
    w = d.textlength(c, font=f("Bold", 28)); d.text((x-w/2, 215), c, font=f("Bold", 28), fill=(255, 255, 255) if c == "Trivelle" else INK)
for i, (r, h) in enumerate(zip(rows, have)):
    y = 320 + i*128
    d.line((70, y-22, 1010, y-22), fill=(222, 226, 222), width=2)
    for j, l in enumerate(wrap(d, r, f("Medium", 27), 420)): d.text((70, y+j*36), l, font=f("Medium", 27), fill=INK)
    for v, x in zip(h, cx):
        cy = y+30
        if v: d.ellipse((x-24, cy-24, x+24, cy+24), fill=(255,255,255) if x==cx[0] else INK); d.line((x-11, cy, x-3, cy+9, x+12, cy-9), fill=INK if x==cx[0] else (255,255,255), width=5)
        else: d.line((x-12, cy-12, x+12, cy+12), fill=(180, 186, 182), width=5); d.line((x-12, cy+12, x+12, cy-12), fill=(180, 186, 182), width=5)
im.save(f"{O}/03-comparison.jpg", quality=94)

# 4 — What's in the box
im = fit(f"{S}/03-flatlay.png", N, N); d = ImageDraw.Draw(im)
d.rounded_rectangle((50, 640, 560, 990), 28, fill=(255, 255, 255))
d.text((90, 675), "What's in the box", font=f("Bold", 40), fill=INK)
for i, t in enumerate(["Trivelle 4-in-1 device", "USB charging cable", "User guide", "Gift box", "Conductive gel (kit only)"]):
    yy = 750 + i*44; d.ellipse((92, yy+10, 108, yy+26), fill=LIME); d.text((124, yy), t, font=f("Regular", 26), fill=INK)
im.save(f"{O}/04-in-the-box.jpg", quality=94)
print("ok")
