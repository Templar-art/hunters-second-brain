"""Build a 3D LUT (.cube) that moves one film's colour statistics toward a reference's.

Method: per-channel quantile mapping of L* (tone curve: blacks, contrast, highlights) plus
mean/spread transfer of a*/b* per tonal band (shadows / mids / highs), blended at `strength`.
Statistics come from frames of both films, so the LUT is global: it can't know a shot is a
bathroom; strong content differences (Desire has water and dusk) aren't something a LUT can
add. Output loads in Final Cut Pro (Custom LUT effect) or DaVinci."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np  # noqa: E402

import measure  # noqa: E402


def lab_to_rgb(L, a, b):
    fy = (L + 16) / 116
    fx, fz = fy + a / 500, fy - b / 200
    def inv(t):
        return np.where(t ** 3 > 0.008856, t ** 3, (t - 16 / 116) / 7.787)
    xyz = np.stack([inv(fx) * 0.95047, inv(fy), inv(fz) * 1.08883], -1)
    m = np.array([[3.2406, -1.5372, -0.4986], [-0.9689, 1.8758, 0.0415], [0.0557, -0.2040, 1.0570]])
    c = np.clip(xyz @ m.T, 0, 1)
    return np.where(c <= 0.0031308, 12.92 * c, 1.055 * c ** (1 / 2.4) - 0.055)


def build(source_video, reference_video, out_cube, strength=0.6, size=33):
    S = measure.lab(measure.frames(source_video))
    R = measure.lab(measure.frames(reference_video))
    qs = np.linspace(0, 100, 101)
    Ls, Lr = np.percentile(S[0], qs), np.percentile(R[0], qs)
    bands = [(0, 25), (25, 70), (70, 101)]
    stats = []
    for lo, hi in bands:
        ms, mr = (S[0] >= lo) & (S[0] < hi), (R[0] >= lo) & (R[0] < hi)
        stats.append(((S[1][ms].mean(), S[1][ms].std() + 1e-6, S[2][ms].mean(), S[2][ms].std() + 1e-6),
                      (R[1][mr].mean(), R[1][mr].std() + 1e-6, R[2][mr].mean(), R[2][mr].std() + 1e-6)))
    centres = np.array([12.5, 47.5, 85.0])

    g = np.linspace(0, 1, size)
    bb, gg, rr = np.meshgrid(g, g, g, indexing="ij")  # .cube order: red fastest
    rgb = np.stack([rr, gg, bb], -1).reshape(-1, 3)
    L, a, b = measure.lab(rgb)
    L2 = np.interp(L, Ls, Lr)
    # Per-band a/b transfer, blended smoothly across L by distance to band centres.
    w = np.exp(-((L[:, None] - centres[None, :]) / 18) ** 2)
    w /= w.sum(1, keepdims=True)
    a2 = np.zeros_like(a)
    b2 = np.zeros_like(b)
    for k, ((sa, ssa, sb, ssb), (ra, rsa, rb, rsb)) in enumerate(stats):
        a2 += w[:, k] * ((a - sa) * (rsa / ssa) + ra)
        b2 += w[:, k] * ((b - sb) * (rsb / ssb) + rb)
    Lo = L + strength * (L2 - L)
    ao = a + strength * (a2 - a)
    bo = b + strength * (b2 - b)
    out = lab_to_rgb(Lo, ao, bo)
    with open(out_cube, "w") as fh:
        fh.write(f'TITLE "Desire match {int(strength * 100)}%"\nLUT_3D_SIZE {size}\nDOMAIN_MIN 0 0 0\nDOMAIN_MAX 1 1 1\n')
        for r_, g_, b_ in out:
            fh.write(f"{r_:.6f} {g_:.6f} {b_:.6f}\n")
    return out_cube


if __name__ == "__main__":
    src, ref, out = sys.argv[1:4]
    strength = float(sys.argv[4]) if len(sys.argv) > 4 else 0.6
    print(build(src, ref, out, strength))
