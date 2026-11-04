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
LINK = os.path.join(D2, "friends", "link.mp3"); L0 = df + 0.5
VOC = os.path.join(WORK, "friends_vo.wav")
sh(["ffmpeg", "-v", "error", "-y", "-i", FR, "-i", LINK, "-filter_complex",
    f"[0:a]apad[a0];[1:a]adelay={int(L0*1000)}|{int(L0*1000)},volume=1.3[a1];[a0][a1]amix=inputs=2:normalize=0:duration=longest[a]",
    "-map", "[a]", "-t", f"{df + 7.5:.3f}", VOC])
lw = [(L0+0.05,L0+0.36,"Okay..."),(L0+0.36,L0+0.77,"send"),(L0+0.77,L0+0.89,"me"),(L0+0.89,L0+1.12,"the"),(L0+1.12,L0+2.2,"link!")]
out = build("trivelle-H-girls-night-raw", seq, VOC, chunks(ws) + chunks(lw), df + 7.5, 0)
fin = os.path.join(OUT, "trivelle-H-girls-night.mp4"); os.replace(out, fin); print(fin)
