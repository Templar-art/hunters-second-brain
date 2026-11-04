"""Trivelle podcast ad: Seedance host clip (own audio) + device B-roll cutaways on the mode words + captions + end card."""
import os
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "build_ads_v2.py")).read()
exec(src[:src.index("B = lambda")])
SCRIPTS["pod"] = ("Okay, honestly? I stopped doing the salon body treatments. I got one of these four-in-one things instead. "
                  "Heat, red light, the little pulses, and a vacuum massage. Ten minutes on the couch, a few nights a week. "
                  "My skin just looks smoother. I'm obsessed.")
POD = os.path.join(D2, "podcast", "pod_raw.mp4"); N2 = lambda n: os.path.join(D2, "broll", n + ".mp4")
ws = words("pod"); dp = dur(POD)
def at(w, after=0): return next(x[0] for x in ws if x[0] >= after and _norm(x[2]).startswith(w))
# cutaways: device during the mode list, then back to her for the payoff
cuts = [(at("heat") - 0.05, N2("v3-arm-red")), (at("little") - 0.1, N2("v1-stomach-glow"))]
back = at("ten") - 0.05
seq, t = [], 0.0
for i, (c0, clip) in enumerate(cuts):
    if i == 0: seq.append((POD + "#ss=0", c0, False))
    nxt = cuts[i + 1][0] if i + 1 < len(cuts) else back
    seq.append((clip, nxt - c0, False))
seq.append((POD + f"#ss={back:.3f}", dp - back, False))
END = os.path.join(WORK, "endcard.mp4"); end_card(END); seq.append((END, 3.5, False))
print(build("trivelle-I-podcast", seq, POD, chunks(ws), dp + 3.5, 0))
