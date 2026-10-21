"""Build + render a relit plate in Blender (Cycles): the plate as a 3D mesh, lit by a dusk HDRI and real lights.

  Blender -b --factory-startup --python blender/build_relight.py -- <scene_####.json> --hdri <path>
          [--yaw 0] [--strength 1] [--exposure 0] [--samples 96] [--out <png>] [--save <blend>]

scene_####.json comes from lib/relight.py prep(): camera matrix, plate + mask PNGs, vertex grid, lamp points.
Materials: plate texture as base colour (an overcast plate is close to albedo: soft, shadowless light);
water (mask R) is a glossy dielectric so Cycles reflects the actual sky; windows (mask G) emit warm
interior light that also lights the balconies and ground around them; pools (mask B) glow cyan.
The camera sees the HDRI as its sky, so sky and ground share one light: no separate sky comp needed.
"""
import json, math, sys
import bpy
import numpy as np

argv = sys.argv[sys.argv.index("--") + 1:]
scene_path = argv[0]


def arg(name, default, cast=str):
    return cast(argv[argv.index(name) + 1]) if name in argv else default


HDRI = arg("--hdri", "")
YAW = arg("--yaw", 0.0, float)
STRENGTH = arg("--strength", 1.0, float)
EXPOSURE = arg("--exposure", 0.0, float)
SAMPLES = arg("--samples", 96, int)
OUT = arg("--out", "")
SAVE = arg("--save", "")
WIN_W = arg("--windows", 40.0, float)
LAMP_W = arg("--lamp", 400.0, float)
PCT = arg("--pct", 100, int)
SOFT = arg("--soft-normals", 0.6, float)

S = json.load(open(scene_path))
geo = np.load(S["geo"])
V, keep = geo["V"], geo["keep"]
gh, gw = keep.shape
W, H = S["width"], S["height"]

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene

# ---- mesh: one vertex per grid cell, quads where all four corners are kept
idx = -np.ones((gh, gw), np.int64)
idx[keep] = np.arange(int(keep.sum()))
verts = V[keep].reshape(-1, 3)
q = np.stack([idx[:-1, :-1], idx[:-1, 1:], idx[1:, 1:], idx[1:, :-1]], -1).reshape(-1, 4)
q = q[(q >= 0).all(1)]
q = q[:, ::-1]  # winding so normals face the camera (up)
ys, xs = np.nonzero(keep)
step = int(geo["step"])
uv_v = np.stack([(xs * step + step / 2) / W, 1 - (ys * step + step / 2) / H], -1)
me = bpy.data.meshes.new("plate")
me.vertices.add(len(verts))
me.vertices.foreach_set("co", verts.astype(np.float32).ravel())
me.loops.add(q.size)
me.loops.foreach_set("vertex_index", q.ravel().astype(np.int32))
me.polygons.add(len(q))
me.polygons.foreach_set("loop_start", (np.arange(len(q)) * 4).astype(np.int32))
me.polygons.foreach_set("loop_total", np.full(len(q), 4, np.int32))
me.update(calc_edges=True)
uvl = me.uv_layers.new(name="UV")
uvl.data.foreach_set("uv", uv_v[q.ravel()].astype(np.float32).ravel())
me.polygons.foreach_set("use_smooth", np.ones(len(q), bool))
ob = bpy.data.objects.new("plate", me)
sc.collection.objects.link(ob)

# ---- material
mat = bpy.data.materials.new("plate")
mat.use_nodes = True
nt = mat.node_tree
for n in list(nt.nodes):
    nt.nodes.remove(n)
