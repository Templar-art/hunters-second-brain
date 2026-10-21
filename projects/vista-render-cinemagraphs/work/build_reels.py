"""Salisbury postcard reels v4. Hard click-ins spaced out (no pop animation, no dissolves, no fade to black),
clips at 0.5x (work/slow2), click SFX per card, click+thud on the logo, royalty-free lofi bed (Pixabay) + soft wind.
3 cards: Solis-reference geometry (x37 1006x566, y 64/678/1290). 4 cards: 800x450 centred, 24px gaps.
usage: build_reels.py out.mp4 music.mp3 music_start clip1 clip2 clip3 [clip4]     0 credits."""
import sys, subprocess, os
out, music, mst, clips = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]
n = len(clips)
if n == 3: W_, H_, X, YS, POPS, CUT = 1006, 566, 37, [64, 678, 1290], [0.5, 3.5, 6.5], 10.4
else:      W_, H_, X, YS, POPS, CUT = 800, 450, 140, [24 + i * 474 for i in range(4)], [0.5, 3.0, 5.5, 8.0], 11.0
if os.environ.get("POPS"):  # music-synced times from work/sync_pops.py: p1,p2,p3,cut
    v = [float(x) for x in os.environ["POPS"].split(",")]; POPS, CUT = v[:-1], v[-1]
TOT = CUT + 3.0
WIND = "/Users/10xhunter/Downloads/traian1984-ambience-wind-blowing-through-trees-01-186986.mp3"
inp = ["-f", "lavfi", "-i", f"color=c=0x0b0b0a:s=1080x1920:r=50:d={TOT}"]
for c in clips: inp += ["-i", f"{os.environ.get("SLOWDIR", "work/slow2")}/{c}.mp4"]
inp += ["-loop", "1", "-framerate", "50", "-t", str(TOT), "-i", "assets/endcard_postcard_916.png",
        "-ss", mst, "-i", music, "-i", WIND, "-i", "assets/sfx/click_1.wav", "-i", "assets/sfx/click_5.wav", "-i", "assets/sfx/thud_4.wav"]
L, M, Wd, K, K5, T4 = n + 1, n + 2, n + 3, n + 4, n + 5, n + 6
fc = []; prev = "0"
for i in range(n):
    fc.append(f"[{i+1}]scale={W_}:{H_}:flags=lanczos,unsharp=5:5:0.3,setpts=PTS-STARTPTS+{POPS[i]}/TB[c{i}]")
    fc.append(f"[{prev}][c{i}]overlay={X}:{YS[i]}:eof_action=repeat:enable='between(t,{POPS[i]},{CUT})'[o{i}]"); prev = f"o{i}"
fc.append(f"[{prev}][{L}]overlay=0:0:enable='gte(t,{CUT})',format=yuv420p[v]")
fc.append(f"[{M}]atrim=0:{TOT},asetpts=PTS-STARTPTS,afade=in:st=0:d=0.6,afade=out:st={TOT-2.2}:d=2.2,loudnorm=I=-16:TP=-2[m]")
fc.append(f"[{Wd}]atrim=0:{TOT},asetpts=PTS-STARTPTS,volume=0.12,afade=out:st={TOT-2.2}:d=2.2[w]")
fc.append(f"[{K}]asplit={n}" + "".join(f"[k{i}]" for i in range(n)))
mix = "[m][w]"
for i in range(n):
    d = int(POPS[i] * 1000); fc.append(f"[k{i}]adelay={d}|{d},volume=0.55[s{i}]"); mix += f"[s{i}]"
d = int(CUT * 1000)
fc.append(f"[{K5}]adelay={d}|{d},volume=0.7[l1]"); fc.append(f"[{T4}]adelay={d}|{d},volume=0.6[l2]")
fc.append(f"{mix}[l1][l2]amix=inputs={n+4}:normalize=0:duration=first,alimiter=limit=0.89[a]")
subprocess.run(["ffmpeg", "-v", "error", "-y", *inp, "-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]",
    "-c:v", "libx264", "-crf", "16", "-preset", "slow", "-c:a", "aac", "-b:a", "256k", "-ar", "48000",
    "-movflags", "+faststart", "-t", str(TOT), out], check=True)
