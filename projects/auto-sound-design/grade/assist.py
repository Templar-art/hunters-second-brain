"""Grade assistant: shot-by-shot balance + consistency suggestions for a graded-master (Path A)
workflow, expressed as numbers you can type into DaVinci Resolve's Primaries (Gain R/G/B).

It does what a colourist does first on the scopes, and nothing creative:
  * white balance: finds near-neutral bright surfaces (walls, ceilings, linen) and measures their
    colour cast; suggests RGB gains that pull them toward neutral (partially: warmth is kept);
  * exposure: compares each shot's midtone level with the film's typical level for that brightness
    class and nudges only outliers (never darkens a shot to chase a reference, never brightens a
    shot that is meant to be dark, e.g. dusk);
  * reports saturation outliers.
House rule (Hunter, 28 Oct 2026): keep his brightness; consistency first, any look subtle.

  python3 grade/assist.py "master.mov" [--out DIR] [--strength 0.6]
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))
import numpy as np  # noqa: E402

import sounddesign  # noqa: E402
from asd import analysis, media  # noqa: E402
import measure  # noqa: E402

W, H = 320, 180


def decode_rgb(path, w=W, h=H, lut=None):
    """Frames as RGB. For a flat/log master pass the camera's log->Rec.709 LUT, so shots are judged as
    they'll look after conversion (the Resolve CDL then sits after the conversion too)."""
    vf = (f"lut3d=file='{lut}'," if lut else "") + f"scale={w}:{h},format=rgb24"
    raw = media._run(["ffmpeg", "-v", "error", "-i", str(path), "-vf", vf, "-f", "rawvideo", "-"], binary=True)
    return np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3)


def to_linear(x):
    x = x / 255.0
    return np.where(x <= 0.04045, x / 12.92, ((x + 0.055) / 1.055) ** 2.4)


def lab_to_linear(L, a, b):
    fy = (L + 16) / 116
    fx, fz = fy + a / 500, fy - b / 200
    inv = lambda t: t ** 3 if t ** 3 > 0.008856 else (t - 16 / 116) / 7.787  # noqa: E731
    xyz = np.array([inv(fx) * 0.95047, inv(fy), inv(fz) * 1.08883])
    m = np.array([[3.2406, -1.5372, -0.4986], [-0.9689, 1.8758, 0.0415], [0.0557, -0.2040, 1.0570]])
    return np.clip(m @ xyz, 1e-6, None)


def timecode(t, fps):
    f = int(round(t * fps))
    n = round(fps)
    return f"{f // (3600 * n):02d}:{f // (60 * n) % 60:02d}:{f // n % 60:02d}:{f % n:02d}"


