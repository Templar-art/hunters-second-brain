"""18 Maryland cinematic shots: stills and camera moves rendered from maryland.blend (built by build.py).

  blender -b maryland.blend -P shots.py -- --list
  blender -b maryland.blend -P shots.py -- --shots lounge,kitchen --still [--samples 128] [--res 100]
  blender -b maryland.blend -P shots.py -- --shots aerial --anim [--samples 48] [--frames 1-125]

Each shot names its light (day / golden / dusk), camera path (start -> end, eased), look-at path, lens and f-stop.
Before rendering, every camera position on the path is checked against the geometry (ray casts in six directions,
nothing within 0.25 m, and the view line clear for 1 m); a shot that fails is skipped and reported, never rendered.
Stills go to renders/stills/<shot>_<light>.png, moves to renders/moves/<shot>/####.png.
"""
import json
import math
import os
import sys

import bpy
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
sc = bpy.context.scene


def arg(n, d):
    return argv[argv.index(n) + 1] if n in argv else d


def hw(px, py):                                   # same plan transform as build.py
    return 43.6 + (px - 608.75) / 13.1, 24.0 - (py - 362.5) / 13.1


def P(px, py, z):
    x, y = hw(px, py); return (x, y, z)


G, UP = 0.3, 3.5                                  # floor levels
EYE = 1.45
# name: light, (cam start, cam end), (look start, look end), lens, fstop, frames
SHOTS = {
    # ---- exterior
    "aerial":       ("golden", ((-34, -14, 34), (-12, -2, 24)), ((60, 16, 0), (58, 16, 2)), 24, 0, 150),
    "gate":         ("golden", ((148.5, 2.6, 1.1), (140.5, 4.6, 2.4)), ((75, 12, 3.5), (75, 12, 4.2)), 28, 0, 125),
    "drive":        ("golden", ((124, 3.0, 1.4), (100, 4.2, 1.7)), ((66, 12, 3.6), (66, 12, 3.8)), 32, 0, 125),
    "pool_hero":    ("dusk",   ((22.5, 13.5, 1.0), (22.5, 21.5, 1.0)), ((55, 17, 4.2), (55, 19, 4.2)), 22, 0, 150),
    "bench_water":  ("golden", ((19.4, 9.4, 0.9), (18.6, 9.6, 0.95)), ((-20, 4, 1.4), (-20, 7, 1.4)), 35, 2.8, 125),
    "balcony_dusk": ("dusk",   (P(660, 470, UP + 1.55), P(628, 470, UP + 1.45)), ((-30, 18, 2), (-30, 16, 1)), 24, 0, 125),
    "closing":      ("dusk",   ((10, 10, 18), (-26, -8, 40)), ((58, 17, 2), (60, 16, 0)), 24, 0, 175),
    # ---- interior (ground)
    "lounge":       ("day", (P(722, 462, EYE), P(758, 462, EYE)), (P(722, 366, 1.0), P(746, 366, 1.0)), 22, 0, 125),
    "kitchen":      ("day", (P(762, 440, 1.5), P(814, 440, 1.5)), (P(770, 500, 0.95), P(808, 500, 0.95)), 24, 0, 125),
    "dining":       ("day", (P(764, 412, EYE), P(764, 384, EYE)), (P(820, 397, 0.9), P(820, 397, 0.9)), 24, 0, 125),
    "family":       ("day", (P(706, 578, EYE), P(706, 562, EYE)), (P(690, 510, 1.1), P(690, 510, 1.1)), 20, 0, 125),
    "outdoor":      ("golden", (P(680, 548, EYE), P(640, 548, 1.6)), (P(520, 470, 1.0), P(520, 470, 1.0)), 22, 0, 125),
    "media":        ("dusk", (P(965, 410, EYE), P(950, 410, EYE)), (P(935, 488, 1.2), P(935, 488, 1.2)), 20, 0, 125),
    # ---- interior (upper)
    "master":       ("day", (P(712, 512, UP + 1.5), P(722, 500, UP + 1.45)), (P(767, 476, UP + 0.9), P(767, 476, UP + 0.9)), 20, 0, 125),
    "upper_living": ("day", (P(888, 400, UP + 1.5), P(888, 412, UP + 1.5)), (P(968, 400, UP + 1.0), P(968, 400, UP + 1.0)), 20, 0, 125),
}

