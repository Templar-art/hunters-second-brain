"""Resolve bridge: build a graded DaVinci Resolve Studio timeline from a flat (Path A) master
in one command, on the Mac, with Resolve open.

  # 1. on the flat master, measure the shots (works anywhere):
  python3 grade/assist.py "Master_flat.mov" --scenes scene.json [--analysis-lut sony_slog3_to_709.cube]
  # 2. on the Mac, Resolve Studio running, External scripting = Local:
  python3 grade/resolve_bridge.py "Master_flat.mov" --assist "output/Master_flat_grade-assist/grade-assist.json" \
      [--powergrade "10x house.drx"] [--drone-lut "DJI_DLogM_to_Rec709.cube"] [--dry-run]

What it does in Resolve:
  1. creates (or opens) project "10x <master name>" with DaVinci YRGB colour management where the API allows;
  2. imports the master and lays it out as one timeline item per shot (cut points from the grade assistant,
     so Resolve's own scene detector isn't needed);
  3. applies the house PowerGrade (.drx exported from the Gallery) to every shot;
  4. writes each shot's balance fix as a CDL (slope = the assistant's gain, saturation from its notes) on the
     balance node; aerials can get the drone LUT on that node instead;
  5. leaves rendering to you (Deliver page), so nothing is exported without a look.

Status: written 28 Oct 2026 against the Resolve scripting calls used by the open-source
lordhoell/davinci-resolve-mcp (SetCDL, GetNodeGraph().ApplyGradeFromDRX / SetLUT, AppendToTimeline).
NOT run against a real Resolve yet: run with --dry-run first, then on a throwaway project.
"""
import argparse
import importlib.machinery
import importlib.util
import json
import os
import sys
from fractions import Fraction
from pathlib import Path

MAC_LIB = "/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"


def plan(assist, fps, node_index=1, aerial_labels=("aerial",)):
    """Pure: grade-assist JSON -> per-shot timeline + grade plan (frames inclusive, as Resolve expects)."""
    shots = []
    for s in assist["shots"]:
        start = int(round(s["start"] * fps))
        end = int(round(s["end"] * fps)) - 1
        if end < start:
            continue
        gain = s.get("resolve_gain", [1.0, 1.0, 1.0])
        sat = 1.0
        note = s.get("note", "")
        if "Sat 45-48" in note:
            sat = 0.92
        elif "Sat 55-58" in note:
            sat = 1.08
        shots.append({
            "shot": s["shot"], "startFrame": start, "endFrame": end, "label": s.get("scene"),
            "skip_grade": "skip" in s,
            "cdl": {"NodeIndex": str(node_index), "Slope": " ".join(f"{g:.4f}" for g in gain),
                    "Offset": "0 0 0", "Power": "1 1 1", "Saturation": f"{sat:.3f}"},
            "aerial": (s.get("scene") in aerial_labels),
            "note": note,
        })
    return shots


