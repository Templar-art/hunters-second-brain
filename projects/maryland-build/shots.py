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
    "gate":         ("golden", ((150.6, 1.6, 1.5), (136.8, 3.8, 1.7)), ((80, 13, 3.2), (79, 13, 3.4)), 32, 0, 125),
    "drive":        ("golden", ((124, 3.0, 1.4), (100, 4.2, 1.7)), ((66, 12, 3.6), (66, 12, 3.8)), 32, 0, 125),
    "pool_hero":    ("dusk",   ((22.5, 13.5, 1.0), (22.5, 21.5, 1.0)), ((55, 17, 4.2), (55, 19, 4.2)), 22, 0, 150),
    "bench_water":  ("golden", ((16.8, 14.4, 1.2), (16.2, 13.5, 1.15)), ((-30, 11.5, 0.2), (-30, 12.5, 0.2)), 35, 2.8, 125),
    "balcony_dusk": ("dusk",   (P(660, 470, UP + 1.55), P(628, 470, UP + 1.45)), ((-30, 18, 2), (-30, 16, 1)), 24, 0, 125),
    "closing":      ("dusk",   ((10, 10, 18), (-26, -8, 40)), ((58, 17, 2), (60, 16, 0)), 24, 0, 175),
    # ---- interior (ground)
    "lounge":       ("day", (P(722, 462, EYE), P(758, 462, EYE)), (P(722, 366, 1.0), P(746, 366, 1.0)), 22, 0, 125),
    "kitchen":      ("day", (P(762, 440, 1.5), P(814, 440, 1.5)), (P(770, 500, 0.95), P(808, 500, 0.95)), 24, 0, 125),
    "dining":       ("day", (P(764, 412, EYE), P(764, 384, EYE)), (P(820, 397, 0.9), P(820, 397, 0.9)), 24, 0, 125),
    "family":       ("day", (P(706, 578, EYE), P(706, 562, EYE)), (P(690, 510, 1.1), P(690, 510, 1.1)), 20, 0, 125),
    "outdoor":      ("golden", (P(664, 560, EYE), P(632, 548, 1.6)), (P(520, 470, 1.0), P(520, 470, 1.0)), 22, 0, 125),
    "media":        ("dusk", (P(965, 410, EYE), P(950, 410, EYE)), (P(935, 488, 1.2), P(935, 488, 1.2)), 20, 0, 125),
    # ---- interior (upper)
    "master":       ("day", (P(712, 512, UP + 1.5), P(722, 500, UP + 1.45)), (P(767, 476, UP + 0.9), P(767, 476, UP + 0.9)), 20, 0, 125),
    "upper_living": ("day", (P(888, 400, UP + 1.5), P(888, 412, UP + 1.5)), (P(968, 400, UP + 1.0), P(968, 400, UP + 1.0)), 20, 0, 125),
}

EXPOSURE = {"lounge": 1.1, "kitchen": 1.0, "dining": 1.0, "family": 1.0, "outdoor": 0.0, "media": 1.0,
            "master": 2.0, "upper_living": 2.0, "balcony_dusk": 1.0, "pool_hero": 1.0, "closing": 1.0,
            "aerial": -0.5, "gate": -0.5, "drive": -0.5, "bench_water": -0.5}

FOCUS = {"bench_water": 3.9}
OUTSIDE = {"aerial", "gate", "drive", "pool_hero", "bench_water", "balcony_dusk", "closing", "outdoor"}

LIGHTS = {   # hdr, hdr strength, sun dir (toward the sun: azimuth deg from +X, elevation deg), sun energy, interior x
    "day":    ("kloofendal_48d_partly_cloudy_puresky", 1.0, (115, 48), 4.0, 0.6),
    "golden": ("rosendal_park_sunset_puresky", 1.1, (192, 6), 6.0, 0.8),
    "dusk":   ("qwantani_dusk_2_puresky", 0.55, (200, -2.5), 0.0, 6.0),
}


