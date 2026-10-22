"""18 Maryland Avenue, Carrara: house + site rebuilt 1:1 from the Kollosche floor plan.

  python3 plan_extract.py                                   # plan -> plan.npz (wall / opening masks)
  blender -b -P build.py -- [--render] [--samples 32] [--res 50]

World: metres, X along the lot from the water (west boundary corner) toward Maryland Ave, Y north, Z up.
Site plan: 2.9 px/m; floor plans: 13.1 px/m. The ground plan is placed on the site from the site-plan residence
outline; the upper level is registered onto the ground level (side verandahs line up); the guest house sits where
the site plan draws it, rotated to the north boundary. Facades/roof from 10x's own footage: white weatherboard,
charcoal tiled hip roofs, white balustrade balconies, solar panels, pyramid cupola on the water side.
v2 (listing photos, raw/18-maryland/listing/): white rendered ground floor + weatherboard upper, Chinese
Chippendale balustrades, porthole window on the water facade, frameless glass pool fence + loungers, rock seawall
(no beach), travertine gate pillars + "18 MARYLAND" sign wall, white gate leaf, flagpole, fire-pit seat wall by
the water, weeping-fig row along the north boundary.
Output: maryland.blend + qc/*.png
"""
import math
import os
import sys

import bmesh
import bpy
import numpy as np
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []


def arg(n, d):
    return argv[argv.index(n) + 1] if n in argv else d


P = np.load(os.path.join(HERE, "plan.npz"))
MPX = 13.1                                       # floor plan px per metre (2000 px sheet)
SUP = float(P["px_per_m"]) / MPX                 # mask supersample
HX0, HY0 = 43.6, 24.0                            # site metres of ground-plan px (608.75, 362.5)
UPPER_ORIGIN = (962 - 352.0, 440 - 82.0)         # upper drawing -> ground plan px (verandahs line up)
GUEST_C, GUEST_ROT = (87.9, 24.2), math.radians(4.5)

FFL, G_TOP, U_FFL, U_TOP = 0.3, 3.3, 3.5, 6.2    # ground floor, ground wall top, upper floor, upper eave


def hw(px, py):
    """ground-plan px -> world xy"""
    return HX0 + (px - 608.75) / MPX, HY0 - (py - 362.5) / MPX


def guest_w(px, py):
    lx, ly = (px - 1082.5) / MPX - 8.35, -((py - 323.75) / MPX - 3.3)
    c, s = math.cos(GUEST_ROT), math.sin(GUEST_ROT)
    return GUEST_C[0] + c * lx - s * ly, GUEST_C[1] + s * lx + c * ly


def site(px, py):
    return (px - 772.8) / 2.9, (779.6 - py) / 2.9


# ------------------------------------------------------------------ scene + materials
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
COLS = {}


def col(name):
    if name not in COLS:
        c = bpy.data.collections.new(name); sc.collection.children.link(c); COLS[name] = c
    return COLS[name]


def mat(name, rgb, rough=0.5, metal=0.0, alpha=1.0, emit=0.0, trans=0.0):
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if trans:
        b.inputs["Transmission Weight"].default_value = trans
    if alpha < 1:
        b.inputs["Alpha"].default_value = alpha
    if emit:
        b.inputs["Emission Color"].default_value = (*rgb, 1); b.inputs["Emission Strength"].default_value = emit
    return m


def shadow_clear(m):
    """glass that still lets direct light through (Cycles blocks sun shadow rays at transmissive surfaces)"""
    nt = m.node_tree; out = next(n for n in nt.nodes if n.type == "OUTPUT_MATERIAL")
    b = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    lp = nt.nodes.new("ShaderNodeLightPath"); tr = nt.nodes.new("ShaderNodeBsdfTransparent"); mx = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(lp.outputs["Is Shadow Ray"], mx.inputs[0]); nt.links.new(b.outputs[0], mx.inputs[1])
    nt.links.new(tr.outputs[0], mx.inputs[2]); nt.links.new(mx.outputs[0], out.inputs["Surface"])
    return m


def textured(m, kind, scale, strength, ramp=None):
    """procedural bump (weatherboard laps, roof tiles, grass) + optional two-colour noise ramp"""
    nt = m.node_tree; b = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    tc = nt.nodes.new("ShaderNodeTexCoord"); bump = nt.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = strength; bump.inputs["Distance"].default_value = 0.02
    if kind == "boards":
        t = nt.nodes.new("ShaderNodeTexWave"); t.wave_type = "BANDS"; t.bands_direction = "Z"; t.wave_profile = "SAW"
        t.inputs["Scale"].default_value = scale; t.inputs["Distortion"].default_value = 0.0
    else:
        t = nt.nodes.new("ShaderNodeTexNoise"); t.inputs["Scale"].default_value = scale
        t.inputs["Detail"].default_value = 8
    nt.links.new(tc.outputs["Object"], t.inputs["Vector"]); nt.links.new(t.outputs["Fac"], bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], b.inputs["Normal"])
    if ramp:
        cr = nt.nodes.new("ShaderNodeValToRGB"); cr.color_ramp.elements[0].color = (*ramp[0], 1)
        cr.color_ramp.elements[1].color = (*ramp[1], 1); nt.links.new(t.outputs["Fac"], cr.inputs["Fac"])
        nt.links.new(cr.outputs["Color"], b.inputs["Base Color"])
    return m


def lawn_mat():
    m = textured(mat("Grass_lawn", (0.1, 0.24, 0.05), 0.9), "noise", 0.15, 0.1, ramp=((0.06, 0.17, 0.03), (0.11, 0.27, 0.05)))
    nt = m.node_tree; b = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED"); cr = next(n for n in nt.nodes if n.type == "VALTORGB")
    tc = next(n for n in nt.nodes if n.type == "TEX_COORD")
    wv = nt.nodes.new("ShaderNodeTexWave"); wv.wave_type = "BANDS"; wv.bands_direction = "Y"; wv.wave_profile = "SIN"
    wv.inputs["Scale"].default_value = 0.26; wv.inputs["Distortion"].default_value = 0.3   # ~2.4 m mower passes
    rmp = nt.nodes.new("ShaderNodeMapRange"); rmp.inputs["From Min"].default_value = 0.45; rmp.inputs["From Max"].default_value = 0.55
    mix = nt.nodes.new("ShaderNodeMix"); mix.data_type = "RGBA"; mix.blend_type = "MULTIPLY"
    mix.inputs["B"].default_value = (1.2, 1.17, 1.12, 1)
    nt.links.new(tc.outputs["Object"], wv.inputs["Vector"]); nt.links.new(wv.outputs["Fac"], rmp.inputs["Value"])
    nt.links.new(rmp.outputs["Result"], mix.inputs["Factor"]); nt.links.new(cr.outputs["Color"], mix.inputs["A"])
    nt.links.new(mix.outputs["Result"], b.inputs["Base Color"])
    return m


