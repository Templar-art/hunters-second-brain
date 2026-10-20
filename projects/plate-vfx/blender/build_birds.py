"""Build (and optionally render) a CG bird pass on a fitted plate camera.

  Blender -b --factory-startup --python blender/build_birds.py -- <job>/shot.json [--render] [--frame N]

Reads <job>/camera.json, <job>/plate.json, <job>/layout.json and the tier in shot.json.
Writes <job>/birds_<tier>.blend and RGBA PNGs to <job>/render/<tier>/b_####.png.
"""
import bpy, json, math, os, sys
from mathutils import Euler, Matrix, Vector

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "lib"))
import flight  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:]
SHOT = os.path.abspath(argv[0])
JOB = os.path.dirname(SHOT)
DO_RENDER = "--render" in argv
ONE_FRAME = int(argv[argv.index("--frame") + 1]) if "--frame" in argv else None
shot = json.load(open(SHOT))
TIER = argv[argv.index("--tier") + 1] if "--tier" in argv else shot.get("tier", "standard")
cam_data = json.load(open(os.path.join(JOB, "camera.json")))
plate = json.load(open(os.path.join(JOB, "plate.json")))
birds = json.load(open(os.path.join(JOB, "layout.json")))["birds"]
N = len(cam_data["frames"])
FPS = cam_data["fps"][0] / cam_data["fps"][1]
W, H = cam_data["width"], cam_data["height"]
F_PX = cam_data["lens_mm"] / 36 * W
A0 = shot["range"][0]  # first plate frame of the shot

TIERS = {
    #           sphere seg/ring, body subsurf, wing subsurf, engine, samples, motion blur, res %
    "draft":    dict(seg=(12, 8), body_sub=0, wing_sub=0, engine="EEVEE", samples=8, blur=False, res=50),
    "standard": dict(seg=(32, 16), body_sub=1, wing_sub=3, engine="EEVEE", samples=64, blur=True, res=100),
    "hero":     dict(seg=(48, 24), body_sub=2, wing_sub=4, engine="CYCLES", samples=128, blur=True, res=100),
}
T = TIERS[TIER]

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.frame_start, sc.frame_end = 1, N
sc.render.fps, sc.render.fps_base = cam_data["fps"]
sc.render.resolution_x, sc.render.resolution_y = W, H
sc.render.resolution_percentage = T["res"]
sc.render.film_transparent = True
sc.view_settings.view_transform = 'Standard'  # plate is display-referred Rec.709
sc.view_settings.look = 'None'
if T["engine"] == "CYCLES":
    sc.render.engine = 'CYCLES'
    sc.cycles.samples = T["samples"]
    sc.cycles.use_denoising = True
    try:
        bpy.context.preferences.addons["cycles"].preferences.compute_device_type = 'METAL'
        bpy.context.preferences.addons["cycles"].preferences.get_devices()
        for d in bpy.context.preferences.addons["cycles"].preferences.devices:
            d.use = True
        sc.cycles.device = 'GPU'
    except Exception:
        pass
else:
    try:
        sc.render.engine = 'BLENDER_EEVEE'
    except TypeError:
        sc.render.engine = 'BLENDER_EEVEE_NEXT'
    try:
        sc.eevee.taa_render_samples = T["samples"]
        sc.eevee.motion_blur_steps = 4
    except AttributeError:
        pass
sc.render.use_motion_blur = T["blur"]
sc.render.motion_blur_shutter = shot.get("shutter", 0.2)  # ~1/120s: drone-typical without heavy ND

# ---------------- camera
cd = bpy.data.cameras.new("PlateCam")
cd.sensor_fit = 'HORIZONTAL'
cd.sensor_width = cam_data["sensor_mm"]
cd.lens = cam_data["lens_mm"]
cd.clip_start, cd.clip_end = 0.1, 20000
cam = bpy.data.objects.new("PlateCam", cd)
sc.collection.objects.link(cam)
sc.camera = cam
for i, M in enumerate(cam_data["frames"]):
    cam.matrix_world = Matrix(M)
    cam.keyframe_insert("location", frame=i + 1)
    cam.keyframe_insert("rotation_euler", frame=i + 1)

