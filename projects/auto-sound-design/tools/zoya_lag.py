import numpy as np, librosa, sys
SR=22050; y,_=librosa.load(sys.argv[1],sr=SR)
a,b=95.13,179.97
oe=librosa.onset.onset_strength(y=y,sr=SR,hop_length=64)
def seg(t): s=int((t-4)*SR/64); return oe[s:s+int(4*SR/64)]   # 4 s before each point
for side,t in (("before",0),):
    A=seg(a); best=[]
    for lag in np.arange(-0.15,0.15,64/SR):
        Bv=seg(b+lag); n=min(len(A),len(Bv)); best.append((np.corrcoef(A[:n],Bv[:n])[0,1],lag))
    best.sort(reverse=True); print("best lag %.4f s corr %.3f ; lag0 corr %.3f"%(best[0][1],best[0][0],[c for c,l in best if abs(l)<64/SR/2][0]))
