"""18 Maryland interior: furniture, kitchen, rugs, beds and interior lights. exec'd by build.py (shares its namespace).

Room positions come from the Kollosche floor plan (ground-plan px, `hw`); upper-level rooms are given in the upper
drawing's own px and shifted by UP_D onto the ground plan. Style from the listing photos: dark timber floors downstairs,
charcoal carpet upstairs, white shaker kitchen with white stone island + rattan dome pendants, white/linen
upholstery, black-and-white patterned rugs, Persian rug by the kitchen.

Every placed piece is registered in PLACED with its footprint, its front direction and what it must face. review.py
reads layout.json and fails any piece whose front doesn't point at its target, that sits in a wall, overlaps another
piece, blocks an opening, or (beds) lacks its headboard wall or a bedside on either side.

Poly Haven assets face -Y natively (checked with tools/calibrate_assets.py, qc/calib_front.png).
"""
import json

ASSETS = os.path.join(HERE, "assets")
UP_D = (-352.0, -82.0)                           # upper drawing px -> ground plan px
LIB = {}
PLACED = []
LINEN = (0.78, 0.75, 0.7)


def U(px, py):
    """upper-drawing px -> world xy"""
    return hw(px + UP_D[0], py + UP_D[1])


def lib(aid, recolor=None):
    """import an asset once (joined into one mesh, origin bottom-centre), kept out of the scene; recolor tints fabric"""
    key = (aid, recolor)
    if key in LIB:
        return LIB[key]
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=os.path.join(ASSETS, aid, aid + ".gltf"))
    new = [o for o in bpy.data.objects if o not in before]
    meshes = [o for o in new if o.type == "MESH"]
    for o in meshes:                                     # bake hierarchy transforms into the mesh
        mw = o.matrix_world.copy(); o.parent = None; o.data = o.data.copy(); o.data.transform(mw); o.matrix_world.identity()
    for o in new:
        if o.type != "MESH":
            bpy.data.objects.remove(o)
    base = meshes[0]
    if len(meshes) > 1:
        with bpy.context.temp_override(active_object=base, selected_editable_objects=meshes, selected_objects=meshes):
            bpy.ops.object.join()
    pts = [Vector(v.co) for v in base.data.vertices]
    lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    from mathutils import Matrix
    base.data.transform(Matrix.Translation(-Vector(((lo.x + hi.x) / 2, (lo.y + hi.y) / 2, lo.z if aid not in HANGING else hi.z))))
    if recolor:
        base.data = base.data.copy()
        for i, m in enumerate(base.data.materials):
            m2 = m.copy(); nt = m2.node_tree; b = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
            if not any(k in m.name.lower() for k in ("wood", "leg", "metal", "frame", "foot", "feet")):
                for l in list(b.inputs["Base Color"].links):
                    nt.links.remove(l)
                b.inputs["Base Color"].default_value = (*recolor, 1)
            base.data.materials[i] = m2
    for c in base.users_collection:
        c.objects.unlink(base)
    base.name = "LIB_" + aid
    LIB[key] = (base, hi - lo)
    return LIB[key]


HANGING = {"Chandelier_03", "ceiling_fan"}


def yaw_for(front):
    """rotation that turns the native -Y front to face `front` (xy vector)"""
    return math.atan2(front[1], front[0]) + math.pi / 2


def register(name, kind, at, front, size, room, target=None, wall=False, level="ground", z=0.0):
    PLACED.append(dict(name=name, kind=kind, at=list(at)[:2], front=list(front)[:2], size=list(size), room=room,
                       target=list(target)[:2] if target else None, wall=wall, level=level, z=z))


def place(aid, at, face, room, kind="seat", wall=False, level="ground", recolor=None, z=None, scale=1.0, check=True):
    """face: a target point (x, y) the front must look at, or a direction vector given as ('dir', dx, dy)"""
    src, dims = lib(aid, recolor)
    if face[0] == "dir":
        front = Vector((face[1], face[2], 0)).normalized(); target = None
    else:
        front = (Vector((face[0], face[1], 0)) - Vector((at[0], at[1], 0))).normalized(); target = face
    zz = z if z is not None else (FFL if level == "ground" else U_FFL)
    o = src.copy(); o.name = f"{room}_{aid}"; col("interior_" + level).objects.link(o)
    o.location = (at[0], at[1], zz); o.rotation_euler = (0, 0, yaw_for(front)); o.scale = (scale,) * 3
    if check:
        register(o.name, kind, at, front, (dims.x * scale, dims.y * scale, dims.z * scale), room, target, wall, level, zz)
    return o


