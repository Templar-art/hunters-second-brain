import librosa,numpy as np,soundfile as sf
SR=48000
F="/Users/10xhunter/Downloads/Austin Snell - Wildfire (Visualizer).mp3"
NV="/private/tmp/claude-502/-Users-10xhunter-Documents-Hunters-Second-Brain/a9457b91-92f8-41fe-9b10-939264c376f9/scratchpad/demucs/htdemucs/Austin Snell - Wildfire (Visualizer)/no_vocals.wav"
y,_=librosa.load(F,sr=SR,mono=False); nv,_=librosa.load(NV,sr=SR,mono=False)
def s(a,b,src=None):
    src=y if src is None else src
    return src[:,int(a*SR):int(b*SR)].copy()
intro=s(2.40,8.24); L=4.64; n=int(L*SR); J=140.32; GAP=139.35
pre=s(J-L,J,nv)[:,:n]; full=s(J-L,J)[:,:n]; n=min(n,pre.shape[1],full.shape[1]); pre,full=pre[:,:n],full[:,:n]
k=int((GAP-(J-L))*SR); bl=int(0.12*SR)
w=np.zeros(n); w[k:k+bl]=np.linspace(0,1,bl); w[k+bl:]=1
pre=pre*(1-w)+full*w
t=np.linspace(0,1,n); fin=np.sin(t**1.6*np.pi/2); fout=np.cos(t*np.pi/2)
intro[:,-n:]=intro[:,-n:]*fout+pre*fin
mix=np.concatenate([intro,s(J,156.78)],axis=1)
m=int(0.3*SR); tt=np.linspace(0,np.pi/2,m); nxt=s(175.61-0.3,184.5)
mix[:,-m:]=mix[:,-m:]*np.cos(tt)+nxt[:,:m]*np.sin(tt); mix=np.concatenate([mix,nxt[:,m:]],axis=1)
f=int(1.0*SR); mix[:,-f:]*=np.cos(np.linspace(0,np.pi/2,f))**2; mix[:,:480]*=np.linspace(0,1,480)
sf.write("output/wildfire-reel/Wildfire_reel.wav",mix.T,SR,subtype="PCM_24")
mm=mix.mean(0);h=SR//2
print(round(mix.shape[1]/SR,2),"s");print(" ".join(f"{i/2:.1f}:{20*np.log10(np.sqrt(np.mean(mm[i*h:(i+1)*h]**2))+1e-9):.0f}" for i in range(len(mm)//h)))
