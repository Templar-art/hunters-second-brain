import json, sys, numpy as np, soundfile as sf
sc=json.load(open(sys.argv[1])); s,sr=sf.read(sys.argv[2]); s=s.mean(1) if s.ndim>1 else s
m,msr=sf.read(sys.argv[3]); m=m.mean(1) if m.ndim>1 else m; assert msr==sr,(msr,sr); old=json.load(open(sys.argv[4])) if len(sys.argv)>4 else {}
db=lambda x:20*np.log10(np.sqrt(np.mean(x**2))+1e-12); out={}
for a,b,lab,tgt in sc:
  i,j=int((a+0.3)*sr),int((b-0.3)*sr)
  if j-i<sr*0.3: i,j=int(a*sr),int(b*sr)
  under=db(m[i:j])-db(s[i:j]); adj=under-tgt; out[lab]=round(old.get(lab,0)+adj,1)
  print("%-28s under %5.1f target %d -> %+.1f"%(lab,under,tgt,adj))
json.dump(out,open(sys.argv[5] if len(sys.argv)>5 else "calib.json","w"),indent=1)
