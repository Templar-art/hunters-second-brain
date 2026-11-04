"""Trivelle girls' night ad: Seedance 3D two-friend clip (own audio) + BEFORE/AFTER mood tags + relax beat + end card."""
import os
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "build_ads_v2.py")).read()
exec(src[:src.index("B = lambda")])
SCRIPTS["friends"] = ("Okay, you need to see this. Heat, red light, little pulses, and a vacuum massage. All in one. "
                      "And this replaced the salon? Ten minutes on the couch. Try it. Oh... That's actually lovely.")
FR = os.path.join(D2, "friends", "friends_raw.mp4"); RELAX = os.path.join(D2, "animated3d", "v6.mp4")
ws = words("friends"); df = dur(FR)
END = os.path.join(WORK, "endcard.mp4"); end_card(END)
seq = [(FR + "#ss=0", df, False), (RELAX, 3.0, False), (END, 3.5, False)]
out = build("trivelle-H-girls-night-raw", seq, FR, chunks(ws), df + 6.5, 0)
# mood before/after tags (feeling, not body)
from PIL import Image, ImageDraw, ImageFont
def tagpng(txt):
    im = Image.new("RGBA", (W, 400), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    f = ImageFont.truetype(os.path.join(FONTS, "Anton-Regular.ttf"), 110); w = d.textlength(txt, font=f)
    d.text(((W - w) / 2, 200), txt, font=f, fill="white", stroke_width=9, stroke_fill=(29, 42, 38))
    p = os.path.join(WORK, f"tag_{txt}.png"); im.save(p); return p
fin = os.path.join(OUT, "trivelle-H-girls-night.mp4")
sh(["ffmpeg", "-v", "error", "-y", "-i", out, "-i", tagpng("BEFORE"), "-i", tagpng("AFTER"), "-filter_complex",
    f"[0:v][1:v]overlay=0:0:enable='between(t,0.3,5.5)'[a];[a][2:v]overlay=0:0:enable='between(t,12.4,{df+3.0:.2f})'[v]",
    "-map", "[v]", "-map", "0:a", "-c:v", "libx264", "-crf", "20", "-preset", "slow", "-c:a", "copy", "-movflags", "+faststart", fin])
os.remove(out); print(fin)