def proc(name, at, front, size, room, kind, level="ground", target=None, wall=False, z=None):
    register(name, kind, at, front, size, room, target, wall, level, z if z is not None else (FFL if level == "ground" else U_FFL))


def wall_hit(pt, d, level, maxd=4.0):
    """distance along unit xy vector d from pt to the first wall rect of `level` (slab-method ray/box), or None"""
    best = None
    for lv, xa, ya, xb, yb in WALLS:
        if lv != level:
            continue
        t0, t1 = 0.0, maxd
        for o, dd, lo, hi in ((pt[0], d[0], xa, xb), (pt[1], d[1], ya, yb)):
            if abs(dd) < 1e-9:
                if not lo <= o <= hi:
                    t0, t1 = 1, 0
                continue
            a, b = (lo - o) / dd, (hi - o) / dd
            t0, t1 = max(t0, min(a, b)), min(t1, max(a, b))
        if t0 <= t1 and (best is None or t0 < best):
            best = t0
    return best


def against(pt, front, depth, level="ground", gap=0.03):
    """centre point for a piece of `depth` whose back sits on the wall behind pt (behind = -front)"""
    b = Vector((-front[0], -front[1], 0)).normalized(); t = wall_hit(pt, b, level)
    if t is None:
        print("WARN no wall behind", pt); return Vector(pt[:2])
    return Vector(pt[:2]) + b.xy * (t - depth / 2 - gap)


# ------------------------------------------------------------------ materials
MI = dict(
    cab=mat("Cabinet_shaker_white", (0.86, 0.86, 0.84), 0.35),
    stone=textured(mat("Stone_benchtop_white", (0.9, 0.9, 0.88), 0.12), "noise", 6, 0.02,
                   ramp=((0.84, 0.84, 0.83), (0.93, 0.93, 0.92))),
    rattan=textured(mat("Rattan_pendant", (0.45, 0.3, 0.16), 0.8), "noise", 60, 0.8, ramp=((0.25, 0.15, 0.07), (0.55, 0.38, 0.2))),
    linen=textured(mat("Linen_bedding_white", (0.85, 0.84, 0.8), 0.9), "noise", 80, 0.15),
    linen_grey=textured(mat("Linen_bedding_grey", (0.42, 0.42, 0.42), 0.9), "noise", 80, 0.15),
    linen_sand=textured(mat("Linen_bedding_sand", (0.62, 0.55, 0.45), 0.9), "noise", 80, 0.15),
    boucle=textured(mat("Boucle_headboard_ivory", (0.8, 0.77, 0.72), 1.0), "noise", 120, 0.6),
    velvet=textured(mat("Velvet_headboard_charcoal", (0.08, 0.08, 0.09), 0.7), "noise", 120, 0.3),
    throw=textured(mat("Knit_throw_charcoal", (0.1, 0.1, 0.1), 1.0), "noise", 40, 0.6),
    throw_tan=textured(mat("Knit_throw_tan", (0.45, 0.32, 0.2), 1.0), "noise", 40, 0.6),
    rug_bw=textured(mat("Rug_black_white", (0.5, 0.5, 0.5), 1.0), "noise", 3, 0.2, ramp=((0.05, 0.05, 0.05), (0.85, 0.83, 0.8))),
    rug_persian=textured(mat("Rug_persian_red", (0.35, 0.06, 0.05), 1.0), "noise", 4, 0.2, ramp=((0.25, 0.03, 0.03), (0.55, 0.32, 0.22))),
    rug_jute=textured(mat("Rug_jute", (0.55, 0.45, 0.3), 1.0), "noise", 90, 0.5),
    tv=mat("TV_screen_black", (0.01, 0.01, 0.012), 0.08),
    bulb=mat("Pendant_bulb_warm", (1.0, 0.75, 0.45), 0.5, emit=6.0),
    fireplace=mat("Fireplace_surround_white", (0.88, 0.87, 0.84), 0.5),
    firebox=mat("Firebox_black", (0.02, 0.02, 0.02), 0.6),
)


