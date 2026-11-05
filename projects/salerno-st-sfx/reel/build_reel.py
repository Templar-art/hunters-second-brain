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
S=[(0.00,0.75,"aerial opener",[("W",10,0),("B",5,-6)],15),
 (0.75,1.71,"pool",[("PW",3,0),("B",60,-5)],13),
 (1.71,3.59,"palms",[("B",90,0),("W",30,-6)],13),
 (3.59,4.96,"entry presenter",[("B",120,0)],15),
 (4.96,5.92,"street",[("B",440,0),("N",585,-6)],13),
 (5.92,6.84,"city aerial",[("W",50,0)],14),
 (6.84,7.80,"dock",[("RW",5,0),("B",360,-5)],13),
 (7.80,11.55,"entry presenter 2",[("B",150,0)],15),
 (11.55,18.73,"interiors (bleed)",[("B",200,0)],22),
 (18.73,23.27,"pool / balcony",[("PW2",8,0),("N",580,-4)],13),
 (23.27,24.65,"city pin",[("W",74,0)],14),
 (24.65,26.53,"presenter pool 1",[("B",330,0),("PW",20,-4)],15),
 (26.53,28.40,"jetty / boat",[("RW",9,0),("B",370,-5)],13),
 (28.40,29.82,"presenter pool 2",[("B",380,0),("PW",24,-4)],15),
 (29.82,31.24,"city aerial 2",[("W",60,0)],14),
 (31.24,34.37,"cafe / shops",[("B",470,0),("N",586,-6)],14),
 (34.37,35.00,"presenter pool 3",[("B",400,0),("PW",28,-4)],15),
 (35.00,38.29,"closing aerial",[("W",20,0)],15)]
X=0.5; calib=json.load(open(sys.argv[2])) if len(sys.argv)>2 else {}
cues=[]
for s,e,lab,ls,tgt in S:
  st=max(0,s-X/2); ln=(e-s)+X; g0=calib.get(lab,0.0)
  for k,ip,rel in ls:
    cues.append({"t":round(st,3),"label":f"amb {lab} ({k})","file":A+F[k],"role":"ambience","anchor":"start",
     "slice":[ip,round(ln,3)],"fade_in":X if s>0 else 0.8,"fade_out":X if e<38 else 2.5,"fade_curve":"qsin","gain_db":round(g0+rel,1)})
json.dump({"video":"/Volumes/10X SSD2/42 Salerno Street, Isle of Capri | Listing Package/Edits/Reel.mp4","keep_audio":"yes",
 "cues":sorted(cues,key=lambda q:q["t"])},open(sys.argv[1],"w"),indent=1)
json.dump([[s,e,lab,tgt] for s,e,lab,ls,tgt in S],open(sys.argv[1].replace(".json","_scenes.json"),"w"))
