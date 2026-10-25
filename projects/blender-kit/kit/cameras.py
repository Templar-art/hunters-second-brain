"""cameras: one camera per shot on a shared timeline, each in its own frame slot with a marker.

scene.json "shots": [
  {"name": "B1_SurfReveal", "preset": "drone_reveal", "frames": 192,
   "path": [[x, y, z], …] | "keys": [[offset_frame, x, y, z], …],
   "look_at": [x, y, z] | [[x, y, z], …] (spread over the slot) | [[offset_frame, x, y, z], …]
            | {"follow": "Rig_Person_BeachWalk", "offset": [0, 0, 1.3]},
   "lens": 32, "shake": 0.2, "guide_frames": [0]}  // guide frames are offsets within the slot
   // or, instead of look_at, a flown gimbal: "rot_keys": [[offset_frame, pitch_deg, yaw_deg], …]
   //   pitch 0 = level, negative = tilted down; yaw 0 = looking toward -Y (the ocean in the beach scenes)
]
A flown gimbal (rot_keys) is how a real drone moves: the aim changes slowly and on purpose, rather
than swinging with a look-at target. Prefer it for drone and crane moves.
Presets only set defaults (lens, shake); anything in the shot overrides them.
"""
import math
import bpy
from . import core

PRESETS = {
    "drone_reveal":  {"lens": 32, "shake": 0.05},
    "top_down_rise": {"lens": 28, "shake": 0.05},
    "glide":         {"lens": 24, "shake": 0.15},   # Shakify INVESTIGATION-style
    "interior_drift": {"lens": 20, "shake": 0.15},
    "walkthrough":   {"lens": 18, "shake": 0.3},    # WALK_TO_THE_STORE-style
    "gimbal_track":  {"lens": 35, "shake": 0.25},
    "car_track":     {"lens": 35, "shake": 0.1},
}


def _spread(points, start, length):
    if len(points) == 1:
        return [(start, points[0])]
    return [(round(start + (length - 1) * i / (len(points) - 1)), p) for i, p in enumerate(points)]


def _add_noise(obj, strength, scale=40):
    for fc in core.fcurves(obj):
        if fc.data_path == "location":
            m = fc.modifiers.new("NOISE")
            m.strength = strength
            m.scale = scale
            m.phase = hash((obj.name, fc.array_index)) % 100


def shot(s, start, ctx, col):
    cfg = {**PRESETS.get(s.get("preset", ""), {}), **s}
    L = cfg.get("frames", 192)
    cam_data = bpy.data.cameras.new(s["name"])
    cam_data.lens = cfg.get("lens", 28)
    cam_data.clip_end = 1000
    cam = bpy.data.objects.new(s["name"], cam_data)
    col.objects.link(cam)

    if "keys" in cfg:
        keys = [(start + k[0], tuple(k[1:4])) for k in cfg["keys"]]
    else:
        keys = _spread([tuple(p) for p in cfg["path"]], start, L)
    core.key_path(cam, keys)

    if "rot_keys" in cfg:
        cam.rotation_mode = "XYZ"
        for k in cfg["rot_keys"]:
            cam.rotation_euler = (math.radians(90 + k[1]), 0.0, math.radians(180 + k[2]))
            cam.keyframe_insert("rotation_euler", frame=start + k[0])
        if cfg.get("shake"):
            _add_noise(cam, cfg["shake"] * 0.08, scale=60)
        m = bpy.context.scene.timeline_markers.new(s["name"], frame=start)
        m.camera = cam
        return L, [start + g for g in cfg.get("guide_frames", [0])]

    tgt = bpy.data.objects.new("Tgt_" + s["name"], None)
    col.objects.link(tgt)
    la = cfg["look_at"]
    if isinstance(la, dict):
        c = tgt.constraints.new("COPY_LOCATION")
        c.target = bpy.data.objects[la["follow"]]
        tgt.location = la.get("offset", (0, 0, 1.3))
        c.use_offset = True
    elif isinstance(la[0], (list, tuple)) and len(la[0]) == 4:      # [offset_frame, x, y, z]
        core.key_path(tgt, [(start + k[0], tuple(k[1:4])) for k in la])
    elif isinstance(la[0], (list, tuple)):
        core.key_path(tgt, _spread([tuple(p) for p in la], start, L))
    else:
        tgt.location = la
        tgt.keyframe_insert("location", frame=start)    # keyed so the shake noise has a curve
    tr = cam.constraints.new("TRACK_TO")
    tr.target = tgt
    tr.track_axis = "TRACK_NEGATIVE_Z"
    tr.up_axis = "UP_Y"

    if cfg.get("shake"):
        _add_noise(tgt, cfg["shake"] * 0.4)
        _add_noise(cam, cfg["shake"] * 0.08, scale=60)

    m = bpy.context.scene.timeline_markers.new(s["name"], frame=start)
    m.camera = cam
    guides = [start + g for g in cfg.get("guide_frames", [0])]
    return L, guides


def build(spec, ctx):
    col = core.coll("Cameras")
    sc = bpy.context.scene
    start, guides = 1, []
    for s in spec:
        L, g = shot(s, start, ctx, col)
        guides += [(s["name"], f) for f in g]
        start += L
    sc.frame_start, sc.frame_end = 1, start - 1
    if spec:
        sc.camera = bpy.data.objects[spec[0]["name"]]
    ctx.report["guide_frames"] = guides
    return guides