def slab(name, x0, y0, x1, y1, z0, z1, m, level="interior_ground"):
    return box(name, x0, y0, x1, y1, z0, z1, m, level)


def rug(name, c, w, d, m, level="ground"):
    z = FFL if level == "ground" else U_FFL
    slab(name, c[0] - w / 2, c[1] - d / 2, c[0] + w / 2, c[1] + d / 2, z, z + 0.012, m, "interior_" + level)


def bed(name, head_mid, front, room, style, level="upper"):
    """king bed (2.03 x 2.15) + upholstered headboard, styled per room so no two beds are dressed alike.
    head_mid: the point on the headboard wall where the bed's centre line meets it; front: direction toward the foot"""
    f = Vector((front[0], front[1], 0)).normalized(); s = Vector((-f.y, f.x, 0))
    t = wall_hit(head_mid, (-f.x, -f.y), level)
    hm = Vector((head_mid[0], head_mid[1], 0)) - f * ((t or 0.0) - 0.0)
    W, L = 2.03, 2.15; z = U_FFL if level == "upper" else FFL
    cen = hm + f * (0.1 + L / 2)
    parts = bmesh.new()

    def obox(bm_, c, along, across, z0, z1):       # oriented box: `along` metres along f, `across` along s
        pts = [c + f * a + s * b for a, b in ((-along / 2, -across / 2), (along / 2, -across / 2), (along / 2, across / 2), (-along / 2, across / 2))]
        add_quad_prism(bm_, [(p.x, p.y) for p in pts], z0, z1)

    hb_m, cover_m, accent_m, throw_m = style
    head = bmesh.new(); obox(head, hm + f * 0.06, 0.1, W + 0.3, z, z + 1.35); obj(name + "_headboard", head, MI[hb_m], "interior_" + level)
    base = bmesh.new(); obox(base, cen, L, W, z + 0.05, z + 0.38); obj(name + "_base", base, MI[hb_m], "interior_" + level)
    mat_ = bmesh.new(); obox(mat_, cen, L - 0.04, W - 0.04, z + 0.38, z + 0.62); o = obj(name + "_mattress", mat_, MI["linen"], "interior_" + level)
    cov = bmesh.new(); obox(cov, cen + f * 0.25, L - 0.55, W + 0.1, z + 0.36, z + 0.66); o = obj(name + "_duvet", cov, MI[cover_m], "interior_" + level)
    bv = o.modifiers.new("soft", "BEVEL"); bv.width = 0.05; bv.segments = 4
    thr = bmesh.new(); obox(thr, cen + f * (L / 2 - 0.35), 0.5, W + 0.14, z + 0.36, z + 0.68); o = obj(name + "_throw", thr, MI[throw_m], "interior_" + level)
    bv = o.modifiers.new("soft", "BEVEL"); bv.width = 0.04; bv.segments = 3
    for k, (off, m_, h_, t_) in enumerate(((-0.5, "linen", 0.62, 0.16), (0.5, "linen", 0.62, 0.16),
                                           (-0.48, accent_m, 0.5, 0.15), (0.48, accent_m, 0.5, 0.15), (0.0, accent_m, 0.4, 0.13))):
        along = 0.22 + (0.15 if k >= 2 else 0) + (0.12 if k == 4 else 0)
        p = bmesh.new(); obox(p, hm + f * along + s * off, t_, 0.62 if k < 4 else 0.5, z + 0.62, z + 0.62 + h_)
        o = obj(f"{name}_pillow{k}", p, MI[m_], "interior_" + level)
        bv = o.modifiers.new("soft", "BEVEL"); bv.width = 0.06; bv.segments = 4
        o.rotation_euler = (0, 0, 0)
    register(name, "bed", (cen.x, cen.y), (f.x, f.y), (W + 0.3, L + 0.2, 1.35), room, None, True, level, z)
    # bedsides both sides, lamps on both
    for side in (-1, 1):
        c = hm + f * 0.35 + s * side * (W / 2 + 0.42)
        place("ClassicNightstand_01" if style[0] != "velvet" else "side_table_01", (c.x, c.y), ("dir", f.x, f.y), room,
              kind="bedside", wall=True, level=level, recolor=(0.88, 0.87, 0.84))
        lamp(f"{name}_lamp{side}", (c.x, c.y), z + 0.7, level)
    return cen


