import numpy as np, librosa
F="/Users/10xhunter/Downloads/Ryan Taubert - Lux.mp3"; SR=44100; H=64
y,_=librosa.load(F,sr=SR); bt=np.loadtxt("lux_bt.txt"); B=bt[1]-bt[0]
o=librosa.onset.onset_strength(y=y,sr=SR,hop_length=H); t=librosa.times_like(o,sr=SR,hop_length=H)
def snap(x,w=0.09):
    m=(t>x-w)&(t<x+w); return t[m][np.argmax(o[m])], o[m].max()/ (np.median(o)+1e-9)
print("B",round(B,4))
for b in (24,32,40,64,72,144):
    s,st=snap(bt[b]); print("beat",b,"grid",round(bt[b],3),"onset",round(s,3),"off ms",round((s-bt[b])*1000),"strength",round(st,1))
def phase(i,n=16,sign=1):
    d=[]
    for k in range(n):
        s,st=snap(bt[i+sign*k],0.07)
        if st>4: d.append(s-bt[i+sign*k])
    return (np.median(d),len(d),np.std(d)) if d else (0,0,0)
def xc(a,b,w=6.0,r=0.3):
    fa=lambda x:o[int(x*SR/H):int((x+w)*SR/H)]
    oa=fa(a); best=(-9,0)
    for k in range(-int(r*SR/H),int(r*SR/H)+1,2):
        ob=fa(b+k*H/SR); n=min(len(oa),len(ob)); c=np.corrcoef(oa[:n],ob[:n])[0,1]
        if c>best[0]: best=(c,k*H/SR)
    return best
y2,_=librosa.load(F,sr=22050); C=librosa.feature.chroma_cqt(y=y2,sr=22050,hop_length=512); M=librosa.power_to_db(librosa.feature.melspectrogram(y=y2,sr=22050,hop_length=512,n_mels=64))
fr=lambda x:int(x*22050/512)
def sim(X,a,b,w): return np.corrcoef(X[:,fr(a):fr(a)+w].ravel(),X[:,fr(b):fr(b)+w].ravel())[0,1]
res=[]
for i in range(176,249,8):
    for j in range(336,381,4):
        pa=phase(i-1,16,-1); pb=phase(j,16,1); c,l=xc(bt[i]-3,bt[j]-3)   # compare what precedes+follows
        w=fr(bt[8])-fr(bt[0]); a0=bt[i]-4*B
        ch=sim(C,a0,bt[j]-4*B,w); ml=sim(M,a0,bt[j]-4*B,w)
        res.append((0.5*ch+0.5*ml,i,j,round(ch,2),round(ml,2),"xc",round(c,2),round(l*1000),"phase ms",round((pb[0]-pa[0])*1000),pa[1],pb[1]))
for r in sorted(res)[-12:]: print(r)