def analyse(path, strength=0.7, max_wb=0.06, max_stops=0.33, wb_tol_b=4.0, wb_tol_a=3.0, exp_tol_stops=0.3,
            scene_map=None, analysis_lut=None, heroes=None, clean_white=(0.5, 4.0), black_tol=4.0):
    """Match each shot to the film's OWN look (its typical white cast and white level), not to
    neutral: an already-graded warm film stays warm; only shots that drift from it get flagged."""
    video, _ = media.video_info(path)
    cfg = sounddesign.load_config()
    cuts = analysis.detect_cuts(video, cfg["analysis"])
    frames = decode_rgb(path, lut=analysis_lut)
    fps = float(video.fps)
    edges = [0.0] + [c.time for c in cuts] + [len(frames) / fps]
    shots = []
    for i, (a, b) in enumerate(zip(edges, edges[1:])):
        fa, fb = int(a * fps) + 1, max(int(a * fps) + 2, int(b * fps) - 1)
        idx = np.linspace(fa, fb - 1, 5).astype(int).clip(0, len(frames) - 1)
        sample = frames[idx].astype(np.float32)
        info = {"shot": i, "start": round(a, 3), "end": round(b, 3), "tc": timecode(a, fps)}
        label = scene_map.label_at((a + b) / 2) if scene_map else None
        info["scene"] = label
        if sample.mean() < 8:
            info["skip"] = "black or fade"
            shots.append(info)
            continue
        L, A, B = measure.lab(sample / 255.0)
        C = np.hypot(A, B)
        neutral = (L > 55) & (L < 97) & (C < 16)
        info.update({"median_L": float(np.median(L)), "black_L": float(np.percentile(L, 10)), "chroma": float(C.mean()),
                     "neutral_share": float(neutral.mean())})
        # White surfaces are only trustworthy indoors: outside, "white" is mostly sky and cloud,
        # and dusk is meant to be cool. With a scene map, compare interiors only.
        indoor = label in (None, "interior", "bathroom", "presenter") if scene_map else True
        if neutral.mean() > 0.03 and indoor:
            lin = to_linear(sample)[neutral]
            rgb = lin.mean(0)
            info.update({"white_a": float(A[neutral].mean()), "white_b": float(B[neutral].mean()),
                         "white_L": float(np.percentile(L[neutral], 90)),
                         "white_ratio": [float(rgb[0] / rgb[1]), float(rgb[2] / rgb[1])]})
        shots.append(info)

    # Reference look: the shots Hunter likes ("heroes"), or the film's median if none are picked.
    ref_shots = [s for s in shots if "white_ratio" in s and (not heroes or s["shot"] in heroes)]
    hero_shots = [s for s in shots if heroes and s["shot"] in heroes and "chroma" in s]
    exterior_mode = bool(heroes) and not ref_shots
    if exterior_mode:
        # Heroes are exteriors (no walls to read). Interiors are matched to a clean white with a hint of
        # warmth, keep their own brightness, and take the heroes' saturation and black level.
        target = np.array(lab_to_linear(90.0, clean_white[0], clean_white[1]))
        interiors = [s for s in shots if "white_ratio" in s]
        ref = {"white_a": clean_white[0], "white_b": clean_white[1],
               "white_L": float(np.median([s["white_L"] for s in interiors])) if interiors else 85.0,
               "rb": [float(target[0] / target[1]), float(target[2] / target[1])],
               "chroma": float(np.median([s["chroma"] for s in hero_shots])),
               "black_L": float(np.median([s["black_L"] for s in hero_shots]))}
    else:
        ref = None
    if ref is None:
        ref = {"white_a": float(np.median([s["white_a"] for s in ref_shots])) if ref_shots else 0.0,
           "white_b": float(np.median([s["white_b"] for s in ref_shots])) if ref_shots else 0.0,
           "white_L": float(np.median([s["white_L"] for s in ref_shots])) if ref_shots else 85.0,
           "rb": [float(np.median([s["white_ratio"][k] for s in ref_shots])) for k in (0, 1)] if ref_shots else [1, 1],
           "chroma": float(np.median([s["chroma"] for s in (hero_shots or [s for s in shots if "chroma" in s])])),
           "black_L": float(np.median([s["black_L"] for s in (hero_shots or [s for s in shots if "black_L" in s])]))}
    for s in shots:
        if "skip" in s:
            continue
        gains = np.ones(3)
        notes = []
        if "white_ratio" in s:
            db, da = s["white_b"] - ref["white_b"], s["white_a"] - ref["white_a"]
            if abs(db) > wb_tol_b or abs(da) > wb_tol_a:
                want = np.array([ref["rb"][0] / s["white_ratio"][0], 1.0, ref["rb"][1] / s["white_ratio"][1]])
                gains = np.clip(1 + strength * (want - 1), 1 - max_wb, 1 + max_wb)
                notes.append(f"whites {'warmer' if db > 0 else 'cooler'} than the reference ({db:+.1f} b*)"
                             + (f", {'magenta' if da > 0 else 'green'} {da:+.1f} a*" if abs(da) > wb_tol_a else ""))
            # Exposure judged on the white surfaces, so a dark-timber kitchen isn't "underexposed".
            y = lambda l: ((l + 16) / 116) ** 3  # noqa: E731
            stops = float(np.log2(y(ref["white_L"]) / y(s["white_L"])))
            if abs(stops) > exp_tol_stops:
                corr = float(np.clip(0.6 * stops, -0.15, max_stops))  # house rule: barely ever darken
                gains = gains * 2 ** corr
                notes.append(f"whites {abs(stops):.2f} stop {'under' if stops > 0 else 'over'} the reference level")
                s["exposure_stops"] = round(corr, 2)
        else:
            notes.append(f"{s.get('scene') or 'no white surfaces'}: not auto-matched; judge by eye against neighbours")
        s.setdefault("exposure_stops", 0.0)
        offset = 0.0
        if "white_ratio" in s and s["black_L"] - ref["black_L"] > black_tol:
            # Shadows more lifted than the reference: pull them down a touch (never crush: capped).
            offset = -float(np.clip((s["black_L"] - ref["black_L"]) / 100 * 0.4, 0, 0.03))
            notes.append(f"shadows lifted vs the reference (L {s['black_L']:.0f} vs {ref['black_L']:.0f})")
        s["resolve_offset"] = [round(offset, 4)] * 3
        if s["chroma"] > ref["chroma"] * 1.35:
            notes.append("noticeably more saturated than the reference: try Sat 45-48")
        elif s["chroma"] < ref["chroma"] * 0.65 and s.get("median_L", 50) > 35:
            notes.append("noticeably flatter than the reference: try Sat 55-58")
        s["resolve_gain"] = [round(float(x), 3) for x in gains]
        s["changed"] = bool(max(abs(x - 1) for x in s["resolve_gain"]) >= 0.015 or abs(offset) >= 0.005)
        s["note"] = "; ".join(notes)
    for s in shots:
        if heroes and s["shot"] in heroes:
            s["note"] = ("HERO (your pick, the reference). " + s.get("note", "")).strip()
            s["resolve_gain"], s["changed"], s["exposure_stops"] = [1.0, 1.0, 1.0], False, 0.0
            s["resolve_offset"] = [0.0, 0.0, 0.0]
    return video, frames, shots, {"exterior_heroes_mode": exterior_mode, "heroes": sorted(heroes) if heroes else None, "target_median_L": ref["white_L"], "median_chroma": ref["chroma"],
                                  "film_white_cast_b": ref["white_b"], "film_white_cast_a": ref["white_a"]}


