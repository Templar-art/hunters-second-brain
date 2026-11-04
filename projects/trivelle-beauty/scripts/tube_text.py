"""Lay vertical label text onto the gel tube in a hero still."""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
F = "/Users/10xhunter/Library/Fonts/Poppins-"
src, out = sys.argv[1], sys.argv[2]
cx, cy = int(sys.argv[3]), int(sys.argv[4])   # tube body centre (px)
im = Image.open(src).convert("RGBA")
col = (38, 46, 20, 235)
big = ImageFont.truetype(F + "SemiBold.ttf", 54)
sm = ImageFont.truetype(F + "Medium.ttf", 22)
# build horizontal label then rotate 90° (reads bottom-to-top like the ref)
W, H = 640, 170
lab = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(lab)
def c(t, f, y):
    w = d.textlength(t, font=f); d.text(((W - w) / 2, y), t, font=f, fill=col)
c("MICROCURRENT GEL", big, 28)
c("PRO GRADE   ·   GLOW · LIFT · SCULPT", sm, 108)
lab = lab.rotate(90, expand=True, resample=Image.BICUBIC).filter(ImageFilter.GaussianBlur(0.4))
im.alpha_composite(lab, (cx - lab.width // 2, cy - lab.height // 2))
im.convert("RGB").save(out, quality=95)
