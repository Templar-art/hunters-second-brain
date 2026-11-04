import sys, numpy as np, librosa
F,V,NV,BT=sys.argv[1:5]; SR=22050; g=np.loadtxt(BT); B=float(np.mean(np.diff(g)))
y,_=librosa.load(F,sr=SR); v,_=librosa.load(V,sr=SR); nv,_=librosa.load(NV,sr=SR)
hop=128
C=librosa.feature.chroma_cqt(y=nv,sr=SR,hop_length=hop); M=librosa.feature.melspectrogram(y=nv,sr=SR,hop_length=hop,n_mels=48); M=librosa.power_to_db(M)
oe=librosa.onset.onset_strength(y=y,sr=SR,hop_length=hop)
fr=lambda t:int(t*SR/hop); W=fr(0)+int(4*B*SR/hop)  # 4 beats either side
def cos(a,b): return float(np.sum(a*b)/(np.linalg.norm(a)*np.linalg.norm(b)+1e-9))
def vdb(t): x=v[int((t-0.1)*SR):int((t+0.1)*SR)]; return 20*np.log10(np.sqrt(np.mean(x**2))+1e-9)
START=g[128]; END=len(y)/SR; res=[]
for i in range(164,352):
  for j in range(i+16,412):
    L=(g[i]-START)+(END-g[j])
    if not 60<=L<=95: continue
    if (j-i)%4: continue
    a,b=fr(g[i]),fr(g[j])
    if a-W<0 or b+W>C.shape[1]: continue
    # best lag in +-50ms on onset env
    best=(-9,0)
    for d in range(-40,41):
      oa=oe[a-W:a+W]; ob=oe[b+d-W:b+d+W]; c=np.corrcoef(oa,ob)[0,1]
      if c>best[0]: best=(c,d)
    d=best[1]
    ch=cos(C[:,a-W:a+W],C[:,b+d-W:b+d+W]); me=np.corrcoef(M[:,a-W:a+W].ravel(),M[:,b+d-W:b+d+W].ravel())[0,1]
    vo=max(vdb(g[i]),vdb(g[j]+d*hop/SR))
    sc=0.35*ch+0.35*me+0.3*best[0]-(0.15 if vo>-30 else 0)
    res.append((sc,ch,me,best[0],d*hop/SR,i,j,g[i],g[j],L,vo))
res.sort(reverse=True)
for r in res[:12]: print("sc %.3f ch %.3f mel %.3f on %.3f lag %+.3f  b%d->b%d  %.2f->%.2f  len %.1f voc %.0f"%r)
