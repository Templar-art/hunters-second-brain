"""Huracán drives down the 18 Maryland driveway: CG car over the listing photo (locked camera).

  blender -b ../huracan_lp580-2.blend -P scene.py -- [--frames 1-200 | --frame 120] [--pct 100] [--samples 64] [--out exr/]

Camera solve (on plate.png, 800x533, letterbox removed; numbers below are in the 2x 1600x1066 frame):
  left wall VP (1383, 529) and sign-wall VP (-1284, 540) are the two walls of the entry, square to each other
  -> horizon y 533 (= image centre: level camera, no shift), f = sqrt(583*2084) = 1102 px -> 24.8 mm on 36 mm.
  Camera height 1.6 m (sign wall then reads 2.4 m tall); house lands ~115 m away and ~17 m wide, gate ~5.3 m.
World: camera at origin looking +y, ground z=0 (shadow catcher). Image point (u, v) on the ground ->
  y = F*H/(v-CY), x = (u-CX)/F*y.
Renders multilayer EXR (Combined RGBA + Shadow Catcher); comp.py puts it over the plate.
"""
import math
import os
import sys

import bpy
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []


def arg(n, d):
    return argv[argv.index(n) + 1] if n in argv else d


W2, H2, F, CX, CY, CAMH = 1600, 1066, 1102.0, 800.0, 533.0, 1.6
FPS, NF = 25, 240

# driveway centreline picked on the 2x plate, then on past the gate and out to the left (street)
PTS_IMG = [(578, 572), (590, 600), (625, 635), (680, 668), (740, 700), (780, 725), (760, 780), (660, 840)]
PTS = [((u - CX) / F * (F * CAMH / (v - CY)), F * CAMH / (v - CY)) for u, v in PTS_IMG]
PTS += [(-3.5, 5.6), (-7.0, 5.2), (-11.0, 5.0)]

sc = bpy.context.scene
for n in ("Camera", "ground"):
    o = bpy.data.objects.get(n)
    if o:
        bpy.data.objects.remove(o, do_unlink=True)

# ---- camera
cd = bpy.data.cameras.new("cam"); cd.sensor_fit = "HORIZONTAL"; cd.sensor_width = 36; cd.lens = F / W2 * 36
cd.clip_start = 0.1; cd.clip_end = 500
cam = bpy.data.objects.new("cam", cd); sc.collection.objects.link(cam); sc.camera = cam
cam.location = (0, 0, CAMH); cam.rotation_euler = (math.radians(90), 0, 0)
sc.render.resolution_x, sc.render.resolution_y = W2, H2
sc.render.resolution_percentage = int(arg("--pct", 100))
sc.render.fps = FPS

