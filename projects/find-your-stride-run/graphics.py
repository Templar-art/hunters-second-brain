"""Captions + graphics overlay for the run reel (cut-timeline transcript). Usage: python3 graphics.py CLEAN.mp4 CUT.json MUSIC OUT.mp4"""
import json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
CLEAN, TR, MUSIC, OUTF = sys.argv[1:5]
FPS=24000/1001; W,H=1080,1920
dur=float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",CLEAN]))
FB=os.path.expanduser('~/Library/Fonts/Poppins-Black.ttf'); FS=os.path.expanduser('~/Library/Fonts/Poppins-SemiBold.ttf')
# words; spread bunched timestamps (whisper stacks words after a pause) by character length
ws=[[s['offsets']['from']/1000,s['text'].strip()] for s in json.load(open(TR))['transcription'] if s['text'].strip()]
ws.insert(0,[0.0,"Hey,"]); ws[1][0]=max(ws[1][0],0.35)
i=0
while i<len(ws):
    j=i
    while j+1<len(ws) and ws[j+1][0]-ws[i][0]<0.06: j+=1
    if j>i:
        end=ws[j+1][0] if j+1<len(ws) else ws[i][0]+1.5
        span=min(end-ws[i][0], 0.32*(j-i+1)); L=[len(ws[k][1]) for k in range(i,j+1)]; acc=0
        for k in range(i,j+1): ws[k][0]=ws[i][0]+span*acc/sum(L); acc+=L[k-i]
    i=j+1
LEAD=0.04  # show each word a hair early so it lands on the syllable
ws=[(max(0,t-LEAD),w) for t,w in ws]
chunks=[];cur=[]
for i,(t,w) in enumerate(ws):
    cur.append((t,w)); nxt=ws[i+1][0] if i+1<len(ws) else t+1
    if len(cur)==3 or w[-1] in ".,?!" or nxt-t>0.6: chunks.append(cur); cur=[]
if cur: chunks.append(cur)
CAP=[]
for ci,ch in enumerate(chunks):
    end_ch=min(chunks[ci+1][0][0] if ci+1<len(chunks) else dur, ch[-1][0]+0.9)
    for wi,(t,w) in enumerate(ch):
        CAP.append((t, ch[wi+1][0] if wi+1<len(ch) else end_ch, [x.upper().strip(',.') for _,x in ch], wi, ch[0][0]))
WHITE=(255,255,255,255); DIM=(255,255,255,165)
def font_fit(path, size, parts, maxw):
    while True:
        f=ImageFont.truetype(path,size); sp=f.getlength(' ')
        tw=sum(f.getlength(p) for p in parts)+sp*(len(parts)-1)
        if tw<=maxw or size<40: return f,tw,sp
        size-=2
def line(img, parts, y, size, active=None, scale=1.0, alpha=1.0, path=FB, maxw=840, track=0):
    f,tw,sp=font_fit(path,int(size*scale),parts,maxw); d=ImageDraw.Draw(img); x=(W-tw)/2
    for i,p in enumerate(parts):
        c=WHITE if (active is None or i in active) else DIM
        c=c[:3]+(int(c[3]*alpha),)
        d.text((x+3,y+4),p,font=f,fill=(0,0,0,int(120*alpha)),anchor='lm')
        d.text((x,y),p,font=f,fill=c,anchor='lm',stroke_width=max(3,int(f.size*0.07)),stroke_fill=(0,0,0,int(255*alpha)))
        x+=f.getlength(p)+sp
def ease(t,a,b,d=0.22):  # 0..1 in, 1..0 out
    if t<a or t>b: return 0
    return max(0,min(1,(t-a)/d,(b-t)/d))
def card(img,t,a,b,small,big):  # two-line top title card, slides up + fades
    e=ease(t,a,b)
    if e<=0: return
    off=int((1-e)*30)
    line(img,[small],215+off,56,alpha=e,path=FS); line(img,big.split(),300+off,92,alpha=e)
def tag(img,t,a,b,name,cx,cy):  # name pill
    e=ease(t,a,b,0.18)
    if e<=0: return
    f=ImageFont.truetype(FB,44); tw=f.getlength(name); pad=26
    pill=Image.new('RGBA',img.size,(0,0,0,0)); d=ImageDraw.Draw(pill)
    d.rounded_rectangle((cx-tw/2-pad,cy-38,cx+tw/2+pad,cy+38),radius=38,fill=(255,255,255,int(235*e)))
    d.text((cx,cy),name,font=f,fill=(17,17,17,int(255*e)),anchor='mm')
    img.alpha_composite(pill)
CARDS=[(0.0,3.0,"42.2 KM FOR","FIND YOUR FEET"),
       (6.9,10.3,"QUEENSTOWN MARATHON","14 NOVEMBER"),
       (17.9,23.2,"TOMMY HERSCHEL","MENTAL HEALTH WORKSHOPS"),
       (41.3,44.3,"EVERY DOLLAR GETS TOMMY INTO","MORE SCHOOLS")]
END=(44.6,dur+1,"SPONSOR US","LINK BELOW")
# soft top/bottom gradients so white type reads over sky
grad=Image.new('RGBA',(W,H),(0,0,0,0)); g=ImageDraw.Draw(grad)
for y in range(460): g.line([(0,y),(W,y)],fill=(0,0,0,int(95*(1-y/460)**1.6)))
fr="out/gfxframes"; os.makedirs(fr,exist_ok=True)
for n in range(round(dur*FPS)):
    t=n/FPS; img=Image.new('RGBA',(W,H),(0,0,0,0))
    if any(ease(t,a,b)>0 for a,b,*_ in CARDS+[END]): img.alpha_composite(grad)
    for c in CARDS+[END]: card(img,t,*c)
    if ease(t,END[0],END[1])>0:  # bouncing arrow under end card
        e=ease(t,END[0],END[1]); import math; y=410+12*math.sin((t-END[0])*6)
        d=ImageDraw.Draw(img); d.polygon([(W/2-26,y),(W/2+26,y),(W/2,y+30)],fill=(255,255,255,int(255*e)),outline=(0,0,0,int(255*e)))
    tag(img,t,0.15,2.7,"EVERETT",290,1000); tag(img,t,1.1,3.3,"ALEX",790,1000)
    for s,e,parts,ai,cs in CAP:
        if s<=t<e: line(img,parts,1230,84,{ai},min(1.0,0.9+(t-cs)/0.08*0.1))
    img.save(f"{fr}/{n:05d}.png")
subprocess.run(["ffmpeg","-v","error","-y","-framerate","24000/1001","-i",f"{fr}/%05d.png","-c:v","qtrle","out/gfx.mov"],check=True)
subprocess.run(["ffmpeg","-v","error","-y","-i",CLEAN,"-i","out/gfx.mov","-i",MUSIC,"-filter_complex",
 "[0:v][1:v]overlay=0:0:format=auto[v];"
 f"[2:a]atrim=0:{dur},asetpts=PTS-STARTPTS,aresample=48000,highpass=f=60,loudnorm=I=-16:LRA=5,volume=-9dB,afade=t=in:d=1.5,afade=t=out:st={dur-3.4}:d=3.4[m];"
 "[0:a]asplit[vo][key];[m][key]sidechaincompress=threshold=0.04:ratio=4:attack=40:release=700[md];[vo][md]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=7[a]",
 "-map","[v]","-map","[a]","-c:v","libx264","-crf","16","-preset","slow","-pix_fmt","yuv420p","-c:a","aac","-b:a","256k","-ar","48000","-movflags","+faststart",OUTF],check=True)
