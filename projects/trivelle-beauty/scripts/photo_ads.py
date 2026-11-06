import os
from PIL import Image, ImageDraw, ImageFont
R="/Users/10xhunter/Documents/Hunters Second Brain/projects/trivelle-beauty"
OUT="/private/tmp/claude-502/-Users-10xhunter-Documents-Hunters-Second-Brain/1c99944e-82b8-4518-b0a9-707f60021b4b/scratchpad/ads"
W,H=1080,1350
GREEN=(29,42,38); LIME=(196,206,38); SAGE=(225,232,229); WHITE=(255,255,255)
anton=lambda s: ImageFont.truetype(R+"/fonts/Anton-Regular.ttf",s)
def mont(s,w="SemiBold"):
    f=ImageFont.truetype(R+"/fonts/Montserrat.ttf",s)
    try: f.set_variation_by_name(w)
    except Exception: pass
    return f
logo=Image.open(R+"/brand/logo-on-dark.png").convert("RGBA"); logo=logo.crop(logo.getbbox())
logo=logo.resize((300,int(logo.height*300/logo.width)),Image.LANCZOS)
def cover(img,w,h,fx=0.5,fy=0.5):
    s=max(w/img.width,h/img.height); img=img.resize((int(img.width*s),int(img.height*s)),Image.LANCZOS)
    x=int((img.width-w)*fx); y=int((img.height-h)*fy); return img.crop((x,y,x+w,y+h))
def wrap(d,t,f,maxw):
    out=[];cur=""
    for w in t.split():
        if d.textlength((cur+" "+w).strip(),font=f)<=maxw: cur=(cur+" "+w).strip()
        else: out.append(cur);cur=w
    out.append(cur);return out
def footer(c,d):
    d.rectangle([0,H-130,W,H],fill=GREEN)
    c.paste(logo,(60,H-130+(130-logo.height)//2),logo)
    t="30-day money-back guarantee"; f=mont(30)
    d.text((W-60-d.textlength(t,font=f),H-130+48),t,font=f,fill=WHITE)
    d.text((W-60-d.textlength("AI-generated image",font=mont(20,"Medium")),12),"AI-generated image",font=mont(20,"Medium"),fill=WHITE) if False else None

# 1. five reasons
c=cover(Image.open(R+"/device-v2/stills/07-kit-hero-gel.png").convert("RGB"),W,H,0.5,0.5)
ov=Image.new("RGBA",(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov)
od.rectangle([0,0,W,840],fill=GREEN+(240,)); c=Image.alpha_composite(c.convert("RGBA"),ov).convert("RGB")
d=ImageDraw.Draw(c)
d.text((60,50),"5 REASONS NOT",font=anton(104),fill=WHITE)
d.text((60,160),"TO BUY THIS",font=anton(104),fill=LIME)
rs=["You want it overnight","You won't use it","You want the cheapest thing online","You want a miracle","You can't wait for delivery"]
y=310
for i,r in enumerate(rs,1):
    d.ellipse([60,y,116,y+56],fill=LIME); d.text((88,y+28),str(i),font=anton(36),fill=GREEN,anchor="mm")
    d.text((140,y+8),r,font=mont(38),fill=WHITE); y+=84
d.text((60,y+14),"Still here? 4 modes. Gel included.",font=mont(34,"Bold"),fill=LIME)
footer(c,d); c.save(OUT+"/ad1-5-reasons-4x5.png")

# 2. scam
c=Image.new("RGB",(W,H),GREEN)
photo=cover(Image.open(R+"/device-v2/stills/s6-sofa-screen.png").convert("RGB"),W,880,0.5,0.3)
c.paste(photo,(0,0)); d=ImageDraw.Draw(c)
d.text((60,905),"IS IT A SCAM?",font=anton(112),fill=WHITE)
t="Fair question. A real device, four modes, gel in the box and a 30-day money-back guarantee."
y=1070
for ln in wrap(d,t,mont(36),W-120): d.text((60,y),ln,font=mont(36),fill=SAGE); y+=50
footer(c,d); c.save(OUT+"/ad2-is-it-a-scam-4x5.png")

# 3. salon bill
c=cover(Image.open(R+"/device-v2/stills/03-flatlay.png").convert("RGB"),W,H,0.5,0.5)
ov=Image.new("RGBA",(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov); od.rectangle([0,0,W,430],fill=GREEN+(235,))
c=Image.alpha_composite(c.convert("RGBA"),ov).convert("RGB"); d=ImageDraw.Draw(c)
d.text((60,50),"ANOTHER SALON BILL?",font=anton(92),fill=WHITE)
d.text((60,160),"THE AT-HOME VERSION.",font=anton(92),fill=LIME)
for k,ln in enumerate(["Warm. Glow. Lift. Smooth.","Ten minutes, a few times a week."]): d.text((60,290+k*54),ln,font=mont(38),fill=SAGE)
footer(c,d); c.save(OUT+"/ad3-salon-bill-4x5.png")
print("ok")