# ---- shadow catcher ground
bpy.ops.mesh.primitive_plane_add(size=400, location=(0, 100, 0)); g = bpy.context.active_object; g.name = "catcher"
g.is_shadow_catcher = True
gm = bpy.data.materials.new("asphalt"); gm.use_nodes = True
gb = next(n for n in gm.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
gb.inputs["Base Color"].default_value = (0.09, 0.09, 0.1, 1); gb.inputs["Roughness"].default_value = 0.55
g.data.materials.append(gm)

# ---- world: blue-hour sky from the sky library, warm band toward the right of frame like the photo
w = sc.world; w.use_nodes = True; nt = w.node_tree
for n in list(nt.nodes):
    nt.nodes.remove(n)
o = nt.nodes.new("ShaderNodeOutputWorld"); bg = nt.nodes.new("ShaderNodeBackground")
env = nt.nodes.new("ShaderNodeTexEnvironment")
env.image = bpy.data.images.load(os.path.join(HERE, "..", "..", "sky-library", "hdr_2k", arg("--sky", "qwantani_dusk_2_puresky") + ".hdr"))
tc = nt.nodes.new("ShaderNodeTexCoord"); mp = nt.nodes.new("ShaderNodeMapping")
mp.inputs["Rotation"].default_value = (0, 0, math.radians(float(arg("--skyrot", 120))))
nt.links.new(tc.outputs["Generated"], mp.inputs["Vector"]); nt.links.new(mp.outputs[0], env.inputs["Vector"])
nt.links.new(env.outputs[0], bg.inputs[0]); bg.inputs["Strength"].default_value = float(arg("--sky_gain", 1.0))
nt.links.new(bg.outputs[0], o.inputs[0])

# ---- car rig: root follows the path; wheels spin; front wheels steer
car = bpy.data.objects["Sketchfab_model"]
R = 0.34
spins = {}
for side in ("Front L", "Front R", "Rear L", "Rear R"):
    wheel = bpy.data.objects["3DWheel " + side]
    mw = wheel.matrix_world.copy()
    steer = bpy.data.objects.new("steer " + side, None); sc.collection.objects.link(steer)
    spin = bpy.data.objects.new("spin " + side, None); sc.collection.objects.link(spin)
    steer.parent = wheel.parent; steer.matrix_world = mw.Translation(mw.translation) if False else steer.matrix_world
    steer.matrix_world = car.matrix_world.to_3x3().to_4x4()
    steer.matrix_world.translation = mw.translation
    spin.parent = steer; spin.matrix_world = steer.matrix_world.copy()
    wheel.parent = spin; wheel.matrix_world = mw
    spins[side] = (steer, spin)


def catmull(pts, n=400):
    P = [Vector((x, y, 0)) for x, y in pts]
    P = [P[0] * 2 - P[1]] + P + [P[-1] * 2 - P[-2]]
    out = []
    for i in range(1, len(P) - 2):
        for k in range(n // (len(P) - 3)):
            t = k / (n // (len(P) - 3))
            p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
            out.append(0.5 * (2 * p1 + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    out.append(P[-2])
    return out


path = catmull(PTS, 2000)
cum = [0.0]
for a, b in zip(path, path[1:]):
    cum.append(cum[-1] + (b - a).length)
L = cum[-1]


def at(s):
    s = max(0, min(L - 1e-6, s))
    i = max(1, next(k for k, c in enumerate(cum) if c >= s))
    a, b = path[i - 1], path[i]
    t = (s - cum[i - 1]) / max(1e-9, cum[i] - cum[i - 1])
    return a.lerp(b, t)


# speed: roll down at ~18 km/h, ease to ~9 km/h through the gate and the turn, pull away
def speed(s):
    gate = 0.62 * L
    return 6.0 - 3.0 * math.exp(-((s - gate) / 8.0) ** 2) + (1.5 if s > 0.85 * L else 0)


s_list, s = [], 0.0
for f in range(NF):
    s_list.append(s); s += speed(s) / FPS
print("path length", round(L, 1), "m; covered", round(s, 1), "m in", NF / FPS, "s")

prev_yaw = None
for f, s in enumerate(s_list, start=1):
    p, q = at(s), at(s + 1.5)
    d = q - p
    yaw = math.atan2(d.x, -d.y)  # car front is local -y
    if prev_yaw is not None:
        while yaw - prev_yaw > math.pi: yaw -= 2 * math.pi
        while yaw - prev_yaw < -math.pi: yaw += 2 * math.pi
    prev_yaw = yaw
    car.location = (p.x, p.y, 0); car.rotation_euler = (0, 0, yaw)
    car.keyframe_insert("location", frame=f); car.keyframe_insert("rotation_euler", frame=f)
    # steering from path curvature over the wheelbase (2.62 m), clamped
    q2 = at(s + 4.0) - at(s + 1.5)
    turn = math.atan2(q2.x, -q2.y) - math.atan2(d.x, -d.y)
    turn = (turn + math.pi) % (2 * math.pi) - math.pi
    steer_a = max(-0.5, min(0.5, turn * 1.6))
    for side, (st, sp) in spins.items():
        sp.rotation_euler = (s / R, 0, 0)   # forward roll (front is -y): positive x
        sp.keyframe_insert("rotation_euler", frame=f)
        if "Front" in side:
            st.rotation_euler = (0, 0, steer_a); st.keyframe_insert("rotation_euler", frame=f)
for fc in (car.animation_data.action.fcurves if hasattr(car.animation_data.action, "fcurves") else []):
    for k in fc.keyframe_points:
        k.interpolation = "LINEAR"

# ---- lights on: LED DRLs/headlights white, tail lights red, real beams on the drive
for m in bpy.data.materials:
    if m.name in ("baseM_Light_Max1", "emis"):
        b = next((n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED"), None)
        if b:
            b.inputs["Emission Color"].default_value = (1, 0.97, 0.92, 1); b.inputs["Emission Strength"].default_value = 25
    if m.name == "baseM_LightGlassNormal_Red_SetHC_Low1":
        b = next((n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED"), None)
        if b:
            b.inputs["Emission Color"].default_value = (1, 0.02, 0.01, 1); b.inputs["Emission Strength"].default_value = 8
for i, x in enumerate((-0.62, 0.62)):
    ld = bpy.data.lights.new(f"beam{i}", "SPOT"); ld.energy = float(arg("--beam", 900)); ld.spot_size = math.radians(55)
    ld.spot_blend = 0.6; ld.shadow_soft_size = 0.05; ld.color = (1, 0.96, 0.9)
    lo = bpy.data.objects.new(f"beam{i}", ld); sc.collection.objects.link(lo)
    lo.parent = car; lo.location = (x, -2.2, 0.72); lo.rotation_euler = (math.radians(-78), 0, 0)

# ---- render
sc.render.engine = "CYCLES"
prefs = bpy.context.preferences.addons["cycles"].preferences
prefs.compute_device_type = "METAL"; prefs.get_devices()
for dv in prefs.devices:
    dv.use = True
sc.cycles.device = "GPU"; sc.cycles.samples = int(arg("--samples", 64)); sc.cycles.use_denoising = True
sc.render.film_transparent = True
sc.render.use_motion_blur = True; sc.render.motion_blur_shutter = 0.5
vl = sc.view_layers[0]; vl.cycles.use_pass_shadow_catcher = True
sc.view_settings.view_transform = "AgX"
sc.view_settings.look = "AgX - Punchy"
sc.view_settings.exposure = float(arg("--exposure", 0.0))
sc.render.image_settings.media_type = "MULTI_LAYER_IMAGE"
sc.render.image_settings.file_format = "OPEN_EXR_MULTILAYER"
sc.render.image_settings.color_depth = "16"
sc.frame_start, sc.frame_end = 1, NF
out = os.path.join(HERE, arg("--out", "exr")) + os.sep
os.makedirs(out, exist_ok=True)
sc.render.filepath = out
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HERE, "maryland.blend"))
if "--frame" in argv:
    sc.frame_set(int(arg("--frame", 120)))
    sc.render.filepath = os.path.join(out, "test_%04d" % int(arg("--frame", 120)))
    bpy.ops.render.render(write_still=True)
elif "--frames" in argv:
    a, b = map(int, arg("--frames", "1-200").split("-"))
    sc.frame_start, sc.frame_end = a, b
    bpy.ops.render.render(animation=True)
print("SCENE_OK")
