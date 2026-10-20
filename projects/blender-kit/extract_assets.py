# One-time: build the kit's asset library from a finished scene.
#   blender -b <source.blend> -P extract_assets.py -- <out kit-assets.blend>
#
# Keeps only reusable template objects (Poly Haven plants/grass/tree/chair, the rigged
# mannequins), groups each into an "A_<key>" collection at the origin, keeps every material
# and the world with a fake user, and saves. Everything else is deleted from the copy.
import bpy, sys

out = sys.argv[sys.argv.index("--") + 1]
O = bpy.data.objects

# key -> how to find the template objects in the source scene
GROUPS = {
    "grass":         lambda o: o.name.startswith("grass_medium_01_"),
    "anthurium":     lambda o: o.users_collection and o.users_collection[0].name == "anthurium_botany_01",
    "calathea":      lambda o: o.users_collection and o.users_collection[0].name == "calathea_orbifolia_01",
    "fern":          lambda o: o.users_collection and o.users_collection[0].name == "fern_02",
    "potted_plant":  lambda o: o.users_collection and o.users_collection[0].name == "potted_plant_02",
    "island_tree":   lambda o: o.name == "StreetTree_0",
    "dining_chair":  lambda o: o.name == "OutDining_Chair_0",
}
PEOPLE = sorted({o.name[len("Rig_"):] for o in O if o.name.startswith("Rig_Person_")})

keep = {}
for key, f in GROUPS.items():
    keep[key] = [o for o in O if o.type == "MESH" and f(o)]
for p in PEOPLE:
    rig = O["Rig_" + p]
    keep["person:" + p] = [rig] + list(rig.children_recursive)

for key, objs in keep.items():
    print(f"ASSET {key}: {len(objs)} objects")
    if not objs:
        raise SystemExit(f"no template objects for {key}")

keep_set = {o for objs in keep.values() for o in objs}
for o in list(O):
    if o not in keep_set:
        O.remove(o, do_unlink=True)

for c in list(bpy.data.collections):
    bpy.data.collections.remove(c)
root = bpy.context.scene.collection
for key, objs in keep.items():
    col = bpy.data.collections.new("A_" + key.replace("person:", "P_"))
    root.children.link(col)
    # move the group so its first object sits at the origin (people keep their rig at origin)
    anchor = objs[0]
    off = anchor.location.copy() if not anchor.parent else None
    for o in objs:
        for c in o.users_collection:
            c.objects.unlink(o)
        col.objects.link(o)
        if off is not None and o.parent is None:
            o.location -= off
            if key == "grass":           # grass pieces were parked 50 m below ground
                o.location.z = 0
for m in bpy.data.materials:
    m.use_fake_user = True
for w in bpy.data.worlds:
    w.use_fake_user = True
for a in bpy.data.actions:
    a.use_fake_user = True

bpy.ops.outliner.orphans_purge(do_recursive=True)
bpy.ops.wm.save_as_mainfile(filepath=out, compress=True)
print("ASSETS SAVED", out, len(bpy.data.objects), "objects")
