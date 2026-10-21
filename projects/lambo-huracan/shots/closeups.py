"""Close-up beauty shots of the Huracán (pure CG, no plate).

  blender -b ../huracan_lp580-2.blend -P closeups.py -- <shot> [--frames 1-100] [--samples 64] [--frame N] [--sky id]
Shots: headlight_slide, wheel_track, rear_push, low_rise, profile_glide. 25 fps, 100 frames, 1920x1080.
Car front is local -y (bumper y=-2.23, rear plate y=+2.11). Moving shots drive the car along -y; the camera
is parented to a carrier that moves with it, so the road and reflections stream past.
"""
import math
import os
import sys

import bpy
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import carlib  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:]
SHOT = argv[0]


def arg(n, d):
    return argv[argv.index(n) + 1] if n in argv else d


FPS, NF = 25, 100
sc = bpy.context.scene
for nme in ("Camera", "ground"):
    o = bpy.data.objects.get(nme)
    if o:
        bpy.data.objects.remove(o, do_unlink=True)

# ---- road: wet-look asphalt with real texture so motion reads under blur
bpy.ops.mesh.primitive_plane_add(size=600, location=(0, 0, 0)); g = bpy.context.active_object; g.name = "road"
m = bpy.data.materials.new("road"); m.use_nodes = True; nt = m.node_tree
b = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
tc = nt.nodes.new("ShaderNodeTexCoord"); nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 60
nz.inputs["Detail"].default_value = 12; vor = nt.nodes.new("ShaderNodeTexVoronoi"); vor.inputs["Scale"].default_value = 900
ramp = nt.nodes.new("ShaderNodeValToRGB"); ramp.color_ramp.elements[0].color = (0.018, 0.018, 0.02, 1)
ramp.color_ramp.elements[1].color = (0.07, 0.07, 0.075, 1)
mix = nt.nodes.new("ShaderNodeMath"); mix.operation = "MULTIPLY"
nt.links.new(tc.outputs["Object"], nz.inputs["Vector"]); nt.links.new(tc.outputs["Object"], vor.inputs["Vector"])
nt.links.new(nz.outputs["Fac"], mix.inputs[0]); nt.links.new(vor.outputs["Distance"], mix.inputs[1])
nt.links.new(mix.outputs[0], ramp.inputs["Fac"]); nt.links.new(ramp.outputs["Color"], b.inputs["Base Color"])
rr = nt.nodes.new("ShaderNodeMapRange"); rr.inputs["To Min"].default_value = 0.12; rr.inputs["To Max"].default_value = 0.45
nt.links.new(nz.outputs["Fac"], rr.inputs["Value"]); nt.links.new(rr.outputs["Result"], b.inputs["Roughness"])
bump = nt.nodes.new("ShaderNodeBump"); bump.inputs["Strength"].default_value = 0.25
nt.links.new(vor.outputs["Distance"], bump.inputs["Height"]); nt.links.new(bump.outputs["Normal"], b.inputs["Normal"])
g.data.materials.append(m)

carlib.world(sc, os.path.join(HERE, "..", "..", "sky-library", "hdr_2k", arg("--sky", "the_sky_is_on_fire") + ".hdr"),
             float(arg("--skyrot", 200)), float(arg("--sky_gain", 1.0)))
car, spins = carlib.rig(sc)
carlib.lights(sc, car, 600, float(arg("--lamp", 25)))  # close on the lamp, ~4 keeps the projector detail

cd = bpy.data.cameras.new("cam"); cd.sensor_width = 36; cd.clip_start = 0.02; cd.clip_end = 2000
cam = bpy.data.objects.new("cam", cd); sc.collection.objects.link(cam); sc.camera = cam
focus = bpy.data.objects.new("focus", None); sc.collection.objects.link(focus)
cd.dof.use_dof = True; cd.dof.focus_object = focus
carrier = bpy.data.objects.new("carrier", None); sc.collection.objects.link(carrier)   # moves with the car
cam.parent = carrier; focus.parent = carrier


def ease(t):
    return t * t * (3 - 2 * t)


