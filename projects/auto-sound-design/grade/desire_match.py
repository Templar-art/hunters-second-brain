"""Match a 10x film to a reference film's look, shot type by shot type.

Why per type: a single film-wide match copies the reference's *mix of shots*. Desire has a lot of dusk and
night, so a global match made Kollosche "just dark" (Hunter, 28 Oct). Matching interiors to Desire's
interiors, exteriors to exteriors, aerials to aerials and dusk to dusk copies the *treatment*, not the content.

Per group it builds a 3D LUT (.cube): L* tone curve by quantile mapping, with the source's own midtone
anchored (keep_mid) so exposure doesn't drop, plus per-band (shadow/mid/high) a*/b* mean+spread transfer.
Strength blends toward the reference. Then it renders a preview with each shot through its group's LUT.

  python3 grade/desire_match.py SRC.mp4 --src-groups src.json REF.mp4 --ref-groups ref.json [--strength 0.8]
Group files: {"grade_segments": [{"start", "end", "label"}]}, or a scene map (its labels are folded into groups).
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))
import numpy as np  # noqa: E402

import measure  # noqa: E402
from transfer import lab_to_rgb  # noqa: E402
from asd import media  # noqa: E402

FOLD = {"exterior": "exterior", "balcony": "exterior", "aerial": "aerial", "dusk": "dusk", "night": "dusk",
        "night_interior": "dusk", "golden": "dusk", "interior": "interior", "bathroom": "interior",
        "presenter": "interior", "endcard": None, "title": None}


def load_groups(path, presenter_outdoor=()):
    data = json.loads(Path(path).read_text())
    segs = data.get("grade_segments") or data.get("segments")
    out = []
    for s in segs:
        label = s["label"]
        if label == "presenter" and any(abs(s["start"] - t) < 0.5 for t in presenter_outdoor):
            label = "exterior"
        group = FOLD.get(label, label)
        if group:
            out.append((float(s["start"]), float(s["end"]), group))
    return out


def sample(path, segs, per_shot=4, w=240, h=135):
    """Frames from the middle 60% of each shot, grouped."""
    frames = {}
    for a, b, g in segs:
        for k in range(per_shot):
            t = a + (b - a) * (0.2 + 0.6 * k / max(1, per_shot - 1))
            raw = media._run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(path), "-frames:v", "1",
                              "-vf", f"scale={w}:{h},format=rgb24", "-f", "rawvideo", "-"], binary=True)
            if len(raw) == w * h * 3:
                frames.setdefault(g, []).append(np.frombuffer(raw, np.uint8).reshape(h, w, 3).astype(np.float32) / 255)
    return {g: np.stack(v) for g, v in frames.items()}


# Per shot type tuning after Hunter's review (28 Oct): "inside too dark, outside too bright, drone far away".
#   keep_mid: 1 = our midtone stays put, 0 = take the reference's; mid_shift: extra L* in the midtones (+ = brighter).
GROUP_TUNING = {
    "interior": {"strength": 0.8, "keep_mid": 1.0, "mid_shift": +5.0, "high_shift": 0.0},
    "exterior": {"strength": 0.8, "keep_mid": 1.0, "mid_shift": -3.0, "high_shift": -5.0},
    # Desire's aerials are golden-hour water and dusk sky: take their contrast, not their colour.
    "aerial": {"strength": 0.8, "colour": 0.25, "keep_mid": 0.75, "mid_shift": 0.0, "high_shift": -6.0},
    "dusk": {"strength": 0.8, "keep_mid": 1.0, "mid_shift": 0.0, "high_shift": 0.0},
}


def build_lut(src, ref, out_cube, strength=0.8, keep_mid=1.0, size=33, title="match", mid_shift=0.0, high_shift=0.0,
              colour=None):
    S, R = measure.lab(src), measure.lab(ref)
    qs = np.linspace(0, 100, 101)
    Ls, Lr = np.percentile(S[0], qs), np.percentile(R[0], qs)
    # Shift the reference curve so our midtone stays put (keep_mid=1) or partly moves (0..1).
    Lr = Lr + float(keep_mid) * (np.percentile(S[0], 50) - np.percentile(R[0], 50))
    centres = np.array([12.5, 47.5, 85.0])
    stats = []
    for lo, hi in [(0, 25), (25, 70), (70, 101)]:
        ms, mr = (S[0] >= lo) & (S[0] < hi), (R[0] >= lo) & (R[0] < hi)
        if ms.sum() < 50 or mr.sum() < 50:
            stats.append(None)
            continue
        stats.append(((S[1][ms].mean(), S[1][ms].std() + 1e-6, S[2][ms].mean(), S[2][ms].std() + 1e-6),
                      (R[1][mr].mean(), R[1][mr].std() + 1e-6, R[2][mr].mean(), R[2][mr].std() + 1e-6)))
    g = np.linspace(0, 1, size)
    bb, gg, rr = np.meshgrid(g, g, g, indexing="ij")
    rgb = np.stack([rr, gg, bb], -1).reshape(-1, 3)
    L, a, b = measure.lab(rgb)
    L2 = np.interp(L, Ls, Lr)
    L2 = L2 + mid_shift * np.exp(-((L - 50) / 28) ** 2)  # bell: moves mids, spares black/white
    L2 = np.clip(L2 + high_shift * np.clip((L - 70) / 25, 0, 1) ** 1.5, 0, 100)  # roll off bright roofs/sky
    w = np.exp(-((L[:, None] - centres[None, :]) / 18) ** 2)
    for k, st in enumerate(stats):
        if st is None:
            w[:, k] = 0
    w /= np.maximum(w.sum(1, keepdims=True), 1e-9)
    a2, b2 = a.copy() * (w.sum(1) == 0), b.copy() * (w.sum(1) == 0)
    for k, st in enumerate(stats):
        if st is None:
            continue
        (sa, ssa, sb, ssb), (ra, rsa, rb, rsb) = st
        a2 += w[:, k] * ((a - sa) * min(1.5, rsa / ssa) + ra)
        b2 += w[:, k] * ((b - sb) * min(1.5, rsb / ssb) + rb)
    cs = strength if colour is None else colour  # colour transfer can be weaker than tone transfer
    out = lab_to_rgb(L + strength * (L2 - L), a + cs * (a2 - a), b + cs * (b2 - b))
    with open(out_cube, "w") as fh:
        fh.write(f'TITLE "{title}"\nLUT_3D_SIZE {size}\nDOMAIN_MIN 0 0 0\nDOMAIN_MAX 1 1 1\n')
        for r_, g_, b_ in out:
            fh.write(f"{r_:.6f} {g_:.6f} {b_:.6f}\n")
    return out_cube


def render(src, segs, luts, out_path, audio_from=None, workdir=None):
    """Each shot through its group's LUT (frame-accurate segments), concatenated, audio laid back."""
    video, _ = media.video_info(src)
    fps = float(video.fps)
    work = Path(workdir or Path(out_path).parent / ".segments")
    work.mkdir(parents=True, exist_ok=True)
    total = video.frame_count
    # Cover the whole film: gaps (title/endcard) pass through ungraded.
    bounds = sorted({0, total, *[int(round(a * fps)) for a, _, _ in segs], *[int(round(b * fps)) for _, b, _ in segs]})
    listing = []
    for i, (f0, f1) in enumerate(zip(bounds, bounds[1:])):
        if f1 <= f0:
            continue
        mid = (f0 + f1) / 2 / fps
        group = next((g for a, b, g in segs if a <= mid < b), None)
        vf = f"lut3d=file='{luts[group]}'" if group in luts else "null"
        seg = work / f"seg{i:04d}.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{f0 / fps:.6f}", "-i", str(src), "-frames:v", str(f1 - f0),
                        "-vf", vf, "-an", "-c:v", "libx264", "-crf", "16", "-preset", "fast", "-pix_fmt", "yuv420p",
                        "-r", str(video.fps), str(seg)], check=True)
        listing.append(f"file '{seg.name}'")
    (work / "list.txt").write_text("\n".join(listing) + "\n")
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(work / "list.txt")]
    cmd += ["-i", str(audio_from or src), "-map", "0:v", "-map", "1:a:0?", "-c:v", "copy", "-c:a", "copy", "-shortest", str(out_path)]
    subprocess.run(cmd, check=True)
    return out_path


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("src")
    p.add_argument("--src-groups", required=True)
    p.add_argument("ref")
    p.add_argument("--ref-groups", required=True)
    p.add_argument("--strength", type=float, default=0.8)
    p.add_argument("--no-keep-mid", action="store_true")
    p.add_argument("--presenter-outdoor", default="", help="start times of presenter segments shot outside")
    p.add_argument("--audio-from", help="take the preview's audio from this file (e.g. the SOUND-MIX)")
    p.add_argument("--out")
    args = p.parse_args(argv)
    outdoor = [float(x) for x in args.presenter_outdoor.split(",") if x]
    src_segs, ref_segs = load_groups(args.src_groups, outdoor), load_groups(args.ref_groups)
    out = Path(args.out or HERE.parent / "output" / f"{Path(args.src).stem}_desire-match")
    out.mkdir(parents=True, exist_ok=True)
    S, R = sample(args.src, src_segs), sample(args.ref, ref_segs)
    luts, report = {}, {}
    for g in S:
        if g not in R:
            report[g] = "no reference shots of this type: left as is"
            continue
        cube = out / f"{Path(args.src).stem}_{g}_desire-{int(args.strength * 100)}.cube"
        t = GROUP_TUNING.get(g, {"strength": args.strength, "keep_mid": 1.0, "mid_shift": 0.0})
        build_lut(S[g], R[g], cube, t["strength"], keep_mid=0.0 if args.no_keep_mid else t["keep_mid"],
                  title=f"Desire match {g}", mid_shift=t["mid_shift"], high_shift=t.get("high_shift", 0.0),
                  colour=t.get("colour"))
        luts[g] = cube
        report[g] = {"src_frames": len(S[g]), "ref_frames": len(R[g]), "lut": cube.name, "tuning": t}
    preview = render(args.src, src_segs, luts, out / f"{Path(args.src).stem}_DESIRE-MATCH-{int(args.strength * 100)}.mp4",
                     audio_from=args.audio_from)
    (out / "desire-match.json").write_text(json.dumps({"strength": args.strength, "groups": report}, indent=1))
    print(json.dumps(report, indent=1))
    print(f"preview -> {preview}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
