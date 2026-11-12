import sys,numpy as np,librosa
F="/Users/10xhunter/Downloads/Ryan Taubert - Lux.mp3";SR=22050
y,_=librosa.load(F,sr=SR);bt=np.loadtxt("tools/lux_bt.txt");H=512
C=librosa.feature.chroma_cqt(y=y,sr=SR,hop_length=H);M=librosa.power_to_db(librosa.feature.melspectrogram(y=y,sr=SR,hop_length=H,n_mels=64))
fr=lambda t:int(t*SR/H)
def sim(X,a,b,w):
    A=X[:,fr(a):fr(a)+w].ravel();B=X[:,fr(b):fr(b)+w].ravel();return np.corrcoef(A,B)[0,1]
w=int(2*(bt[8]-bt[0])*SR/H/2)  # ~1 bar either side
res=[]
for i in range(int(sys.argv[1]),int(sys.argv[2]),2):
  for j in range(int(sys.argv[3]),min(int(sys.argv[4]),len(bt)-8),2):
    a,b=bt[i],bt[j];ww=fr(bt[i+4])-fr(a)
    s=[sim(C,a-(bt[i+4]-a),b-(bt[i+4]-a),2*ww),sim(M,a-(bt[i+4]-a),b-(bt[i+4]-a),2*ww)]
    res.append((0.5*s[0]+0.5*s[1],i,j,round(a,1),round(b,1),[round(x,3) for x in s]))
for r in sorted(res)[-8:]:print(r)
