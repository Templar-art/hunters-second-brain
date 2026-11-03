# Renders the 10X "Postcards" title overlay (4K transparent PNG) + preview.jpg
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np, cairosvg, io, sys
S="/System/Library/Fonts/Supplemental/"; W,H=3840,2160
LOGO="/Users/10xhunter/Desktop/_Brand & Tools/10x-Visuals/Logos & Symbols/10xVisuals_White Logo (all white).svg"
def champagne(mask):
    yy,xx=np.mgrid[0:H,0:W]; t=((xx-W*.3)*.35+(yy-H*.3))/H
    base=np.array([226,204,160.]); hi=np.array([250,240,218.])
    col=base+(hi-base)*(np.exp(-((t-.34)/.14)**2)[...,None]*.7)
    im=Image.fromarray(col.astype(np.uint8)).convert("RGBA"); im.putalpha(mask); return im
ital=ImageFont.truetype(S+"Bodoni 72.ttc",340,index=1)
L=Image.new("L",(W,H),0); d=ImageDraw.Draw(L); cx=W//2; base=1130
d.text((cx,base),"Postcards",font=ital,fill=255,anchor="ms")
d.line((cx-45,base+100,cx+45,base+100),fill=210,width=3)
logo=Image.open(io.BytesIO(cairosvg.svg2png(url=LOGO,output_width=380))).convert("RGBA"); logo=logo.crop(logo.getbbox())
a=np.array(logo.getchannel("A")); logo=Image.new("RGBA",logo.size,(250,246,238,0)); logo.putalpha(Image.fromarray((a*.92).astype(np.uint8)))
lx,ly=cx-logo.width//2,base+165
full=L.copy(); full.paste(logo.getchannel("A"),(lx,ly),logo.getchannel("A"))
c=Image.new("RGBA",(W,H),(0,0,0,0))
for blur,op,off in((60,.38,0),(4,.35,4)):
    sh=Image.new("RGBA",(W,H),(0,0,0,0)); sh.putalpha(full.filter(ImageFilter.GaussianBlur(blur)).point(lambda v:int(v*op))); c.alpha_composite(sh,(off,off))
c.alpha_composite(champagne(L)); c.alpha_composite(logo,(lx,ly)); c.save("10x_postcards_title_4K.png")
if len(sys.argv)>1:
    bg=Image.open(sys.argv[1]).convert('RGBA')
    top=bg.crop((0,150,1174,420)); low=bg.crop((0,650,1174,858))
    b=Image.new('RGBA',(1174,708)); b.paste(top.resize((1174,400)),(0,0)); b.paste(low.resize((1174,308)),(0,400))
    b=b.resize((W,H)); b.alpha_composite(c); b.convert('RGB').resize((1920,1080)).save('preview.jpg',quality=88)
