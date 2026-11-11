"""Bespoke / Emerald Lakes 'If you're a runner' piece-to-camera. C8194 opener + agent lines from C8200.
Agent's takes picked by lav loudness (agent 45-55 dB vs Damon's prompts 20-35 dB). Times re-timed on short windows."""
import json, wave, numpy as np, sys
S = sys.argv[1]
w = wave.open(S + "/a.wav"); AUD = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float)
def db(a, b):
    x = AUD[int(a*16000):int(b*16000)]; return 20*np.log10(np.sqrt((x**2).mean())+1e-9)
def tail(t, lim=0.35):
    t0 = t
    while t - t0 < lim and db(t, t+0.12) > 36: t += 0.01
    return t + 0.06
FPS = 25; fr = lambda t: int(round(t*FPS))
SEG = [  # (start, end, broll (clip, clip_in_s) or None)
 (103.60, 105.15, None),                       # It's a European-style community
 (108.52, 110.20, ("C3939.MP4", 1.0)),         # that offers scenic views all the way around
 (163.76, 165.55, None),                       # That's why, if you're a runner,
 (167.90, 169.55, ("C8180.MP4", 0.5)),         # you're gonna love the six kilometre track.
 (171.48, 175.20, None),                       # Doesn't matter where you are on it, you're gonna see something new.
 (191.00, 193.30, ("C3944.MP4", 1.0)),         # Whether it's running over a bridge
 (195.46, 196.60, ("C3925.MP4", 2.0)),         # or past all the cafes,
 (202.42, 205.85, None),                       # this offers a runner's lifestyle like no other place on the coast.
]
OPEN = {"clip": "C8194.MP4", "src_in": 0, "src_out": 203}
out, rec = [], OPEN["src_out"] - OPEN["src_in"]
for a, b, br in SEG:
    f0, f1 = fr(a - 0.03), fr(tail(b))
    out.append({"src_in": f0, "src_out": f1, "rec": rec, "broll": [{"clip": br[0], "src_in": fr(br[1]), "rec_in": rec - 12, "rec_out": rec + f1 - f0}] if br else []})  # B-roll starts 12f early to hide the join
    rec += f1 - f0
# every remaining join gets a short B-roll cover (Hunter: no Smooth Cuts, just B-roll)
FILL = ["C3929.MP4", "C3949.MP4", "C3924.MP4", "C3927.MP4"]
k = 0
for i in range(1, len(out)):
    j = out[i]["rec"]
    if not any(b["rec_in"] < j < b["rec_out"] for o in out for b in o["broll"]):
        out[i]["broll"].append({"clip": FILL[k % len(FILL)], "src_in": 25, "rec_in": j - 12, "rec_out": j + 20}); k += 1
allb = sorted((b for o in out for b in o["broll"]), key=lambda b: b["rec_in"])
for x, y in zip(allb, allb[1:]):
    if y["rec_in"] < x["rec_out"]:
        y["src_in"] += x["rec_out"] - y["rec_in"]; y["rec_in"] = x["rec_out"]  # butt-join, no overlap on V2
json.dump({"opener": OPEN, "segs": out}, open("edl.json", "w"), indent=1)
print("total", rec / FPS)
