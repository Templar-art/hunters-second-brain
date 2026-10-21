"""Side-by-side + 50% overlay of a rebuild against its source render: compare.py <src.jpg> <render.png> <out.jpg>"""
import sys
from PIL import Image, ImageDraw
src, ren, out = sys.argv[1:4]
a = Image.open(src).convert("RGB"); b = Image.open(ren).convert("RGB").resize(a.size)
w, h = a.size
s = (w // 2, h // 2)
ov = Image.blend(a, b, 0.5).resize(s)
sheet = Image.new("RGB", (s[0] * 3, s[1] + 30), "black")
for i, (im, t) in enumerate(((a.resize(s), "original"), (b.resize(s), "rebuild"), (ov, "overlay 50%"))):
    sheet.paste(im, (i * s[0], 30)); ImageDraw.Draw(sheet).text((i * s[0] + 8, 8), t, fill="white")
sheet.save(out, quality=88)
