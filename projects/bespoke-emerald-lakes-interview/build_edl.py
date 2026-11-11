"""Bespoke / Emerald Lakes street interview -> <60 s vertical social cut. Times = C8197 seconds."""
import json, wave, numpy as np, sys
S = sys.argv[1]
w = wave.open(S + "/a.wav"); AUD = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float)
def db(a, b):
    x = AUD[int(a*16000):int(b*16000)]; return 20*np.log10(np.sqrt((x**2).mean())+1e-9)
floor = np.percentile([db(t, t+0.05) for t in np.arange(0, 245, 0.05)], 20) + 6
def snap(t, d, lim=0.35):
    t0 = t
    while abs(t - t0) < lim:
        if db(*((t, t+0.12) if d > 0 else (t-0.12, t))) < floor: break
        t += 0.01*d
    return t + 0.05*d
# (start, end, angle, broll list [(clip, clip_in_s, cover_from_s, cover_to_s)] in interview time)
SEG = [
 (47.00, 48.80, "W",  []),
 (48.99, 52.95, "W", []),
 (53.25, 55.85, "W", []),
 (55.99, 59.30, "W", []),
 (59.35, 60.95, "W", []),
 (69.40, 71.95, "W",  []),
 (118.98, 124.35, "W", []),   # cafe Q+A in one piece (whisper times drift ~1.2 s here; energy-checked)
 (133.15, 136.05, "W",  []),
 (136.05, 138.75, "W", []),
 (192.30, 198.20, "W",  []),
 (214.70, 224.00, "W", []),
 (235.75, 240.40, "W", []),
 (240.90, 244.40, "W",  []),
]
FPS = 25; fr = lambda t: int(round(t*FPS)); out = []; rec = 0
for i, (a, b, ang, br) in enumerate(SEG):
    prev_b = SEG[i-1][1] if i else -9; next_a = SEG[i+1][0] if i+1 < len(SEG) else 999
    a2 = a - 0.02   # starts sit exactly on the first word (snapping back pulled in 'yep', 'take two', 'um')
    b2 = b if next_a - b < 0.6 else snap(b, +1)
    if out and fr(a2) < out[-1]["src_out"] and abs(a - SEG[i-1][1]) < 0.1: a2 = SEG[i-1][1]  # contiguous
    f0, f1 = fr(a2), fr(b2)
    brs = []
    for clip, cin, c0, c1 in br:
        s = rec + (fr(c0) - f0 if c0 else 0); e = rec + (fr(c1) - f0 if c1 else f1 - f0)
        brs.append({"clip": clip, "src_in": fr(cin), "rec_in": s, "rec_out": e})
    out.append({"src_in": f0, "src_out": f1, "angle": ang, "rec": rec, "broll": brs}); rec += f1 - f0
# Hunter 2026-11-11: B-roll over every cut, runs of 3 clips back-to-back, clips in filename order
BR = ["C%d.MP4" % n for n in range(3917, 3956) if n != 3918]
k = 0
for i in range(1, len(out)):
    j = out[i]["rec"]; t = j - 24
    for _ in range(3):
        out[i]["broll"].append({"clip": BR[k % len(BR)], "src_in": 25, "rec_in": t, "rec_out": t + 20}); t += 20; k += 1
OPEN = {"clip": "C8194.MP4", "src_in": 0, "src_out": 0}  # opener removed: C8194 belongs to the other video  # full walk-in line "If you're a runner... Here's why.", own audio, before the interview
json.dump({"opener": OPEN, "segs": out}, open("edl.json", "w"), indent=1)
print("total", rec/FPS, "s")