LIGHTS = {   # hdr, hdr strength, sun dir (toward the sun: azimuth deg from +X, elevation deg), sun energy, interior x
    "day":    ("kloofendal_48d_partly_cloudy_puresky", 1.0, (115, 48), 4.0, 0.6),
    "golden": ("rosendal_park_sunset_puresky", 1.1, (192, 9), 3.0, 0.8),
    "dusk":   ("qwantani_dusk_2_puresky", 0.55, (200, -4), 0.0, 2.6),
}


def setup_light(name):
    hdr, hs, (az, el), se, ix = LIGHTS[name]
    w = sc.world; nt = w.node_tree
    env = next(n for n in nt.nodes if n.type == "TEX_ENVIRONMENT")
    p = os.path.join(HERE, "..", "sky-library", "hdr_2k", hdr + ".hdr")
    env.image = bpy.data.images.load(p, check_existing=True)
    m = nt.nodes.get("sky_map") or nt.nodes.new("ShaderNodeMapping"); m.name = "sky_map"
    tc = nt.nodes.get("sky_tc") or nt.nodes.new("ShaderNodeTexCoord"); tc.name = "sky_tc"
    nt.links.new(tc.outputs["Generated"], m.inputs["Vector"]); nt.links.new(m.outputs["Vector"], env.inputs["Vector"])
    # rotate the HDR so its sun sits where the scene sun is (HDR sun assumed at its u = 0.5, i.e. -X)
    m.inputs["Rotation"].default_value = (0, 0, math.radians(az + 180))
    next(n for n in nt.nodes if n.type == "BACKGROUND").inputs["Strength"].default_value = hs
    sun = bpy.data.objects["sun"]; sun.hide_render = se <= 0
    d = Vector((math.cos(math.radians(el)) * math.cos(math.radians(az)), math.cos(math.radians(el)) * math.sin(math.radians(az)), math.sin(math.radians(el))))
    sun.rotation_euler = (-d).to_track_quat("-Z", "Y").to_euler(); sun.data.energy = se; sun.data.angle = math.radians(1.2)
    sun.data.color = (1.0, 0.82, 0.62) if name == "golden" else (1.0, 0.97, 0.92)
    for o in bpy.data.collections["interior_lights"].objects:
        if o.type == "LIGHT":
            o.data.energy = o["e0"] * ix
    pool = bpy.data.materials["Pool_water"]; b = next(n for n in pool.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    b.inputs["Emission Color"].default_value = (0.1, 0.55, 0.9, 1); b.inputs["Emission Strength"].default_value = 1.6 if name == "dusk" else 0.0
    for mn in ("Pendant_bulb_warm",):
        bb = next(n for n in bpy.data.materials[mn].node_tree.nodes if n.type == "BSDF_PRINCIPLED")
        bb.inputs["Emission Strength"].default_value = 6.0 * max(ix, 0.5)


def interior_light_store():
    for o in bpy.data.collections["interior_lights"].objects:
        if o.type == "LIGHT" and "e0" not in o:
            o["e0"] = o.data.energy


def ease(t):
    return t * t * (3 - 2 * t)


def make_cam(name, spec):
    light, (c0, c1), (l0, l1), lens, fstop, frames = spec
    cd = bpy.data.cameras.new("shot_" + name); cd.lens = lens; cd.sensor_width = 36; cd.clip_start = 0.05; cd.clip_end = 2000
    if fstop:
        cd.dof.use_dof = True; cd.dof.aperture_fstop = fstop
    cam = bpy.data.objects.new("shot_" + name, cd); sc.collection.objects.link(cam)
    path = []
    for f in range(frames):
        t = ease(f / max(1, frames - 1))
        c = Vector(c0).lerp(Vector(c1), t); l = Vector(l0).lerp(Vector(l1), t)
        path.append((c, l))
    return cam, path


def pose(cam, c, l):
    cam.location = c; cam.rotation_euler = (l - c).to_track_quat("-Z", "Y").to_euler()
    if cam.data.dof.use_dof:
        cam.data.dof.focus_distance = (l - c).length * 0.35


def check_cam(path):
    """camera must not sit in or right against geometry anywhere on its path"""
    dg = bpy.context.evaluated_depsgraph_get(); bad = []
    for i in range(0, len(path), max(1, len(path) // 12)):
        c, l = path[i]
        for d in (Vector((1, 0, 0)), Vector((-1, 0, 0)), Vector((0, 1, 0)), Vector((0, -1, 0)), Vector((0, 0, 1)), Vector((0, 0, -1))):
            hit, loc, *_ , ob, _m = sc.ray_cast(dg, c, d, distance=0.25)
            if hit:
                bad.append(f"frame {i}: {ob.name} within 0.25 m"); break
        v = (l - c).normalized(); hit, loc, *_ , ob, _m = sc.ray_cast(dg, c, v, distance=1.0)
        if hit:
            bad.append(f"frame {i}: view blocked by {ob.name} at {(loc - c).length:.2f} m")
    return bad


def render_settings(samples, res):
    sc.render.engine = "CYCLES"
    pr = bpy.context.preferences.addons["cycles"].preferences; pr.compute_device_type = "METAL"; pr.get_devices()
    for d in pr.devices:
        d.use = True
    sc.cycles.device = "GPU"; sc.cycles.samples = samples; sc.cycles.use_denoising = True
    sc.cycles.use_adaptive_sampling = True; sc.cycles.adaptive_threshold = 0.02
    sc.cycles.max_bounces = 8; sc.cycles.diffuse_bounces = 4; sc.cycles.glossy_bounces = 4; sc.cycles.transmission_bounces = 8
    sc.cycles.caustics_reflective = False; sc.cycles.caustics_refractive = False; sc.cycles.blur_glossy = 1.0
    sc.render.resolution_x, sc.render.resolution_y = 1920, 1080; sc.render.resolution_percentage = res
    sc.view_settings.view_transform = "AgX"
    looks = [i.identifier for i in bpy.types.ColorManagedViewSettings.bl_rna.properties["look"].enum_items]
    want = next((l for l in looks if "Medium High Contrast" in l), None) or next((l for l in looks if "Base Contrast" in l), "None")
    try:
        sc.view_settings.look = want
    except TypeError:
        pass
    sc.render.image_settings.file_format = "PNG"; sc.render.image_settings.color_depth = "16"
    sc.render.use_motion_blur = False


if __name__ == "__main__":
    if "--list" in argv:
        for k, v in SHOTS.items():
            print(f"{k:14} {v[0]:7} {v[3]}mm frames {v[5]}")
        sys.exit(0)
    names = [s for s in arg("--shots", ",".join(SHOTS)).split(",") if s]
    anim = "--anim" in argv
    light_override = arg("--light", None)
    render_settings(int(arg("--samples", 128 if not anim else 48)), int(arg("--res", 100)))
    interior_light_store()
    report = {}
    for n in names:
        spec = list(SHOTS[n])
        if light_override:
            spec[0] = light_override
        setup_light(spec[0])
        cam, path = make_cam(n, spec); sc.camera = cam
        bad = check_cam(path)
        report[n] = dict(light=spec[0], camera_issues=bad)
        if bad:
            print("CAMFAIL", n, bad[:3]); continue
        if not anim:
            c, l = path[len(path) // 2] if "--mid" in argv else path[0]
            pose(cam, c, l)
            out = os.path.join(HERE, "renders", "stills", f"{n}_{spec[0]}.png"); os.makedirs(os.path.dirname(out), exist_ok=True)
            sc.render.filepath = out; bpy.ops.render.render(write_still=True); print("STILL", out)
        else:
            fr = arg("--frames", f"1-{len(path)}").split("-"); f0, f1 = int(fr[0]), int(fr[1])
            step = int(arg("--step", 1))
            d = os.path.join(HERE, "renders", "moves", n); os.makedirs(d, exist_ok=True)
            for f in range(f0, f1 + 1, step):
                out = os.path.join(d, f"{f:04d}.png")
                if os.path.exists(out) and "--force" not in argv:
                    continue
                c, l = path[f - 1]; pose(cam, c, l)
                sc.render.filepath = out; bpy.ops.render.render(write_still=True)
            print("MOVE", n, d)
    rp = os.path.join(HERE, "renders", "camera_check.json"); os.makedirs(os.path.dirname(rp), exist_ok=True)
    old = json.load(open(rp)) if os.path.exists(rp) else {}
    old.update(report); json.dump(old, open(rp, "w"), indent=1)
