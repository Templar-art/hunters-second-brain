"""Salisbury postcard reel, frame-by-frame so the pop-ins can be eased. 0 credits.
Layout from Hunter's Solis Postcard Post reference: ink bg, three 16:9 cards (x37, 1006x566, y 64/678/1290).
Pop: card rises 70px + scales 0.90 -> 1 with a small overshoot (easeOutBack) over 0.5s, alpha 0->1 in the
first 0.12s so it reads as a pop, not a dissolve. Hard cut to the logo card, logo settles 0.94 -> 1.
usage: postcard.py out.mp4 music.mp3 music_start pop1,pop2,pop3 cut total clipA clipB clipC"""
import sys, subprocess, numpy as np
from PIL import Image
out, music, mst, pops, CUT, TOT = sys.argv[1], sys.argv[2], float(sys.argv[3]), [float(x) for x in sys.argv[4].split(",")], float(sys.argv[5]), float(sys.argv[6])
clips = sys.argv[7:10]
FPS, W, H, CW, CH, X, YS = 50, 1080, 1920, 1006, 566, 37, [64, 678, 1290]
INK = (0x0b, 0x0b, 0x0a); POP = 0.5
WIND = "/Users/10xhunter/Downloads/traian1984-ambience-wind-blowing-through-trees-01-186986.mp3"
def reader(p):
    return subprocess.Popen(["ffmpeg", "-v", "error", "-i", p, "-vf", f"scale={CW}:{CH}:flags=lanczos,unsharp=5:5:0.3", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
rd = [reader(c) for c in clips]; last = [None] * 3
def nextframe(i):
    b = rd[i].stdout.read(CW * CH * 3)
    if len(b) == CW * CH * 3: last[i] = Image.frombuffer("RGB", (CW, CH), b)
    return last[i]
def out_cubic(x): return 1 - (1 - x) ** 3
def out_back(x, s=1.4): x -= 1; return 1 + (s + 1) * x ** 3 + s * x ** 2
logo = Image.open("assets/endcard_postcard_916.png").convert("RGB")
ls = logo.crop((290, 760, 790, 1160))  # logo region for the settle
fo = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
    "-ss", str(mst), "-i", music, "-i", WIND, "-filter_complex",
    f"[1]atrim=0:{TOT},asetpts=PTS-STARTPTS,afade=out:st={TOT-2}:d=2[m];[2]atrim=0:{TOT},asetpts=PTS-STARTPTS,volume=0.15,afade=out:st={TOT-2}:d=2[w];[m][w]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]",
    "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-crf", "16", "-preset", "slow", "-pix_fmt", "yuv420p",
    "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-t", str(TOT), "-movflags", "+faststart", out], stdin=subprocess.PIPE)
for n in range(int(TOT * FPS)):
    t = n / FPS
    if t >= CUT:
        x = min(1, (t - CUT) / 0.6); s = 0.94 + 0.06 * out_cubic(x)
        f = Image.new("RGB", (W, H), INK); l = ls.resize((round(500 * s), round(400 * s)), Image.LANCZOS)
        f.paste(l, ((W - l.width) // 2, (H - l.height) // 2))
    else:
        f = Image.new("RGB", (W, H), INK)
        for i in range(3):
            if t < pops[i]: continue
            fr = nextframe(i); x = min(1, (t - pops[i]) / POP)
            s = 0.90 + 0.10 * out_back(x); dy = round(70 * (1 - out_cubic(x))); a = min(1, (t - pops[i]) / 0.12)
            c = fr if s == 1 else fr.resize((round(CW * s), round(CH * s)), Image.BILINEAR)
            px, py = X + (CW - c.width) // 2, YS[i] + (CH - c.height) // 2 + dy
            if a < 1: c = Image.blend(Image.new("RGB", c.size, INK), c, a)
            f.paste(c, (px, py))
    fo.stdin.write(f.tobytes())
fo.stdin.close(); fo.wait()
