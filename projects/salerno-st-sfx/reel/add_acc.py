import json,sys
d=json.load(open(sys.argv[1]))
d['cues'].append({"t":23.8,"label":"accent pin reveal","id":2014,"role":"chime","anchor":"peak","gain_db":-6,"highpass":500,
 "layers":[{"dt":0.0,"id":460,"role":"hit","anchor":"arrive","gain_db":-12,"lowpass":180}]})
d['cues'].sort(key=lambda q:q['t']); json.dump(d,open(sys.argv[1],'w'),indent=1)
