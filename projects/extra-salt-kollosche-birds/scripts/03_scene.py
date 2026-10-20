"""Build the bird scene on the fitted drone camera and render an RGBA bird pass.

  Blender -b --factory-startup --python scripts/03_scene.py [-- --preview]
Saves birds.blend (plate as camera background) and renders render/b_####.png (frames 1-45).
"""
import bpy, json, math, os, sys
from mathutils import Matrix, Vector

JOB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cam_data = json.load(open(os.path.join(JOB, "camera.json")))
N = len(cam_data["frames"])
PREVIEW = "--preview" in sys.argv
FPS = cam_data["fps"][0] / cam_data["fps"][1]

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.frame_start, sc.frame_end = 1, N
sc.render.fps, sc.render.fps_base = cam_data["fps"]
sc.render.resolution_x, sc.render.resolution_y = 1920, 1080
sc.render.resolution_percentage = 100
sc.render.film_transparent = True
sc.view_settings.view_transform = 'Standard'  # plate is display-referred Rec.709
sc.view_settings.look = 'None'
try:
    sc.render.engine = 'BLENDER_EEVEE'
except TypeError:
    sc.render.engine = 'BLENDER_EEVEE_NEXT'
sc.render.use_motion_blur = True
sc.render.motion_blur_shutter = 0.2  # ~1/120s, drone-typical without heavy ND
try:
    sc.eevee.motion_blur_steps = 4
    sc.eevee.taa_render_samples = 64
except AttributeError:
    pass

# ---------------- camera
cd = bpy.data.cameras.new("DroneCam")
cd.sensor_fit = 'HORIZONTAL'
cd.sensor_width = cam_data["sensor_mm"]
cd.lens = cam_data["lens_mm"]
cd.clip_start, cd.clip_end = 0.1, 20000
cam = bpy.data.objects.new("DroneCam", cd)
sc.collection.objects.link(cam)
sc.camera = cam
for i, M in enumerate(cam_data["frames"]):
    cam.matrix_world = Matrix(M)
    cam.keyframe_insert("location", frame=i + 1)
    cam.keyframe_insert("rotation_euler", frame=i + 1)
for fc in cam.animation_data.action.fcurves if hasattr(cam.animation_data.action, "fcurves") else []:
    for k in fc.keyframe_points:
        k.interpolation = 'LINEAR'

# plate as camera background (for the .blend; not rendered)
img = bpy.data.images.load(os.path.join(JOB, "frames", "f_0001.png"))
img.source = 'SEQUENCE'
cd.show_background_images = True
bg = cd.background_images.new()
bg.image = img
bg.image_user.frame_duration = N
bg.image_user.frame_start = 1
bg.image_user.use_auto_refresh = True
bg.alpha = 1.0

# ---------------- light: soft overcast sun from upper left + sky fill
world = bpy.data.worlds.new("Sky")
sc.world = world
world.use_nodes = True
bgn = next(n for n in world.node_tree.nodes if n.type == 'BACKGROUND')
bgn.inputs[0].default_value = (0.70, 0.70, 0.69, 1)
bgn.inputs[1].default_value = 0.9
sun_d = bpy.data.lights.new("Sun", 'SUN')
sun_d.energy = 2.6
sun_d.angle = math.radians(25)  # hazy sun = soft shadows
sun_d.color = (1.0, 0.95, 0.87)
sun = bpy.data.objects.new("Sun", sun_d)
sc.collection.objects.link(sun)
sun.rotation_euler = (math.radians(45), math.radians(-30), math.radians(-35))


# ---------------- gull materials
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


M_WHITE = mat("GullWhite", (0.86, 0.85, 0.82))
M_GREY = mat("GullGrey", (0.50, 0.53, 0.57))
M_BLACK = mat("GullTip", (0.03, 0.03, 0.035))
M_BILL = mat("GullBill", (0.55, 0.06, 0.04), 0.4)


def mesh_obj(name, verts, faces, material, parent=None, solid=0.012):
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    o = bpy.data.objects.new(name, me)
    sc.collection.objects.link(o)
    o.data.materials.append(material)
    # densify: crease the outline so the wing planform keeps its points, smooth the interior
    crease = me.attributes.new("crease_edge", 'FLOAT', 'EDGE')
    use = {}
    for p in me.polygons:
        for ek in p.edge_keys:
            use[ek] = use.get(ek, 0) + 1
    for e in me.edges:
        crease.data[e.index].value = 0.85 if use.get(tuple(sorted(e.vertices)), 0) == 1 else 0.0
    sub = o.modifiers.new("subd", 'SUBSURF')
    sub.levels = sub.render_levels = 3
    for p in me.polygons:
        p.use_smooth = True
    if solid:
        mod = o.modifiers.new("thick", 'SOLIDIFY')
        mod.thickness = solid
    o.parent = parent
    return o


