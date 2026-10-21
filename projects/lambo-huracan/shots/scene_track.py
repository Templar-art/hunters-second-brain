"""CG Huracán in a camera-solved ground-level plate.

  blender -b ../huracan_lp580-2.blend -P scene_track.py -- <shot dir> [--frame N | --frames a-b] [--samples 48]

<shot>/solve.json comes from solve.py (Blender libmv, arbitrary scale/orientation). <shot>/shot.json says:
  ground_px   polygon (frame-1 pixels, top-left origin) where solved points lie on the ground: plane fit (RANSAC)
  cam_height  metres above ground at frame 1 (gimbal) -> sets scale
  path_px     drive centreline in frame-1 pixels, in driving order; back-projected onto the ground
  pre         extra path points in metres, before path_px, in ground coords where the frame-1 camera sits at
              (0,0) looking +y (e.g. coming from behind the camera)
  v0, vmax, accel   speed (m/s, m/s^2)
  sky, skyrot, sky_gain, beam
Output: <shot>/exr/####.exr (Combined RGBA + Shadow Catcher), <shot>/scene.blend.
"""
import json
import math
import os
import random
import sys

import bpy
import numpy as np
from mathutils import Matrix, Vector

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import carlib  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:]
SHOT = os.path.abspath(argv[0])


def arg(n, d):
    return argv[argv.index(n) + 1] if n in argv else d


cfg = json.load(open(os.path.join(SHOT, "shot.json")))
sol = json.load(open(os.path.join(SHOT, "solve.json")))
W, H = sol["w"], sol["h"]; FPS = sol["fps"]
FPX = sol["focal_mm"] / sol["sensor_mm"] * W
cams = {c["frame"]: Matrix(c["matrix"]) for c in sol["cameras"]}
NF = max(cams)


def ray(M, u, v):
    """Pixel (top-left origin) -> world ray from a Blender camera matrix (camera looks -Z, +Y up)."""
    d = Vector(((u - W / 2) / FPX, -(v - H / 2) / FPX, -1.0))
    return M.translation.copy(), (M.to_3x3() @ d).normalized()


def inside(poly, x, y):
    c = False
    for (x1, y1), (x2, y2) in zip(poly, poly[1:] + poly[:1]):
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            c = not c
    return c


C1 = np.array(cams[1].translation[:])
gf = os.path.join(SHOT, "ground_fit.json")
if os.path.exists(gf):
    # ground from a few solved points known to sit at ground level (sills, hedge bases); up is the camera-1
    # up axis made perpendicular to the camera travel (a level gimbal move), tilted by the fitted theta
    g = json.load(open(gf)); R1 = np.array(cams[1].to_3x3()); Tr = np.array(cams[NF].translation[:]) - C1
    Tr /= np.linalg.norm(Tr); Y0 = R1[:, 1] - (R1[:, 1] @ Tr) * Tr; Y0 /= np.linalg.norm(Y0); Z0 = np.cross(Tr, Y0)
    n = math.cos(g["theta"]) * Y0 + math.sin(g["theta"]) * Z0; c0 = C1 - g["hs"] * n
    print("ground from ground_fit.json")
else:
    pts = []
    for b in sol["bundles"]:
        if b["px"] and b["err"] < 1.0:
            u, v = b["px"][0][0] * W, (1 - b["px"][0][1]) * H
            if inside(cfg["ground_px"], u, v):
                pts.append(b["co"])
    P = np.array(pts); print("ground candidates", len(P))
    random.seed(1); best = None
    spread = np.linalg.norm(P - P.mean(0), axis=1).mean()
    for _ in range(3000):
        a3, b3, c3 = P[random.sample(range(len(P)), 3)]
        nv = np.cross(b3 - a3, c3 - a3); nn = np.linalg.norm(nv)
        if nn < 1e-9:
            continue
        nv /= nn; d = np.abs((P - a3) @ nv); inl = d < 0.03 * spread
        if best is None or inl.sum() > best[0]:
            best = (inl.sum(), inl)
    Q = P[best[1]]; c0 = Q.mean(0); _, _, Vt = np.linalg.svd(Q - c0); n = Vt[2]
    if (C1 - c0) @ n < 0:
        n = -n
    print("ground inliers", best[0], "of", len(P))
