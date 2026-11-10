"""8 Nassau Ave Terranora REEL (30 s, 9:16): ambience beds only, same recipe as the Main (Hunter does whooshes; the
Fire Fire FX cut carries riser/booms). Interiors 16.56-26.15 silent; outdoor beds end at the cut into an interior."""
import json, sys
P="/Users/10xhunter/Documents/Hunters Second Brain/projects/"; A=P+"auto-sound-design/sfx/pixabay-owned/"
F=dict(W=A+"traian1984-ambience-wind-blowing-through-trees-01-186986.mp3",B=A+"freesound_community-birds-19624.mp3",
 N=A+"u_vr5icvkppa-nature-ambience-323729.mp3",PW=A+"freesound_community-pool-water-27449.mp3",PW2=A+"freesound_community-water-of-a-pool-54298.mp3")
END=29.5   # beds fade out under the end card tail
S=[(0.000,1.668,"air"),(1.668,1.960,"dusk"),(1.960,3.587,"out"),(3.587,5.047,"air"),(5.047,6.381,"out"),
   (6.381,7.925,"duskpool"),(7.925,9.843,"pool"),(9.843,10.802,"duskpool"),(10.802,16.558,"out"),
   (16.558,26.151,"int"),(26.151,END,"air")]
L=dict(air=[("W",0),("B",-7)],out=[("B",0),("N",-6)],pool=[("PW",0),("B",-5)],duskpool=[("PW2",0),("N",-4)],dusk=[("N",0)])
T=dict(air=14,out=14,pool=13,duskpool=13,dusk=14)
X=0.5; calib=json.load(open(sys.argv[2])) if len(sys.argv)>2 else {}
cues=[]; scenes=[]; ip={"W":20,"B":40,"N":520,"PW":30,"PW2":20}
for n,(s,e,k) in enumerate(S):
  if k=="int": continue
  lab=f"{k} {s:.1f}"; po=n>0 and S[n-1][2]!="int"; no=n+1<len(S) and S[n+1][2]!="int"
  st=max(0,s-(X/2 if po else 0)); en=e+(X/2 if no else 0); g0=calib.get(lab,0.0)
  for key,rel in L[k]:
    cues.append({"t":round(st,3),"label":f"amb {lab} ({key})","file":F[key],"role":"ambience","anchor":"start",
     "slice":[ip[key],round(en-st,3)],"fade_in":(X if po else (0.4 if s==0 else 0.12)),
     "fade_out":(X if no else (1.5 if e==END else 0.12)),"fade_curve":"qsin","gain_db":round(g0+rel,1)})
    ip[key]+=(en-st)+2
  scenes.append([s,min(e,28.0),lab,T[k]])
json.dump({"video":"/Volumes/T7/8 Nassau Avenue Terranora/Exports/Reel.mp4","keep_audio":"yes",
 "cues":sorted(cues,key=lambda q:q["t"])},open(sys.argv[1],"w"),indent=1)
json.dump(scenes,open(sys.argv[1].replace(".json","_scenes.json"),"w"))
print(len(scenes),"outdoor scenes")
