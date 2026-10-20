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
    if solid:
        mod = o.modifiers.new("thick", 'SOLIDIFY')
        mod.thickness = solid
    o.parent = parent
    return o


def ellipsoid(name, center, radii, material, parent, seg=12, ring=8):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=ring, radius=1, location=center)
    o = bpy.context.active_object
    o.name = name
    o.scale = radii
    o.data.materials.append(material)
    o.parent = parent
    for p in o.data.polygons:
        p.use_smooth = True
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
    bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=0.01 * s, depth=0.045 * s,
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
#  flap Hz, phase, heading tilt toward/away from camera deg, span m,
#  bank deg: far wing raised so the drone sees the bird's back)
BIRDS = [
    ("hero", 7.0, -520, -600, 10.0, 3.0, 0.0, 50, 0.95, 12),
    ("b2", 11.0, -950, -470, 9.5, 3.3, 1.7, 44, 0.92, 10),
    ("b3", 16.0, -1150, -230, 9.8, 2.8, 3.1, 40, 0.98, 14),
    ("b4", 22.0, -1260, -60, 10.5, 3.2, 0.9, 36, 0.92, 8),
]
if PREVIEW:
    sc.render.resolution_percentage = 50

for tag, depth, sx, sy, speed, hz, ph, tilt, span, bank in BIRDS:
    root, wings = make_gull(tag, span)
    p_cam = Vector((sx / f_px * depth, sy / f_px * depth, -depth))
    start = M1 @ p_cam
    a = math.radians(tilt)
    vel = (cam_right * math.cos(a) + cam_fwd_h * math.sin(a)) * speed
    heading = math.atan2(vel.y, vel.x) - math.pi / 2  # local +Y faces travel
    for f in range(1, N + 1):
        t = (f - 1) / FPS
        w = 2 * math.pi * hz * t + ph
        bob = -0.04 * span * math.sin(w)  # body dips on the downstroke
        root.location = start + vel * t + Vector((0, 0, bob))
        root.rotation_euler = (math.radians(-4) + 0.04 * math.cos(w), math.radians(bank) + 0.03 * math.sin(w * 0.5), heading)
        root.keyframe_insert("location", frame=f)
        root.keyframe_insert("rotation_euler", frame=f)
        amp = 1.0 if tag != "b3" else max(0.15, min(1.0, 1 - (t - 0.7) * 3))  # b3 settles into a glide
        for side, inner, outer in wings:
            up = math.sin(w) * amp
            inner.rotation_euler = (0, -side * math.radians(10 + 32 * up), 0)
            outer.rotation_euler = (0, -side * math.radians(-6 + 22 * math.sin(w - 0.7) * amp), 0)
            inner.keyframe_insert("rotation_euler", frame=f)
            outer.keyframe_insert("rotation_euler", frame=f)

sc.render.image_settings.file_format = 'PNG'
sc.render.image_settings.color_mode = 'RGBA'
sc.render.filepath = os.path.join(JOB, "render", "b_")
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(JOB, "birds.blend"))
if "--norender" not in sys.argv:
    bpy.ops.render.render(animation=True)
print("DONE")