img = bpy.data.images.load(os.path.join(JOB, "frames", f"f_{A0:04d}.png"))
img.source = 'SEQUENCE'
cd.show_background_images = True
bg = cd.background_images.new()
bg.image = img
bg.image_user.frame_duration = N
bg.image_user.frame_start = 1
bg.image_user.use_auto_refresh = True
bg.alpha = 1.0

# ---------------- light matched to the plate
sky = plate["sky_linear_rgb"]
lum = max(1e-3, 0.2126 * sky[0] + 0.7152 * sky[1] + 0.0722 * sky[2])
fill = [0.70 * c / lum for c in sky]  # keep the plate's sky hue at a known-good level
warm = max(-0.15, min(0.15, plate["warmth_rb"] - 1.0))
world = bpy.data.worlds.new("Sky")
sc.world = world
world.use_nodes = True
bgn = next(n for n in world.node_tree.nodes if n.type == 'BACKGROUND')
bgn.inputs[0].default_value = (*fill, 1)
bgn.inputs[1].default_value = 0.9
sun_d = bpy.data.lights.new("Sun", 'SUN')
sun_d.energy = shot.get("sun_energy", 2.6)
sun_d.angle = math.radians(shot.get("sun_softness_deg", 25))
sun_d.color = (1.0, 0.95 + 0.2 * warm * -0.25, 0.87 - 0.6 * warm)
sun = bpy.data.objects.new("Sun", sun_d)
sc.collection.objects.link(sun)
sun.rotation_euler = [math.radians(a) for a in shot.get("sun_euler_deg", [45, -30, -35])]


