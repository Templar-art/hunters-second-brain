# Assembles the four ZED option boards from rooms/{option}-{nn}-{room}.png
import glob, sys
from PIL import Image, ImageDraw, ImageFont
F='/Users/10xhunter/Library/Fonts/'
O={'01':('WARM ORGANIC CONTEMPORARY','Ivory linen, smoked walnut and olive. Calm, earthy and timeless.',[('Warm ivory','#E9E2D6'),('Oatmeal','#D8D0C2'),('Smoked walnut','#4A3326'),('Travertine','#C9B79B'),('Eucalyptus olive','#6B7257'),('Aged brass','#9A7445')],(244,240,233)),
'02':('GALLERY STONE','Chalk plaster, honed travertine and sculptural curves. Quiet and architectural.',[('Chalk','#ECE8E1'),('Plaster greige','#D3CBBF'),('Honed travertine','#BFA98C'),('Smoked oak','#5C4A3B'),('Brushed bronze','#7A6650'),('Graphite','#3E3C38')],(246,244,240)),
'03':('SMOKED OAK SUITE','Espresso oak, cognac leather and smoked glass. A five-star hotel suite at home.',[('Soft linen','#E4DDD3'),('Mushroom','#A89A8A'),('Espresso oak','#3B2C22'),('Cognac leather','#8C5A3A'),('Smoked glass','#5A5550'),('Antique bronze','#7D6145')],(240,236,229)),
'04':('RIVIERA RESORT','Limewash, sand linen, natural oak and clay. Mediterranean resort living.',[('Limewash white','#F1ECE3'),('Sand linen','#DCCFBB'),('Travertine','#C8B392'),('Natural oak','#8A6A4C'),('Muted clay','#A9745A'),('Sage olive','#7E8467')],(247,244,238))}
R=['Living','Dining','Kitchen','Master Bedroom','Guest Bedroom','Study','Entry','Bathroom','Outdoor Lounge','Outdoor Dining']
W=4800; pad=120; gap=40; cw=(W-2*pad-4*gap)//5; ch=cw*2//3
ink=(42,40,37); mute=(110,104,96)
fT=ImageFont.truetype(F+'Poppins-Light.ttf',110); fS=ImageFont.truetype(F+'Poppins-Regular.ttf',48)
fC=ImageFont.truetype(F+'Poppins-Medium.ttf',34); fSw=ImageFont.truetype(F+'Poppins-Regular.ttf',32); fE=ImageFont.truetype(F+'Poppins-Regular.ttf',36)
def tr(d,xy,t,f,fill,track,anchor='l'):
    w=sum(d.textlength(c,font=f) for c in t)+track*(len(t)-1); x,y=xy
    if anchor=='c': x-=w/2
    for c in t: d.text((x,y),c,font=f,fill=fill); x+=d.textlength(c,font=f)+track
for o in (sys.argv[1:] or O):
    name,desc,sw,bg=O[o]
    c=Image.new('RGB',(W,3000),bg); d=ImageDraw.Draw(c); y=pad
    tr(d,(W/2,y),f'ZED  ·  OPTION {o}',fE,mute,14,'c'); y+=70
    tr(d,(W/2,y),name,fT,ink,22,'c'); y+=150
    d.text((W/2,y),desc,font=fS,fill=mute,anchor='ma'); y+=110
    sww=(W-2*pad-5*gap)//6
    for i,(n,h) in enumerate(sw):
        x=pad+i*(sww+gap); d.rectangle([x,y,x+sww,y+150],fill=h); tr(d,(x+sww/2,y+170),n.upper(),fSw,mute,6,'c')
    y+=300
    for i,f in enumerate(sorted(glob.glob(f'rooms/{o}-*.png'))):
        im=Image.open(f).convert('RGB'); im=im.resize((cw,int(im.height*cw/im.width)),Image.LANCZOS)
        if im.height>ch: t=(im.height-ch)//2; im=im.crop((0,t,cw,t+ch))
        x=pad+(i%5)*(cw+gap); yy=y+(i//5)*(ch+90+gap)
        c.paste(im,(x,yy)); tr(d,(x+cw/2,yy+ch+28),R[i].upper(),fC,ink,8,'c')
    c.crop((0,0,W,y+2*(ch+90)+pad)).save(f'boards-v2/zed-option-{o}.jpg',quality=92); print('built',o)
