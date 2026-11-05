"""Person mattes → build/matte/mNNNN.png (alpha = person).
Usage: matte.py <build_dir> [a-b ...]  (optional second ranges; default every frame)"""
import glob, os, sys
from PIL import Image
from rembg import new_session, remove

build = sys.argv[1]; os.makedirs(f"{build}/matte", exist_ok=True)
session = new_session("u2net_human_seg")
frames = sorted(glob.glob(f"{build}/frames/f*.jpg"))
if len(sys.argv) > 2:                                   # only frames inside the given second ranges (30fps)
    rng = [tuple(map(float, r.split("-"))) for r in sys.argv[2:]]
    frames = [f for f in frames if any(a <= (int(os.path.basename(f)[1:5]) - 1) / (24000/1001) <= b for a, b in rng)]
for i, f in enumerate(frames):
    dst = f"{build}/matte/m{os.path.basename(f)[1:5]}.png"
    if os.path.exists(dst): continue
    m = remove(Image.open(f), session=session, only_mask=True)
    a = Image.new("RGBA", m.size, (255, 255, 255, 0)); a.putalpha(m); a.save(dst)
    if i % 50 == 0: print(f"matte {i}/{len(frames)}", flush=True)
