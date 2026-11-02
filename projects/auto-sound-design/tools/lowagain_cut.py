"""Low Again ~75 s cut. ~70 BPM. Joins at vocal gaps (demucs), beat shifts in whole bars:
beat 18 -> 102 (intro gap into the big section's breath, chroma 0.91), beat 151 -> 167 (outro, 0.99).
Equal-power crossfades one beat long, centred on the join beat."""
import librosa, numpy as np, soundfile as sf
y,sr=librosa.load("/Users/10xhunter/Downloads/Low Again (1).mp3",sr=None,mono=False); bt=np.loadtxt("bt.txt")
H=0.43; J=[(bt[18],bt[102]),(bt[151],bt[167])]
segs=[];st=0.0
for o,i in J: segs.append((st,o)); st=i
segs.append((st,y.shape[1]/sr)); mix=None; m=int(2*H*sr); t=np.linspace(0,np.pi/2,m)
for k,(a,b) in enumerate(segs):
  x=y[:,int(max(0,a-(H if k else 0))*sr):int((b+(H if k<len(segs)-1 else 0))*sr)].copy()
  if mix is None: mix=x; continue
  mix[:,-m:]=mix[:,-m:]*np.cos(t)+x[:,:m]*np.sin(t); mix=np.concatenate([mix,x[:,m:]],1)
sf.write("cut.wav",mix.T,sr,subtype="PCM_24"); print([(round(a,2),round(b,2)) for a,b in segs], round(mix.shape[1]/sr,2))
