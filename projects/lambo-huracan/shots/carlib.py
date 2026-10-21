"""Shared Huracán rig + drive animation for the tracked shots (same model and fixes as ../maryland/scene.py).

The Sketchfab root carries a quaternion import rotation and x100 scale, so it can't be keyed with a yaw
euler; a clean world-aligned rig drives it (front is local -y). The path is the REAR axle (bicycle model,
no sideways slip), smoothed so curvature is continuous; front wheels steer by atan(wheelbase * curvature).
"""
import math

import bpy
from mathutils import Vector

WB, R = 2.62, 0.34


def rig(sc):
    model = bpy.data.objects["Sketchfab_model"]
    car = bpy.data.objects.new("car_rig", None); sc.collection.objects.link(car); car.rotation_mode = "XYZ"
    mw0 = model.matrix_world.copy(); model.parent = car; model.matrix_world = mw0
    spins = {}
    for side in ("Front L", "Front R", "Rear L", "Rear R"):
        wheel = bpy.data.objects["3DWheel " + side]; mw = wheel.matrix_world.copy()
        steer = bpy.data.objects.new("steer " + side, None); sc.collection.objects.link(steer)
        spin = bpy.data.objects.new("spin " + side, None); sc.collection.objects.link(spin)
        steer.parent = car; steer.location = mw.translation; spin.parent = steer
        bpy.context.view_layer.update()
        wheel.parent = spin; wheel.matrix_world = mw
        spins[side] = (steer, spin)
    return car, spins


def catmull(pts, n=200):
    P = [Vector((x, y, 0)) for x, y in pts]
    P = [P[0] * 2 - P[1]] + P + [P[-1] * 2 - P[-2]]
    out = []
    for i in range(1, len(P) - 2):
        for k in range(n):
            t = k / n; p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
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
        t = (s - cum[i - 1]) / max(1e-9, cum[i] - cum[i - 1]); out.append(path[i - 1].lerp(path[i], t)); s += step
    return out


class Path:
    def __init__(self, pts, sigma=1.5, step=0.1):
        raw = resample(catmull(pts), step); sig = max(1, int(sigma / step))
        ker = [math.exp(-0.5 * (k / sig) ** 2) for k in range(-3 * sig, 3 * sig + 1)]
        sm = []
        for i in range(len(raw)):
            acc, ws = Vector((0, 0, 0)), 0.0
            for k, wk in enumerate(ker):
                j = min(len(raw) - 1, max(0, i + k - 3 * sig)); acc += raw[j] * wk; ws += wk
            sm.append(acc / ws)
        self.p = resample(sm, step); self.step = step; self.L = (len(self.p) - 1) * step

    def at(self, s):
        x = max(0.0, min(self.L - 1e-6, s)) / self.step; i = int(x)
        return self.p[i].lerp(self.p[min(i + 1, len(self.p) - 1)], x - i)

    def heading(self, s):
        d = self.at(s + 0.3) - self.at(s - 0.3); return math.atan2(d.y, d.x)

    def curvature(self, s):
        dh = self.heading(s + 0.5) - self.heading(s - 0.5); return ((dh + math.pi) % (2 * math.pi) - math.pi) / 1.0

    def tightest(self):
        k = max(abs(self.curvature(i * 0.5)) for i in range(2, int(self.L / 0.5) - 2)); return 1 / max(k, 1e-6)


def animate(car, spins, path, s_list):
    prev, s_front, fprev = None, 0.0, None
    for f, s in enumerate(s_list, start=1):
        rear = path.at(s); h = path.heading(s); fwd = Vector((math.cos(h), math.sin(h), 0))
        yaw = math.atan2(fwd.x, -fwd.y)
        if prev is not None:
            while yaw - prev > math.pi: yaw -= 2 * math.pi
            while yaw - prev < -math.pi: yaw += 2 * math.pi
        prev = yaw
        front = rear + fwd * WB; s_front += (front - fprev).length if fprev is not None else 0.0; fprev = front
        car.location = (rear + fwd * (WB / 2)).to_tuple(); car.rotation_euler = (0, 0, yaw)
        car.keyframe_insert("location", frame=f); car.keyframe_insert("rotation_euler", frame=f)
        steer = math.atan(WB * path.curvature(s))
        for side, (st, sp) in spins.items():
            sp.rotation_euler = ((s_front if "Front" in side else s) / R, 0, 0); sp.keyframe_insert("rotation_euler", frame=f)
            if "Front" in side:
                st.rotation_euler = (0, 0, steer); st.keyframe_insert("rotation_euler", frame=f)


