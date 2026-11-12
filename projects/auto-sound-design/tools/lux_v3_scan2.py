import numpy as np, librosa
F="/Users/10xhunter/Downloads/Ryan Taubert - Lux.mp3"; SR=22050; H=128
y,_=librosa.load(F,sr=SR); bt=np.loadtxt("lux_bt.txt")
# 1) where the lift and the big hit really start: steepest rise of 20 ms RMS (dB)
r=librosa.feature.rms(y=y,frame_length=1024,hop_length=H)[0]; rt=librosa.times_like(r,sr=SR,hop_length=H); db=20*np.log10(r+1e-6)
for name,x in (("lift",18.12),("hit",64.11),("final",159.63),("break",141.94)):
    m=(rt>x-0.5)&(rt<x+0.5); k=int(0.05*SR/H); d=db[k:]-db[:-k]; mm=m[:-k]
    i=np.argmax(np.where(mm,d,-99)); print(name,"grid",x,"steepest rise at",round(rt[i]+0.025,3),"rise dB",round(d[i],1), "level before/after", round(db[i-40:i].mean(),1), round(db[i+k:i+k+80].mean(),1))
# 2) join 2 by spectrum: for out points a in the loud section, best in point b in the final section
M=librosa.power_to_db(librosa.feature.melspectrogram(y=y,sr=SR,hop_length=H,n_mels=80,n_fft=2048),ref=1.0)
M=M-M.mean(1,keepdims=True); f=lambda x:int(round(x*SR/H))
W=f(4.0)
def score(a,b):
    A=M[:,f(a)-W:f(a)+W]; Bm=M[:,f(b)-W:f(b)+W]; return np.corrcoef(A.ravel(),Bm.ravel())[0,1]
out=[]
for a in np.arange(84.0,100.0,0.4422*4):
    best=max((score(a,b),b) for b in np.arange(150.0,173.0,0.05))
    b0=best[1]; best=max((score(a,b),b) for b in np.arange(b0-0.06,b0+0.06,H/SR))
    out.append((round(best[0],3),round(a,2),round(best[1],3)))
for o in sorted(out): print(o)
print("--- join 1: strings (a) -> build before hit (b)")
for a in np.arange(26.0,35.6,0.4422*2):
    best=max((score(a,b),b) for b in np.arange(52.0,64.0,0.05)); b0=best[1]
    best=max((score(a,b),b) for b in np.arange(b0-0.06,b0+0.06,H/SR))
    print(round(best[0],3),round(a,2),round(best[1],3),"offset",round(best[1]-a,3))
print("--- join 2 along the 76.797 line; level (dB) around a and b")
lv=lambda x:round(db[f(x)-40:f(x)+40].mean(),1)
for a in np.arange(84.0,101.5,0.4422):
    print(round(a,2),round(score(a,a+76.797),3),lv(a),lv(a+76.797))