def fcp_words(s):
    """Plain Final Cut instructions (Color Wheels on the clip). Amounts are words, not numbers:
    FCP's wheels don't map 1:1 to RGB gain, so set it by eye with the preview as the target."""
    if s.get("skip") or not s.get("changed"):
        return ""
    r, g, b = s["resolve_gain"]
    out = []
    stops = s.get("exposure_stops", 0.0)
    if abs(stops) >= 0.05:
        size = "a little" if abs(stops) < 0.2 else "noticeably"
        out.append(f"Master brightness {'up' if stops > 0 else 'down'} {size}")
    tint = g - (r + b) / 2
    if abs(r - b) >= 0.03:
        size = "a touch" if abs(r - b) < 0.08 else "clearly"
        out.append(f"Temperature {size} {'warmer' if r > b else 'cooler'}")
    if abs(tint) >= 0.03:
        out.append(f"Tint {'toward green' if tint > 0 else 'toward magenta'}")
    if s.get("resolve_offset", [0])[0] < -0.004:
        out.append("Shadows down a little (Shadows wheel brightness)")
    if "Sat 45-48" in s.get("note", ""):
        out.append("Master saturation down ~5-10%")
    elif "Sat 55-58" in s.get("note", ""):
        out.append("Master saturation up ~5-10%")
    return "Color Wheels: " + "; ".join(out) if out else ""


def apply(frames, shots, fps):
    out = frames.astype(np.float32).copy()
    for s in shots:
        if "skip" in s:
            continue
        a, b = int(round(s["start"] * fps)), int(round(s["end"] * fps))
        lin = to_linear(out[a:b])
        lin *= np.array(s["resolve_gain"], dtype=np.float32)
        lin += np.array(s.get("resolve_offset", [0, 0, 0]), dtype=np.float32) * 0.5  # rough preview of a CDL offset
        lin = np.clip(lin, 0, 1)
        out[a:b] = np.where(lin <= 0.0031308, 12.92 * lin, 1.055 * lin ** (1 / 2.4) - 0.055) * 255
    return out.clip(0, 255).astype(np.uint8)