M = dict(
    wall=mat("Render_white", (0.84, 0.84, 0.82), 0.6),
    boards=textured(mat("Weatherboard_white", (0.84, 0.84, 0.82), 0.55), "boards", 1.75, 0.35),
    trim=mat("Render_trim_white", (0.9, 0.9, 0.88), 0.4),
    roof=textured(mat("Roof_tile_charcoal", (0.045, 0.048, 0.052), 0.65), "noise", 40, 0.25),
    glass=mat("Glass_window", (0.9, 0.95, 0.95), 0.0, trans=1.0),
    floor=mat("Floor_tile_light", (0.6, 0.58, 0.55), 0.4),
    timber_floor=textured(mat("Floor_timber_dark", (0.09, 0.06, 0.045), 0.35), "noise", 2.0, 0.05,
                          ramp=((0.06, 0.04, 0.03), (0.13, 0.085, 0.06))),
    carpet=textured(mat("Carpet_charcoal", (0.17, 0.17, 0.175), 1.0), "noise", 300, 0.15, ramp=((0.13, 0.13, 0.135), (0.21, 0.21, 0.215))),
    pavers=mat("Concrete_pavers_grey", (0.42, 0.42, 0.41), 0.75),
    drive=mat("Concrete_drive", (0.48, 0.47, 0.45), 0.8),
    lawn=lawn_mat(),
    lawn_far=textured(mat("Grass_far", (0.06, 0.13, 0.04), 0.9), "noise", 0.02, 0.0, ramp=((0.04, 0.09, 0.03), (0.09, 0.17, 0.05))),
    sand=textured(mat("Rock_seawall", (0.25, 0.24, 0.22), 0.9), "noise", 6, 1.0, ramp=((0.07, 0.07, 0.065), (0.3, 0.28, 0.25))),
    water=mat("Water_canal", (0.05, 0.11, 0.12), 0.05),
    pool=mat("Pool_water", (0.12, 0.45, 0.5), 0.05),
    coping=mat("Stone_coping", (0.7, 0.68, 0.63), 0.6),
    hedge=mat("Plants_hedge", (0.05, 0.13, 0.04), 0.9),
    leaf=mat("Plants_tree_canopy", (0.07, 0.15, 0.05), 0.9),
    trunk=mat("Trunk_bark", (0.25, 0.2, 0.15), 0.9),
    stone=textured(mat("Stone_wall_travertine", (0.58, 0.53, 0.45), 0.75), "noise", 4, 0.15, ramp=((0.48, 0.43, 0.36), (0.66, 0.61, 0.53))),
    solar=mat("Metal_solar_panel", (0.02, 0.03, 0.06), 0.15, metal=0.6),
    road=mat("Asphalt_road", (0.1, 0.1, 0.1), 0.9),
    neigh=mat("Render_neighbour", (0.78, 0.74, 0.68), 0.7),
    terracotta=mat("Roof_terracotta", (0.42, 0.16, 0.1), 0.7),
    timber=mat("Timber_jetty", (0.35, 0.27, 0.2), 0.8),
    black=mat("Metal_black", (0.03, 0.03, 0.03), 0.4),
    glass_dark=mat("Glass_dark_reflective", (0.02, 0.025, 0.03), 0.05, metal=0.3),
    glass_lit=mat("Glass_lit_warm", (0.9, 0.65, 0.4), 0.3, emit=0.001),
    fence=shadow_clear(mat("Glass_pool_fence", (0.8, 0.9, 0.9), 0.02, trans=1.0)),
    steel=mat("Steel_brushed", (0.7, 0.7, 0.7), 0.3, metal=1.0),
    cushion=mat("Fabric_lounger_charcoal", (0.08, 0.08, 0.085), 0.8),
)


def obj(name, bm, material, collection):
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); col(collection).objects.link(o)
    o.data.materials.append(material)
    return o


def add_box(bm, x0, y0, x1, y1, z0, z1):
    vs = [bm.verts.new((x, y, z)) for z in (z0, z1) for x, y in ((x0, y0), (x1, y0), (x1, y1), (x0, y1))]
    for f in ((0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)):
        bm.faces.new([vs[i] for i in f])


def add_quad_prism(bm, pts, z0, z1):
    """extrude an arbitrary convex/concave ring of xy points"""
    lo = [bm.verts.new((x, y, z0)) for x, y in pts]; hi = [bm.verts.new((x, y, z1)) for x, y in pts]
    bm.faces.new(lo[::-1]); bm.faces.new(hi)
    n = len(pts)
    for i in range(n):
        j = (i + 1) % n; bm.faces.new((lo[i], lo[j], hi[j], hi[i]))


def box(name, x0, y0, x1, y1, z0, z1, material, collection):
    bm = bmesh.new(); add_box(bm, min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1), z0, z1)
    return obj(name, bm, material, collection)


def prism(name, pts, z0, z1, material, collection):
    bm = bmesh.new(); add_quad_prism(bm, pts, z0, z1); return obj(name, bm, material, collection)


# ------------------------------------------------------------------ mask -> wall boxes
def rects(mask):
    """greedy: horizontal runs per row merged down while the span repeats"""
    H, W = mask.shape; out = []; open_ = {}
    for r in range(H + 1):
        row = mask[r] if r < H else np.zeros(W, np.uint8)
        runs = set(); c = 0
        while c < W:
            if row[c]:
                s = c
                while c < W and row[c]:
                    c += 1
                runs.add((s, c))
            else:
                c += 1
        nxt = {}
        for span, r0 in open_.items():
            if span in runs:
                nxt[span] = r0
            else:
                out.append((span[0], r0, span[1], r))
        for span in runs:
            nxt.setdefault(span, r)
        open_ = nxt
    return out


def to_world(rect, origin, fn):
    c0, r0, c1, r1 = rect
    a = fn(origin[0] + c0 / SUP, origin[1] + r0 / SUP); b = fn(origin[0] + c1 / SUP, origin[1] + r1 / SUP)
    return a, b


