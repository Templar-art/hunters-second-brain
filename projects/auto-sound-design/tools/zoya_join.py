import sys, numpy as np, librosa
F,V,BT=sys.argv[1:4]; SR=22050; g=np.loadtxt(BT)
y,_=librosa.load(F,sr=SR); v,_=librosa.load(V,sr=SR)
C=librosa.feature.chroma_cqt(y=y,sr=SR,hop_length=512); ct=librosa.times_like(C,sr=SR,hop_length=512)
oe=librosa.onset.onset_strength(y=y,sr=SR,hop_length=512)
def win(M,a,b): return M[...,(ct>=a)&(ct<b)]
def vdb(t,w=0.25): x=v[int((t-w)*SR):int((t+w)*SR)]; return 20*np.log10(np.sqrt(np.mean(x**2))+1e-9)
def mdb(t,w=0.5): x=y[int((t-w)*SR):int((t+w)*SR)]; return 20*np.log10(np.sqrt(np.mean(x**2))+1e-9)
START=g[128]; END=len(y)/SR; out=[]
for i in range(164,260,4):          # join-out beat (after drop at 160)
  for j in range(352,412,4):        # join-in beat in drop 2
    L=(g[i]-START)+(END-g[j])
    if not 55<=L<=66: continue
    B=g[4]-g[0]
    a=win(C,g[i]-2*B,g[i]+2*B); b=win(C,g[j]-2*B,g[j]+2*B); n=min(a.shape[1],b.shape[1])
    ch=np.mean(np.sum(a[:,:n]*b[:,:n],0)/(np.linalg.norm(a[:,:n],axis=0)*np.linalg.norm(b[:,:n],axis=0)+1e-9))
    oa=win(oe,g[i]-2*B,g[i]+2*B); ob=win(oe,g[j]-2*B,g[j]+2*B); n=min(len(oa),len(ob))
    oc=np.corrcoef(oa[:n],ob[:n])[0,1]
    out.append((0.6*ch+0.4*oc,ch,oc,i,j,g[i],g[j],L,vdb(g[i]),vdb(g[j]),mdb(g[i])-mdb(g[j])))
out.sort(reverse=True)
for r in out[:15]: print("score %.3f ch %.3f on %.3f  beat %d->%d  %.2f->%.2f  len %.1f  voc %.0f/%.0f  lvlΔ %.1f"%r)
