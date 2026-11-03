# Renders the 10x "Postcards" title overlay to brand guidelines v1.0 (4K transparent PNG) + preview.jpg
# Poppins Bold title, white on footage, master logo (blue X untouched, no shadow on logo), 10X Light Blue accent.
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np, cairosvg, io, sys
F="/Users/10xhunter/Library/Fonts/"; W,H=3840,2160
LOGO="/Users/10xhunter/Desktop/_Brand & Tools/10x-Visuals/Logos & Symbols/10xVisuals_White Logo Blue X.svg"
BLUE=(97,168,216,255)
title=ImageFont.truetype(F+"Poppins-Bold.ttf",230)
L=Image.new("L",(W,H),0); d=ImageDraw.Draw(L); cx=W//2; base=1080
txt="POSTCARDS"; sp=int(230*0.18)
w=sum(d.textlength(ch,font=title) for ch in txt)+sp*(len(txt)-1); x=cx-w/2
for ch in txt: d.text((x,base),ch,font=title,fill=255,anchor="ls"); x+=d.textlength(ch,font=title)+sp
logo=Image.open(io.BytesIO(cairosvg.svg2png(url=LOGO,output_width=460))).convert("RGBA"); logo=logo.crop(logo.getbbox())
c=Image.new("RGBA",(W,H),(0,0,0,0))
sh=Image.new("RGBA",(W,H),(0,0,0,0)); sh.putalpha(L.filter(ImageFilter.GaussianBlur(50)).point(lambda v:int(v*.4))); c.alpha_composite(sh)
txtim=Image.new("RGBA",(W,H),(255,255,255,0)); txtim.putalpha(L); c.alpha_composite(txtim)
ry=base+95; ImageDraw.Draw(c).rectangle((cx-70,ry,cx+70,ry+6),fill=BLUE)
c.alpha_composite(logo,(cx-logo.width//2,ry+110))
c.save("10x_postcards_title_4K.png")
if len(sys.argv)>1:
    bg=Image.open(sys.argv[1]).convert('RGBA')
    top=bg.crop((0,150,1174,420)); low=bg.crop((0,650,1174,858))
    b=Image.new('RGBA',(1174,708)); b.paste(top.resize((1174,400)),(0,0)); b.paste(low.resize((1174,308)),(0,400))
    b=b.resize((W,H)); b.alpha_composite(c); b.convert('RGB').resize((1920,1080)).save('preview.jpg',quality=88)