WALLS, OPENINGS = [], []                         # (level, xa, ya, xb, yb) world rects, read by interior.py + review.py


def walls_from(level, origin, fn, z0, z1, collection, footprint, wall_mat="wall"):
    w = P[level + "_wall"]; h = P[level + "_header"]
    bm = bmesh.new()
    for rc in rects(w):
        (x0, y0), (x1, y1) = to_world(rc, origin, fn)
        if abs(x1 - x0) * abs(y1 - y0) > 0.004:
            add_box(bm, min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1), z0, z1)
            if level != "guest":
                WALLS.append((level, min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)))
    obj(f"{level}_walls", bm, M[wall_mat], collection)
    bmh = bmesh.new(); bmg = bmesh.new(); bmf = bmesh.new()
    for rc in rects(h):
        (x0, y0), (x1, y1) = to_world(rc, origin, fn)
        xa, xb, ya, yb = min(x0, x1), max(x0, x1), min(y0, y1), max(y0, y1)
        if (xb - xa) * (yb - ya) < 0.004:
            continue
        if level != "guest":
            OPENINGS.append((level, xa, ya, xb, yb))
        add_box(bmh, xa, ya, xb, yb, z0 + 2.2, z1)
        cx, cy = (xa + xb) / 2, (ya + yb) / 2; horiz = (xb - xa) > (yb - ya)
        p1 = (cx, cy + 0.8) if horiz else (cx + 0.8, cy); p2 = (cx, cy - 0.8) if horiz else (cx - 0.8, cy)
        if inside(footprint, p1) != inside(footprint, p2):          # exterior opening -> glazing + frame
            pad = 0.05
            if horiz:
                add_box(bmg, xa, cy - 0.02, xb, cy + 0.02, z0, z0 + 2.2)
                add_box(bmf, xa, cy - 0.05, xb, cy + 0.05, z0 + 2.15, z0 + 2.2)
                n = max(1, round((xb - xa) / 1.0))
                for k in range(n + 1):
                    x = xa + (xb - xa) * k / n; add_box(bmf, x - pad / 2, cy - 0.05, x + pad / 2, cy + 0.05, z0, z0 + 2.2)
            else:
                add_box(bmg, cx - 0.02, ya, cx + 0.02, yb, z0, z0 + 2.2)
                add_box(bmf, cx - 0.05, ya, cx + 0.05, yb, z0 + 2.15, z0 + 2.2)
                n = max(1, round((yb - ya) / 1.0))
                for k in range(n + 1):
                    y = ya + (yb - ya) * k / n; add_box(bmf, cx - 0.05, y - pad / 2, cx + 0.05, y + pad / 2, z0, z0 + 2.2)
    obj(f"{level}_headers", bmh, M[wall_mat], collection)
    obj(f"{level}_glazing", bmg, M["glass"], collection)
    obj(f"{level}_window_frames", bmf, M["black"], collection)


def inside(poly, p):
    x, y = p; c = False
    for (x1, y1), (x2, y2) in zip(poly, poly[1:] + poly[:1]):
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            c = not c
    return c


# ------------------------------------------------------------------ roofs
def hip(name, x0, y0, x1, y1, z, pitch=25, over=0.6, collection="house_roof", material=None, solar=None):
    x0, x1 = min(x0, x1) - over, max(x0, x1) + over; y0, y1 = min(y0, y1) - over, max(y0, y1) + over
    w, d = x1 - x0, y1 - y0; t = math.tan(math.radians(pitch))
    bm = bmesh.new()
    a, b, c, e = (bm.verts.new(v) for v in ((x0, y0, z), (x1, y0, z), (x1, y1, z), (x0, y1, z)))
    if w >= d:
        hgt = d / 2 * t; r1 = bm.verts.new((x0 + d / 2, (y0 + y1) / 2, z + hgt)); r2 = bm.verts.new((x1 - d / 2, (y0 + y1) / 2, z + hgt))
        bm.faces.new((a, b, r2, r1)); bm.faces.new((c, e, r1, r2)); bm.faces.new((e, a, r1)); bm.faces.new((b, c, r2))
    else:
        hgt = w / 2 * t; r1 = bm.verts.new(((x0 + x1) / 2, y0 + w / 2, z + hgt)); r2 = bm.verts.new(((x0 + x1) / 2, y1 - w / 2, z + hgt))
        bm.faces.new((b, c, r2, r1)); bm.faces.new((e, a, r1, r2)); bm.faces.new((a, b, r1)); bm.faces.new((c, e, r2))
    bm.faces.new((e, c, b, a))                                   # soffit
    o = obj(name, bm, material or M["roof"], collection)
    box(name + "_fascia", x0, y0, x1, y1, z - 0.22, z, M["trim"], collection).display_type = "WIRE"
    bpy.data.objects.remove(bpy.data.objects[name + "_fascia"])
    fas = bmesh.new()
    for xa, ya, xb, yb in ((x0, y0, x1, y0 + 0.04), (x0, y1 - 0.04, x1, y1), (x0, y0, x0 + 0.04, y1), (x1 - 0.04, y0, x1, y1)):
        add_box(fas, xa, ya, xb, yb, z - 0.22, z)
    obj(name + "_fascia", fas, M["trim"], collection)
    if solar:                                                    # panels on the north face
        sx0, sx1 = solar
        pv = bmesh.new()
        ym = (y0 + y1) / 2; ny = 3 if w >= d else 2
        for i in range(int((sx1 - sx0) / 1.05)):
            for j in range(ny):
                px = sx0 + i * 1.05; py = ym + 0.4 + j * 1.75
                if py + 1.7 > y1 - 0.3:
                    continue
                zz = z + (y1 - (py + 0.85)) * t + 0.06
                add_box(pv, px, py, px + 1.0, py + 1.7, zz, zz + 0.04)
        o2 = obj(name + "_solar", pv, M["solar"], collection)
        o2.rotation_mode = "XYZ"
    return o


def flat_roof(name, x0, y0, x1, y1, z, collection="house_roof"):
    box(name, x0, y0, x1, y1, z, z + 0.25, M["trim"], collection)