N = lambda t: nt.nodes.new(t)
out = N("ShaderNodeOutputMaterial")
tex = N("ShaderNodeTexImage"); tex.image = bpy.data.images.load(S["plate"]); tex.interpolation = "Cubic"
msk = N("ShaderNodeTexImage"); msk.image = bpy.data.images.load(S["mask"]); msk.image.colorspace_settings.name = "Non-Color"
sep = N("ShaderNodeSeparateColor")
nt.links.new(msk.outputs["Color"], sep.inputs["Color"])
ground = N("ShaderNodeBsdfPrincipled")
nt.links.new(tex.outputs["Color"], ground.inputs["Base Color"])
ground.inputs["Roughness"].default_value = 0.85
# depth-mesh "walls" between trees and ground are not real surfaces: bend shading normals toward up so they
# don't catch the sky as bright/dark fringes (the geometry, shadows and occlusion stay real)
geon = N("ShaderNodeNewGeometry")
upv = N("ShaderNodeCombineXYZ"); upv.inputs["Z"].default_value = 1.0
nmix = N("ShaderNodeMix"); nmix.data_type = "VECTOR"; nmix.inputs["Factor"].default_value = SOFT
nt.links.new(geon.outputs["Normal"], nmix.inputs[4]); nt.links.new(upv.outputs[0], nmix.inputs[5])
nnorm = N("ShaderNodeVectorMath"); nnorm.operation = "NORMALIZE"
nt.links.new(nmix.outputs[1], nnorm.inputs[0]); nt.links.new(nnorm.outputs[0], ground.inputs["Normal"])
water = N("ShaderNodeBsdfPrincipled")
dark = N("ShaderNodeMix"); dark.data_type = "RGBA"; dark.blend_type = "MULTIPLY"
dark.inputs["Factor"].default_value = 1.0
dark.inputs[7].default_value = (0.35, 0.4, 0.42, 1)
nt.links.new(tex.outputs["Color"], dark.inputs[6])
nt.links.new(dark.outputs[2], water.inputs["Base Color"])
water.inputs["Roughness"].default_value = 0.06
water.inputs["IOR"].default_value = 1.33
bump = N("ShaderNodeBump"); bump.inputs["Strength"].default_value = 0.08
noise = N("ShaderNodeTexNoise"); noise.inputs["Scale"].default_value = 0.6; noise.inputs["Detail"].default_value = 6
nt.links.new(noise.outputs["Fac"], bump.inputs["Height"])
nt.links.new(bump.outputs["Normal"], water.inputs["Normal"])
mix_w = N("ShaderNodeMixShader")
nt.links.new(sep.outputs["Red"], mix_w.inputs["Fac"])
nt.links.new(ground.outputs["BSDF"], mix_w.inputs[1])
nt.links.new(water.outputs["BSDF"], mix_w.inputs[2])
# windows: warm interior light, 2700 K
bb = N("ShaderNodeBlackbody"); bb.inputs["Temperature"].default_value = 2700
em = N("ShaderNodeEmission"); nt.links.new(bb.outputs["Color"], em.inputs["Color"])
mulw = N("ShaderNodeMath"); mulw.operation = "MULTIPLY"; mulw.inputs[1].default_value = WIN_W
nt.links.new(sep.outputs["Green"], mulw.inputs[0]); nt.links.new(mulw.outputs[0], em.inputs["Strength"])
addw = N("ShaderNodeAddShader")
nt.links.new(mix_w.outputs[0], addw.inputs[0]); nt.links.new(em.outputs[0], addw.inputs[1])
# pools: cyan LED
emp = N("ShaderNodeEmission"); emp.inputs["Color"].default_value = (0.1, 0.75, 1.0, 1)
mulp = N("ShaderNodeMath"); mulp.operation = "MULTIPLY"; mulp.inputs[1].default_value = 6.0
nt.links.new(sep.outputs["Blue"], mulp.inputs[0]); nt.links.new(mulp.outputs[0], emp.inputs["Strength"])
addp = N("ShaderNodeAddShader")
nt.links.new(addw.outputs[0], addp.inputs[0]); nt.links.new(emp.outputs[0], addp.inputs[1])
nt.links.new(addp.outputs[0], out.inputs["Surface"])
ob.data.materials.append(mat)

# ---- streetlights: warm point lights 6 m above the marked ground points
for i, p in enumerate(S["lamps"]):
    ld = bpy.data.lights.new(f"lamp{i}", "POINT")
    ld.energy = LAMP_W
    ld.shadow_soft_size = 0.2
    ld.use_custom_distance = False
    ld.color = (1.0, 0.72, 0.42)
    lo = bpy.data.objects.new(f"lamp{i}", ld)
    lo.location = (p[0], p[1], 6.0)
    sc.collection.objects.link(lo)

# ---- world: the dusk HDRI, rotated so its sunset sits where we want it
world = bpy.data.worlds.new("dusk"); sc.world = world; world.use_nodes = True
wn = world.node_tree
for n in list(wn.nodes):
    wn.nodes.remove(n)
wo = wn.nodes.new("ShaderNodeOutputWorld")
bg = wn.nodes.new("ShaderNodeBackground"); bg.inputs["Strength"].default_value = STRENGTH
env = wn.nodes.new("ShaderNodeTexEnvironment"); env.image = bpy.data.images.load(HDRI)
tc = wn.nodes.new("ShaderNodeTexCoord"); mp = wn.nodes.new("ShaderNodeMapping")
mp.inputs["Rotation"].default_value = (0, 0, -YAW)
wn.links.new(tc.outputs["Generated"], mp.inputs["Vector"]); wn.links.new(mp.outputs["Vector"], env.inputs["Vector"])
wn.links.new(env.outputs["Color"], bg.inputs["Color"]); wn.links.new(bg.outputs["Background"], wo.inputs["Surface"])

# ---- camera: the solved frame
cd = bpy.data.cameras.new("cam"); cd.lens = S["lens_mm"]; cd.sensor_width = 36.0; cd.sensor_fit = "HORIZONTAL"
cd.clip_start = 1.0; cd.clip_end = 1e6
co = bpy.data.objects.new("cam", cd); sc.collection.objects.link(co); sc.camera = co
from mathutils import Matrix
co.matrix_world = Matrix(S["camera"])

# ---- render
sc.render.engine = "CYCLES"
try:
    prefs = bpy.context.preferences.addons["cycles"].preferences
    prefs.compute_device_type = "METAL"; prefs.get_devices()
    for d in prefs.devices:
        d.use = True
    sc.cycles.device = "GPU"
except Exception as e:
    print("GPU setup failed:", e)
sc.cycles.samples = SAMPLES
sc.cycles.use_denoising = True
sc.cycles.max_bounces = 6
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = W, H, PCT
sc.view_settings.exposure = EXPOSURE
sc.render.image_settings.file_format = "PNG"
if SAVE:
    bpy.ops.wm.save_as_mainfile(filepath=SAVE)
if OUT:
    sc.render.filepath = OUT
    bpy.ops.render.render(write_still=True)
print("RELIGHT_OK", len(verts), "verts", len(q), "quads")