def ellipsoid(name, center, radii, material, parent, seg=32, ring=16):
    seg, ring = max(seg, 32), max(ring, 16)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=ring, radius=1, location=center)
    o = bpy.context.active_object
    o.name = name
    o.scale = radii
    o.data.materials.append(material)
    o.parent = parent
    for p in o.data.polygons:
        p.use_smooth = True
    sub = o.modifiers.new("subd", 'SUBSURF')
    sub.levels = sub.render_levels = 1
    return o


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


M_WING = two_tone("GullWing", (0.55, 0.56, 0.58), (0.78, 0.77, 0.75))


def make_gull(tag, span=0.95):
    """Silver gull. Local axes: +Y forward, +Z up, span along X. Returns (root, wings)."""
    s = span / 1.1
    root = bpy.data.objects.new(f"Gull_{tag}", None)
    sc.collection.objects.link(root)
    ellipsoid(f"{tag}_body", (0, 0, 0), (0.055 * s, 0.19 * s, 0.058 * s), M_WHITE, root, 16, 10)
    ellipsoid(f"{tag}_head", (0, 0.175 * s, 0.03 * s), (0.04 * s, 0.05 * s, 0.042 * s), M_WHITE, root)
    bpy.ops.mesh.primitive_cone_add(vertices=24, radius1=0.01 * s, depth=0.045 * s,
                                    location=(0, 0.245 * s, 0.022 * s), rotation=(-math.pi / 2, 0, 0))
    bill = bpy.context.active_object
    bill.name = f"{tag}_bill"; bill.data.materials.append(M_BILL); bill.parent = root
    mesh_obj(f"{tag}_tail", [(-0.03 * s, -0.15 * s, 0.01 * s), (0.03 * s, -0.15 * s, 0.01 * s),
                             (0.05 * s, -0.27 * s, 0.0), (-0.05 * s, -0.27 * s, 0.0)], [(0, 1, 2, 3)], M_WHITE, root, 0.006)
    wings = []
    for side in (1, -1):
        x = lambda v: v * side * s
        y = lambda v: v * s
        inner = bpy.data.objects.new(f"{tag}_wingIn_{side}", None)  # shoulder pivot
        sc.collection.objects.link(inner)
        inner.parent = root
        inner.location = (x(0.045), y(0.05), y(0.025))
        # arm: slight camber (raised mid-chord)
        mesh_obj(f"{tag}_arm_{side}",
                 [(0, y(0.06), 0), (x(0.10), y(0.065), y(0.008)), (x(0.20), y(0.06), y(0.006)),
                  (x(0.20), y(-0.10), 0), (x(0.10), y(-0.115), 0), (0, y(-0.12), 0)],
                 [(0, 1, 4, 5), (1, 2, 3, 4)], M_WING, inner, 0.01 * s)
        outer = bpy.data.objects.new(f"{tag}_wingOut_{side}", None)  # wrist pivot
        sc.collection.objects.link(outer)
        outer.parent = inner
        outer.location = (x(0.20), 0, 0)
        mesh_obj(f"{tag}_hand_{side}",
                 [(0, y(0.06), 0), (x(0.10), y(0.045), 0), (x(0.17), y(0.02), 0),
                  (x(0.17), y(-0.105), 0), (x(0.10), y(-0.11), 0), (0, y(-0.10), 0)],
                 [(0, 1, 4, 5), (1, 2, 3, 4)], M_WING, outer, 0.008 * s)
        mesh_obj(f"{tag}_tip_{side}",
                 [(x(0.17), y(0.02), 0), (x(0.25), y(-0.03), 0), (x(0.30), y(-0.10), 0), (x(0.17), y(-0.105), 0)],
                 [(0, 1, 2, 3)], M_BLACK, outer, 0.006 * s)
        wings.append((side, inner, outer))
    return root, wings


# ---------------- flight paths (defined in frame-1 camera space, flown in world space)
M1 = Matrix(cam_data["frames"][0])
cam_right = (M1.to_3x3() @ Vector((1, 0, 0)))
cam_right.z = 0
cam_right.normalize()
cam_fwd_h = (M1.to_3x3() @ Vector((0, 0, -1)))
cam_fwd_h.z = 0
cam_fwd_h.normalize()
f_px = cam_data["lens_mm"] / 36 * 1920

# (tag, depth m, start screen x px from centre, screen y px from centre(+up), speed m/s,
#  flap Hz, phase (cycles), mid-shot heading toward/away from camera deg, span m,
#  bank deg (far wing raised so the drone sees the bird's back; also sets the turn rate),
#  glide windows in seconds)
BIRDS = [
    ("hero", 7.0, -520, -600, 10.0, 2.9, 0.00, 50, 0.95, 12, [(0.95, 1.35)]),
    ("b2", 11.0, -950, -470, 9.5, 3.2, 0.35, 44, 0.92, 10, [(0.0, 0.40)]),
    ("b3", 16.0, -1150, -230, 9.8, 2.7, 0.60, 40, 0.98, 14, [(0.75, 9.0)]),
    ("b4", 22.0, -1260, -60, 10.5, 3.1, 0.15, 36, 0.92, 8, [(1.30, 1.70)]),
]
if PREVIEW:
    sc.render.resolution_percentage = 50

