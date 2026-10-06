import sys
from PIL import Image
import numpy as np
def gray(im): return np.asarray(im.convert('L')).astype(np.float32)
def align(ai,o):
    # coarse: AI at width 384
    S=384/ai.width; A=gray(ai.resize((384,round(ai.height*S)),Image.BILINEAR))
    best=None
    for fw in np.linspace(0.70,1.0,31):   # original width as fraction of AI width
        w=round(384*fw); h=round(o.height*w/o.width)
        if h>A.shape[0]: continue
        O=gray(o.resize((w,h),Image.BILINEAR)); O-=O.mean()
        for y in range(0,A.shape[0]-h+1,2):
            for x in range(0,384-w+1,2):
                P=A[y:y+h,x:x+w]; e=np.abs((P-P.mean())-O).mean()
                if best is None or e<best[0]: best=(e,fw,x,y)
    e,fw,x,y=best
    # refine at mid res (width 1024)
    S2=1024/ai.width; A2=gray(ai.resize((1024,round(ai.height*S2)),Image.BILINEAR))
    best2=None
    for w in range(round(1024*fw)-12,round(1024*fw)+13,2):
        if w>1024: continue
        h=round(o.height*w/o.width); O=gray(o.resize((w,h),Image.BILINEAR)); O-=O.mean()
        cx,cy=round(x/384*1024),round(y/384*1024)
        for yy in range(max(0,cy-8),min(A2.shape[0]-h,cy+8)+1):
            for xx in range(max(0,cx-8),min(1024-w,cx+8)+1):
                P=A2[yy:yy+h:3,xx:xx+w:3]; e2=np.abs((P-P.mean())-O[::3,::3]).mean()
                if best2 is None or e2<best2[0]: best2=(e2,w,xx,yy)
    e2,w,xx,yy=best2
    return e2, w/1024, xx/1024, yy/1024  # fractions of AI width
def comp(i,src='nbp'):
    ai=Image.open(f'{src}/{i:02d}.png').convert('RGB'); o=Image.open(f'clean/{i:02d}.png').convert('RGB')
    e,fw,fx,fy=align(ai,o)
    k=o.width/(fw*ai.width)   # scale AI so original lands 1:1
    big=ai.resize((round(ai.width*k),round(ai.height*k)),Image.LANCZOS)
    X,Y=round(fx*big.width),round(fy*big.width)
    F=int(__import__("os").environ.get("FEATHER","16")); m=np.ones((o.height,o.width),np.float32); r=np.linspace(0,1,F)
    if Y>0: m[:F]*=r[:,None]
    if Y+o.height<big.height: m[-F:]*=r[::-1][:,None]
    if X>0: m[:,:F]*=r[None,:]
    if X+o.width<big.width: m[:,-F:]*=r[::-1][None,:]
    big.paste(o,(X,Y),Image.fromarray((m*255).astype('uint8')))
    W=big.width; H=round(W*16/9)
    if H>big.height: H=big.height; W=round(H*9/16)
    l=(big.width-W)//2; t=(big.height-H)//2
    big=big.crop((l,t,l+W,t+H))
    big.save(f'final/{i:02d}_full.jpg',quality=95)
    big.resize((1080,1920),Image.LANCZOS).save(f'final/{i:02d}.jpg',quality=95)
    print(i,'err',round(float(e),2),'origW/aiW',round(float(fw),3),'k',round(k,3),'pos',X,Y,'out',big.size,flush=True)
for a in sys.argv[1:]: comp(int(a))