def pyramid(name, cx, cy, half, z, h, collection="house_roof"):
    bm = bmesh.new(); v = [bm.verts.new((cx + sx * half, cy + sy * half, z)) for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    top = bm.verts.new((cx, cy, z + h))
    for i in range(4):
        bm.faces.new((v[i], v[(i + 1) % 4], top))
    bm.faces.new(v[::-1]); obj(name, bm, M["roof"], collection)


def bar(bm, p, q, t0, z0, t1, z1, th=0.025):
    """thin square bar in the vertical plane of side p->q, from (t0, z0) to (t1, z1) (t in metres along the side)"""
    L = math.dist(p, q); ux, uy = (q[0] - p[0]) / L, (q[1] - p[1]) / L
    a = Vector((p[0] + ux * t0, p[1] + uy * t0, z0)); b = Vector((p[0] + ux * t1, p[1] + uy * t1, z1))
    d = (b - a).normalized(); n = Vector((-uy, ux, 0)); m = d.cross(n).normalized()
    vs = [bm.verts.new(c + n * sn * th + m * sm * th) for c in (a, b) for sn, sm in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    for f in ((0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)):
        bm.faces.new([vs[i] for i in f])


def chippendale(bm, p, q, z0, z1, panel=1.25):
    """Chinese Chippendale fretwork: per panel a post, a centre square and the X through it (listing photos 02/06)"""
    L = math.dist(p, q); n = max(1, round(L / panel)); w = L / n; h = z1 - z0
    for i in range(n + 1):
        bar(bm, p, q, i * w, z0, i * w, z1, 0.045)
    for i in range(n):
        a, b = i * w, (i + 1) * w; c = (a + b) / 2; s = min(w, h) * 0.22; zm = z0 + h / 2
        bar(bm, p, q, a, z0, b, z1); bar(bm, p, q, a, z1, b, z0)
        for (t0, za, t1, zb) in ((c - s, zm - s, c + s, zm - s), (c - s, zm + s, c + s, zm + s),
                                 (c - s, zm - s, c - s, zm + s), (c + s, zm - s, c + s, zm + s)):
            bar(bm, p, q, t0, za, t1, zb)
        bar(bm, p, q, a, zm, c - s, zm); bar(bm, p, q, c + s, zm, b, zm)


# ------------------------------------------------------------------ house
GROUND_PX = [(686.25, 362.5), (972.5, 362.5), (972.5, 490), (853.75, 490), (853.75, 510), (843.75, 510),
             (843.75, 627.5), (670, 627.5), (670, 503.75), (700, 503.75), (700, 426.25), (686.25, 426.25)]
UPPER_PX = [(685.5, 363), (971.75, 363), (971.75, 488), (858, 488), (858, 515.5), (769, 515.5),
            (769, 593), (704, 593), (704, 431.75), (685.5, 431.75)]
G_POLY = [hw(*p) for p in GROUND_PX]; U_POLY = [hw(*p) for p in UPPER_PX]

walls_from("ground", (600, 320), hw, FFL, G_TOP, "house_ground", G_POLY)
walls_from("upper", UPPER_ORIGIN, hw, U_FFL, U_TOP, "house_upper", U_POLY, "boards")
prism("ground_slab", G_POLY, 0.0, FFL, M["timber_floor"], "house_ground")
prism("upper_slab", U_POLY, G_TOP, U_FFL, M["carpet"], "house_upper")
prism("ground_ceiling", U_POLY, G_TOP - 0.02, G_TOP, M["trim"], "house_ground")
prism("upper_ceiling", U_POLY, U_TOP - 0.05, U_TOP, M["trim"], "house_upper")

# decks (plan px rects) -> pavers at ground, balcony decks upstairs
DECKS = {"outdoor_entertaining": (608.75, 362.5, 686.25, 585), "verandah_west": (853.75, 325, 931.25, 362.5),
         "verandah_east": (972.5, 362.5, 996.25, 490), "porch": (853.75, 490, 896.25, 510)}
for n, (a, b, c, d) in DECKS.items():
    (x0, y0), (x1, y1) = hw(a, b), hw(c, d); box("deck_" + n, x0, y0, x1, y1, 0, FFL - 0.02, M["pavers"], "house_decks")
BALC = {"master_balcony": (614.25, 433, 704.25, 525.5), "east_balcony": (971.75, 363, 996.75, 488)}
for n, (a, b, c, d) in BALC.items():
    (x0, y0), (x1, y1) = hw(a, b), hw(c, d)
    box(n + "_deck", x0, y0, x1, y1, G_TOP, U_FFL, M["floor"], "house_decks")
    # white balustrade: top rail + balusters on the three open sides
    bm = bmesh.new(); xa, xb, ya, yb = min(x0, x1), max(x0, x1), min(y0, y1), max(y0, y1)
    open_sides = [((xa, ya), (xb, ya)), ((xa, yb), (xb, yb))]
    open_sides.append(((xa, ya), (xa, yb)) if n == "master_balcony" else ((xb, ya), (xb, yb)))
    for (p, q) in open_sides:
        add_box(bm, min(p[0], q[0]) - 0.05, min(p[1], q[1]) - 0.05, max(p[0], q[0]) + 0.05, max(p[1], q[1]) + 0.05, U_FFL + 1.0, U_FFL + 1.08)
        add_box(bm, min(p[0], q[0]) - 0.03, min(p[1], q[1]) - 0.03, max(p[0], q[0]) + 0.03, max(p[1], q[1]) + 0.03, U_FFL + 0.08, U_FFL + 0.16)
        chippendale(bm, p, q, U_FFL + 0.16, U_FFL + 1.0)
    obj(n + "_balustrade", bm, M["trim"], "house_decks")
    for cx, cy in ((xa, ya), (xb, ya), (xa, yb), (xb, yb)):   # posts carrying the balcony roof, and the deck below
        box(n + "_post", cx - 0.12, cy - 0.12, cx + 0.12, cy + 0.12, 0, U_TOP, M["trim"], "house_decks")

# porthole window in the weatherboard wall north of the master balcony (listing photo 02)
px_, py_ = hw(685.5, 398)
bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=0.6, depth=0.12, location=(px_ - 0.08, py_, U_FFL + 1.55), rotation=(0, math.pi / 2, 0))
o = bpy.context.active_object; o.name = "porthole_glass"; o.data.materials.append(M["glass"])
bpy.ops.mesh.primitive_torus_add(major_radius=0.64, minor_radius=0.07, location=(px_ - 0.14, py_, U_FFL + 1.55), rotation=(0, math.pi / 2, 0))
o2 = bpy.context.active_object; o2.name = "porthole_frame"; o2.data.materials.append(M["trim"])
for ob in (o, o2):
    for c in ob.users_collection:
        c.objects.unlink(ob)
    col("house_upper").objects.link(ob)


# roofs
def hw_rect(a, b, c, d):
    (x0, y0), (x1, y1) = hw(a, b), hw(c, d); return x0, y0, x1, y1


hip("roof_upper_main", *hw_rect(685.5, 363, 971.75, 488), U_TOP, solar=(HX0 + 8, HX0 + 22))
hip("roof_upper_master", *hw_rect(704, 488, 769, 595), U_TOP)
hip("roof_upper_bed3", *hw_rect(769, 488, 858, 515.5), U_TOP)
hip("roof_master_balcony", *hw_rect(614.25, 433, 704.25, 525.5), U_TOP, pitch=22)
hip("roof_east_balcony", *hw_rect(971.75, 363, 996.75, 488), U_TOP, pitch=22)
hip("roof_ground_south", *hw_rect(670, 504, 844, 627.5), G_TOP, solar=(HX0 + 11, HX0 + 17))
hip("roof_verandah_west", *hw_rect(853.75, 325, 931.25, 362.5), G_TOP, pitch=18)
hip("roof_porch", *hw_rect(853.75, 490, 896.25, 512), G_TOP, pitch=18)
# outdoor entertaining: flat roof where the master balcony doesn't cover it, pyramid cupola over the north end
flat_roof("roof_outdoor_north", *hw_rect(608.75, 362.5, 686.25, 433), G_TOP)
flat_roof("roof_outdoor_south", *hw_rect(608.75, 525.5, 686.25, 585), G_TOP)
cx, cy = hw(647.5, 397.75); pyramid("roof_cupola", cx, cy, 2.9, G_TOP + 0.25, 2.6)
box("cupola_lantern", cx - 0.8, cy - 0.8, cx + 0.8, cy + 0.8, G_TOP + 2.2, G_TOP + 3.0, M["trim"], "house_roof")
pyramid("roof_cupola_cap", cx, cy, 1.0, G_TOP + 3.0, 0.9)
for (a, b) in ((608.75, 362.5), (608.75, 433), (608.75, 525.5), (608.75, 585), (686.25, 585)):
    x, y = hw(a, b); box("outdoor_post", x - 0.15, y - 0.15, x + 0.15, y + 0.15, 0, G_TOP, M["trim"], "house_decks")

# ------------------------------------------------------------------ guest house
GUEST_PX = [(1082.5, 323.75), (1301.25, 323.75), (1301.25, 410), (1082.5, 410)]
GP = [guest_w(*p) for p in GUEST_PX]
walls_from("guest", (1078, 320), guest_w, FFL, G_TOP, "guest_house", GP, "boards")
prism("guest_slab", GP, 0, FFL, M["floor"], "guest_house")
g = hip("roof_guest", -8.35, -3.3, 8.35, 3.3, G_TOP, pitch=25, collection="guest_house")
for o in list(col("guest_house").objects):
    if o.name.startswith("roof_guest"):
        o.location = (*GUEST_C, 0); o.rotation_euler = (0, 0, GUEST_ROT)

# ------------------------------------------------------------------ site
LOT = [site(772.8, 779.6), site(1177.4, 779.6), site(1249.9, 678.7), site(826.5, 710.6)]
prism("lot_lawn", LOT, -0.05, 0.0, M["lawn"], "site")
(wx0, wy0), (wx1, wy1) = LOT[0], LOT[3]
SHORE = [(-24, -60), (-6, -22), (0, 0), (18.5, 23.8), (28, 52), (32, 80), (33, 112)]   # lot shore extended along the canal bend


def shore_x(y):
    for (x0, y0), (x1, y1) in zip(SHORE, SHORE[1:]):
        if y0 <= y <= y1:
            return x0 + (x1 - x0) * (y - y0) / (y1 - y0)
    return SHORE[0][0] if y < SHORE[0][1] else SHORE[-1][0]


def offset_shore(dx):
    return [(x + dx, y) for x, y in SHORE]


prism("ground_beyond", offset_shore(-1.5) + [(230, 112), (230, -60)], -0.25, -0.06, M["lawn"], "site")
prism("canal_water", [(-120, -60)] + offset_shore(-3.5) + [(-120, 112)], -0.6, -0.55, M["water"], "site")
# rock revetment: a sloped strip from the lawn edge (z 0) down under the water (z -0.9), boulder-lumpy
bm = bmesh.new(); rows = []
for k, (dx, z) in enumerate(((0.6, 0.02), (-0.4, -0.15), (-1.4, -0.35), (-2.4, -0.6), (-3.6, -0.95))):
    rows.append([bm.verts.new((x, y, z)) for x, y in offset_shore(dx)])
for r0, r1 in zip(rows, rows[1:]):
    for i in range(len(SHORE) - 1):
        bm.faces.new((r0[i], r0[i + 1], r1[i + 1], r1[i]))
sw_o = obj("beach_sand", bm, M["sand"], "site")
sw_o.modifiers.new("sub", "SUBSURF").levels = 0; sw_o.modifiers["sub"].render_levels = 0
rm = sw_o.modifiers.new("remesh", "REMESH"); rm.mode = "VOXEL"; rm.voxel_size = 0.25
sol = sw_o.modifiers.new("solid", "SOLIDIFY"); sol.thickness = 0.3; sw_o.modifiers.move(2, 0)
dsp = sw_o.modifiers.new("boulders", "DISPLACE"); tx = bpy.data.textures.new("boulders", "VORONOI"); tx.noise_scale = 0.55
dsp.texture = tx; dsp.strength = 0.35; dsp.mid_level = 0.3
(wx0, wy0), (wx1, wy1) = LOT[0], LOT[3]
# jetty + pontoon + boat (drone c05/c06)
sx = shore_x(10.25)
box("jetty_walk", sx - 6, 9.6, sx + 0.5, 10.9, -0.15, 0.0, M["timber"], "site")
for k in range(5):
    box("jetty_pile", sx - 6 + k * 1.5 - 0.1, 9.45, sx - 6 + k * 1.5 + 0.1, 9.65, -1.0, 0.9, M["timber"], "site")
box("pontoon", sx - 18, 7.2, sx - 6, 10.9, -0.45, -0.22, M["timber"], "site")
# a 7 m centre-console boat moored alongside: tapered hull, white deck, console with a T-top
bx, by = sx - 16.5, 5.6
bm = bmesh.new()
add_quad_prism(bm, [(bx, by - 1.2), (bx + 5.4, by - 1.2), (bx + 7.2, by), (bx + 5.4, by + 1.2), (bx, by + 1.2)], -0.55, 0.15)
obj("boat_hull", bm, M["trim"], "site")
bm = bmesh.new()
add_quad_prism(bm, [(bx + 0.1, by - 1.1), (bx + 5.3, by - 1.1), (bx + 6.9, by), (bx + 5.3, by + 1.1), (bx + 0.1, by + 1.1)], 0.15, 0.2)
obj("boat_deck", bm, M["coping"], "site")
box("boat_stripe", bx, by - 1.21, bx + 5.4, by + 1.21, -0.1, 0.0, M["black"], "site")
box("boat_console", bx + 2.6, by - 0.45, bx + 3.4, by + 0.45, 0.2, 1.25, M["trim"], "site")
box("boat_screen", bx + 3.35, by - 0.45, bx + 3.45, by + 0.45, 1.25, 1.55, M["glass"], "site")
for dy in (-0.55, 0.55):
    box("boat_ttop_post", bx + 2.4, by + dy - 0.03, bx + 2.46, by + dy + 0.03, 0.2, 2.3, M["steel"], "site")
    box("boat_ttop_post", bx + 3.5, by + dy - 0.03, bx + 3.56, by + dy + 0.03, 0.2, 2.3, M["steel"], "site")
box("boat_ttop", bx + 2.2, by - 0.75, bx + 3.8, by + 0.75, 2.3, 2.36, M["cushion"], "site")
box("boat_engine", bx - 0.6, by - 0.35, bx, by + 0.35, -0.3, 0.75, M["black"], "site")
# pool (site plan), coping, surround with the step notch on the south side
box("pool_surround", 24.6, 14.2, 43.4, 24.8, -0.02, 0.09, M["pavers"], "site")
for (xa, ya, xb, yb) in ((26.6, 16.0, 42.0, 16.5), (26.6, 22.6, 42.0, 23.1), (26.6, 16.0, 27.2, 23.1), (41.4, 16.0, 42.0, 23.1)):
    box("pool_coping", xa, ya, xb, yb, 0.0, 0.12, M["coping"], "site")
box("pool_water", 27.2, 16.5, 41.4, 22.6, 0.0, 0.1, M["pool"], "site")
box("pool_step", 32.5, 15.2, 36.0, 16.6, 0.0, 0.1, M["coping"], "site")
# frameless glass fence along the pool's north (lawn) and west sides, spigots; three loungers on the north deck
for (xa, ya, xb, yb) in ((24.6, 24.8, 43.4, 24.8), (24.6, 14.2, 24.6, 24.8)):
    L = math.dist((xa, ya), (xb, yb)); k = int(L / 1.6)
    for i in range(k):
        t0, t1 = i / k, (i + 1) / k - 0.02 / L
        x0, y0 = xa + (xb - xa) * t0, ya + (yb - ya) * t0; x1, y1 = xa + (xb - xa) * t1, ya + (yb - ya) * t1
        box("pool_fence", x0 - 0.006, y0 - 0.006, x1 + 0.006, y1 + 0.006, 0.12, 1.32, M["fence"], "site")
        box("pool_spigot", x0 + (x1 - x0) * 0.2 - 0.03, y0 + (y1 - y0) * 0.2 - 0.03, x0 + (x1 - x0) * 0.2 + 0.03, y0 + (y1 - y0) * 0.2 + 0.03, 0.06, 0.3, M["steel"], "site")
for i in range(3):
    x = 31.0 + i * 1.0
    box("lounger_frame", x, 23.0, x + 0.7, 24.95 - 0.1, 0.06, 0.3, M["steel"], "site")
    box("lounger_cushion", x + 0.03, 23.05, x + 0.67, 24.4, 0.3, 0.38, M["cushion"], "site")
    bar(bm := bmesh.new(), (x + 0.35, 24.4), (x + 0.35, 24.85), 0, 0.38, 0.45, 0.85, 0.3); obj("lounger_back", bm, M["cushion"], "site")
# timber bench under the waterside tree, facing the water: the directed "looking out at the water" moment
BENCH = (shore_x(12.6) + 3.2, 12.6)
bm = bmesh.new()
for k in range(5):                                            # seat slats (along y), backrest slats, legs
    add_box(bm, BENCH[0] - 0.22 + k * 0.095, BENCH[1] - 0.9, BENCH[0] - 0.22 + k * 0.095 + 0.08, BENCH[1] + 0.9, 0.43, 0.46)
for k in range(3):
    add_box(bm, BENCH[0] + 0.25 + k * 0.02, BENCH[1] - 0.9, BENCH[0] + 0.28 + k * 0.02, BENCH[1] + 0.9, 0.55 + k * 0.13, 0.65 + k * 0.13)
for dy in (-0.8, 0.8):
    add_box(bm, BENCH[0] - 0.22, BENCH[1] + dy - 0.04, BENCH[0] + 0.25, BENCH[1] + dy + 0.04, 0.0, 0.43)
    add_box(bm, BENCH[0] + 0.24, BENCH[1] + dy - 0.04, BENCH[0] + 0.32, BENCH[1] + dy + 0.04, 0.0, 0.95)
obj("waterside_bench", bm, M["timber"], "site")
# fire pit + curved rendered seat wall near the water, the "bench looking at the water" spot (listing photo 05)
FP = (17.0, 7.0)
bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.55, depth=0.4, location=(*FP, 0.2))
fp = bpy.context.active_object; fp.name = "fire_pit"; fp.data.materials.append(M["black"])
for c in fp.users_collection:
    c.objects.unlink(fp)