def _load_resolve():
    try:
        import fusionscript  # noqa: F401
        return fusionscript.scriptapp("Resolve")
    except ImportError:
        pass
    path = os.getenv("RESOLVE_SCRIPT_LIB", MAC_LIB)
    loader = importlib.machinery.ExtensionFileLoader("fusionscript", path)
    spec = importlib.util.spec_from_loader("fusionscript", loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module.scriptapp("Resolve")


def run(args):
    assist = json.loads(Path(args.assist).read_text())
    master = Path(args.master).expanduser().resolve()
    fps = float(Fraction(args.fps)) if args.fps else None  # e.g. "24000/1001"
    if fps is None:
        sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
        from asd import media
        fps = float(media.video_info(master)[0].fps)
    shots = plan(assist, fps, args.node)
    report = {"master": str(master), "fps": fps, "shots": len(shots), "steps": []}

    def step(msg, ok=True):
        report["steps"].append({"step": msg, "ok": bool(ok)})
        print(("  ok   " if ok else "  FAIL ") + msg)

    if args.dry_run:
        print(f"DRY RUN: {len(shots)} shots from {master.name} at {fps:.3f} fps")
        for s in shots[:60]:
            what = ("skip (black)" if s["skip_grade"] else
                    f"CDL slope {s['cdl']['Slope']} sat {s['cdl']['Saturation']}" + (" + drone LUT" if s["aerial"] and args.drone_lut else ""))
            print(f"  shot {s['shot']:02d} frames {s['startFrame']}-{s['endFrame']} [{s['label'] or '-'}] {what}")
        return 0

    resolve = _load_resolve()
    if resolve is None:
        print("Could not reach Resolve. Open DaVinci Resolve Studio and set Preferences > System > General > "
              "External scripting using: Local.")
        return 2
    pm = resolve.GetProjectManager()
    name = args.project or f"10x {master.stem}"
    project = pm.LoadProject(name) or pm.CreateProject(name)
    step(f"project '{name}'", project)
    if not project:
        return 2
    for key, value in (("colorScienceMode", "davinciYRGBColorManagedv2"), ("timelineFrameRate", f"{fps:.3f}".rstrip("0").rstrip("."))):
        step(f"setting {key}={value}", project.SetSetting(key, value))
    mp = project.GetMediaPool()
    items = mp.ImportMedia([str(master)])
    step("import master", items)
    if not items:
        return 2
    clip = items[0]
    if args.input_color_space:
        step(f"input colour space {args.input_color_space}", clip.SetClipProperty("Input Color Space", args.input_color_space))
    timeline = mp.CreateEmptyTimeline(f"{master.stem} graded")
    step("create timeline", timeline)
    project.SetCurrentTimeline(timeline)
    infos = [{"mediaPoolItem": clip, "startFrame": s["startFrame"], "endFrame": s["endFrame"]} for s in shots]
    appended = mp.AppendToTimeline(infos) or []
    step(f"lay out {len(appended)} of {len(shots)} shots", len(appended) == len(shots))
    for s, item in zip(shots, appended):
        graph = item.GetNodeGraph() if hasattr(item, "GetNodeGraph") else None
        if args.powergrade and graph:
            step(f"shot {s['shot']:02d} house PowerGrade", graph.ApplyGradeFromDRX(str(Path(args.powergrade).resolve()), 0))
        if s["skip_grade"]:
            continue
        if s["aerial"] and args.drone_lut and graph:
            step(f"shot {s['shot']:02d} drone LUT", graph.SetLUT(args.node, str(Path(args.drone_lut).resolve())))
        step(f"shot {s['shot']:02d} CDL {s['cdl']['Slope']}", item.SetCDL(s["cdl"]))
        if s["note"] and hasattr(item, "AddMarker"):
            item.AddMarker(0, "Blue", f"shot {s['shot']:02d}", s["note"][:250], 1)
    out = Path(args.assist).with_name("resolve-bridge-report.json")
    out.write_text(json.dumps(report, indent=1))
    failed = [x for x in report["steps"] if not x["ok"]]
    print(f"Done: {len(report['steps']) - len(failed)} steps ok, {len(failed)} failed. Report: {out}")
    return 0 if not failed else 1


def main(argv=None):
    p = argparse.ArgumentParser(description="Build a graded Resolve timeline from a flat master + grade-assist JSON.")
    p.add_argument("master")
    p.add_argument("--assist", required=True, help="grade-assist.json from grade/assist.py")
    p.add_argument("--powergrade", help=".drx exported from Resolve's Gallery (your house node tree)")
    p.add_argument("--drone-lut", help="LUT for aerial shots (e.g. DJI D-Log M to Rec.709)")
    p.add_argument("--input-color-space", help='e.g. "S-Gamut3.Cine/S-Log3" (applies to the whole master)')
    p.add_argument("--node", type=int, default=1, help="node index for the balance CDL (default 1)")
    p.add_argument("--project")
    p.add_argument("--fps", help='override, e.g. "24000/1001"')
    p.add_argument("--dry-run", action="store_true")
    return run(p.parse_args(argv))


if __name__ == "__main__":
    sys.exit(main())
