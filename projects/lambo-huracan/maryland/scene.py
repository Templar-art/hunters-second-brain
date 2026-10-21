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
FPS, NF = 25, 175

# Drives IN: off the street (behind and left of camera) across the paver apron, through the gate, up the drive.
# Drive centreline picked on the 2x plate (far to near), converted to ground metres; apron points in metres.
DRIVE_IMG = [(578, 572), (590, 600), (625, 635), (680, 668), (740, 700)]
DRIVE = [((u - CX) / F * (F * CAMH / (v - CY)), F * CAMH / (v - CY)) for u, v in DRIVE_IMG]
PTS = [(-4.6, -1.6), (-3.5, 0.5), (-2.3, 3.3), (-1.3, 6.3), (-0.9, 8.4)] + DRIVE[::-1] + [(-10.6, 52.0)]
WB = 2.62   # Huracán wheelbase; the path is the REAR axle (bicycle model: no sideways slip)

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
# The Sketchfab root carries a quaternion import rotation and x100 scale, so it can't be keyed with a yaw euler
# (that is what made the car slide sideways without turning). Drive a clean world-aligned rig instead: front is -y.
model = bpy.data.objects["Sketchfab_model"]
car = bpy.data.objects.new("car_rig", None); sc.collection.objects.link(car)
car.rotation_mode = "XYZ"
mw0 = model.matrix_world.copy(); model.parent = car; model.matrix_world = mw0
R = 0.34
spins = {}
for side in ("Front L", "Front R", "Rear L", "Rear R"):
    wheel = bpy.data.objects["3DWheel " + side]
    mw = wheel.matrix_world.copy()
    steer = bpy.data.objects.new("steer " + side, None); sc.collection.objects.link(steer)
    spin = bpy.data.objects.new("spin " + side, None); sc.collection.objects.link(spin)
    steer.parent = car; steer.location = mw.translation   # rig is at identity here: local = world
    spin.parent = steer
    bpy.context.view_layer.update()
    wheel.parent = spin; wheel.matrix_world = mw
    spins[side] = (steer, spin)


def catmull(pts, n=400):
    P = [Vector((x, y, 0)) for x, y in pts]
    P = [P[0] * 2 - P[1]] + P + [P[-1] * 2 - P[-2]]
    out = []
    for i in range(1, len(P) - 2):
        for k in range(n):
            t = k / n
            p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
            out.append(0.5 * (2 * p1 + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    out.append(P[-2])
    return out


def resample(path, step):
    cum = [0.0]
    for a, b in zip(path, path[1:]):
        cum.append(cum[-1] + (b - a).length)
    out, s, i = [], 0.0, 1
    while s <= cum[-1]:
        while cum[i] < s:
            i += 1
        t = (s - cum[i - 1]) / max(1e-9, cum[i] - cum[i - 1])
        out.append(path[i - 1].lerp(path[i], t)); s += step
    return out


# hand-picked points wobble; resample every 10 cm and Gaussian-smooth (sigma 1.5 m) so curvature is continuous
STEP = 0.1
raw = resample(catmull(PTS, 200), STEP)
sig = int(1.5 / STEP); ker = [math.exp(-0.5 * (k / sig) ** 2) for k in range(-3 * sig, 3 * sig + 1)]
path = []
for i in range(len(raw)):
    acc, wsum = Vector((0, 0, 0)), 0.0
    for k, wk in enumerate(ker):
        j = min(len(raw) - 1, max(0, i + k - 3 * sig)); acc += raw[j] * wk; wsum += wk
    path.append(acc / wsum)
path = resample(path, STEP)
L = (len(path) - 1) * STEP


def at(s):
    x = max(0.0, min(L - 1e-6, s)) / STEP; i = int(x)
    return path[i].lerp(path[min(i + 1, len(path) - 1)], x - i)


def heading(s):
    d = at(s + 0.3) - at(s - 0.3); return math.atan2(d.y, d.x)


def curvature(s):
    dh = heading(s + 0.5) - heading(s - 0.5); dh = (dh + math.pi) % (2 * math.pi) - math.pi; return dh / 1.0


kmax = max(abs(curvature(k * 0.5)) for k in range(2, int(L / 0.5) - 2))
print("path length", round(L, 1), "m; tightest radius", round(1 / max(kmax, 1e-6), 1), "m")

# speed: rolls in off the street at ~9 km/h, eases up to ~20 km/h along the drive (accel <= 1 m/s^2)
v, s, s_list = 2.5, 2.6, []
for f in range(NF):
    s_list.append(s)
    v = min(5.5, v + 1.0 / FPS); s += v / FPS
    if s > L - 3:
        break
NF = len(s_list)
print("frames", NF, "covered", round(s_list[-1], 1), "m")

prev_yaw, s_front, front_prev = None, 0.0, None
for f, s in enumerate(s_list, start=1):
    rear = at(s); h = heading(s)
    fwd = Vector((math.cos(h), math.sin(h), 0))
    yaw = math.atan2(fwd.x, -fwd.y)          # car front is local -y
    if prev_yaw is not None:
        while yaw - prev_yaw > math.pi: yaw -= 2 * math.pi
        while yaw - prev_yaw < -math.pi: yaw += 2 * math.pi
    prev_yaw = yaw
    front = rear + fwd * WB
    s_front += (front - front_prev).length if front_prev is not None else 0.0
    front_prev = front
    car.location = (rear + fwd * (WB / 2)).to_tuple(); car.rotation_euler = (0, 0, yaw)
    car.keyframe_insert("location", frame=f); car.keyframe_insert("rotation_euler", frame=f)
    steer_a = math.atan(WB * curvature(s))   # Ackermann-free bicycle steer; + = left (CCW from above)
    for side, (st, sp) in spins.items():
        dist = s_front if "Front" in side else s
        sp.rotation_euler = (dist / R, 0, 0); sp.keyframe_insert("rotation_euler", frame=f)
        if "Front" in side:
            st.rotation_euler = (0, 0, steer_a); st.keyframe_insert("rotation_euler", frame=f)

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
