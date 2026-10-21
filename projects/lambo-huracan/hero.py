"""Quick beauty still of the Huracán:  blender -b huracan_lp580-2.blend -P hero.py -- <sky id> <out.png> [skyrot]"""
import math, os, sys
import bpy
from mathutils import Vector
a = sys.argv[sys.argv.index("--") + 1:]
sky, out = a[0], a[1]; rot = float(a[2]) if len(a) > 2 else 200
HERE = os.path.dirname(os.path.abspath(__file__)); sc = bpy.context.scene
w = sc.world; nt = w.node_tree
env = next(n for n in nt.nodes if n.type == "TEX_ENVIRONMENT")
env.image = bpy.data.images.load(os.path.join(HERE, "..", "sky-library", "hdr_2k", sky + ".hdr"))
mp = next((n for n in nt.nodes if n.type == "MAPPING"), None)
if mp is None:
    tc = nt.nodes.new("ShaderNodeTexCoord"); mp = nt.nodes.new("ShaderNodeMapping")
    nt.links.new(tc.outputs["Generated"], mp.inputs["Vector"]); nt.links.new(mp.outputs[0], env.inputs["Vector"])
mp.inputs["Rotation"].default_value = (0, 0, math.radians(rot))
g = bpy.data.objects.get("ground")
if g:   # wet-look dark asphalt so the car gets a reflection
    m = bpy.data.materials.new("hero_asphalt"); m.use_nodes = True
    b = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    b.inputs["Base Color"].default_value = (0.03, 0.03, 0.035, 1); b.inputs["Roughness"].default_value = 0.22
    g.data.materials.clear(); g.data.materials.append(m)
cd = bpy.data.cameras.new("hero"); cd.lens = 55
cam = bpy.data.objects.new("hero", cd); sc.collection.objects.link(cam); sc.camera = cam
cam.location = (-4.6, -6.4, 0.95)
cam.rotation_euler = (Vector((0, -0.2, 0.55)) - cam.location).to_track_quat("-Z", "Y").to_euler()
sc.render.engine = "CYCLES"; sc.cycles.samples = 160; sc.cycles.use_denoising = True
p = bpy.context.preferences.addons["cycles"].preferences; p.compute_device_type = "METAL"; p.get_devices()
for d in p.devices: d.use = True
sc.cycles.device = "GPU"; sc.render.film_transparent = False
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1920, 1080, 100
sc.view_settings.view_transform = "AgX"; sc.view_settings.look = "AgX - Punchy"
sc.render.image_settings.file_format = "PNG"; sc.render.filepath = out
bpy.ops.render.render(write_still=True); print("HERO_OK", out)
