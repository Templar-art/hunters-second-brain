"""21 Albany Reel ambience only (Hunter did the whooshes/shings). Outside shots get calibrated beds; interiors get
NOTHING (Hunter: no birds inside the house), and outdoor beds end at the cut into an interior instead of crossfading in."""
import json, sys
P="/Users/10xhunter/Documents/Hunters Second Brain/projects/"; A=P+"auto-sound-design/sfx/pixabay-owned/"; Bd=P+"albany-21-main-sfx/beds/"
F=dict(W=A+"traian1984-ambience-wind-blowing-through-trees-01-186986.mp3",B=A+"freesound_community-birds-19624.mp3",
 N=A+"u_vr5icvkppa-nature-ambience-323729.mp3",PW=A+"freesound_community-pool-water-27449.mp3",
 PW2=A+"freesound_community-water-of-a-pool-54298.mp3",WV=Bd+"u_m17uwtnjmh-soft-waves-on-the-beach-sound-190884.mp3")
END=27.6   # beds fade out across Hunter's whip into the end card
S=[(0.00,1.17,"top-down open",[("W",10,0),("B",5,-6)],14),
 (1.17,2.13,"rock beach aerial",[("WV",20,0),("W",20,-6)],13),
 (2.13,3.09,"creek park",[("B",30,0),("N",585,-6)],13),
 (3.09,4.05,"sunset deck",[("B",45,0)],15),
 (4.05,5.00,"driveway",[("B",60,0)],14),
 (5.00,6.97,"pool day-dusk",[("PW",3,0),("B",75,-5)],13),
 (6.97,7.92,"hanging chair",[("B",90,0),("N",580,-6)],14),
 (7.92,8.88,"pool rear",[("PW2",8,0),("B",105,-5)],13),
 (8.88,9.84,"balcony underside",[("B",120,0),("W",30,-6)],14),
 (9.84,14.64,"INTERIOR living/kitchen",[],None),
 (14.64,15.60,"outdoor lounge",[("B",150,0),("PW",12,-6)],14),
 (15.60,16.56,"entertaining pool",[("PW",18,0),("B",165,-5)],14),
 (16.56,19.44,"INTERIOR bed/bath",[],None),
 (19.44,20.40,"covered deck sunset",[("B",200,0)],15),
 (20.40,21.81,"covered entertaining",[("B",215,0)],16),
 (21.81,22.77,"outdoor table",[("B",230,0),("N",586,-6)],14),
 (22.77,23.73,"woman profile",[("B",245,0)],14),
 (23.73,25.19,"aerial in trees",[("W",45,0),("B",260,-6)],14),
 (25.19,END,"top-down close",[("W",55,0),("B",275,-6)],14)]
X=0.5; calib=json.load(open(sys.argv[2])) if len(sys.argv)>2 else {}
cues=[]
for n,(s,e,lab,ls,tgt) in enumerate(S):
  if not ls: continue
  po=n>0 and S[n-1][3]; no=n+1<len(S) and S[n+1][3]
  st=max(0,s-(X/2 if po else 0)); en=e+(X/2 if no else 0); g0=calib.get(lab,0.0)
  for k,ip,rel in ls:
    cues.append({"t":round(st,3),"label":f"amb {lab} ({k})","file":F[k],"role":"ambience","anchor":"start",
     "slice":[ip,round(en-st,3)],"fade_in":(X if po else (0.6 if s==0 else 0.12)),
     "fade_out":(X if no else (1.2 if e==END else 0.12)),"fade_curve":"qsin","gain_db":round(g0+rel,1)})
json.dump({"video":"/Volumes/10X SSD3/21 Albany Avenue, Currumbin/Exports/Reel.mp4","keep_audio":"yes",
 "cues":sorted(cues,key=lambda q:q["t"])},open(sys.argv[1],"w"),indent=1)
json.dump([[s,min(e,26.6),lab,tgt] for s,e,lab,ls,tgt in S if ls],open(sys.argv[1].replace(".json","_scenes.json"),"w"))
