"""Vista #5 powder room, 1:1 rebuild of inputs/5.jpg.

  blender -b -P scripts/room_05_powder.py -- [--pct 50] [--samples 128] [--tag v1] [--sky <hdr>] [--plate]

Camera solve (one-point perspective, measured on the 2000x1368 render):
  vanishing point (1033, 651); back wall 795 px wide; counter top back edge y962 and front edge y1008 spread from
  795 to 913 px, which with a 0.5 m counter puts the back wall 3.88 m away; f = 1607 px (28.9 mm on 36 mm);
  the floor line (y1290) puts the camera 1.54 m up. A wall-to-wall vanity makes the room 1.92 m wide.
Sun: enters through the back-left window and lands on the left wall 0.2-1.9 m forward of it (measured off the
  light patch), travelling forward-left and down.
"""
import math
import os
import sys

import bpy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C

A = C.args()
W, H, F, VP = 2000, 1368, 1607.0, (1033, 651)
CAM = (0.0, -3.88, 1.54)
HALF = 0.96          # half room width
CT, CB = 0.79, 0.63  # counter top / bottom
NX0, NX1, ND = -0.077, 0.765, 0.15  # niche outer x, depth
NCX, NR = (NX0 + NX1) / 2, (NX1 - NX0) / 2
NSPRING = 2.585 - NR
CEIL = 3.4

sc = C.reset()


# ---------------- materials
def lin(*srgb):
    return tuple(c ** 2.2 for c in srgb)


plaster = C.solid("paint", lin(0.90, 0.885, 0.86), rough=0.85)
_nt = plaster.node_tree; _b = next(n for n in _nt.nodes if n.type == "BSDF_PRINCIPLED")
_tc = _nt.nodes.new("ShaderNodeTexCoord"); _nz = _nt.nodes.new("ShaderNodeTexNoise"); _nz.inputs["Scale"].default_value = 120
_nt.links.new(_tc.outputs["Object"], _nz.inputs["Vector"])
_bm = _nt.nodes.new("ShaderNodeBump"); _bm.inputs["Strength"].default_value = 0.02
_nt.links.new(_nz.outputs["Fac"], _bm.inputs["Height"]); _nt.links.new(_bm.outputs[0], _b.inputs["Normal"])


