"""Label the skin cross-section render (2048px) -> 1080 graphic."""
import os
from PIL import Image, ImageDraw, ImageFont
F = "/Users/10xhunter/Library/Fonts/Poppins-"
FD = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "fonts")
def f(w, s):
    """Brand kit: Anton display (Bold/Black), Montserrat body."""
    if w in ("Bold", "Black"):
        return ImageFont.truetype(f"{FD}/Anton-Regular.ttf", int(s * 1.08))
    ft = ImageFont.truetype(f"{FD}/Montserrat.ttf", s)
    ft.set_variation_by_name({"SemiBold": "SemiBold", "Medium": "Medium", "Regular": "Regular"}.get(w, "Regular"))
    return ft
INK, SAGE, MUTE = (29, 42, 38), (62, 86, 80), (88, 100, 96)
im = Image.open("stills/09-skin-layers.png").convert("RGB"); d = ImageDraw.Draw(im)
d.text((90, 90), "How Trivelle works", font=f("Bold", 92), fill=INK)
d.text((90, 205), "Three rituals, working together", font=f("Regular", 46), fill=SAGE)
labels = [((255, 92, 80), "Glow", "Red light for a radiant-looking surface", 820, (1080, 870)),
          ((120, 160, 220), "Lift", "EMS pulses for a toning, firming feel", 1140, (1150, 1250)),
          ((200, 170, 60), "Sculpt", "Suction massage to smooth the look of skin", 1530, (1100, 1620))]
for col, h, b, y, tgt in labels:
    x0, x1 = 60, 840
    d.rounded_rectangle((x0, y, x1, y+170), 30, fill=(255, 255, 255))
    d.ellipse((x0+30, y+38, x0+66, y+74), fill=col)
    d.text((x0+90, y+22), h, font=f("Bold", 56), fill=INK)
    d.text((x0+90, y+98), b, font=f("Regular", 30), fill=MUTE)
    d.line((x1, y+85, tgt[0], tgt[1]), fill=(255, 255, 255), width=5)
    d.ellipse((tgt[0]-12, tgt[1]-12, tgt[0]+12, tgt[1]+12), fill=(255, 255, 255), outline=INK, width=4)
d.text((90, 1950), "Cosmetic use. Results vary by person.", font=f("Regular", 28), fill=MUTE)
im.resize((1080, 1080), Image.LANCZOS).save("graphics/05-how-it-works.jpg", quality=94)