def lamp(name, at, z, level):
    bpy.ops.mesh.primitive_cone_add(vertices=24, radius1=0.2, radius2=0.14, depth=0.26, location=(at[0], at[1], z + 0.48))
    sh = bpy.context.active_object; sh.name = name + "_shade"; sh.data.materials.append(MI["linen"])
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.07, depth=0.34, location=(at[0], at[1], z + 0.17))
    bs = bpy.context.active_object; bs.name = name + "_base"; bs.data.materials.append(MI["stone"])
    for ob in (sh, bs):
        for c in ob.users_collection:
            c.objects.unlink(ob)
        col("interior_" + level).objects.link(ob)
    L = bpy.data.lights.new(name, "POINT"); L.energy = 18; L.color = (1.0, 0.78, 0.55); L.shadow_soft_size = 0.12
    lo = bpy.data.objects.new(name, L); col("interior_lights").objects.link(lo); lo.location = (at[0], at[1], z + 0.45)


def pendant(name, at, z_top, r=0.32, drop=0.9, level="ground"):
    """rattan dome pendant (kitchen island, listing photos 08/09/15)"""
    zc = z_top - drop
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=r, location=(at[0], at[1], zc))
    o = bpy.context.active_object; o.name = name
    bm_ = bmesh.new(); bm_.from_mesh(o.data)
    bmesh.ops.delete(bm_, geom=[v for v in bm_.verts if v.co.z < -0.02], context="VERTS"); bm_.to_mesh(o.data); bm_.free()
    o.modifiers.new("shell", "SOLIDIFY").thickness = 0.015
    o.data.materials.append(MI["rattan"])
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.006, depth=drop - r, location=(at[0], at[1], z_top - (drop - r) / 2))
    cord = bpy.context.active_object; cord.name = name + "_cord"; cord.data.materials.append(M["black"])
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.06, location=(at[0], at[1], zc + 0.05))
    bulb = bpy.context.active_object; bulb.name = name + "_bulb"; bulb.data.materials.append(MI["bulb"])
    for ob in (o, cord, bulb):
        for c in ob.users_collection:
            c.objects.unlink(ob)
        col("interior_" + level).objects.link(ob)
    L = bpy.data.lights.new(name + "_l", "POINT"); L.energy = 40; L.color = (1.0, 0.8, 0.58); L.shadow_soft_size = 0.1
    lo = bpy.data.objects.new(name + "_l", L); col("interior_lights").objects.link(lo); lo.location = (at[0], at[1], zc - 0.02)


def downlights(room, x0, y0, x1, y1, z, nx, ny, energy=60):
    """recessed ceiling downlights as soft area lights (warm 3000 K) + the visible trim discs"""
    for i in range(nx):
        for j in range(ny):
            x = x0 + (x1 - x0) * (i + 0.5) / nx; y = y0 + (y1 - y0) * (j + 0.5) / ny
            L = bpy.data.lights.new(f"{room}_dl{i}{j}", "AREA"); L.shape = "DISK"; L.size = 0.12; L.energy = energy
            L.color = (1.0, 0.83, 0.65); lo = bpy.data.objects.new(L.name, L); col("interior_lights").objects.link(lo)
            lo.location = (x, y, z - 0.03)
            slab(f"{room}_dl_trim{i}{j}", x - 0.06, y - 0.06, x + 0.06, y + 0.06, z - 0.025, z - 0.02, MI["bulb"], "interior_lights")


def rect_px(a, b, c, d, f=hw):
    (x0, y0), (x1, y1) = f(a, b), f(c, d)
    return min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)


