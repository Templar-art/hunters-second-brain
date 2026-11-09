"""21 Albany Ave Main SFX: scene beds calibrated under the music (Salerno v3 recipe) + 4 whooshes on zone changes /
the pin / the whip (Hunter-approved Coastal Albany picks) + one soft flare on the sunburst. The music ends at 59.3 s,
so the whip, dusk aerial and end card get a fixed-level wind bed fading out."""
import json, sys
P="/Users/10xhunter/Documents/Hunters Second Brain/projects/"; A=P+"auto-sound-design/sfx/pixabay-owned/"; Bd=P+"albany-21-main-sfx/beds/"
F=dict(W=A+"traian1984-ambience-wind-blowing-through-trees-01-186986.mp3",B=A+"freesound_community-birds-19624.mp3",
 N=A+"u_vr5icvkppa-nature-ambience-323729.mp3",SW=A+"storegraphic-soft-wind-477404.mp3",
 PW=A+"freesound_community-pool-water-27449.mp3",PW2=A+"freesound_community-water-of-a-pool-54298.mp3",
 WV=Bd+"u_m17uwtnjmh-soft-waves-on-the-beach-sound-190884.mp3",WV2=Bd+"juliush-sandy-beach-calm-waves-water-nature-sounds-8052.mp3")
S=[(0.00,1.46,"beach aerial",[("WV",20,0),("W",10,-6)],14),
 (1.46,2.92,"house aerial",[("W",30,0),("B",5,-5)],14),
 (2.92,4.34,"lake aerial",[("W",40,0),("B",15,-8)],15),
 (4.34,5.80,"rock beach",[("WV2",10,0)],12),
 (5.80,7.26,"sand beach",[("WV",50,0),("W",50,-8)],13),
 (7.26,8.72,"creek park",[("B",30,0),("N",585,-6)],13),
 (8.72,10.18,"garden path",[("B",45,0)],13),
 (10.18,12.10,"balcony ext",[("B",60,0),("W",60,-8)],14),
 (12.10,13.56,"sunset chair",[("B",75,0)],15),
 (13.56,14.51,"bbq wine",[("B",90,0)],15),
 (14.51,16.93,"twilight front",[("W",84,0),("N",580,-8)],15),
 (16.93,31.95,"interiors (bleed)",[("B",120,0)],23),
 (31.95,33.37,"balcony woman",[("B",150,0)],18),
 (33.37,34.83,"railing hand",[("B",165,0),("W",75,-6)],14),
 (34.83,36.37,"aerial houses",[("W",5,0),("B",180,-6)],14),
 (36.37,38.29,"wide aerial pin",[("W",20,0),("B",190,-6)],14),
 (38.29,39.66,"sun window",[("B",200,0)],16),
 (39.66,42.58,"pool ext",[("PW",3,0),("B",210,-5)],13),
 (42.58,43.54,"pool feet",[("PW2",8,0)],13),
 (43.54,44.50,"balcony low",[("B",230,0),("W",45,-6)],14),
 (44.50,46.46,"outdoor table",[("B",240,0),("N",586,-6)],14),
 (46.46,47.38,"entertaining",[("B",255,0)],15),
 (47.38,56.22,"bed/bath (bleed)",[("B",270,0)],23),
 (56.22,59.98,"top-down aerials",[("W",55,0),("B",300,-6)],14),
 (59.98,64.06,"tail aerial + card",[("W",65,0)],0)]
X=0.5; calib=json.load(open(sys.argv[2])) if len(sys.argv)>2 else {}
cues=[]
for s,e,lab,ls,tgt in S:
  st=max(0,s-X/2); ln=(e-s)+X; g0=calib.get(lab,0.0)
  for k,ip,rel in ls:
    cues.append({"t":round(st,3),"label":f"amb {lab} ({k})","file":F[k],"role":"ambience","anchor":"start",
     "slice":[ip,round(min(ln,64.06-st),3)],"fade_in":X if s>0 else 0.8,"fade_out":X if e<64 else 3.0,"fade_curve":"qsin","gain_db":round(g0+rel,1)})
WH="/Users/10xhunter/Music/SFX Library/Ocular Sounds/"
cues+= [{"t":34.83,"label":"whoosh into aerial","file":WH+"Foundation/DSGNWhsh/DSGNWhsh_WHOOSH-Weight_Ocular_Foundation.wav","role":"whoosh","gain_db":-4},
 {"t":36.60,"label":"whoosh pin","file":WH+"Forged/DSGNWhsh/DSGNWhsh_SWEETENER-Movement Sweetener 33_Ocular_Forged.wav","role":"whoosh","gain_db":-8},
 {"t":56.22,"label":"whoosh into top-down","file":WH+"Forged/DSGNWhsh/DSGNWhsh_SWEETENER-Movement Sweetener 33_Ocular_Forged.wav","role":"whoosh","gain_db":-4},
 {"t":60.35,"label":"whoosh whip","file":WH+"Foundation/DSGNWhsh/DSGNWhsh_WHOOSH-Weight_Ocular_Foundation.wav","role":"whoosh","gain_db":-3},
 {"t":38.75,"label":"flare sunburst","file":P+"sfx-custom/out/lens-flare_soft.wav","role":"chime","anchor":"peak","gain_db":-6}]
json.dump({"video":"/Volumes/10X SSD3/21 Albany Avenue, Currumbin/Exports/21 Albany Avenue | Main.mp4","keep_audio":"yes",
 "cues":sorted(cues,key=lambda q:q["t"])},open(sys.argv[1],"w"),indent=1)
json.dump([[s,e,lab,tgt] for s,e,lab,ls,tgt in S if tgt],open(sys.argv[1].replace(".json","_scenes.json"),"w"))
