"""Osupa Ti (Radio Edit), ~60 s cut for Kollosche. 119.7 BPM, downbeat = beat 2 (bar 0 at 1.25 s); bt.txt = librosa beat times.
Map: intro 1.25-33.6, break 33.6-49.6, drop 49.6-97.6, break 97.6-129.7, drop 129.7-225.6, decay to 228.7.
Splices are whole 4-bar shifts at a vocal breath gap (demucs): bar 6 b1 -> bar 10 b1, bar 27 b2 -> bar 107 b2 (chroma 0.997).
0.24 s equal-power crossfades (levels match, no jump). Master: straight -5.6 dB gain -> -14 LUFS / -5.2 dBTP. Result 64.25 s."""
import librosa, numpy as np, soundfile as sf
F="/Users/10xhunter/Downloads/Osupa Ti (Radio Edit).mp3"
y,sr=librosa.load(F,sr=None,mono=False); bt=np.loadtxt("bt.txt")
beat=lambda bar,b: bt[2+4*bar+b]
H=0.12
# (out_time, in_time): splice in vocal breath gaps, whole 4-bar shifts
J=[(beat(6,1),beat(10,1)),(beat(27,2),beat(107,2))]
segs=[];start=0.0
for o,i in J: segs.append((start,o)); start=i
segs.append((start,len(y[0])/sr))
print([(round(a,3),round(b,3)) for a,b in segs])
mix=None;m=int(2*H*sr);t=np.linspace(0,np.pi/2,m)
for k,(a,b) in enumerate(segs):
  a0=max(0,a-(H if k else 0)); b1=b+(H if k<len(segs)-1 else 0)
  x=y[:,int(a0*sr):int(b1*sr)].copy()
  if mix is None: mix=x;continue
  mix[:,-m:]=mix[:,-m:]*np.cos(t)+x[:,:m]*np.sin(t); mix=np.concatenate([mix,x[:,m:]],1)
sf.write("cut.wav",mix.T,sr,subtype="PCM_24"); print(round(mix.shape[1]/sr,2),"s")
