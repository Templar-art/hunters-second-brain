#!/usr/bin/env python3
"""plate-vfx: put CG birds into real footage without touching the plate.

  python3 plate_vfx.py init   <clip> --job <dir> [--aspect 16:9|9:16|4:5|1:1]
  python3 plate_vfx.py track  <dir> [--model auto|line|free]
  python3 plate_vfx.py match  <dir>
  python3 plate_vfx.py layout <dir> [--count 4] [--seed 1] [--direction 1|-1]
  python3 plate_vfx.py pilot  <dir> [--frame N] [--tier draft]
  python3 plate_vfx.py render <dir> [--tier draft|standard|hero]
  python3 plate_vfx.py prep   <clip> --job <dir> ...   # init+track+match+layout+pilot, then stop for approval

Tiers trade poly count / render engine for time: draft (~10 s), standard (~1 min), hero (Cycles, ~15-30 min).
"""
import argparse, glob, json, os, shutil, subprocess, sys, time

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "lib"))
BLENDER = os.environ.get("BLENDER", "/Applications/Blender.app/Contents/MacOS/Blender")


def jload(p):
    return json.load(open(p))


def jsave(p, d):
    json.dump(d, open(p, "w"), indent=1)


def ffprobe_video(clip):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=width,height,r_frame_rate", "-of", "json", clip], capture_output=True, text=True, check=True)
    s = json.loads(out.stdout)["streams"][0]
    num, den = (int(x) for x in s["r_frame_rate"].split("/"))
    return s["width"], s["height"], [num, den]


def plate_paths(job):
    return sorted(glob.glob(os.path.join(job, "frames", "f_*.png")))


def cmd_init(a):
    import plate
    job = os.path.abspath(a.job)
    for d in ("src", "frames", "render", "comp", "out"):
        os.makedirs(os.path.join(job, d), exist_ok=True)
    src = os.path.join(job, "src", "plate" + os.path.splitext(a.clip)[1])
    shutil.copy2(a.clip, src)
    subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-map", "0:v:0", "-start_number", "1",
                    os.path.join(job, "frames", "f_%04d.png"), "-y"], check=True)
    w, h, fps = ffprobe_video(src)
    paths = plate_paths(job)
    cuts, _ = plate.find_cuts(paths)
    rng = plate.usable_range(len(paths), cuts)
    shot = {"clip": os.path.abspath(a.clip), "src": src, "frames": len(paths), "width": w, "height": h, "fps": fps,
            "cuts_at": [c + 1 for c in cuts], "range": list(rng), "aspect": a.aspect, "tier": "standard",
            "shutter": 0.2}
    jsave(os.path.join(job, "shot.json"), shot)
    print(f"init: {len(paths)} frames {w}x{h} @ {fps[0]}/{fps[1]}; cuts at {shot['cuts_at'] or 'none'}; "
          f"CG range {rng[0]}-{rng[1]}; aspect {a.aspect}")


def cmd_track(a):
    import cv2, track_fit
    job = os.path.abspath(a.job)
    shot = jload(os.path.join(job, "shot.json"))
    r0, r1 = shot["range"]
    frames = [cv2.imread(p, 0) for p in plate_paths(job)[r0 - 1:r1]]
    cam = track_fit.fit(frames, shot["width"], shot["height"], shot["fps"], model=a.model)
    jsave(os.path.join(job, "camera.json"), cam)
    ok = cam["mean_err_px"] < 0.5
    print(f"track: {'PASS' if ok else 'FAIL'} mean {cam['mean_err_px']:.3f}px (gate 0.5px)")
    sys.exit(0 if ok else 2)


def cmd_match(a):
    import plate
    job = os.path.abspath(a.job)
    shot = jload(os.path.join(job, "shot.json"))
    r0, r1 = shot["range"]
    m = plate.analyse(plate_paths(job)[r0 - 1:r1])
    jsave(os.path.join(job, "plate.json"), m)
    print(f"match: sky {[round(x, 3) for x in m['sky_linear_rgb']]} warmth {m['warmth_rb']:.3f} grain {[round(x, 2) for x in m['grain_bgr']]}")


def cmd_layout(a):
    import layout
    job = os.path.abspath(a.job)
    shot = jload(os.path.join(job, "shot.json"))
    cam = jload(os.path.join(job, "camera.json"))
    lay = layout.auto(cam, count=a.count, aspect=shot["aspect"], seed=a.seed, direction=a.direction)
    jsave(os.path.join(job, "layout.json"), lay)
    layout.preview(lay, cam, plate_paths(job)[shot["range"][0] - 1], os.path.join(job, "layout_preview.jpg"))
    print(f"layout: {len(lay['birds'])} birds -> layout.json, layout_preview.jpg")


def blender_build(job, tier, render=False, frame=None):
    args = [BLENDER, "-b", "--factory-startup", "--python", os.path.join(ROOT, "blender", "build_birds.py"), "--",
            os.path.join(job, "shot.json"), "--tier", tier]
    if render:
        args.append("--render")
    if frame:
        args += ["--frame", str(frame)]
    t = time.time()
    res = subprocess.run(args, capture_output=True, text=True)
    if "BUILD_OK" not in res.stdout:
        print(res.stdout[-3000:], res.stderr[-3000:])
        raise SystemExit("blender build failed")
    return time.time() - t


