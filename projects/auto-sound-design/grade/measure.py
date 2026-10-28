"""Colour stats (CIELAB) for a video or a graded test: black floor, contrast, saturation, casts."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import numpy as np  # noqa: E402

from asd import media  # noqa: E402


def frames(path, vf="", w=192, h=108, fps=2):
    chain = (vf + "," if vf else "") + f"fps={fps},scale={w}:{h},format=rgb24"
    raw = media._run(["ffmpeg", "-v", "error", "-i", str(path), "-vf", chain, "-f", "rawvideo", "-"], binary=True)
    f = np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3).astype(np.float32) / 255
    return f[f.mean((1, 2, 3)) > 0.05]


def lab(rgb):
    c = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    m = np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]])
    xyz = c @ m.T / np.array([0.95047, 1.0, 1.08883])
    f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16 / 116)
    return 116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])


def stats(path, vf=""):
    L, a, b = lab(frames(path, vf))
    C = np.hypot(a, b)
    out = {"black_p10": np.percentile(L, 10), "mid_p50": np.percentile(L, 50), "high_p90": np.percentile(L, 90),
           "contrast": np.percentile(L, 90) - np.percentile(L, 10), "chroma": C.mean()}
    for lo, hi, k in [(0, 25, "shadow"), (25, 70, "mid"), (70, 101, "high")]:
        sel = (L >= lo) & (L < hi)
        out[f"{k}_b"] = b[sel].mean() if sel.any() else 0.0
        out[f"{k}_a"] = a[sel].mean() if sel.any() else 0.0
    hue = (np.degrees(np.arctan2(b, a)) + 360) % 360
    sat = C > 15
    out["cool_share"] = ((hue[sat] > 180) & (hue[sat] < 315)).mean() if sat.any() else 0.0
    return out


if __name__ == "__main__":
    for p in sys.argv[1:]:
        s = stats(p)
        print(Path(p).name, " ".join(f"{k} {v:.1f}" if k != "cool_share" else f"{k} {v:.2f}" for k, v in s.items()))