def setup_light(name):
    hdr, hs, (az, el), se, ix = LIGHTS[name]
    w = sc.world; nt = w.node_tree
    env = next(n for n in nt.nodes if n.type == "TEX_ENVIRONMENT")
    bg = next(n for n in nt.nodes if n.type == "BACKGROUND")
    sky = nt.nodes.get("phys_sky") or nt.nodes.new("ShaderNodeTexSky"); sky.name = "phys_sky"
    if name in ("golden", "dusk"):                     # physical sky: the glow sits exactly where the sun is
        sky.sky_type = "MULTIPLE_SCATTERING"; sky.sun_elevation = math.radians(el); sky.sun_rotation = math.radians(90 - az)
        sky.sun_disc = name == "golden"; sky.air_density = 1.0; sky.aerosol_density = 0.5 if name == "golden" else 1.0
        nt.links.new(sky.outputs["Color"], bg.inputs["Color"])
    else:
        nt.links.new(env.outputs["Color"], bg.inputs["Color"])
    if name == "day":
        env.image = bpy.data.images.load(os.path.join(HERE, "..", "sky-library", "hdr_2k", hdr + ".hdr"), check_existing=True)
    m = nt.nodes.get("sky_map") or nt.nodes.new("ShaderNodeMapping"); m.name = "sky_map"
    tc = nt.nodes.get("sky_tc") or nt.nodes.new("ShaderNodeTexCoord"); tc.name = "sky_tc"
    nt.links.new(tc.outputs["Generated"], m.inputs["Vector"]); nt.links.new(m.outputs["Vector"], env.inputs["Vector"])
    # rotate the HDR so its sun sits where the scene sun is (HDR sun assumed at its u = 0.5, i.e. -X)
    m.inputs["Rotation"].default_value = (0, 0, math.radians(az + 180))
    bg.inputs["Strength"].default_value = hs if name == "day" else (0.15 if name == "golden" else 1.4)
    sun = bpy.data.objects["sun"]; sun.hide_render = se <= 0
    d = Vector((math.cos(math.radians(el)) * math.cos(math.radians(az)), math.cos(math.radians(el)) * math.sin(math.radians(az)), math.sin(math.radians(el))))
    sun.rotation_euler = (-d).to_track_quat("-Z", "Y").to_euler(); sun.data.energy = se; sun.data.angle = math.radians(1.2)
    sun.data.color = (1.0, 0.62, 0.32) if name == "golden" else (1.0, 0.96, 0.9)
    for o in bpy.data.collections["interior_lights"].objects:
        if o.type == "LIGHT":
            o.data.energy = o["e0"] * ix
    pool = bpy.data.materials["Pool_water"]; b = next(n for n in pool.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    b.inputs["Emission Color"].default_value = (0.1, 0.55, 0.9, 1); b.inputs["Emission Strength"].default_value = 1.6 if name == "dusk" else 0.0
    gl = next(n for n in bpy.data.materials["Glass_lit_warm"].node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    gl.inputs["Emission Strength"].default_value = 4.0 if name == "dusk" else 0.0
    for mn in ("Pendant_bulb_warm",):
        bb = next(n for n in bpy.data.materials[mn].node_tree.nodes if n.type == "BSDF_PRINCIPLED")
        bb.inputs["Emission Strength"].default_value = 6.0 * max(ix, 0.5)


HAZE = {"day": (0.74, 0.8, 0.88), "golden": (0.95, 0.72, 0.52), "dusk": (0.3, 0.33, 0.48)}


def haze(light, strength=0.55, start=60, depth=1400):
    """atmospheric perspective from the mist pass: far land fades into the light's haze colour"""
    vl = bpy.context.view_layer; vl.use_pass_mist = True
    sc.world.mist_settings.start = start; sc.world.mist_settings.depth = depth; sc.world.mist_settings.falloff = "QUADRATIC"
    tree = sc.compositing_node_group if hasattr(sc, "compositing_node_group") else None
    if tree is None or "--nohaze" in argv:
        try:
            sc.use_nodes = True; tree = sc.node_tree
        except AttributeError:
            pass
    if tree is None:
        tree = bpy.data.node_groups.new("haze_comp", "CompositorNodeTree"); sc.compositing_node_group = tree
    for n in list(tree.nodes):
        tree.nodes.remove(n)
    rl = tree.nodes.new("CompositorNodeRLayers")
    mix = tree.nodes.new("CompositorNodeMixRGB") if hasattr(bpy.types, "CompositorNodeMixRGB") else tree.nodes.new("ShaderNodeMix")
    mul = tree.nodes.new("ShaderNodeMath") if "ShaderNodeMath" in dir(bpy.types) else None
    out = None
    for t in ("CompositorNodeComposite", "NodeGroupOutput"):
        try:
            out = tree.nodes.new(t); break
        except RuntimeError:
            continue
    col_ = (*HAZE[light], 1)
    if mix.bl_idname == "ShaderNodeMix":
        mix.data_type = "RGBA"; mix.inputs["B"].default_value = col_
        mul.operation = "MULTIPLY"; mul.inputs[1].default_value = strength
        tree.links.new(rl.outputs["Mist"], mul.inputs[0]); tree.links.new(mul.outputs[0], mix.inputs["Factor"])
        tree.links.new(rl.outputs["Image"], mix.inputs["A"])
        res = mix.outputs["Result"]
    else:
        mix.inputs[2].default_value = col_
        tree.links.new(rl.outputs["Mist"], mix.inputs[0]); tree.links.new(rl.outputs["Image"], mix.inputs[1]); res = mix.outputs[0]
    if out.bl_idname == "NodeGroupOutput":
        if not tree.interface.items_tree:
            tree.interface.new_socket("Image", in_out="OUTPUT", socket_type="NodeSocketColor")
        tree.links.new(res, out.inputs[0])
    else:
        tree.links.new(res, out.inputs["Image"])


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
        cam.data.dof.focus_distance = FOCUS.get(cam.name[5:], (l - c).length * 0.35)


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


def cull(cam, path, margin=0.3, near=40.0, big=50.0):
    """hide_render everything no frame of this move can see (expanded frustum). Kept regardless: anything within
    `near` m of the camera path (shadows, reflections, bounce) and anything bigger than `big` m (ground, water, sky planes)."""
    from bpy_extras.object_utils import world_to_camera_view
    keep_cols = {"_protos"}
    samples = path[::max(1, len(path) // 12)] + [path[-1]]
    hidden = 0
    obs = [o for o in sc.objects if o.type in {"MESH", "CURVE", "FONT"} and o.name != cam.name
           and not any(c.name in keep_cols for c in o.users_collection)]
    boxes = []
    for o in obs:
        pts = [o.matrix_world @ Vector(b) for b in o.bound_box]
        ctr = sum(pts, Vector()) / 8; diag = (Vector(o.bound_box[6]) - Vector(o.bound_box[0])).length * max(o.scale)
        boxes.append((o, pts + [ctr], ctr, diag))
    seen = set()
    for c, l in samples:
        pose(cam, c, l); bpy.context.view_layer.update()
        for o, pts, ctr, diag in boxes:
            if o.name in seen:
                continue
            if diag > big or (ctr - c).length < near + diag / 2:
                seen.add(o.name); continue
            for p in pts:
                v = world_to_camera_view(sc, cam, p)
                if v.z > 0 and -margin < v.x < 1 + margin and -margin < v.y < 1 + margin:
                    seen.add(o.name); break
    for o, *_ in boxes:
        if o.name not in seen and not o.hide_render:
            o["_cull_was"] = False; o.hide_render = True; hidden += 1
    print(f"CULL {cam.name}: {hidden}/{len(boxes)} objects off-camera, hidden")


def uncull():
    for o in sc.objects:
        if "_cull_was" in o:
            o.hide_render = bool(o["_cull_was"]); del o["_cull_was"]


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
    try:
        sc.view_settings.look = arg("--look", "AgX - Medium High Contrast")
    except TypeError as e:
        print("LOOK not set:", e)
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
    sc.render.use_persistent_data = True              # only the camera moves: keep the BVH between frames
    interior_light_store()
    report = {}
    for n in names:
        spec = list(SHOTS[n])
        if light_override:
            spec[0] = light_override
        setup_light(spec[0]); sc.view_settings.exposure = EXPOSURE.get(n, 0.0)
        if n in OUTSIDE:
            haze(spec[0])
        else:
            haze(spec[0], strength=0.0)
        cam, path = make_cam(n, spec); sc.camera = cam
        bad = check_cam(path)
        report[n] = dict(light=spec[0], camera_issues=bad)
        if bad:
            print("CAMFAIL", n, bad[:3]); continue
        uncull()
        if "--nocull" not in argv:
            cull(cam, path)
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