# ================================================================== GROUND
GZ = FFL
# ---- lounge: sofa faces the fireplace on the north wall (plan px 720-745, 362)
fp = Vector(hw(733, 366))
slab("lounge_fireplace_surround", fp.x - 1.0, fp.y - 0.45, fp.x + 1.0, fp.y, GZ, GZ + 1.25, MI["fireplace"])
slab("lounge_firebox", fp.x - 0.45, fp.y - 0.47, fp.x + 0.45, fp.y - 0.4, GZ + 0.2, GZ + 0.85, MI["firebox"])
slab("lounge_mantel", fp.x - 1.15, fp.y - 0.55, fp.x + 1.15, fp.y, GZ + 1.25, GZ + 1.32, MI["fireplace"])
fire = bpy.data.lights.new("fire_glow", "AREA"); fire.size = 0.6; fire.energy = 30; fire.color = (1.0, 0.45, 0.15)
fo = bpy.data.objects.new("fire_glow", fire); col("interior_lights").objects.link(fo); fo.location = (fp.x, fp.y - 0.5, GZ + 0.45)
fo.rotation_euler = (math.radians(90), 0, 0)
ct = Vector((fp.x, fp.y - 3.0))
rug("lounge_rug", (ct.x, ct.y - 0.2), 3.6, 2.8, MI["rug_bw"])
place("CoffeeTable_01", ct, ("dir", 0, 1), "lounge", kind="table", recolor=None)
place("sofa_03", (ct.x, ct.y - 1.55), (fp.x, fp.y), "lounge", recolor=LINEN)
place("ArmChair_01", (ct.x - 1.75, ct.y + 0.1), (ct.x, ct.y + 0.1), "lounge", recolor=(0.2, 0.2, 0.2))
place("ArmChair_01", (ct.x + 1.75, ct.y + 0.1), (ct.x, ct.y + 0.1), "lounge", recolor=(0.2, 0.2, 0.2))
for sx in (-1.65, 1.65):
    place("side_table_tall_01", (ct.x + sx, ct.y - 1.55), ("dir", 0, 1), "lounge", kind="decor")
place("potted_plant_01", (fp.x + 1.6, fp.y - 0.45), ("dir", 0, -1), "lounge", kind="decor")
place("ceramic_vase_01", (fp.x - 0.7, fp.y - 0.25), ("dir", 0, -1), "lounge", kind="decor", z=GZ + 1.32, check=False)
downlights("lounge", *rect_px(702, 372, 778, 465), G_TOP, 2, 3)

# ---- dining (plan px 782-822, 365-430): table long axis north-south, chairs face the table
dc = Vector(hw(802, 397))
rug("dining_rug", dc, 2.4, 3.4, MI["rug_jute"])
place("dining_table", dc, ("dir", 1, 0), "dining", kind="table")
for dy in (-0.7, 0.0, 0.7):
    for sx in (-1, 1):
        place("dining_chair_02", (dc.x + sx * 0.92, dc.y + dy), (dc.x, dc.y + dy), "dining")
for sy in (-1, 1):
    place("dining_chair_02", (dc.x, dc.y + sy * 1.45), (dc.x, dc.y), "dining")
place("Chandelier_03", dc, ("dir", 0, -1), "dining", kind="hanging", z=G_TOP - 0.05, check=False)

# ---- kitchen: island (plan px 765-812, 468-480), stools on the north side facing it, shaker run on the south wall
ic = Vector(hw(788.5, 474)); IW, ID, IH = 3.6, 1.05, 0.92
slab("kitchen_island_body", ic.x - IW / 2 + 0.05, ic.y - ID / 2 + 0.05, ic.x + IW / 2 - 0.05, ic.y + ID / 2 - 0.05, GZ, GZ + IH - 0.04, MI["cab"])
slab("kitchen_island_top", ic.x - IW / 2, ic.y - ID / 2, ic.x + IW / 2, ic.y + ID / 2, GZ + IH - 0.04, GZ + IH, MI["stone"])
for sx in (-1, 1):                                                   # waterfall ends
    slab("kitchen_island_waterfall", ic.x + sx * IW / 2 - (0.04 if sx > 0 else 0), ic.y - ID / 2, ic.x + sx * IW / 2 + (0 if sx > 0 else 0.04), ic.y + ID / 2, GZ, GZ + IH, MI["stone"])
