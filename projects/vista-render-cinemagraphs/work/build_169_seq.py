"""16:9 full-frame reel: clips one after another, hard cuts, shutter on every cut, each clip's own ambience under it,
optional music bed, hard cut to the 16:9 Salisbury card with click+thud. Optional whoosh peaking on every cut. 0 credits.
usage: build_169_seq.py out.mp4 music.mp3|none p1,p2,p3,cut clip:amb clip:amb clip:amb [whoosh.mp3]"""
import sys, subprocess
out, music = sys.argv[1], sys.argv[2]; P = [float(x) for x in sys.argv[3].split(",")]
pairs = [a.split(":") for a in sys.argv[4:7]]; whoosh = sys.argv[7] if len(sys.argv) > 7 else None
CUT = P[3]; TOT = CUT + 3.0; ends = [P[1], P[2], CUT]; WPEAK = 0.40  # whoosh_simple loudest point
inp = ["-f", "lavfi", "-i", f"color=c=0x0b0b0a:s=1920x1080:r=50:d={TOT}"]
for c, _ in pairs: inp += ["-i", f"work/slow75/{c}.mp4"]
inp += ["-loop", "1", "-framerate", "50", "-t", str(TOT), "-i", "deliver/endcard/salisbury_endcard_169.png"]
n = 5; idx = {}
def add(key, *a):
    global n; inp.extend(a); idx[key] = n; n += 1
for k, f in [("shut", "deliver/sfx/00_popin_shutter.wav"), ("click", "assets/sfx/click_5.wav"), ("thud", "assets/sfx/thud_4.wav")]: add(k, "-i", f)
for i, (_, a) in enumerate(pairs): add(f"amb{i}", "-i", a)
if music != "none": add("music", "-i", music)
if whoosh: add("whoosh", "-i", whoosh)
fc = []; prev = "0"
for i in range(3):
    fc.append(f"[{i+1}]setpts=PTS-STARTPTS+{P[i]}/TB[c{i}]")
    fc.append(f"[{prev}][c{i}]overlay=0:0:eof_action=repeat:enable='between(t,{P[i]},{ends[i]}-0.001)'[o{i}]"); prev = f"o{i}"
fc.append(f"[{prev}][4]overlay=0:0:enable='gte(t,{CUT})',format=yuv420p[v]")
fc.append(f"anullsrc=r=48000:cl=stereo,atrim=0:{TOT}[base]"); mix = ["[base]"]
if music != "none":
    fc.append(f"[{idx['music']}]atrim=0:{TOT},asetpts=PTS-STARTPTS,afade=in:st=0:d=0.5,afade=out:st={TOT-2.2}:d=2.2,loudnorm=I=-17:TP=-2,volume=0.85[m]"); mix.append("[m]")
fc.append(f"[{idx['shut']}]asplit=3[k0][k1][k2]")
for i in range(3):
    d = int(P[i] * 1000); fc.append(f"[k{i}]adelay={d}|{d},volume=0.9[s{i}]"); mix.append(f"[s{i}]")
    dur = ends[i] - P[i] + 0.25
    fc.append(f"[{idx[f'amb{i}']}]atrim=0:{dur},asetpts=PTS-STARTPTS,afade=in:st=0:d=0.12,afade=out:st={dur-0.4}:d=0.4,volume={0.6 if music != 'none' else 0.5},adelay={d}|{d}[a{i}]"); mix.append(f"[a{i}]")
d = int(CUT * 1000)
fc.append(f"[{idx['click']}]adelay={d}|{d},volume=0.7[l1]"); fc.append(f"[{idx['thud']}]adelay={d}|{d},volume=0.6[l2]"); mix += ["[l1]", "[l2]"]
if whoosh:
    fc.append(f"[{idx['whoosh']}]aformat=channel_layouts=stereo,volume=1.0,asplit=4[w0][w1][w2][w3]")
    for i, t in enumerate(P):
        d = max(0, int((t - WPEAK) * 1000)); fc.append(f"[w{i}]adelay={d}|{d}[ww{i}]"); mix.append(f"[ww{i}]")
fc.append(f"{''.join(mix)}amix=inputs={len(mix)}:normalize=0:duration=first,alimiter=limit=0.89[aout]")
subprocess.run(["ffmpeg", "-v", "error", "-y", *inp, "-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[aout]",
    "-c:v", "libx264", "-crf", "16", "-preset", "slow", "-c:a", "aac", "-b:a", "256k", "-ar", "48000",
    "-movflags", "+faststart", "-t", str(TOT), out], check=True, stdin=subprocess.DEVNULL)
