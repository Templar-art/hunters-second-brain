"""18 Maryland landscape: palms, trees, hedge foliage, mown lawn, canal water + the far bank. exec'd by build.py.

tree(name, x, y, r, h)  -> instance of a Poly Haven broadleaf (island_tree_01 / 02, CC0) scaled to height h
palm(name, x, y, h)     -> procedural queen palm: curved ringed trunk, crownshaft, 14 arching fronds of leaflets
Lawn: instanced grass clumps (blades 4-7 cm, mown) scattered on the lot lawn; hedges get leaf-cluster instances.
"""
import random

RNG = random.Random(18)
_PROTO = {}


def _hide(o):
    for c in o.users_collection:
        c.objects.unlink(o)
    col("_protos").objects.link(o)


def _proto_col():
    """prototypes stay renderable (excluded collections don't feed particle instances); bury_protos() moves them
    500 m under the ground once everything is placed"""
    return col("_protos")


def bury_protos():
    for o in col("_protos").objects:
        o.location.z -= 500


def leaf_mat(name, rgb, var):
    m = textured(mat(name, rgb, 0.55), "noise", 8, 0.1, ramp=(tuple(c * (1 - var) for c in rgb), tuple(min(1, c * (1 + var)) for c in rgb)))
    b = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    b.inputs["Subsurface Weight"].default_value = 0.0
    try:
        b.inputs["Transmission Weight"].default_value = 0.0
        b.inputs["Sheen Weight"].default_value = 0.2
    except KeyError:
        pass
    # thin leaves: let some light through (translucency mix)
    nt = m.node_tree; out = next(n for n in nt.nodes if n.type == "OUTPUT_MATERIAL")
    tl = nt.nodes.new("ShaderNodeBsdfTranslucent"); tl.inputs["Color"].default_value = (rgb[0] * 1.6, rgb[1] * 1.6, rgb[2] * 0.8, 1)
    mx = nt.nodes.new("ShaderNodeMixShader"); mx.inputs[0].default_value = 0.25
    nt.links.new(b.outputs[0], mx.inputs[1]); nt.links.new(tl.outputs[0], mx.inputs[2]); nt.links.new(mx.outputs[0], out.inputs["Surface"])
    return m


ML = dict(
    frond=leaf_mat("Palm_frond", (0.09, 0.2, 0.04), 0.35),
    palm_trunk=textured(mat("Palm_trunk_grey", (0.25, 0.23, 0.2), 0.9), "boards", 9.0, 0.6, ramp=((0.15, 0.14, 0.12), (0.32, 0.3, 0.26))),
    crownshaft=mat("Palm_crownshaft", (0.25, 0.3, 0.12), 0.6),
    hedge_leaf=leaf_mat("Hedge_leaf_lillypilly", (0.06, 0.16, 0.035), 0.4),
    hedge_new=leaf_mat("Hedge_leaf_new_growth", (0.35, 0.18, 0.08), 0.2),
    grass=leaf_mat("Lawn_blade", (0.09, 0.22, 0.04), 0.3),
)