def drive(speed):
    """Straight drive along -y at constant speed; wheels roll; carrier follows the car."""
    pts = [(0, 40), (0, -400)]
    path = carlib.Path(pts, sigma=0.2)
    s0 = 40.0 - carlib.WB / 2   # path is the rear axle; this puts the car centre at the carrier origin
    carlib.animate(car, spins, path, [s0 + speed * (f - 1) / FPS for f in range(1, NF + 1)])
    for f in range(1, NF + 1):
        carrier.location = (0, -speed * (f - 1) / FPS, 0); carrier.keyframe_insert("location", frame=f)


def keys(cam_pts, focus_pt, lens, fstop):
    """cam_pts: [(t 0..1, (x,y,z))] eased; camera always aims at focus_pt (car-local / carrier space)."""
    cd.lens = lens; cd.dof.aperture_fstop = fstop; focus.location = focus_pt
    for f in range(1, NF + 1):
        t = ease((f - 1) / (NF - 1))
        for (t0, p0), (t1, p1) in zip(cam_pts, cam_pts[1:]):
            if t0 <= t <= t1:
                u = (t - t0) / max(1e-9, t1 - t0); p = Vector(p0).lerp(Vector(p1), u); break
        cam.location = p
        cam.rotation_euler = (Vector(focus_pt) - p).to_track_quat("-Z", "Y").to_euler()
        cam.keyframe_insert("location", frame=f); cam.keyframe_insert("rotation_euler", frame=f)


if SHOT == "headlight_slide":      # static car, low lateral slide across the lit left headlight
    drive(0.0)
    keys([(0, (-2.3, -3.4, 0.6)), (1, (-0.2, -3.6, 0.66))], (-0.72, -2.02, 0.6), 85, 2.0)
elif SHOT == "wheel_track":        # camera rides beside the front-left wheel at 30 km/h
    drive(8.3)
    keys([(0, (-2.7, -2.9, 0.42)), (1, (-2.6, -0.4, 0.5))], (-0.86, -1.31, 0.4), 30, 2.8)
elif SHOT == "rear_push":          # slow push in on tail lights + ZEDDDD plate
    drive(0.0)
    keys([(0, (0.35, 6.2, 0.95)), (1, (0.15, 3.3, 0.78))], (0.0, 2.1, 0.62), 55, 2.8)
elif SHOT == "low_rise":           # from road level in front, rise and push over the bonnet
    drive(0.0)
    keys([(0, (-0.6, -5.2, 0.12)), (1, (-0.3, -3.6, 1.45))], (0.0, -0.6, 0.75), 35, 4.0)
elif SHOT == "profile_glide":      # tracking alongside at 25 km/h, camera drifts rear to front
    drive(7.0)
    keys([(0, (-4.2, 2.6, 0.85)), (1, (-4.0, -2.4, 0.9))], (-0.9, 0.0, 0.6), 50, 4.0)
else:
    raise SystemExit("unknown shot " + SHOT)

carlib.render_settings(sc, 1920, 1080, int(arg("--samples", 64)), FPS)
sc.render.film_transparent = False
sc.render.motion_blur_shutter = 0.5
sc.view_layers[0].cycles.use_pass_shadow_catcher = False
sc.render.image_settings.media_type = "IMAGE"; sc.render.image_settings.file_format = "PNG"
sc.render.image_settings.color_depth = "8"
sc.view_settings.exposure = float(arg("--exposure", 0.0))
sc.frame_start, sc.frame_end = 1, NF
out = os.path.join(HERE, "closeups", SHOT); os.makedirs(out, exist_ok=True)
if "--frame" in argv:
    f = int(arg("--frame", 50)); sc.frame_set(f); sc.render.filepath = os.path.join(out, "test_%04d" % f)
    bpy.ops.render.render(write_still=True)
else:
    a, b2 = map(int, arg("--frames", f"1-{NF}").split("-")); sc.frame_start, sc.frame_end = a, b2
    sc.render.filepath = out + os.sep; bpy.ops.render.render(animation=True)
print("CLOSEUP_OK", SHOT)
