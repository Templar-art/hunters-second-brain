"""10x Blender kit — build a whole scene from one scene.json, headless.

    blender -b -P projects/blender-kit/build.py -- path/to/x.scene.json [--no-render]

Outputs (into scene.json "output", relative to the json): <name>.blend, guides/, id/,
report.json (stage timings, object counts, density, clearance hits).
Stages: imports -> house -> site -> landscape -> people -> cameras -> lighting -> save -> passes.
"""
import json, math, os, sys, time
import bpy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import core, house, site, landscape, people, cameras, passes  # noqa: E402


def imports(spec, ctx):
    """Bring in job-specific geometry (e.g. the house until the house generator exists) from
    another .blend, skipping everything the kit regenerates."""
    col = core.coll(spec.get("collection", "Imported"))
    pre = tuple(spec.get("exclude_prefixes", []))
    names = set(spec.get("exclude_names", []))
    types = set(spec.get("exclude_types", []))
    with bpy.data.libraries.load(ctx.path(spec["from"]), link=False) as (src, dst):
        dst.objects = [n for n in src.objects if not n.startswith(pre) and n not in names]
    kept = 0
    for o in dst.objects:
        if o is None:
            continue
        if o.type in types:
            bpy.data.objects.remove(o)
            continue
        col.objects.link(o)
        kept += 1
    return kept


def _hdri_sun(world):
    """World-space direction toward the HDRI's brightest pixel (its sun), after the world Mapping
    rotation. Blender equirect: u = -atan2(y, x)/2pi + 0.5, v = atan2(z, hypot(x, y))/pi + 0.5."""
    from mathutils import Matrix, Vector
    nodes = world.node_tree.nodes
    img = next(n.image for n in nodes if n.type == "TEX_ENVIRONMENT")
    W, H = img.size
    px = img.pixels[:]
    best, bx, by = -1.0, 0, 0
    for y in range(0, H, 2):
        for x in range(0, W, 2):
            i = (y * W + x) * 4
            lum = px[i] * 0.2126 + px[i + 1] * 0.7152 + px[i + 2] * 0.0722
            if lum > best:
                best, bx, by = lum, x, y
    az = (0.5 - (bx + 0.5) / W) * 2 * math.pi
    el = ((by + 0.5) / H - 0.5) * math.pi
    d = Vector((math.cos(el) * math.cos(az), math.cos(el) * math.sin(az), math.sin(el)))
    mp = next((n for n in nodes if n.type == "MAPPING"), None)
    if mp:   # POINT mapping looks up env(R @ dir), so the sun appears at R^-1 @ d
        d = mp.inputs["Rotation"].default_value.to_matrix().inverted() @ d
    return d.normalized()


def lighting(spec, ctx):
    """"world_rotation_deg" turns the HDRI about Z. "sun": {"match_hdri": true} aims the lamp at the
    HDRI's own sun and switches off the world's extracted sun shadow, so there is one sun, not two."""
    sc = bpy.context.scene
    if spec.get("world"):
        sc.world = bpy.data.worlds[spec["world"]]
    if "world_rotation_deg" in spec:
        mp = next(n for n in sc.world.node_tree.nodes if n.type == "MAPPING")
        mp.inputs["Rotation"].default_value[2] = math.radians(spec["world_rotation_deg"])
    s = spec.get("sun")
    if s:
        d = bpy.data.lights.new("Sun", "SUN")
        d.energy = s.get("energy", 5)
        d.angle = math.radians(s.get("angle_deg", 0.8))
        o = bpy.data.objects.new("Sun", d)
        if s.get("match_hdri"):
            sd = _hdri_sun(sc.world)
            o.rotation_euler = sd.to_track_quat("Z", "Y").to_euler()     # lamp +Z points at the sun
            sc.world.use_sun_shadow = False
            ctx.report["sun_dir"] = [round(v, 4) for v in sd]
        else:
            o.rotation_euler = [math.radians(v) for v in s["rotation_deg"]]
        core.coll("Lighting").objects.link(o)


def main():
    argv = sys.argv[sys.argv.index("--") + 1:]
    scene_path = os.path.abspath(argv[0])
    spec = json.load(open(scene_path))
    base = os.path.dirname(scene_path)
    out_dir = os.path.normpath(os.path.join(base, spec.get("output", "build")))
    os.makedirs(out_dir, exist_ok=True)

    bpy.ops.wm.read_homefile(use_empty=True)
    sc = bpy.context.scene
    r = spec.get("render", {})
    sc.render.engine = r.get("engine", "BLENDER_EEVEE")
    sc.render.fps = r.get("fps", 24)
    sc.render.resolution_x, sc.render.resolution_y = r.get("resolution", [1920, 1080])
    sc.view_settings.view_transform = r.get("view_transform", "AgX")
    sc.eevee.taa_render_samples = r.get("samples", 64)

    ctx = core.Ctx(spec, base)
    timings, t0 = {}, time.time()

    def stage(name, fn):
        t = time.time()
        res = fn()
        timings[name] = round(time.time() - t, 1)
        print(f"KIT {name}: {timings[name]}s", flush=True)
        return res

    stage("assets", lambda: core.load_assets(ctx.path(spec["assets"])))
    for i, imp in enumerate(spec.get("imports", [])):
        n = stage(f"import_{i}", lambda imp=imp: imports(imp, ctx))
        ctx.report[f"imported_{i}"] = n
    if "house" in spec:
        stage("house", lambda: house.build(spec["house"], ctx))
    if "site" in spec:
        stage("site", lambda: site.build(spec["site"], ctx))
    if "landscape" in spec:
        stage("landscape", lambda: landscape.build(spec["landscape"], ctx))
    if "people" in spec:
        stage("people", lambda: people.build(spec["people"], ctx))
    if "shots" in spec:
        stage("cameras", lambda: cameras.build(spec["shots"], ctx))
    stage("lighting", lambda: lighting(spec.get("lighting", {}), ctx))

    blend = os.path.join(out_dir, spec.get("name", "scene") + ".blend")
    stage("save", lambda: bpy.ops.wm.save_as_mainfile(filepath=blend, compress=True))
    ctx.report["objects"] = len([o for o in sc.objects if o.users_collection[0].name not in (core.ASSET_COL,) and not o.users_collection[0].name.startswith("A_")])

    if "passes" in spec:
        p = dict(spec["passes"])
        if "--no-render" in argv:
            p["guides"] = p["id"] = False
        stage("passes", lambda: passes.build(p, ctx, out_dir, blend))

    ctx.report["timings_s"] = {**timings, "total": round(time.time() - t0, 1)}
    ctx.report["blend"] = blend
    json.dump(ctx.report, open(os.path.join(out_dir, "report.json"), "w"), indent=1)
    d = ctx.report.get("density", {})
    print(f"KIT DONE {ctx.report['objects']} objects in {ctx.report['timings_s']['total']}s; "
          f"density fails={d.get('fails')}; clearance hits={len(ctx.report.get('clearance', []))}", flush=True)


main()