TOP, BOT, DOWN = 50.0, -28.0, 0.58  # arm elevation range (deg); downstroke takes 58% of the beat
T_SHOT = (N - 1) / FPS


def smooth(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def elev(u):
    """Arm elevation through one beat: slow powered downstroke, quick recovery."""
    u %= 1.0
    if u < DOWN:
        return TOP + (BOT - TOP) * (1 - math.cos(math.pi * u / DOWN)) / 2
    return BOT + (TOP - BOT) * (1 - math.cos(math.pi * (u - DOWN) / (1 - DOWN))) / 2


def w_up(u):
    u %= 1.0
    return math.sin(math.pi * (u - DOWN) / (1 - DOWN)) if u >= DOWN else 0.0


def w_dn(u):
    u %= 1.0
    return math.sin(math.pi * u / DOWN) if u < DOWN else 0.0


def glide_w(t, windows, ramp=0.15):
    g = 0.0
    for a, b in windows:
        g = max(g, smooth((t - a) / ramp) * (1 - smooth((t - b) / ramp)) if a > 0 else 1 - smooth((t - b) / ramp))
    return g


GLIDE = dict(elev=6.0, arm_sweep=6.0, hand_dih=-6.0, hand_sweep=12.0, twist=0.0)
SUB = 4  # integration substeps per frame
KEY_STEP = 0.5  # keyframe every half frame so motion blur follows the wingbeat

for tag, depth, sx, sy, speed, hz, ph, tilt, span, bank, glides in BIRDS:
    root, wings = make_gull(tag, span)
    pos = M1 @ Vector((sx / f_px * depth, sy / f_px * depth, -depth))
    omega0 = 9.81 * math.tan(math.radians(bank)) / speed  # coordinated turn rate
    ang = math.radians(tilt) + omega0 * T_SHOT / 2  # so mid-shot heading == tilt
    phase = ph
    dt = 1 / (FPS * SUB)
    t = 0.0
    next_key = 1.0
    frame = 1.0
    while frame <= N + 1e-6:
        g = glide_w(t, glides)
        u = phase % 1.0
        # ---- wing pose: flap blended toward a held glide pose
        fl = dict(elev=elev(u), arm_sweep=14 * w_up(u),
                  hand_dih=0.55 * (elev(u - 0.07) - elev(u)) - 4,
                  hand_sweep=40 * w_up(u), twist=-9 * w_dn(u))
        pose = {k: (1 - g) * fl[k] + g * GLIDE[k] for k in fl}
        # ---- body: lifts as the wings come down (lagged), noses up slightly on the power stroke
        lowness = (TOP - elev(u - 0.22)) / (TOP - BOT)
        lift = (1 - g) * 0.05 * span * (lowness - 0.5)
        roll = bank + 2.0 * math.sin(1.3 * t + ph * 6)
        if frame >= next_key - 1e-6:
            dirv = cam_right * math.cos(ang) + cam_fwd_h * math.sin(ang)
            heading = math.atan2(dirv.y, dirv.x) - math.pi / 2  # local +Y faces travel
            root.location = pos + Vector((0, 0, lift))
            root.rotation_euler = (math.radians(-4 + 2.5 * (1 - g) * w_dn(u) - 1.5 * g), math.radians(roll), heading)
            root.keyframe_insert("location", frame=next_key)
            root.keyframe_insert("rotation_euler", frame=next_key)
            for side, inner, outer in wings:
                inner.rotation_euler = (0, -side * math.radians(pose["elev"]), -side * math.radians(pose["arm_sweep"]))
                outer.rotation_euler = (math.radians(pose["twist"]), -side * math.radians(pose["hand_dih"]),
                                        -side * math.radians(pose["hand_sweep"]))
                inner.keyframe_insert("rotation_euler", frame=next_key)
                outer.keyframe_insert("rotation_euler", frame=next_key)
            next_key += KEY_STEP
        # ---- integrate: surge on the downstroke, climb while flapping, sink while gliding
        v = speed * ((1 - g) * (1 + 0.05 * w_dn(u)) + g * 0.97)
        dirv = cam_right * math.cos(ang) + cam_fwd_h * math.sin(ang)
        pos = pos + dirv * v * dt + Vector((0, 0, ((1 - g) * 0.25 - g * 0.7) * dt))
        ang -= 9.81 * math.tan(math.radians(roll)) / v * dt  # right wing low -> turn right
        phase += hz * (1 - g) * dt
        t += dt
        frame += 1 / SUB

sc.render.image_settings.file_format = 'PNG'
sc.render.image_settings.color_mode = 'RGBA'
sc.render.filepath = os.path.join(JOB, "render", "b_")
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(JOB, "birds.blend"))
if "--norender" not in sys.argv:
    bpy.ops.render.render(animation=True)
print("DONE")