def palm_proto(h, seed):
    key = ("palm", round(h), seed)
    if key in _PROTO:
        return _PROTO[key]
    r = random.Random(seed); bm_ = bmesh.new()
    # trunk: 28 rings with a gentle lean curve, radius 0.22 -> 0.16
    lean = Vector((r.uniform(-1, 1), r.uniform(-1, 1), 0)).normalized() * r.uniform(0.3, 0.9)
    rings = []
    for i in range(29):
        t = i / 28; c = lean * (t ** 2) + Vector((0, 0, h * t)); rad = 0.22 - 0.06 * t
        ring = [bm_.verts.new(c + Vector((math.cos(a) * rad, math.sin(a) * rad, 0))) for a in (k / 12 * 2 * math.pi for k in range(12))]
        rings.append(ring)
    for a_, b_ in zip(rings, rings[1:]):
        for k in range(12):
            bm_.faces.new((a_[k], a_[(k + 1) % 12], b_[(k + 1) % 12], b_[k]))
    trunk = bmesh.new(); trunk_me = bpy.data.meshes.new("palm_trunk"); bm_.to_mesh(trunk_me); bm_.free()
    top = lean + Vector((0, 0, h))
    # crownshaft
    bpy.ops.mesh.primitive_cone_add(vertices=12, radius1=0.2, radius2=0.12, depth=1.1, location=top + Vector((0, 0, 0.5)))
    cs = bpy.context.active_object
    from mathutils import Matrix
    cs.data.transform(Matrix.Translation(cs.location)); cs.location = (0, 0, 0)
    # fronds
    fb = bmesh.new(); tipz = top.z + 1.0
    nf = 14
    for f in range(nf):
        az = f / nf * 2 * math.pi + r.uniform(-0.15, 0.15)
        up = r.uniform(0.2, 0.9) if f % 3 else r.uniform(0.9, 1.4)          # some fronds stand, most arch
        L = r.uniform(3.2, 4.2); d = Vector((math.cos(az), math.sin(az), 0))
        sd = Vector((-d.y, d.x, 0))
        prev = None
        for i in range(40):
            s = i / 39
            p = Vector((top.x, top.y, tipz)) + d * (L * s) + Vector((0, 0, L * (up * s - 0.9 * s * s)))
            ll = 0.75 * math.sin(math.pi * min(1, s * 1.1 + 0.05)) * (1 - 0.4 * s)
            for side in (-1, 1):                                              # leaflet: drooping blade
                droop = Vector((0, 0, -ll * 0.55))
                q0 = p; q1 = p + sd * side * ll * 0.95 + droop + d * 0.12
                w = 0.028
                v = [fb.verts.new(q0 - d * w), fb.verts.new(q0 + d * w), fb.verts.new(q1 + d * w * 0.3), fb.verts.new(q1 - d * w * 0.3)]
                fb.faces.new(v)
            prev = p
    fme = bpy.data.meshes.new("palm_fronds"); fb.to_mesh(fme); fb.free()
    o = bpy.data.objects.new(f"PROTO_palm_{round(h)}_{seed}", trunk_me); col("_protos").objects.link(o)
    o.data.materials.append(ML["palm_trunk"])
    fo = bpy.data.objects.new(o.name + "_fronds", fme); col("_protos").objects.link(fo); fo.data.materials.append(ML["frond"])
    _hide(cs); cs.name = o.name + "_shaft"; cs.data.materials.append(ML["crownshaft"])
    _PROTO[key] = (o, fo, cs)
    return _PROTO[key]


def palm(name, x, y, h):
    _proto_col()
    parts = palm_proto(h, RNG.randint(0, 2))
    rot = RNG.uniform(0, 2 * math.pi)
    for p in parts:
        o = bpy.data.objects.new(name + "_" + p.name.split("_")[-1], p.data); col("landscape").objects.link(o)
        o.location = (x, y, 0); o.rotation_euler = (0, 0, rot)


def tree_proto(kind):
    if kind in _PROTO:
        return _PROTO[kind]
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=os.path.join(HERE, "assets", kind, kind + ".gltf"))
    new = [o for o in bpy.data.objects if o not in before]; me = next(o for o in new if o.type == "MESH")
    mw = me.matrix_world.copy(); me.parent = None; me.data.transform(mw); me.matrix_world.identity()
    for o in new:
        if o is not me:
            bpy.data.objects.remove(o)
    zs = [v.co.z for v in me.data.vertices]; h0 = max(zs) - min(zs)
    _hide(me); me.name = "PROTO_" + kind
    _PROTO[kind] = (me, h0)
    return _PROTO[kind]


