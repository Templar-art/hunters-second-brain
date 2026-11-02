"""Low Again v2: join 1 rebuilt as a one-bar beat-locked swell. Over the bar before beat 18 the intro keeps playing
(its vocal ends in the beat-18 breath) while the big section's own pre-roll bar (beats 98-102) comes in on the
demucs instrumental stem on a delayed equal-power curve; from beat 102 the full mix takes over. Join 2 unchanged."""
import librosa, numpy as np, soundfile as sf
F="/Users/10xhunter/Downloads/Low Again (1).mp3"
y,sr=librosa.load(F,sr=None,mono=False); nv,_=librosa.load("dm/htdemucs/no_vocals.wav",sr=sr,mono=False)
_b=np.loadtxt("bt.txt"); _k=np.arange(len(_b)); bt=np.polyval(np.polyfit(_k,_b,1),_k); I=lambda t:int(round(t*sr))
def xf(a,b,sec):
  m=int(sec*sr); t=np.linspace(0,np.pi/2,m); a=a.copy(); a[:,-m:]=a[:,-m:]*np.cos(t)+b[:,:m]*np.sin(t); return np.concatenate([a,b[:,m:]],1)
# segment 1: intro to beat 14, then the swell bar
A=y[:,:I(bt[14])]
o=y[:,I(bt[14]):I(bt[18])]; inc=nv[:,I(bt[98]):I(bt[98])+o.shape[1]]
n=o.shape[1]; u=np.linspace(0,1,n); gi=np.sin(u**2.2*np.pi/2); go=np.cos(u**2.2*np.pi/2)**0.5
sw=o*go+inc*gi
# hand-off at beat 102: stem -> full mix over a quarter beat, both from the same source time (no rhythm jump)
q=I(0.2); stem_tail=nv[:,I(bt[102]):I(bt[102])+q]; full=y[:,I(bt[102]):I(bt[151]+0.43)]  # +half the crossfade so the incoming downbeat lands on bt[151]
w=np.linspace(0,1,q); full[:,:q]=stem_tail*(1-w)+full[:,:q]*w
mix=np.concatenate([A,sw,full],1)
mix=xf(mix,y[:,I(bt[167])-I(0.43):],0.86)  # join 2 as v1 (outro, chroma 0.99)
sf.write("cut3.wav",mix.T,sr,subtype="PCM_24"); print(round(mix.shape[1]/sr,2))
