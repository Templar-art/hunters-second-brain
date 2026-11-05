"""Find Your Stride run reel: tighten, punch-ins, grade, captions, hook. Usage: python3 build.py SRC TR.JSON OUTDIR"""
import json, subprocess, sys, os
SRC, TR, OUT = sys.argv[1:4]
os.makedirs(OUT, exist_ok=True)
FPS = 24000/1001
# (start, end, base zoom) in source seconds; talking-head segs alternate zoom to hide jump cuts
SEGS = [(0,13.9,1.0),(13.9,16.4,1.0),(19.0,26.62,1.0),(27.25,34.52,1.14),(35.05,38.7,1.0),
        (40.1,43.15,1.14),(43.55,46.72,1.0),(47.36,50.62,1.14),(51.2,57.0,1.0)]
def remap(t):
    acc=0
    for s,e,_ in SEGS:
        if s<=t<e: return acc+(t-s)
        acc+=e-s
    return None
GRADE="eq=contrast=1.07:saturation=1.18:gamma=0.98,colorbalance=rs=0.03:bs=-0.03:rm=0.02:bm=-0.02,unsharp=5:5:0.4"
fc=[]; 
for i,(s,e,z) in enumerate(SEGS):
    n=round((e-s)*FPS)
    push=f"{z}+0.05*on/{n}"   # slow push across every segment
    fc.append(f"[0:v:0]trim={s}:{e},setpts=PTS-STARTPTS,fps=24000/1001,scale=1080:1920,"
              f"zoompan=z='{push}':x='iw/2-iw/zoom/2':y='ih*0.42-ih/zoom*0.42':d=1:s=1080x1920:fps=24000/1001,{GRADE}[v{i}];")
    fc.append(f"[0:a:0]atrim={s}:{e},asetpts=PTS-STARTPTS,afade=t=in:d=0.04,afade=t=out:st={e-s-0.06}:d=0.06[a{i}];")
k=len(SEGS)
fc.append("".join(f"[v{i}][a{i}]" for i in range(k))+f"concat=n={k}:v=1:a=1[vc][ac];")
# captions: PIL-rendered alpha layer (this ffmpeg has no libass). 3-word chunks, active word blue, pop-in
from PIL import Image, ImageDraw, ImageFont
words=[(w['offsets']['from']/1000,w['text'].strip()) for w in json.load(open(TR))['transcription'] if w['text'].strip()]
ws=[(remap(a),w) for a,w in words if remap(a) is not None]
total=sum(e-s for s,e,_ in SEGS)
chunks=[]; cur=[]
for i,(t,w) in enumerate(ws):
    cur.append((t,w)); nxt=ws[i+1][0] if i+1<len(ws) else t+1
    if len(cur)==3 or w[-1] in ".,?!" or nxt-t>0.7: chunks.append(cur); cur=[]
if cur: chunks.append(cur)
CAP=[]  # (start,end,words,active_idx,chunk_start)
for ci,ch in enumerate(chunks):
    end_ch=min(chunks[ci+1][0][0] if ci+1<len(chunks) else total, ch[-1][0]+1.2)
    for wi,(t,w) in enumerate(ch):
        CAP.append((t, ch[wi+1][0] if wi+1<len(ch) else end_ch, [x.upper().strip(',.') for _,x in ch], wi, ch[0][0]))
FB=os.path.expanduser('~/Library/Fonts/Poppins-Black.ttf')
BLUE=(255,255,255,255)  # client job (Ashley Cooper Construction): no 10x blue; active word = white, others dimmed
def draw_line(img, parts, y, size, active=None, scale=1.0):
    f=ImageFont.truetype(FB, int(size*scale)); d=ImageDraw.Draw(img)
    sp=f.getlength(' '); widths=[f.getlength(p) for p in parts]; W=sum(widths)+sp*(len(parts)-1)
    x=(1080-W)/2
    for i,(p,w) in enumerate(zip(parts,widths)):
        col=BLUE if (active is None or i in active) else (255,255,255,170)
        d.text((x+3,y+4),p,font=f,fill=(0,0,0,140),anchor='lm')
        d.text((x,y),p,font=f,fill=col,anchor='lm',stroke_width=6,stroke_fill=(0,0,0,255))
        x+=w+sp
HOOK=[(0.1,2.9,["42.2 KM FOR"],None),(0.1,2.9,["FIND","YOUR","FEET"],{0,1,2})]
fr=f"{OUT}/capframes"; os.makedirs(fr,exist_ok=True)
N=0 if os.environ.get("CLEAN") else round(total*FPS)
for n in range(N):
    t=n/FPS; img=Image.new('RGBA',(1080,1920),(0,0,0,0))
    for s,e,parts,ai,cs in CAP:
        if s<=t<e:
            pop=min(1.0,0.9+(t-cs)/0.09*0.1)
            draw_line(img,parts,1400,80,{ai},pop)
    if t<2.9:
        a=min(1,(t-0.1)/0.15) if t>0.1 else 0
        if a>0:
            draw_line(img,["42.2 KM FOR"],230,72); draw_line(img,["FIND","YOUR","FEET"],320,92,{0,1,2})
    if t>total-5.6:
        draw_line(img,["SPONSOR US"],230,72); draw_line(img,["LINK","BELOW"],320,92,{0,1})
    img.save(f"{fr}/{n:05d}.png")
None if os.environ.get("CLEAN") else subprocess.run(["ffmpeg","-v","error","-y","-framerate","24000/1001","-i",f"{fr}/%05d.png","-c:v","qtrle",f"{OUT}/caps.mov"],check=True)
fc.append(("[vc]null[vo];" if os.environ.get("CLEAN") else "[vc][1:v]overlay=0:0:format=auto[vo];")+f"[ac]highpass=f=85,afftdn=nr=10:nf=-45,equalizer=f=250:t=q:w=1.2:g=-2,equalizer=f=3500:t=q:w=1.5:g=2,deesser=i=0.3,acompressor=threshold=-20dB:ratio=2.5:attack=15:release=200:makeup=3,loudnorm=I=-14:TP=-1.5:LRA=7[ao]")
subprocess.run(["ffmpeg","-v","error","-y","-i",SRC,"-i",f"{OUT}/caps.mov","-filter_complex","".join(fc),"-map","[vo]","-map","[ao]",
  "-c:v","libx264","-crf","17","-preset","medium","-pix_fmt","yuv420p","-c:a","aac","-b:a","256k","-ar","48000","-movflags","+faststart",f"{OUT}/"+("clean.mp4" if os.environ.get("CLEAN") else "picture.mp4")],check=True)
print("total",round(total,2))