def tree(name, x, y, r, h):
    _proto_col()
    kind = "island_tree_01" if h >= 8 or RNG.random() < 0.5 else "island_tree_02"
    src, h0 = tree_proto(kind)
    o = bpy.data.objects.new(name, src.data); col("landscape").objects.link(o)
    s = h / h0 * RNG.uniform(0.9, 1.1); o.scale = (s * RNG.uniform(0.9, 1.15), s * RNG.uniform(0.9, 1.15), s)
    o.location = (x, y, 0); o.rotation_euler = (0, 0, RNG.uniform(0, 2 * math.pi))


def leaf_cluster():
    if "leaf" in _PROTO:
        return _PROTO["leaf"]
    bm_ = bmesh.new(); r = random.Random(3)
    for k in range(9):
        c = Vector((r.uniform(-0.06, 0.06), r.uniform(-0.06, 0.06), r.uniform(-0.04, 0.04)))
        a = r.uniform(0, 2 * math.pi); u = Vector((math.cos(a), math.sin(a), r.uniform(-0.3, 0.6))).normalized() * 0.055
        w = u.cross(Vector((0, 0, 1))).normalized() * 0.022
        v = [bm_.verts.new(c - w), bm_.verts.new(c + u * 0.5 + w * 1.2), bm_.verts.new(c + u), bm_.verts.new(c + u * 0.5 - w * 1.2)]
        bm_.faces.new(v)
    me = bpy.data.meshes.new("leaf_cluster"); bm_.to_mesh(me); bm_.free()
    o = bpy.data.objects.new("PROTO_leaf_cluster", me); col("_protos").objects.link(o); o.data.materials.append(ML["hedge_leaf"])
    _PROTO["leaf"] = o
    return o


def grass_clump():
    if "grass" in _PROTO:
        return _PROTO["grass"]
    bm_ = bmesh.new(); r = random.Random(5)
    for k in range(110):
        c = Vector((r.uniform(-0.2, 0.2), r.uniform(-0.2, 0.2), 0)); hgt = r.uniform(0.035, 0.07)
        a = r.uniform(0, 2 * math.pi); bend = Vector((math.cos(a), math.sin(a), 0)) * hgt * r.uniform(0.15, 0.45)
        w = Vector((-math.sin(a), math.cos(a), 0)) * 0.0025
        p0, p1, p2 = c, c + bend * 0.3 + Vector((0, 0, hgt * 0.55)), c + bend + Vector((0, 0, hgt))
        v = [bm_.verts.new(p0 - w), bm_.verts.new(p0 + w), bm_.verts.new(p1 + w * 0.7), bm_.verts.new(p1 - w * 0.7)]
        bm_.faces.new(v); t = bm_.verts.new(p2); bm_.faces.new((v[3], v[2], t))
    me = bpy.data.meshes.new("grass_clump"); bm_.to_mesh(me); bm_.free()
    from mathutils import Matrix
    me.transform(Matrix.Rotation(math.radians(90), 4, "Y"))        # hair instances align local +X with the hair (up)
    o = bpy.data.objects.new("PROTO_grass_clump", me); col("_protos").objects.link(o); o.data.materials.append(ML["grass"])
    _PROTO["grass"] = o
    return o


def scatter(target, inst, count, size, size_rand=0.3, name="scatter", seed=1):
    """instance `inst` over target's faces (hair particles rendered as objects, random rotation)"""
    ps = target.modifiers.new(name, "PARTICLE_SYSTEM"); st = ps.particle_system.settings
    st.type = "HAIR"; st.count = count; st.hair_length = 0.1; st.emit_from = "FACE"; st.use_even_distribution = True
    st.render_type = "OBJECT"; st.instance_object = inst; st.particle_size = size / 0.1; st.size_random = size_rand   # hair instances come out at 0.1x
    st.use_rotations = True; st.rotation_mode = "NOR"; st.phase_factor_random = 2.0
    st.rotation_factor_random = 0.15 if "grass" in name else 1.0
    ps.particle_system.seed = seed
    st.use_advanced_hair = True
    return ps


