"""Label the skin cross-section render (2048px) -> 1080 graphic."""
from PIL import Image, ImageDraw, ImageFont
F = "/Users/10xhunter/Library/Fonts/Poppins-"
def f(w, s): return ImageFont.truetype(F + w + ".ttf", s)
INK, SAGE, MUTE = (24, 52, 46), (60, 96, 86), (96, 112, 106)
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