col("site").objects.link(fp)
box("fire_pit_pad", FP[0] - 2.6, FP[1] - 2.6, FP[0] + 2.6, FP[1] + 2.6, -0.02, 0.09, M["pavers"], "site")
bm = bmesh.new()
for k in range(10):                                           # seat wall arc on the house side, facing the water
    a0, a1 = math.radians(-70 + k * 14), math.radians(-70 + (k + 1) * 14)
    r0, r1 = 2.0, 2.45
    pts = [(FP[0] + r0 * math.cos(a0), FP[1] + r0 * math.sin(a0)), (FP[0] + r1 * math.cos(a0), FP[1] + r1 * math.sin(a0)),
           (FP[0] + r1 * math.cos(a1), FP[1] + r1 * math.sin(a1)), (FP[0] + r0 * math.cos(a1), FP[1] + r0 * math.sin(a1))]
    add_quad_prism(bm, pts, 0, 0.45)
obj("seat_wall", bm, M["wall"], "site")
# driveway: street (SE corner) along the south boundary into the garage apron
drive = [(141, 2.6), (120, 3.3), (98, 4.3), (78, 5.6), (70, 7.0)]
bm = bmesh.new()
for (x0, y0), (x1, y1) in zip(drive, drive[1:]):
    dx, dy = x1 - x0, y1 - y0; L = math.hypot(dx, dy); nx, ny = -dy / L * 2.0, dx / L * 2.0
    add_quad_prism(bm, [(x0 + nx, y0 + ny), (x0 - nx, y0 - ny), (x1 - nx, y1 - ny), (x1 + nx, y1 + ny)], -0.02, 0.09)
