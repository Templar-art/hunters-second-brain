import cv2,json,numpy as np,sys
D='graphics/main/frames/f_%04d.png'; N=67
A=np.load('cadastre/A_sat2last.npy')
p=np.float32(json.load(open('cadastre/sat_polys.json'))['polys']['231RP110045'][:4])
q=cv2.transform(p[None],A)[0]  # 4K coords in last frame
# order: find front (street side = smallest x+y... street is top-left)
c=q.mean(0); s=(q-c)@np.float32([1,1])/np.sqrt(2)   # along lot axis toward canal
front=q[np.argsort(s)[:2]]; back=q[np.argsort(s)[2:]]
# kerb line (display coords x2.4)
k0=np.float32([420,330])*2.4; k1=np.float32([690,130])*2.4
def isect(a,b):  # line a->b with kerb
    d=b-a; e=k1-k0; M=np.array([d,-e]).T; t=np.linalg.solve(M,k0-a); return a+t[0]*d
nf=[]
for f in front:
    b=back[np.argmin(np.linalg.norm(back-f,axis=1))]; nf.append(isect(b,f))
nf=np.float32(nf); b2=np.float32([back[np.argmin(np.linalg.norm(back-f,axis=1))] for f in front])
poly=np.float32([nf[0],nf[1],b2[1],b2[0]])
print(poly)
sift=cv2.SIFT_create(4000); sc=0.4
def kd(i):
    g=cv2.cvtColor(cv2.imread(D%i),cv2.COLOR_BGR2GRAY); g=cv2.resize(g,None,fx=sc,fy=sc); return sift.detectAndCompute(g,None)
H={N:np.eye(3)}; prev=kd(N)
for i in range(N-1,0,-1):
    cur=kd(i); m=cv2.BFMatcher().knnMatch(cur[1],prev[1],k=2)
    g=[a for a,b in m if a.distance<0.75*b.distance]
    if len(g)<30: print('lost',i); break
    a=np.float32([cur[0][x.queryIdx].pt for x in g])/sc; b=np.float32([prev[0][x.trainIdx].pt for x in g])/sc
    h,mk=cv2.findHomography(a,b,cv2.RANSAC,4); H[i]=H[i+1]@h  # i -> N
    prev=cur
json.dump({i:cv2.perspectiveTransform(poly[None],np.linalg.inv(H[i]))[0].tolist() for i in H},open('graphics/out/outline_track.json','w'))
print('tracked',min(H))