def lights(sc, car, beam=900, lamp=25.0):
    for m in bpy.data.materials:
        b = next((n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED"), None) if m.node_tree else None
        if not b:
            continue
        if m.name in ("baseM_Light_Max1", "emis"):
            b.inputs["Emission Color"].default_value = (1, 0.97, 0.92, 1); b.inputs["Emission Strength"].default_value = lamp
        if m.name == "baseM_LightGlassNormal_Red_SetHC_Low1":
            b.inputs["Emission Color"].default_value = (1, 0.02, 0.01, 1); b.inputs["Emission Strength"].default_value = 8
    for i, x in enumerate((-0.62, 0.62)):
        ld = bpy.data.lights.new(f"beam{i}", "SPOT"); ld.energy = beam; ld.spot_size = math.radians(55)
        ld.spot_blend = 0.6; ld.shadow_soft_size = 0.05; ld.color = (1, 0.96, 0.9)
        lo = bpy.data.objects.new(f"beam{i}", ld); sc.collection.objects.link(lo)
        lo.parent = car; lo.location = (x, -2.2, 0.72); lo.rotation_euler = (math.radians(-78), 0, 0)


def world(sc, hdr_path, rot_deg, gain=1.0):
    w = sc.world; nt = w.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    o = nt.nodes.new("ShaderNodeOutputWorld"); bg = nt.nodes.new("ShaderNodeBackground")
    env = nt.nodes.new("ShaderNodeTexEnvironment"); env.image = bpy.data.images.load(hdr_path)
    tc = nt.nodes.new("ShaderNodeTexCoord"); mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Rotation"].default_value = (0, 0, math.radians(rot_deg))
    nt.links.new(tc.outputs["Generated"], mp.inputs["Vector"]); nt.links.new(mp.outputs[0], env.inputs["Vector"])
    nt.links.new(env.outputs[0], bg.inputs[0]); bg.inputs["Strength"].default_value = gain; nt.links.new(bg.outputs[0], o.inputs[0])


def catcher(sc, size=400, center=(0, 0)):
    bpy.ops.mesh.primitive_plane_add(size=size, location=(center[0], center[1], 0)); g = bpy.context.active_object
    g.name = "catcher"; g.is_shadow_catcher = True
    m = bpy.data.materials.new("asphalt"); m.use_nodes = True; b = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    b.inputs["Base Color"].default_value = (0.09, 0.09, 0.1, 1); b.inputs["Roughness"].default_value = 0.55
    g.data.materials.append(m)
    return g


def render_settings(sc, w, h, samples=48, fps=25):
    sc.render.engine = "CYCLES"
    p = bpy.context.preferences.addons["cycles"].preferences; p.compute_device_type = "METAL"; p.get_devices()
    for d in p.devices:
        d.use = True
    sc.cycles.device = "GPU"; sc.cycles.samples = samples; sc.cycles.use_denoising = True
    sc.render.film_transparent = True; sc.render.use_motion_blur = True; sc.render.motion_blur_shutter = 0.5
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = w, h, 100
    sc.render.fps = fps
    sc.view_layers[0].cycles.use_pass_shadow_catcher = True
    sc.view_settings.view_transform = "AgX"; sc.view_settings.look = "AgX - Punchy"
    sc.render.image_settings.media_type = "MULTI_LAYER_IMAGE"
    sc.render.image_settings.file_format = "OPEN_EXR_MULTILAYER"; sc.render.image_settings.color_depth = "16"
