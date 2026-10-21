"""Reel with full sound design: postcard layout, shutter pop-ins, each card brings its own ambience in at its pop
(ambience loops under the rest of the reel), music bed, shutter+thump on the logo. 0 credits.
usage: build_reel_sfx.py out.mp4 music.mp3 p1,p2,p3,cut clipA:amb.wav clipB:amb.wav clipC:amb.wav"""
import sys, subprocess
out, music, P = sys.argv[1], sys.argv[2], [float(x) for x in sys.argv[3].split(",")]
pairs = [a.split(":") for a in sys.argv[4:7]]
POPS, CUT = P[:3], P[3]; TOT = CUT + 3.0
X, W_, H_, YS = 37, 1006, 566, [64, 678, 1290]
SH = "deliver/sfx/00_popin_shutter.wav"
inp = ["-f", "lavfi", "-i", f"color=c=0x0b0b0a:s=1080x1920:r=50:d={TOT}"]
for c, _ in pairs: inp += ["-i", f"work/slow3/{c}.mp4"]
inp += ["-loop", "1", "-framerate", "50", "-t", str(TOT), "-i", "assets/endcard_postcard_916.png", "-i", music, "-i", SH]
for _, a in pairs: inp += ["-stream_loop", "-1", "-i", a]
fc = []; prev = "0"
for i in range(3):
    fc.append(f"[{i+1}]scale={W_}:{H_}:flags=lanczos,unsharp=5:5:0.3,setpts=PTS-STARTPTS+{POPS[i]}/TB[c{i}]")
    fc.append(f"[{prev}][c{i}]overlay={X}:{YS[i]}:eof_action=repeat:enable='between(t,{POPS[i]},{CUT})'[o{i}]"); prev = f"o{i}"
fc.append(f"[{prev}][4]overlay=0:0:enable='gte(t,{CUT})',format=yuv420p[v]")
fc.append(f"[5]atrim=0:{TOT},asetpts=PTS-STARTPTS,afade=in:st=0:d=0.6,afade=out:st={TOT-2.2}:d=2.2,loudnorm=I=-17:TP=-2,volume=0.85[m]")
fc.append("[6]asplit=4[k0][k1][k2][k3]")
mix = "[m]"
for i, t in enumerate(POPS + [CUT]):
    d = int(t * 1000); fc.append(f"[k{i}]adelay={d}|{d},volume={0.9 if i < 3 else 1.0}[s{i}]"); mix += f"[s{i}]"
for i in range(3):  # ambience: in at its card's pop, out with the logo
    d = int(POPS[i] * 1000); dur = CUT - POPS[i] + 0.8
    fc.append(f"[{7+i}]atrim=0:{dur},asetpts=PTS-STARTPTS,afade=in:st=0:d=0.15,afade=out:st={dur-0.9}:d=0.9,volume={[0.55,0.5,0.5][i]},adelay={d}|{d}[a{i}]"); mix += f"[a{i}]"
fc.append(f"{mix}amix=inputs=8:normalize=0:duration=first,alimiter=limit=0.89[aout]")
subprocess.run(["ffmpeg", "-v", "error", "-y", *inp, "-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[aout]",
    "-c:v", "libx264", "-crf", "16", "-preset", "slow", "-c:a", "aac", "-b:a", "256k", "-ar", "48000",
    "-movflags", "+faststart", "-t", str(TOT), out], check=True, stdin=subprocess.DEVNULL)