obj("driveway", bm, M["drive"], "site")
box("garage_apron", 59.9, 1.9, 73.9, 12.4, -0.02, 0.09, M["drive"], "site")
# street + front wall with gate pillars and the 18 MARYLAND sign
(ex0, ey0), (ex1, ey1) = LOT[1], LOT[2]
ux, uy = (ex1 - ex0) / math.dist(LOT[1], LOT[2]), (ey1 - ey0) / math.dist(LOT[1], LOT[2])
prism("maryland_ave", [(ex0 + 1 - ux * 30, ey0 - uy * 30), (ex0 + 1 - ux * 30 + 12 * uy, ey0 - uy * 30 - 12 * ux), (ex1 + 1 + ux * 30 + 12 * uy, ey1 + uy * 30 - 12 * ux), (ex1 + 1 + ux * 30, ey1 + uy * 30)], -0.05, -0.02, M["road"], "street")
for t0, t1 in ((6.5, 18), (24, 40)):                         # wall either side of the 5.5 m gate opening
    pts = [(ex0 + ux * t0, ey0 + uy * t0), (ex0 + ux * t1, ey0 + uy * t1)]
    (a0, b0), (a1, b1) = pts
    prism("front_wall", [(a0, b0), (a1, b1), (a1 - 0.35, b1), (a0 - 0.35, b0)], 0, 1.9 if t0 > 7 else 2.3, M["stone"], "street")
    prism("front_hedge", [(a0 - 0.4, b0), (a1 - 0.4, b1), (a1 - 1.3, b1), (a0 - 1.3, b0)], 0, 1.4, M["hedge"], "street")
