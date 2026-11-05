"""Salerno St SFX v3: scene-matched beds on the 15:14 re-export. Hunter's own SFX (logo 0-3 s, ramps ~27/32/35 s, whip 63 s)
are already in the audio, so this pass adds no whooshes. Each scene's bed level is calibrated to the music: TARGET dB under
(measured in a second pass by calib.json)."""
import json, sys
P="/Users/10xhunter/Documents/Hunters Second Brain/projects/"; A=P+"auto-sound-design/sfx/pixabay-owned/"
F=dict(W="traian1984-ambience-wind-blowing-through-trees-01-186986.mp3",B="freesound_community-birds-19624.mp3",
 O="freesound_community-outside-ambience-with-birds-61606.mp3",N="u_vr5icvkppa-nature-ambience-323729.mp3",
 CUR="freesound_community-160170_wind-blowing-curtain_owi-102398.mp3",PW="freesound_community-pool-water-27449.mp3",
 PW2="freesound_community-water-of-a-pool-54298.mp3",RW="alex_jauk-running-water-gentle-sound-185148.mp3")
# start, end, scene, layers [(key, in_point, relative dB within the scene)], target dB under the music
S=[(0.00,2.59,"aerial opener",[("W",10,0),("B",5,-6)],15),
 (2.59,3.54,"curtain interior",[("CUR",2,0)],14),
 (3.54,5.92,"pool",[("PW",3,0),("B",60,-5)],13),
 (5.92,7.13,"palms",[("B",90,0),("W",30,-6)],13),
 (7.13,10.18,"front garden",[("B",120,0)],13),
 (10.18,11.14,"city aerial",[("W",50,0)],14),
 (11.14,13.26,"entry / street",[("B",440,0)],13),
 (13.26,18.18,"front / garden",[("B",150,0),("N",585,-6)],13),
 (18.18,25.50,"interiors (window bleed)",[("B",200,0)],22),
 (25.50,30.00,"patio / pool",[("PW2",8,0),("N",580,-4)],13),
 (30.00,34.74,"hut / pool / house",[("PW",12,0),("B",260,-4)],13),
 (34.74,38.96,"aerials",[("W",40,0)],14),
 (38.96,48.88,"upstairs interiors (bleed)",[("B",300,0)],23),
 (48.88,49.84,"curtain window",[("CUR",4,0)],14),
 (49.84,51.26,"presenter pool 1",[("B",330,0),("PW",20,-4)],15),
 (51.26,53.14,"dock / jetty",[("RW",5,0),("B",360,-5)],13),
 (53.14,54.10,"street / tower",[("N",589,0)],14),
 (54.10,55.05,"presenter pool 2",[("B",380,0),("PW",24,-4)],15),
 (55.05,59.31,"cafe / shops",[("B",470,0),("N",586,-6)],14),
 (59.31,63.52,"presenter pool 3",[("B",400,0),("PW",28,-4)],15),
 (63.52,67.82,"closing aerial",[("W",60,0)],15)]
X=0.5; calib=json.load(open(sys.argv[2])) if len(sys.argv)>2 else {}
cues=[]
for s,e,lab,ls,tgt in S:
  st=max(0,s-X/2); ln=(e-s)+X; g0=calib.get(lab,0.0)
  for k,ip,rel in ls:
    cues.append({"t":round(st,3),"label":f"amb {lab} ({k})","file":A+F[k],"role":"ambience","anchor":"start",
     "slice":[ip,round(ln,3)],"fade_in":X if s>0 else 0.8,"fade_out":X if e<67 else 2.5,"fade_curve":"qsin","gain_db":round(g0+rel,1)})
cues.append({"t":6.23,"label":"shing flare","file":P+"sfx-custom/out/shing_classic.wav","role":"chime","anchor":"peak","gain_db":-4})
json.dump({"video":"/Volumes/10X SSD2/42 Salerno Street, Isle of Capri | Listing Package/Edits/Main.mp4","keep_audio":"yes",
 "cues":sorted(cues,key=lambda q:q["t"])},open(sys.argv[1],"w"),indent=1)
json.dump([[s,e,lab,tgt] for s,e,lab,ls,tgt in S],open(sys.argv[1].replace(".json","_scenes.json"),"w"))
