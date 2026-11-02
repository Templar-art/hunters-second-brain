#!/usr/bin/env python3
"""plate-vfx: put CG birds into real footage without touching the plate.

  python3 plate_vfx.py init   <clip> --job <dir> [--aspect 16:9|9:16|4:5|1:1]
  python3 plate_vfx.py track  <dir> [--model auto|line|free]
  python3 plate_vfx.py match  <dir>
  python3 plate_vfx.py layout <dir> [--count 4] [--flock 24] [--seed 1] [--direction 1|-1]
  python3 plate_vfx.py pilot  <dir> [--frame N] [--tier draft]
  python3 plate_vfx.py render <dir> [--tier draft|standard|hero]
  python3 plate_vfx.py prep   <clip> --job <dir> ...   # init+track+match+layout+pilot, then stop for approval
  python3 plate_vfx.py lines  <dir> [--marks marks.json]   # tracked lot outlines + pins (template written on first run)
  python3 plate_vfx.py dusk   <dir> [--sky <id>] [--sun -45] [--ev -2.5]   # day-to-dusk: grade + sky + water + lights
  python3 plate_vfx.py sky    <dir> [--sky <polyhaven puresky id>] [--sun 180] [--brightness 0.8] [--ev 0]

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
    gate = 0.5 * max(shot["width"], shot["height"]) / 1920  # 0.5 px at 1080p on the long side (4K = 1.0 px; 9:16 same as 16:9)
    ok = cam["mean_err_px"] < gate
    print(f"track: {'PASS' if ok else 'FAIL'} mean {cam['mean_err_px']:.3f}px (gate {gate:.2f}px)")
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
    lay = layout.auto(cam, count=a.count, aspect=shot["aspect"], seed=a.seed, direction=a.direction, sky_y=getattr(a, "sky_y", None)) if a.count else \
        {"aspect": shot["aspect"], "seed": a.seed, "safe_rect": layout.safe_rect(cam["width"], cam["height"], shot["aspect"]), "birds": []}
    lay["flocks"] = [layout.auto_flock(cam, count=a.flock, aspect=shot["aspect"], seed=a.seed, direction=a.direction)] if a.flock else []
    jsave(os.path.join(job, "layout.json"), lay)
    layout.preview(lay, cam, plate_paths(job)[shot["range"][0] - 1], os.path.join(job, "layout_preview.jpg"))
    print(f"layout: {len(lay['birds'])} birds + {sum(f['count'] for f in lay['flocks'])} in flocks -> layout.json, layout_preview.jpg")


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


def comp_all(job, tier, out_dir, frames=None, grain=None, soften=0.5):
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
        g = (tier != "draft") if grain is None else grain
        plate.composite(plates[i - 1], cg, o, grain_bgr=pm["grain_bgr"] if g else None, soften=soften, seed=i)
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


def encode(job, shot, comp_dir, label, prores=True, alpha_dir=None):
    """comp_dir/c_####.png -> out/<clip>_<label>.mp4 (+ ProRes 422 HQ, + ProRes 4444 of alpha_dir's RGBA layer)."""
    fps = f"{shot['fps'][0]}/{shot['fps'][1]}"
    name = os.path.splitext(os.path.basename(shot["clip"]))[0].replace(" ", "-").replace("?", "")
    out = os.path.join(job, "out")
    os.makedirs(out, exist_ok=True)
    rate = ["-framerate", fps]
    audio = ["-i", shot["src"], "-map", "0:v", "-map", "1:a?", "-shortest"]
    col = ["-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709"]
    run = lambda args: subprocess.run(["ffmpeg", "-v", "error", "-y"] + args, check=True)
    run(rate + ["-i", os.path.join(comp_dir, "c_%04d.png")] + audio +
        ["-c:v", "libx264", "-preset", "slow", "-crf", "12", "-pix_fmt", "yuv420p"] + col + ["-c:a", "copy",
         os.path.join(out, f"{name}_{label}.mp4")])
    if prores:
        run(rate + ["-i", os.path.join(comp_dir, "c_%04d.png")] + audio +
            ["-c:v", "prores_ks", "-profile:v", "3", "-pix_fmt", "yuv422p10le"] + col + ["-c:a", "pcm_s16le",
             os.path.join(out, f"{name}_{label}_prores.mov")])
    if alpha_dir:
        run(rate + ["-i", os.path.join(alpha_dir, "b_%04d.png"), "-vf", "gblur=sigma=0.5:planes=0xF",
                    "-c:v", "prores_ks", "-profile:v", "4", "-pix_fmt", "yuva444p10le", "-alpha_bits", "16",
                    os.path.join(out, f"{name}_{label}_layer-alpha.mov")])
    return out