def plant_hedges():
    _proto_col(); leaf = leaf_cluster()
    for o in list(bpy.data.objects):
        if o.name.startswith(("hedge_", "front_hedge")) and o.type == "MESH":
            area = sum(p.area for p in o.data.polygons)
            o.modifiers.new("lumpy", "DISPLACE").strength = 0.12
            o.modifiers["lumpy"].texture = bpy.data.textures.new(o.name + "_n", "CLOUDS"); o.modifiers["lumpy"].texture.noise_scale = 0.6
            sub = o.modifiers.new("sub", "SUBSURF"); o.modifiers.move(len(o.modifiers) - 1, 0); sub.levels = 3; sub.render_levels = 3
            scatter(o, leaf, int(area * 520), 1.6, 0.4, "hedge_leaves", seed=len(o.name))


def lawn_grass(poly, keep=lambda x, y: True, cell=0.5):
    """grass emitter = the lawn polygon cut into cells, dropping every cell `keep` rejects (paving, house, pool)"""
    _proto_col(); g = grass_clump()
    xs = [p[0] for p in poly]; ys = [p[1] for p in poly]
    bm_ = bmesh.new(); x = min(xs)
    while x < max(xs):
        y = min(ys)
        while y < max(ys):
            cx, cy = x + cell / 2, y + cell / 2
            if inside(poly, (cx, cy)) and keep(cx, cy):
                vs = [bm_.verts.new((a, b, 0.001)) for a, b in ((x, y), (x + cell, y), (x + cell, y + cell), (x, y + cell))]
                bm_.faces.new(vs)
            y += cell
        x += cell
    me = bpy.data.meshes.new("lawn_grass"); bm_.to_mesh(me); bm_.free()
    o = bpy.data.objects.new("lawn_grass_emitter", me); col("site").objects.link(o)
    o.data.materials.append(M["lawn"])
    area = sum(p.area for p in me.polygons)
    scatter(o, g, int(area * 14), 1.0, 0.35, "grass", seed=7)
    o.hide_render = False
    return o


def water_material():
    m = M["water"]; nt = m.node_tree; b = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    b.inputs["Base Color"].default_value = (0.012, 0.035, 0.035, 1); b.inputs["Roughness"].default_value = 0.02
    b.inputs["IOR"].default_value = 1.33
    tc = nt.nodes.new("ShaderNodeTexCoord"); mp = nt.nodes.new("ShaderNodeMapping"); mp.inputs["Scale"].default_value = (1.0, 0.35, 1.0)
    n1 = nt.nodes.new("ShaderNodeTexNoise"); n1.inputs["Scale"].default_value = 0.9; n1.inputs["Detail"].default_value = 10
    n2 = nt.nodes.new("ShaderNodeTexWave"); n2.inputs["Scale"].default_value = 0.6; n2.inputs["Distortion"].default_value = 6
    mx = nt.nodes.new("ShaderNodeMath"); mx.operation = "ADD"
    bu = nt.nodes.new("ShaderNodeBump"); bu.inputs["Strength"].default_value = 0.14; bu.inputs["Distance"].default_value = 0.05
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"]); nt.links.new(mp.outputs[0], n1.inputs["Vector"]); nt.links.new(mp.outputs[0], n2.inputs["Vector"])
    nt.links.new(n1.outputs["Fac"], mx.inputs[0]); nt.links.new(n2.outputs["Fac"], mx.inputs[1])
    nt.links.new(mx.outputs[0], bu.inputs["Height"]); nt.links.new(bu.outputs["Normal"], b.inputs["Normal"])