for t in (1.0, 6.5):
    x, y = ex0 + ux * t, ey0 + uy * t; box("gate_pillar", x - 0.6, y - 0.6, x + 0.6, y + 0.6, 0, 2.6, M["stone"], "street")
# white gate leaf, swung open inward off the south pillar (listing photo 01)
gx, gy = ex0 + ux * 1.6, ey0 + uy * 1.6; sw = math.radians(-168)   # swung fully open inward, flat along the south boundary
bm = bmesh.new()
for k in range(26):                                          # vertical slats + top/bottom rails
    add_box(bm, 0.05 + k * 0.175, -0.035, 0.05 + k * 0.175 + 0.13, 0.035, 0.12, 2.15)
add_box(bm, 0, -0.045, 4.6, 0.045, 0.1, 0.22); add_box(bm, 0, -0.045, 4.6, 0.045, 2.05, 2.2)
g = obj("gate_leaf", bm, M["trim"], "street")
g.location = (gx - 0.6, gy, 0); g.rotation_euler = (0, 0, sw)
# "18 MARYLAND" in dark metal letters on the street face of the sign wall, north of the gate
cu = bpy.data.curves.new("sign", "FONT"); cu.body = "18 MARYLAND"; cu.size = 0.42; cu.extrude = 0.015; cu.align_x = "CENTER"
so = bpy.data.objects.new("sign_18_maryland", cu); col("street").objects.link(so); so.data.materials.append(M["black"])
tx, ty = ex0 + ux * 10.5, ey0 + uy * 10.5
so.location = (tx + 0.02, ty, 1.15); so.rotation_euler = (math.pi / 2, 0, math.atan2(uy, ux))
# flagpole on the front lawn (listing photos 01/06)
bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.05, depth=8.0, location=(77.0, 10.0, 4.0))
fl = bpy.context.active_object; fl.name = "flagpole"; fl.data.materials.append(M["trim"])
for c in fl.users_collection:
    c.objects.unlink(fl)
col("site").objects.link(fl)
# boundary hedges (tall, both sides) + neighbours
box("hedge_south", 12, -1.6, 140, -0.2, 0, 3.2, M["hedge"], "site")
box("hedge_north", 22, 31.2, 150, 33.0, 0, 4.0, M["hedge"], "site")
NEIGH = [(30, -22, 52, -6, M["terracotta"]), (62, -20, 82, -5, M["terracotta"]), (32, 36, 56, 52, M["roof"]), (70, 38, 92, 54, M["roof"])]
for i, (x0, y0, x1, y1, rm) in enumerate(NEIGH):
    box(f"neighbour_{i}", x0, y0, x1, y1, 0, 6.0, M["neigh"], "neighbours")
    for z0 in (0.4, 3.6):                                    # a few big openings per side so they read as houses
        for k in range(5):
            t = 2.5 + k * 5.5; wm = M["glass_lit"] if (i + k + int(z0)) % 3 == 0 else M["glass_dark"]
            hz = 2.4 if z0 < 1 else 1.6
            if x0 + t + 2.6 < x1 - 1.5:
                for yy in (y0 - 0.03, y1):
                    box(f"neighbour_{i}_glass", x0 + t, yy, x0 + t + 2.6, yy + 0.03, z0, z0 + hz, wm, "neighbours")
            if y0 + t + 2.6 < y1 - 1.5:
                for xx in (x0 - 0.03, x1):
                    box(f"neighbour_{i}_glass", xx, y0 + t, xx + 0.03, y0 + t + 2.6, z0, z0 + hz, wm, "neighbours")
    hip(f"neighbour_{i}_roof", x0, y0, x1, y1, 6.0, collection="neighbours", material=rm)


# ------------------------------------------------------------------ trees + palms + lawn + water (landscape.py)
exec(open(os.path.join(HERE, "landscape.py")).read())

