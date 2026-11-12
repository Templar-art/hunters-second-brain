import numpy as np, librosa
from scipy.signal import butter, sosfilt, correlate
F="/Users/10xhunter/Downloads/Ryan Taubert - Lux.mp3"; SR=22050
y,_=librosa.load(F,sr=SR)
def env(x0,x1,step=0.05):
    lo=sosfilt(butter(4,150,"low",fs=SR,output="sos"),y)
    for t in np.arange(x0,x1,step):
        a,b=int(t*SR),int((t+step)*SR); d=lambda z:round(20*np.log10(np.sqrt(np.mean(z[a:b]**2))+1e-6),1)
        print(round(t,2),d(y),d(lo))
print("lift"); env(17.8,18.7); print("hit"); env(63.8,64.8); print("end"); env(177.2,178.6,0.1)
# join 2: band-limited waveform xcorr around a=99.5 vs b=a+76.797
bp=sosfilt(butter(4,[200,4000],"band",fs=SR,output="sos"),y)
for a in (98.6,99.5,100.3):
    A=bp[int((a-1.5)*SR):int((a+1.5)*SR)]; c0=int((a+76.797-1.5-0.2)*SR); Bx=bp[c0:c0+len(A)+int(0.4*SR)]
    e=lambda z:np.abs(z)  # envelope corr (phase-agnostic)
    ea=np.convolve(e(A),np.ones(64)/64,"same"); eb=np.convolve(e(Bx),np.ones(64)/64,"same")
    c=correlate(eb-eb.mean(),ea-ea.mean(),"valid"); k=np.argmax(c); n=len(ea)
    cc=np.corrcoef(ea,eb[k:k+n])[0,1]
    w=correlate(Bx,A,"valid"); kw=np.argmax(np.abs(w)); wc=np.corrcoef(A,Bx[kw:kw+n])[0,1]
    print("a",a,"env lag ms",round((k/SR-0.2)*1000,1),"env corr",round(cc,3),"| waveform lag ms",round((kw/SR-0.2)*1000,1),"corr",round(wc,3))
