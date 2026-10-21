import sys
from PIL import Image, ImageDraw
C='shots/closeups/'
J=[('01_tail_light',C+'rear_push/0040.png',(1180,250,1700,640)),
('02_rear_badge_plate',C+'rear_push/0100.png',(380,0,1540,780)),
('03_front_wheel_headlight',C+'wheel_track/0030.png',(1060,140,1920,860)),
('04_arch_intake',C+'wheel_track/0070.png',(560,120,1840,1000)),
('05_front_badge_plate','hero_golden.png',(1460,560,1720,760)),
('06_mirror_window',C+'profile_glide/0025.png',(1100,120,1900,620)),
('07_hero_headlight','hero_golden.png',(1060,490,1420,680)),
('08_hero_front_wheel','hero_golden.png',(790,500,1060,830))]
out=[]
for n,p,b in J:
    im=Image.open(p).convert('RGB'); out.append((n,im.crop(b)))
if sys.argv[1:]==['save']:  # run from projects/lambo-huracan
    for n,c in out:
        if c.width<1600: c=c.resize((1600,round(c.height*1600/c.width)),Image.LANCZOS)
        c.save(f'details/{n}.jpg',quality=95)
else:
    s=Image.new('RGB',(4*480,2*320))
    for k,(n,c) in enumerate(out):
        t=c.copy(); t.thumbnail((480,320)); ImageDraw.Draw(t).text((4,4),n,fill=(255,255,0)); s.paste(t,((k%4)*480,(k//4)*320))
    s.save(sys.argv[1])
