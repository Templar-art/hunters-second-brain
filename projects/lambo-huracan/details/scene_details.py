"""16:9 detail stills of the Huracán parked at 18 Maryland (CG car, real backdrop from the shoot).

  blender -b ../huracan_lp580-2.blend -P scene_details.py -- [shot ...] [--samples 256] [--res 100]

The backdrop is a frame of 10x's own ground footage (maryland-scan/frames_ground, Sony S-Log3/S-Gamut3.Cine),
decoded to linear Rec.709 and shown on a camera-only emissive card far behind the car, so Cycles' depth of
field blurs it like a real lens would. The car is lit by a matching daylight HDRI; the ground under the car
is CG concrete pavers in the courtyard's grey. Output: details/md_<shot>.png (AgX Punchy, 1920x1080).
"""
import math
import os
import sys

import bpy
import numpy as np
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "shots"))
import carlib  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []


def arg(n, d):
    return argv[argv.index(n) + 1] if n in argv else d


FR = os.path.join(HERE, "..", "..", "maryland-scan", "frames_ground")
# name: camera, aim (car-local metres; front is -y, rear plate y=+2.11), lens mm, f-stop, backdrop frame
SHOTS = {
    "tail_light":   ((1.9, 3.9, 0.95), (0.7, 2.0, 0.84), 70, 2.8, "g4914_023"),
    "rear_plate":   ((0.6, 4.6, 1.05), (0.0, 2.1, 0.75), 50, 2.8, "g4911_025"),
    "front_wheel":  ((-2.5, -3.0, 0.45), (-0.9, -1.3, 0.42), 50, 2.8, "g4914_023"),
    "headlight":    ((-1.6, -4.4, 0.9), (-0.7, -2.05, 0.7), 60, 2.8, "g4910_005"),
    "front_badge":  ((0.5, -4.8, 0.95), (0.0, -2.2, 0.6), 45, 2.8, "g4914_023"),
    "mirror":       ((-2.6, 0.9, 1.15), (-1.0, -0.3, 1.0), 60, 2.8, "g4911_025"),
    "rear_wheel":   ((-2.3, 3.1, 0.45), (-0.9, 1.3, 0.42), 50, 2.8, "g4910_005"),
    "side_intake":  ((-2.7, 2.6, 0.8), (-1.0, 0.7, 0.6), 45, 2.8, "g4914_023"),
}
want = [a for a in argv if a in SHOTS] or list(SHOTS)

SG3C_TO_709 = np.array([[1.6269474, -0.5401385, -0.0868088],
                        [-0.1785155, 1.4179409, -0.2394254],
                        [-0.0444361, -0.1959199, 1.2403560]])


def slog3_decode(rgb):
    c = (64 + rgb * 876) / 1023
    return np.where(c >= 171.2102946929 / 1023, (10 ** ((c * 1023 - 420) / 261.5)) * 0.19 - 0.01,
                    (c * 1023 - 95) * 0.01125 / (171.2102946929 - 95))


def plate(name):
    """Log JPEG -> float image in linear Rec.709 (scene-referred, so it sits under the same AgX view as the car)."""
    key = "bg_" + name
    if key in bpy.data.images:
        return bpy.data.images[key]
    src = bpy.data.images.load(os.path.join(FR, name + ".jpg")); src.colorspace_settings.name = "Non-Color"
    w, h = src.size; px = np.empty(w * h * 4, np.float32); src.pixels.foreach_get(px); px = px.reshape(h, w, 4)
    lin = np.clip(slog3_decode(px[..., :3]) @ SG3C_TO_709.T, 0, None) * float(arg("--bg_gain", 1.0))
    out = bpy.data.images.new(key, w, h, float_buffer=True); out.colorspace_settings.name = "Linear Rec.709"
    out.pixels.foreach_set(np.dstack([lin, np.ones((h, w, 1), np.float32)]).astype(np.float32).ravel())
    bpy.data.images.remove(src)
    return out


sc = bpy.context.scene
for nme in ("Camera", "ground"):
    o = bpy.data.objects.get(nme)
    if o:
        bpy.data.objects.remove(o, do_unlink=True)
car, spins = carlib.rig(sc)                       # parked: rig at the origin, front -y, wheels straight
carlib.lights(sc, car, 0, float(arg("--lamp", 2.0)))   # daytime: DRLs on, no beams
carlib.world(sc, os.path.join(HERE, "..", "..", "sky-library", "hdr_2k", arg("--sky", "kiara_6_afternoon") + ".hdr"),
             float(arg("--skyrot", 140)), float(arg("--sky_gain", 1.0)))

