"""8 Nassau Ave Terranora Main: ambience beds only (Hunter does whooshes; no shings). Interiors silent, outdoor beds end at the cut."""
import json, sys
P="/Users/10xhunter/Documents/Hunters Second Brain/projects/"; A=P+"auto-sound-design/sfx/pixabay-owned/"
F=dict(W=A+"traian1984-ambience-wind-blowing-through-trees-01-186986.mp3",B=A+"freesound_community-birds-19624.mp3",
 N=A+"u_vr5icvkppa-nature-ambience-323729.mp3",PW=A+"freesound_community-pool-water-27449.mp3",PW2=A+"freesound_community-water-of-a-pool-54298.mp3")
C=[0,4.296,4.838,5.380,5.881,6.423,6.965,7.508,8.550,12.804,17.059,18.101,19.144,20.229,21.271,22.356,23.398,24.483,28.737,29.780,30.822,31.907,32.950,34.034,35.077,36.161,37.204,38.288,40.415,41.458,42.543,43.585,44.670,45.712,46.797,47.839,48.882,49.967,51.009,52.094,53.136,54.179,55.264,56.390,58.475,60.602,63.730,64.815,65.899,66.942,68.026,69.069,70.153,71.196,72.281,73.323,74.366,75.450,76.493,77.578,78.620,79.705,80.747,81.832,82.874,83.959,85.002,86.086,87.129,94.761]
# shot index -> kind
K={0:"air",8:"air",43:"air",44:"air",68:"sky"}
for i in list(range(1,8))+[10,11,12,13,14,15,29,30,31,33,34,36,37,38,39,40,41,42,45,61,62,63,64]: K[i]="out"
for i in [17,27,28,32,35]: K[i]="pool"
for i in [65,67]: K[i]="duskpool"
K[66]="dusk"
L=dict(air=[("W",0),("B",-7)],out=[("B",0),("N",-6)],pool=[("PW",0),("B",-5)],duskpool=[("PW2",0),("N",-4)],dusk=[("N",0)],sky=[("W",0)])
T=dict(air=14,out=14,pool=13,duskpool=13,dusk=14,sky=15)
# merge runs of same kind into scenes
S=[]; 
for i in range(len(C)-1):
  k=K.get(i,"int")
  if S and S[-1][2]==k: S[-1][1]=C[i+1]
  else: S.append([C[i],C[i+1],k])
X=0.5; calib=json.load(open(sys.argv[2])) if len(sys.argv)>2 else {}
cues=[]; scenes=[]; ip={"W":10,"B":5,"N":500,"PW":3,"PW2":8}
for n,(s,e,k) in enumerate(S):
  if k=="int": continue
  lab=f"{k} {s:.1f}"; po=n>0 and S[n-1][2]!="int"; no=n+1<len(S) and S[n+1][2]!="int"
  st=max(0,s-(X/2 if po else 0)); en=e+(X/2 if no else 0); g0=calib.get(lab,0.0)
  for key,rel in L[k]:
    cues.append({"t":round(st,3),"label":f"amb {lab} ({key})","file":F[key],"role":"ambience","anchor":"start",
     "slice":[ip[key],round(en-st,3)],"fade_in":(X if po else (0.6 if s==0 else 0.12)),
     "fade_out":(X if no else (2.5 if n==len(S)-1 else 0.12)),"fade_curve":"qsin","gain_db":round(g0+rel,1)})
    ip[key]+= (en-st)+2
  scenes.append([s,min(e,90.0),lab,T[k]])
json.dump({"video":"/Volumes/T7/8 Nassau Avenue Terranora/Exports/Main.mp4","keep_audio":"yes",
 "cues":sorted(cues,key=lambda q:q["t"])},open(sys.argv[1],"w"),indent=1)
json.dump(scenes,open(sys.argv[1].replace(".json","_scenes.json"),"w"))
print(len(scenes),"outdoor scenes;",[(round(s,1),round(e,1),k) for s,e,k in S])