for k in range(6):                                                   # shaker door grooves on the kitchen side
    x = ic.x - IW / 2 + 0.3 + k * (IW - 0.6) / 5
    slab("kitchen_island_groove", x - 0.004, ic.y - ID / 2 + 0.045, x + 0.004, ic.y - ID / 2 + 0.05, GZ + 0.1, GZ + IH - 0.1, M["black"])
proc("kitchen_island", (ic.x, ic.y), (0, 1), (IW, ID, IH), "kitchen", "fixture")
for dx in (-1.2, -0.4, 0.4, 1.2):
    place("bar_chair_round_01", (ic.x + dx, ic.y + ID / 2 + 0.38), (ic.x + dx, ic.y), "kitchen", kind="stool")
for dx in (-0.85, 0.85):
    pendant(f"kitchen_pendant{'LR'[dx > 0]}", (ic.x + dx, ic.y), G_TOP, r=0.34, drop=1.05)
kx0, _, kx1, _ = rect_px(742, 497, 822, 505)                          # back run against the south wall
kc = against(hw(782, 495), (0, 1), 0.65); ky0, ky1 = kc.y - 0.325, kc.y + 0.325
ky0, ky1 = ky1, ky0                                                    # ky0 = room-side face (north), ky1 = wall side
slab("kitchen_back_run", kx0, ky1, kx1, ky0 - 0.02, GZ, GZ + 0.88, MI["cab"])
slab("kitchen_back_top", kx0, ky1, kx1, ky0, GZ + 0.88, GZ + 0.92, MI["stone"])
slab("kitchen_splashback", kx0, ky1, kx1, ky1 + 0.02, GZ + 0.92, GZ + 1.5, MI["stone"])
slab("kitchen_uppers", kx0, ky1, kx1, ky1 + 0.36, GZ + 1.55, G_TOP - 0.05, MI["cab"])
slab("kitchen_rangehood", (kx0 + kx1) / 2 - 0.5, ky1, (kx0 + kx1) / 2 + 0.5, ky1 + 0.5, GZ + 1.55, GZ + 2.0, M["steel"])
slab("kitchen_cooktop", (kx0 + kx1) / 2 - 0.45, ky1 + 0.05, (kx0 + kx1) / 2 + 0.45, ky0 - 0.05, GZ + 0.92, GZ + 0.93, M["black"])
proc("kitchen_back_run", (kc.x, kc.y), (0, 1), (kx1 - kx0, 0.65, 0.92), "kitchen", "fixture", wall=True)
rug("kitchen_rug", (ic.x, ic.y + 1.4), 3.0, 1.0, MI["rug_persian"])
downlights("kitchen", *rect_px(742, 466, 822, 498), G_TOP, 3, 1, 45)

# ---- meals (plan px 700-760, 470-505): round table + four chairs facing it
mc = Vector(hw(722, 485))
place("round_wooden_table_02", mc, ("dir", 0, 1), "meals", kind="table")
for a in (45, 135, 225, 315):
    p = Vector((mc.x + math.cos(math.radians(a)) * 0.8, mc.y + math.sin(math.radians(a)) * 0.8))
    place("gallinera_chair", p, (mc.x, mc.y), "meals")
place("potted_plant_02", hw(706, 470), ("dir", 1, 0), "meals", kind="decor")

