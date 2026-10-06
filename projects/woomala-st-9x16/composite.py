import sys
from PIL import Image
import numpy as np
def comp(i):
    ai=Image.open(f'ai-raw/{i:02d}.png').convert('RGB'); o=Image.open(f'clean/{i:02d}.png').convert('RGB')
    # find original position inside AI frame (search x and y at AI scale)
    A=np.asarray(ai).astype(float)
    s=min(ai.width/o.width, ai.height/o.height)
    best=None
    for sc in np.linspace(s*0.97,s*1.0001,12):
        w,h=round(o.width*sc),round(o.height*sc)
        if w>ai.width or h>ai.height: continue
        O=np.asarray(o.resize((w,h),Image.LANCZOS)).astype(float)
        for y in range(0,ai.height-h+1,2):
            for x in range(0,ai.width-w+1,2):
                e=np.abs(A[y:y+h:4,x:x+w:4]-O[::4,::4]).mean()
                if best is None or e<best[0]: best=(e,sc,x,y)
    e,sc,x,y=best
    k=1/sc  # AI px -> original px
    big=ai.resize((round(ai.width*k),round(ai.height*k)),Image.LANCZOS)
    X,Y=round(x*k),round(y*k)
    F=10
    m=np.ones((o.height,o.width),float)
    r=np.linspace(0,1,F)
    if Y>0: m[:F]*=r[:,None]
    if Y+o.height<big.height: m[-F:]*=r[::-1][:,None]
    if X>0: m[:,:F]*=r[None,:]
    if X+o.width<big.width: m[:,-F:]*=r[::-1][None,:]
    big.paste(o,(X,Y),Image.fromarray((m*255).astype('uint8')))
    # trim to exact 9:16
    W=big.width; H=round(W*16/9)
    if H>big.height: H=big.height; W=round(H*9/16)
    big=big.crop(((big.width-W)//2,(big.height-H)//2,(big.width-W)//2+W,(big.height-H)//2+H))
    big.resize((1080,1920),Image.LANCZOS).save(f'final/{i:02d}.jpg',quality=95)
    print(i,'err',round(e,2),'scale',round(sc,4),'pos',X,Y,'canvas',big.size)
for a in sys.argv[1:]: comp(int(a))
