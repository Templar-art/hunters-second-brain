"""Leaf-shadow dapple over the powder-room wall sun patch. 0 credits.
Mask = bright pixels (sun patch) on the left wall in the still; animated leaf texture
sways (sinusoidal offsets, two layers) and darkens the patch inside the mask only."""
import sys, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFilter
SRC, STILL, OUT = sys.argv[1:4]
W, H, FPS = 1920, 1080, 50
still = np.asarray(Image.open(STILL).convert("L").resize((W, H)), float)
m = np.clip((still - 190) / 35, 0, 1)
m[:, 600:] = 0
mask = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(6)), float) / 255
Image.fromarray((mask * 255).astype(np.uint8)).save("work/powder_mask.png")

rng = np.random.default_rng(7)
def leaves(n, size, blur):
    T = Image.new("L", (W + 400, H + 400), 0); d = ImageDraw.Draw(T)
    for _ in range(n):
        x, y = rng.uniform(0, W + 400), rng.uniform(0, H + 400)
        r = rng.uniform(*size); ang = rng.uniform(0, np.pi)
        pts = [(x + r * np.cos(t) * np.cos(ang) - 0.45 * r * np.sin(t) * np.sin(ang),
                y + r * np.cos(t) * np.sin(ang) + 0.45 * r * np.sin(t) * np.cos(ang)) for t in np.linspace(0, 2 * np.pi, 16)]
        d.polygon(pts, fill=255)
    return np.asarray(T.filter(ImageFilter.GaussianBlur(blur)), float) / 255
L1 = leaves(900, (18, 40), 7)   # near leaves, sharper
L2 = leaves(600, (30, 70), 16)  # far canopy, softer
ff = subprocess.Popen(["ffmpeg", "-v", "error", "-i", SRC, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
fo = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                       "-c:v", "libx264", "-crf", "16", "-preset", "slow", "-pix_fmt", "yuv420p", "-movflags", "+faststart", OUT], stdin=subprocess.PIPE)
def sub(L, dx, dy):  # subpixel shift (bilinear) so the sway glides instead of stepping
    x0, y0 = int(dx), int(dy); fx, fy = dx - x0, dy - y0
    c = lambda y, x: L[y:y + H, x:x + W]
    return ((1 - fy) * ((1 - fx) * c(y0, x0) + fx * c(y0, x0 + 1)) + fy * ((1 - fx) * c(y0 + 1, x0) + fx * c(y0 + 1, x0 + 1)))
i = 0
while True:
    buf = ff.stdout.read(W * H * 3)
    if len(buf) < W * H * 3: break
    f = np.frombuffer(buf, np.uint8).reshape(H, W, 3).astype(float)
    t = i / FPS
    dx1 = 200 + 22 * np.sin(2 * np.pi * t / 2.3) + 8 * np.sin(2 * np.pi * t / 0.9)
    dy1 = 200 + 10 * np.sin(2 * np.pi * t / 3.1 + 1)
    dx2 = 200 + 12 * np.sin(2 * np.pi * t / 3.7 + 2)
    dy2 = 200 + 6 * np.sin(2 * np.pi * t / 4.3)
    s1 = sub(L1, dx1, dy1); s2 = sub(L2, dx2, dy2)
    shadow = np.clip(0.55 * s1 + 0.35 * s2, 0, 0.75) * mask
    f *= (1 - 0.45 * shadow)[..., None] * np.array([1.0, 0.99, 0.97])[None, None, :] ** shadow[..., None]
    fo.stdin.write(np.clip(f, 0, 255).astype(np.uint8).tobytes()); i += 1
fo.stdin.close(); fo.wait(); print("frames", i)