# ---- family / entertaining (plan px 672-733, 510-583): sofa faces the TV unit on the south wall
tvc = against(hw(688, 512), (0, -1), 0.52)
place("modern_wooden_cabinet", tvc, ("dir", 0, -1), "family", kind="fixture", wall=True, recolor=(0.86, 0.86, 0.84))
wy = tvc.y + 0.26 + 0.03
slab("family_tv", tvc.x - 0.85, wy - 0.05, tvc.x + 0.85, wy, GZ + 1.05, GZ + 2.0, MI["tv"])
proc("family_tv", (tvc.x, wy - 0.025), (0, -1), (1.7, 0.05, 0.95), "family", "decor", z=GZ + 1.05)
fc = Vector((tvc.x, tvc.y - 2.9))
rug("family_rug", (fc.x, fc.y + 1.1), 3.2, 2.6, MI["rug_bw"])
place("modern_coffee_table_02", (fc.x, fc.y + 1.3), ("dir", 0, 1), "family", kind="table")
place("sofa_03", fc, (tvc.x, tvc.y), "family", recolor=LINEN)
place("modern_arm_chair_01", (fc.x + 1.85, fc.y + 1.3), (fc.x, fc.y + 1.3), "family", recolor=(0.75, 0.72, 0.66))
downlights("family", *rect_px(674, 512, 731, 581), G_TOP, 2, 2)
# bar counter (plan px 735-760, 528-570) + stools on the room side facing it
bx0, by0, bx1, by1 = rect_px(738, 530, 752, 568)
slab("bar_counter", bx0, by0, bx1, by1, GZ, GZ + 1.05, MI["cab"]); slab("bar_top", bx0 - 0.08, by0, bx1, by1, GZ + 1.05, GZ + 1.09, MI["stone"])
proc("bar_counter", ((bx0 + bx1) / 2, (by0 + by1) / 2), (-1, 0), (by1 - by0, bx1 - bx0 + 0.08, 1.09), "family", "fixture")
for t in (0.25, 0.5, 0.75):
    y = by0 + (by1 - by0) * t
    place("bar_chair_round_01", (bx0 - 0.42, y), (bx0, y), "family", kind="stool")

# ---- office (plan px 672-738, 588-627): desk on the south wall, chair faces the desk
oc = against(hw(705, 615), (0, 1), 0.59)
place("ClassicConsole_01", oc, ("dir", 0, 1), "office", kind="fixture", wall=True)
place("gallinera_chair", (oc.x, oc.y + 0.75), (oc.x, oc.y), "office")
downlights("office", *rect_px(674, 590, 736, 625), G_TOP, 2, 1)

# ---- media (plan px 908-972, 405-490): sofa faces the TV on the south wall
tc_ = against(hw(940, 480), (0, 1), 0.52)
place("modern_wooden_cabinet", tc_, ("dir", 0, 1), "media", kind="fixture", wall=True, recolor=(0.12, 0.1, 0.09))
tm = Vector((tc_.x, tc_.y - 0.29))
slab("media_tv", tm.x - 1.1, tm.y, tm.x + 1.1, tm.y + 0.05, GZ + 1.0, GZ + 2.25, MI["tv"])
proc("media_tv", (tm.x, tm.y + 0.025), (0, 1), (2.2, 0.05, 1.25), "media", "decor", z=GZ + 1.0)
place("sofa_03", (tm.x, tm.y + 3.6), (tm.x, tm.y), "media", recolor=(0.16, 0.16, 0.17))
place("Ottoman_01", (tm.x, tm.y + 2.3), ("dir", 0, -1), "media", kind="table")
rug("media_rug", (tm.x, tm.y + 2.8), 3.4, 2.6, MI["rug_jute"])
downlights("media", *rect_px(910, 407, 970, 488), G_TOP, 2, 2, 25)

# ---- entry hall: console + plant by the stair
place("potted_plant_01", against(hw(895, 475), (-1, 0), 0.65), ("dir", -1, 0), "entry", kind="decor")
downlights("entry", *rect_px(845, 420, 905, 495), G_TOP, 1, 2)

# ---- outdoor entertaining (plan px 608-686, 362-585): dining under the cupola, lounge facing the pool
od = Vector(hw(647, 398))
place("dining_table", od, ("dir", 0, 1), "outdoor", kind="table")
for dx in (-0.7, 0.0, 0.7):
    for sy in (-1, 1):
        place("gallinera_chair", (od.x + dx, od.y + sy * 0.92), (od.x + dx, od.y), "outdoor")
pendant("outdoor_pendant", od, G_TOP + 1.2, r=0.4, drop=1.6)
ol = Vector(hw(655, 505))
rug("outdoor_rug", (ol.x - 0.8, ol.y), 2.6, 3.4, MI["rug_jute"])
place("sofa_02", (ol.x + 0.6, ol.y), ("dir", -1, 0), "outdoor", recolor=(0.82, 0.8, 0.76))
place("CoffeeTable_01", (ol.x - 0.75, ol.y), ("dir", -1, 0), "outdoor", kind="table")
for sy in (-1, 1):
    place("mid_century_lounge_chair", (ol.x - 0.8, ol.y + sy * 1.55), (ol.x - 0.75, ol.y), "outdoor")
