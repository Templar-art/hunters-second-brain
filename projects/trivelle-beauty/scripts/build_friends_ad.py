"""Trivelle girls' night ad: Seedance 3D two-friend clip (own audio) + relax beat + end card."""
import os
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "build_ads_v2.py")).read()
exec(src[:src.index("B = lambda")])
SCRIPTS["friends"] = ("Okay, you need to see this. Heat, red light, little pulses, and a vacuum massage. All in one. "
                      "And this replaced the salon? Ten minutes on the couch. Try it. Oh... That's actually lovely.")
FR = os.path.join(D2, "friends", "friends_raw.mp4"); PAY = os.path.join(D2, "friends", "payoff.mp4")
ws = words("friends"); df = dur(FR)
END = os.path.join(WORK, "endcard.mp4"); end_card(END)
seq = [(FR + "#ss=0", df, False), (PAY, 4.0, False), (END, 3.5, False)]
out = build("trivelle-H-girls-night-raw", seq, FR, chunks(ws) + chunks([(df+0.4,df+1.2,"Okay..."),(df+1.3,df+1.7,"send"),(df+1.7,df+2.0,"me"),(df+2.0,df+2.3,"the"),(df+2.3,df+3.8,"link!")]), df + 7.5, 0)
fin = os.path.join(OUT, "trivelle-H-girls-night.mp4"); os.replace(out, fin); print(fin)
