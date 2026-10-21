"""Shared helpers for the Vista 1:1 rebuilds (run inside Blender, headless).

Conventions: metres; x right, y away from the camera, z up. Each room script builds its geometry with these
helpers, matches the camera from the render's vanishing point, and renders to renders/<room>_<tag>.png.
"""
import math
import os
import sys

import bpy
from mathutils import Vector

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEX = os.path.join(ROOT, "tex")
SKIES = os.path.join(ROOT, "..", "sky-library", "hdr_2k")


def args():
    a = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    out = {}
    for i, t in enumerate(a):
        if t.startswith("--"):
            out[t[2:]] = a[i + 1] if i + 1 < len(a) and not a[i + 1].startswith("--") else True
    return out


def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    return bpy.context.scene


def link(ob):
    bpy.context.scene.collection.objects.link(ob)
    return ob


def box(name, x0, x1, y0, y1, z0, z1, mat=None, bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2))
    ob = bpy.context.active_object
    ob.name = name
    ob.scale = (x1 - x0, y1 - y0, z1 - z0)
    bpy.ops.object.transform_apply(scale=True)
    if bevel:
        m = ob.modifiers.new("bev", "BEVEL"); m.width = bevel; m.segments = 3; m.limit_method = "ANGLE"
    if mat:
        ob.data.materials.append(mat)
    return ob


def cyl(name, x, y, z0, z1, r, mat=None, verts=96, axis="Z", bevel=0.0):
    h = z1 - z0
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=h, location=(x, y, (z0 + z1) / 2))
    ob = bpy.context.active_object
    ob.name = name
    for p in ob.data.polygons:
        p.use_smooth = True
    if bevel:
        m = ob.modifiers.new("bev", "BEVEL"); m.width = bevel; m.segments = 3; m.limit_method = "ANGLE"
    if mat:
        ob.data.materials.append(mat)
    return ob


def cut(target, cutter, apply=True):
    m = target.modifiers.new("cut", "BOOLEAN")
    m.operation = "DIFFERENCE"; m.solver = "EXACT"; m.object = cutter
    if apply:
        bpy.context.view_layer.objects.active = target
        bpy.ops.object.modifier_apply(modifier=m.name)
        bpy.data.objects.remove(cutter, do_unlink=True)
    return target


def nodes(mat):
    mat.use_nodes = True
    nt = mat.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    nt.links.new(bsdf.outputs[0], out.inputs["Surface"])
    return nt, bsdf, out


def solid(name, rgb, rough=0.5, metal=0.0, coat=0.0):
    m = bpy.data.materials.new(name)
    nt, b, _ = nodes(m)
    b.inputs["Base Color"].default_value = (*rgb, 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if coat:
        b.inputs["Coat Weight"].default_value = coat
    return m


def textured(name, key, tint=(1, 1, 1), scale=1.0, rough_mul=1.0, bump=0.15):
    """Poly Haven texture set tex/<key>_{diff,rough,nor}.jpg, box-projected in object space at `scale` m per tile."""
    m = bpy.data.materials.new(name)
    nt, b, _ = nodes(m)
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping"); mp.inputs["Scale"].default_value = (1 / scale,) * 3
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])

    def img(kind, colour):
        t = nt.nodes.new("ShaderNodeTexImage")
        t.image = bpy.data.images.load(os.path.join(TEX, f"{key}_{kind}.jpg"))
        if not colour:
            t.image.colorspace_settings.name = "Non-Color"
        t.projection = "BOX"; t.projection_blend = 0.2
        nt.links.new(mp.outputs[0], t.inputs["Vector"])
        return t
    d = img("diff", True)
    mul = nt.nodes.new("ShaderNodeMix"); mul.data_type = "RGBA"; mul.blend_type = "MULTIPLY"
    mul.inputs["Factor"].default_value = 1.0
    nt.links.new(d.outputs["Color"], mul.inputs[6]); mul.inputs[7].default_value = (*tint, 1)
    nt.links.new(mul.outputs[2], b.inputs["Base Color"])
    r = img("rough", False)
    rm = nt.nodes.new("ShaderNodeMath"); rm.operation = "MULTIPLY"; rm.inputs[1].default_value = rough_mul
    nt.links.new(r.outputs["Color"], rm.inputs[0]); nt.links.new(rm.outputs[0], b.inputs["Roughness"])
    n = img("nor", False)
    nm = nt.nodes.new("ShaderNodeNormalMap"); nm.inputs["Strength"].default_value = bump
    nt.links.new(n.outputs["Color"], nm.inputs["Color"]); nt.links.new(nm.outputs[0], b.inputs["Normal"])
    return m