place("planter_box_03", hw(612, 440), ("dir", -1, 0), "outdoor", kind="decor")
place("potted_plant_01", hw(612, 575), ("dir", -1, 0), "outdoor", kind="decor")

# ================================================================== UPPER (upper drawing px)
UZ = U_FFL
# ---- master (upper px 1057-1120, 517-600): headboard on the east wall, bed faces west to the balcony + water
mh = Vector(U(1119, 556))
bed("master_bed", mh, (-1, 0), "master", ("boucle", "linen", "linen_sand", "throw_tan"))
place("Ottoman_01", (mh.x - 2.65, mh.y), ("dir", -1, 0), "master", kind="table", level="upper", recolor=(0.8, 0.77, 0.72))
place("ArmChair_01", U(1068, 590), U(1090, 556), "master", level="upper", recolor=LINEN)
rug("master_rug", (mh.x - 1.5, mh.y), 2.8, 3.6, MI["rug_jute"], "upper")
downlights("master", *rect_px(1059, 519, 1118, 598, U), U_TOP, 2, 2, 30)
# ---- bedroom 2 (upper px 1100-1167, 447-497): headboard east wall, faces west
b2 = Vector(U(1134, 492))
bed("bed2", b2, (0, 1), "bed2", ("velvet", "linen_grey", "linen", "throw"))
downlights("bed2", *rect_px(1102, 449, 1165, 495, U), U_TOP, 1, 1, 30)
# ---- bedroom 3 (upper px 1120-1192, 517-565): headboard on the west wall, faces east
b3 = Vector(U(1124, 548))
bed("bed3", b3, (1, 0), "bed3", ("boucle", "linen_sand", "linen_grey", "throw"))
downlights("bed3", *rect_px(1122, 519, 1170, 562, U), U_TOP, 1, 1, 30)
# ---- bedroom 4 (upper px 1245-1322, 520-568): headboard on the south wall, faces north
b4 = Vector(U(1287, 567))
bed("bed4", b4, (0, 1), "bed4", ("velvet", "linen", "linen_grey", "throw_tan"))
downlights("bed4", *rect_px(1247, 522, 1320, 566, U), U_TOP, 1, 1, 30)
# ---- upper living (upper px 1250-1320, 450-515): sofa backs onto the void, faces east to the balcony
ul = Vector(U(1285, 482))
rug("upper_living_rug", ul, 3.0, 3.4, MI["rug_bw"], "upper")
place("modern_coffee_table_02", ul, ("dir", 1, 0), "upper_living", kind="table", level="upper")
place("sofa_02", (ul.x - 1.45, ul.y), ("dir", 1, 0), "upper_living", level="upper", recolor=LINEN)
for sy in (-1, 1):
    place("modern_arm_chair_01", (ul.x + 0.2, ul.y + sy * 1.55), (ul.x, ul.y), "upper_living", level="upper", recolor=(0.75, 0.72, 0.66))
downlights("upper_living", *rect_px(1250, 450, 1320, 515, U), U_TOP, 2, 2, 30)
# ---- master balcony (ground px 614-704, 433-525): two lounge chairs facing the water (west)
mb = Vector(hw(640, 479))
for sy in (-1, 1):
    place("mid_century_lounge_chair", (mb.x, mb.y + sy * 0.9), ("dir", -1, 0), "master_balcony", level="upper", z=U_FFL)
place("side_table_01", (mb.x, mb.y), ("dir", -1, 0), "master_balcony", kind="decor", level="upper", z=U_FFL)
place("potted_plant_02", hw(618, 437), ("dir", -1, 0), "master_balcony", kind="decor", level="upper", z=U_FFL)

json.dump(dict(placed=PLACED, walls=WALLS, openings=OPENINGS), open(os.path.join(HERE, "layout.json"), "w"), indent=1)
print("INTERIOR", len(PLACED), "pieces")