def comp_all(job, tier, out_dir, frames=None):
    import plate
    shot = jload(os.path.join(job, "shot.json"))
    pm = jload(os.path.join(job, "plate.json"))
    r0, r1 = shot["range"]
    plates = plate_paths(job)
    idx = frames or range(1, len(plates) + 1)
    cgs, outs, used = [], [], []
    for i in idx:
        cg = os.path.join(job, "render", tier, f"b_{i - r0 + 1:04d}.png") if r0 <= i <= r1 else None
        if cg and not os.path.exists(cg):
            cg = None
        o = os.path.join(out_dir, f"c_{i:04d}.png")
        plate.composite(plates[i - 1], cg, o, grain_bgr=pm["grain_bgr"] if tier != "draft" else None, seed=i)
        cgs.append(cg); outs.append(o); used.append(plates[i - 1])
    return plate.verify(used, cgs, outs)


def cmd_pilot(a):
    job = os.path.abspath(a.job)
    shot = jload(os.path.join(job, "shot.json"))
    r0, r1 = shot["range"]
    f = a.frame or (r1 - r0) // 2 + 1
    dt = blender_build(job, a.tier, frame=f)
    import plate
    pm = jload(os.path.join(job, "plate.json"))
    out = os.path.join(job, f"pilot_{a.tier}.png")
    plate.composite(plate_paths(job)[r0 + f - 2], os.path.join(job, "render", a.tier, f"pilot_{f:04d}.png"), out,
                    grain_bgr=pm["grain_bgr"] if a.tier != "draft" else None)
    print(f"pilot: {a.tier} frame {f} in {dt:.1f}s -> {out}")


def cmd_render(a):
    job = os.path.abspath(a.job)
    shot = jload(os.path.join(job, "shot.json"))
    tier = a.tier or shot.get("tier", "standard")
    for p in glob.glob(os.path.join(job, "render", tier, "b_*.png")):
        os.remove(p)
    dt = blender_build(job, tier, render=True)
    comp_dir = os.path.join(job, "comp", tier)
    os.makedirs(comp_dir, exist_ok=True)
    worst = comp_all(job, tier, comp_dir)
    fps = f"{shot['fps'][0]}/{shot['fps'][1]}"
    name = os.path.splitext(os.path.basename(shot["clip"]))[0].replace(" ", "-").replace("?", "")
    out = os.path.join(job, "out")
    rate = ["-framerate", fps]
    audio = ["-i", shot["src"], "-map", "0:v", "-map", "1:a?", "-shortest"]
    col = ["-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709"]
    run = lambda args: subprocess.run(["ffmpeg", "-v", "error", "-y"] + args, check=True)
    run(rate + ["-i", os.path.join(comp_dir, "c_%04d.png")] + audio +
        ["-c:v", "libx264", "-preset", "slow", "-crf", "12", "-pix_fmt", "yuv420p"] + col + ["-c:a", "copy",
         os.path.join(out, f"{name}_birds_{tier}.mp4")])
    if tier != "draft":
        run(rate + ["-i", os.path.join(comp_dir, "c_%04d.png")] + audio +
            ["-c:v", "prores_ks", "-profile:v", "3", "-pix_fmt", "yuv422p10le"] + col + ["-c:a", "pcm_s16le",
             os.path.join(out, f"{name}_birds_{tier}_prores.mov")])
        run(rate + ["-i", os.path.join(job, "render", tier, "b_%04d.png"), "-vf", "gblur=sigma=0.5:planes=0xF",
                    "-c:v", "prores_ks", "-profile:v", "4", "-pix_fmt", "yuva444p10le", "-alpha_bits", "16",
                    os.path.join(out, f"{name}_birds-only_alpha_{tier}.mov")])
    status = "PASS" if worst == 0 else "FAIL"
    print(f"render: {tier} in {dt:.0f}s; plate-untouched check {status} (max diff outside CG {worst}); outputs in {out}")
    jsave(os.path.join(job, f"render_{tier}.json"), {"tier": tier, "seconds": round(dt, 1), "untouched_max_diff": worst})


def cmd_prep(a):
    cmd_init(a)
    a.job = os.path.abspath(a.job)
    try:
        cmd_track(a)
    except SystemExit as e:
        if e.code not in (0, None):
            raise
    cmd_match(a)
    cmd_layout(a)
    a.frame, a.tier = None, "draft"
    cmd_pilot(a)
    print("prep done: review layout_preview.jpg + pilot_draft.png, then `render`")


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    for name in ("init", "prep"):
        p = sp.add_parser(name); p.add_argument("clip"); p.add_argument("--job", required=True)
        p.add_argument("--aspect", default="16:9")
        p.add_argument("--model", default="auto"); p.add_argument("--count", type=int, default=4)
        p.add_argument("--seed", type=int, default=1); p.add_argument("--direction", type=int, default=1)
    p = sp.add_parser("track"); p.add_argument("job"); p.add_argument("--model", default="auto")
    p = sp.add_parser("match"); p.add_argument("job")
    p = sp.add_parser("layout"); p.add_argument("job"); p.add_argument("--count", type=int, default=4)
    p.add_argument("--seed", type=int, default=1); p.add_argument("--direction", type=int, default=1)
    p = sp.add_parser("pilot"); p.add_argument("job"); p.add_argument("--frame", type=int); p.add_argument("--tier", default="draft")
    p = sp.add_parser("render"); p.add_argument("job"); p.add_argument("--tier")
    a = ap.parse_args()
    {"init": cmd_init, "track": cmd_track, "match": cmd_match, "layout": cmd_layout,
     "pilot": cmd_pilot, "render": cmd_render, "prep": cmd_prep}[a.cmd](a)


if __name__ == "__main__":
    main()