h_solver = (C1 - c0) @ n
S = cfg["cam_height"] / h_solver
# ground frame: origin under camera 1, z = n, y = camera-1 forward projected on the plane
fwd = -np.array(cams[1].to_3x3().col[2][:]); fwd = fwd - (fwd @ n) * n; fwd /= np.linalg.norm(fwd)
xax = np.cross(fwd, n)
O = C1 - h_solver * n
Rg = Matrix([list(xax), list(fwd), list(n)])          # rows: world->ground rotation
T = Matrix.Scale(S, 4) @ Rg.to_4x4() @ Matrix.Translation(Vector(-O))


def to_ground(M):
    m = T @ M
    loc, rot, _ = m.decompose()
    return Matrix.LocRotScale(loc, rot, Vector((1, 1, 1)))


G = {f: to_ground(M) for f, M in cams.items()}
# sanity: reproject solved points through camera 1 and compare with their tracked pixels
errs = []
for b in sol["bundles"]:
    if not b["px"]:
        continue
    p = T @ Vector(b["co"]); q = G[1].inverted() @ p
    if q.z >= -0.1:
        continue
    u, v = W / 2 + FPX * q.x / -q.z, H / 2 - FPX * q.y / -q.z
    errs.append(math.hypot(u - b["px"][0][0] * W, v - (1 - b["px"][0][1]) * H))
print("frame-1 reprojection: median", round(float(np.median(errs)), 2), "px over", len(errs))
print("cam1", [round(x, 2) for x in G[1].translation], "camN", [round(x, 2) for x in G[NF].translation],
      "travel", round((G[NF].translation - G[1].translation).length, 2), "m")


def hit_ground(M, u, v):
    o, d = ray(M, u, v)
    t = -o.z / d.z
    return o + d * t


sc = bpy.context.scene
for nme in ("Camera", "ground"):
    o = bpy.data.objects.get(nme)
    if o:
        bpy.data.objects.remove(o, do_unlink=True)

# ---- camera, keyed per frame from the solve
cd = bpy.data.cameras.new("cam"); cd.sensor_fit = "HORIZONTAL"; cd.sensor_width = sol["sensor_mm"]; cd.lens = sol["focal_mm"]
cd.clip_start = 0.05; cd.clip_end = 1000
cam = bpy.data.objects.new("cam", cd); sc.collection.objects.link(cam); sc.camera = cam
for f, M in sorted(G.items()):
    cam.matrix_world = M; cam.keyframe_insert("location", frame=f); cam.keyframe_insert("rotation_euler", frame=f)

carlib.catcher(sc, 400, (0, 100))
carlib.world(sc, os.path.join(HERE, "..", "..", "sky-library", "hdr_2k", cfg.get("sky", "qwantani_dusk_2_puresky") + ".hdr"),
             float(arg("--skyrot", cfg.get("skyrot", 120))), float(arg("--sky_gain", cfg.get("sky_gain", 1.0))))

# ---- path: pre points (metres) + drive centreline back-projected from frame 1
drive = [hit_ground(G[1], u, v) for u, v in cfg["path_px"]]
pts = [tuple(p) for p in cfg.get("pre", [])] + [(p.x, p.y) for p in drive]
path = carlib.Path(pts, sigma=cfg.get("sigma", 1.5))
print("path", round(path.L, 1), "m, tightest radius", round(path.tightest(), 1), "m")
car, spins = carlib.rig(sc)
v, s, s_list = cfg.get("v0", 3.0), cfg.get("s0", 0.5), []
for f in range(NF):
    s_list.append(s); v = min(cfg.get("vmax", 6.0), v + cfg.get("accel", 1.0) / FPS)
    v = min(v, math.sqrt(2 * cfg.get("brake", 1.8) * max(0.0, path.L - 0.3 - s)))   # ease to a stop at the end
    s = min(s + v / FPS, path.L - 0.3)
carlib.animate(car, spins, path, s_list)
carlib.lights(sc, car, float(arg("--beam", cfg.get("beam", 900))))

carlib.render_settings(sc, W, H, int(arg("--samples", 48)), FPS)
sc.view_settings.exposure = 0.0
sc.frame_start, sc.frame_end = 1, NF
out = os.path.join(SHOT, "exr"); os.makedirs(out, exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(SHOT, "scene.blend"))
if "--frame" in argv:
    f = int(arg("--frame", 1)); sc.frame_set(f); sc.render.filepath = os.path.join(out, "test_%04d" % f)
    bpy.ops.render.render(write_still=True)
elif "--frames" in argv:
    a, b = map(int, arg("--frames", "1-1").split("-")); sc.frame_start, sc.frame_end = a, b
    sc.render.filepath = out + os.sep; bpy.ops.render.render(animation=True)
print("SCENE_OK")
