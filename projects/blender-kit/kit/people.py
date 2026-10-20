"""people: rigged mannequins (MPFB2) from the kit library, placed or walked along a path.
The AI repaints them from the cast refs; they only fix position, scale and gait.

scene.json "people": [
  {"name": "Person_BeachWalk", "template": "Person_BeachWalk", "at": [x, y, z], "rot_z": 1.57},
  {"name": "Person_Walker2", "template": "Person_BeachWalk", "path": [[frame, x, y], …], "ground": true}
]
Templates (kit library): Person_BalconyA/B, Person_BeachWalk/2 (walk cycle), Person_Kitchen,
Person_Lounger, Person_PoolEdge. `path` keys the rig empty; z follows the terrain when "ground".
"""
import bpy
from . import core


def build(spec, ctx):
    col = core.coll("People")
    for p in spec:
        root = bpy.data.objects.get("KIT_Rig_" + p["template"])
        if root is None:
            raise KeyError(f"people: template {p['template']} not in kit library")
        rig = core.copy_hierarchy(root, p["name"], col)
        if "at" in p:
            rig.location = p["at"]
        if "rot_z" in p:
            rig.rotation_euler.z = p["rot_z"]
        if "path" in p:
            pts = []
            for f, x, y, *z in p["path"]:
                zz = z[0] if z else (ctx.terrain(x, y) if p.get("ground", True) else rig.location.z)
                pts.append((f, (x, y, zz)))
            core.key_path(rig, pts)
