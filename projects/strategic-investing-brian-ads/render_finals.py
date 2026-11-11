"""Full-res 4K vertical finals from edl.json (A wide / B close, A-cam audio). Ungraded."""
import json, subprocess, sys
from pathlib import Path
OUT = Path(__file__).parent / "finals"; OUT.mkdir(exist_ok=True)
A = "/Volumes/Kristian T7/Brian Ads/A7siii 1/C8202.MP4"
B = "/Volumes/Kristian T7/Brian Ads/A7siii 2/C9731.MP4"
B_OFF_F = round(63.52 * 25)
for name, segs in json.load(open(Path(__file__).parent / "edl.json")).items():
    args, fc = ["ffmpeg", "-v", "error", "-y"], ""
    for i, (f0, f1, cam) in enumerate(segs):
        vs = (f0 if cam == "A" else f0 - B_OFF_F) / 25
        args += ["-ss", f"{vs:.3f}", "-t", f"{(f1-f0)/25:.3f}", "-i", A if cam == "A" else B,
                 "-ss", f"{f0/25:.3f}", "-t", f"{(f1-f0)/25:.3f}", "-i", A]
        fc += f"[{2*i}:v]scale=2160:3840,setsar=1,fps=25[v{i}];[{2*i+1}:a]aresample=48000[a{i}];"
    n = len(segs)
    fc += "".join(f"[v{i}][a{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=1[v][a]"
    out = OUT / f"Brian {name} AB.mp4"
    subprocess.run(args + ["-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-b:v", "45M", "-maxrate", "60M", "-bufsize", "90M", "-preset", "medium", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-c:a", "aac", "-b:a", "320k", str(out)], check=True)
    print("ok", out.name)