def contact_sheet(video_path, out=None, lut=None):
    """Numbered thumbnail of every shot, so Hunter can say which ones he likes."""
    video, _ = media.video_info(video_path)
    cfg = sounddesign.load_config()
    cuts = analysis.detect_cuts(video, cfg["analysis"])
    edges = [0.0] + [c.time for c in cuts] + [video.duration]
    out = Path(out or (HERE.parent / "output" / f"{Path(video_path).stem}_grade-assist"))
    out.mkdir(parents=True, exist_ok=True)
    tiles = out / "tiles"
    tiles.mkdir(exist_ok=True)
    for i, (a, b) in enumerate(zip(edges, edges[1:])):
        vf = (f"lut3d=file='{lut}'," if lut else "") + (f"scale=320:-2,drawtext=text='{i:02d}':x=8:y=8:fontsize=28:"
                                                        "fontcolor=yellow:box=1:boxcolor=black@0.6")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{(a + b) / 2:.3f}", "-i", str(video_path), "-frames:v", "1",
                        "-vf", vf, str(tiles / f"s{i:03d}.png")], check=True)
    sheet = out / "shots-numbered.png"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(tiles / "s%03d.png"), "-vf", "tile=6x10",
                    "-frames:v", "1", str(sheet)], check=True)
    print(f"{len(edges) - 1} shots -> {sheet}")
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("video")
    p.add_argument("--out")
    p.add_argument("--strength", type=float, default=0.7)
    p.add_argument("--scenes", help="scene-map JSON: only interiors are auto-matched")
    p.add_argument("--analysis-lut", help="log->Rec.709 .cube for flat/log masters (judge shots after conversion)")
    p.add_argument("--heroes", help="shots you like, e.g. '3,8,15' (numbers from the contact sheet): the rest are matched to them")
    p.add_argument("--contact-sheet", action="store_true", help="just write a numbered contact sheet to pick heroes from")
    args = p.parse_args(argv)
    if args.contact_sheet:
        return contact_sheet(args.video, args.out, args.analysis_lut)
    from asd import scenes as scenes_mod
    smap = scenes_mod.load(args.scenes) if args.scenes else None
    heroes = {int(x) for x in args.heroes.split(",")} if args.heroes else None
    video, frames, shots, summary = analyse(args.video, args.strength, scene_map=smap, analysis_lut=args.analysis_lut,
                                            heroes=heroes)
    out = Path(args.out or (HERE.parent / "output" / f"{Path(args.video).stem}_grade-assist"))
    out.mkdir(parents=True, exist_ok=True)
    fps = float(video.fps)
    graded = apply(frames, shots, fps)

    # Preview at analysis size (fast), side by side: before | after.
    side = np.concatenate([frames, graded], axis=2)
    prev = out / "before-after_preview.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W * 2}x{H}",
                    "-r", str(video.fps), "-i", "-", "-i", str(video.path), "-map", "0:v", "-map", "1:a?",
                    "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", str(prev)],
                   input=side.tobytes(), check=True)
    # Stills of the shots that changed.
    changed = [s for s in shots if s.get("changed")]
    rows = []
    for s in changed[:16]:
        f = int(((s["start"] + s["end"]) / 2) * fps)
        rows.append(np.concatenate([frames[f], graded[f]], axis=1))
    if rows:
        sheet = np.concatenate(rows, axis=0)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s",
                        f"{sheet.shape[1]}x{sheet.shape[0]}", "-i", "-", str(out / "changed-shots_before-after.png")],
                       input=sheet.tobytes(), check=True)

    lines = [f"# Grade assistant: {Path(args.video).name}", "",
             "Consistency pass only (white balance on neutral surfaces + exposure outliers). Keeps your brightness.",
             ("Reference = your exterior hero shots " + str(summary['heroes']) + " for saturation and black level; interiors get clean "
              "whites with a hint of warmth and keep their own brightness: " if summary.get("exterior_heroes_mode") else
              f"Reference = your hero shots {summary['heroes']}: " if summary.get("heroes") else "Reference = the film's own typical look: ")
             + f"whites at L* {summary['target_median_L']:.1f}, cast b* {summary['film_white_cast_b']:+.1f}, "
             f"typical chroma {summary['median_chroma']:.1f}. Other shots are matched to that, not to neutral.", "",
             "Type these into **Resolve → Color → Primaries (bars) → Gain R / G / B** on each shot. "
             "Leave Lift/Gamma alone for this pass.", "",
             "**In Final Cut:** select the shot → Inspector → Color → add Color Wheels → follow the *Final Cut* column, "
             "matching the right side of the preview by eye.", "",
             "| Shot | TC in | Final Cut | Gain R | Gain G | Gain B | Exposure | White cast (b*) | Note |",
             "|---|---|---|---|---|---|---|---|---|"]
    for s in shots:
        if "skip" in s:
            lines.append(f"| {s['shot']:02d} | {s.get('tc', '')} | – | – | – | – | – | – | {s['skip']} |")
            continue
        r, g, b = s["resolve_gain"]
        cast = f"{s['white_b']:+.1f}" if "white_b" in s else "–"
        note = s["note"] or ("fine as is" if not s["changed"] else "")
        if not s["changed"] and "not auto-matched" not in note and "Sat" not in note:
            note = "fine as is"
        lines.append(f"| {s['shot']:02d} | {s['tc']} | {fcp_words(s) or '–'} | {r:.3f} | {g:.3f} | {b:.3f} | "
                     f"{s['exposure_stops']:+.2f} st | {cast} | {note} |")
    lines += ["", f"{len(changed)} of {len(shots)} shots would change by more than 1.5%.",
              "Preview: before-after_preview.mp4 (left = yours, right = suggested). Stills: changed-shots_before-after.png."]
    (out / "GRADE-NOTES.md").write_text("\n".join(lines) + "\n")
    (out / "grade-assist.json").write_text(json.dumps({"summary": summary, "shots": shots}, indent=1))
    print(f"{len(changed)} of {len(shots)} shots flagged -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