def travertine(name, scale=1.0):
    m = bpy.data.materials.new(name)
    nt, b, _ = C.nodes(m)
    tc = nt.nodes.new("ShaderNodeTexCoord")
    wv = nt.nodes.new("ShaderNodeTexWave"); wv.wave_type = "BANDS"; wv.bands_direction = "Z"
    wv.inputs["Scale"].default_value = 2.5 * scale; wv.inputs["Distortion"].default_value = 5.0
    wv.inputs["Detail"].default_value = 6.0; wv.inputs["Detail Scale"].default_value = 1.5
    nt.links.new(tc.outputs["Object"], wv.inputs["Vector"])
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 60; nz.inputs["Detail"].default_value = 8
    nt.links.new(tc.outputs["Object"], nz.inputs["Vector"])
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].color = (*lin(0.82, 0.79, 0.75), 1)
    ramp.color_ramp.elements[1].color = (*lin(0.88, 0.86, 0.82), 1)
    ramp.color_ramp.elements[0].position = 0.25; ramp.color_ramp.elements[1].position = 0.75
    mix = nt.nodes.new("ShaderNodeMath"); mix.operation = "MULTIPLY_ADD"
    nt.links.new(wv.outputs["Fac"], mix.inputs[0]); mix.inputs[1].default_value = 0.35
    nt.links.new(nz.outputs["Fac"], mix.inputs[2])
    sub = nt.nodes.new("ShaderNodeMath"); sub.operation = "SUBTRACT"; sub.inputs[1].default_value = 0.3
    nt.links.new(mix.outputs[0], sub.inputs[0]); nt.links.new(sub.outputs[0], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.55
    bm = nt.nodes.new("ShaderNodeBump"); bm.inputs["Strength"].default_value = 0.05
    nt.links.new(nz.outputs["Fac"], bm.inputs["Height"]); nt.links.new(bm.outputs[0], b.inputs["Normal"])
    return m


trav = travertine("travertine")


def finger_tiles():
    """Glazed terracotta finger tiles, vertical, stack offset by half (0.07 x 0.42 m), speckled, light grout."""
    m = bpy.data.materials.new("tiles")
    nt, b, _ = C.nodes(m)
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(tc.outputs["Object"], sep.inputs[0])
    comb = nt.nodes.new("ShaderNodeCombineXYZ")
    nt.links.new(sep.outputs["Z"], comb.inputs["X"]); nt.links.new(sep.outputs["X"], comb.inputs["Y"])
    br = nt.nodes.new("ShaderNodeTexBrick")
    br.inputs["Scale"].default_value = 1.0
    br.inputs["Brick Width"].default_value = 0.40; br.inputs["Row Height"].default_value = 0.058
    br.inputs["Mortar Size"].default_value = 0.0025; br.inputs["Mortar Smooth"].default_value = 0.3
    br.offset = 0.5; br.squash = 1.0
    br.inputs["Color1"].default_value = (*lin(0.52, 0.42, 0.36), 1)
    br.inputs["Color2"].default_value = (*lin(0.62, 0.51, 0.44), 1)
    br.inputs["Mortar"].default_value = (*lin(0.82, 0.78, 0.72), 1)
    br.inputs["Bias"].default_value = 0.0
    nt.links.new(comb.outputs[0], br.inputs["Vector"])
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 400; nz.inputs["Detail"].default_value = 2
    nt.links.new(tc.outputs["Object"], nz.inputs["Vector"])
    spk = nt.nodes.new("ShaderNodeMapRange")
    spk.inputs["From Min"].default_value = 0.62; spk.inputs["From Max"].default_value = 0.68
    spk.inputs["To Min"].default_value = 1.0; spk.inputs["To Max"].default_value = 0.45
    nt.links.new(nz.outputs["Fac"], spk.inputs["Value"])
    mul = nt.nodes.new("ShaderNodeMix"); mul.data_type = "RGBA"; mul.blend_type = "MULTIPLY"
    nt.links.new(spk.outputs[0], mul.inputs["Factor"])
    nt.links.new(br.outputs["Color"], mul.inputs[6]); mul.inputs[7].default_value = (*lin(0.85, 0.75, 0.70), 1)
    # factor drives how dark the speckles are; invert so speckle -> stronger multiply
    inv = nt.nodes.new("ShaderNodeMath"); inv.operation = "SUBTRACT"; inv.inputs[0].default_value = 1.0
    nt.links.new(spk.outputs[0], inv.inputs[1]); nt.links.new(inv.outputs[0], mul.inputs["Factor"])
    nt.links.new(mul.outputs[2], b.inputs["Base Color"])
    rr = nt.nodes.new("ShaderNodeMapRange"); rr.inputs["To Min"].default_value = 0.28; rr.inputs["To Max"].default_value = 0.8
    nt.links.new(br.outputs["Fac"], rr.inputs["Value"]); nt.links.new(rr.outputs[0], b.inputs["Roughness"])
    bm = nt.nodes.new("ShaderNodeBump"); bm.inputs["Strength"].default_value = 0.4; bm.invert = True
    nt.links.new(br.outputs["Fac"], bm.inputs["Height"]); nt.links.new(bm.outputs[0], b.inputs["Normal"])
    return m


tiles = finger_tiles()


def crazy_pave():
    m = bpy.data.materials.new("crazy_pave")
    nt, b, _ = C.nodes(m)
    tc = nt.nodes.new("ShaderNodeTexCoord")
    vo = nt.nodes.new("ShaderNodeTexVoronoi"); vo.inputs["Scale"].default_value = 4.0
    vo.inputs["Randomness"].default_value = 1.0
    nt.links.new(tc.outputs["Object"], vo.inputs["Vector"])
    ve = nt.nodes.new("ShaderNodeTexVoronoi"); ve.feature = "DISTANCE_TO_EDGE"; ve.inputs["Scale"].default_value = 4.0
    nt.links.new(tc.outputs["Object"], ve.inputs["Vector"])
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].color = (*lin(0.70, 0.62, 0.50), 1)
    ramp.color_ramp.elements[1].color = (*lin(0.84, 0.77, 0.64), 1)
    sepc = nt.nodes.new("ShaderNodeSeparateColor"); nt.links.new(vo.outputs["Color"], sepc.inputs[0])
    nt.links.new(sepc.outputs[0], ramp.inputs["Fac"])
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 25; nz.inputs["Detail"].default_value = 10
    nt.links.new(tc.outputs["Object"], nz.inputs["Vector"])
    tex = nt.nodes.new("ShaderNodeMix"); tex.data_type = "RGBA"; tex.blend_type = "OVERLAY"
    tex.inputs["Factor"].default_value = 0.35
    nt.links.new(ramp.outputs["Color"], tex.inputs[6]); nt.links.new(nz.outputs["Color"], tex.inputs[7])
    grout = nt.nodes.new("ShaderNodeMapRange")
    grout.inputs["From Min"].default_value = 0.004; grout.inputs["From Max"].default_value = 0.010
    nt.links.new(ve.outputs["Distance"], grout.inputs["Value"])
    mx = nt.nodes.new("ShaderNodeMix"); mx.data_type = "RGBA"
    nt.links.new(grout.outputs[0], mx.inputs["Factor"])
    mx.inputs[6].default_value = (*lin(0.85, 0.80, 0.70), 1); nt.links.new(tex.outputs[2], mx.inputs[7])
    nt.links.new(mx.outputs[2], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.6
    bm = nt.nodes.new("ShaderNodeBump"); bm.inputs["Strength"].default_value = 0.3
    nt.links.new(grout.outputs[0], bm.inputs["Height"]); nt.links.new(bm.outputs[0], b.inputs["Normal"])
    return m


pave = crazy_pave()
brass = C.solid("brass", lin(0.78, 0.60, 0.36), rough=0.32, metal=1.0)
mirror = C.solid("mirror", (0.9, 0.9, 0.9), rough=0.02, metal=1.0)
white_frame = C.solid("frame", lin(0.93, 0.92, 0.90), rough=0.35)
glass = bpy.data.materials.new("glass"); nt, b, _ = C.nodes(glass)
b.inputs["Transmission Weight"].default_value = 1.0; b.inputs["Roughness"].default_value = 0.0; b.inputs["IOR"].default_value = 1.0
amber = bpy.data.materials.new("amber"); nt, b, _ = C.nodes(amber)
b.inputs["Base Color"].default_value = (*lin(0.35, 0.16, 0.06), 1); b.inputs["Roughness"].default_value = 0.08
b.inputs["Coat Weight"].default_value = 1.0
label = bpy.data.materials.new("label"); nt, b, _ = C.nodes(label)
tc = nt.nodes.new("ShaderNodeTexCoord"); wv = nt.nodes.new("ShaderNodeTexWave"); wv.bands_direction = "Z"
wv.inputs["Scale"].default_value = 40; wv.inputs["Distortion"].default_value = 0
nt.links.new(tc.outputs["Object"], wv.inputs["Vector"])
lr = nt.nodes.new("ShaderNodeValToRGB"); lr.color_ramp.interpolation = "CONSTANT"
lr.color_ramp.elements[0].color = (0.02, 0.02, 0.02, 1); lr.color_ramp.elements[1].color = (*lin(0.90, 0.88, 0.82), 1)
lr.color_ramp.elements[1].position = 0.35
nt.links.new(wv.outputs["Fac"], lr.inputs["Fac"]); nt.links.new(lr.outputs[0], b.inputs["Base Color"])
b.inputs["Roughness"].default_value = 0.5
black = C.solid("black", (0.02, 0.02, 0.02), rough=0.4)
towel = C.solid("towel", lin(0.92, 0.91, 0.88), rough=0.95)
towel_stripe = C.solid("towel_stripe", lin(0.62, 0.60, 0.57), rough=0.95)

# ---------------- shell
C.box("floor", -HALF - 0.2, HALF + 0.2, -4.8, ND + 0.3, -0.1, 0.0, pave)
C.box("ceiling", -HALF - 0.2, HALF + 0.2, -4.8, ND + 0.3, CEIL, CEIL + 0.1, plaster)
C.box("wall_L", -HALF - 0.2, -HALF, -4.8, 0.3, 0, CEIL, plaster)
C.box("wall_R", HALF, HALF + 0.2, -4.8, 0.3, 0, CEIL, plaster)
C.box("wall_F", -HALF, HALF, -4.8, -4.6, 0, CEIL, plaster)
back = C.box("wall_B", -HALF - 0.2, HALF + 0.2, 0.0, 0.25, 0, CEIL, plaster)

# window opening (through) and arched niche (recessed ND)
WX0, WX1, WZ0, WZ1 = -0.92, -0.29, 0.87, 2.58
C.cut(back, C.box("cut_win", WX0, WX1, -0.1, 0.4, WZ0, WZ1))
C.cut(back, C.box("cut_niche", NX0, NX1, -0.1, ND, 0.0, NSPRING))
arch = C.cyl("cut_arch", 0, 0, -0.1, ND, NR, verts=128)
arch.rotation_euler = (math.radians(90), 0, 0); arch.location = (NCX, (ND - 0.1) / 2, NSPRING)
bpy.context.view_layer.objects.active = arch
bpy.ops.object.transform_apply(rotation=True, location=False)
C.cut(back, arch)
for p in back.data.polygons:
    p.use_smooth = False

# tile lining at the back of the niche
C.box("tiles", NX0, NX1, ND - 0.01, ND, 0.0, 2.585, tiles)
tcut = C.box("tile_top", NX0 - 0.1, NX1 + 0.1, ND - 0.05, ND + 0.05, NSPRING, 3.0)
tarch = C.cyl("tile_arch", 0, 0, ND - 0.06, ND + 0.06, NR + 0.002, verts=128)
tarch.rotation_euler = (math.radians(90), 0, 0); tarch.location = (NCX, ND, NSPRING)
bpy.context.view_layer.objects.active = tarch; bpy.ops.object.transform_apply(rotation=True, location=False)
C.cut(tcut, tarch)
C.cut(bpy.data.objects["tiles"], tcut)

# window: frame (60 mm white) set mid-wall, glass pane
FD = 0.10
fw = 0.06
for nm, a in (("fr_l", (WX0, WX0 + fw, WZ0, WZ1)), ("fr_r", (WX1 - fw, WX1, WZ0, WZ1)),
              ("fr_b", (WX0, WX1, WZ0, WZ0 + fw)), ("fr_t", (WX0, WX1, WZ1 - fw, WZ1))):
    C.box(nm, a[0], a[1], FD, FD + 0.06, a[2], a[3], white_frame)
pane = C.box("pane", WX0 + fw, WX1 - fw, FD + 0.028, FD + 0.032, WZ0 + fw, WZ1 - fw, glass)
pane.visible_shadow = False  # Cycles blocks direct sun through refractive glass

# ---------------- vanity
C.box("counter", -HALF, HALF, -0.5, ND, CB, CT, trav, bevel=0.004)
C.cyl("pedestal", NCX, -0.22, 0.0, CB, 0.21, trav)
basin = C.cyl("basin", NCX, -0.25, CT, CT + 0.16, 0.235, trav, bevel=0.01)
C.cut(basin, C.cyl("basin_in", NCX, -0.25, CT + 0.035, CT + 0.3, 0.205))

# mirror on the tiles
MZ, MR = 1.605, 0.31
rim = C.cyl("mirror_rim", 0, 0, 0, 0.025, MR, brass, verts=128)
rim.rotation_euler = (math.radians(90), 0, 0); rim.location = (NCX, ND - 0.0125 - 0.01, MZ)
glassm = C.cyl("mirror", 0, 0, 0, 0.026, MR - 0.008, mirror, verts=128)
glassm.rotation_euler = (math.radians(90), 0, 0); glassm.location = (NCX, ND - 0.0125 - 0.012, MZ)

# tapware (wall spout + mixer)
TZ = 1.07
sp = C.cyl("spout_arm", 0, 0, 0, 0.15, 0.011, brass, verts=32)
sp.rotation_euler = (math.radians(90), 0, 0); sp.location = (NCX, ND - 0.075, TZ)
C.cyl("spout_tip", NCX, ND - 0.145, TZ - 0.05, TZ, 0.011, brass, verts=32)
C.cyl("spout_tip_cap", NCX, ND - 0.145, TZ - 0.002, TZ + 0.011, 0.011, brass, verts=32)
mx_x = NCX + 0.14
ps = C.cyl("mixer_plate", 0, 0, 0, 0.012, 0.03, brass, verts=48)
ps.rotation_euler = (math.radians(90), 0, 0); ps.location = (mx_x, ND - 0.006, TZ)
bd = C.cyl("mixer_body", 0, 0, 0, 0.05, 0.012, brass, verts=32)
bd.rotation_euler = (math.radians(90), 0, 0); bd.location = (mx_x, ND - 0.035, TZ)
C.cyl("mixer_lever", mx_x, ND - 0.055, TZ, TZ + 0.06, 0.004, brass, verts=16)

# products: jar + two amber pump bottles
C.cyl("jar", -0.16, -0.12, CT, CT + 0.055, 0.032, amber, verts=48)
C.cyl("jar_label", -0.16, -0.12, CT + 0.012, CT + 0.04, 0.0325, label, verts=48)
C.cyl("jar_lid", -0.16, -0.12, CT + 0.055, CT + 0.07, 0.033, black, verts=48)
for nm, x, h in (("bottle_a", -0.07, 0.17), ("bottle_b", 0.025, 0.21)):
    C.cyl(nm, x, -0.1, CT, CT + h, 0.03, amber, verts=48, bevel=0.004)
    C.cyl(nm + "_label", x, -0.1, CT + 0.03, CT + h * 0.75, 0.0305, label, verts=48)
    C.cyl(nm + "_pump", x, -0.1, CT + h, CT + h + 0.05, 0.009, black, verts=24)
    C.box(nm + "_nozzle", x - 0.005, x + 0.005, -0.15, -0.1, CT + h + 0.04, CT + h + 0.055, black)

# towel bar on the right wall + hanging hand towel
BZ, BY = 1.205, -0.54
bar = C.cyl("towel_bar", 0, 0, 0, 0.2, 0.008, brass, verts=24)
bar.rotation_euler = (0, math.radians(90), 0); bar.location = (HALF - 0.1, BY, BZ)
pl = C.cyl("bar_plate", 0, 0, 0, 0.012, 0.025, brass, verts=32)
pl.rotation_euler = (0, math.radians(90), 0); pl.location = (HALF - 0.006, BY, BZ)
C.box("towel", 0.79, 0.93, BY - 0.012, BY + 0.012, 0.94, BZ + 0.01, towel, bevel=0.008)
C.box("towel_stripe", 0.79, 0.93, BY - 0.0125, BY + 0.0125, 0.975, 0.995, towel_stripe)

# doorway behind the camera, lit hallway beyond (the original is evenly bright: light comes from behind us)
ld = bpy.data.lights.new("hall", "AREA"); ld.shape = "RECTANGLE"; ld.size, ld.size_y = 1.8, 3.0
ld.energy = float(A.get("fill", 3000)); ld.color = C.kelvin_rgb(6500)
lo = bpy.data.objects.new("hall", ld); C.link(lo); lo.location = (0, -4.5, 1.6); lo.rotation_euler = (math.radians(90), 0, 0)  # area lights emit along local -Z -> +y, into the room
# the original lights the right wall far more than the back or left: a second opening on the left, behind us
l2 = bpy.data.lights.new("side", "AREA"); l2.shape = "RECTANGLE"; l2.size, l2.size_y = 0.9, 2.2
l2.energy = float(A.get("side", 60)); l2.color = C.kelvin_rgb(6000)
so = bpy.data.objects.new("side", l2); C.link(so); so.location = (-HALF + 0.02, -3.3, 1.2); so.rotation_euler = (0, math.radians(-90), 0)

# ---------------- camera, light, world
cam = C.camera(*CAM, F, W, H, VP)
C.sun((-0.27, -0.96, -0.26), strength=float(A.get("sun", 5.0)), angle=3.0, kelvin=5300)
sky = A.get("sky", os.path.join(C.SKIES, "kloofendal_48d_partly_cloudy_puresky.hdr"))
C.world_hdri(sky, strength=float(A.get("world", 1.0)))
if A.get("plate"):
    C.backplate(os.path.join(C.ROOT, "inputs", "5.jpg"), cam, 2.5, F, W, H, VP, strength=1.0)

for _o in bpy.data.objects:
    if _o.type == 'LIGHT' and _o.data.type == 'AREA':
        _o.visible_glossy = False; _o.visible_camera = False
C.render_setup(samples=int(A.get("samples", 128)), pct=int(A.get("pct", 50)), exposure=float(A.get("exposure", 0.0)))
tag = A.get("tag", "v1")
os.makedirs(os.path.join(C.ROOT, "renders"), exist_ok=True)
C.finish(os.path.join(C.ROOT, "renders", f"05_powder_{tag}.png"),
         save_blend=os.path.join(C.ROOT, "renders", f"05_powder_{tag}.blend") if A.get("save") else None)