def far_bank():
    """Nerang River's west bank ~120 m across: low land, a tree line, a few houses behind"""
    prism("far_bank", [(-400, -140), (-125, -140), (-118, 170), (-400, 170)], -0.6, 0.4, M["lawn"], "far_bank")
    prism("far_bank_wall", [(-127, -140), (-123, -140), (-116, 170), (-120, 170)], -0.6, 0.5, M["sand"], "far_bank")
    for i in range(46):
        y = -130 + i * 6.6 + RNG.uniform(-2, 2); x = -128 - RNG.uniform(0, 14) + (y + 140) * 0.023
        tree(f"far_tree_{i}", x, y, 4, RNG.uniform(7, 14))
        if i % 5 == 0:
            palm(f"far_palm_{i}", x + 3, y + 2, RNG.uniform(9, 14))
    for i in range(11):
        y = -120 + i * 27 + RNG.uniform(-4, 4); x = -150 - RNG.uniform(0, 12)
        box(f"far_house_{i}", x - 9, y - 7, x + 9, y + 7, 0.4, 7.5, M["neigh"], "far_bank")
        hip(f"far_house_{i}_roof", x - 9, y - 7, x + 9, y + 7, 7.5, collection="far_bank", material=M["roof"] if i % 3 else M["terracotta"])


def shrub(name, x, y, r, h):
    """garden-bed shrub: lumpy sphere carpeted in leaf clusters"""
    _proto_col()
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3, radius=r, location=(x, y, h * 0.55))
    o = bpy.context.active_object; o.name = name; o.scale = (1, 1, h / (2 * r) + 0.2)
    for c in o.users_collection:
        c.objects.unlink(o)
    col("landscape").objects.link(o); o.data.materials.append(ML["hedge_leaf"])
    d = o.modifiers.new("lumpy", "DISPLACE"); t = bpy.data.textures.new(name + "_n", "CLOUDS"); t.noise_scale = r * 0.5
    d.texture = t; d.strength = r * 0.3
    scatter(o, leaf_cluster(), int(4 * math.pi * r * r * 220), 1.2, 0.4, "shrub_leaves", seed=hash(name) % 999)


BURB = [mat("Render_burb_cream", (0.62, 0.58, 0.5), 0.8), mat("Render_burb_grey", (0.45, 0.45, 0.44), 0.8),
        mat("Render_burb_sand", (0.55, 0.48, 0.38), 0.8)]


def horizon():
    """suburb out to ~650 m (haze hides the edge; shots.cull drops what a move cannot see): dark far-grass ground with a scatter of tree canopies, so no frame ends in a void"""
    prism("suburb_east", [(230, -900), (900, -900), (900, 1200), (230, 1200)], -0.3, -0.1, M["lawn_far"], "far_bank")
    prism("suburb_ns", [(-118, -900), (230, -900), (230, -60), (-118, -60)], -0.3, -0.1, M["lawn_far"], "far_bank")
    prism("suburb_n", [(-118, 110), (230, 110), (230, 1200), (-118, 1200)], -0.3, -0.1, M["lawn_far"], "far_bank")
    prism("suburb_west", [(-900, -900), (-400, -900), (-400, 1200), (-900, 1200)], -0.3, 0.3, M["lawn_far"], "far_bank")
    prism("river_far", [(-400, -900), (-118, -900), (-118, 1200), (-400, 1200)], -0.65, -0.6, M["water"], "far_bank")
    r = random.Random(11)
    for i in range(800):
        while True:
            x, y = r.uniform(-650, 650), r.uniform(-420, 620)
            if not (-420 < x < 235 and -70 < y < 120) and not (-400 < x < -118):
                break
        tree(f"burb_tree_{i}", x, y, 4, r.uniform(9, 18))
        if i % 9 == 0:
            palm(f"burb_palm_{i}", x + 4, y + 3, r.uniform(9, 15))
    for i in range(130):
        while True:
            x, y = r.uniform(-650, 650), r.uniform(-420, 620)
            if not (-420 < x < 235 and -70 < y < 120) and not (-400 < x < -118):
                break
        w, d = r.uniform(14, 24), r.uniform(10, 18)
        box(f"burb_house_{i}", x - w / 2, y - d / 2, x + w / 2, y + d / 2, 0, 6.5, BURB[i % 3], "far_bank")
        hip(f"burb_house_{i}_roof", x - w / 2, y - d / 2, x + w / 2, y + d / 2, 6.5, collection="far_bank", material=M["roof"] if i % 3 else M["terracotta"])