def camera(x, y, z, f_px, w, h, vp, yaw=0.0, pitch=0.0):
    """Pinhole camera matched to a render: f_px focal in pixels at width w, vp = principal point (px) -> lens shift."""
    sc = bpy.context.scene
    cd = bpy.data.cameras.new("cam"); cd.sensor_fit = "HORIZONTAL"; cd.sensor_width = 36.0
    cd.lens = f_px / w * 36.0
    cd.shift_x = (w / 2 - vp[0]) / w  # shifting the frame right moves the axis point left
    cd.shift_y = (vp[1] - h / 2) / w
    cd.clip_start = 0.05; cd.clip_end = 200
    co = bpy.data.objects.new("cam", cd); link(co)
    co.location = (x, y, z)
    co.rotation_euler = (math.radians(90 + pitch), 0, math.radians(-yaw))
    sc.camera = co
    sc.render.resolution_x, sc.render.resolution_y = w, h
    return co


def sun(direction, strength=4.0, angle=0.6, kelvin=5200, name="sun"):
    """direction = the way the light TRAVELS (world vector)."""
    ld = bpy.data.lights.new(name, "SUN"); ld.energy = strength; ld.angle = math.radians(angle)
    ld.color = kelvin_rgb(kelvin)
    lo = bpy.data.objects.new(name, ld); link(lo)
    lo.rotation_euler = Vector(direction).normalized().to_track_quat("-Z", "Y").to_euler()
    return lo


def kelvin_rgb(k):
    t = k / 100
    r = 255 if t <= 66 else 329.7 * (t - 60) ** -0.1332
    g = 99.47 * math.log(t) - 161.12 if t <= 66 else 288.1 * (t - 60) ** -0.0755
    b = 255 if t >= 66 else (0 if t <= 19 else 138.5 * math.log(t - 10) - 305.04)
    return tuple(max(0, min(255, c)) / 255 for c in (r, g, b))


def world_hdri(path, strength=1.0, yaw_deg=0.0):
    sc = bpy.context.scene
    w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True
    nt = w.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    o = nt.nodes.new("ShaderNodeOutputWorld"); bg = nt.nodes.new("ShaderNodeBackground")
    env = nt.nodes.new("ShaderNodeTexEnvironment"); env.image = bpy.data.images.load(path)
    tc = nt.nodes.new("ShaderNodeTexCoord"); mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Rotation"].default_value = (0, 0, math.radians(yaw_deg))
    nt.links.new(tc.outputs["Generated"], mp.inputs["Vector"]); nt.links.new(mp.outputs[0], env.inputs["Vector"])
    nt.links.new(env.outputs[0], bg.inputs["Color"]); bg.inputs["Strength"].default_value = strength
    nt.links.new(bg.outputs[0], o.inputs["Surface"])


def backplate(image_path, cam, depth, f_px, w, h, vp, strength=1.0):
    """Camera-only emissive card that reproduces the render exactly where it is seen (window views)."""
    cx, cy, cz = cam.location
    D = depth - cy
    pw, ph = w * D / f_px, h * D / f_px
    ox = (w / 2 - vp[0]) * D / f_px
    oz = (vp[1] - h / 2) * D / f_px
    bpy.ops.mesh.primitive_plane_add(size=1, location=(cx + ox, depth, cz + oz), rotation=(math.radians(90), 0, 0))
    ob = bpy.context.active_object; ob.name = "backplate"; ob.scale = (pw, ph, 1)
    m = bpy.data.materials.new("backplate"); m.use_nodes = True; nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new("ShaderNodeOutputMaterial"); em = nt.nodes.new("ShaderNodeEmission")
    t = nt.nodes.new("ShaderNodeTexImage"); t.image = bpy.data.images.load(image_path); t.extension = "CLIP"
    nt.links.new(t.outputs[0], em.inputs[0]); em.inputs["Strength"].default_value = strength
    nt.links.new(em.outputs[0], out.inputs["Surface"])
    ob.data.materials.append(m)
    ob.visible_shadow = False; ob.visible_diffuse = False; ob.visible_glossy = True
    ob.visible_transmission = True; ob.visible_volume_scatter = False
    return ob


def render_setup(samples=128, pct=50, exposure=0.0, look="AgX - Medium High Contrast"):
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    try:
        prefs = bpy.context.preferences.addons["cycles"].preferences
        prefs.compute_device_type = "METAL"; prefs.get_devices()
        for d in prefs.devices:
            d.use = True
        sc.cycles.device = "GPU"
    except Exception as e:
        print("GPU setup failed:", e)
    sc.cycles.samples = samples
    sc.cycles.use_denoising = True
    sc.cycles.max_bounces = 8
    sc.cycles.light_sampling_threshold = 0.01
    sc.render.resolution_percentage = pct
    sc.view_settings.view_transform = "AgX"
    try:
        sc.view_settings.look = look
    except TypeError:
        pass
    sc.view_settings.exposure = exposure
    sc.render.image_settings.file_format = "PNG"


def finish(out_png, save_blend=None):
    sc = bpy.context.scene
    if save_blend:
        bpy.ops.wm.save_as_mainfile(filepath=save_blend)
    sc.render.filepath = out_png
    bpy.ops.render.render(write_still=True)
    print("RENDER_OK", out_png)