# neighbour lots dressed like the drone aerial (photo 03): a pool on the water side, canopy trees, a palm or two
for i, (x0, y0, x1, y1, rm) in enumerate(NEIGH):
    cy = (y0 + y1) / 2; px0 = max(x0 - 12, shore_x(cy) + 5)
    box(f"neighbour_{i}_pool_surround", px0 - 1, cy - 4, px0 + 10, cy + 4, -0.06, 0.04, M["pavers"], "neighbours")
    box(f"neighbour_{i}_pool", px0, cy - 2.5, px0 + 9, cy + 2.5, -0.06, 0.06, M["pool"], "neighbours")
    for k, (tx, ty) in enumerate(((x1 + 8, y0 + 2), (x1 + 14, y1 - 3), (x0 - 22, y0 + 1))):
        tree(f"neighbour_{i}_tree{k}", max(tx, shore_x(ty) + 3), ty, 4, 7 + 2 * k)
    palm(f"neighbour_{i}_palm", px0 - 3, cy + 5, 12)


for i, (x, y) in enumerate([(119.2, 26.8), (129, 26), (138, 29.2), (137.7, 22.2), (146.2, 28.2), (155.5, 30.5)]):
    tree(f"fig_{i}", x, y, 5.0, 9.0)
for i in range(7):                                           # weeping-fig row on the north boundary (photo 06)
    tree(f"fig_row_{i}", 100 + i * 2.8, 31.0 + (i % 2) * 0.6, 3.6, 13.0)
for i, (x, y) in enumerate([(16, 15.8), (13.2, 10.6), (4.5, 2.1), (9.5, 2.8), (14.5, 2.1)]):
    tree(f"waterside_tree_{i}", max(x, shore_x(y) + 3.0), y, 3.2, 6.0)
for i, (x, y, h) in enumerate([(22.5, 27, 12), (24.5, 29.5, 14), (6.5, 6.5, 11), (19.5, 21.5, 13), (22, 4, 10), (48, 29, 12), (75, 30, 11)]):
    palm(f"palm_{i}", max(x, shore_x(y) + 2.5), y, h)
for i in range(14):                                          # hedge-line shrubs + garden beds by the house
    x = 46 + i * 2.1; shrub(f"shrub_{i}", x, 29.6, 0.8, 1.1)
plant_hedges()
def _seg_d(p, a, c):
    ax, ay = a; bx_, by_ = c; dx, dy = bx_ - ax, by_ - ay
    t = max(0, min(1, ((p[0] - ax) * dx + (p[1] - ay) * dy) / (dx * dx + dy * dy)))
    return math.hypot(p[0] - ax - t * dx, p[1] - ay - t * dy)


HARD = [(24.4, 14.0, 43.6, 25.0), (59.7, 1.7, 74.1, 12.6), (FP[0] - 2.8, FP[1] - 2.8, FP[0] + 2.8, FP[1] + 2.8)]
HARD += [(min(hw(a_, b_)[0], hw(c_, d_)[0]) - 0.3, min(hw(a_, b_)[1], hw(c_, d_)[1]) - 0.3,
          max(hw(a_, b_)[0], hw(c_, d_)[0]) + 0.3, max(hw(a_, b_)[1], hw(c_, d_)[1]) + 0.3) for a_, b_, c_, d_ in DECKS.values()]


def lawn_keep(x, y):
    if inside(G_POLY, (x, y)) or inside(GP, (x, y)):
        return False
    if any(xa <= x <= xb and ya <= y <= yb for xa, ya, xb, yb in HARD):
        return False
    return min(_seg_d((x, y), a_, c_) for a_, c_ in zip(drive, drive[1:])) > 2.3


lawn_grass(LOT, lawn_keep)
water_material()
far_bank()
horizon()
bury_protos()

# ------------------------------------------------------------------ interior (furniture, kitchen, lights)
M["glass"] = shadow_clear(M["glass"])
exec(open(os.path.join(HERE, "interior.py")).read())

# ------------------------------------------------------------------ light, cameras, render
w = bpy.data.worlds.new("sky"); sc.world = w; w.use_nodes = True
bgn = next(n for n in w.node_tree.nodes if n.type == "BACKGROUND")
hdr = os.path.join(HERE, "..", "sky-library", "hdr_2k", arg("--sky", "kloofendal_48d_partly_cloudy_puresky") + ".hdr")
if os.path.exists(hdr):
    env = w.node_tree.nodes.new("ShaderNodeTexEnvironment"); env.image = bpy.data.images.load(hdr)
    w.node_tree.links.new(env.outputs[0], bgn.inputs[0])
sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun", "SUN")); sc.collection.objects.link(sun)
sun.data.energy = 3.5; sun.rotation_euler = (math.radians(45), 0, math.radians(-60))

CAMS = {   # name: location, look-at, lens
    "top_down": ((70, 15, 160), (70, 15, 0), 35),
    "street_gate": ((145.8, 3.7, 1.6), (75, 12, 4), 28),
    "water_aerial": ((-12, -2, 22), (55, 18, 3), 28),
    "lawn_house": ((24, 10, 1.6), (60, 15, 4.5), 24),
}
for n, (loc, at, lens) in CAMS.items():
    cd = bpy.data.cameras.new(n); cd.lens = lens; cd.clip_end = 1000
    c = bpy.data.objects.new("cam_" + n, cd); sc.collection.objects.link(c); c.location = loc
    c.rotation_euler = (Vector(at) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()

os.makedirs(os.path.join(HERE, "qc"), exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HERE, "maryland.blend"))
print("objects", len(bpy.data.objects))
if "--render" in argv:
    sc.render.engine = "CYCLES"
    p = bpy.context.preferences.addons["cycles"].preferences; p.compute_device_type = "METAL"; p.get_devices()
    for d in p.devices:
        d.use = True
    sc.cycles.device = "GPU"; sc.cycles.samples = int(arg("--samples", 32)); sc.cycles.use_denoising = True
    sc.render.resolution_x, sc.render.resolution_y = 1920, 1080; sc.render.resolution_percentage = int(arg("--res", 50))
    sc.view_settings.view_transform = "AgX"
    for n in CAMS:
        sc.camera = bpy.data.objects["cam_" + n]; sc.render.filepath = os.path.join(HERE, "qc", n + ".png")
        bpy.ops.render.render(write_still=True)
print("BUILD_OK")