# ---- ground: grey concrete pavers like the courtyard (100 x 200 mm, herringbone-ish via brick texture)
bpy.ops.mesh.primitive_plane_add(size=44, location=(0, 0, 0)); g = bpy.context.active_object; g.name = "pavers"
m = bpy.data.materials.new("pavers"); m.use_nodes = True; nt = m.node_tree
b = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
tc = nt.nodes.new("ShaderNodeTexCoord"); br = nt.nodes.new("ShaderNodeTexBrick")
br.inputs["Scale"].default_value = 5.0; br.inputs["Mortar Size"].default_value = 0.006
br.inputs["Brick Width"].default_value = 0.2; br.inputs["Row Height"].default_value = 0.1
br.inputs["Color1"].default_value = (0.13, 0.13, 0.125, 1); br.inputs["Color2"].default_value = (0.15, 0.148, 0.142, 1)
br.inputs["Mortar"].default_value = (0.10, 0.10, 0.097, 1)
nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 300
mx = nt.nodes.new("ShaderNodeMix"); mx.data_type = "RGBA"; mx.blend_type = "MULTIPLY"; mx.inputs["Factor"].default_value = 0.35
nt.links.new(tc.outputs["Object"], br.inputs["Vector"]); nt.links.new(tc.outputs["Object"], nz.inputs["Vector"])
nt.links.new(br.outputs["Color"], mx.inputs["A"]); nt.links.new(nz.outputs["Color"], mx.inputs["B"])
nt.links.new(mx.outputs["Result"], b.inputs["Base Color"]); b.inputs["Roughness"].default_value = 0.7
bump = nt.nodes.new("ShaderNodeBump"); bump.inputs["Strength"].default_value = 0.3
nt.links.new(br.outputs["Fac"], bump.inputs["Height"]); nt.links.new(bump.outputs["Normal"], b.inputs["Normal"])
# fade the pavers out 5-11 m from the car so the footage's own ground carries on behind (no hard horizon)
out = next(n for n in nt.nodes if n.type == "OUTPUT_MATERIAL"); tr = nt.nodes.new("ShaderNodeBsdfTransparent")
ms = nt.nodes.new("ShaderNodeMixShader"); ln = nt.nodes.new("ShaderNodeVectorMath"); ln.operation = "LENGTH"
mr = nt.nodes.new("ShaderNodeMapRange"); mr.inputs["From Min"].default_value = 5; mr.inputs["From Max"].default_value = 11
nt.links.new(tc.outputs["Object"], ln.inputs[0]); nt.links.new(ln.outputs["Value"], mr.inputs["Value"])
nt.links.new(mr.outputs["Result"], ms.inputs["Fac"]); nt.links.new(b.outputs[0], ms.inputs[1]); nt.links.new(tr.outputs[0], ms.inputs[2])
nt.links.new(ms.outputs[0], out.inputs["Surface"])
g.data.materials.append(m)

# ---- backdrop card: camera rays only, emission = linear plate
bpy.ops.mesh.primitive_plane_add(size=1); card = bpy.context.active_object; card.name = "backdrop"
for v in ("visible_diffuse", "visible_glossy", "visible_transmission", "visible_volume_scatter", "visible_shadow"):
    setattr(card, v, False)
cm = bpy.data.materials.new("backdrop"); cm.use_nodes = True; ct = cm.node_tree
for n in list(ct.nodes):
    ct.nodes.remove(n)
co = ct.nodes.new("ShaderNodeOutputMaterial"); em = ct.nodes.new("ShaderNodeEmission"); tex = ct.nodes.new("ShaderNodeTexImage")
ct.links.new(tex.outputs["Color"], em.inputs["Color"]); ct.links.new(em.outputs[0], co.inputs["Surface"])
card.data.materials.append(cm)

cd = bpy.data.cameras.new("cam"); cd.sensor_width = 36; cd.sensor_fit = "HORIZONTAL"; cd.clip_start = 0.02; cd.clip_end = 500
cam = bpy.data.objects.new("cam", cd); sc.collection.objects.link(cam); sc.camera = cam
cd.dof.use_dof = True

carlib.render_settings(sc, 1920, 1080, int(arg("--samples", 256)), 25)
sc.render.resolution_percentage = int(arg("--res", 100))
sc.render.film_transparent = False; sc.render.use_motion_blur = False
sc.view_layers[0].cycles.use_pass_shadow_catcher = False
sc.render.image_settings.media_type = "IMAGE"; sc.render.image_settings.file_format = "PNG"
sc.render.image_settings.color_depth = "8"
sc.view_settings.exposure = float(arg("--exposure", 0.0))
sc.frame_set(1)

D = 30.0   # backdrop distance (m)
for name in want:
    cp, aim, lens, fstop, frame = SHOTS[name]
    cp, aim = Vector(cp), Vector(aim)
    cam.location = cp; q = (aim - cp).to_track_quat("-Z", "Y"); cam.rotation_euler = q.to_euler()
    cd.lens = lens; cd.dof.aperture_fstop = fstop; cd.dof.focus_distance = (aim - cp).length
    # card faces the camera along its view axis, level (no roll), big enough to fill 16:9 with margin
    fwd = (aim - cp); fwd.z = 0; fwd.normalize()
    hw = D * 18 / lens * 1.25                 # half-width covering the horizontal FOV
    card.location = cp + fwd * D                  # plate horizon (frame centre) at eye level
    card.rotation_euler = (math.pi / 2, 0, math.atan2(-fwd.x, fwd.y))   # normal to camera, image x = screen right
    img = plate(frame); tex.image = img
    card.scale = (2 * hw, 2 * hw * img.size[1] / img.size[0], 1)
    sc.render.filepath = os.path.join(HERE, "md_" + name + ".png")
    bpy.ops.render.render(write_still=True)
    print("DETAIL_OK", name)
