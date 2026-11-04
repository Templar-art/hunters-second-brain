import sys, numpy as np, librosa
F=sys.argv[1]; V=sys.argv[2]; SR=22050
y,_=librosa.load(F,sr=SR); v,_=librosa.load(V,sr=SR)
oenv=librosa.onset.onset_strength(y=y,sr=SR,hop_length=256)
tempo,bt=librosa.beat.beat_track(onset_envelope=oenv,sr=SR,hop_length=256,units='time')
# snap each beat to local onset peak then refit
ot=librosa.times_like(oenv,sr=SR,hop_length=256); sn=[]
for b in bt:
    m=(ot>b-0.07)&(ot<b+0.07); sn.append(ot[m][np.argmax(oenv[m])] if m.any() else b)
k=np.arange(len(sn)); p=np.polyfit(k,sn,1); res=np.array(sn)-np.polyval(p,k)
ok=np.abs(res)<0.04; p=np.polyfit(k[ok],np.array(sn)[ok],1); g=np.polyval(p,k)
np.savetxt(sys.argv[3],g,fmt="%.4f")
print("tempo",float(np.atleast_1d(tempo)[0]),"refit bpm",round(60/p[0],2),"beats",len(g),"first",round(g[0],3))
db=lambda x:20*np.log10(np.sqrt(np.mean(x**2))+1e-9)
for i in range(0,len(g)-4,4):
    a,b=int(g[i]*SR),int(g[i+4]*SR)
    print(f"bar{i//4:3d} beat{i:3d} {g[i]:7.2f}s mix{db(y[a:b]):6.1f} voc{db(v[a:b]):6.1f}")