ML_PY = os.path.expanduser(os.environ.get("PLATE_VFX_ML_PY", "~/.venvs/demucs/bin/python"))
SKIES = os.path.join(ROOT, "assets", "skies")


def sky_probs(job, shot, cam, log=print):
    """Sky probability per CG-range frame: frame 1 carried by the camera rotation, or per-frame inference
    when the carried matte disagrees with a fresh one on the last frame (parallax from near objects)."""
    import cv2, numpy as np, sky
    r0, r1 = shot["range"]
    w, h = cam["width"], cam["height"]
    f_px = cam["lens_mm"] / 36 * w
    run_ml = lambda fr: subprocess.run([ML_PY, os.path.join(ROOT, "lib", "sky_matte.py"), job] + [str(f) for f in fr],
                                       check=True, capture_output=True, text=True)
    rd = lambda f: cv2.imread(os.path.join(job, "sky", f"prob_{f:04d}.png"), 0).astype(np.float32) / 255
    if not all(os.path.exists(os.path.join(job, "sky", f"prob_{f:04d}.png")) for f in (r0, r1)):
        run_ml([r0, (r0 + r1) // 2, r1])
    p1 = rd(r0)
    carry = lambda k: cv2.warpPerspective(p1, sky.rot_homography(cam["frames"][0], cam["frames"][k - r0], f_px, w, h), (w, h),
                                          flags=cv2.INTER_LINEAR | cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_REPLICATE)
    agree = sky.iou(carry(r1), rd(r1))
    if agree >= 0.97:
        log(f"sky: matte carried by camera rotation (last-frame IoU {agree:.3f})")
        return {k: carry(k) for k in range(r0, r1 + 1)}
    log(f"sky: carried matte IoU {agree:.3f} < 0.97, inferring every frame")
    run_ml(list(range(r0, r1 + 1)))
    probs = {k: rd(k) for k in range(r0, r1 + 1)}
    ks = sorted(probs)  # light temporal smoothing against flicker
    return {k: np.mean([probs[j] for j in ks[max(0, i - 1): i + 2]], 0) for i, k in enumerate(ks)}


def cmd_sky(a):
    import cv2, math, numpy as np, sky
    job = os.path.abspath(a.job)
    shot = jload(os.path.join(job, "shot.json"))
    cam = jload(os.path.join(job, "camera.json"))
    pm = jload(os.path.join(job, "plate.json"))
    r0, r1 = shot["range"]
    w, h = cam["width"], cam["height"]
    f_px = cam["lens_mm"] / 36 * w
    probs = sky_probs(job, shot, cam)
    hdr = sky.load_hdri(os.path.join(SKIES, a.sky + ".hdr"))
    fwd = np.asarray(cam["frames"][0])[:3, :3] @ np.array([0, 0, -1.0])
    sun_az, _ = sky.sun_azimuth(hdr)
    yaw = math.atan2(fwd[1], fwd[0]) + math.radians(a.sun) - sun_az
    tag = a.tag or a.sky.replace("_puresky", "")
    lay_dir = os.path.join(job, "render", f"sky_{tag}")
    os.makedirs(lay_dir, exist_ok=True)
    plates = plate_paths(job)
    expo = None
    for k in range(r0, r1 + 1):
        pl = cv2.imread(plates[k - 1])
        alpha = sky.refine(probs[k], pl)
        lin = sky.render_sky(hdr, cam["frames"][k - r0], f_px, w, h, yaw, lift=a.lift)
        if expo is None:  # one exposure for the whole shot: sky median lands at a set fraction of the old sky
            lum = lin[alpha > 0.5] @ np.array([0.0722, 0.7152, 0.2126], np.float32)
            old = float(np.dot(pm["sky_linear_rgb"], [0.2126, 0.7152, 0.0722]))
            expo = a.brightness * old / max(1e-6, float(np.median(lum)))
        sk = sky.tone(lin, expo * 2 ** a.ev, warmth=pm["warmth_rb"])
        cv2.imwrite(os.path.join(lay_dir, f"b_{k - r0 + 1:04d}.png"), sky.layer(pl, sk, alpha, haze=a.haze))
    comp_dir = os.path.join(job, "comp", f"sky_{tag}")
    os.makedirs(comp_dir, exist_ok=True)
    worst = comp_all(job, f"sky_{tag}", comp_dir)
    mid = (r0 + r1) // 2
    shutil.copy2(os.path.join(comp_dir, f"c_{mid:04d}.png"), os.path.join(job, f"pilot_sky_{tag}.png"))
    out = encode(job, shot, comp_dir, f"sky-{tag}", alpha_dir=lay_dir)
    print(f"sky: {a.sky} sun at {a.sun:.0f} deg from camera heading, exposure {expo:.3f}; "
          f"plate-untouched outside sky matte {'PASS' if worst == 0 else 'FAIL'} ({worst}); outputs in {out}")


def cmd_lines(a):
    import overlay
    job = os.path.abspath(a.job)
    shot = jload(os.path.join(job, "shot.json"))
    cam = jload(os.path.join(job, "camera.json"))
    marks_p = os.path.join(job, a.marks)
    if not os.path.exists(marks_p):
        jsave(marks_p, {"lots": [{"poly": [[800, 930], [1100, 930], [1090, 745], [810, 745]], "label": "Lot name", "sub": "detail line"}],
                        "pins": [{"at": [960, 600], "label": "Landmark", "sub": "detail"}]})
        raise SystemExit(f"wrote a template {marks_p}: set frame-1 pixel corners + copy, then rerun")
    lay_dir = os.path.join(job, "render", "lines")
    overlay.render(jload(marks_p), cam, shot["fps"][0] / shot["fps"][1], lay_dir)
    comp_dir = os.path.join(job, "comp", "lines")
    os.makedirs(comp_dir, exist_ok=True)
    worst = comp_all(job, "lines", comp_dir, grain=False, soften=0)
    r0, r1 = shot["range"]
    shutil.copy2(os.path.join(comp_dir, f"c_{min(r1, r0 + 40):04d}.png"), os.path.join(job, "pilot_lines.png"))
    out = encode(job, shot, comp_dir, "lines", alpha_dir=lay_dir)
    print(f"lines: plate-untouched outside graphics {'PASS' if worst == 0 else 'FAIL'} ({worst}); outputs in {out}")


def cmd_dusk(a):
    import cv2, math, numpy as np, dusk, ground, sky
    job = os.path.abspath(a.job)
    shot = jload(os.path.join(job, "shot.json"))
    cam = jload(os.path.join(job, "camera.json"))
    pm = jload(os.path.join(job, "plate.json"))
    r0, r1 = shot["range"]
    w, h = cam["width"], cam["height"]
    f_px = cam["lens_mm"] / 36 * w
    L = dict(dusk.LOOK, ev=a.ev)
    probs = sky_probs(job, shot, cam)
    wat1 = cv2.imread(os.path.join(job, "sky", f"water_{r0:04d}.png"), 0)
    wat1 = None if wat1 is None else wat1.astype(np.float32) / 255
    hdr = sky.load_hdri(os.path.join(SKIES, a.sky + ".hdr"))
    M1 = np.asarray(cam["frames"][0])
    fwd = M1[:3, :3] @ np.array([0, 0, -1.0])
    cam_az = math.atan2(fwd[1], fwd[0])
    sun_az, _ = sky.sun_azimuth(hdr)
    yaw = cam_az + math.radians(a.sun) - sun_az
    sd = np.array([math.cos(cam_az + math.radians(a.sun)), math.sin(cam_az + math.radians(a.sun)), 0.05])
    c = np.linalg.inv(M1[:3, :3]) @ sd
    sun_x = float(np.clip(f_px * c[0] / max(-c[2], 1e-3) + w / 2, -0.5 * w, 1.5 * w)) if c[2] < 0 else (w * 1.5 if c[0] > 0 else -w * 0.5)
    marks = jload(os.path.join(job, a.marks)).get("dusk", {}) if os.path.exists(os.path.join(job, a.marks)) else {}
    mt = dusk.track_marks(marks, cam)
    tag = a.tag or a.sky.replace("_puresky", "")
    comp_dir = os.path.join(job, "comp", f"dusk_{tag}")
    os.makedirs(comp_dir, exist_ok=True)
    plates = plate_paths(job)
    expo = horizon = None
    rng = np.random.default_rng(0)
    for k in range(r0, r1 + 1):
        pl = cv2.imread(plates[k - 1])
        M = cam["frames"][k - r0]
        sky_a = sky.refine(probs[k], pl)
        wat = None
        if wat1 is not None:
            H = ground.ground_H(cam["frames"][0], M, f_px, w, h)
            wat = cv2.warpPerspective(wat1, H, (w, h), flags=cv2.INTER_LINEAR | cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_REPLICATE)
            wat = sky.refine(wat, pl) * (1 - sky_a)
        if expo is None:
            lin = sky.render_sky(hdr, M, f_px, w, h, yaw, lift=a.lift)
            lum = lin[sky_a > 0.5] @ np.array([0.0722, 0.7152, 0.2126], np.float32)
            old = float(np.dot(pm["sky_linear_rgb"], [0.2126, 0.7152, 0.0722]))
            expo = L["sky_brightness"] * old / max(1e-6, float(np.median(lum))) * 2 ** a.sky_ev
            rows = dusk.skyline_rows(sky_a).astype(int)
            band = np.zeros((h, w), bool)
            for x in range(w):
                band[max(0, rows[x] - 40):rows[x] + 1, x] = True
            d1 = sky.pixel_dirs(M, f_px, w, h)
            horizon = dusk.twilight(sky.tone_lin(lin, expo, pm["warmth_rb"]), d1, cam_az + math.radians(a.sun), L["sky_gain"])[band & (sky_a > 0.5)].mean(0)
        E = dusk.emission(mt, k - r0, w, h, L)
        out = dusk.frame(pl, sky_a, wat, hdr, M, f_px, yaw, a.lift, expo, pm["warmth_rb"], sun_x, horizon, E, L, cam_az + math.radians(a.sun))
        n = rng.standard_normal((h, w, 1)).astype(np.float32) * np.array(pm["grain_bgr"], np.float32) * 0.9
        out = np.clip(out + n * sky_a[..., None] + 0.5, 0, 255).astype(np.uint8)  # the new sky gets the plate's grain
        cv2.imwrite(os.path.join(comp_dir, f"c_{k - r0 + 1:04d}.png"), out)
    mid = (r1 - r0) // 2 + 1
    before = cv2.imread(plates[r0 + mid - 2]); after = cv2.imread(os.path.join(comp_dir, f"c_{mid:04d}.png"))
    cv2.imwrite(os.path.join(job, f"pilot_dusk_{tag}.png"), after)
    cv2.imwrite(os.path.join(job, f"pilot_dusk_{tag}_before-after.jpg"), np.hstack([before, after]))
    out = encode(job, shot, comp_dir, f"dusk-{tag}")
    print(f"dusk: {a.sky}, sun {a.sun:.0f} deg, ground {a.ev:+.1f} EV, {len(marks.get('windows', []))} windows, "
          f"{len(marks.get('pools', []))} pools, {len(marks.get('lamps', []))} lamps; frames {r0}-{r1}; outputs in {out}")


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
    out = encode(job, shot, comp_dir, f"birds_{tier}", alpha_dir=None if tier == "draft" else os.path.join(job, "render", tier),
                 prores=tier != "draft")
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
        p.add_argument("--flock", type=int, default=0)
    p = sp.add_parser("track"); p.add_argument("job"); p.add_argument("--model", default="auto")
    p = sp.add_parser("match"); p.add_argument("job")
    p = sp.add_parser("layout"); p.add_argument("job"); p.add_argument("--count", type=int, default=4)
    p.add_argument("--seed", type=int, default=1); p.add_argument("--direction", type=int, default=1)
    p.add_argument("--flock", type=int, default=0, help="add a flock of N birds")
    p.add_argument("--sky-y", type=int, help="keep birds above this pixel row (horizon): gulls against sky, not canopy")
    p = sp.add_parser("pilot"); p.add_argument("job"); p.add_argument("--frame", type=int); p.add_argument("--tier", default="draft")
    p = sp.add_parser("render"); p.add_argument("job"); p.add_argument("--tier")
    p = sp.add_parser("dusk"); p.add_argument("job"); p.add_argument("--sky", default="industrial_sunset_02_puresky")
    p.add_argument("--sun", type=float, default=-45, help="sun azimuth vs camera heading, + = left; at dusk it sits on the horizon")
    p.add_argument("--ev", type=float, default=-2.5, help="ground exposure change"); p.add_argument("--sky-ev", type=float, default=0.0)
    p.add_argument("--lift", type=float, default=8); p.add_argument("--marks", default="marks.json"); p.add_argument("--tag")
    p = sp.add_parser("lines"); p.add_argument("job"); p.add_argument("--marks", default="marks.json")
    p = sp.add_parser("sky"); p.add_argument("job"); p.add_argument("--sky", default="kloofendal_48d_partly_cloudy_puresky")
    p.add_argument("--sun", type=float, default=180, help="sun azimuth relative to camera heading (180 = behind camera)")
    p.add_argument("--brightness", type=float, default=0.7, help="new sky median vs the old sky's luminance")
    p.add_argument("--ev", type=float, default=0.0); p.add_argument("--haze", type=float, default=0.35)
    p.add_argument("--lift", type=float, default=14, help="degrees: sample the HDRI higher up (bluer, more cloud)")
    p.add_argument("--tag")
    a = ap.parse_args()
    {"init": cmd_init, "track": cmd_track, "match": cmd_match, "layout": cmd_layout,
     "pilot": cmd_pilot, "render": cmd_render, "prep": cmd_prep, "sky": cmd_sky, "lines": cmd_lines, "dusk": cmd_dusk}[a.cmd](a)


if __name__ == "__main__":
    main()