# ---------------- gull
def mat(name, rgb, rough=0.6):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    p = next(n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
    p.inputs["Base Color"].default_value = (*rgb, 1)
    p.inputs["Roughness"].default_value = rough
    try:
        p.inputs["Subsurface Weight"].default_value = 0.08  # light through feathers
    except KeyError:
        pass
    return m


def two_tone(name, top, under):
    """Upper surface `top`, underside `under` (by object-space normal Z)."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    p = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED')
    p.inputs["Roughness"].default_value = 0.65
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    mr = nt.nodes.new("ShaderNodeMapRange")
    mr.inputs["From Min"].default_value, mr.inputs["From Max"].default_value = -0.2, 0.2
    mix = nt.nodes.new("ShaderNodeMix")
    mix.data_type = 'RGBA'
    mix.inputs["A"].default_value = (*under, 1)
    mix.inputs["B"].default_value = (*top, 1)
    nt.links.new(tc.outputs["Normal"], sep.inputs[0])
    nt.links.new(sep.outputs["Z"], mr.inputs["Value"])
    nt.links.new(mr.outputs["Result"], mix.inputs["Factor"])
    nt.links.new(mix.outputs["Result"], p.inputs["Base Color"])
    return m


M_WHITE = mat("GullWhite", (0.86, 0.85, 0.82))
M_BLACK = mat("GullTip", (0.03, 0.03, 0.035))
M_BILL = mat("GullBill", (0.55, 0.06, 0.04), 0.4)
M_WING = two_tone("GullWing", (0.55, 0.56, 0.58), (0.78, 0.77, 0.75))


def mesh_obj(name, verts, faces, material, parent=None, solid=0.012):
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    o = bpy.data.objects.new(name, me)
    sc.collection.objects.link(o)
    o.data.materials.append(material)
    if T["wing_sub"]:
        # crease the outline so the planform keeps its points, smooth the interior
        crease = me.attributes.new("crease_edge", 'FLOAT', 'EDGE')
        use = {}
        for p in me.polygons:
            for ek in p.edge_keys:
                use[ek] = use.get(ek, 0) + 1
        for e in me.edges:
            crease.data[e.index].value = 0.85 if use.get(tuple(sorted(e.vertices)), 0) == 1 else 0.0
        sub = o.modifiers.new("subd", 'SUBSURF')
        sub.levels = sub.render_levels = T["wing_sub"]
        for p in me.polygons:
            p.use_smooth = True
    if solid:
        o.modifiers.new("thick", 'SOLIDIFY').thickness = solid
    o.parent = parent
    return o


def ellipsoid(name, center, radii, material, parent):
    seg, ring = T["seg"]
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=ring, radius=1, location=center)
    o = bpy.context.active_object
    o.name, o.scale, o.parent = name, radii, parent
    o.data.materials.append(material)
    for p in o.data.polygons:
        p.use_smooth = True
    if T["body_sub"]:
        sub = o.modifiers.new("subd", 'SUBSURF')
        sub.levels = sub.render_levels = T["body_sub"]
    return o


class ProceduralGull:
    """Silver gull. Local axes: +Y forward, +Z up, span along X."""

    def __init__(self, tag, span):
        s = span / 1.1
        self.root = bpy.data.objects.new(f"Gull_{tag}", None)
        sc.collection.objects.link(self.root)
        r = self.root
        ellipsoid(f"{tag}_body", (0, 0, 0), (0.055 * s, 0.19 * s, 0.058 * s), M_WHITE, r)
        ellipsoid(f"{tag}_head", (0, 0.175 * s, 0.03 * s), (0.04 * s, 0.05 * s, 0.042 * s), M_WHITE, r)
        bpy.ops.mesh.primitive_cone_add(vertices=24 if TIER != "draft" else 8, radius1=0.01 * s, depth=0.045 * s,
                                        location=(0, 0.245 * s, 0.022 * s), rotation=(-math.pi / 2, 0, 0))
        bill = bpy.context.active_object
        bill.name = f"{tag}_bill"; bill.data.materials.append(M_BILL); bill.parent = r
        mesh_obj(f"{tag}_tail", [(-0.03 * s, -0.15 * s, 0.01 * s), (0.03 * s, -0.15 * s, 0.01 * s),
                                 (0.05 * s, -0.27 * s, 0.0), (-0.05 * s, -0.27 * s, 0.0)], [(0, 1, 2, 3)], M_WHITE, r, 0.006)
        self.wings = []
        for side in (1, -1):
            x = lambda v: v * side * s
            y = lambda v: v * s
            inner = bpy.data.objects.new(f"{tag}_wingIn_{side}", None)  # shoulder pivot
            sc.collection.objects.link(inner)
            inner.parent, inner.location = r, (x(0.045), y(0.05), y(0.025))
            mesh_obj(f"{tag}_arm_{side}",
                     [(0, y(0.06), 0), (x(0.10), y(0.065), y(0.008)), (x(0.20), y(0.06), y(0.006)),
                      (x(0.20), y(-0.10), 0), (x(0.10), y(-0.115), 0), (0, y(-0.12), 0)],
                     [(0, 1, 4, 5), (1, 2, 3, 4)], M_WING, inner, 0.01 * s)
            outer = bpy.data.objects.new(f"{tag}_wingOut_{side}", None)  # wrist pivot
            sc.collection.objects.link(outer)
            outer.parent, outer.location = inner, (x(0.20), 0, 0)
            mesh_obj(f"{tag}_hand_{side}",
                     [(0, y(0.06), 0), (x(0.10), y(0.045), 0), (x(0.17), y(0.02), 0),
                      (x(0.17), y(-0.105), 0), (x(0.10), y(-0.11), 0), (0, y(-0.10), 0)],
                     [(0, 1, 4, 5), (1, 2, 3, 4)], M_WING, outer, 0.008 * s)
            mesh_obj(f"{tag}_tip_{side}",
                     [(x(0.17), y(0.02), 0), (x(0.25), y(-0.03), 0), (x(0.30), y(-0.10), 0), (x(0.17), y(-0.105), 0)],
                     [(0, 1, 2, 3)], M_BLACK, outer, 0.006 * s)
            self.wings.append((side, inner, outer))

    def key(self, k):
        f = k["frame"]
        self.root.location = Vector(k["pos"])
        self.root.rotation_euler = k["euler"]
        self.root.keyframe_insert("location", frame=f)
        self.root.keyframe_insert("rotation_euler", frame=f)
        p = k["wings"]
        for side, inner, outer in self.wings:
            inner.rotation_euler = (0, -side * math.radians(p["elev"]), -side * math.radians(p["arm_sweep"]))
            outer.rotation_euler = (math.radians(p["twist"]), -side * math.radians(p["hand_dih"]), -side * math.radians(p["hand_sweep"]))
            inner.keyframe_insert("rotation_euler", frame=f)
            outer.keyframe_insert("rotation_euler", frame=f)


ASSET = os.path.join(HERE, "..", "assets", "gull_herring.blend")
MODEL = shot.get("model", {"draft": "procedural"}.get(TIER, "asset"))
if MODEL == "asset" and not os.path.exists(ASSET):
    MODEL = "procedural"


class AssetGull:
    """Rigged herring gull from assets/gull_herring.blend (CC BY, credit in the object's 'attribution')."""
    base = None

    def __init__(self, tag, span):
        if AssetGull.base is None:
            with bpy.data.libraries.load(ASSET, link=False) as (src, dst):
                dst.objects = ["GullRig", "GullHerring"]
            AssetGull.base = dst.objects
        brig, bmesh_ = AssetGull.base
        self.rig = brig.copy(); self.rig.name = f"Gull_{tag}"
        sc.collection.objects.link(self.rig)
        m = bmesh_.copy(); m.name = f"{tag}_mesh"
        sc.collection.objects.link(m)
        m.parent = self.rig
        m.matrix_parent_inverse.identity()
        m.modifiers["rig"].object = self.rig
        if TIER == "hero":
            sub = m.modifiers.new("subd", 'SUBSURF')
            sub.levels = sub.render_levels = 1
        self.rig.scale = (span, span, span)
        for pb in self.rig.pose.bones:
            pb.rotation_mode = 'XYZ'

    def key(self, k):
        f = k["frame"]
        self.rig.location = Vector(k["pos"])
        self.rig.rotation_euler = k["euler"]
        self.rig.keyframe_insert("location", frame=f)
        self.rig.keyframe_insert("rotation_euler", frame=f)
        p = k["wings"]
        for side, sfx in ((1, "L"), (-1, "R")):
            for bn, eul in ((f"arm.{sfx}", (0, -side * math.radians(p["elev"]), -side * math.radians(p["arm_sweep"]))),
                            (f"hand.{sfx}", (math.radians(p["twist"]), -side * math.radians(p["hand_dih"]),
                                             -side * math.radians(p["hand_sweep"])))):
                pb = self.rig.pose.bones[bn]
                B = pb.bone.matrix_local.to_3x3()
                pb.rotation_euler = (B.inverted() @ Euler(eul, 'XYZ').to_matrix() @ B).to_euler('XYZ')
                pb.keyframe_insert("rotation_euler", frame=f)


M1 = cam_data["frames"][0]
print("MODEL", MODEL)
for b in birds:
    gull = (AssetGull if MODEL == "asset" else ProceduralGull)(b["tag"], b["span"])
    for k in flight.simulate(b, M1, F_PX, FPS, N):
        gull.key(k)

out_dir = os.path.join(JOB, "render", TIER)
os.makedirs(out_dir, exist_ok=True)
sc.render.image_settings.file_format = 'PNG'
sc.render.image_settings.color_mode = 'RGBA'
sc.render.filepath = os.path.join(out_dir, "b_")
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(JOB, f"birds_{TIER}.blend"))
if ONE_FRAME:
    sc.frame_set(ONE_FRAME)
    sc.render.filepath = os.path.join(out_dir, f"pilot_{ONE_FRAME:04d}.png")
    bpy.ops.render.render(write_still=True)
elif DO_RENDER:
    bpy.ops.render.render(animation=True)
print("BUILD_OK", TIER)
