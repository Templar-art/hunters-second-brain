import cv2,json,numpy as np,os
T={int(k):np.float32(v) for k,v in json.load(open('graphics/out/outline_track.json')).items()}
os.makedirs('graphics/out/ol',exist_ok=True);os.makedirs('graphics/out/olp',exist_ok=True)
S0,DUR,W,SS=22,14,21,4
def ease(t):return 1-(1-t)**3
for i in range(1,68):
    im=np.zeros((2160*1,3840,4),np.uint8)
    if i>=S0:
        t=ease(min(1,(i-S0+1)/DUR)); P=T[i]; pts=np.vstack([P,P[:1]])
        L=np.linalg.norm(np.diff(pts,axis=0),axis=1); tot=L.sum()*t; path=[pts[0]]
        for a,b,l in zip(pts[:-1],pts[1:],L):
            if tot<=0:break
            u=min(1,tot/l); path.append(a+(b-a)*u); tot-=l
        big=np.zeros((2160*SS//2,3840*SS//2),np.uint8)
        cv2.polylines(big,[(np.float32(path)*SS/2*8).astype(np.int32)],False,255,W*SS//2,cv2.LINE_AA,shift=3)
        a=cv2.resize(big,(3840,2160),interpolation=cv2.INTER_AREA)
        for p in path: pass
        im[...,:3]=255; im[...,3]=a
    cv2.imwrite('graphics/out/ol/o_%04d.png'%i,im)
    f=cv2.imread('graphics/main/frames/f_%04d.png'%i).astype(np.float32); al=im[...,3:4]/255.
    cv2.imwrite('graphics/out/olp/p_%04d.jpg'%i,(f*(1-al)+255*al).astype(np.uint8))
